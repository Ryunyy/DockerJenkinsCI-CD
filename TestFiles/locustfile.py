from locust import HttpUser, events, task, between
from locust.runners import MasterRunner
import json
from json import JSONDecodeError
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session_resp = None

@events.test_start.add_listener
def on_start_test(environment, **kwargs):
	
	global session_resp

	try:
		if not isinstance(environment.runner, MasterRunner):
			url = "https://127.0.0.0:2443/redfish/v1/SessionService/Sessions"
			headers = {"Content-Type": "application/json"}
			root_data = {"UserName": "root", "Password": "0penBmc"}

			session_resp = requests.post(url, headers=headers, data=json.dumps(root_data), verify=False)

	except HTTPError:
		assert 0, "HTTP request returned an unsuccessful status code."
	except ConnectionError:
		assert 0, "A Connection error occured."
	except Timeout:
		assert 0, "The request timed out while trying to connect/send data to the server."


class OpenBmcUser(HttpUser):
	#host = "https://127.0.0.0:2443"
	wait_time = between(3, 5)

	@task
	def system_info_task(self):
		with self.client.get("/redfish/v1/Systems/system", 
							headers={"X-Auth-Token": session_resp.headers["X-Auth-Token"]},
							verify=False,
							catch_response=True) as response:

			if response.status_code != 200:
				response.failure("Returned unsuccessful status")

			try:
				testdata_json = response.json()
				print("Status code:", response.status_code)
				print("Health:", testdata_json["Status"]["Health"])
			except JSONDecodeError:
				response.failure("Response could not be decoded as JSON")
			except KeyError:
				reponse.failure("Response did not contain some keys: 'Status' or 'Health'")


	@task
	def powerstate_task(self):
		with self.client.get("/redfish/v1/Systems/system",
							headers={"X-Auth-Token": session_resp.headers["X-Auth-Token"]},
							verify=False,
							catch_response=True) as response:

			try:
				testdata_json = response.json()
				print("PowerState:", testdata_json["PowerState"])

			except JSONDecodeError:
				response.failure("Response could not be decoded as JSON")
			except KeyError:
				response.failure("Response did not contain expected key 'PowerState'")
                
# from locust import HttpUser, between, task
# from loguru import logger

# host = '0.0.0.0'
# port = 2443
# userName = 'root'
# userPass = '0penBmc'

# logPath = '/var/jenkins_home/workspace/PyTests_CI_CD/TestReports/locust_logs.log'
# logger.add(logPath, level='DEBUG')

# class OBMCAPI(HttpUser):
#     authToken = ""

#     def on_start(self):
#         response = self.client.post(
#             f'/{host}:{port}/redfish/v1/SessionService/Sessions', 
#             json={"UserName":userName, "Password":userPass},
#             verify=False
#         )
#         jdata = response.headers
#         logger.info(response.status_code)
#         logger.info(response.text)
#         #logger.info(jdata)

#         try:
#             self.authToken = jdata['X-Auth-Token']
#             logger.info('Grated auth token = ' + str(self.authToken))
#             if self.authToken == "":
#                 plug = 0
#                 logger.debug("Couldn't get auth token")
#         except: 
#             plug = 0
#             logger.debug("Response headers: 'X-Auth-Token' - no such element in response!")


#     @task
#     def getRedfishInfo(self):
#         logger.info('User used auth token: ' + str(self.authToken))
#         self.client.get(
#             f'/{host}:{port}/redfish/v1/Systems/system',
#             headers={"X-Auth-Token": self.authToken}, 
#             verify=False
#         )


# class PublicAPI(HttpUser):
#     wait_time = between(1, 2)

#     @task
#     def getJSON(self):
#         self.client.get(
#             '/jsonplaceholder.typicode.com/posts'
#         )

#     @task
#     def getWeather(self):
#         self.client.get(
#             '/wttr.in/Novosibirsk?format=j1'
#         )
