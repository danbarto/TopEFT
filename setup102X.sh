# 
# Recipe to continue the setup of our 102X analysis after the checkout of TopEFT package
#
eval `scram runtime -sh`
cd $CMSSW_BASE/src

git clone https://github.com/HephySusySW/RootTools
#git clone https://github.com/TTXPheno/TTXPheno ## not used atm

#compile
cd $CMSSW_BASE/src
scram b -j9
