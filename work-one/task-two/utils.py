import re
from collections import OrderedDict

INDICATORS_WISHED = [
	"População estimada",
	"Densidade demográfica",
	"Matrículas",
	"Per capita",
	"Veículos",
	"IDH",
	"Unidade Territorial"
]

indicators_normalized = list(map(str.lower,INDICATORS_WISHED))

def get_normalized(indicator_name):
	for index, indicator in enumerate(indicators_normalized):
		if indicator in indicator_name.lower():
			return INDICATORS_WISHED[index]

def is_acceptable(indicator_name):
	for indicator in indicators_normalized:
		if indicator in indicator_name.lower():
			return True
	return False

def obtain_indicators(headers_indicators):
	state_indicators = {}

	for indicator in headers_indicators:
		indicator_name = indicator.find_element_by_class_name("lista__nome").text
		indicator_value = indicator.find_element_by_class_name("lista__valor").text

		if indicator_name and is_acceptable(indicator_name):
			normalized_indicator = get_normalized(indicator_name)

			new_value = normalize_money_or_value(indicator_value.strip())
			state_indicators[normalized_indicator] = new_value

	return state_indicators

def normalize_money_or_value(value):
	if "R$" in value:
		return " ".join(list(reversed(value.split())))
	else:
		return value
	
def normalize_to_compare(value):	

	for element in ["R$", "km²","hab/km²","pessoas"]:
		value = value.replace(element,"")

	value = value.replace(",","")
	value = value.replace(".","")

	return float(value)

def order_values(states_infos,by_indicator):
	indicator = INDICATORS_WISHED[by_indicator-1]
	print(indicator)
	key_comparator = lambda x : normalize_to_compare(x[1][indicator])

	ordered = OrderedDict(sorted(states_infos.items(),
						  key=key_comparator,reverse=True))

	return ordered

def show_menu():

	menu = [
		"Visualizar 1 (um) estado.",
		"Visualizar ordenado por indicador.",
		"Comparar Estados."
	]

	print("+"+ "-"*19 + "MENU" + "-"*19 + "+")
	for index, item in enumerate(menu,start=1):
		print("{} - {}".format(index,item))
	print("+" + "-"*42 + "+")


def show_data(state,data):
	print("Estado escolhido: {}".format(state))
	
	print("{:-^54}".format("-"))
	print("{:^25}|{:^25}".format("INDICADOR","VALOR"))
	print("{:-^54}".format("-"))
	for indicator, value in data.items():
		print("{:^25}|{:^25}".format(indicator,value))
		print("{:-^54}".format("-"))

def show_compared(state_one,state_two,states_infos):

	state_one_info = states_infos.get(state_one)
	state_two_info = states_infos.get(state_two)

	print("{:-^84}".format("-"))
	print("{:^25}|{:^30}|{:^30}".format(" ",state_one.upper(),state_two.upper()))
	print("{:-^84}".format("-"))
	for indicator in INDICATORS_WISHED:
		indicator_one = state_one_info.get(indicator)
		indicator_two = state_two_info.get(indicator)

		print("{:^25}|{:^30}|{:^30}".format(indicator,indicator_one,indicator_two))
		print("{:-^84}".format("-"))
		

def show_ranking(states_infos, indicator):

	states_infos = order_values(states_infos,indicator)

	indicator = INDICATORS_WISHED[indicator-1]

	print("{:-^57}".format("-"))
	print("{:^3}|{:^25}|{:^30}".format(" ","ESTADO",indicator))
	print("{:-^57}".format("-"))

	position = 1
	for state, state_data in states_infos.items():

		data_indicator = state_data.get(indicator)

		print("{:^3}|{:^25}|{:^30}".format(position,state,data_indicator))
		print("{:-^57}".format("-"))

		position += 1