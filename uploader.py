from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from omegaconf import OmegaConf
import time
import os


DIR = os.getcwd().replace("/build/exe.linux-x86_64-3.9/", "")
CFG = OmegaConf.load(f'{DIR}/config/linkedin.yaml')


def login(driver: webdriver) -> None:
    driver.get("https://www.linkedin.com?l=en_EN")

    driver.find_element(By.ID, "session_key").send_keys(CFG.account.email)
    driver.find_element(By.ID, "session_password").send_keys(CFG.account.pw)
    driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()


def upload_image(driver: webdriver) -> None:
    driver.get(CFG.account.profile_url)
    driver.find_element(By.XPATH, "//button[@class='artdeco-button artdeco-button--circle artdeco-button--inverse artdeco-button--1 artdeco-button--primary ember-view']").click()
    driver.find_element(By.XPATH, "//input[@type='file']").send_keys(f"{DIR}/plots/BTCEUR.png")
    time.sleep(2) #wait to upload the plot 
    driver.find_element(By.XPATH, "//button[@class='background-image-cropper__apply-action artdeco-button artdeco-button--2 artdeco-button--primary ember-view']").click()


def main() -> None:
    options = Options()
    options.add_argument('--headless')
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(options=options, service=service)
    #service = Service(executable_path=ChromeDriverManager().install())
    #driver = webdriver.Chrome(options=options, service=service)
    login(driver)
    upload_image(driver)
    driver.quit()


if __name__ == "__main__":
    main()