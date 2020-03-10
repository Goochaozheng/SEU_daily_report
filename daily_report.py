from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import sys
import getopt
import traceback

def main(argv):

    if len(argv) != 4:
        print("Insufficient arguments")
        print("Usage: daily_report.py -u <user_id> -p <password>")
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "u:p:")
    except:
        print("Incorrect arguments")
        print("Usage: daily_report.py -u <user_id> -p <password>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-u':
            userid = arg
        elif opt == '-p':
            password = arg


    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/index.do?t_s=1583651212299#/dailyReport")

    print("Enter login page")
    WebDriverWait(driver, 60, 1).until(expected_conditions.visibility_of_element_located((By.ID, "username")))

    driver.find_element_by_id("username").send_keys(userid)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_xpath("//button[@type='submit']").click()

    #Refresh if timeout or exception
    for i in range(5):
        try:
            WebDriverWait(driver, 60, 1).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@data-action='add']")))
            print("Login successfully as %s" % userid)

            driver.find_element_by_xpath("//div[@data-action='add']").click()

            try:
                WebDriverWait(driver, 60, 1).until(expected_conditions.visibility_of_element_located((By.XPATH, "//p[@data-name='USER_ID']")))
            except Exception as e:
                if expected_conditions.visibility_of_element_located((By.XPATH, "//a[@class='bh-dialog-btn bh-bg-primary bh-color-primary-5']")):
                    print("Already reported")
                    sys.exit()
                else:
                    raise e
            print("Adding data")

            driver.find_element_by_xpath("//div[@data-action='save']").click()
            WebDriverWait(driver, 60, 1).until(expected_conditions.visibility_of_element_located((By.XPATH, "//a[@class='bh-dialog-btn bh-bg-primary bh-color-primary-5']")))
            driver.find_element_by_xpath("//a[@class='bh-dialog-btn bh-bg-primary bh-color-primary-5']").click()
            print("Save success")
            sys.exit()

        except Exception as e:
            traceback.print_ecx()
            print("..refresh")
            driver.refresh()
            continue
        break


if __name__ == "__main__":
    main(sys.argv[1:])
