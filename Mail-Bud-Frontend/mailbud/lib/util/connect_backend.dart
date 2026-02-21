import 'package:url_launcher/url_launcher.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:developer';
import 'global_function.dart' as fn;

FlutterSecureStorage storage=FlutterSecureStorage();

Future<void> openAuth() async {
  final uri = Uri.parse(
    "https://9xkmd6fc-5000.inc1.devtunnels.ms/auth/google"
  );

  await launchUrl(
    uri,
    mode: LaunchMode.externalApplication,
  );
}

Future<void> sessionManager() async {
  final uri=Uri.parse("https://9xkmd6fc-5000.inc1.devtunnels.ms/oauth/managesession");
  String? session=await storage.read(key: "session_id");
  if (session.toString().isNotEmpty){
    await http.post(uri, headers: {"authorization": "bearer $session"});
  }
  else{
    final response=await http.get(uri, headers: {"content-type": "application/json"});
    String sessionID=jsonDecode(response.body)["session_id"];
    storage.write(key: "session_id", value: sessionID);
  }
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
  
Future<Map> getStat(String name) async
{
  try{
    final url=Uri.parse("https://9xkmd6fc-5005.inc1.devtunnels.ms/getstat");
    final response=await http.post(url, headers: {"Content-Type": "application/json"}, body: jsonEncode({"name": name}));
    return jsonDecode(response.body);
  }
  catch(e){
    log(e.toString());
    return {"Error": e};
    }}

Future<Map> getEmails(String name) async
{
  try{
    final url=Uri.parse("https://9xkmd6fc-5005.inc1.devtunnels.ms/getemail");
    final response=await http.post(url, headers: {"Content-Type": "application/json"}, body: jsonEncode({"name": name}));
    return jsonDecode(response.body);
  }
  catch(e){
    log(e.toString());
    return {"Error": e};
    }}

Future<bool> sendName(String name) async
{
  try{
    final url=Uri.parse("https://9xkmd6fc-5005.inc1.devtunnels.ms/sendname");
    final response=(await http.post(url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"name": name})));
    log(response.statusCode.toString());
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

Future<void> sendMail(String flag, String name, String project, String subject, String message, String link) async {
  var request=http.MultipartRequest("POST", Uri.parse("https://9xkmd6fc-5005.inc1.devtunnels.ms/sendmail"));
  try{
    request.fields['flag']=flag;
    request.fields['name']=name;
    request.fields['project']=project;
    request.fields['subject']=subject;
    request.fields['message']=message;
    request.fields['link']=link;
  if (fn.GlobalFunction.imgPath!=""){
    request.files.add(await http.MultipartFile.fromPath('file', fn.GlobalFunction.imgPath));
  }
  if (fn.GlobalFunction.csvPath!=""){
    request.files.add(await http.MultipartFile.fromPath('file', fn.GlobalFunction.csvPath));
  }
  var response=await request.send();
  await response.stream.bytesToString();

  if (response.statusCode==200){
    log("Success");
  }
  if (response.statusCode==500){
    http.post(Uri.parse("https://9xkmd6fc-5005.inc1.devtunnels.ms/refresh"), headers: {"content-type": "application/json"}, 
    body: jsonEncode({"name": name}));
    openAuth();
  }
  }
  catch(e){
    log(e.toString());
  }
  }
