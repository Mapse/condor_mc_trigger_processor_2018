#!/bin/bash

set -e

hostname
date

echo "---------------working dir---------------"
ls
#tar -zxf WORKDIR.tar.gz
#rm -rf WORKDIR.tar.gz
#cat *_jobs/*
mv *_jobs/ OniaOpenCharmRun2ULAna/.
echo $1

echo "Done"
echo "---------------Creating Python Environment---------------"

export HOME=$PWD
export PATH

sh Miniconda3-latest-Linux-x86_64.sh -b -p $PWD/miniconda3
export PATH=$PWD/miniconda3/bin:$PATH
rm -rf Miniconda3-latest-Linux-x86_64.sh

python -m pip install --upgrade pip
python -m pip install --upgrade --ignore-installed --force-reinstall coffea

conda install -c conda-forge xrootd

ls

echo "Done"
echo "---------------Starting the processing---------------"

cd OniaOpenCharmRun2ULAna
ls -a

python nanoAODplus_condor.py $1

