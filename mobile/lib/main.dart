import 'package:flutter/material.dart';
import 'services/auth_service.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const CwmApp());
}

class CwmApp extends StatelessWidget {
  const CwmApp({super.key});

  @override
  Widget build(BuildContext context) {
    const navy = Color(0xFF0A1F44);
    const gold = Color(0xFFC9A646);

    return MaterialApp(
      title: 'Costa Workforce Manager',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: navy, primary: navy, secondary: gold),
        appBarTheme: const AppBarTheme(
          backgroundColor: navy,
          foregroundColor: Colors.white,
          elevation: 0,
        ),
        scaffoldBackgroundColor: const Color(0xFFF5F6FA),
      ),
      home: const _StartupGate(),
    );
  }
}

/// Decide se mostra o ecrã de login ou o ecrã principal,
/// consoante exista uma sessão guardada no telemóvel.
class _StartupGate extends StatelessWidget {
  const _StartupGate();

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: AuthService.isLoggedIn(),
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }
        return (snapshot.data ?? false) ? const HomeScreen() : const LoginScreen();
      },
    );
  }
}
