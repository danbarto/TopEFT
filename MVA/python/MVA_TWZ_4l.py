#!/usr/bin/env python

# Standard imports
from operator                    import attrgetter
from math import pi, sqrt, cosh
import ROOT

# helpers
from TopEFT.Tools.helpers import deltaPhi, deltaR2, deltaR

# Logger
import TopEFT.Tools.logger as logger
logger = logger.get_logger("INFO", logFile = None )

# Training variables
read_variables = [\
                    "weight/F",
                    "nBTag/I",
                    "nJetSelected/I",
                    "met_pt/F", "met_phi/F",
                    "ht/F",
                    "lep[pt/F,eta/F,phi/F]",
                    "nonZ1_l1_index_4l/I", "nonZ_l1_index/I",
                    "nonZ1_l2_index_4l/I", "nonZ_l2_index/I",
                    "Z1_pt_4l/F", "Z1_eta_4l/F", "Z1_phi_4l/F", "Z1_mass_4l/F", "Z1_cosThetaStar_4l/F",
                    "jet[pt/F,eta/F,phi/F,btagDeepCSV/F]",
                    "nMuons_tight_4l/I", "nElectrons_tight_4l/I",
                    "nlep/I",
                    ]

# sequence 
sequence = []

def flavorBin( event, sample=None):
    event.flavorBin = 0

    if      event.nMuons_tight_4l==4 and event.nElectrons_tight_4l==0: event.flavorBin = 1 
    elif    event.nMuons_tight_4l==3 and event.nElectrons_tight_4l==1: event.flavorBin = 2
    elif    event.nMuons_tight_4l==2 and event.nElectrons_tight_4l==2: event.flavorBin = 3
    elif    event.nMuons_tight_4l==1 and event.nElectrons_tight_4l==3: event.flavorBin = 4
    elif    event.nMuons_tight_4l==0 and event.nElectrons_tight_4l==4: event.flavorBin = 5    
#sequence.append( flavorBin )

def getDeltaPhi(event, sample=None):
    event.nonZl1_Z1_deltaPhi = deltaPhi(event.lep_phi[event.nonZ1_l1_index_4l], event.Z1_phi_4l)
    event.nonZl2_Z1_deltaPhi = deltaPhi(event.lep_phi[event.nonZ1_l2_index_4l], event.Z1_phi_4l)
sequence.append( getDeltaPhi )

def getDeltaEta(event, sample=None):
    event.nonZl1_Z1_deltaEta = abs(event.lep_eta[event.nonZ1_l1_index_4l] - event.Z1_eta_4l) 
    event.nonZl2_Z1_deltaEta = abs(event.lep_eta[event.nonZ1_l2_index_4l] - event.Z1_eta_4l)
sequence.append( getDeltaEta )

def getDeltaR(event, sample=None):
    event.nonZl1_Z1_deltaR     = deltaR({'eta':event.lep_eta[event.nonZ1_l1_index_4l], 'phi':event.lep_phi[event.nonZ1_l1_index_4l]}, {'eta':event.Z1_eta_4l, 'phi':event.Z1_phi_4l})
    event.nonZl2_Z1_deltaR     = deltaR({'eta':event.lep_eta[event.nonZ1_l2_index_4l], 'phi':event.lep_phi[event.nonZ1_l2_index_4l]}, {'eta':event.Z1_eta_4l, 'phi':event.Z1_phi_4l})
    event.jet0_Z1_deltaR       = deltaR({'eta':event.jet_eta[0], 'phi':event.jet_phi[0]}, {'eta':event.Z1_eta_4l, 'phi':event.Z1_phi_4l})
    event.jet0_nonZl1_deltaR   = deltaR({'eta':event.jet_eta[0], 'phi':event.jet_phi[0]}, {'eta':event.lep_eta[event.nonZ1_l1_index_4l], 'phi':event.lep_phi[event.nonZ1_l1_index_4l]})
    event.jet0_nonZl2_deltaR   = deltaR({'eta':event.jet_eta[0], 'phi':event.jet_phi[0]}, {'eta':event.lep_eta[event.nonZ1_l2_index_4l], 'phi':event.lep_phi[event.nonZ1_l2_index_4l]})
    event.jet1_Z1_deltaR       = deltaR({'eta':event.jet_eta[1], 'phi':event.jet_phi[1]}, {'eta':event.Z1_eta_4l, 'phi':event.Z1_phi_4l})
    event.jet1_nonZl1_deltaR   = deltaR({'eta':event.jet_eta[1], 'phi':event.jet_phi[1]}, {'eta':event.lep_eta[event.nonZ1_l1_index_4l], 'phi':event.lep_phi[event.nonZ1_l1_index_4l]})
    event.jet1_nonZl2_deltaR   = deltaR({'eta':event.jet_eta[1], 'phi':event.jet_phi[1]}, {'eta':event.lep_eta[event.nonZ1_l2_index_4l], 'phi':event.lep_phi[event.nonZ1_l2_index_4l]})
    event.jet2_Z1_deltaR       = deltaR({'eta':event.jet_eta[2], 'phi':event.jet_phi[2]}, {'eta':event.Z1_eta_4l, 'phi':event.Z1_phi_4l})
    event.jet2_nonZl1_deltaR   = deltaR({'eta':event.jet_eta[2], 'phi':event.jet_phi[2]}, {'eta':event.lep_eta[event.nonZ1_l1_index_4l], 'phi':event.lep_phi[event.nonZ1_l1_index_4l]})
    event.jet2_nonZl2_deltaR   = deltaR({'eta':event.jet_eta[2], 'phi':event.jet_phi[2]}, {'eta':event.lep_eta[event.nonZ1_l2_index_4l], 'phi':event.lep_phi[event.nonZ1_l2_index_4l]})

##    event.nonZl1_nonZl2_deltaR = deltaR({'eta':event.lep_eta[event.nonZ1_l1_index_4l], 'phi':event.lep_phi[event.nonZ1_l1_index_4l]}, {'eta':event.lep_eta[event.nonZ1_l2_index_4l], 'phi':event.lep_phi[event.nonZ1_l2_index_4l]})
sequence.append( getDeltaR )

## met, ht, nonZ1_pt/eta, Z1_pt, nJet, nBTag, lep1_eta
#mva_variables =  {
##                    "met_pt"    :attrgetter("met_pt"), # copy
#                    "ht"        :attrgetter("ht"), # copy
#                    "lnonZ1_pt" :(lambda event: event.lep_pt[event.nonZ1_l1_index_4l]),
#                    "lnonZ1_eta":(lambda event: event.lep_eta[event.nonZ1_l1_index_4l]),
#                    "Z1_pt_4l"  :attrgetter("Z1_pt_4l"),
##                    "lep1_pt"   :(lambda event: event.lep_pt[0]),
##                    "lep2_pt"   :(lambda event: event.lep_pt[1]),
#                    "lep1_eta"  :(lambda event: event.lep_eta[0]),
##                    "lep2_eta"  :(lambda event: event.lep_eta[1]),
#                    "nJetSelected":attrgetter("nJetSelected"),
#                    "nBTag"     :attrgetter("nBTag"),      
##                    "yield"     :(lambda event: event.flavorBin),
##                    "jet1_pt"   :(lambda event: event.jet_pt[0]),
##                    "nLepLoose":(lambda event: event.nlep),
#                    #"myvar1" :(lambda event: event.nBTag), # calculate on the fly
#                    #"myvar2" :(lambda event: event.myFancyVar), # from sequence
#        

mva_variables = {
                "mva_ht"                    :(lambda event, sample: event.ht),
                "mva_met_pt"                :(lambda event, sample: event.met_pt),
                "mva_nJetSelected"          :(lambda event, sample: event.nJetSelected),
                "mva_nBTag"                 :(lambda event, sample: event.nBTag),
#                "mva_flavorBin"             :(lambda event, sample: event.flavorBin),
#                "mva_nlep"                  :(lambda event, sample: event.nlep),
                

                "mva_jet0_pt"               :(lambda event, sample: event.jet_pt[0]          if event.nJetSelected >=1 else 0),
                "mva_jet0_eta"              :(lambda event, sample: event.jet_eta[0]         if event.nJetSelected >=1 else -10),
                "mva_jet0_btagDeepCSV"      :(lambda event, sample: event.jet_btagDeepCSV[0] if event.nJetSelected >=1 else -10),              
                "mva_jet1_pt"               :(lambda event, sample: event.jet_pt[1]          if event.nJetSelected >=2 else 0),
                "mva_jet1_eta"              :(lambda event, sample: event.jet_eta[1]         if event.nJetSelected >=2 else -10),
                "mva_jet1_btagDeepCSV"      :(lambda event, sample: event.jet_btagDeepCSV[1] if event.nJetSelected >=2 else -10),
                "mva_jet2_pt"               :(lambda event, sample: event.jet_pt[2]          if event.nJetSelected >=3 else 0),
                "mva_jet2_eta"              :(lambda event, sample: event.jet_eta[2]         if event.nJetSelected >=3 else -10),
                "mva_jet2_btagDeepCSV"      :(lambda event, sample: event.jet_btagDeepCSV[2] if event.nJetSelected >=3 else -10),

                "mva_nonZ1_l1_pt"           :(lambda event, sample: event.lep_pt[event.nonZ1_l1_index_4l]),
#                "mva_nonZ1_l1_eta"          :(lambda event, sample: event.lep_eta[event.nonZ1_l1_index_4l]),
                "mva_nonZ1_l2_pt"           :(lambda event, sample: event.lep_pt[event.nonZ1_l2_index_4l]),
#                "mva_nonZ1_l2_eta"          :(lambda event, sample: event.lep_eta[event.nonZ1_l2_index_4l]),
#                "mva_nonZl1_nonZl2_deltaR"  :(lambda event, sample: event.nonZl1_nonZl2_deltaR),                

                "mva_Z1_pt_4l"              :(lambda event, sample: event.Z1_pt_4l),
                "mva_Z1_eta_4l"             :(lambda event, sample: event.Z1_eta_4l),
                "mva_Z1_cosThetaStar_4l"    :(lambda event, sample: event.Z1_cosThetaStar_4l),
                "mva_Z1_mass_4l"            :(lambda event, sample: event.Z1_mass_4l),  
             
#                "mva_nonZl1_Z1_deltaPhi"    :(lambda event, sample: event.nonZl1_Z1_deltaPhi),
#                "mva_nonZl1_Z1_deltaEta"    :(lambda event, sample: event.nonZl1_Z1_deltaEta),
                "mva_nonZl1_Z1_deltaR"      :(lambda event, sample: event.nonZl1_Z1_deltaR),
#                "mva_nonZl2_Z1_deltaPhi"    :(lambda event, sample: event.nonZl2_Z1_deltaPhi),
#                "mva_nonZl2_Z1_deltaEta"    :(lambda event, sample: event.nonZl2_Z1_deltaEta),
                "mva_nonZl2_Z1_deltaR"      :(lambda event, sample: event.nonZl2_Z1_deltaR),

                "mva_jet0_Z1_deltaR"        :(lambda event, sample: event.jet0_Z1_deltaR        if event.nJetSelected >=1 else -1),
                "mva_jet0_nonZl1_deltaR"    :(lambda event, sample: event.jet0_nonZl1_deltaR    if event.nJetSelected >=1 else -1),
                "mva_jet0_nonZl2_deltaR"    :(lambda event, sample: event.jet0_nonZl2_deltaR    if event.nJetSelected >=1 else -1),
                "mva_jet1_Z1_deltaR"        :(lambda event, sample: event.jet1_Z1_deltaR        if event.nJetSelected >=2 else -1),
                "mva_jet1_nonZl1_deltaR"    :(lambda event, sample: event.jet1_nonZl1_deltaR    if event.nJetSelected >=2 else -1),
                "mva_jet1_nonZl2_deltaR"    :(lambda event, sample: event.jet1_nonZl2_deltaR    if event.nJetSelected >=2 else -1),
                "mva_jet2_Z1_deltaR"        :(lambda event, sample: event.jet2_Z1_deltaR        if event.nJetSelected >=3 else -1),
#                "mva_jet2_nonZl1_deltaR"    :(lambda event, sample: event.jet2_nonZl1_deltaR    if event.nJetSelected >=3 else -1),
#                "mva_jet2_nonZl2_deltaR"    :(lambda event, sample: event.jet2_nonZl2_deltaR    if event.nJetSelected >=3 else -1),
 
               }

bdt1 = {
"type"                : ROOT.TMVA.Types.kBDT,
"name"                : "bdt1",
"color"               : ROOT.kGreen,
"options"             : ["!H","!V","NTrees=250","BoostType=Grad","Shrinkage=0.20","UseBaggedBoost","GradBaggingFraction=0.5","SeparationType=GiniIndex","nCuts=50","PruneMethod=NoPruning","MaxDepth=1"],
}

bdt2 = {
"type"                : ROOT.TMVA.Types.kBDT,
"name"                : "bdt2",
"color"               : ROOT.kRed,
"options"             : ["!H","!V","NTrees=250","BoostType=Grad","Shrinkage=0.20","UseBaggedBoost","GradBaggingFraction=0.5","SeparationType=GiniIndex","nCuts=250","PruneMethod=NoPruning","MaxDepth=1"],
}

bdt3 = {
"type"                : ROOT.TMVA.Types.kBDT,
"name"                : "bdt3",
"color"               : ROOT.kBlack,
"options"             : ["!H","!V","NTrees=250","BoostType=Grad","Shrinkage=0.20","UseBaggedBoost","GradBaggingFraction=0.5","SeparationType=GiniIndex","nCuts=1000","PruneMethod=NoPruning","MaxDepth=1"],
}

bdt4 = {
"type"                : ROOT.TMVA.Types.kBDT,
"name"                : "bdt4",
"color"               : ROOT.kRed,
"options"             : ["!H","!V","NTrees=250","BoostType=Grad","Shrinkage=0.20","UseBaggedBoost","GradBaggingFraction=0.5","SeparationType=GiniIndex","nCuts=2000","PruneMethod=NoPruning","MaxDepth=1"],
}

mlp1 = {
"type"                : ROOT.TMVA.Types.kMLP,
"name"                : "mlp1",
"layers"              : "N+3", 
"color"               : ROOT.kRed+5,
"options"             : ["!H","!V","VarTransform=Norm,Deco","NeuronType=sigmoid","NCycles=10000","TrainingMethod=BP","LearningRate=0.03", "DecayRate=0.01","Sampling=0.3","SamplingEpoch=0.8","ConvergenceTests=1","CreateMVAPdfs=True","TestRate=10" ],
}

mlp2 = {
"type"                : ROOT.TMVA.Types.kMLP,
"name"                : "mlp2",
"layers"              : "N+5",
"color"               : ROOT.kYellow,
"options"             : ["!H","!V","VarTransform=Norm,Deco","NeuronType=sigmoid","NCycles=10000","TrainingMethod=BP","LearningRate=0.03", "DecayRate=0.01","Sampling=0.3","SamplingEpoch=0.8","ConvergenceTests=1","CreateMVAPdfs=True","TestRate=10" ],
}

mlp3 = {
"type"                : ROOT.TMVA.Types.kMLP,
"name"                : "mlp3",
"layer"               : "N+7",
"color"               : ROOT.kBlue,
"options"             : ["!H","!V","VarTransform=Norm,Deco","NeuronType=sigmoid","NCycles=10000","TrainingMethod=BP","LearningRate=0.03", "DecayRate=0.01","Sampling=0.3","SamplingEpoch=0.8","ConvergenceTests=1","CreateMVAPdfs=True","TestRate=10" ],
}

mlp = {
"type"                : ROOT.TMVA.Types.kMLP,
"name"                : "mlp",
"layers"              : "N,1",
"color"               : ROOT.kRed,
"options"             : ["!H","!V","VarTransform=Norm,Deco","NeuronType=sigmoid","NCycles=10000","TrainingMethod=BP","LearningRate=0.02","DecayRate=0.01","Sampling=0.5","SamplingEpoch=0.5","ConvergenceTests=1","CreateMVAPdfs=True","TestRate=10"]
}



