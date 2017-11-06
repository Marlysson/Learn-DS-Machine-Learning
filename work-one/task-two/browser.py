from selenium import webdriver

def browser():

	from os.path import join, dirname, abspath
	
	relative_path = dirname(dirname(abspath(__file__)))
	address = join(relative_path,"chromedriver.exe")

	return webdriver.Chrome(address)

	