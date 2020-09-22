import sys
import argparse
import subprocess
import multiprocessing
from multiprocessing import Pool
from contextlib import closing
import time
import os

nproc = 3

modules = [
	'-m sitting_time_sensor.sitting_time_system',
	'bot_run.py',
	'scheduler_WBGT.py',
    ]

def proc(argument):
    start = time.time()
    p = subprocess.Popen(['python', argument],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    res = p.communicate()
    end = time.time()
    with open('run_HeatStroke_Sitting.log', 'w') as ofs:
        ofs.write(str(end - start))
        ofs.write('\n' + '-'*30 + '\n')
        ofs.write(str(res))
    return None

if __name__ == '__main__':
    with closing(Pool(nproc)) as p:
        res = p.map(proc, modules)
        p.terminate()
