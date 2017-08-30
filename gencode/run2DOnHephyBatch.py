# Standard imports
import os
import time
import itertools
import argparse

import TopEFT.tools.logger as logger

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',    action='store',         nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], default='INFO', help="Log level for logging" )

args = argParser.parse_args()

logger = logger.get_logger(args.logLevel, logFile = None)

def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in xrange(0, len(l), n)]

model_name = "ewkDM"

# for 4D scans
nonZeroCouplings = ("DC1V","DC1A","DC2V","DC2A")
dc1v = [ i*1.3/4 for i in range(-4,3) ]
dc1a = [ i*1.3/4 for i in range(-2,5) ]
dc2v = [ i*0.15/3 for i in range(-3,4) ]
dc2a = [ i*0.15/3 for i in range(-3,4) ]
couplingValues = [dc1v,dc1a,dc2v,dc2a]

# for 2D scans
nonZeroCouplings = ("DC2V","DC2A")
dc2v = [ i*0.25/5 for i in range(-5,6) ]
dc2a = [ i*0.25/5 for i in range(-5,6) ]
couplingValues = [dc2v,dc2a]

# prepare the grid with all points
couplingGrid = [ a for a in itertools.product(*couplingValues) ]

# zip with coupling names
allCombinations =  [ zip(nonZeroCouplings, a) for a in couplingGrid ]
allCombinationsFlat = []
for comb in allCombinations:
    allCombinationsFlat.append([item for sublist in comb for item in sublist])


processes = ['ttZ','ttW','ttH']
#submitCMD = "submitBatch.py"
submitCMD = "echo"

nJobs = len(processes)*len(allCombinationsFlat)

logger.info("Will need to run over %i combinations.",nJobs)

combinationChunks = chunks(allCombinationsFlat, 40)

for p in processes[:1]:
    for i,comb in enumerate(combinationChunks):
        with open("%s_%i.txt"%(p,i), 'w') as f:
            for c in comb:
                strBase = "{} {} "*nDim
                couplingStr = (strBase+'\n').format(*c)
                f.write(couplingStr)
                
        os.system(submitCMD+" --title DM_%s_%i 'python calcXSecModified.py --model "%(p,i)+model_name+" --process "+p+" --couplings %s_%i.txt'"%(p,i))
