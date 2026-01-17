from flask import Flask, request
app=Flask(__name__)
@app.route("/getdata", methods=["POST"])
def getData():
    data = request.get_json()
    print(data)
    return "Received"

if __name__=="__main__":
    app.run(debug=True)