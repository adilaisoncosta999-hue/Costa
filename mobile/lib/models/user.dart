class AppUser {
  final String id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final String role;
  final String? companyId;

  AppUser({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.role,
    this.companyId,
  });

  String get fullName => '$firstName $lastName'.trim().isEmpty ? username : '$firstName $lastName';

  bool get canManage => role == 'super_admin' || role == 'company_admin' || role == 'hr';
  bool get isSupervisor => role == 'supervisor' || canManage;

  factory AppUser.fromJson(Map<String, dynamic> json) {
    return AppUser(
      id: json['id'].toString(),
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      role: json['role'] ?? 'employee',
      companyId: json['company']?.toString(),
    );
  }
}
