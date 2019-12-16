from bs4 import BeautifulSoup
import bs4
with open("htmls//Aishwarya_Lath_resume.html", 'rb') as fp:
    soup = BeautifulSoup(fp.read(), features = "lxml")

#print(soup.body.contents)
body_contentes = soup.body.contents
'''for string in soup.body.stripped_strings:
    print(repr(string))'''
    
    
'''for content in body_contentes:
    if content != str:
        print(content)'''
        #if content.strings != None:
         #   print(content.strings)

#print(body_contentes[3].string)
#print(body_contentes[5].children)


#for child in body_contentes[5].children:
#    print(child)
all_strings = []
dict_data = []
print(type(body_contentes[0]))
for j in range(0, len(body_contentes)):
    if type(body_contentes[j]) != bs4.element.NavigableString:
        print(j, '\n', body_contentes[j])
        res = list(body_contentes[j].children)
        print(body_contentes[j]['style'])
        #print(res)
        inner = []
        styles = []
        for i in range(0, len(res)):
            if type(res[i]) != bs4.element.NavigableString:
                #print(res[i].children)
                try:
                    styles.append(res[i]['style'])
                except KeyError:
                    pass
                inner.append(list(res[i].children))
            else:
                print(res[i])
        
        #print(inner)
        
        for k, object in enumerate(inner):
            for string in object:
                if type(string) == bs4.element.NavigableString:
                    info = {}
                    string = string.strip('\n')
                    string = string.strip('\r')
                    all_strings.append(string)
                    try:
                        info['String'] = string.encode('utf-8')
                        info['Style'] = styles[k]
                        info['DIV-STYLE'] = body_contentes[j]['style']
                        #info[string] = styles[k]
                        print(info)
                        dict_data.append(info)
                        #print(dict_data)
                    except IndexError:
                        pass
                    #print(string)
#print(all_strings)
#print(info)
                        
#print(dict_data)

import csv
csv_cloumns = ['String', 'Font Type','Font Style', 'Font Description','Font Size','position', ' border', ' writing-mode', ' left', ' top', ' width', ' height']
csv_file = 'Aishwarya_Lath_resume.csv'
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_cloumns)
        writer.writeheader()
        for data in dict_data:
            src = data['Style']
            x = src.find(':')
            y = src.find('+')
            z = src.find(';')
            font_style = src[y+1:z]
            m=font_style.find('-')
            font_description = ''
            if m == -1:
                font_description = 'default'
            else:
                font_description = font_style[m+1:]
                font_style = font_style[:m]
            del data['Style']
            data['Font Type']=(src[x+2:y])
            data['Font Style']=font_style
            data['Font Description'] = font_description
            data['Font Size']=(src[len(src)-4:])
            lst=(data['DIV-STYLE'].split(';'))
            del data['DIV-STYLE']
            for i in range(0,len(lst)-1):
                a = lst[i].split(':')
                print(a)
                data[str(a[0])]=str(a[1])
            writer.writerow(data)
except IOError:
    print("I/O error")
except UnicodeEncodeError:
    print('unicode error')