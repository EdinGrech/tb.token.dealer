from requests.exceptions import HTTPError
from flask import Flask, jsonify
import TbApi
from dotenv import load_dotenv
import os
import base64
import auto_mail_handeler
import socket

#print(base64.b64encode("password".encode("utf-8")))
#print(base64.b64decode("cGFzc3dvcmQ=").decode("utf-8"))

load_dotenv('.env')
email = os.environ.get("tb_email_login")
password = base64.b64decode(os.environ.get("tb_email_login_password")).decode("utf-8")

app = Flask(__name__)
tbapi_url = "https://demo.thingsboard.io:443"
tbapi = TbApi.TbApi(tbapi_url, email, password)

@app.route("/deviceName/<string:deviceName>")
def newDevice(deviceName):
    try:
        auto_mail_handeler.setTimeVerification()
        auto_mail_handeler.send_email_notification("Device "+deviceName+" wants to connect to your server.\nSend an email with subject 'accept "+deviceName+"' to add device.\nYou have 8 minutes to sent appruval")
        auto_mail_handeler.mailLookUp()
        message = auto_mail_handeler.message
        print(message)#debugging
        verification_str = str("accept "+deviceName)
        print(verification_str)#debugging
        if message == False:
            return jsonify({"error": "No new mail"})
        else:
            if message == verification_str:
                try:
                    tbapi.add_device(device_name=deviceName, device_type=None, shared_attributes=None, server_attributes=None)
                except:
                    return jsonify({"error": "Device already exists"}),400
                token = tbapi.get_device_token(tbapi.get_devices_by_name(deviceName))
                return jsonify({ "token": token }), 200
            else:
                return jsonify({"error": "Device denied"}), 469
    except HTTPError as error:
        response = error.response.json()
        return jsonify({ "error": response["message"] }), 400

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)
    app.run(debug=True,host = ip)