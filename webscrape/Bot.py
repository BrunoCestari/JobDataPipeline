import boto3
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, time
import subprocess
import os
import requests
from atexit import register
from pyvirtualdisplay import Display

#Exclude display line if need run with Chrome Graphical Inteface
display = Display(visible=0, size=(1024, 768))
display.start()

       

max_time = 10
print('')
def open_chrome(port=4444):
    my_env = os.environ.copy()
    print('opening chrome (Linux)')
    subprocess.Popen(
        f'google-chrome --remote-debugging-port={port} --user-data-dir=data_dir'.split(), env=my_env)
    print('open chrome')

class Bot():
    def __init__(self, port_no=4444, headless=False, verbose=False):
        print('initialising bot')

        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-application-cache")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-setuid-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            
            
        else:
            open_chrome()
        # attach to the same port that you're running chrome on

        # without this, the chrome webdriver can't start (SECURITY RISK)
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')

       # Attach to the same port that you're running chrome on
       # options.add_experimental_option(
       #     f"debuggerAddress", f"127.0.0.1:{port_no}")
       # options.add_argument("--windows-size=1920x1080")
        self.driver = webdriver.Chrome(service=Service(),options=options)
        
        print("worked")
        self.verbose = verbose   

# Rest of your Bot class methods


    def scroll(self, x=0, y=10000):
        self.driver.execute_script(f'window.scrollBy({x}, {y})')

    def click_btn(self, text):
        if self.verbose:
            print(f'clicking {text} btn')
        element_types = ['button', 'div', 'input', 'a', 'label']
        for element_type in element_types:
            btns = self.driver.find_elements_by_xpath(f'//{element_type}')
            # for btn in btns:
            #      print(btn.text)

            # SEARCH BY TEXT
            try:
                btn = [b for b in btns if b.text.lower() == text.lower()][0]
                btn.click()
                return
            except IndexError:
                pass

            # SEARCH BY VALUE ATTRIBUTE IF NOT YET FOUND
            try:
                btn = self.driver.find_elements_by_xpath(
                    f'//{element_type}[@value="{text}"]')[0]
                btn.click()
                return
            except:
                continue

        raise ValueError(f'button containing "{text}" not found')

    def _search(self, query, _type='search', placeholder=None):
        sleep(1)
        input_elements = self.driver.find_elements_by_xpath(f'//input[@type="{_type}"]')
        print(input_elements)
        if placeholder:
            input_element = [i for i in input_elements if i.get_attribute('placeholder').lower() == placeholder.lower()][0]
        else:
            input_element = input_elements[0]
        input_element.send_keys(query)

    def toggle_verbose(self):
        self.verbose = not self.verbose

    def download_file(self, src_url, local_destination):
        response = requests.get(src_url)
        with open(local_destination, 'wb+') as f:
                  f.write(response.content)
    def s3_upload(self, obj, filename):
        s3 = boto3.resource('s3')
        s3.Object(key=filename).put(Body=json.dump(obj))

    def __exit__ (self, exec_type, exec_value, traceback):
        self.driver.quit()      