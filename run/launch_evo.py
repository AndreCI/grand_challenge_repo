#!/usr/bin/env python3
import os
import sys
import subprocess
import shlex
import argparse
from extract_write import extract_evol_conf, write_into_csv, extract_results

parser = argparse.ArgumentParser()
parser.add_argument('--conf_number', help='Number of the evol Conf file', default='1', type=str)
parser.add_argument('--seed', help='Seed for the evo', default=1, type=int)
parser.add_argument('--wriring_path', help='Where to write the exp', default='../outputs/current', type=str)
parser.add_argument('--csv_name', help='Csv file to write results', default='../results', type=str)
parser.add_argument('--port', help='Current port for the server' 	, default=8001, type=int)

opt = parser.parse_args()

#TOCHANGE
run_path = "C:\\Users\\andre\\Documents\\robogen-windows\\run\\"

seed = str(opt.seed)
writing_dir = opt.wriring_path
evol_conf = '../data/EvolConf_' + str(opt.conf_number) + '.txt'
metadata = extract_evol_conf(evol_conf)

FNULL = open(os.devnull, 'w')
subprocess.Popen([run_path + "robogen-server.exe", str(opt.port)], stdout=FNULL)
#Popen will not pause the prgm
subprocess.call([run_path + "robogen-evolver.exe", seed, writing_dir, evol_conf, '--overwrite'])
#wait until evolver has finished

results = extract_results(writing_dir)
to_write = {**metadata, **results}
write_into_csv(to_write, opt.csv_name)
