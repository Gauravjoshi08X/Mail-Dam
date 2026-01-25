import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
class ReusableComponents {
  // Reusable Components
  Widget exploreButtons(double btnWidth, String lbl, Color textColor, VoidCallback fn){
      return ElevatedButton(
        onPressed: fn,
       style: ElevatedButton.styleFrom(backgroundColor: Color.fromRGBO(25, 25, 25, 0.698),
       shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
       minimumSize: Size(btnWidth, 50)),
       child: Text(lbl, style: TextStyle(fontSize: 20, color: textColor)), 
      );
  }

  Widget fields(String hint, TextEditingController? controller, int maxsize){
    return TextField(decoration: InputDecoration(hintText: hint, 
              border: OutlineInputBorder(),
              filled: true,
              fillColor: Color.fromRGBO(25, 25, 25, 0.698)),
              controller: controller,
              maxLines: maxsize
              );
  }

  Widget attachments(String text, String ico, double cardPadding, double cardHeight, double cardSpacing, double width, VoidCallback fn, BuildContext context, {Color clr=const Color.fromRGBO(18, 18, 18, 1)}){ 
      return Card(
        color: clr,
        elevation: 1,
        child: InkWell(
          onTap: fn,
        child: Container(
          padding: EdgeInsets.only(top: cardPadding),
          width: MediaQuery.of(context).size.width * width,
          height: cardHeight,
          child: Column(
            spacing: cardSpacing,
            children: [
          SvgPicture.string(ico, color: Color.fromRGBO(224, 225, 231, 1)),
          Text(text, style: TextStyle(fontFamily: "Roboto", fontSize: 20, fontWeight: FontWeight.w300, color: Color.fromRGBO(224, 225, 231, 1)),)
        ]),
      )
        ));
  }

  Widget loginButton(String? logo, Color clr,  VoidCallback fn, {String text="Sign in with Google"}){
    return ElevatedButton(
            onPressed: fn, 
            style: ButtonStyle(
            backgroundColor: WidgetStatePropertyAll(clr),
            shape: WidgetStatePropertyAll(RoundedRectangleBorder(borderRadius: BorderRadius.circular(8))),
            elevation: WidgetStatePropertyAll(1), shadowColor: WidgetStatePropertyAll(Color.fromARGB(78, 255, 255, 255)),),
              child: Row(spacing: 15, mainAxisAlignment: MainAxisAlignment.center, children: [SvgPicture.string(logo??""), 
              Text(text, 
              style: TextStyle(height: 4, fontSize: 16, fontFamily: "sans-serif",
              color: Color.fromRGBO(224, 225, 231, 1)),)
    ]));
  }

  Widget card(String iconCode, String primaryText, String secondaryText, Color colorCode){
    return Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Card(
              shadowColor: Color.fromARGB(78, 179, 0, 255),
              surfaceTintColor: Color.fromARGB(255, 20, 105, 102),
              color: Color.fromRGBO(18, 18, 18, 1),
              elevation: 1,
              child: Container(
                padding: EdgeInsets.fromLTRB(0, 15, 0, 4),
                width: 400,
                height: 110,
                child: Column(children: [Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  spacing: 78,
                  children: [
                SvgPicture.string(iconCode, color: Color.fromRGBO(224, 225, 231, 1)),
                Text(
                  primaryText,
                  textAlign: TextAlign.right,
                  style: TextStyle(fontSize: 35, fontWeight: FontWeight.bold, color: Color.fromRGBO(224, 225, 231, 1)),
                ),
                  ]
                ),

                Container(
                  margin: EdgeInsets.only(top: 3),
                  child: Text(secondaryText, style: TextStyle(color: colorCode, fontSize: 15),textAlign: TextAlign.right)
                )
                
                
                ]
                )
                
              ),
            )
          ],
        );
        }
}