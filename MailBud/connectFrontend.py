from flask import Flask, request, json
app=Flask(__name__)
@app.route("/getdata", methods=["POST", "GET"])
def getData():
    data = json.dumps(request.get_json())
    print(data)
    return "Received"

if __name__=="__main__":
    app.run(debug=True)