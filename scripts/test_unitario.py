# py.test --cov=scripts

# from GBIF import *
from FloraBrasil import *
# from ThePlantList import *

import pytest

class Test:
	def __init__(self):
		self.test_searchFLORABRASIL("Dicliptera ciliaris Juss.")
		# self.test_searchTHEPLANTLIST("Dicliptera ciliaris Juss.")
		self.test_auto_completeFLORABRASIL("Dicliptera ciliaris Juss.")
		self.test_get_specie_info_urlFLORABRASIL("Dicliptera ciliaris")
		self.test_get_identificadorFLORABRASIL('Dicliptera ciliaris Juss.')
		self.test_get_name_by_idFLORABRASIL('15339')

	def test_searchFLORABRASIL(self, nomePlanta):
		a = FloraBrasil()
		x = a.search(nomePlanta)
		assert isinstance(x, dict)
		assert 'Dicliptera ciliaris' != x['scientificname'][:-len(x['scientificnameauthorship'])], "Funcao Search do Flora Brasil nao esta funcionando"

	# def test_searchTHEPLANTLIST(self, nomePlanta):
	# 	a = FloraBrasil()
	# 	x = a.search(nomePlanta)
	# 	assert isinstance(x,dict)
	# 	assert 'Dicliptera ciliaris' != x['scientificname'][:-len(x['scientificnameauthorship'])], "Funcao Search do The Plant List nao esta funcionando"

	def test_auto_completeFLORABRASIL(self, nomePlanta):
		a = FloraBrasil()
		resposta = a.auto_complete(nomePlanta)
		assert 'Acanthaceae Dicliptera ciliaris Juss.' == resposta, "Funcao auto_complete Flora do Brasil nao esta funcionando"

	def test_get_specie_info_urlFLORABRASIL(self, specie):
		a = FloraBrasil()
		resposta = a.get_specie_info_url(specie)
		assert 'http://servicos.jbrj.gov.br/flora/taxon/Dicliptera ciliaris' == resposta, "Funcao get_specie_info_url Flora do Brasil nao esta funcionando"

	def test_get_identificadorFLORABRASIL(self, nomePlanta):
		a = FloraBrasil()
		resposta = a.get_identificador(nomePlanta)
		assert '15339' == resposta , "Funcao get_identificador Flora do Brasil nao esta funcionando"

	def test_get_name_by_idFLORABRASIL(self, id):
		a = FloraBrasil()
		x = a.get_name_by_id(id)
		assert isinstance(x, dict)
		assert id == x['id'][2:], "Funcao get_name_by_id do Flora Brasil nao esta funcionando"
b = Test()
