import 'package:flutter_file_dialog/flutter_file_dialog.dart';
class GlobalFunction {

static Future<String?> pickFile(OpenFileDialogType dialogType) async {
  final params = OpenFileDialogParams(
    dialogType: dialogType,
    sourceType: SourceType.photoLibrary,
  );
  final filePath = await FlutterFileDialog.pickFile(params: params);
  return filePath;
}

  Future<String?> selectImage() async {
    final imagePath = await GlobalFunction.pickFile(OpenFileDialogType.image);
    return imagePath;
}

  Future<String?> selectCSV() async {
    final imagePath = await GlobalFunction.pickFile(OpenFileDialogType.document);
    return imagePath;
}
}