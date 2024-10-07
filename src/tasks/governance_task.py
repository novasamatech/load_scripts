import json
import random
from locust import TaskSet, constant_pacing, task
from locust.user.task import tag
from queries import casting_votings, casting_votings_referenda, delegates

class GovernanceTasks(TaskSet):
    @tag('governance')
    @tag('gov_casting_votings')
    @task(85)
    def casting_votings(self):
        data = json.dumps(casting_votings(random.choice(self.user.addresses), self.user.address_prefics))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="gov_casting_votings")
        wait_time = constant_pacing(6)

    @tag('governance')
    @tag('gov_casting_votings_referenda')
    @task(5)
    def casting_votings_referenda(self):
        data = json.dumps(casting_votings_referenda(
            random.randint(1, 1000), random.choice([True, False])))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="gov_casting_votings_referenda")

    @tag('governance')
    @tag('gov_delegations')
    @task(10)
    def delegates(self):
        data = json.dumps(delegates(block=23916253))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="gov_delegations")
