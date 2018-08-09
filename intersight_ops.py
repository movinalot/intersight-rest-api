"""
    intersight_ops.py - shows ho to use intersight REST API

    author: John McDonough (jomcdono@cisco.com)
"""
import json
import requests

from intersight_auth import IntersightAuth

# Create an AUTH object
AUTH = IntersightAuth(
    secret_key_filename="SecretKey.txt",
    api_key_id="replace-with-your-api-key"
    )

# Intersight REST API Base URL
BURL = 'https://www.intersight.com/api/v1/'

if __name__ == "__main__":

    # intersight operations, GET, POST, PATCH, DELETE
    OPERATIONS = [
        {
            "resource_path":"compute/PhysicalSummaries",
            "request_method":"GET"
        },
        {
            "resource_path":"ntp/Policies",
            "request_method":"GET"
        },
        {
            "resource_path":"ntp/Policies",
            "request_method":"POST",
            "request_body":{
                "Enabled":True,
                "Name":"ntp-policy",
                "Description":"NTP Policy for ntp.org",
                "NtpServers":[
                    "pool.ntp.org"
                    ],
                "Tags":[]
            }
        },
        {
            "resource_path":"ntp/Policies",
            "request_method":"POST",
            "request_body":{
                "Enabled":True,
                "Name":"ntp-policy-west",
                "Description":"NTP Policy for ntp.org West Coast",
                "NtpServers":[
                    "0.pool.ntp.org",
                    "1.pool.ntp.org"
                    ],
                "Tags":[]
            }
        },
        {
            "resource_path":"ntp/Policies",
            "request_method":"POST",
            "request_body":{
                "Enabled":True,
                "Name":"ntp-policy-east",
                "Description":"NTP Policy for ntp.org East Coast",
                "NtpServers":[
                    "2.pool.ntp.org",
                    "3.pool.ntp.org"
                    ],
                "Tags":[]
            }
        },
        {
            "resource_name":"ntp-policy",
            "resource_path":"ntp/Policies",
            "request_method":"PATCH",
            "request_body":{
                "NtpServers":[
                    "pool.ntp.org",
                    "10.10.10.30"
                    ]
                }
        },
        {
            "resource_name":"ntp-policy-east",
            "resource_path":"ntp/Policies",
            "request_method":"DELETE"
        }
    ]


    for operation in OPERATIONS:

        response = None
        print(operation['request_method'])

        # GET
        if operation['request_method'] == "GET":
            response = requests.get(
                BURL + operation['resource_path'],
                auth=AUTH
                )

        # POST
        if operation['request_method'] == "POST":
            req_data = json.dumps(operation['request_body'])
            response = requests.post(
                BURL + operation['resource_path'],
                data=req_data,
                auth=AUTH
                )

        # PATCH
        if operation['request_method'] == "PATCH":

            # GET the Moid of the MO to PATCH
            response = requests.get(
                (
                    BURL + operation['resource_path'] +
                    "?$filter=Name eq '" + operation['resource_name'] + "'"
                    ),
                auth=AUTH
                )

            # Extract the Moid from the Results
            json_result = json.loads(response.text)
            moid = json_result["Results"][0]["Moid"]

            req_data = json.dumps(operation['request_body'])
            response = requests.patch(
                BURL + operation['resource_path'] + "/" + moid,
                data=req_data,
                auth=AUTH
                )

        # DELETE
        if operation['request_method'] == "DELETE":

            # GET the Moid of the MO to DELETE
            response = requests.get(
                (
                    BURL + operation['resource_path'] +
                    "?$filter=Name eq '" + operation['resource_name'] + "'"
                    ),
                auth=AUTH
                )

            # Extract the Moid from the Results
            json_result = json.loads(response.text)
            moid = json_result["Results"][0]["Moid"]

            response = requests.delete(
                BURL + operation['resource_path'] + "/" + moid,
                auth=AUTH
                )

        print(response)
        print(response.text)
