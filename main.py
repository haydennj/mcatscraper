from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import selenium.webdriver.support.expected_conditions as EC
import time
import vonage
import datetime

client = vonage.Client(key="b971b598", secret="02hxwYFjOSUrUK8z")
sms = vonage.Sms(client)

# Press the green button in the gutter to run the script.
def check_login(driver):
    if 'login' not in driver.current_url:
        return
    USERNAME = "haydennj"
    PASSWORD = "Ee271828!@"
    driver.find_element(By.CSS_SELECTOR, "input[name='IDToken1']").send_keys(USERNAME)
    driver.find_element(By.ID, "password-field").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-btn").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.ID, "dashboard_registration_info_tile")))
    print("Successfully logged in")
    # driver.close()


def navigate_to_scheduling(driver):
    driver.find_element(By.ID, "dashboard_registration_info_tile").find_element(By.TAG_NAME, "button").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.ID, "RPPoliciesForm")))
    driver.find_element(By.ID, "nextButton").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.ID, "testCenterFormId")))
    return


def search_exams(driver):
    ADDRESS = "Washington, D.C."
    driver.find_element(By.ID, "testCentersNearAddress").clear()
    driver.find_element(By.ID, "testCentersNearAddress").send_keys(ADDRESS)
    driver.find_element(By.ID, "preferredDateShown").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.ID, "ui-datepicker-div")))
    driver.find_element(By.ID, "ui-datepicker-div").find_element(By.CSS_SELECTOR, "a[aria-label='Friday 27th of May 2022']").click()
    driver.find_element(By.ID, "addressSearch").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.ID, "testCenterListTable")))
    testCenterList = driver.find_element(By.ID, "testCenterListTable")
    testCenters = testCenterList.find_elements(By.TAG_NAME, "tr")
    filename = "/Users/haydenn/Desktop/mcatbot/" + str(time.time()) + ".txt"
    file = open(filename, "w")
    for testCenter in testCenters[0:5]:
        name = testCenter.find_element(By.CLASS_NAME, "tc_name").text
        address = testCenter.find_element(By.CLASS_NAME, "tc_address").text
        available = False
        try:
            driver.find_element(By.CLASS_NAME, "none-available")
        except NoSuchElementException:
            available = True
        if available:
            response = sms.send_message({
                "from": "18444006072",
                "to": "19143125913",
                "text": "NEW TEST CENTER AVAILABLE\n" + name + "\n" + "address" + "\n" + "AVAILABLE: " + str(available)
            })
            if response["messages"][0]["status"] == "0":
                print("Message sent successfully")
            else:
                print(f"Message failed with error: {response['messages'][0]['error-text']}")
        file.write(name + '\n')
        file.write(address + '\n')
        file.write("Available: " + str(available))
        file.write('\n\n')
    driver.close()


if __name__ == '__main__':
    while True:
        try:
            options = webdriver.FirefoxOptions()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            url = 'https://mcat.aamc.org/mrs/#/dashboard/14854873'
            driver.get(url)
            time.sleep(5)
            check_login(driver)
            navigate_to_scheduling(driver)
            search_exams(driver)
        except Exception:
            print("EXCEPTION OCCURRED")
            continue
        time.sleep(300)
