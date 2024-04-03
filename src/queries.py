def stake_changes_by_address(address):
    query = '{\n    stakeChanges(orderBy:TIMESTAMP_ASC, filter:{address:{equalTo:\"%s\"}}){\n    nodes{\n          id\n        address\n        timestamp\n        amount\n        accumulatedAmount\n        type\n      }\n    }\n  }' % (address)
    return {"query": query}

def history_changes_by_address(address):
    query = '{\n    historyElements(orderBy: TIMESTAMP_ASC, filter:{not:{ reward:{equalTo:\"null\"}}, address:{equalTo:\"%s\"},}) {nodes {id timestamp address reward }}}' % (address)
    return {"query": query}