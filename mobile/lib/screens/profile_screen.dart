import 'package:flutter/material.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import 'login_screen.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  AppUser? _user;

  @override
  void initState() {
    super.initState();
    _loadUser();
  }

  Future<void> _loadUser() async {
    final user = await AuthService.getCurrentUser();
    setState(() => _user = user);
  }

  Future<void> _logout() async {
    await AuthService.logout();
    if (!mounted) return;
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const LoginScreen()),
      (route) => false,
    );
  }

  static const _roleLabels = {
    'super_admin': 'Super Administrador',
    'company_admin': 'Administrador da Empresa',
    'hr': 'Recursos Humanos',
    'supervisor': 'Supervisor',
    'employee': 'Funcionário',
  };

  @override
  Widget build(BuildContext context) {
    const navy = Color(0xFF0A1F44);
    const gold = Color(0xFFC9A646);

    return Scaffold(
      appBar: AppBar(title: const Text('Perfil')),
      body: _user == null
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(20),
              children: [
                CircleAvatar(
                  radius: 42,
                  backgroundColor: navy,
                  child: Text(
                    _user!.fullName.isNotEmpty ? _user!.fullName[0].toUpperCase() : '?',
                    style: const TextStyle(color: gold, fontSize: 32, fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(height: 16),
                Center(
                  child: Text(_user!.fullName, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                ),
                Center(
                  child: Text(
                    _roleLabels[_user!.role] ?? _user!.role,
                    style: const TextStyle(color: Colors.black54),
                  ),
                ),
                const SizedBox(height: 28),
                _InfoTile(icon: Icons.alternate_email, label: 'E-mail', value: _user!.email),
                _InfoTile(icon: Icons.person_outline, label: 'Utilizador', value: _user!.username),
                const SizedBox(height: 28),
                SizedBox(
                  width: double.infinity,
                  height: 48,
                  child: OutlinedButton.icon(
                    onPressed: _logout,
                    icon: const Icon(Icons.logout, color: Colors.red),
                    label: const Text('Terminar sessão', style: TextStyle(color: Colors.red)),
                    style: OutlinedButton.styleFrom(side: const BorderSide(color: Colors.red)),
                  ),
                ),
              ],
            ),
    );
  }
}

class _InfoTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _InfoTile({required this.icon, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon, color: const Color(0xFF0A1F44)),
      title: Text(label, style: const TextStyle(fontSize: 12, color: Colors.black54)),
      subtitle: Text(value.isEmpty ? '-' : value, style: const TextStyle(fontSize: 15)),
    );
  }
}
