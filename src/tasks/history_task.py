import json
import os
import random
from locust import TaskSet, task
from locust.user.task import tag
from queries import history_changes_by_address


class HistoryTasks(TaskSet):
    @tag('history')
    @tag('history_elements')
    @task
    def history_elements(self):
        data = json.dumps(history_changes_by_address(
            random.choice(self.user.addresses), self.user.address_prefics))
        self.client.post('/', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="history_elements")
