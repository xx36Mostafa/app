import os
import random
import re
from playwright.sync_api import sync_playwright
import sys
import time , names
from twocaptcha import TwoCaptcha
import threading
import base64
import phone_iso3166.country as countries
import phonenumbers , pycountry
from colorama import Fore,Style,init
from TempMail import TempMail
init(strip=not sys.stdout.isatty())
os.system('cls')

class bot():
    def __init__(self,number,mode,mode_proxy,proxies,mode_call):
        self.number = number
        self.mode = mode
        self.proxy,self.mode_proxy = proxies,mode_proxy
        self.mode_call = mode_call
        self.captcha = open('captcha.txt','r').read()
        self.random_numbers = random.sample(range(1000), 1)
        ########################
        if self.mode == "1":
            self.mode = True
        else:
            self.mode = False
        # Get Info Phone
        test = "+" + str(self.number)
        x = phonenumbers.parse(test)
        phone_number = x.national_number
        countriess = x.country_code
        self.cnt = countries.phone_country(test)
        phonenumber = str(phone_number)
        self.phone = phonenumber
        # Get Email
        # Get Mail
        while True:
            self.inbox = TempMail.generateInbox()
            self.address = self.inbox.address
            check_add = self.address.split('@')
            if check_add[1] == 'inactivemachine.com' or check_add[1] == 'beaconmessenger.com':
                break
    def start(self):
        with sync_playwright() as playwright:
            try:
                if self.mode_proxy == '1':
                    driver = playwright.firefox.launch(proxy={
                        "server": f"http://{self.proxy}"},
                        headless=self.mode)
                else:
                    driver = playwright.firefox.launch(headless=self.mode)
                self.context = driver.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1")
                page = self.context.new_page()
                page.set_default_timeout(20000)
                page.goto('https://appleid.apple.com/account')
                try:
                    self.filldata(page)
                except Exception as e:
                    print(f"{Fore.RED} Failed >>> {self.number}")
            except:
                pass

    def random_names(self):
        nums = str(random.randint(0,999)+1)
        fname = f'{names.get_first_name()}'
        lname = f'{names.get_last_name()}'
        return {
            'fname': fname, 'lname': lname
        }

    def filldata(self,browser):
        self.browser = browser
        try:
            namesObject = self.random_names()
            fname = str(namesObject['fname'])
            lname = str(namesObject['lname'])
            self.browser.wait_for_selector('//input[@class="generic-input-field   form-textbox form-textbox-text       "]', timeout=10000)
            self.browser.fill('//input[@class="generic-input-field   form-textbox form-textbox-text       "]', f'{fname}')
            self.browser.fill('last-name-input > div > idms-textbox > idms-error-wrapper > div > div > input',lname)
            self.browser.fill('wc-birthday > div > div > div > div > masked-date > div > idms-error-wrapper > div > div > input',"02021998")
            self.browser.wait_for_selector('//input[@id="password"]', timeout=10000)
            self.browser.fill('//input[@id="password"]', 'mobodaa2@A')
            self.browser.keyboard.press("Tab")
            self.browser.keyboard.type("mobodaa2@A")
            self.reg_phone()
        except:
            print(f'{Fore.RED}[+] Error To Fill Data')

    def reg_phone(self):
        try:
            
            # Menu Tab 
            self.browser.wait_for_selector('//input[@type="email"]', timeout=10000)
            self.browser.fill('//input[@type="email"]', f'{self.address}')
            self.browser.click('//select[@class="generic-input-field  form-control form-dropdown    "]',timeout=10000)
            country_selector = self.browser.locator('.phone-input > idms-dropdown > div > idms-error-wrapper > div > div > select')
            country_selector.select_option(f"{self.cnt}")
            self.browser.wait_for_selector('//input[@class="generic-input-field   form-textbox form-textbox-text    force-ltr trusted-number phone-field placeholder-default-direction    "]', timeout=10000)
            self.browser.fill('//input[@class="generic-input-field   form-textbox form-textbox-text    force-ltr trusted-number phone-field placeholder-default-direction    "]', self.phone)
            
            if self.mode_call == "2":
                self.browser.wait_for_selector('//input[@class="verify-mode-voice-input"]', timeout=10000)
                self.browser.click('//input[@class="verify-mode-voice-input"]')
            
            
            if self.solvecaptcha(self.browser):
                if 'Please enter the characters you see or hear to continue.' in self.browser.inner_text('*', timeout=1000):
                    if self.solvecaptcha(self.browser):
                        while True:
                            emails = TempMail.getEmails(self.inbox)
                            maildata = str(emails)
                            try:
                                msgcode1 = maildata.split('verification page:')[1].split("This code")[0]
                                msgcod = msgcode1.strip()
                                if msgcod:
                                    self.browser.wait_for_selector('//input[@id="char0"]',timeout=3000)
                                    for i in range(len(str(msgcod))):
                                        self.browser.fill(f'//input[@id="char{i}"]',str(msgcod)[i])
                                    time.sleep(0.5)
                                    self.browser.keyboard.press("Enter")
                                    if self.mode_call == "1" or self.mode_call == 1:
                                        self.start_massage(self.browser)
                                    self.context.close()
                                    self.browser.close()
                                    break
                            except:
                                if 'Your account cannot be created at this time.' in self.browser.inner_text('*', timeout=2000):
                                    self.context.close()
                                    self.browser.close()
                                    break
                elif 'Enter a valid phone number.' in self.browser.inner_text('*', timeout=1000):
                    print(Fore.LIGHTRED_EX+f'{self.number} >>> Failed')
                else:
                    while True:
                        emails = TempMail.getEmails(self.inbox)
                        maildata = str(emails)
                        try:
                            msgcode1 = maildata.split('verification page:')[1].split("This code")[0]
                            msgcod = msgcode1.strip()
                            if msgcod:
                                self.browser.wait_for_selector('//input[@id="char0"]',timeout=3000)
                                for i in range(len(str(msgcod))):
                                    self.browser.fill(f'//input[@id="char{i}"]',str(msgcod)[i])
                                time.sleep(0.5)
                                self.browser.keyboard.press("Enter")
                                if self.mode_call == "1" or self.mode_call == 1:
                                    self.start_massage(self.browser)
                                self.context.close()
                                self.browser.close()
        
                                break
                        except:
                            if 'Your account cannot be created at this time.' in self.browser.inner_text('*', timeout=2000):
                                self.context.close()
                                self.browser.close()
                                print(Fore.LIGHTRED_EX+f'{self.number} >>> Failed')
                                with open('failed.txt','a+') as f:
                                    f.write(f'{self.number}\n')
                                break
        except:
            print(Fore.LIGHTRED_EX+f'{self.number} >>> Failed')
            with open('failed.txt','a+') as f:
                f.write(f'{self.number}\n')


    def start_massage(self,browser):
        self.browser = browser
        for i in range(5):
            try:
                if i == 0:
                    self.browser.click('//button[@id="resend-code"]',timeout=3000)
                    self.browser.click('//i[@class="icon no-flip icon_reload"]',timeout=3000)
                    print(Fore.LIGHTGREEN_EX+f'{self.number} >>> Success')
                    with open('success.txt','a+') as f:
                        f.write(f'{self.number}\n')
                else:
                    self.browser.click('//button[@id="resend-code"]',timeout=3000)
                    self.browser.click('//button[@id="resend-code"]',timeout=3000)
                    self.browser.click('//i[@class="icon no-flip icon_reload"]',timeout=3000)
                    print(Fore.LIGHTGREEN_EX+f'{self.number} >>> Success')
                    with open('success.txt','a+') as f:
                        f.write(f'{self.number}\n')
            except:
                print(Fore.LIGHTRED_EX+f'{self.number} >>> Failed')

    def solvecaptcha(self,browser):
        self.browser = browser
        try:
            time.sleep(1)
            solver = TwoCaptcha(f'{self.captcha}', defaultTimeout=600, pollingInterval=10)
            image = self.browser.get_attribute('//img[@alt="Image challenge"]','src')
            path = f"module/captcha{self.random_numbers}"
            if image:
                imgdata = base64.b64decode(image.split(',')[1])
                with open(f'{path}.jpeg', 'wb') as file:
                    file.write(imgdata)
            else:
                print("Error: Could not find the captcha image")
            result = solver.normal(f'{path}.jpeg')
            code = result['code']
            self.browser.wait_for_selector('//input[@class="generic-input-field   form-textbox form-textbox-text       "]', timeout=10000)
            # Fill Captcha Solve
            self.browser.fill('//input[@class="generic-input-field   form-textbox form-textbox-text       "]',code)
            # Submit Form
            self.browser.click('//button[@class="button button-primary last nav-action  pull-right weight-medium"]')
            # Remove Photo's
            try:
                os.remove(f'{path}.jpeg')
            except:
                pass
            return True
        except:
            print('[+] Error To Solve Captcha')
            return False
        

def intro():
    print(Fore.GREEN + '''
██ ██████   ██████  ██████   ██████  ██████   █████  
██      ██ ██       ██   ██ ██    ██ ██   ██ ██   ██ 
██  █████  ███████  ██████  ██    ██ ██   ██ ███████ 
        ██ ██    ██ ██   ██ ██    ██ ██   ██ ██   ██ 
██ ██████   ██████  ██████   ██████  ██████  ██   ██ ''')
    print(Fore.RED + 'MUSTAFA NASSER - Whattsapp [+201098974486]'+Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX)

def get_number():
    with open('numbers.txt','r') as ff:
        one = ff.read().splitlines()
    number = one[0]
    numbers = one[1:]
    with open('numbers.txt','w') as num:
        for i in numbers:
            num.write(i+'\n')
        num.write(number+'\n')
    return number

def get_proxy():
    # Proxy
    with open('proxy.txt','r') as pr:
        proxiesss = pr.read().splitlines()
    proxy = proxiesss[0]
    proxies = proxiesss[1:]
    with open('proxy.txt','w') as pro:
        for proxyy in proxies:
            pro.write(proxyy+'\n')
        pro.write(proxy+'\n')
    return proxy



if __name__ == '__main__':
    intro()
    try:
        browser_num = int(input('[ Number of browsers ]\n<> '))
        headles= int(input('[ 1 >> Browser Headless ]\n[ 2 >> Browser None Headless ]\n < Your Option? > '))
        mode_proxy= int(input('[ 1 >> Browser With Proxy ]\n[ 2 >> Browser None Proxy ]\n< Your Option? > '))
        call_num = "1"
        numbers = input('Enter Path numbers.txt: ')
        proxy = input('Enter Path proxy.txt: ')
        captcha_ = input('Enter Captcha Code: ')
        x = open(f'{numbers}.txt','r').read().splitlines()
        proxy_file = open(f'{proxy}.txt','r').read().splitlines()
        if len(proxy_file) <= 1:
            prox = 2
        if len(x) % browser_num == 0:
            count_ = (len(x) // browser_num)
        else:
            count_ = (len(x) // browser_num) + 1
        for i in range(count_):
            threads = []
            for i in range(browser_num):
                num = get_number()
                proxy = get_proxy()
                s = bot(num,headles,mode_proxy,proxy,call_num,proxy)
                t = threading.Thread(target=s.start,args=())
                t.start()
                threads.append(t)
            for j in threads:
                j.join()
        input(f'PRESS ENTER TO EXIT')      

    except Exception as e:
        print(e)
        input('Press Any Key To Exit....')