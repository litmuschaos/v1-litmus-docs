import os
import re
import glob
from re import sub

# function to convert string to camelCase
def camelCase(string):
  if (string != string.lower() and string != string.upper() and "_" not in string):
      return string
  else:
      string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
  return string[0].lower() + string[1:]

# function to convert string to pascalCase
def pascalCase(string):
  return capitalCase(camelCase(string))

# function to convert string to capitalCase
def capitalCase(string):
    string = str(string)
    if not string:
        return string
    return upperCase(string[0]) + string[1:]  

# function to convert string to upperCase
def upperCase(string):
    return str(string).upper() 

# function to convert string to lowerCase
def lowerCase(string):
    return str(string).lower()

specString = ['chaos service account','ChaosServiceAccount','chaosserviceaccount','job cleanup policy','JobCleanUpPolicy','jobcleanuppolicy',
              'auxiliary app info','AuxiliaryAppInfo','Auxiliary app info','EngineState','Engine state','engineState','engine state'
              'AnnotationCheck','annotationCheck','annotation check','annotation checks','app info','appinfo','AppInfo','appInfo',
              'appns','AppNs','app ns','appNS','appLabel','applabel','Applabel','app label','appKind','appkind','Appkind','app kind',
              'appinfo','AppInfo','app info','imagePullPolicy','image pull policy','ImagePullPolicy','image','apiVersion','api version',
             ]

resourceString = ['chaos engine','Chaos Engine','chaosEngine','Chaosengine'
                  'chaos experiment','Chaos Experiment','chaosExperiment','Chaosexperiment',
                  'chaos result','Chaos Result','chaosResult','Chaosresult','chaos results',
                  'chaos schedule','Chaos Schedule','chaosSchedule','Chaosschedule',
                  'chaos observability','Chaos Observability','chaosObservability','Chaosobservability',
                  'chaos operator','Chaos Operator','chaosOperator','Chaosoperator',
                  'chaos runner','Chaos Runner','chaosRunner','Chaosrunner',
                  'chaos exporter','Chaos Exporter','chaosExporter','ChaosExporter',
                  'chaos charts','Chaos Charts','chaosCharts','ChaosCharts', 'chaos chart',
                 ]


# It converts the spec components into camel case
path = 'docs'
for filename in glob.glob(os.path.join(path, '*.md')):
   with open(os.path.join(filename), 'rt') as fin:
       data = fin.read()
       for i in specString:
           if data.find(i) > 0:
               convCamelCase=camelCase(i)
               data = data.replace(i,convCamelCase)
       fin.close()
   with open(os.path.join(filename), 'wt') as fin:
       fin.write(data)
       fin.close()

# It converts component names into pascal case
path = 'docs'
for filename in glob.glob(os.path.join(path, '*.md')):
   with open(os.path.join(filename), 'rt') as fin:
       data = fin.read()
       for i in resourceString:
           if data.find(i) > 0:
               convPascalCase=pascalCase(i)
               data = data.replace(i,convPascalCase)
       fin.close()
   with open(os.path.join(filename), 'wt') as fin:
       fin.write(data)
       fin.close()

