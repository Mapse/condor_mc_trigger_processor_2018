
## Variable definitions

# Take the current directory to come back when producing the final txt file
here='/afs/cern.ch/work/m/mabarros/public/CMSSW_10_6_12/src/condor/MC_Trigger_processor/2018'

# Main path where the NanoAODPlus files are stored
main_path='/eos/user/m/mabarros/Monte_Carlo/2018'

# Txt file name that we provide to our condor code
file_name='Monte_Carlo_JpsiDstar_DPS_2018_path.txt'

rm $file_name

## Do the magic (In case of more files just add or create a better logic!)

cd $main_path 

cd 0000/ && ls -d "$PWD"/* > a0.txt && mv a0.txt $here

cd ../0001 && ls -d "$PWD"/* > a1.txt && mv a1.txt $here

cd ../0002 && ls -d "$PWD"/* > a2.txt && mv a2.txt $here

cd ../0003 && ls -d "$PWD"/* > a3.txt && mv a3.txt $here

cd ../0004 && ls -d "$PWD"/* > a4.txt && mv a4.txt $here

cd ../0005 && ls -d "$PWD"/* > a5.txt && mv a5.txt $here

cd ../0006 && ls -d "$PWD"/* > a6.txt && mv a6.txt $here

cd ../0007 && ls -d "$PWD"/* > a7.txt && mv a7.txt $here

cd ../0008 && ls -d "$PWD"/* > a8.txt && mv a8.txt $here

cd $here

cat a0.txt a1.txt a2.txt a3.txt a4.txt a5.txt a6.txt a7.txt a8.txt > $file_name

rm a*.txt


