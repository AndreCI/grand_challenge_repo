#!/usr/bin/env python3
import os
import sys
import subprocess
import shlex
import argparse
import winsound
import random
from extract_write import extract_evol_conf, write_into_csv, extract_results, move_current
import time
from datetime import datetime

print("Program launch: [%s]." %(str(datetime.now())))
frequency = 800  # Set Frequency To 800 Hertz
duration = 500  # Set Duration To 500 ms == 0.5 second
winsound.Beep(frequency, duration)

parser = argparse.ArgumentParser()
parser.add_argument('--conf_number', help='Number of the evol Conf file', default='1', type=str)
parser.add_argument('--seed', help='Seed for the evo', default=25, type=int)
parser.add_argument('--random_seed', help='If set to True, the seed will be a random int between 1 and --seed.', default=True, type=bool)
parser.add_argument('--writing_path', help='Where to write the exp', default='../outputs/', type=str)
parser.add_argument('--csv_name', help='Csv file to write results', default='../results', type=str)
parser.add_argument('--port', help='Current port for the server' 	, default=8001, type=int)
parser.add_argument('--writing_dir', help='writing dir for the exp', default='current', type=str)
parser.add_argument('--verbose', help="Display info about evolution?", default="low", type=str)
opt = parser.parse_args()

#TOCHANGE
run_path = "C:\\Users\\Chloé\\Documents\\EvoRob\\robogen-windows\\run\\"
if opt.random_seed:
 seed = str(random.randint(1, opt.seed))
else:
 seed = str(opt.seed)
writing_dir = opt.writing_path + opt.writing_dir
evol_conf = '../data/EvolConf_' + str(opt.conf_number) + '.txt'
metadata = extract_evol_conf(evol_conf)

FNULL = open(os.devnull, 'w')
print("Running server...")
subprocess.Popen([run_path + "robogen-server.exe", str(opt.port)], stdout=FNULL)
#Popen will not pause the prgm
print("Running evolver with seed [%s]..." %seed)
t0 = time.time()
if opt.verbose == "low":
 subprocess.call([run_path + "robogen-evolver.exe", seed, writing_dir, evol_conf, '--overwrite'], stdout=FNULL)
else:
 subprocess.call([run_path + "robogen-evolver.exe", seed, writing_dir, evol_conf, '--overwrite'])
#wait until evolver has finished
print("Evolution done in %.3f seconds or %.3f minutes." %((time.time() - t0), (time.time() - t0)/60))

results = extract_results(writing_dir)
to_write = {**metadata, **results}
to_write["seed"] = seed
write_into_csv(to_write, opt.csv_name)

move_current(opt.writing_path, opt.writing_dir, to_write['scenario'])
frequency = 900  # Set Frequency To 900 Hertz
duration = 200  # Set Duration To 200 ms == 0.2 second
winsound.Beep(frequency, duration)
winsound.Beep(frequency, duration) #beep twice