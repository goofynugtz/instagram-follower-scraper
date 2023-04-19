import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
from decouple import config

USERNAME = config('IG_USERNAME')
PASSWORD = config('IG_PASSWORD')
TIMEOUT = 15

class scraper_client():
  def __init__(self, username=USERNAME, password=PASSWORD) -> None:
    self.username = username
    self.password = password
    self.follower_accounts = set()
    self.following_accounts = set()
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
      "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    self.bot = webdriver.Chrome(executable_path=CM().install(), options=options)

  def login(self):
    print("[Info] - Logging in...")  
    username = WebDriverWait(
      self.bot, 10).until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(
      self.bot, 10).until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR, "input[name='password']")))
    username.clear()
    username.send_keys(USERNAME)
    password.clear()
    password.send_keys(PASSWORD)
    button = WebDriverWait(
      self.bot, 2).until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR, "button[type='submit']"))).click()

  def scrape_followers(self, usr, no_of_followers):
    self.bot.get('https://www.instagram.com/{}/'.format(usr))
    time.sleep(3.5)
    WebDriverWait(self.bot, TIMEOUT).until(
      EC.presence_of_element_located((
        By.XPATH, "//a[contains(@href, '/followers')]"))).click()
    time.sleep(2)
    print('[Info] - Scraping followers...')
    self.follower_accounts.clear()
    print(no_of_followers)
    for _ in range(round(no_of_followers // 20)):
      ActionChains(self.bot).send_keys(Keys.END).perform()
      time.sleep(1)
    followers = self.bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")
  
    # Getting url from href attribute
    for i in followers:
      if i.get_attribute('href'):
        self.follower_accounts.add(i.get_attribute('href').split("/")[3])
      else:
        continue
    print('[Info] - Saving...')
    print('[DONE] - Your followers are saved in followers.txt file!')
    with open('followers.txt', 'w') as file:
      file.write('\n'.join(self.follower_accounts) + "\n")

  def scrape_following(self, usr, no_of_followings):
    self.bot.get('https://www.instagram.com/{}/'.format(usr))
    time.sleep(3.5)
    WebDriverWait(self.bot, TIMEOUT).until(
      EC.presence_of_element_located((
        By.XPATH, "//a[contains(@href, '/following')]"))).click()
    time.sleep(2)
    print('[Info] - Scraping following...')
    self.following_accounts.clear()
    print(no_of_followings)
    for _ in range(round(no_of_followings // 20)):
      ActionChains(self.bot).send_keys(Keys.END).perform()
      time.sleep(1)
    following = self.bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")

    # Getting url from href attribute
    for i in following:
      if i.get_attribute('href'):
        self.following_accounts.add(i.get_attribute('href').split("/")[3])
      else:
        continue
    print('[Info] - Saving...')
    print('[DONE] - Your following are saved in following.txt file!')
    with open('following.txt', 'w') as file:
      file.write('\n'.join(self.following_accounts) + "\n")


  def scrape_difference(self):
    if (len(self.following_accounts) > len(self.follower_accounts)):
      no_followbacks = self.following_accounts - self.follower_accounts
    else:
      no_followbacks = self.follower_accounts - self.following_accounts

    print('[Info] - Saving...')
    print('[DONE] - Accounts not following/followed back are saved in difference.txt file!')
    with open('difference.txt', 'w') as file:
      file.write('\n'.join(no_followbacks) + "\n")

  def scrape(self):
    usr = self.username
    no_of_followers = 2
    no_of_followings = 7
    self.bot.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)
    #check for cookies 
    try:
      element = self.bot.find_element(By.XPATH,"/html/body/div[4]/div/div/div[3]/div[2]/button")
      element.click()
    except NoSuchElementException:
      print("[Info] - Instagram did not require to accept cookies this time.")

    self.login()
    time.sleep(10)
    self.scrape_followers(usr, no_of_followers)
    self.scrape_following(usr, no_of_followings)
    self.scrape_difference()


if __name__ == '__main__':
  ig = scraper_client(USERNAME, PASSWORD)
  ig.scrape()