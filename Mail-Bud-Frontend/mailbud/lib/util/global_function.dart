import 'package:flutter_file_dialog/flutter_file_dialog.dart';
class GlobalFunction {
static String imgPath='';
static String csvPath='';
// Used by below fn with class name
static Future<String?> pickFile(OpenFileDialogType dialogType) async {
  final params = OpenFileDialogParams(
    dialogType: dialogType,
    sourceType: SourceType.photoLibrary,
  );
  final filePath = await FlutterFileDialog.pickFile(params: params);
  return filePath;
}

Future<String?> selectImage() async {
  final String? imagePath = await GlobalFunction.pickFile(OpenFileDialogType.image);
  if (imagePath!=null){
    imgPath=imagePath.toString();
    }
  return imagePath;
}

Future<String?> selectCSV() async {
  final String? csvpath = await GlobalFunction.pickFile(OpenFileDialogType.document);
  if (csvpath!=null){
    csvPath=csvpath.toString();
    }
  return csvpath;
}
}


