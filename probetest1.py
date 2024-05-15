
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

email = ""
password = ""
chromedriver_autoinstaller.install() 
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
#wep browser get the facebook
driver.get('https://m.facebook.com/')
#filling info about login stuff
email_input = driver.find_element(By.XPATH,'//*[@id="m_login_email"]')
email_input.send_keys(email)
password_input = driver.find_element(By.XPATH,'//*[@id="m_login_password"]')
password_input.send_keys(password)
# login success
login_btn = driver.find_element(By.XPATH,'//*[@id="u_0_5_t0"]')
login_btn.click()
# wait.until(EC.url_changes('https://m.facebook.com/'))
# driver.get('https://m.facebook.com/')
# #finding search box
# search_box = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div/div[1]/div[3]/div/div/div[1]/div/div[2]/div')
# post_input = search_box.find_element_by_xpath('..')
# post_input.click()
# driver.quit()