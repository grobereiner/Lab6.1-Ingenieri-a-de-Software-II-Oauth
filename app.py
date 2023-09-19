from flask import redirect, Flask, request
import json 
import requests
import base64

env = None
with open("client.json", "r") as f:
    env = json.load(f)

query_params = {
    "scope":"openid%20email%20profile",
    "response_type": "code",
    "state": "abcdefgh",
    "client_id": env["CLIENT_ID"],
    "redirect_uri": env["REDIRECT_URI"]
}

def query_param_string(qp) -> str:
    result = ''

    for i, k in enumerate(qp):
        result += f'{k}={qp[k]}'
        if i != len(qp)-1:
            result += '&'

    return result

print(query_param_string(query_params))

app = Flask(__name__)
app.secret_key = "nosepe"



print(f'{env["DIRECCION"]}authorize?{query_param_string(query_params)}')

@app.route('/')
def loguear():
    return redirect(f'{env["DIRECCION"]}authorize?{query_param_string(query_params)}')

@app.route("/authorization-code/callback")
def retornar():
    param_code, param_state = request.args.get('code'),request.args.get('state')
    print(f'STATE: {param_state}\nCODE: {param_code}')

    token_resp = requests.post(
        url=f'{env["DIRECCION"]}token', 
        headers={
            'Content-type': 'application/x-www-form-urlencoded',
        }, 
        data={
            'client_id': env['CLIENT_ID'],
            'client_secret': env["CLIENT_SECRET"],
            'grant_type': 'authorization_code',
            'redirect_uri': env["REDIRECT_URI"],
            'code': param_code
        }
    )
    
    access_token = token_resp.json()['access_token']

    user_info_resp = requests.get(
        url=f'{env["DIRECCION"]}userinfo',
        headers={
            'Authorization': f"Bearer {access_token}"
        }
    )

    print(user_info_resp.json())

    return "ccall"


app.run("0.0.0.0", port=8080,debug=True)