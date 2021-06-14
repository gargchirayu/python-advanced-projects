import argparse
import requests

parser = argparse.ArgumentParser(description="Checks availability if a domain")
parser.add_argument("domain", type=str, help="Domain name to be checked")

args = parser.parse_args()

# GoDaddy user credentials
api_key = "3mM44UbgnG2FKv_Fxne44Xcwqo87qr7Vp4XPW"
secret_key = "DQGX6QRKPvevjfs2czSTKS"
req_headers = {
    "accept": "application/json",
    "Authorization": f"sso-key {api_key}:{secret_key}"
}


# getting request url
def return_req_url(domain):
    return f"https://api.ote-godaddy.com/v1/domains/available?domain={domain}"


# checking domain availability from json file
def check_availability(domain):
    print(f"Checking availability of {domain}")
    req_url = return_req_url(domain)
    req = requests.get(req_url, headers=req_headers)

    # if unsuccessful to retrieve info
    if req.status_code != 200:
        print(f"Could not check for {domain}. Error Code - {req.status_code}")
    # response according to availability
    else:
        response = req.json()
        if response["available"] == True:
            print(f"{domain} is available")
        else:
            print(f"{domain} is not available")


check_availability(args.domain)
