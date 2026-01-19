import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import 'dart:developer' as dev;
Future<void> openAuth() async {
  final uri = Uri.parse(
    "https://9xkmd6fc-5000.inc1.devtunnels.ms/auth/google"
  );

  await launchUrl(
    uri,
    mode: LaunchMode.externalApplication,
  );
}

Future sendData({String? project, String? senderEmail, String? subject, String? message, String? link, File? image, File? csv}) async {
  try {
    var url = Uri.parse('https://9xkmd6fc-5000.inc1.devtunnels.ms/getdata');
    await http.post(url, 
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({"project": project, 'sender': senderEmail, "subject": subject}));
  } catch (e) {
    dev.log('Error sending data: $e');
    rethrow;
  }
}
