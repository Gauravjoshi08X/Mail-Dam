import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:developer' as dev;
import 'global_function.dart' as fn;

Future<void> openAuth() async {
  final uri = Uri.parse(
    "https://9xkmd6fc-5000.inc1.devtunnels.ms/auth/google"
  );

  await launchUrl(
    uri,
    mode: LaunchMode.externalApplication,
  );
}

Future<void> sendData({String? project, String? senderEmail, String? subject, String? message, String? link}) async {
  try {
    var url = Uri.parse('https://9xkmd6fc-5000.inc1.devtunnels.ms/getdata');
    await http.post(url, 
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({"project": project, 'sender': senderEmail, "subject": subject, "message": message, "link": link}));
  } catch (e) {
    dev.log('Error sending data: $e');
    rethrow;
  }
}

Future<void> sendFiles() async {
  var request=http.MultipartRequest("POST", Uri.parse("https://9xkmd6fc-5000.inc1.devtunnels.ms/sendfile"));
  try{
  request.files.add(await http.MultipartFile.fromPath('file', fn.GlobalFunction.csvPath));
  request.files.add(await http.MultipartFile.fromPath('file', fn.GlobalFunction.imgPath));
  var response=await request.send();
  if (response.statusCode==200){
    dev.log("Success");
  }}
  catch(e){
    dev.log(e.toString());
  }
  }

Future<void> sendMail() async {
  try{
  final uri= Uri.parse(
    "https://9xkmd6fc-5000.inc1.devtunnels.ms/sendmail"
  );
  await http.get(uri);
  }
  catch (e){
    dev.log(e.toString());
  }
}