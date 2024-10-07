import json
import os
import random


def get_addresses() -> (tuple[list, int]):
  network = os.environ.get('NETWORK', '').lower()

  network_files = {
    'polkadot': 'data/polkadot_gov_addresses.json',
    'kusama': 'data/polkadot_gov_addresses.json',
  }

  file_path = network_files.get(network, 'data/address_list.json')

  if network not in network_files:
    print(
      f'Network was not set or is not recognized ({network}). Using default address list.')

  with open(file_path) as f:
    data = json.load(f)
    return data['addresses'], data['address_prefix']


def get_opengov_data_single() -> str:

  with open('data/opengov_data.json') as f:
    opengov_data = json.load(f)

    chain = random.choice(opengov_data['chains'])
    referendum_id = random.choice(chain['referendumIds'])
    language_iso_code = random.choice(opengov_data["languageIsoCode"])

    return json.dumps({
      "chainId": chain['chainId'],
      "languageIsoCode": language_iso_code,
      "referendumId": referendum_id
    })


def get_opengov_data_list() -> str:
  with open('data/opengov_data.json') as f:
    opengov_data = json.load(f)

    chain = random.choice(opengov_data['chains'])
    language_iso_code = random.choice(opengov_data["languageIsoCode"])

    return json.dumps({
      "chainId": chain['chainId'],
      "languageIsoCode": language_iso_code,
      "referendumIds": chain['referendumIds']
    })
