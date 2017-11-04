from selenium import webdriver

def get_driver():
	driver = join(dirname(abspath(__file__)), "chromedriver.exe")
	return driver

driver = get_driver()

options = webdriver.ChromeOptions()

browser = webdriver.Chrome(driver, chrome_options=options)
browser.get("https://www.reddit.com/")

titles = []

for page in range(3):
	elements = browser.find_elements_by_css_selector(".title .may-blank")

	for element in elements:
		titles.append(element.text.encode("utf-8"))

	button = browser.find_element_by_css_selector(".next-button a")
	button.click()

for title in titles:
	print("="*len(title))
	print(title)
