from driver_ibge import IBGECrawler
from utils import (show_menu, show_data, show_compared,
				   show_ranking, INDICATORS_WISHED)

'''TO-DO
- Verify why iterating over states and the state_info not change, 
keep the same content
- When search by one attribute create method to find by one attribute
and not all of them
- Create cache variable when search a state already saved
'''

crawler = IBGECrawler()

states_infos = {}
	
while True:

	show_menu()

	option = int(input("Escolha a opção desejada: "))

	if option == 1:

		state = str(input("Escolha um estado: "))
		
		crawler.start()			
		if state not in states_infos:

			crawler.search_by(state.capitalize())
			states_infos[state] = crawler.collect_data()

		crawler.finish()

		show_data(state,states_infos.get(state))

	if option == 2:

		for index, indicator in enumerate(INDICATORS_WISHED,start=1):
			print("{} - {}".format(index,indicator))

		indicator_index = int(input("Escolha o indicador: "))
		state_quant = int(input("Quantidade de estados:"))
		states = [str(input("Estado: ")) for _ in range(state_quant)]

		crawler.start()

		for state in states:
			if state not in states_infos:		
				crawler.search_by(state)
				states_infos[state] = crawler.collect_data()
				
		crawler.finish()

		show_ranking(states_infos, indicator_index)

	if option == 3:

		state_one = str(input("Digite o primeiro estado: "))
		state_two = str(input("Digite o segundo estado: "))

		crawler.start()
		for state in [state_one, state_two]:
			if state not in states_infos:
				crawler.search_by(state)
				states_infos[state] = crawler.collect_data()

		crawler.finish()

		show_compared(state_one,state_two,states_infos)