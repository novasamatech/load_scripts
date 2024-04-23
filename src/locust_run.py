import json
import os
import random
from locust import HttpUser, task
from locust.user.task import tag
from locust.user.wait_time import constant
from queries import stake_changes_by_address, history_changes_by_address, active_stakers


class QuickstartUser(HttpUser):
    wait_time = constant(float(os.environ.get('WAIT_TIME', 1)))
    host = os.environ.get('BASE_URL')
    verification = bool(os.environ.get('VERIFICATION', True))
    headers = {"content-type": "application/json",
               "user-agent": "fearless/1 CFNetwork/978.0.7 Darwin/20.6.0",
               }
    address = json.load(open('data/address_list.json'))

    @tag('stake_changes')
    @task
    def stake_changes(self):
        data = json.dumps(stake_changes_by_address(random.choice(self.address), 42))
        self.client.post('/', data=data, headers=self.headers, verify=self.verification)

    @tag('history_elements')
    @task
    def history_elements(self):
        data = json.dumps(history_changes_by_address(random.choice(self.address), 42))
        self.client.post('/', data=data, headers=self.headers, verify=self.verification)

    @tag('active_stakers')
    @task
    def active_stakers(self):
        data = json.dumps(active_stakers(random.choice(self.address)))
        self.client.post('/', data=data, headers=self.headers, verify=self.verification)
