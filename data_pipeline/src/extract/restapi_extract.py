import requests
import json
import configparser
import csv
import boto3

lat = 42.36
lon = 71.05
lat_log_params = {"lat" : lat, "lon" : lon}

api_response = requests.get("http://api.open-notify.org/iss-pass.json", params=lat_log_params)

# 응답 내용에서 json 객체 생성

response_json = json.loads(api_response.content)

all_passes = []
for response in response_json['response'] :
  current_pass = []

  # 요청에서 위도/경도를 저장
  
  current_pass.append(lat)
  current_pass.append(lon)

  # 통과 시 지속 시간과 상승 시간을 저장

  current_pass.append(response['duration'])
  current_pass.append(response['risetime'])

  all_passes.append(current_pass)

export_file = "export_file.csv"

with open(export_file, 'w') as fp :
  csvw = csv.writer(fp, delimiter='|')
  csvw.writerows(all_passes)

fp.close()

# aws_boto_credentials 값을 로드

parser = configparser.ConfigParser()
parser.read("../pipeline.conf")
access_key = parser.get('aws_boto_credentials', 'access_key')
secret_key = parser.get('aws_boto_credentials', 'secret_key')
bucket_name = parser.get('aws_boto_credentials', 'bucket_name')

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

s3.upload_file(export_file, bucket_name, export_file)