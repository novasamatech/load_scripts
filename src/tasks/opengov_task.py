from locust import TaskSet, task
from locust.user.task import tag
from utils.data_functions import get_opengov_data_list, get_opengov_data_single


class OpenGovTasks(TaskSet):
    @tag('opengov')
    @tag('opengov_single')
    @task
    def opengov_single(self):
        data = get_opengov_data_single()
        self.client.post('/not-secure/api/v1/referendum-summaries/single', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="opengov_single")

    @tag('opengov')
    @tag('opengov_list')
    @task
    def opengov_list(self):
        data = get_opengov_data_list()
        self.client.post('/not-secure/api/v1/referendum-summaries/list', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="opengov_list")
