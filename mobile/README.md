# Costa Workforce Manager (CWM) — App Android (Flutter)

App para supervisores/funcionários marcarem presença lendo o QR Code do cartão de funcionário.

## 1. O que já está pronto

Todo o código Dart em `lib/`:
- `main.dart` — arranque da app, decide login vs. ecrã principal
- `screens/login_screen.dart` — login
- `screens/scanner_screen.dart` — **leitor de QR Code** (câmara) com check-in/check-out automático
- `screens/history_screen.dart` — histórico de presenças
- `screens/profile_screen.dart` — perfil e logout
- `services/auth_service.dart` — login, tokens JWT, sessão guardada no telemóvel
- `services/api_service.dart` — chamadas à API Django (com renovação automática de token)
- `services/location_service.dart` — GPS no momento da marcação
- `models/` — estruturas de dados (utilizador, registo de presença)

## 2. O que falta gerar (pastas nativas)

Eu não tenho o Flutter SDK disponível neste ambiente para correr `flutter create`, que gera as pastas nativas `android/` e `ios/`. Tens de gerar isso no teu computador — é automático, leva 1 minuto:

```bash
# Pré-requisito: Flutter SDK instalado (https://docs.flutter.dev/get-started/install)
flutter --version   # confirma que está instalado

# Dentro da pasta mobile/ que te dei:
cd mobile
flutter create . --org com.costa.cwm --project-name cwm_mobile
```

Isto vai gerar `android/`, `ios/`, `test/`, etc. **sem apagar** os ficheiros `lib/` e `pubspec.yaml` que já tens.

## 3. Instalar dependências e correr

```bash
flutter pub get
flutter run
```

Escolhe o emulador Android ou liga o teu telemóvel por USB com a depuração ativada.

## 4. Ligar à tua API (backend)

Edita `lib/config/api_config.dart`:

- **Emulador Android** → mantém `http://10.0.2.2:8000/api` (é como o emulador "vê" o `localhost` do teu PC)
- **Telemóvel físico na mesma rede Wi-Fi** → usa o IP local do teu PC, ex: `http://192.168.1.50:8000/api`
- **Servidor em produção** → usa o domínio, ex: `https://api.costaworkforce.com/api`

Garante que o backend Django está a correr (`python manage.py runserver 0.0.0.0:8000` se for um telemóvel físico).

## 5. Permissões necessárias (após `flutter create`)

### Android — `android/app/src/main/AndroidManifest.xml`
Adiciona dentro de `<manifest>`, antes de `<application>`:

```xml
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
<uses-permission android:name="android.permission.INTERNET"/>
```

### iOS — `ios/Runner/Info.plist`
Adiciona dentro de `<dict>`:

```xml
<key>NSCameraUsageDescription</key>
<string>Precisamos da câmara para ler o QR Code do cartão de funcionário</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>Precisamos da localização para registar onde a presença foi marcada</string>
```

## 6. Testar com os dados de demonstração

Se já correste `python manage.py seed_demo` no backend, usa:
- Utilizador: `gestor` / Palavra-passe: `Gestor#2026`

No painel `/admin/` do Django consegues ver o QR Code gerado de cada funcionário demo (Ana Costa, Bruno Fernandes, Carla Sousa) — imprime ou mostra esse QR Code no ecrã de outro telemóvel/monitor para testar a leitura.

## 7. Gerar o APK final

```bash
flutter build apk --release
```

O ficheiro fica em `build/app/outputs/flutter-apk/app-release.apk`, pronto a instalar em qualquer Android.

## 8. Próximas fases já planeadas

- Modo **offline** com sincronização automática quando houver internet
- **Reconhecimento facial** como segunda verificação no scanner
- Notificações push (falta/atraso)
- Pedido de férias e licenças pelo próprio funcionário
