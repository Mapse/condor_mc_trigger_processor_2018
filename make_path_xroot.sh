
voms-proxy-init --rfc --voms cms -valid 192:00

## Variable definitions


# Txt file name that we provide to our condor code
file_name='Monte_Carlo_Jpsi_25to45_Dstar_DPS_2018_13TeV_path.txt'

radic='Jpsi_25to45_Dstar_DPS_2018_13TeV_NanoAODPlus_'


echo 'Taking paths...'

xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0000 > a0.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0001 > a1.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0002 > a2.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0003 > a3.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0004 > a4.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0005 > a5.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0006 > a6.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0007 > a7.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0008 > a8.txt
xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0009 > a9.txt
#xrdfs xrootd-redir.ultralight.org ls -u /store/group/uerj/mabarros/CRAB_PrivateMC_RunII_UL_2018/Jpsi_25to45_Dstar_DPS_2018_13TeV/220508_053446/0010 > a10.txt

echo 'Done :)'
echo 'Correcting paths...'

python3 correct_path.py -t='a0.txt' -f=$radic   
python3 correct_path.py -t='a1.txt' -f=$radic
python3 correct_path.py -t='a2.txt' -f=$radic
python3 correct_path.py -t='a3.txt' -f=$radic
python3 correct_path.py -t='a4.txt' -f=$radic
python3 correct_path.py -t='a5.txt' -f=$radic
python3 correct_path.py -t='a6.txt' -f=$radic
python3 correct_path.py -t='a7.txt' -f=$radic
python3 correct_path.py -t='a8.txt' -f=$radic
python3 correct_path.py -t='a9.txt' -f=$radic
#python3 correct_path.py -t='a10.txt' -f=$radic

echo 'Making final txt file...'

cat a0.txt a1.txt a2.txt a3.txt a4.txt a5.txt a6.txt a7.txt a8.txt a9.txt > $file_name

rm a*.txt 

echo 'Finished'


