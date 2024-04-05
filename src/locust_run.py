import json
import os
import random
from locust import HttpUser, TaskSet, constant_pacing, task
from locust.user.task import tag
from locust.user.wait_time import constant
from queries import casting_votings, casting_votings_referenda, delegates, stake_changes_by_address, history_changes_by_address, active_stakers


class HistoryTasks(TaskSet):
    @tag('history')
    @tag('history_elements')
    @task
    def history_elements(self):
        data = json.dumps(history_changes_by_address(
            random.choice(self.address), 42))
        self.client.post('/', data=data, headers=self.headers,
                         verify=self.verification)


class MultiStakingTasks(TaskSet):
    @tag('multistaking')
    @tag('active_stakers')
    @task
    def active_stakers(self):
        data = json.dumps(active_stakers(random.choice(self.address)))
        self.client.post('/', data=data, headers=self.headers,
                         verify=self.verification)

    @tag('multistaking')
    @tag('stake_changes')
    @task
    def stake_changes(self):
        data = json.dumps(stake_changes_by_address(
            random.choice(self.address), 42))
        self.client.post('/', data=data, headers=self.headers,
                         verify=self.verification)


class GovernanceTasks(TaskSet):
    @tag('governance')
    @tag('gov_casting_votings')
    @task
    def casting_votings(self):
        data = json.dumps(casting_votings(random.choice(self.user.address)))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification)
        wait_time = constant_pacing(6)

    @tag('governance')
    @tag('gov_casting_votings_referenda')
    @task
    def casting_votings_referenda(self):
        data = json.dumps(casting_votings_referenda(
            random.randint(1, 1000), random.choice([True, False])))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification)

    @tag('governance')
    @tag('gov_delegations')
    @task
    def delegates(self):
        data = json.dumps(delegates(block=23916253))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification)


class QuickstartUser(HttpUser):
    wait_time = constant(float(os.environ.get('WAIT_TIME', 1)))
    host = os.environ.get('BASE_URL')
    verification = bool(os.environ.get('VERIFICATION', True))
    headers = {"content-type": "application/json",
               "user-agent": "fearless/1 CFNetwork/978.0.7 Darwin/20.6.0",
               }
    address = json.load(open('data/address_list.json'))

    tasks = [HistoryTasks, GovernanceTasks, MultiStakingTasks]
