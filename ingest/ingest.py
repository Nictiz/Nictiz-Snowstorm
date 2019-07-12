import requests, json
from requests_toolbelt import MultipartEncoder
import time
import sys
from time import sleep

branchPath  = sys.argv[1]
shortName   = sys.argv[2]
fileName    = sys.argv[3]
serverUrl   = sys.argv[4]
importType  = sys.argv[5]

try:
    print("******************* Ingest: *******************\n")
    print("branchPath: {}".format(branchPath))
    print("shortName: {}".format(shortName))
    print("File name: {}".format(fileName))
    print("Server URL: {}".format(serverUrl))
    print("Import type: {}".format(importType))

    print("******************* BranchPath: *******************")
    url = 'http://{}/codesystems'.format(serverUrl)
    payload = "{ \
                    \"branchPath\": \""+branchPath+"\", \
                    \"shortName\": \""+shortName+"\" \
                }"
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=payload, headers=headers)
    # Get the reponse code
    string = str(r)
    responseCode = string[11:-2]
    # Response 201 > branch created successfully
    if responseCode == "201":
        print("Successfully created new branch [{}]\nCreating import job.".format(branchPath))
        url = 'http://{}/imports'.format(serverUrl)
        payload = '{ \
                    "branchPath": "'+branchPath+'", \
                    "createCodeSystemVersion": true, \
                    "type": "'+importType+'" \
                   }'
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(url, data=payload, headers=headers)

        headers = r.headers['location']
        importId = headers.split("/")
        importId = importId[-1]
        string = str(r)
        responseCode = string[11:-2]
        if responseCode == "201":
            print("\n******************* Import job creation: *******************")
            print("Successfully created import job [{}]".format(importId))
            fileLocation = fileName
            print("Uploading file [{}]".format(fileName))

            url = "http://{}/imports/{}/archive".format(serverUrl, importId)
            m = MultipartEncoder(
                fields={'file': (fileName, open(fileLocation, 'rb'), 'text/plain')}
            )
            r = requests.post(url, data=m,
                              headers={'Content-Type': m.content_type})
            startTime = time.time()
            while True:
                url = 'http://{}/imports/{}'.format(serverUrl, importId)
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                r = requests.get(url, headers=headers)
                r = r.json()

                stopWatch = time.time()
                runtime = round(stopWatch - startTime, 0)
                print("\n******************* Import job status: *******************")
                print("Import type:\t", r['type'])
                print("BranchPath:\t", r['branchPath'])
                print("Status:\t\t", r['status'])
                print("Runtime:\t", runtime, "seconds")
                if r['status'] == "FAILED":
                    print("\n******************* IMPORT ERROR *******************")
                    print("For more information, see the log files of the snowstorm process / container")
                    break
                if r['status'] == "COMPLETED":
                    print("\n******************* IMPORT SUCCESS *******************")
                    print("Duration:\t{} seconds")
                    print("For more information, see the log files of the snowstorm process / container")
                sleep(10)

    # Response 400 > branch exists
    if responseCode == "400":
        print("branchPath [{}] already exists - uploading".format(branchPath))
        url = 'http://{}/imports'.format(serverUrl)
        payload = '{ \
                    "branchPath": "'+branchPath+'", \
                    "createCodeSystemVersion": false, \
                    "type": "'+importType+'" \
                   }'
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(url, data=payload, headers=headers)

        headers = r.headers['location']
        importId = headers.split("/")
        importId = importId[-1]
        string = str(r)
        responseCode = string[11:-2]
        if responseCode == "201":
            print("\n******************* Import job creation: *******************")
            print("Successfully created import job [{}]".format(importId))
            fileLocation = fileName
            print("Uploading file [{}]".format(fileName))

            url = "http://{}/imports/{}/archive".format(serverUrl, importId)
            m = MultipartEncoder(
                fields={'file': (fileName, open(fileLocation, 'rb'), 'text/plain')}
            )
            r = requests.post(url, data=m,
                              headers={'Content-Type': m.content_type})

            startTime = time.time()

            while True:
                url = 'http://{}/imports/{}'.format(serverUrl, importId)
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                r = requests.get(url, headers=headers)
                r = r.json()

                stopWatch = time.time()
                runtime = round(stopWatch - startTime, 0)
                print("\n******************* Import job status: *******************")
                print("Import type:\t", r['type'])
                print("BranchPath:\t", r['branchPath'])
                print("Status:\t\t", r['status'])
                print("Runtime:\t", runtime, "seconds")
                if r['status'] == "FAILED":
                    print("\n******************* IMPORT ERROR *******************")
                    print("For more information, see the log files of the snowstorm process / container")
                    break
                if r['status'] == "COMPLETED":
                    print("\n******************* IMPORT SUCCESS *******************")
                    print("For more information, see the log files of the snowstorm process / container")
                    break
                sleep(10)
except:
    print("Some error has occurred during the import process.")

print("\n******************* All existing codesystems: *******************\n")
try:
    url = 'http://{}/codesystems'.format(serverUrl)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.get(url, headers=headers)
    response = json.loads(r.text)
    print(json.dumps(response, indent=4, sort_keys=True))
except:
    print("json: error")