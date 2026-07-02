import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/attendance_record.dart';
import 'auth_service.dart';

class ApiException implements Exception {
  final String message;
  ApiException(this.message);
  @override
  String toString() => message;
}

class ApiService {
  /// Envia a leitura do QR Code para registar entrada/saída.
  static Future<ScanResult> scanQrCode({
    required String qrToken,
    double? latitude,
    double? longitude,
  }) async {
    final response = await _authorizedPost(ApiConfig.attendanceScan, {
      'qr_token': qrToken,
      if (latitude != null) 'latitude': latitude,
      if (longitude != null) 'longitude': longitude,
    });

    if (response.statusCode == 200) {
      return ScanResult.fromJson(jsonDecode(response.body));
    }

    final body = jsonDecode(response.body);
    throw ApiException(body['detail'] ?? 'Não foi possível registar a presença.');
  }

  /// Histórico de presenças (opcionalmente filtrado por funcionário).
  static Future<List<AttendanceRecord>> getAttendanceHistory({String? employeeId}) async {
    var url = ApiConfig.attendanceRecords;
    if (employeeId != null) {
      url += '?employee=$employeeId';
    }
    final response = await _authorizedGet(url);

    if (response.statusCode != 200) {
      throw ApiException('Não foi possível carregar o histórico.');
    }

    final data = jsonDecode(response.body);
    final results = data is Map && data.containsKey('results') ? data['results'] : data;
    return (results as List).map((e) => AttendanceRecord.fromJson(e)).toList();
  }

  static Future<Map<String, dynamic>> getDashboardStats() async {
    final response = await _authorizedGet(ApiConfig.dashboard);
    if (response.statusCode != 200) {
      throw ApiException('Não foi possível carregar as estatísticas.');
    }
    return jsonDecode(response.body);
  }

  // --- Helpers internos com autenticação e renovação automática de token ---

  static Future<http.Response> _authorizedGet(String url) async {
    var token = await AuthService.getAccessToken();
    var response = await http.get(Uri.parse(url), headers: _headers(token));

    if (response.statusCode == 401) {
      final refreshed = await AuthService.tryRefreshToken();
      if (refreshed) {
        token = await AuthService.getAccessToken();
        response = await http.get(Uri.parse(url), headers: _headers(token));
      }
    }
    return response;
  }

  static Future<http.Response> _authorizedPost(String url, Map<String, dynamic> body) async {
    var token = await AuthService.getAccessToken();
    var response = await http.post(
      Uri.parse(url),
      headers: _headers(token),
      body: jsonEncode(body),
    );

    if (response.statusCode == 401) {
      final refreshed = await AuthService.tryRefreshToken();
      if (refreshed) {
        token = await AuthService.getAccessToken();
        response = await http.post(
          Uri.parse(url),
          headers: _headers(token),
          body: jsonEncode(body),
        );
      }
    }
    return response;
  }

  static Map<String, String> _headers(String? token) => {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };
}
