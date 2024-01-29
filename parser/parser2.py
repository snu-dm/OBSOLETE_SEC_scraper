import os
import numpy as np
import glob
import codecs
import pandas as pd
from bs4 import BeautifulSoup
import re, unidecode
from collections import OrderedDict
import json

# Initial setup - currently set as a temporary file path in the current directory
current_path = os.path.dirname(__file__)
experiment_path = os.path.join(current_path, 'experiment_files')

df = pd.DataFrame(columns=[['ticker','text_length']])
p_item1_start = re.compile('(item)\s+[1I]\s*[.:-]*\s*\w{0,5}\s*(business)', re.I)
p_item2_start = re.compile('(item)\s+[2I]+\s*[.:-]*\s*\w*\s*\w*\s*(properties|communitiesn)', re.I)
table_pattern = re.compile('\s+[0-9]+\s+(table of contents)\s+', re.I) # table of contents 제거

file_paths = glob.glob('{}/*'.format(experiment_path), recursive=True)
print("Total number of files: " + str(len(file_paths)))

for i in range(1): #range(len(file_paths)):
    print(str(i)+" processing started")

    infos = file_paths[i].split('\\')[-1].split('_')
    print(infos)
    print(file_paths[i])

    try:
        f = codecs.open(file_paths[i], 'r', 'utf-8')
        soup = BeautifulSoup(f.read(), 'lxml')
        text = unidecode.unidecode(soup.get_text('\n'))

        lines_with_tags = []


        for tag in soup.find_all(True):
            if tag.name:
                tag_name = unidecode.unidecode(tag.name)
                tag_text = unidecode.unidecode(tag.get_text(strip=True))

                if tag.attrs:
                    tag_name += " " + " ".join([f'{key}="{value}"' for key, value in tag.attrs.items()])

            # Check if tag_text is non-empty before appending to the list
            if tag_text:
                line = (tag_name, tag_text)
                lines_with_tags.append(line)
        
        item_1 = 'ITEM 1. BUSINESS'
        item_1a = 'ITEM 1A. RISK FACTORS'

        start_1 = 0
        start_1a = -1
        overview_idx = -1


        for i in range(len(lines_with_tags)):
            if item_1 in lines_with_tags[i][1]:
                start_1 = i
            #if item_1a in lines_with_tags[i][1]:
            #    start_1a = i
            if ('Overview' in lines_with_tags[i][1]) or ('OVERVIEW' in lines_with_tags[i][1]):
                overview_idx = i
        
        if start_1 == 0:
            print("PARSING ERROR, NO ITEM 1")

        #if start_1a == -1:
        #    od.pop()


        tag_bt = lines_with_tags[start_1][0]
        tag_st = lines_with_tags[overview_idx][0]
        tag_mt = lines_with_tags[overview_idx+1][0]
        
        num_lines_test = 600

        given_data = lines_with_tags[start_1:start_1+num_lines_test]

        od = OrderedDict()

        prev_tag = ''
        for i in range(len(given_data)):
            data_tag = given_data[i][0]
            data_text = given_data[i][1]
            

            if data_tag == tag_bt:
                od[data_text] = OrderedDict()
            if data_tag == tag_st:
                od[next(reversed(od))][data_text] = []
            if data_tag == tag_mt:
                od[next(reversed(od))][next(reversed(od[next(reversed(od))]))].append(data_text)

            prev_tag = data_tag
        

        document = json.dumps(od, indent=4)

    except Exception as e:
        df.loc[len(df)] = [infos[0], 0]
        print("error : %s, Missed File : %s, Missed File URL: %s" % (e, infos[:1], file_paths[i]))


    # Saving the log - for experiments, need change when saving to database

    file_name = f"log3_{i}.txt"

    with open(file_name, 'w') as log:
        log.write(document)