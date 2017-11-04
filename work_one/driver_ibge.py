from browser import browser
from utils import obtain_indicators

class IBGECrawler:

	def __init__(self):
		self.browser = None
		self.ibge_url = "https://cidades.ibge.gov.br"
		self.state_indicators = {}
		
	def start(self):
		self.browser = browser()
		self.browser.maximize_window()
		self.browser.get(self.ibge_url)

	def search_by(self, state):
		search = self.browser.find_element_by_tag_name("input")
		search.send_keys(state)

		state_suggestions = self.browser.find_element_by_class_name("busca__auto-completar__resultado")

		self._select_state_from_suggestions(state_suggestions)

	def _select_state_from_suggestions(self, suggestions):
					
		while not suggestions.is_displayed():
			self.browser.implicitly_wait(1)

		suggestions_items = suggestions.find_elements_by_class_name("busca__auto-completar__resultado__item")

		is_country = lambda element : element.find_element_by_class_name("busca__tipo").text in ["Estado", "State"]

		country_wished = list(filter(is_country,suggestions_items))[0]
		country_wished.click()

		self.browser.implicitly_wait(5)

		headers_indicators = self.browser.find_elements_by_class_name("lista__cabecalho")

		self._process_indicators(headers_indicators)

	def _process_indicators(self,headers_indicators):

		for header_indicator in headers_indicators:

			if headers_indicators.index(header_indicator) != 0:
				header_indicator.click()

			indicators = self.browser.find_elements_by_class_name("lista__indicador")

			processed_indicators = obtain_indicators(indicators)

			self.state_indicators.update(processed_indicators)

			header_indicator.click()

		self._new_tab()

	def _new_tab(self):
		self.browser.execute_script("window.open('"+self.ibge_url+"','_blank');")
		self.browser.close()
		self.browser.switch_to_window(self.browser.window_handles[-1])

	def finish(self):
		if self.browser:
			self.browser.quit()

	def collect_data(self):
		return self.state_indicators.copy()

