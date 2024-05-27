import pytest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from login_page import LoginPage

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    yield driver
    driver.quit()

def get_test_data():
    df = pd.read_excel("test_data.xlsx")
    return df

def update_test_result(test_id, result):
    df = pd.read_excel("test_data.xlsx")
    df.loc[df['Test ID'] == test_id, 'Test Result'] = result
    df.to_excel("test_data.xlsx", index=False)

def test_login(driver):
    test_data = get_test_data()
    for index, row in test_data.iterrows():
        login_page = LoginPage(driver)
        login_page.enter_username(row['Username'])
        login_page.enter_password(row['Password'])
        login_page.click_login_button()

        # Check login success by verifying the presence of a logout button
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='/web/index.php/auth/logout']"))
            )
            update_test_result(row['Test ID'], 'Passed')
            driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        except:
            update_test_result(row['Test ID'], 'Failed')
