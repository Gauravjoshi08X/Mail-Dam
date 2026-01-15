import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';
import 'dart:developer' as developer;
import 'dart:convert';

void sendStat() async {
    try {
      final response = await http.get(Uri.parse("http://localhost:5000/auth/google"));
      final jsonData = jsonDecode(response.body);
      final authURL = Uri.parse(jsonData['auth_url']);
      if (await canLaunchUrl(authURL)) {
        await launchUrl(authURL, mode: LaunchMode.externalApplication);
      }
    } catch (e) {
      developer.log('Error: $e');
      rethrow;
    }
}