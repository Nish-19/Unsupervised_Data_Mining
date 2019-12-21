'''
Used for analysing a directory of html files, it:
	Extracts data and convertes them to csv
	Generates heading for each file
	Finds the heading distribution 

'''
import os

# Importing BeautifulSoup
import bs4
from bs4 import BeautifulSoup

# Importing csv
import csv

# Importing defaultdict
from collections import defaultdict

# Importing the html_parser python file
from html_parser import *

def all_files(output_directory, path):
	'''
	Iterates through each html file in the directory, and updates the parsed information in csv
	Collects all headings of each files and returns them

	Parameters : output_directory - Directory in which all output files will be saved
				 path 			  - Path of the current location of .html file

	return 	   : all_headings - Dictionary with file name as key and list of headings as value
	'''
	files = list()
	root = ''

	for r, d, f in os.walk(path):
		root = r
		for file in f:
			if '.html' in file:
				files.append(file)

	#output_directory = os.path.join(path, 'output')

	try:
		os.mkdir(output_directory)
	except FileExistsError:
		print("Folder already exists, for running again delete the folder")

	all_headings = dict()

	for f in files:
		file_name = os.path.join(path, f)
		body_contents = file_open(file_name)
		dict_data = preprocess_data(body_contents)
		output_path = os.path.join(output_directory, f)
		write_csv(dict_data, output_path)
		heading_scores = generate_headings(dict_data)
		headings = find_headings(heading_scores)
		all_headings[f] = headings

	#print_all_headings(output_directory, all_headings)
	return all_headings

def print_all_headings(output_directory, all_headings):
	'''
	Prints all the headings of different files into an output text file

	Parameters : output_directory - Directory of the output
				 all_headings - Dictionary with file name as key and list of headings as value
	'''
	text_file = os.path.join(output_directory, 'all_headings.txt')
	with open(text_file, 'w') as f:
		print(all_headings, file = f)

def generate_heading_frequency(output_directory, all_headings):
	'''
	Generates and prints the heading frequency distribution

	Parameters : output_directory - Directory of the output
				 all_headings - Dictionary with file name as key and list of headings as value
	Return : Void
	'''
	heading_data = defaultdict(int)

	for file, names in all_headings.items():
		for string in names:
			string = string.decode()
			string = string.strip('\n')
			string = string.strip('\r')
			lst = string.split(' ')
			lst = list(filter(''.__ne__, lst))

			string = ''

			for element in lst:
				element = element.strip('-')
				element = element.strip(':')

				if element.isalpha():
					string = string + element + ' '

			string = string.strip(' ')
			string = string.upper()
			heading_data[string] = heading_data[string] + 1


	dictionary_file = os.path.join(output_directory, 'headings_data.txt')
	with open(dictionary_file, 'w') as f:
		for w in sorted(heading_data, key=heading_data.get, reverse = True):
			print(w, heading_data[w])
			print(w, heading_data[w], file = f)

def main():
	path = 'D:/Text_mining/Htmls/samiran/samiran_resumes'
	output_directory = os.path.join(path, 'output')
	all_headings = all_files(output_directory, path)
	generate_heading_frequency(output_directory, all_headings)
	print_all_headings(output_directory, all_headings)

if __name__ == '__main__':
	main()
