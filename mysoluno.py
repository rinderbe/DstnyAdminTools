import requests

API_BASE_URL = "https://mysoluno.se/api"


def get_call_api(endpoint, inp_auth, inp_org=""):
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {str(inp_auth.auth_token)}",
        "Refreshtoken": str(inp_auth.refresh_token),
        "Organization": str(inp_org)
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def post_call_api(endpoint, inp_auth, inp_org, inp_json=""):
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {str(inp_auth.auth_token)}",
        "Refreshtoken": str(inp_auth.refresh_token),
        "Organization": str(inp_org)
    }
    if inp_json != "":
        params = {
            "number": inp_json['fnr']
        }
        response = requests.post(url, headers=headers, json=inp_json, params=params)
    else:
        response = requests.post(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        return False
    if response.status_code == 200:
        return True
    else:
        return False


def get_all_function_numbers_acd(inp_auth, inp_org):
    response = get_call_api("FunctionNumber/AllFunctionNumbers", inp_auth, inp_org)
    return response['ACD']


def get_all_function_numbers_external(inp_auth, inp_org):
    response = get_call_api("FunctionNumber/AllFunctionNumbers", inp_auth, inp_org)
    return response['EXTERNAL_SYSTEM']


def get_all_function_numbers_rbn(inp_auth, inp_org):
    response = get_call_api("FunctionNumber/AllFunctionNumbers", inp_auth, inp_org)
    return response['RULE_BASED']


def get_agent_login_state(inp_auth, inp_org, inp_acd):
    concat_endpoint = "User/GetAgentsLoginState/" + inp_acd
    response = get_call_api(concat_endpoint, inp_auth, inp_org)
    return response


def get_manageable_orgs(inp_auth):
    concat_endpoint = "Organization/GetManageableOrganizationsInfo"
    response = get_call_api(concat_endpoint, inp_auth)
    return response


def enable_agent_login_state(inp_auth, inp_org, inp_acd, inp_userid):
    concat_endpoint = "User/LoginAgent/" + inp_acd + "/" + inp_org + "/" + inp_userid
    response = post_call_api(concat_endpoint, inp_auth, inp_org)
    return response


def disable_agent_login_state(inp_auth, inp_org, inp_acd, inp_userid):
    concat_endpoint = "User/LogoutAgent/" + inp_acd + "/" + inp_org + "/" + inp_userid
    response = post_call_api(concat_endpoint, inp_auth, inp_org)
    return response
