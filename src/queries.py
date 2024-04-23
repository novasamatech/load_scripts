import json
from substrateinterface import Keypair
from build_multichain_query import build_query


def stake_changes_by_address(publick_key, key_format):
  address = Keypair(public_key=publick_key, ss58_format=key_format).ss58_address
  query = '{\n    stakeChanges(orderBy:TIMESTAMP_ASC, filter:{address:{equalTo:\"%s\"}}){\n    nodes{\n          id\n        address\n        timestamp\n        amount\n        accumulatedAmount\n        type\n      }\n    }\n  }' % (address)
  return {"query": query}

def history_changes_by_address(publick_key, key_format):
  address = Keypair(public_key=publick_key, ss58_format=key_format).ss58_address
  query = '{\n    historyElements(orderBy: TIMESTAMP_ASC, filter:{not:{ reward:{equalTo:\"null\"}}, address:{equalTo:\"%s\"},}) {nodes {id timestamp address reward }}}' % (address)
  return {"query": query}


def active_stakers(publick_key):
  network_list = json.load(open("./data/network_list.json"))
  data = []
  for network in network_list:
        data.append({
            "networkId": network["networkId"],
            "address": Keypair(public_key=publick_key, ss58_format=network["ss58_format"]).ss58_address,
            "stakingType": network["stakingType"]
        })
  query = build_query(data)

  return {"query": query}
