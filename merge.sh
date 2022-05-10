''' 

This script is used before merge_coffea in order to merge only data files (not histograms!)
Then, the merged content is moved to the folder on the conda work area and the data file is read to produce the histograms files

'''

############################################ To edit ############################################

name='Monte_Carlo_Jpsi_25to45_Dstar_DPS_2018_13TeV'

output='output_Jpsi_25to45_Dstar_DPS_2018_13TeV'

analysis_path='/afs/cern.ch/work/m/mabarros/public/CMSSW_10_6_12/src/OniaOpenCharmRun2ULAna/output'

############################################ End editing ############################################

mv *.coffea $output

echo 'merging data files.. (For MC 2017 this takes around 8 minutes)'
python3 merge_coffea.py -d

echo 'moving files to process area'

mv data_Monte_Carlo_2018_Jpsi_25to45_Dstar_DPS_2018_13TeV.coffea $name.coffea

mv $name.coffea $analysis_path

cd $analysis_path

rm -r $name

mkdir $name

mv $name.coffea $name

cd ../trigger_efficiency_mc

python3 HistogramingProcessor.py
