import json
import os
import random
from locust import TaskSet, task
from locust.user.task import tag
from queries import stake_changes_by_address, active_stakers

class MultiStakingTasks(TaskSet):
    @tag('multistaking')
    @tag('active_stakers')
    @task
    def active_stakers(self):
        data = json.dumps(active_stakers(random.choice(self.user.addresses)))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="active_stakers")

    @tag('multistaking')
    @tag('stake_changes')
    @task
    def stake_changes(self):
        data = json.dumps(stake_changes_by_address(
            random.choice(self.user.addresses), self.user.address_prefics))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="stake_changes")
