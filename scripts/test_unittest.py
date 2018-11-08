import unittest

from GBIF import *
from FloraBrasil import *
from ThePlantList import *
from SpeciesLink import *

from main import *
from project import *


class Testing(unittest.TestCase):
        
    # def test_search_FLORABRASIL(self, nomePlanta = 'Dicliptera ciliaris Juss.'):
    #     a = FloraBrasil()
    #     x = a.search(nomePlanta)[0]
    #     self.assertEqual('Dicliptera ciliaris', x['scientificname'][:-len(x['scientificnameauthorship'])])

    # def test_search_THEPLANTLIST(self, nomePlanta = 'Dicliptera ciliaris Juss.'):
    #     a = FloraBrasil()
    #     x = a.search(nomePlanta)[0]
    #     self.assertEqual('Dicliptera ciliaris', x['scientificname'][:-len(x['scientificnameauthorship'])])
        
    # def test_auto_complete_FLORABRASIL(self, nomePlanta = 'Dicliptera ciliaris Juss.'):
    #     a = FloraBrasil()
    #     resposta = a.auto_complete(nomePlanta)
    #     self.assertEqual('Acanthaceae Dicliptera ciliaris Juss.', resposta)

    def test_GBIF_run(self):
        a = GBIF()
        query = 'Justicia laevilinguis (Nees) Lindau'
        result = a.search(query)
        assss = Project()
        result = a.search(assss.correct_name(query))
        x = a.occurrence(result)
        self.assertIsNotNone(x)

if __name__ == '__main__':
    unittest.main()
