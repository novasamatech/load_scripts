import json
import os


def get_addresses() -> (list, int):
    network = os.environ.get('NETWORK', '').lower()

    network_files = {
        'polkadot': 'data/polkadot_gov_addresses.json',
        'kusama': 'data/polkadot_gov_addresses.json',
    }

    file_path = network_files.get(network, 'data/address_list.json')

    if network not in network_files:
        print(f'Network was not set or is not recognized ({network}). Using default address list.')

    with open(file_path) as f:
      data = json.load(f)
      return data['addresses'], data['address_prefix']
