from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import re
import os

def lambda_handler(event, context):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"

    service_args = ['--ignore-ssl-errors=yes']
    task_root = os.getenv("LAMBDA_TASK_ROOT")
    paths = "{}/phantomjs".format(task_root)
    print(paths)

    driver = webdriver.PhantomJS(
        executable_path=paths,
        desired_capabilities={
            'phantomjs.page.settings.userAgent': USER_AGENT,
        },
        service_args=service_args,
        service_log_path=os.path.devnull
    )

    target_url = os.getenv("CRAWLING_TARGET_URL")
    driver.get(target_url)

    data = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(data, "lxml")

    for div in soup.find_all(class_=re.compile("card")):
        print(div)
        print(div.find_all(class_=re.compile("placement_status")))

    driver.quit()
