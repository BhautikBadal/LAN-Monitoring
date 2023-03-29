import requests
import json
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def nxapi_ping(switch_ip, switch_user, switch_password, vrf_name, destination_ip):
    """
    This function sends a ping command to a Cisco Nexus switch via NX-API.
    Args:
    - switch_ip (str): the IP address of the switch
    - switch_user (str): the username for authentication
    - switch_password (str): the password for authentication
    - vrf_name (str): the name of the VRF to use
    - destination_ip (str): the IP address or hostname to ping
    Returns:
    - The response from the switch as a Python dictionary.
    """

    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # Set the URL and headers
    url = f'https://{switch_ip}/ins'
    myheaders = {'content-type': 'application/json-rpc'}

    # Build the payload
    payload = [
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": f"ping {destination_ip} vrf {vrf_name}",
                "version": 1
            },
            "id": 1
        }
    ]

    # Send the request and get the response
    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(
        switch_user, switch_password), verify=False).json()

    return response


def gateway_ping(switch_ip, switch_user, switch_password, vrf_name, destination_ip,intFaceID):
    """
    This function sends a ping command to a Cisco Nexus switch via NX-API.
    Args:
    - switch_ip (str): the IP address of the switch
    - switch_user (str): the username for authentication
    - switch_password (str): the password for authentication
    - vrf_name (str): the name of the VRF to use
    - destination_ip (str): the IP address or hostname to ping
    Returns:
    - The response from the switch as a Python dictionary.
    """

    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # Set the URL and headers
    url = f'https://{switch_ip}/ins'
    myheaders = {'content-type': 'application/json-rpc'}

    # Build the payload
    payload = [
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": f"ping {destination_ip} vrf {vrf_name}",
                "version": 1
            },
            "id": 1
        }
    ]

    # Send the request and get the response
    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(
        switch_user, switch_password), verify=False).json()

    if '100.00% packet loss' in response['result']['msg']:
        print("Lost Gateway Connection, Logging a case with Service Provider...")
    else:
        intResponse = show_interface(intFaceID)
        print("Your current interface state is:-", intResponse)
        if intResponse == "down":
            update_interface('172.26.21.101','admin', 'Lock&Key()19', intFaceID)   
        



def show_interface(intfaceID):

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    switchuser = 'admin'
    switchpassword = 'Lock&Key()19'
    url = 'https://172.26.21.101/ins'
    myheaders = {'content-type': 'application/json-rpc'}
    payload = [{"jsonrpc": "2.0",        "method": "cli",        "params": {
        "cmd": f"show int eth 1/{intfaceID}",          "version": 1},        "id": 1}]
    

    response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(
        switchuser, switchpassword), verify=False).json()

    
    print("Verifying Interface Status...")

    interface_State = response["result"]["body"]["TABLE_interface"]["ROW_interface"]["state"]

    return interface_State


def update_interface(switch_ip, switch_user, switch_password, intFaceID):
    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    print("Network Auto healing in Progress...")
    # Set the URL and headers
    url = f'https://{switch_ip}/ins'
    myheaders = {'content-type': 'application/json-rpc'}

    payload = [{"jsonrpc": "2.0",            "method": "cli",            "params": {"cmd": "conf t",                "version": 1},            "id": 1},        {"jsonrpc": "2.0",            "method": "cli",            "params": {
        "cmd": f"int eth 1/{intFaceID}",                "version": 1},            "id": 2},        {"jsonrpc": "2.0",            "method": "cli",            "params": {"cmd": "no shutdown",                "version": 1},            "id": 3},]

    requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(
        switch_user, switch_password), verify=False).json()
    
    
    interfaceRes =show_interface(intFaceID)
    print("your interface state is ", interfaceRes)


# main entry
response = nxapi_ping('172.26.21.101', 'admin',
                      'Lock&Key()19', 'wan', '10.10.0.2')

response1 = nxapi_ping('172.26.21.101', 'admin',
                      'Lock&Key()19', 'wan', '10.10.10.2')

print("Checking For 10.10.0.2")

if '100.00% packet loss' in response['result']['msg']:
    print("Detected LAN connection is Down...")
    response = nxapi_ping('172.26.21.101', 'admin',
                          'Lock&Key()19', 'wan', '10.10.0.2')
    if '100.00% packet loss' in response['result']['msg']:
        print("LAN connection is Down, verifying network connectivity!")
        gateway_ping('172.26.21.101', 'admin','Lock&Key()19', 'wan', '10.10.0.1',4)
    else:
        print("LAN connection is Up!")
else:
    print("LAN connection is Up")

print("Checking For 10.10.10.2")

if '100.00% packet loss' in response1['result']['msg']:
    print("Detected WAN connection is Down...")
    response1 = nxapi_ping('172.26.21.101', 'admin',
                          'Lock&Key()19', 'wan', '10.10.10.2')
    if '100.00% packet loss' in response1['result']['msg']:
        print("WAN connection is Down, verifying network connectivity!")
        gateway_ping('172.26.21.101', 'admin','Lock&Key()19', 'wan', '10.10.0.1',1)
    else:
        print("WAN connection is Up!")
else:
    print("WAN connection is Up")
