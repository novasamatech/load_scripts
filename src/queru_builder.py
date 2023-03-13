def stake_changes_by_address(address):
    query = '{\n    stakeChanges(orderBy:TIMESTAMP_ASC, filter:{address:{equalTo:\"%s\"}}){\n    nodes{\n          id\n        address\n        timestamp\n        amount\n        accumulatedAmount\n        type\n      }\n    }\n  }' % (address)
    return {"query": query}

def history_changes_by_address(address):
    query = '{\n    historyElements(orderBy: TIMESTAMP_ASC, filter:{not:{ reward:{equalTo:\"null\"}}, address:{equalTo:\"%s\"},}) {nodes {id timestamp address reward }}}' % (address)
    return {"query": query}

def android_voting_screeen_request(voter_address, delegator_address):
    """
    This query is sent on voting screen by each block
    """
    query = {
        'query': 'query {{\n   castingVotings(filter: {{ voter: {{equalTo: "{}"}}}}) {{\n    nodes {{\n      referendumId\n      standardVote\n      splitVote\n      splitAbstainVote\n    }}\n  }}\n  \n  delegatorVotings(filter: {{delegator: {{equalTo: "{}"}}}}) {{\n    nodes {{\n      vote\n      parent {{\n        referendumId\n        delegate {{\n          accountId\n        }}\n        standardVote\n      }}\n    }}\n  }}\n}}'.format(voter_address, delegator_address)
    }

    return query

def ios_voting_screeen_request(voter_address, delegator_address):
    """
    This query is sent on voting screen by each block
    """
    query = f'{{\n    castingVotings(filter: {{ voter: {{equalTo: "{voter_address}"}}}}) {{\n        nodes {{\n            referendumId\n            standardVote\n            splitVote\n            splitAbstainVote\n        }}\n    }}\n\n    delegatorVotings(filter: {{delegator: {{equalTo: "{delegator_address}"}}}}) {{\n        nodes {{\n            vote\n            parent {{\n                referendumId\n                voter\n                standardVote\n            }}\n        }}\n    }}\n}}'

    return {'query': query}

def android_votes_for_referenda(referenda_id, direction: bool):
    """
    This query get all votes for referenda
    """
    payload = {
        "query": f"query {{\n    castingVotings(filter:{{referendumId:{{equalTo:\"{referenda_id}\"}}, or: [{{standardVote: {{contains: {{aye: {direction}}}}}}},{{splitVote: {{isNull: false}}}},{{splitAbstainVote: {{isNull: false}}}}]}}) {{\n        nodes {{\n            voter\n            standardVote\n            splitVote\n            splitAbstainVote\n            delegateId\n            delegatorVotes {{\n                nodes {{\n                    delegator\n                    vote\n                }}\n            }}\n        }}\n    }}\n}}"
    }

    return payload

def ios_votes_for_referenda(referenda_id, direction: bool):
    """
    This query get all votes for referenda
    """
    payload = {
        "query": f"{{\n    castingVotings (filter: {{\n        referendumId: {{equalTo: \"{referenda_id}\"}},\n        or: [\n              {{splitVote: {{ isNull: false }}}},\n              {{splitAbstainVote: {{isNull: false}}}},\n              {{standardVote: {{ contains: {{ aye: {direction}}}}}}}\n            ]\n    }}) {{\n        nodes {{\n          referendumId\n          standardVote\n          splitVote\n          splitAbstainVote\n          voter\n          delegatorVotes {{\n            nodes {{\n              delegator\n              vote\n            }}\n          }}\n        }}\n    }}\n}}"
    }

    return payload

def get_account_delegations(delegator_address, block: int):

    query = "{\n   delegates(filter:{accountId:{in:[\"%s\"]}}) {\n      totalCount\n      nodes {\n        accountId\n        delegators\n        delegatorVotes\n        delegateVotes(filter: {at: {greaterThanOrEqualTo: %s}}) {\n          totalCount\n        }\n      }\n   }\n}" % (delegator_address, block)

    return {"query": query}

def get_delegator_info(delegator_address, block: int):
    query = "{\n   delegates(filter: {accountId: {equalTo: \"%s\"}}) {\n      nodes {\n        accountId\n        delegators\n        delegatorVotes\n        allVotes: delegateVotes {\n          totalCount\n        }\n        recentVotes: delegateVotes(filter: {at: {greaterThanOrEqualTo: %s}}) {\n          totalCount\n        }\n      }\n   }\n}" % (delegator_address, block)

    return {"query": query}

def get_delegations_list(delegator_address):
    query = "{\n  delegations(filter: {delegateId: {equalTo: \"%s\" }}) {\n    nodes {\n      delegator\n      delegation\n    }\n  }\n}" % (delegator_address)

    return {"query": query}

def get_delegators_list(block: int):
    query = "{\n   delegates {\n      totalCount\n      nodes {\n        accountId\n        delegators\n        delegatorVotes\n        delegateVotes(filter: {at: {greaterThanOrEqualTo: %s}}) {\n          totalCount\n        }\n      }\n   }\n}" % (block)

    return {"query": query}

def get_votes(delegator_address, block: int = 0):
    """This function generate query for getting all votes for delegate

    Args:
        delegator_address (_type_): ss58 address
        block (int, optional): Defaults to 0.
    """
    query = "{\n  castingVotings(filter: { and: { voter: {equalTo: \"%s\"}, at: { greaterThanOrEqualTo: %s}}}) {\n    nodes {\n      referendumId\n      standardVote\n      splitVote\n      splitAbstainVote\n    }\n  }\n}" % (delegator_address, block)

    return {"query": query}