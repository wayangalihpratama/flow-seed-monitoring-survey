import requests as r
from os import environ
from time import time

auth_data = {
    'client_id': environ['AUTH0_CLIENT'],
    'username': environ['AUTH0_USER'],
    'password': environ['AUTH0_PWD'],
    'grant_type': 'password',
    'scope': 'openid email'
}
auth_url = "https://akvofoundation.eu.auth0.com/oauth/token"
flow_api_url = "https://api-auth0.akvo.org/flow/orgs/seap/surveys/survey_id"
tc_api_url = "http://tech-consultancy.akvo.org/akvo-flow-web-api/seap/form_id/update"

# Farmer test survey from Demo Survey
survey_id = 6087710401888256
registraton_form = 6286483501613056
monitoring_form = 5968064826834944


def get_token():
    account = r.post(auth_url, auth_data)
    try:
        account = account.json()
    except ValueError:
        print('FAILED: TOKEN ACCESS UNKNOWN')
        return False
    return {'token': account['id_token'], 'time': time()}


def get_header(token):
    return {
        'Authorization': f"Bearer {token['token']}",
        'Accept': 'application/vnd.akvo.flow.v2+json',
        'Content-Type': 'application/json'
    }


def get_data(url, token):
    header = get_header(token)
    response = r.get(url, headers=header)
    print("FETCH: " + str(response.status_code) + " | " + url)
    if response.status_code == 200:
        response = response.json()
        return response
    print("ERROR: " + url)
    return response


def get_form(token, form_id: int):
    form_url = tc_api_url.replace('form_id', str(form_id))
    return get_data(form_url, token)
