from pathlib import Path

from symspellpy import SymSpell
class Project:
    instance = None

    def __init__(self):
        if not Project.instance:
            Project.instance = Project._Project()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class _Project:

        def __init__(self):
            initial_capacity = 83000
            max_edit_distance_dictionary = 2
            prefix_length = 7
            self.sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                                 prefix_length)

            # load dictionary
            dictionary_path = Path('dict_final.txt')

            count_index = 1  # column of the term frequency in the dictionary text file
            term_index = 0  # column of the term in the dictionary text file
            if not self.sym_spell.load_dictionary(dictionary_path, term_index, count_index):
                print("Dictionary file not found")
                return

        def correct_name(self, query):

            input_term = (query)  # max edit distance per lookup (per single word, not per whole input string)
            max_edit_distance_lookup = 2
            suggestions = self.sym_spell.lookup_compound(input_term,
                                                    max_edit_distance_lookup)

            # display suggestion term, edit distance, and term frequency
            # writer = csv.writer(f, delimiter='\t')
            for suggestion in suggestions:
                # writer.writerow(['']+[suggestion.term])
                return suggestion.term


if __name__ == '__main__':
    x = Project()
    print(x.correct_name('Hygrophila costata'))
