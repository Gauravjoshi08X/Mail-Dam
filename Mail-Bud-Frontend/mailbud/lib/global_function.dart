import 'package:flutter_file_dialog/flutter_file_dialog.dart';
import 'dart:developer' as dev;
class GlobalFunction {
static var imgPath='';
static var csvPath='';

static Future<String?> pickFile(OpenFileDialogType dialogType) async {
  final params = OpenFileDialogParams(
    dialogType: dialogType,
    sourceType: SourceType.photoLibrary,
  );
  final filePath = await FlutterFileDialog.pickFile(params: params);
  return filePath;
}

  void selectImage() async {
    final imagePath = await GlobalFunction.pickFile(OpenFileDialogType.image);
    imgPath = imagePath.toString();
    dev.log(imgPath);
}

  void selectCSV() async {
    final imagePath = await GlobalFunction.pickFile(OpenFileDialogType.document);
    csvPath = imagePath.toString();
    dev.log(csvPath);
}
}