import 'package:flutter_file_dialog/flutter_file_dialog.dart';
class GlobalFunction {
static var imgPath='';
static var csvPath='';
static var docPath='';

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
    docPath = imagePath.toString();
    print(docPath);
}

  void selectDoc() async {
    final imagePath = await GlobalFunction.pickFile(OpenFileDialogType.document);
    imgPath = imagePath.toString();
    print(imgPath);
}
  void selectCSV() async {
    final imagePath = await GlobalFunction.pickFile(OpenFileDialogType.document);
    csvPath = imagePath.toString();
    print(csvPath);
}
}