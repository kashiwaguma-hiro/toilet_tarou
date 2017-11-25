from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import re
import os
import boto3
from datetime import datetime as dt


def get_content(target_url):
    paths = "{}/phantomjs".format(os.getenv("LAMBDA_TASK_ROOT"))

    service_args = ['--ignore-ssl-errors=yes']
    driver = webdriver.PhantomJS(
        executable_path=paths,
        desired_capabilities={
            'phantomjs.page.settings.userAgent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        },
        service_args=service_args,
        service_log_path=os.path.devnull        
    )
    print("target_url: {}".format(target_url))
    driver.get(target_url)

    data = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(data, "lxml")
    print(soup.title.string)
    return soup.prettify()


def create_html_file(content):
    tmp_dir = '/tmp/'

    cur_ts = dt.now().strftime('%Y%m%d_%H%M%S')
    file_path = tmp_dir + 'cur_ts.html'
    with open(file_path, 'w') as file:
        file.write(content)
    return file_path


def upload_text_s3bucket(upload_file_path, s3_bucket, key):
    print("upload text. file_path:{}, upload_s3_bucket:{}, key:{}".format(upload_file_path, s3_bucket, key))
    bucket = boto3.resource('s3').Bucket(s3_bucket)
    bucket.upload_file(upload_file_path, key)


def lambda_handler(event, context):

    current_dt = dt.now().strftime('%Y%m%d%H%M%S')
    upload_s3_bucket = os.getenv("UPLOAD_S3_BUCKET")
    target_url = os.getenv("CRAWLING_TARGET_URL")
    target_url_without_slash = target_url.replace("/", "_")

    # get content
    content = get_content(target_url)

    # save
    saved_file_path = create_html_file(content)

    # upload
    upload_text_s3bucket(saved_file_path, upload_s3_bucket, "crawling_result/{}/{}.html".format(target_url_without_slash, current_dt))