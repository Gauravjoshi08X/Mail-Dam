import 'dart:convert';
// lagecy: remove me later
import 'package:http/http.dart' as http;
Future<http.Response> sendStat({String status = "Not available"}) async {
    try {
      final response = await http.post(
        Uri.parse("http://localhost:5000/api/status"),
        headers: {
          'Content-Type': 'application/json'
        },
        body: jsonEncode({"status": status})
      );
      return response;
    } catch (e) {
      print('Error: $e');
      rethrow;
    }
}

void main() async {
  await sendStat(status: "hello");
}