import json
import math
from typing import List, Tuple
import requests


def send_request(url, data):
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d',
        'baggage': 'sentry-public_key=da3d374c00b64b6196b5d5861d4d1374,sentry-trace_id=fb6a06eb7a3c4ada9263c2451eadfba2,sentry-sample_rate=0.01',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    return requests.request("POST", url, headers=headers,
                            json=data)

def request_processor(url, payload):
    return_data = []
    first_response = send_request(
        url, payload_update(payload, 0)).json()
    count = int(first_response.get("data").get("count"))
    request_count = math.ceil(count/100)
    if count <= 100:
        return_data.append(first_response)
    else:
        for i in range(request_count):
            response = send_request(
                url, payload_update(payload, i)).json()
            return_data.append(response)
    return return_data

def payload_update(payload, n) -> str:
    payload['page'] = n
    payload['row'] = 100
    return payload

def collect_accounts_who_delegate_and_block() -> Tuple[List[str], int]:
    url = "https://kusama.webapi.subscan.io/api/v2/scan/extrinsics"
    payload = {"signed":"signed","address":"","module":"convictionvoting","call":"delegate","no_params":True}
    response = request_processor(url, payload)
    account_list = []
    higer_block = 0
    for data_array in response:
        for extrinsic in data_array['data']['extrinsics']:
            if extrinsic['block_num'] > higer_block:
                higer_block = extrinsic['block_num']
            account_list.append(extrinsic['account_display']['address'])
    return (account_list, higer_block)

def collect_voters_accounts() -> List[str]:
    url = "https://kusama.webapi.subscan.io/api/v2/scan/extrinsics"
    payload = {"row": 100, "page": 1, "signed":"signed","address":"","module":"convictionvoting","call":"vote","no_params":True}
    response = send_request(url, payload)
    data = json.loads(response.text)
    account_list = []
    for extrinsic in data['data']['extrinsics']:
        account_list.append(extrinsic['account_display']['address'])
    return account_list

def collect_all_referenda_ids() -> List[int]:
    url = "https://kusama.webapi.subscan.io/api/scan/referenda/referendums"
    payload_1 = {"status":"completed","origin":"all"}
    payload_2 = {"status":"active","origin":"all"}
    response_1 = request_processor(url, payload_1)
    response_2 = request_processor(url, payload_2)
    data_like = response_1 + response_2
    referendum_list = []
    for data in data_like:
        for extrinsic in data['data']['list']:
            referendum_list.append(extrinsic['referendum_index'])

    return referendum_list

def save_data_in_json(subsquare_referenda_dict, path='referenda_data.json'):
    with open(path, 'w') as outfile:
        json.dump(subsquare_referenda_dict, outfile)

def read_data_from_json(path):
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None

# save_data_in_json(collect_accounts_who_delegate_and_block(), 'delegator_data.json')
# save_data_in_json(collect_voters_accounts(), 'voters_data.json')
# save_data_in_json(collect_all_referenda_ids(), 'referendas_data.json')
