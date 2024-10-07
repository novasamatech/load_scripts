import os
from locust import HttpUser
from locust.user.wait_time import constant
from tasks import GovernanceTasks, HistoryTasks, MultiStakingTasks, SwipeGovTasks
from utils.data_functions import get_addresses


class QuickstartUser(HttpUser):
    wait_time = constant(float(os.environ.get('WAIT_TIME', 1)))
    host = os.environ.get('BASE_URL')
    verification = os.environ.get('VERIFICATION', 'True').lower() == 'true'
    headers = {"content-type": "application/json"}
    addresses, address_prefics = get_addresses()
    print(f'Verification: {verification}')

    tasks = [HistoryTasks, GovernanceTasks, MultiStakingTasks, SwipeGovTasks]
