from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import re
import os

def lambda_handler(event, context):
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

    target_url = os.getenv("CRAWLING_TARGET_URL")
    print("target_url: {}".format(target_url))
    driver.get(target_url)

    data = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(data, "lxml")
    print("data: {}".format(data))
    print("soup: {}".format(soup))

    driver.quit()
