#!/usr/bin/env python

# Analysis
from Analysis.TMVA.Trainer       import Trainer
from Analysis.TMVA.Reader        import Reader
from Analysis.TMVA.defaults      import default_methods, default_factory_settings 

# TopEFT
from TopEFT.Tools.user           import plot_directory
from TopEFT.Tools.user           import mva_directory 
from TopEFT.Tools.cutInterpreter import *

# MVA configuration
from TopEFT.MVA.MVA_TZZ import bdt1, bdt2, sequence, read_variables, mva_variables 

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--plot_directory',     action='store',             default=None)
argParser.add_argument('--selection',          action='store', type=str,   default='quadlepTWZ')#"quadlepTWZ-onZ1-noZ2")
#argParser.add_argument('--selection',          action='store', type=str,   default="btag1-njet1p")#-btag1-njet1p")#None)
argParser.add_argument('--trainingFraction',   action='store', type=float, default=0.5)
argParser.add_argument('--small',              action='store_true')
argParser.add_argument('--overwrite',          action='store_true')

args = argParser.parse_args()

#Logger

import TopEFT.Tools.logger as logger
logger = logger.get_logger("INFO", logFile = None )

if args.plot_directory == None:
    args.plot_directory = plot_directory

if args.selection == None:
    selectionString = "(1)"
else:
    selectionString = cutInterpreter.cutString( args.selection )



# Samples
from TopEFT.samples.cmgTuples_Summer16_mAODv2_postProcessed import *

#signal      = yt_TWZ
#signal2     = TWZ
signal  = yt_TZZ
signal2 = ZZ

#print "yt_TZZ", signal.chain.CopyTree(selectionString).GetEntries()
#print "ZZ", signal2.chain.CopyTree(selectionString).GetEntries()
#print "yt_TWZ", signal.chain.CopyTree(selectionString).GetEntries()
#print "TWZ", signal2.chain.CopyTree(selectionString).GetEntries()

#exit()

#backgrounds = [ TTZtoLLNuNu ]
backgrounds = [ ZZ ]
samples = backgrounds + [signal]
for sample in samples:
    sample.setSelectionString( selectionString )
    if args.small:
        sample.reduceFiles(to = 1)

mvas = [bdt1, bdt2]

## TMVA Trainer instance
trainer = Trainer( 
    signal = signal, 
    backgrounds = backgrounds, 
    output_directory = mva_directory, 
    plot_directory   = plot_directory, 
    mva_variables    = mva_variables,
    label            = "Test", 
    fractionTraining = args.trainingFraction, 
    )

weightString = "(1)"
trainer.createTestAndTrainingSample( 
    read_variables   = read_variables,   
    sequence         = sequence,
    weightString     = weightString,
    overwrite        = args.overwrite, 
    )

#trainer.addMethod(method = default_methods["BDT"])
#trainer.addMethod(method = default_methods["MLP"])



#ncuts 250
for mva in mvas:
    trainer.addMethod(method = mva)
#trainer.addMethod(method = bdt2)
#trainer.addMethod(method = bdt3)
#trainer.addMethod(method = bdt4)
#trainer.addMethod(method = mlp1)

trainer.trainMVA( factory_settings = default_factory_settings )
trainer.plotEvaluation()

reader = Reader( 
    mva_variables    = mva_variables, 
    weight_directory = './weights/',
    label            = "Test")

reader.addMethod(method = bdt1)
#reader.addMethod(method = default_methods["MLP"])

#print reader.evaluate("BDT", met_pt=100, ht=-210, Z1_pt_4l=100, lnonZ1_pt=100, lnonZ1_eta=0)
#print reader.evaluate("BDT", met_pt=120, ht=-210)
