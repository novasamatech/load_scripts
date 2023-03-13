import json
import random
import os
from locust import HttpUser, task, tag, constant, FastHttpUser
from queru_builder import android_votes_for_referenda, android_voting_screeen_request, get_account_delegations, get_delegations_list, get_delegator_info, get_delegators_list, get_votes, ios_votes_for_referenda, ios_voting_screeen_request
from subscan_requests import read_data_from_json


class QuickstartUser(FastHttpUser):
    wait_time = constant(float(os.environ.get('WAIT_TIME', 1)))
    host = os.environ.get('SUBQUERY_URL')
    tasks = []
    project_path = "/nova-wallet-kusama-governance2"
    headers = {
        'Host': 'api.subquery.network',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.0',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    def on_start(self):
        # Code to prepare data goes here
        delegate_account_list = read_data_from_json('data/delegator_data.json')
        self.higher_block_number = 17005224
        self.voter_addresses = read_data_from_json('data/voters_data.json')
        self.referenda_ids = read_data_from_json('data/referendas_data.json')
        self.block_for_30_days_in_past = self.higher_block_number - 14_400 * 30
        self.delegate_account_list = delegate_account_list

    @tag('voting_screen_requests_android')
    @task
    def voting_screen_requests_android(self):
        voter_adress = random.choice(self.voter_addresses)
        delegator_address = random.choice(self.delegate_account_list)
        data = json.dumps(android_voting_screeen_request(voter_adress, delegator_address),  indent=0)
        response = self.client.post(self.project_path, data=data, headers=self.headers)
        if response.status_code != 200:
            print(response.text)

    @tag('voting_screen_requests_ios')
    @task
    def voting_screen_requests_ios(self):
        voter_adress = random.choice(self.voter_addresses)
        delegator_address = random.choice(self.delegate_account_list)
        data = json.dumps(ios_voting_screeen_request(voter_adress, delegator_address))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

    @tag('votes_for_referenda_android')
    @task
    def votes_for_referenda_android(self):
        referenda_id = random.choice(self.referenda_ids)
        data = json.dumps(android_votes_for_referenda(referenda_id, True))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

    @tag('votes_for_referenda_ios')
    @task
    def votes_for_referenda_ios(self):
        referenda_id = random.choice(self.referenda_ids)
        data = json.dumps(ios_votes_for_referenda(referenda_id, True))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

    @tag('get_account_delegations')
    @task
    def get_account_delegations(self):
        delegator_address = random.choice(self.delegate_account_list)
        data = json.dumps(get_account_delegations(delegator_address, self.block_for_30_days_in_past))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

    @tag('get_delegator_info')
    @task
    def get_delegator_info(self):
        delegator_address = random.choice(self.delegate_account_list)
        data = json.dumps(get_delegator_info(delegator_address, self.block_for_30_days_in_past))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

    @tag('get_delegations_list')
    @task
    def get_delegations_list(self):
        delegator_address = random.choice(self.delegate_account_list)
        data = json.dumps(get_delegations_list(delegator_address))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

    @tag('get_delegator_list')
    @task
    def get_delegator_list(self):
        data = json.dumps(get_delegators_list(self.block_for_30_days_in_past))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

    @tag('votes_for_all_time')
    @task
    def votes_for_all_time(self):
        delegator_address = random.choice(self.delegate_account_list)
        data = json.dumps(get_votes(delegator_address, 0))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

    @tag('votes_for_last_30_days')
    @task
    def votes_for_last_30_days(self):
        delegator_address = random.choice(self.delegate_account_list)
        data = json.dumps(get_votes(delegator_address, self.block_for_30_days_in_past))
        response = self.client.post(self.project_path, data=data, headers=self.headers)

