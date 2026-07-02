/// Configurações de ligação à API do Costa Workforce Manager.
///
/// IMPORTANTE:
/// - No emulador Android, "localhost" do teu computador é "10.0.2.2".
/// - Num telemóvel físico, usa o IP da tua rede local (ex: 192.168.1.50)
///   ou o domínio do servidor quando estiver publicado em produção.
class ApiConfig {
  static const String baseUrl = 'http://10.0.2.2:8000/api';

  // Endpoints
  static const String login = '$baseUrl/auth/login/';
  static const String refresh = '$baseUrl/auth/refresh/';
  static const String employees = '$baseUrl/employees/';
  static const String attendanceScan = '$baseUrl/attendance/scan/';
  static const String attendanceRecords = '$baseUrl/attendance/records/';
  static const String dashboard = '$baseUrl/attendance/dashboard/';
  static const String justifications = '$baseUrl/attendance/justifications/';
}
