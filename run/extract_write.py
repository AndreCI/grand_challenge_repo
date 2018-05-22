#!/usr/bin/env python3
import os
import csv

def extract_results(current_dir):
 results = (current_dir + '/' + 'BestAvgStd.txt')
 data = {}
 with open(results, 'r', encoding='utf-8') as f:
  last_line = (f.readlines()[-1])[:-1].split(' ') #remove \n
 data['generations_done']=last_line[0]
 data['best_score']=last_line[1]
 data['avg_score']=last_line[2]
 data['std_score']=last_line[3]
 return data
 
def extract_evol_conf(file):
 conf_path = file.split('/')
 conf_path = conf_path[0] + '/' + conf_path[1] + '/'
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
   data.append(current)
 return data
 
def write_into_csv(data, file):
 print(data)
 exist = True
 fitness = data['scenario']
 file += '_' + fitness + '.csv'
 if not os.path.exists(file): #check if we need the header
  exist = False
 with open(file, 'w', encoding='utf-8') as f:
  csvwriter = csv.DictWriter(f, data.keys())
  if not exist:
   csvwriter.writeheader()
  csvwriter.writerow(data)
 