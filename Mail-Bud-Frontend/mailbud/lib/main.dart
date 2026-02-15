import 'package:flutter/material.dart';
import 'util/connect_backend.dart' as connect_backend;
import 'util/reusable_components.dart' as reuseable;
import 'util/global_function.dart' as global_fn;
import 'util/svg_content.dart';

final TextEditingController projectControl=TextEditingController();
final TextEditingController subjectControl=TextEditingController();
final TextEditingController linkControl=TextEditingController();
final TextEditingController messageControl=TextEditingController();
final TextEditingController nameControl=TextEditingController();

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
      return MaterialApp(
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Color.fromRGBO(10, 10, 10, 1),
        scaffoldBackgroundColor: Color.fromRGBO(10, 10, 10, 1)
      ),
      title: 'Mail Bud - Login',
      debugShowCheckedModeBanner: false,
      home: LoginPage(),
      
    );
  }
}

SVGContent svg = SVGContent();
class LoginPage extends StatelessWidget {
  const LoginPage({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(padding: EdgeInsetsGeometry.only(top: 80, left: 30, right: 30), child: Column(
        spacing: 12,
        children: [
          Text("Welcome", style: TextStyle(fontFamily: "sans-serif", fontSize: 36, color: Color.fromRGBO(224, 225, 231, 1)),),
          Text("Sign in with continue", style: TextStyle(fontFamily: "sans-serif", fontSize: 18, color: Color.fromRGBO(224, 225, 231, .65)),),
          Padding(padding: EdgeInsetsGeometry.symmetric(vertical: 16), child: reuseable.ReusableComponents().loginButton(svg.google, Color.fromRGBO(18, 18, 18, 1), connect_backend.openAuth)),
          
          Row(children: [
          Expanded(child: Divider(endIndent: 25)),
          Center(child: Text("OR", style: TextStyle(fontFamily: "sans-serif", fontSize: 14),)),
          Expanded(child: Divider(indent: 25)),
        ]),
        Padding(padding: EdgeInsetsGeometry.symmetric(vertical: 30), child: reuseable.ReusableComponents().fields("Enter your name", nameControl, 1)),
        reuseable.ReusableComponents().loginButton("", Color.fromRGBO(27, 38, 103, 1),
         ()async{
            await connect_backend.sendName(nameControl.text)?Navigator.push(context, MaterialPageRoute(builder: (context) => MyHomePage(title: "Mail bud"))):"";
         },
        text: "Continue")
        ])));}
        }


class EmailList extends StatefulWidget {
  const EmailList({super.key});

  @override
  State<EmailList> createState() => _EmailListState();
}

class _EmailListState extends State<EmailList> {
List<String> emails=[];

  @override
void initState() {
  super.initState();
  loadEmail();
}

Future<void> loadEmail() async {
  final listEmail = await connect_backend.getEmails(nameControl.text);
  setState(() {
    emails=List<String>.from(listEmail['email']);
  });
}
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromRGBO(10, 10, 10, .5),
        title: Text("Email Opened", textAlign: TextAlign.center)),
        body: RefreshIndicator(onRefresh: loadEmail,
        child: 
        ListView.builder(
          itemCount: emails.length,
          itemBuilder: (context, index) {
            return ListTile(
              title: Text(emails[index]),
            );
  },
), ),
    );
  }
}


// Main Screen
class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage>{
    int currentTabIndex = 0;

String? selectedImg;
String? selectedCSV;
String opened='';
String clicked='';
String rating='';
String location='';
String ctor='';

  @override
  void initState() {
    super.initState();
    loadStats();
  }

  Future<void> loadStats() async {
    final stat = await connect_backend.getStat(nameControl.text);
    setState(() {
      opened = stat['opened'].toString();
      clicked = stat['clicked'].toString();
      rating = stat['rating'].toString();
      location = stat['location'].toString();
      ctor = stat['ctor'].toString();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: NavigationBar(
        onDestinationSelected: (int index) {setState(() {
          currentTabIndex=index;
        });},
        selectedIndex: currentTabIndex,
        backgroundColor: Color.fromRGBO(10, 10, 10, .5),
        destinations: [
          NavigationDestination(icon: Icon(Icons.home_outlined), label: "Home"),
          NavigationDestination(icon: Icon(Icons.analytics_outlined), label: "Explore")
        ],
      ),
      // drawer: Drawer(
      //   backgroundColor: Color.fromRGBO(15, 15, 15, 1),
      //   child: ListView(
      //     padding: EdgeInsets.only(top: 60),
      //     children: <Widget>[
      //       reuseable.ReusableComponents().exploreButtons(0, "Create project", Color.fromRGBO(224, 225, 231, 1), connect_backend.sendData),
      //       Padding(padding: EdgeInsetsGeometry.only(top: 20, left: 20, bottom: 0) ,child: Text("Recent", style: TextStyle(fontSize: 18, fontWeight: FontWeight.w400))),
      //       ListTile(
      //         title: const Text('Promotion of new course', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400),),
      //       ),
      //       ListTile(
      //         title: const Text('Brand Affiliation with NTK', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400),),
      //       ),
      //       ListTile(
      //         title: const Text('Community partner promotion with RAN', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400, overflow: TextOverflow.ellipsis),),
      //       ),
      //     ],
      //   ),
      // ),
      appBar: AppBar(
        backgroundColor: Color.fromRGBO(10, 10, 10, .5),
        title: Text(widget.title, textAlign: TextAlign.center)
      ),
      body: <Widget>
      [
    // Home
    SingleChildScrollView(child: Container(
      padding: EdgeInsets.all(12),
      child: Column(
        spacing: 15,
        children: [

      reuseable.ReusableComponents().fields("Enter Project name", projectControl, 1),
      reuseable.ReusableComponents().fields("Enter Subject", subjectControl, 1),

      Row(
      children: [
      reuseable.ReusableComponents().attachments("Insert Document", svg.png, 20, 150, 20,0.45,
        () async {final path= await global_fn.GlobalFunction().selectImage();
          setState(() {
          selectedImg=path;
          });
          },
          clr: selectedImg!=null?Color.fromRGBO(0,141,0,.763):Color.fromRGBO(18, 18, 18, 1),
          context),

      reuseable.ReusableComponents().attachments("Insert CSV", svg.csv, 20, 150, 20,0.45,
      () async{
        final path=await global_fn.GlobalFunction().selectCSV();
        setState(() {
          selectedCSV=path;
        });
      },
      clr: selectedCSV!=null?Color.fromRGBO(0,141,0,.763):Color.fromRGBO(18, 18, 18, 1),
      context),
      ]),

      reuseable.ReusableComponents().fields("Enter Message", messageControl, 5),
      reuseable.ReusableComponents().fields("Enter a link (Optional)", linkControl, 1),

      Padding(padding: EdgeInsetsGeometry.only(left: 17),
        child: Row(
          spacing: MediaQuery.of(context).size.width*.2,
          children: [
          reuseable.ReusableComponents().exploreButtons(120, "Test email", Color.from(alpha: 1, red: 0, green: 155, blue: 0), () async{await connect_backend.sendMail("test", nameControl.text, projectControl.text, subjectControl.text, messageControl.text, linkControl.text);}),
          reuseable.ReusableComponents().exploreButtons(120, "Send email",Color.fromARGB(255, 133, 133, 255),
          () async {
                await connect_backend.sendMail("send", nameControl.text, projectControl.text, subjectControl.text, messageControl.text, linkControl.text);
          }),
        ])), 
      ])
    )),
        // Explore
        RefreshIndicator(
          onRefresh: loadStats,
            child: SingleChildScrollView(
            physics: AlwaysScrollableScrollPhysics(),
          child: Padding(padding: EdgeInsetsGeometry.symmetric(horizontal: 10), child: Column(
            spacing: 15,
          children: [
          InkWell(onTap: () {
            Navigator.push(context, MaterialPageRoute(builder: (context) => EmailList()));
          }, child: reuseable.ReusableComponents().card(svg.email,"Email Views", opened)),
          reuseable.ReusableComponents().card(svg.link,"Link Clicks", clicked),
          reuseable.ReusableComponents().card(svg.star,"Email Pull", rating
          ),
          reuseable.ReusableComponents().card(svg.bounce,"Click to Open", ctor
          ),
          reuseable.ReusableComponents().card(svg.location,"Location", location
          ),
        ]))
      )
    )][currentTabIndex]
    );
  }
  }

