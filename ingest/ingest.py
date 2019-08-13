import requests, json
from requests_toolbelt import MultipartEncoder
import time
import sys, os
from time import sleep

server_url   = sys.argv[1]
import_type  = sys.argv[2]

def import_release(branch_path, short_name, file_name, import_type, server_url):
    # Add the absolute path of the release in the container
    file_name = "/releases/"+file_name

    try:
        # Summarize received parameters
        print("******************* Ingest: *******************\n")
        print("branchPath: {}".format(branch_path))
        print("shortName: {}".format(short_name))
        print("File name: {}".format(file_name))
        print("Server URL: {}".format(server_url))
        print("Import type: {}".format(import_type))

        print("******************* BranchPath: *******************")
        payload = '{ "branchPath": "'+branch_path+'", "shortName": "'+short_name+'" }'
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(server_url+'/codesystems', data=payload, headers=headers)
        # Get the reponse code
        string = str(r)
        response_code = string[11:-2]
        # Response 201 > branch created successfully
        if response_code == "201":
            print("Successfully created new branch [{}]\nCreating import job.".format(branch_path))
            payload = '{ "branchPath": "'+branch_path+'", "createCodeSystemVersion": true, "type": "'+import_type+'" }'
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            r = requests.post(server_url+'/imports', data=payload, headers=headers)

            # Get the import job ID
            headers = r.headers['location']
            import_id = headers.split("/")
            import_id = import_id[-1]
            # Get the reponse code
            string = str(r)
            response_code = string[11:-2]
            if response_code == "201":
                print("\n******************* Import job creation: *******************")
                print("Successfully created import job [{}]".format(import_id))
                print("Uploading file [{}]".format(file_name))

                m = MultipartEncoder( fields={'file': (file_name, open(file_name, 'rb'), 'text/plain')})
                url = "{}/imports/{}/archive".format(server_url, import_id)
                r = requests.post(url, data=m, headers={'Content-Type': m.content_type})
                start_time = time.time()
                # Start infinite loop for import monitoring
                while True:
                    url = '{}/imports/{}'.format(server_url, import_id)
                    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                    r = requests.get(url, headers=headers)
                    r = r.json()

                    stop_watch = time.time()
                    runtime = round(stop_watch - start_time, 0)
                    print("\n******************* Import job status: *******************")
                    print("Import file:\t", file_name)
                    print("Import type:\t", r['type'])
                    print("BranchPath:\t", r['branchPath'])
                    print("Status:\t\t", r['status'])
                    print("Runtime:\t", runtime, "seconds")
                    if r['status'] == "FAILED":
                        print("\n******************* IMPORT ERROR *******************")
                        print("Import file:\t", file_name)
                        print("For more information, see the log files of the snowstorm process / container")
                        break
                    if r['status'] == "COMPLETED":
                        print("\n******************* IMPORT SUCCESS *******************")
                        print("Import file:\t", file_name)
                        print("Duration:\t{} seconds")
                        print("For more information, see the log files of the snowstorm process / container")
                        break
                    sleep(10)

        # Response 400 > branch exists
        if response_code == "400":
            print("branchPath [{}] already exists - uploading".format(branch_path))
            payload = '{ "branchPath": "'+branch_path+'", "createCodeSystemVersion": false, "type": "'+import_type+'" }'
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            r = requests.post(server_url+'/imports', data=payload, headers=headers)

            headers = r.headers['location']
            import_id = headers.split("/")
            import_id = import_id[-1]
            string = str(r)
            response_code = string[11:-2]
            if response_code == "201":
                print("\n******************* Import job creation: *******************")
                print("Successfully created import job [{}]".format(import_id))
                print("Uploading file [{}]".format(file_name))

                m = MultipartEncoder(fields={'file': (file_name, open(file_name, 'rb'), 'text/plain')})
                url = "{}/imports/{}/archive".format(server_url, import_id)
                r = requests.post(url, data=m, headers={'Content-Type': m.content_type})

                start_time = time.time()
                # Start infinite loop for import monitoring
                while True:
                    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                    r = requests.get(server_url+'/imports/'+import_id, headers=headers)
                    r = r.json()

                    stop_watch = time.time()
                    runtime = round(stop_watch - start_time, 0)
                    print("\n******************* Import job status: *******************")
                    print("Import file:\t", file_name)
                    print("Import type:\t", r['type'])
                    print("BranchPath:\t", r['branchPath'])
                    print("Status:\t\t", r['status'])
                    print("Runtime:\t", runtime, "seconds")
                    if r['status'] == "FAILED":
                        print("\n******************* IMPORT ERROR *******************")
                        print("Import file:\t", file_name)
                        print("For more information, see the log files of the snowstorm process / container")
                        break
                    if r['status'] == "COMPLETED":
                        print("\n******************* IMPORT SUCCESS *******************")
                        print("Import file:\t", file_name)
                        print("For more information, see the log files of the snowstorm process / container")
                        break
                    sleep(10)
    except Exception as e:
        print("An error has occurred during the import process.")
        print("Exception: ",e)
        print("Import file:\t", fileName)

# Check for a provided filename and codebase
try:
    file_name = sys.argv[3]
    code_base = sys.argv[4]
    short_name = sys.argv[5]
    import_release(code_base, short_name, file_name, import_type, server_url)
# Otherwise, use all .zip files in the folder
except:
    # List all release files in directory
    for file in os.listdir("/releases"):
        if file.endswith(".zip"):
            file = os.path.join("", file)
            import_release("MAIN", "SNOMEDCT", file, import_type, server_url)

        
print("\n******************* All existing codesystems: *******************\n")
try:
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.get(server_url+'/codesystems', headers=headers)
    response = json.loads(r.text)
    print(json.dumps(response, indent=4, sort_keys=True))
except Exception as e:
    print("json: error")
    print("Exception: ",e)