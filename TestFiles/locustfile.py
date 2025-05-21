from locust import HttpUser, between, task
from loguru import logger

host = '0.0.0.0'
port = 2443
userName = 'root'
userPass = '0penBmc'

logPath = '/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_logs.log'
logger.add(logPath, level='DEBUG')

class OBMCAPI(HttpUser):
    authToken = ""

    def on_start(self):
        response = self.client.post(
            f'/{host}:{port}/redfish/v1/SessionService/Sessions', 
            json={"UserName":userName, "Password":userPass},
            verify=False
        )
        jdata = response.headers
        #logger.info(jdata)

        try:
            self.authToken = jdata['X-Auth-Token']
            logger.info('Grated auth token = ' + str(self.authToken))
            if self.authToken == "":
                plug = 0
                # logger.debug("Couldn't get auth token")
        except: 
            plug = 0
            # logger.debug("Response headers: 'X-Auth-Token' - no such element in response!")


    @task
    def getRedfishInfo(self):
        logger.info('User used auth token: ' + str(self.authToken))
        self.client.get(
            f'/{host}:{port}/redfish/v1/Systems/system',
            headers={"X-Auth-Token": self.authToken}, 
            verify=False
        )


class PublicAPI(HttpUser):
    wait_time = between(1, 2)

    @task
    def getJSON(self):
        self.client.get(
            '/jsonplaceholder.typicode.com/posts'
        )

    @task
    def getWeather(self):
        self.client.get(
            '/wttr.in/Novosibirsk?format=j1'
        )
