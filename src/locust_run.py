import time
import json
from locust import HttpUser, task, between
from fixtures import stake_changes_by_address, history_changes_by_address


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://api.subquery.network/sq/ef1rspb"
    headers = {"content-type": "application/json",
               "user-agent": "fearless/1 CFNetwork/978.0.7 Darwin/20.6.0",
               }
    address = '114SUbKCXjmb9czpWTtS3JANSmNRwVa4mmsMrWYpRG1kDH5'

    @task
    def stake_changes(self):
        data = json.dumps(stake_changes_by_address(self.address))
        self.client.post('/fearless-wallet', data=data, headers=self.headers)

    @task
    def history_elements(self):
        data = json.dumps(history_changes_by_address(self.address))
        self.client.post('/fearless-wallet', data=data, headers=self.headers)
