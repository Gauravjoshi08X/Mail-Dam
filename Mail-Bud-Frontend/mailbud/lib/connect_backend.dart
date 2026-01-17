import 'dart:io';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;

Future<void> openAuth() async {
  final uri = Uri.parse(
    "https://9xkmd6fc-5000.inc1.devtunnels.ms/auth/google"
  );

  await launchUrl(
    uri,
    mode: LaunchMode.externalApplication,
  );
}

Future<void> sendData() async {
  final url=Uri.parse("https://9xkmd6fc-5000.inc1.devtunnels.ms/auth");
  Map<String, dynamic> payload={"name": "gaurav"};
  Map<String, String> header={"Content-Type": "application/json"};
  http.post(url, headers: header, body:  payload);
}

void main() {
  sendData();
}