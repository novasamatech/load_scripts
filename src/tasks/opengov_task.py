from locust import TaskSet, task
from locust.user.task import tag
from utils.data_functions import get_opengov_data_list, get_opengov_data_single


class SwipeGovTasks(TaskSet):
    @tag('swipegov')
    @tag('swipegov_single')
    @task
    def swipegov_single(self):
        data = get_opengov_data_single()
        self.client.post('/not-secure/api/v1/referendum-summaries/single', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="swipegov_single")

    @tag('swipegov')
    @tag('swipegov_list')
    @task
    def swipegov_list(self):
        data = get_opengov_data_list()
        self.client.post('/not-secure/api/v1/referendum-summaries/list', data=data, headers=self.user.headers,
                         verify=self.user.verification, name="swipegov_list")
