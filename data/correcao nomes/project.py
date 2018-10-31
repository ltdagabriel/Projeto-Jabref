import os
import sys
import csv
from more_itertools import *
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

def main():
	# create object
	initial_capacity = 83000
	# maximum edit distance per dictionary precalculation
	max_edit_distance_dictionary = 2
	prefix_length = 7
	sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
						 prefix_length)
	# load dictionary

	dictionary_path = os.path.join(sys.argv[0],
								   "dict_final.txt")
	count_index = 1  # column of the term frequency in the dictionary text file
	term_index = 0  # column of the term in the dictionary text file
	if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
		print("Dictionary file not found")
		return
	list = []
	lista_nome_errado = []
	
	#xd = pd.read_csv('Null_names.csv')
	
	with open("Null_names.csv", "r") as f:
		line = f.readline()
		while line:
			line = f.readline()
			# p = peekable(f.readlines())
			# print(p.peek())
			print("Nome pra ser corrigido:", line)
			lista_nome_errado.append(line)
			# lookup suggestions for multi-word input strings (supports compound
			# splitting & merging)
			input_term = (line)	    # max edit distance per lookup (per single word, not per whole input string)
			max_edit_distance_lookup = 2
			suggestions = sym_spell.lookup_compound(input_term,
													max_edit_distance_lookup)
			# display suggestion term, edit distance, and term frequency
			#writer = csv.writer(f, delimiter='\t') 
			for suggestion in suggestions:
				#writer.writerow(['']+[suggestion.term])
				list.append(suggestion.term)
				print("{}, {}, {}".format("sugestao: ",suggestion.term, suggestion.count,
										  suggestion.distance))
			

	with open("output.csv", "w", newline='' ) as fcs:
		escreve = csv.writer(fcs, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
		escreve.writerow(['Nome entrada','Nome corrigido'])
		for l in zip(list,lista_nome_errado):
			escreve.writerow([l[1], l[0]])
if __name__ == "__main__":
	main()