from flask import Flask, request
import flask as fk
app = Flask(__name__) 

@app.route('/image/<emailID>')
def send_file(emailID):
    with open("loginLog.log", "a") as logs:

        userAgent = request.headers.get('User-Agent', 'Unknown')
        logs.write(f"{emailID}|{userAgent}\n")
    return fk.send_file("image/trackingPixel.png", mimetype="image/png")

if __name__ == '__main__':
    app.run(debug=True)