# Standard imports
import os

# Logger
import logging
logger = logging.getLogger(__name__)

class crab:
    def __init__(self, release, releasePath):
        self.release = release
        os.system("scram runtime -sh")
        os.system("source ")

    def config(self):
        return

    def launch(self):
        logger.info( 'Launching jobs with config:' )

        #get the crabDir
        self.crabDir = "" #should be the absolute path

    def status(self, crabDir):
        return
