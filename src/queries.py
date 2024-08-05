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


def casting_votings(publick_key: str, address_format: int):
  address = Keypair(public_key=publick_key, ss58_format=address_format).ss58_address
  query = '{\n   castingVotings(filter: { voter: {equalTo: \"%s\"}}) {\n    nodes {\n      referendumId\n      standardVote\n      splitVote\n      splitAbstainVote\n    }\n  }\n  \n  delegatorVotings(filter: {delegator: {equalTo: \"%s\"}}) {\n    nodes {\n      vote\n      parent {\n        referendumId\n        delegate {\n          accountId\n        }\n        standardVote\n      }\n    }\n  }\n}' % (address, address)
  
  return {"query": query}


def casting_votings_referenda(referenda_id: int, aye: bool, split: bool = False, split_abstain: bool = False):
  query = '{\n    castingVotings(filter:{referendumId:{equalTo:\"%s\"}, or: [{standardVote: {contains: {aye: %s}}},{splitVote: {isNull: %s}},{splitAbstainVote: {isNull: %s}}]}) {\n        nodes {\n            voter\n     \t\tstandardVote\n            splitVote\n            splitAbstainVote\n            delegateId\n            delegatorVotes {\n                nodes {\n                    delegator\n                    vote\n                }\n            }\n        }\n    }\n}' % (referenda_id, str(aye).lower(), str(split).lower(), str(split_abstain).lower())
  
  return {"query": query}


def delegates(block: int):
  query = '{\n   delegates {\n      totalCount\n      nodes {\n        accountId\n        delegators\n        delegatorVotes\n        delegateVotes(filter: {at: {greaterThanOrEqualTo: %s}}) {\n          totalCount\n        }\n      }\n   }\n}' % (block)
  
  return {"query": query}