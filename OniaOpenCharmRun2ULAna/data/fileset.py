import yaml

# For update the filesets use the fileset.yaml file. This script creates a dict with the filesets path.
# dict keys are formed with the primary_dataset + year + datatier
# the values are arrays containing the path of each file (they are formed from the .txt files in the folder data)

filesets = {}

filesets_yaml = yaml.load(open("data/fileset.yaml", "r"), Loader=yaml.FullLoader)

for f in filesets_yaml:
   array = filesets_yaml[f]
   for i in array:
      filesets[i['primary_dataset'] + i['year'] + i['datatier']] = []
      for l in i['path']:
         path = open(l)
         filesets[i['primary_dataset'] + i['year'] + i['datatier']] += path.read().splitlines()
