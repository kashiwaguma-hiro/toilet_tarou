import boto3
import botocore
import os
from bs4 import BeautifulSoup

S3_LIST_OBJECT_PAGING_SIZE=600
# MAX_PARSE_SIZE=600
MAX_PARSE_SIZE=1

def resume(s3_bucket_name, prefix):
    s3 = boto3.resource('s3')

    try :
        obj = s3.Object(s3_bucket_name, "{}/_latest".format(prefix))
        response = obj.get()
        body = response['Body'].read()
        bodyStr = body.decode('utf-8')
        return bodyStr

    except botocore.exceptions.ClientError as e:
        print(type(e))
        print(e)

    return None

def fetch_file_paths(s3_bucket_name, latest_file_path, max_size):

    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')
    paginationConfig = {'MaxItems': max_size, 'StartingToken': latest_file_path, 'PageSize': S3_LIST_OBJECT_PAGING_SIZE}
    page_iterator = paginator.paginate(Bucket=s3_bucket_name, PaginationConfig=paginationConfig)

    for page in page_iterator:
        for item in page['Contents']:
            yield item['Key']

def load_content(s3_bucket, path):
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket, path)
    
    response = obj.get()
    body = response['Body'].read()
    body_str = body.decode('utf-8')
    return body_str

def parse(key, content):
    datetime=os.path.splitext( os.path.basename(key))[0]
    soup = BeautifulSoup(content, "lxml")
    print(soup)

    placement_name=""
    return [
            key,      # key(filepath)
            datetime, # 日付
            placement_name, # 何階の
            "d", # どのトイレ
            "e",  #トイレのタイプ
            "f", # 開いてるかどうか(boolean)
            "g", # 何分あいて無いか
            ]

def register(toilet_info):
    pass

def record_latest(latest_file_path):
    # 最後に処理したファイルを記録する
    print("latest:{}".format(latest_file_path))


def lambda_handler(event, context):
    # TODO 環境変数化
    target = "https:__toilet.mono-connect.jp_u_dmm7248_location_145_placement_307"
    s3_bucket_name="toilet-man"

    latest_file_path = resume(s3_bucket_name, target)

    for file_path in fetch_file_paths(s3_bucket_name, latest_file_path, MAX_PARSE_SIZE):
        content = load_content(s3_bucket_name, file_path)

        toilet_info = parse(file_path, content)

        register(toilet_info)

        latest_file_path = file_path

    record_latest(latest_file_path)
