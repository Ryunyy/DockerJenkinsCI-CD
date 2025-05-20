import pytest
import requests
import json
import time
from loguru import logger

#local variables
host = '0.0.0.0'
port = 2443
userName = 'root'
userPass = '0penBmc'

#path for log file
logPath = '/home/svyat/Desktop/pytests/logs.log'
logger.add(logPath, level='DEBUG')

#fixture creating connection. disassemble headers and return bundle of status code and auth token
@pytest.fixture(scope="session")
def create_session():
    response = requests.post(f'https://{host}:{port}/redfish/v1/SessionService/Sessions', json={"UserName":userName, "Password":userPass}, verify=False)
    jdata = response.headers
    logger.info(jdata)

    try:
        authToken = jdata['X-Auth-Token']
        logger.info('Auth token = ' + str(authToken))
        if authToken == "":
            logger.debug("Couldn't get auth token")
    except: 
        logger.debug("Response headers: 'X-Auth-Token' - no such element in response!")

    responseBundle = [response.status_code, authToken]
    return responseBundle

#test case for successful authentification
def test_case_SUCCESS_AUTH(create_session):
    errors = []
    logger.info(10*'-' + 'TEST CASE SUCCESS AUTH' + 10*'-')
    response = create_session
    actualResponseCode = response[0]
    expectedResponseCode = 201

    logger.info('Expected response code = ' + str(expectedResponseCode))
    logger.info('Actual response code = ' + str(actualResponseCode))
    if not actualResponseCode == expectedResponseCode:
        logger.debug(f'Response code is not equal {expectedResponseCode}')
        errors.append("Error")
    
    if response[1] == "":
        errors.append("Error")
    else:
        logger.info('Auth Token = ' + response[1])

    if errors:
        logger.info(10*'-' + 'TEST CASE FAILED' + 10*'-')
    else:
        logger.info(10*'-' + 'TEST CASE PASSED' + 10*'-')

    assert not errors


#test case for getting system information
def test_case_GET_SYSINFO(create_session):
    errors = []
    logger.info(10*'-' + 'TEST CASE GET SYSINFO' + 10*'-')
    authToken = create_session[1]
    logger.info('Auth Token = ' + authToken)

    response = requests.get(f'https://{host}:{port}/redfish/v1/Systems/system', headers={"X-Auth-Token":authToken}, verify=False)
    actualResponseCode = response.status_code
    expectedResponseCode = 200

    logger.info('Expected response code = ' + str(expectedResponseCode))
    logger.info('Actual response code = ' + str(actualResponseCode))
    if not actualResponseCode == expectedResponseCode:
        logger.debug(f'Response code is not equal {expectedResponseCode}')
        errors.append("Error")

    jdata = json.loads(response.text)
    logger.info(jdata)

    try:
        powerStatus = jdata['PowerState']
        logger.info('Power state = ' + str(powerStatus))
        if powerStatus == "":
            logger.debug("Couldn't get power state")
            errors.append("Error")
    except: 
        logger.debug("Response text: 'PowerState' - no such element in response!")
        errors.append("Error")

    try:
        state = jdata['Status']
        logger.info('Status = ' + str(state))
        if state == "":
            logger.debug("Couldn't get Status")
            errors.append("Error")
    except: 
        logger.debug("Response text: 'Status' - no such element in response!")
        errors.append("Error")

    if errors:
        logger.info(10*'-' + 'TEST CASE FAILED' + 10*'-')
    else:
        logger.info(10*'-' + 'TEST CASE PASSED' + 10*'-')

    assert not errors


#test case for execution power management commands
def test_case_POWER_MANAGEMENT(create_session):
    errors = []
    logger.info(10*'-' + 'TEST CASE POWER MANGEMENT' + 10*'-')
    authToken = create_session[1]
    logger.info('Auth Token = ' + authToken)

    response1 = requests.post(f'https://{host}:{port}/redfish/v1/Systems/system/Actions/ComputerSystem.Reset', headers={"X-Auth-Token":authToken}, json={"ResetType":"On"}, verify=False)
    actualResponseCode = response1.status_code
    expectedResponseCode = 204

    logger.info('Expected response code = ' + str(expectedResponseCode))
    logger.info('Actual response code = ' + str(actualResponseCode))
    response2 = requests.get(f'https://{host}:{port}/redfish/v1/Systems/system', headers={"X-Auth-Token":authToken}, verify=False)
    if not actualResponseCode == expectedResponseCode:
        logger.debug(f'Response code is not equal {expectedResponseCode}')
        errors.append("Error")

    
    jdata = json.loads(response2.text)
    logger.info(jdata)

    try:
        powerStatus = jdata['PowerState']
        logger.info('Power state = ' + str(powerStatus))
        if powerStatus == "":
            logger.debug("Couldn't get power state")
            errors.append("Error")
        if powerStatus != "On" and powerStatus != "PoweringOn":
            logger.debug("Power state not match")
            errors.append("Error")
    except: 
        logger.debug("Response text: 'PowerState' - no such element in response!")
        errors.append("Error")

    if errors:
        logger.info(10*'-' + 'TEST CASE FAILED' + 10*'-')
    else:
        logger.info(10*'-' + 'TEST CASE PASSED' + 10*'-')

    assert not errors