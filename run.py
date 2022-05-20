import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM

# Complete these 2 fields ==================
USERNAME = 'YOUR USERNAME'
PASSWORD = 'YOUR PASSWORD'
# Make sure to remove 2 factor authentication for a short while.
# ==========================================

TIMEOUT = 15

def login(bot):
    user_element = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')))

    user_element.send_keys(USERNAME)
    pass_element = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')))
    
    pass_element.send_keys(PASSWORD)
    login_button = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[6]/button')))

    time.sleep(0.4)
    login_button.click()
    time.sleep(5)


follower_accounts = set()
following_accounts = set()


def scrape_followers(bot, usr, no_of_followers):
    bot.get('https://www.instagram.com/{}/'.format(usr))
    time.sleep(3.5)
    WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="react-root"]/section/main/div/ul/li[2]/a'))).click()
    time.sleep(2)
    print('[Info] - Scraping followers...')
    follower_accounts.clear()

    for _ in range(round(no_of_followers // 10)):
        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(2)
        followers = bot.find_elements_by_xpath(
            '//*[@id="react-root"]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')
        # Getting url from href attribute
        for i in followers:
            if i.get_attribute('href'):
                follower_accounts.add(i.get_attribute('href').split("/")[3])
            else:
                continue

    print('[Info] - Saving...')
    print('[DONE] - Your followers are saved in followers.txt file!')
    with open('followers.txt', 'w') as file:
        file.write('\n'.join(follower_accounts) + "\n")


    
def scrape_followings(bot, usr, no_of_followings):
    bot.get('https://www.instagram.com/{}/'.format(usr))
    time.sleep(3.5)
    WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="react-root"]/section/main/div/ul/li[3]/a'))).click()
    time.sleep(2)
    print('[Info] - Scraping followings...')
    following_accounts.clear()

    for _ in range(round(no_of_followings // 10)):
        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(2)
        followings = bot.find_elements_by_xpath(
            '//*[@id="react-root"]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')
        # Getting url from href attribute
        for i in followings:
            if i.get_attribute('href'):
                following_accounts.add(i.get_attribute('href').split("/")[3])
            else:
                continue

    print('[Info] - Saving...')
    print('[DONE] - Your followings are saved in followings.txt file!')
    with open('followings.txt', 'w') as file:
        file.write('\n'.join(following_accounts) + "\n")



def scrape_difference():
    if (len(following_accounts) > len(follower_accounts)):
        no_followbacks = following_accounts - follower_accounts
    else:
        no_followbacks = follower_accounts - following_accounts


    print('[Info] - Saving...')
    print('[DONE] - Accounts not following/followed back are saved in difference.txt file!')
    with open('difference.txt', 'w') as file:
        file.write('\n'.join(no_followbacks) + "\n")



def scrape():
    usr = input('[Required] - Whose data do you want to scrape: ')
    no_of_followers = int(
        input('[Required] - How many followers do you want to scrape: '))
    no_of_followings = int(
        input('[Required] - How many followings do you want to scrape: '))

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    bot = webdriver.Chrome(executable_path=CM().install(), options=options)
    bot.set_window_size(600, 1000)

    bot.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)

    print("[Info] - Logging in...")
    login(bot=bot)

    scrape_followers(bot, usr, no_of_followers)
    scrape_followings(bot, usr, no_of_followings)
    scrape_difference()


if __name__ == '__main__':
    scrape()
