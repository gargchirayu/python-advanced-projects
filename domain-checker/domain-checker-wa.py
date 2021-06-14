import requests
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request

# GoDaddy user credentials
api_key = "3mM44UbgnG2FKv_Fxne44Xcwqo87qr7Vp4XPW"
secret_key = "DQGX6QRKPvevjfs2czSTKS"
req_headers = {
    "accept": "application/json",
    "Authorization": f"sso-key {api_key}:{secret_key}"
}

app = Flask(__name__)


# getting request url
def return_req_url(domain):
    return f"https://api.ote-godaddy.com/v1/domains/available?domain={domain}"


# checking domain availability from json file and sending WA update
@app.route('/bot', methods=['POST'])
def check_availability():
    # whatsapp functionality
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    print(f"Checking availability of {incoming_msg}")
    req_url = return_req_url(incoming_msg)
    req = requests.get(req_url, headers=req_headers)

    # if unsuccessful to retrieve info
    if req.status_code != 200:
        # print(f"Could not check for {domain}. Error Code - {req.status_code}")
        reply = f"Could not check for {domain}. Error Code - {req.status_code}"
        msg.body(reply)
        responded = True

    # response according to availability
    else:
        response = req.json()
        if response["available"] == True:
            reply = f"{incoming_msg} is available"
        else:
            reply = f"{incoming_msg} is not available"
        msg.body(reply)
        responded = True
    return str(resp)


if __name__ == '__main__':
    app.run()



