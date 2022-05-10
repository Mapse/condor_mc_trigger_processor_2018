# coding: utf-8

import time
import os, sys

import coffea.processor as processor
from coffea.nanoevents import BaseSchema

from nanoAODplus_processor.EventSelectorProcessor import EventSelectorProcessor
from tools.merger import merger
from tools.plotter import plotter

tstart = time.time()

job = sys.argv[1]
number = job.split('.')[-2].split('_')[-1]

with open(job) as f:
    file_list = f.read().splitlines()

name = file_list[0].split('/')[-1].split('_')[0]
name = name + '_' + number

files = {name: file_list}

print(name)

# creating necessary folders into dir output data
os.system("mkdir -p output/" + name)
os.system("rm -rf output/" + name + "/*")          

output = processor.run_uproot_job(files,
                                treename='Events',
                                processor_instance=EventSelectorProcessor(name),
                                executor=processor.iterative_executor,
                                executor_args={'schema': BaseSchema, 'skipbadfiles': True},
                                chunksize=10000,
                                )

elapsed = round(time.time() - tstart, 2)
print(f"Process finished in: {elapsed} s")

merger(name)

plotter(name)

print("Transfering files...")
os.system("cp output/" + name + "/* ../.")
