# Analysis Onia + Open Charm

Repository for Quarkonia + Open Charm Analysis using Run2 UL datasets.

# Instalation instructions

## Setting up the conda environment

Miniconda should be installed as in:

https://conda.io/projects/conda/en/latest/user-guide/install/linux.html

```
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b 
~/miniconda3/bin/conda init
echo 'conda deactivate ; conda deactivate' >> ~/.bashrc
rm Miniconda3-latest-Linux-x86_64.sh
```

After installation, reload the session.

## Setup conda Environmment (only once!)

```
conda deactivate ; conda deactivate 

conda env create -f environment.yml

# for jupyterlab w/ ipython widgets
conda activate OniaOpenCharmRun2ULenv
jupyter labextension install @jupyter-widgets/jupyterlab-manager

#only if CMSSW needed:

#export SCRAM_ARCH=slc7_amd64_gcc700

#cmsrel CMSSW_10_6_12
#cd CMSSW_10_6_12/src
#cmsenv

#######################

mkdir plots
mkdir output
```

## Set the virtual environment after setup:

```
cd OniaOpenCharmRun2ULAna
. quick_setup.sh
```
