import random
import numpy as np
import os

x_pos = [0, 1]
y_pos = [0, 0.5]
az = [0, 120]

with open('start_pos.txt', 'w', encoding='utf-8') as file:
    for x in x_pos:
        for y in y_pos:
            for a in az:
                file.write(str(str(x)+ ' ' + str(y) + ' '+ str(a) + '\n'))