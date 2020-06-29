# 
# Recipe to continue the setup of our 92X analysis after the checkout of TopEFT package
#
eval `scram runtime -sh`
cd $CMSSW_BASE/src

git clone https://github.com/HephySusySW/RootTools
scram b -j9

#
cd $CMSSW_BASE/src
#compile
scram b -j 8 
