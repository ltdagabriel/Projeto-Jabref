from GBIF import *
from FloraBrasil import *
from ThePlantList import *

import pytest

class Test:
	def __init__(self):
		self.test_searchFLORABRASIL("Dicliptera ciliaris Juss.")
		self.test_searchTHEPLANTLIST("Dicliptera ciliaris Juss.")
		self.test_auto_completeFLORABRASIL("Dicliptera ciliaris Juss.")

	def test_searchFLORABRASIL(self, nomePlanta):
		a = FloraBrasil()
		x = a.search(nomePlanta)[0]
		assert 'Dicliptera ciliaris' != x['scientificname'][:-len(x['scientificnameauthorship'])], "Funcao Search do Flora Brasil nao esta funcionando"

	def test_searchTHEPLANTLIST(self, nomePlanta):
		a = FloraBrasil()
		x = a.search(nomePlanta)[0]
		assert 'Dicliptera ciliaris' != x['scientificname'][:-len(x['scientificnameauthorship'])], "Funcao Search do The Plant List nao esta funcionando"

	def test_auto_completeFLORABRASIL(self, nomePlanta):
		a = FloraBrasil()
		resposta = a.auto_complete(nomePlanta)
		assert 'Acanthaceae Dicliptera ciliaris Juss.' == resposta, "Funcao auto_complete Flora do Brasil nao esta funcionando"

b = Test()
