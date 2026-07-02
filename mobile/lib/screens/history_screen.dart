import 'package:flutter/material.dart';
import '../models/attendance_record.dart';
import '../services/api_service.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  late Future<List<AttendanceRecord>> _future;

  @override
  void initState() {
    super.initState();
    _future = ApiService.getAttendanceHistory();
  }

  Future<void> _refresh() async {
    setState(() => _future = ApiService.getAttendanceHistory());
    await _future;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Histórico de Presenças')),
      body: RefreshIndicator(
        onRefresh: _refresh,
        child: FutureBuilder<List<AttendanceRecord>>(
          future: _future,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snapshot.hasError) {
              return ListView(
                children: [
                  const SizedBox(height: 80),
                  Center(child: Text('Erro ao carregar: ${snapshot.error}')),
                ],
              );
            }
            final records = snapshot.data ?? [];
            if (records.isEmpty) {
              return ListView(
                children: const [
                  SizedBox(height: 80),
                  Center(child: Text('Ainda não há registos de presença.')),
                ],
              );
            }
            return ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: records.length,
              itemBuilder: (context, index) => _RecordCard(record: records[index]),
            );
          },
        ),
      ),
    );
  }
}

class _RecordCard extends StatelessWidget {
  final AttendanceRecord record;
  const _RecordCard({required this.record});

  @override
  Widget build(BuildContext context) {
    const navy = Color(0xFF0A1F44);
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(color: navy.withOpacity(0.08), shape: BoxShape.circle),
              child: const Icon(Icons.calendar_today, color: navy, size: 20),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(record.date, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                  const SizedBox(height: 4),
                  Text(
                    'Entrada: ${_fmt(record.checkIn)}   •   Saída: ${_fmt(record.checkOut)}',
                    style: const TextStyle(color: Colors.black54, fontSize: 13),
                  ),
                  if (record.workedHours != null)
                    Text('${record.workedHours} horas trabalhadas', style: const TextStyle(fontSize: 12)),
                ],
              ),
            ),
            if (record.isLate)
              const Icon(Icons.schedule, color: Colors.orange)
            else
              const Icon(Icons.check_circle, color: Colors.green),
          ],
        ),
      ),
    );
  }

  String _fmt(String? iso) {
    if (iso == null) return '--:--';
    try {
      final dt = DateTime.parse(iso).toLocal();
      return '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
    } catch (_) {
      return '--:--';
    }
  }
}
