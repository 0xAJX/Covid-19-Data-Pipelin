from datetime import datetime, timezone
import json
from os import listdir
from os.path import isfile, join
import boto3
import urllib3

LOCAL_FILE_SYS = "/tmp"
S3_BUCKET = ""

def lambda_handler(event, context):

    try:
        file_name = download_data()

        s3_client = boto3.client("s3")
        key = _get_key()

        files = [f for f in listdir(LOCAL_FILE_SYS) if isfile(join(LOCAL_FILE_SYS, f))]
        for f in files:
            s3_client.upload_file(LOCAL_FILE_SYS + "/" + f, S3_BUCKET, key + f)

    except:
        return {
            'statusCode': 400,
            'body': "Faliure"
        }

    return {
        'statusCode': 200,
        'body': "Success"
    }

def get_data(get_path="https://api.covidtracking.com/v1/us/daily.json"):
    http = urllib3.PoolManager()
    try:
        r = http.request(
            "GET",
            get_path,
            retries=urllib3.util.Retry(3),
        )
        if r.status == 200:
            data = r.data
            print(data)
    except KeyError as e:
        print(f"Wrong format url {get_path}", e)
    except urllib3.exceptions.MaxRetryError as e:
        print(f"API unavailable at {get_path}", e)
    return data

def write_to_local(data, part="test", loc="/tmp"):
    dt_now = datetime.now(tz=timezone.utc)
    file_name = loc + "/" + str(part) + "-" + dt_now.strftime("%Y-%m-%d") + "-" + dt_now.strftime("%H") + "-" + dt_now.strftime("%M") + "-" + dt_now.strftime("%M")
    with open(file_name, "w") as file:
        file.write(data)
    return file_name


def download_data():
    data = get_data()
    return write_to_local(json.dumps(json.loads(data)))

# def _get_key():
#     dt_now = datetime.now(tz=timezone.utc)
#     KEY = (
#         dt_now.strftime("%Y-%m-%d")
#         + "/"
#         + dt_now.strftime("%H")
#         + "/"
#         + dt_now.strftime("%M")
#         + "/"
#     )
#     return KEY

def _get_key():
    dt_now = datetime.now(tz=timezone.utc)
    KEY = (
            dt_now.strftime("%Y-%m-%d")
            + "/"

    )
    return KEY