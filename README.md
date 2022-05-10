# Condor Monte Carlo Trigger Processor 2018

This repository contains the machinery for running condor in lxplus enviroment for producing .coffea files with trigger information. The files produced here are used for plotting HLT curves efficiencies.

# To run

There are several codes that should be run separately. Below one can find the steps.

## Make paths for condor

There are two options: Local paths or remote paths.
There are several codes that should be run separately. Below one can find the steps.

### Local paths

First one should create the text file with the paths to the *NanoAODPlus.root* files.

In order to do so, you need to run the script named *make_path.sh*.

There, you need to provide the current directory on the variable *here*, the main path where the NanoAODPlus files are stored *main_path* and the file name to be provide to condor, file_name.

Note: It is important to consider how many 000x folders the MC production. For this version it is hardcoded: We consider from 0000/ to 0009/. Don't worry, you can simple change it or construct a better logic.

Finally, you can do:

    . make_path.sh

### Remote paths

First you need to guarantee that the coffea enviroment has xrootd installed on it.
Thenn, on the file you need to use grid certificate,

    . voms-proxy-init --rfc --voms cms -valid 192:00
    
Then, provide the name of the file to be provided to condor *file_name*. And the variable *radic* to provide the logic to the script *correct_path.py* (Always used for files from Caltech!!).

## Run condor

The second steps one need to run condor in order to produce *.coffea* files. First, activate *voms* certificate:

    . voms-proxy-init --rfc --voms cms -valid 192:00
    
Then, copy it to the current directory:

    cp /tmp/x509up_u128055 .

Now, the script *condor.py* can be run:

    python3 condor.py -n=*name* -s

Where *name* is the content of *file_name* without *_path.txt*

Example:

> If *file_name* is *Monte_Carlo_path.txt* then *name* should be Monte_Carlo:

    python3 condor.py -n=*Monte_Carlo* -s

After that, condor should run normally

> Comment: It is important follow the condor process by typing *condor_q user_name* and also look on the *output.err* files.

## Merge data and make histograms.

In this step the files produced in the last step are going to be merged and moved to *OniaOpenCharmRun2ULAna* folder to produce the histogram files and the trigger efficiency analysis.

The code that do that is *merged.sh*. There, one should provide the name of the folder where all files (coffea data and coffea histogram) are going to be moved. Remember that this folder is located at OniaOpenCharmRun2ULAna/output. The name of the folder is stored on the variable *name*.
There you should provide the *output* variable, which stores the coffea files produced with condor. (This step is ongoing work)

> Comment: Be aware, always use the same processors version (histogram and event selection) in both cases, condor and  OniaOpenCharmRun2ULAna.

Finnaly, run the code:

    . merge.sh
    
If everthing went well, you should have your .coffea and hists.coffea on the folder OniaOpenCharmRun2ULAna/output/*name*.

Now you can proceed with the plots and trigger efficiency analysis.
