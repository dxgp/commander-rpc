import os
import multiprocessing
from constants import SOLDIER_COUNT

def run_command(cmd):
    os.system(cmd)

def run_commands(commands, n_parallel):
    worker = multiprocessing.Pool(n_parallel)
    worker.map(run_command,commands)

if __name__=='__main__':
    commands = []
    for i in range(SOLDIER_COUNT):
        commands.append(f"python soldier.py {60000+i}")
    run_commands(commands,n_parallel=SOLDIER_COUNT)