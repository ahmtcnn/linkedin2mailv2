from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import unidecode
from optparse import OptionParser
import chromedriver_binary


class LinkedinScraper():
	def __init__(self,options):
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		#self.driver = webdriver.Chrome('./chromedriver')
		self.driver.maximize_window()
		self.temp_userlist = []
		self.userlist = []
		self.maillist  = []
		self.companymail = options.emailformat
		self.seperator = options.seperator
		self.company_link = options.link

	def read_config(self):
		with open("credentials.txt","r+") as configfile:
			context = configfile.readlines()
			email, password = context[0], context[1]
			self.email = (email.split(":")[1]).rstrip("\n")
			self.password = (password.split(":")[1]).rstrip("\n")
			if email == "" or password == None:
				print("[-] Please give credentials from credentials file")
				exit()

	# Linkedin login fonksiyonu
	def login(self):
		self.driver.get('https://www.linkedin.com')
		self.driver.implicitly_wait(3)

		# email input box ın belirlenmesi
		username = self.driver.find_element_by_xpath('//*[@type="text"]')

		# email input değerine ilgili kimlik bilgisinin gönderilmesi
		username.send_keys(self.email)

		# Parola input box ın belirlenmesi
		password = self.driver.find_element_by_xpath('//*[@type="password"]')

		# Parolanın ilgili input box a gönderimi
		password.send_keys(self.password) # Your password

		# Login butonuna tıklanması
		log_in_button= self.driver.find_element_by_xpath('//*[@class="sign-in-form__submit-button"]')
		log_in_button.click()
		self.driver.implicitly_wait(5) #driver will wait for 1 second to load everything completely

	# ilgili şirketin linkine gidilmesi, kullanıcıların tümü için belirli aralıklarla scroll yapılması, html source çekilmesi ve parse edilmesi.
	def search(self):
		self.driver.get(self.company_link)
		self.driver.implicitly_wait(5)

		check_height = self.driver.execute_script("return document.body.scrollHeight;") 
		while True:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(5)
			height = self.driver.execute_script("return document.body.scrollHeight;") 
			if height == check_height: 
				break 
			check_height = height
		html_source_code = self.driver.execute_script("return document.body.innerHTML;")
		soup = BeautifulSoup(html_source_code, 'html.parser')
		mydivs = soup.find_all("div", {"class": "org-people-profile-card__profile-title"})

		self.parse_list(mydivs)

	# elde edilen listenin parse edilmesi ve email list için uygun hale gelmesi.
	def parse_list(self,divlist):
		with open("normal_names.txt","w+",encoding="utf-8") as f:
			for i in divlist:
				full_name = i.contents[0].strip()
				self.temp_userlist.append(full_name)
				f.write(full_name)
				f.write("\n")

		for full_name in self.temp_userlist:
			lower_full_name = unidecode.unidecode(full_name).lower()
			self.userlist.append(lower_full_name)
			
		for user in self.userlist:
			user_with_list = user.split(" ")
			if len(user_with_list) == 2:
				first_name = user_with_list[0]
				lastname = user_with_list[1]
			
			if len(user_with_list) == 3:
				first_name = user_with_list[0]
				lastname = user_with_list[2]
				
			email = first_name + self.seperator + lastname + "@" + self.companymail
			print(email)
			self.maillist.append(email)

			with open("output.txt","w+") as f:
				for email in self.maillist:
					f.write(email)
					f.write("\n")
		self.driver.quit()

# kullanıcıdan gerekli parametrelerin alınması
def get_options():
    parser = OptionParser()
    parser.add_option("-l", "--link", dest="link",
                    help="Write company linkedin page to scrape")

    parser.add_option("-e", "--email",
                    dest="emailformat",
                    help="Write emailformat to concatenate example 'hotmail.com' ")

    parser.add_option("-s", "--seperator",
                dest="seperator",
                help="Enter seperator between firstname and last name")

    (options, args) = parser.parse_args()
    if not options.emailformat:
        parser.error("Please enter the email format! example : -e hotmail.com, gmail.com etc.\nFull Example: python main.py -e hotmail.com -l https://www.linkedin.com/company/google/people -s .")
    if not options.link:
        parser.error("Please enter company 'people page' link to search! example : -l https://www.linkedin.com/company/google/people")
    if not options.seperator:
        parser.error("Enter seperator between firstname and last name examples: -s '.' ")
    return options


options = get_options()

scrapper = LinkedinScraper(options)
scrapper.read_config()
scrapper.login()
scrapper.search()