# This code is used to merge the coffea files that are produced from a condor processing
from coffea.util import save, load
from tqdm import tqdm
import argparse
import os

# For argument parsing
parser = argparse.ArgumentParser(description="Merge coffea files from condor processing")
parser.add_argument("-d", "--data", help="Merge the data files", action="store_true")
parser.add_argument("-p", "--hist", help="Merge the hist files", action="store_true")
args = parser.parse_args()

# Function to create a list with all coffea files in a path

path = '/afs/cern.ch/work/m/mabarros/public/CMSSW_10_6_12/src/condor/MC_Trigger_processor/2018/output_Jpsi_25to45_Dstar_DPS_2018_13TeV'
name = 'Monte_Carlo_2018_Jpsi_25to45_Dstar_DPS_2018_13TeV'

def merg_files(path, name):

    if args.data:
        typ = '.coffea'
        sv = 'data'
    elif args.hist:
        typ = 'hists.coffea'
        sv = 'hists'
    else:
        print("You should provide an option: -d for merge data files or -p to merge the hist files")

    files = []
    with os.scandir(path) as aux:
        for file in aux:
            if file.name.endswith(typ) and (file.stat().st_size != 0):
                files.append(file.path)
    # Takes the first to start the accumulator
    acc = load(files[0])
    # Take the length of the list
    
    if args.data:
        le_files = int(round(len(files)/2, 0))
    elif args.hist:
        le_files = len(files) 

    # For accumulate the files
    if args.data:
        #print("First half")
        for i in tqdm(range(1, le_files), desc="Processing", unit="files"):
            acc += load(files[i])
        save(acc, sv + '_' + name + '.coffea')
        
    if args.hist:
        for i in tqdm(range(1, le_files), desc="Processing", unit="files"):
            acc += load(files[i])
        save(acc, sv + '_' + name + '.coffea')

    print ("Finished")

merg_files(path, name)


########### Sketch

""" acc = load(sv + '_' + name + '.coffea')
print("Last half")
if isinstance(le_files, int):
    lim = 2 * le_files 
elif isinstance(le_files, float):
    lim = 2 * (le_files - 1)       
for i in tqdm(range(le_files+1, lim), desc="Processing", unit="files"):
    acc += load(files[i])
save(acc, sv + '_' + name + '.coffea') """

 


