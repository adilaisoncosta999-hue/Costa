class AttendanceRecord {
  final String id;
  final String employeeName;
  final String date;
  final String? checkIn;
  final String? checkOut;
  final bool isLate;
  final int lateMinutes;
  final bool leftEarly;
  final double? workedHours;

  AttendanceRecord({
    required this.id,
    required this.employeeName,
    required this.date,
    this.checkIn,
    this.checkOut,
    this.isLate = false,
    this.lateMinutes = 0,
    this.leftEarly = false,
    this.workedHours,
  });

  factory AttendanceRecord.fromJson(Map<String, dynamic> json) {
    return AttendanceRecord(
      id: json['id'].toString(),
      employeeName: json['employee_name'] ?? '',
      date: json['date'] ?? '',
      checkIn: json['check_in'],
      checkOut: json['check_out'],
      isLate: json['is_late'] ?? false,
      lateMinutes: json['late_minutes'] ?? 0,
      leftEarly: json['left_early'] ?? false,
      workedHours: json['worked_hours'] != null
          ? double.tryParse(json['worked_hours'].toString())
          : null,
    );
  }
}

/// Resultado devolvido pelo endpoint /attendance/scan/
class ScanResult {
  final String action; // 'check_in' ou 'check_out'
  final String employeeName;
  final String employeeNumber;
  final String time;
  final bool isLate;
  final int lateMinutes;
  final bool leftEarly;

  ScanResult({
    required this.action,
    required this.employeeName,
    required this.employeeNumber,
    required this.time,
    this.isLate = false,
    this.lateMinutes = 0,
    this.leftEarly = false,
  });

  factory ScanResult.fromJson(Map<String, dynamic> json) {
    return ScanResult(
      action: json['action'] ?? '',
      employeeName: json['employee'] ?? '',
      employeeNumber: json['employee_number'] ?? '',
      time: json['time'] ?? '',
      isLate: json['is_late'] ?? false,
      lateMinutes: json['late_minutes'] ?? 0,
      leftEarly: json['left_early'] ?? false,
    );
  }

  bool get isCheckIn => action == 'check_in';
}
