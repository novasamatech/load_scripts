def build_query(data):
    filter_ors = [
        f'{{and: [{{networkId: {{equalTo: "{item["networkId"]}"}}}}, {{or: [{{and: [{{address: {{equalTo: "{item["address"]}"}}}}, {{stakingType: {{equalTo: "{item["stakingType"]}"}}}}]}}]}}]}}'
        for item in data
    ]

    query = f"""
{{
  activeStakers(
    filter: {{or: [{', '.join(filter_ors)}]}}
  ) {{
    nodes {{
      networkId
      stakingType
      address
    }}
  }}
  stakingApies {{
    nodes {{
      networkId
      stakingType
      maxAPY
    }}
  }}
  rewards: rewards(
    filter: {{and: [{{or: [{', '.join(filter_ors)}]}}, {{type: {{equalTo: reward}}}}]}}
  ) {{
    groupedAggregates(groupBy: [NETWORK_ID, STAKING_TYPE]) {{
      sum {{
        amount
      }}
      keys
    }}
  }}
  slashes: rewards(
    filter: {{and: [{{or: [{', '.join(filter_ors)}]}}, {{type: {{equalTo: slash}}}}]}}
  ) {{
    groupedAggregates(groupBy: [NETWORK_ID, STAKING_TYPE]) {{
      sum {{
        amount
      }}
      keys
    }}
  }}
}}
"""
    return query