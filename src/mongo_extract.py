from pymongo import MongoClient
import csv
import boto3
import datetime
from datetime import timedelta
import configparser

# mongo_config 값을 로드

parser = configparser.ConfigParser()
parser.read("../pipeline.conf")
hostname = parser.get("mongo_config", "hostname")
username = parser.get("mongo_config", "username")
password = parser.get("mongo_config", "password")
database_name= parser.get("mongo_config", "database")
collection_name = parser.get("mongo_config", "collection")

mongo_client = MongoClient("mongodb+srv://" + username 
                           + ":" + password 
                           + "@" + hostname 
                           + "/" + database_name 
                           + "?retryWrites=true&" 
                           + "w=majority&ssl=true&" 
                           + "ssl_cert_reqs=CERT_NONE")

# 컬렉션이 위치한 db에 연결
mongo_db = mongo_client[database_name]

# 문서를 쿼리할 컬렉션을 선택
mongo_collection = mongo_db[collection_name]

start_date = datetime.datetime.today() + timedelta(days = -1)
end_date = start_date + timedelta(days = 1)

mongo_query = { "$and" : [ { "event_timestamp" : { "$gte" : start_date } }, { "event_timestamp" : { "$lt" : end_date } } ] }

event_docs = mongo_collection.find(mongo_query, batch_size = 3000)

# 결과를 저장할 빈 리스트를 생성

all_events = []

# 커서를 통해 반복 작업

for doc in event_docs :
  # 기본 값을 포함
  event_id = str(doc.get("event_id", -1))
  event_timestamp = doc.get("event_timestamp", None)
  event_name = doc.get("event_name", None)

  # 리스트에 모든 이벤트 속성을 추가

  current_event = []
  current_event.append(event_id)
  current_event.append(event_timestamp)
  current_event.append(event_name)

  # 이벤트의 최종 리스트에 이벤트를 추가

  all_events.append(current_event)

export_file = "events_export.csv"

with open(export_file, 'w') as fp :
  csvw = csv.writer(fp, delimiter = "|")
  csvw.writerows(all_events)

fp.close()

# aws_boto_credentials 값을 로드

parser = configparser.ConfigParser()
parser.read("../pipeline.conf")
access_key = parser.get("aws_boto_credentials", "access_key")
secret_key = parser.get("aws_boto_credentials", "secret_key")
bucket_name = parser.get("aws_boto_credentials", "bucket_name")

s3 = boto3.client("s3", aws_access_key_id = access_key, aws_secret_access_key = secret_key)

s3_file = export_file

s3.upload_file(export_file, bucket_name, s3_file)