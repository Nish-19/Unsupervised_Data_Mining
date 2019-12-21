# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:48:46 2019

@author: NISCHAL
"""
"""
Program for paring the html file and finding the structure in the data

Given a html file the output is a csv file with the parameters defining the attributes of the string(text)

Makes use of BeautifulSoup package for parsing the html data.
"""

# Importing BeautifulSoup
import bs4
from bs4 import BeautifulSoup

# Importing csv
import csv

def file_open(file_name):
	"""
	Opens the html file and converts it into Beautiful Soup object

	Params : file_name - Name of the file to be opened

	Returns : body_contents - a BeautifulSoup object
	"""
	if '.html' in file_name:
		with open(file_name, 'rb') as fp:
			soup = BeautifulSoup(fp.read(), features = "lxml")
			body_contents = soup.body.contents
			return body_contents

def preprocess_data(body_contents):
	"""
	Finds pattern in the HTML object and stores it

	params : body_contents - BeautifulSoup Object

	return : dict_data - List of dictionaries containing string name and its parameters
	"""
	dict_data = []
	for j in range(0, len(body_contents)):
		inner = list()
		styles = list()
		if type(body_contents[j]) != bs4.element.NavigableString:
			res = list(body_contents[j].children)

			for i in range(0, len(res)):
				if type(res[i]) != bs4.element.NavigableString:
					try:
						styles.append(res[i]['style'])
					except KeyError:
						pass
					inner.append(list(res[i].children))
				else:
					#print(res[i])
					pass

		for k, object in enumerate(inner):
			all_strings = ''
			all_strings = all_strings.encode('utf-8')
			for string in object:
				if type(string) == bs4.element.NavigableString:
					string = string.encode('utf-8')
					all_strings = all_strings + string
			info = {}
			try:
				info['String'] = all_strings
				info['Style'] = styles[k]
				info['DIV-STYLE'] = body_contents[j]['style']
				dict_data.append(info)
			except IndexError:
				pass
	return dict_data

def write_csv(dict_data, f):
	"""
	Writes the found data in the csv file

	params : dict_data - List of dictionaries each representing a string and its parameters like font size etc.

	return : void
	"""
	csv_cloumns = ['String', 'Font Type','Font Style', 'Font Description','Font Size','position', ' border', ' writing-mode', ' left', ' top', ' width', ' height']
	csv_file = f.strip('.html')
	csv_file = csv_file + '.csv'
	try:
		with open(csv_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = csv_cloumns)
			writer.writeheader()

			for data in dict_data:
				src = data['Style']
				x = src.find(':')
				y = src.find('+')
				z = src.find(';')
				font_style = src[y+1:z]
				m = font_style.find('-')
				font_description = ''
				if m == -1:
					font_description = 'default'
				else:
					font_description = font_style[m+1:]
					font_style = font_style[:m]
				del data['Style']
				data['Font Type'] = src[x+2:y]
				data['Font Style'] = font_style
				data['Font Description'] = font_description
				data['Font Size'] = src[len(src)-4:]
				lst = data['DIV-STYLE'].split(';')
				del data['DIV-STYLE']
				for i in range(0, len(lst) - 1):
					a = lst[i].split(':')
					data[str(a[0])] = str(a[1])
				try:
					writer.writerow(data)
				except ValueError:
					pass
	except IOError:
		print("I/O error")
	except UnicodeEncodeError:
		print('unicode error')

def generate_headings(dict_data):
	"""
	Generates a dictionary containing all strings with their corresponding heading scores

	params : dict_data - list of set of dictionaries

	return : heading_scores - dictionary containing all strings with their corresponding heading scores
	"""
	fonts = list()
	eligible_strings = dict()
	heading_scores = dict()

	for data in dict_data:
		heading_scores[data['String']] = 0
		string = data['String'].decode()
		string = string.strip('\n')
		string = string.strip('\r')

		for i in range(0, len(string)):
			string = string.strip(' ')
		string = string.strip('-')
		string = string.strip(':')

		lst = string.split(' ')
		for i in range(0, len(lst)):
			if '' in lst:
				lst.remove('')

		if len(lst) <= 3:
			heading_scores[data['String']] = 1
		string = string.replace(' ', '')

		if string.isalpha():
			data['Font Size'] = data['Font Size'].strip(':')
			eligible_strings[data['String']] = data['Font Size']

			if data['Font Size'] not in fonts:
				fonts.append(data['Font Size'])

			if string.isupper():
				heading_scores[data['String']] = heading_scores[data['String']] + 1

	# Sorting the fonts
	res = list()
	for font in fonts:
		font = font.strip('px')
		font = int(font)
		res.append(font)

	res.sort()
	fonts = list()
	for font in res:
		font = str(font)
		font = font + 'px'
		fonts.append(font)

	for key, value in eligible_strings.items():
		try:
			heading_scores[key] = heading_scores[key] + fonts.index(value)
		except ValueError:
			pass

	return heading_scores

def find_headings(heading_scores):
	"""
	Finds the possible headings of the given resume

	params : heading_scores - dictionary containing all strings with their corresponding heading scores

	return - headings - list of strings which are the headings
	"""
	headings = list()
	i = 0
	j = 0
	int_max = 99999
	cur = 0
	for w in sorted(heading_scores, key = heading_scores.get, reverse = True):
		if j < 5:
			if heading_scores[w] < int_max:
				int_max = heading_scores[w]
				i = i +1
			if i <= 3:
				headings.append(w)
				cur = heading_scores[w]
		else:
			if (heading_scores[w] == cur):
				headings.append(w)
		j = j + 1
	return headings

def main():
	body_contents = file_open("..\htmls\\Nischal_resume.html")
	dict_data = preprocess_data(body_contents)
	write_csv(dict_data, 'Nischal_resume')
	heading_scores = generate_headings(dict_data)
	headings = find_headings(heading_scores)
	print(headings)

if __name__ == '__main__':
	main()
