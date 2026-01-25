import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:developer';
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

Future<void> getName(String name) async
{
  try{
    final url=Uri.parse("https://9xkmd6fc-5005.inc1.devtunnels.ms/getname");
    await http.post(url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"name": name}));
  }
  catch(e){
    log(e.toString());
    }}

Future<bool> sendName(String name) async
{
  try{
    final url=Uri.parse("https://9xkmd6fc-5005.inc1.devtunnels.ms/sendname");
    final response=(await http.post(url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"name": name})));
    final isUser=jsonDecode(response.body)["isUser"];
    if (isUser){
      return true;
    }
    else{
      return false;
    }
  } catch (e){
    log(e.toString());
    return  false;
  }
}

Future<void> sendData({String? name, String? project, String? subject, String? message, String? link}) async {
  try {
    var url = Uri.parse('https://9xkmd6fc-5005.inc1.devtunnels.ms/sendmail');
    await http.post(url, 
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({"name":name, "project": project, "subject": subject, "message": message, "link": link}));
  } catch (e) {
    log('Error sending data: $e');
    rethrow;
  }
}

Future<void> sendFiles() async {
  var request=http.MultipartRequest("POST", Uri.parse("https://9xkmd6fc-5005.inc1.devtunnels.ms/sendfile"));
  try{
  request.files.add(await http.MultipartFile.fromPath('file', fn.GlobalFunction.csvPath));
  request.files.add(await http.MultipartFile.fromPath('file', fn.GlobalFunction.imgPath));
  var response=await request.send();
  if (response.statusCode==200){
    log("Success");
  }}
  catch(e){
    log(e.toString());
  }
  }

Future<void> sendMail() async {
  try{
  final uri= Uri.parse(
    "https://9xkmd6fc-5005.inc1.devtunnels.ms/sendmail"
  );
  await http.get(uri, headers: {"content-type": "application/json"});
  }
  catch (e){
    log(e.toString());
  }
}