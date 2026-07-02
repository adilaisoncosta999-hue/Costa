import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/api_config.dart';
import '../models/user.dart';

class AuthException implements Exception {
  final String message;
  AuthException(this.message);
  @override
  String toString() => message;
}

class AuthService {
  static const _accessKey = 'cwm_access_token';
  static const _refreshKey = 'cwm_refresh_token';
  static const _userKey = 'cwm_user_json';

  /// Faz login na API e guarda os tokens localmente.
  static Future<AppUser> login(String username, String password) async {
    final response = await http.post(
      Uri.parse(ApiConfig.login),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );

    if (response.statusCode != 200) {
      throw AuthException('Utilizador ou palavra-passe inválidos.');
    }

    final data = jsonDecode(response.body);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_accessKey, data['access']);
    await prefs.setString(_refreshKey, data['refresh']);
    await prefs.setString(_userKey, jsonEncode(data['user']));

    return AppUser.fromJson(data['user']);
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_accessKey);
    await prefs.remove(_refreshKey);
    await prefs.remove(_userKey);
  }

  static Future<String?> getAccessToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_accessKey);
  }

  static Future<AppUser?> getCurrentUser() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_userKey);
    if (raw == null) return null;
    return AppUser.fromJson(jsonDecode(raw));
  }

  static Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null;
  }

  /// Tenta renovar o access token usando o refresh token guardado.
  static Future<bool> tryRefreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    final refresh = prefs.getString(_refreshKey);
    if (refresh == null) return false;

    final response = await http.post(
      Uri.parse(ApiConfig.refresh),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh': refresh}),
    );

    if (response.statusCode != 200) return false;
    final data = jsonDecode(response.body);
    await prefs.setString(_accessKey, data['access']);
    return true;
  }
}
