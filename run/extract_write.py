#!/usr/bin/env python3
import os
import csv

def extract_results(current_dir):
 results = (current_dir + '/' + 'BestAvgStd.txt')
 data = {}
 with open(results, 'r', encoding='utf-8') as f:
  last_line = (f.readlines()[-1])[:-1].split(' ') #remove \n
 print("Last genenation got score:", last_line)
 data['generations_done']=last_line[0]
 data['best_score']=last_line[1]
 data['avg_score']=last_line[2]
 data['std_score']=last_line[3]
 return data
 
def extract_evol_conf(file):
 conf_path = file.split('/')
 conf_path = conf_path[0] + '/' + conf_path[1] + '/'
 print("Extracting data from [%s]..." %file)
 with open(file) as f:
  lines = (f.readlines())
 data = {}
 for l in lines:
  if l[0] != '#':
   l = l[:-1]
   current = l.split('=')
   if current[0] == 'simulatorConfFile': #get path for conf_file
    conf_path += current[1]
   data[current[0]] = current[1] #add key (current[0]) and val (current[1]) to dict
 additional_data = extract_conf(conf_path)
 print(additional_data)
 for d in additional_data:
  data[d[0]] = d[1]
 return data

def extract_conf(file):
 with open(file) as f:
  lines = f.readlines()
 data = []
 for l in lines:
  if l[0] != '#': #remove comments
   l = l[:-1] #remove \n
   current = l.split('=')
   if len(current) > 1:
    data.append(current)
 return data
 
def write_into_csv(data, file):
 exist = False
 fitness = data['scenario']
 if "." in fitness:
  fitness = fitness.split('.')[0] #remove .js
 file += '_' + fitness + '.csv'
 print("writing into csv [%s]..." %file)
 if os.path.exists(file): #check if we need the header
  exist = True
 with open(file, 'a', encoding='utf-8') as f:
  csvwriter = csv.DictWriter(f, data.keys())
  if not exist:
   csvwriter.writeheader()
  csvwriter.writerow(data)

def move_current(writing_path, writing_dir, scenario):
 writing_current = writing_path + writing_dir
 dirs = os.listdir(writing_path)
 num_dir = 0
 for d in dirs:
  if os.path.isdir(writing_path + d):
   num_dir += 1
 new_writing_current = writing_path + 'exp_' + str(num_dir) + '_' + scenario
 print("Renaming [%s] into [%s]..." %(writing_current, new_writing_current))
 os.rename(writing_current, new_writing_current)
 
 
