import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../models/attendance_record.dart';
import '../services/api_service.dart';
import '../services/location_service.dart';

class ScannerScreen extends StatefulWidget {
  const ScannerScreen({super.key});

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  final MobileScannerController _controller = MobileScannerController();
  bool _processing = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _handleDetect(BarcodeCapture capture) async {
    if (_processing) return;
    final barcode = capture.barcodes.firstOrNull;
    final rawValue = barcode?.rawValue;
    if (rawValue == null) return;

    setState(() => _processing = true);
    await _controller.stop();

    try {
      final position = await LocationService.getCurrentPosition();
      final result = await ApiService.scanQrCode(
        qrToken: rawValue,
        latitude: position?.latitude,
        longitude: position?.longitude,
      );
      if (mounted) _showResultDialog(result);
    } catch (e) {
      if (mounted) _showErrorDialog(e.toString().replaceFirst('ApiException: ', ''));
    }
  }

  void _showResultDialog(ScanResult result) {
    const navy = Color(0xFF0A1F44);
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Row(
          children: [
            Icon(
              result.isCheckIn ? Icons.login_rounded : Icons.logout_rounded,
              color: result.isCheckIn ? Colors.green : navy,
            ),
            const SizedBox(width: 8),
            Text(result.isCheckIn ? 'Entrada registada' : 'Saída registada'),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(result.employeeName, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            Text('Nº ${result.employeeNumber}'),
            const SizedBox(height: 8),
            Text('Hora: ${_formatTime(result.time)}'),
            if (result.isLate) ...[
              const SizedBox(height: 6),
              Text('⚠️ Atraso de ${result.lateMinutes} minutos', style: const TextStyle(color: Colors.orange)),
            ],
            if (result.leftEarly) ...[
              const SizedBox(height: 6),
              const Text('⚠️ Saída antecipada', style: TextStyle(color: Colors.orange)),
            ],
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              setState(() => _processing = false);
              _controller.start();
            },
            child: const Text('Ler outro QR Code'),
          ),
        ],
      ),
    );
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Row(
          children: [
            Icon(Icons.error_outline, color: Colors.red),
            SizedBox(width: 8),
            Text('Não foi possível registar'),
          ],
        ),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              setState(() => _processing = false);
              _controller.start();
            },
            child: const Text('Tentar novamente'),
          ),
        ],
      ),
    );
  }

  String _formatTime(String isoTime) {
    try {
      final dt = DateTime.parse(isoTime).toLocal();
      return '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
    } catch (_) {
      return isoTime;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Ler QR Code')),
      body: Stack(
        children: [
          MobileScanner(controller: _controller, onDetect: _handleDetect),
          // Moldura de mira
          Center(
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                border: Border.all(color: const Color(0xFFC9A646), width: 3),
                borderRadius: BorderRadius.circular(16),
              ),
            ),
          ),
          if (_processing)
            Container(
              color: Colors.black54,
              child: const Center(child: CircularProgressIndicator(color: Colors.white)),
            ),
          Positioned(
            bottom: 32,
            left: 0,
            right: 0,
            child: Text(
              'Aponta a câmara para o QR Code do cartão do funcionário',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w600,
                shadows: [Shadow(blurRadius: 6, color: Colors.black.withOpacity(0.8))],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

extension _FirstOrNull<T> on List<T> {
  T? get firstOrNull => isEmpty ? null : first;
}
