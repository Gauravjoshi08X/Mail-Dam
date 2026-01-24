import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'util/connect_backend.dart' as connect_backend;
import 'util/reusable_components.dart' as reuseable;
import 'util/global_function.dart' as global_fn;
import 'util/svg_content.dart';

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

class LoginPage extends StatelessWidget {
  LoginPage({super.key});
  final String google="""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#e3e3e3"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>""";
  final TextEditingController nameControl=TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
          Padding(padding: EdgeInsetsGeometry.symmetric(horizontal: 10),
          child: reuseable.ReusableComponents().fields("Enter a nickname", nameControl, 1, (value) async{
            await connect_backend.sendName(value)?Navigator.push(context, MaterialPageRoute(builder: (context) => MyHomePage(title: "Mail bud"))):"";
            })),
          Padding(padding:  EdgeInsetsGeometry.symmetric(vertical: 10), child: Text("or", style: TextStyle(fontSize: 15, fontWeight: FontWeight.w400, color: Color.fromRGBO(224, 225, 231, 1)))),
          ElevatedButton(
          onPressed: () {
            connect_backend.openAuth();
          },
          child: Padding(
          padding: EdgeInsetsGeometry.only(top: 10, bottom: 10),
          child: Row(mainAxisSize: MainAxisSize.min,
           spacing: 20,
           children: [SvgPicture.string(google),Text("Continue with Google", style: TextStyle(fontSize: 22),)
          ]))
        ),
      ],
      ),
    ));
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
    SVGContent svg = SVGContent();

final TextEditingController projectControl=TextEditingController();
final TextEditingController senderControl=TextEditingController();
final TextEditingController subjectControl=TextEditingController();
final TextEditingController linkControl=TextEditingController();
final TextEditingController messageControl=TextEditingController();

String? selectedImg;
String? selectedCSV;

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
      drawer: Drawer(
        backgroundColor: Color.fromRGBO(15, 15, 15, 1),
        child: ListView(
          padding: EdgeInsets.only(top: 60),
          children: <Widget>[
            reuseable.ReusableComponents().exploreButtons(0, "Create project", Color.fromRGBO(224, 225, 231, 1), connect_backend.sendData),
            Padding(padding: EdgeInsetsGeometry.only(top: 20, left: 20, bottom: 0) ,child: Text("Recent", style: TextStyle(fontSize: 18, fontWeight: FontWeight.w400))),
            ListTile(
              title: const Text('Promotion of new course', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400),),
            ),
            ListTile(
              title: const Text('Brand Affiliation with NTK', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400),),
            ),
            ListTile(
              title: const Text('Community partner promotion with RAN', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400, overflow: TextOverflow.ellipsis),),
            ),
          ],
        ),
      ),
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

      reuseable.ReusableComponents().fields("Enter Project name", projectControl, 1, (value){}),
      reuseable.ReusableComponents().fields("Enter Company's email", senderControl, 1, (value){}),
      reuseable.ReusableComponents().fields("Enter Subject", subjectControl, 1, (value){}),

      Row(
      children: [
      reuseable.ReusableComponents().attachments("Insert Image", svg.png, 20, 150, 20,0.45,
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

      reuseable.ReusableComponents().fields("Enter Message", messageControl, 5, (value){}),
      reuseable.ReusableComponents().fields("Enter a link (Optional)", linkControl, 1, (value){}),

      Padding(padding: EdgeInsetsGeometry.only(left: 17),
        child: Row(
          spacing: MediaQuery.of(context).size.width*.2,
          children: [
          reuseable.ReusableComponents().exploreButtons(120, "Test email", Color.from(alpha: 1, red: 0, green: 155, blue: 0), () => connect_backend.sendData(senderEmail: senderControl.text, message: messageControl.text, subject: subjectControl.text, link: linkControl.text)),
          reuseable.ReusableComponents().exploreButtons(120, "Send email",Color.fromARGB(255, 133, 133, 255),
          () async {
            // await connect_backend.sendData(project: projectControl.text, senderEmail: senderControl.text, subject: subjectControl.text, message: messageControl.text, link: linkControl.text);
                    // await connect_backend.sendFiles();
                    await connect_backend.sendMail();
          }),
        ])), 
      ])
    )),
        // Explore
        SingleChildScrollView(
        child: Column(
        children: [reuseable.ReusableComponents().card(svg.email,"Email Views", "128/410", Color.fromRGBO(0, 141, 0, 0.763)),
        reuseable.ReusableComponents().card(svg.link,"Link Clicks", "68/410", Color.fromRGBO(185, 0, 0, 0.811)),
        reuseable.ReusableComponents().card(svg.star,"Email Pull", "Moderate", Color.fromRGBO(0,141,0,.763)),
        reuseable.ReusableComponents().card(svg.bounce,"Bounce", "8/410", Color.fromRGBO(0,141,0,.763)),
        reuseable.ReusableComponents().card(svg.location,"Location", "Lalitpur", Color.fromRGBO(224, 225, 231, 1)),
        Image.asset("asset/images/chart.png")
      ])
    )
    ][currentTabIndex]
    );
  }
  }

