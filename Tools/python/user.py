import os

runOnGentT2 = True

if os.environ['USER'] in ['schoef', 'rschoefbeck', 'schoefbeck']:
    results_directory   = "/afs/hephy.at/data/rschoefbeck02/TopEFT/results/"
    skim_output_directory      = "/afs/hephy.at/data/rschoefbeck02/TopEFT/skims/"
    skim_directory      = "/afs/hephy.at/data/dspitzbart01/TopEFT/skims/"
    tmp_directory       = "/afs/hephy.at/data/rschoefbeck02/TopEFT_tmp/"
    plot_directory      = "/afs/hephy.at/user/r/rschoefbeck/www/TopEFT/"
    data_directory      = "/afs/hephy.at/data/dspitzbart02/cmgTuples/"
    mva_directory       = "/afs/hephy.at/data/cms04/ttschida/weights/"
    #data_directory      = "/afs/hephy.at/data/rschoefbeck02/cmgTuples/"
    #postprocessing_output_directory = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/"
    postprocessing_output_directory = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/"
    analysis_results    = results_directory

    runOnGentT2 = False

if os.environ['USER'] in ['dspitzbart', 'dspitzba']:
    tmp_directory       = "/home/users/dspitzba/Top_tmp/"
    results_directory   = "/home/users/dspitzba/TopEFT/results/"
    skim_directory      = "/home/users/dspitzba/TopEFT/skims/"
    skim_output_directory      = "/home/users/dspitzba/TopEFT/skims/"
    plot_directory      = "/home/users/dspitzba/public_html/TopEFT/"
    combineReleaseLocation = '/afs/hephy.at/work/d/dspitzbart/top/devel/CMSSW_8_1_0/src'
    #data_directory = "/afs/hephy.at/data/dspitzbart02/cmgTuples/"
    data_directory     = "/home/users/dspitzba/"
    postprocessing_output_directory = "/home/users/dspitzba/"
    analysis_results    = results_directory
    
    runOnGentT2 = False

