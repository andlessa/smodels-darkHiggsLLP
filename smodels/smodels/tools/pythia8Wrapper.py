#!/usr/bin/env python3

"""
.. module:: pythia8Wrapper
   :synopsis: Wrapper for pythia8.

.. moduleauthor:: Wolfgang Waltenberger <wolfgang.waltenberger@gmail.com>

"""

from __future__ import print_function
from smodels.tools.wrapperBase import WrapperBase
from smodels.tools import wrapperBase
from smodels.base.smodelsLogging import logger, setLogLevel
from smodels.base.physicsUnits import fb, pb, TeV, mb
from smodels.base.crossSection import getXsecFromLHEFile
from smodels import installation
from smodels.tools.pythia8particles import particles
from smodels.decomposition.exceptions import SModelSDecompositionError as SModelSError
import os, sys, io, shutil

try:
    import commands as executor  # python2
except ImportError:
    import subprocess as executor # python3

class Pythia8Wrapper(WrapperBase):
    """
    An instance of this class represents the installation of pythia8.
    """

    def __init__(self,
                 configFile="<install>/smodels/etc/pythia8.cfg",
                 executablePath="<install>/smodels/lib/pythia8/pythia8.exe",
                 srcPath="<install>/smodels/lib/pythia8/"):
        """
        :param configFile: Location of the config file, full path; copy this
                           file and provide tools to change its content and to provide a template
        :param executablePath: Location of executable, full path (pythia8.exe)
        :param srcPath: Location of source code
        """

        WrapperBase.__init__(self)
        self.name = "pythia8"
        self.executablePath = self.absPath(executablePath)
        self.executable = None
        self.srcPath = self.absPath(srcPath)
        self.version = self.getPythiaVersion()
        includeFile = f"<install>/smodels/lib/pythia8/pythia{self.version}/include/Pythia8/Pythia.h"
        self.includeFile = self.absPath ( includeFile )
        self.compiler = "C++"
        self.tempdir = None
        self.cfgfile = self.checkFileExists(configFile)
        self.keepTempDir = False
        self.nevents = 10000
        self.sqrts = 13
        self.secondsPerEvent = 10
        self.pythiacard = None

        self.unlink()

    def getPythiaVersion( self ):
        """obtain the pythia version we wish to use, stored in file 'pythiaversion'"""
        versionfile = f"{self.srcPath}/pythiaversion"
        if not os.path.exists( versionfile ):
            print( f"[installer.py] error cannot determine pythiaversion: did not find {versionfile}")
            sys.exit(-1)
        with open( versionfile, "rt") as f:
            ver = f.read()
            ver = ver.strip()
            f.close()
        return ver

    def checkFileExists(self, inputFile):
        """
        Check if file exists, raise an IOError if it does not.

        :returns: absolute file name if file exists.

        """
        nFile = self.absPath(inputFile)
        if not os.path.exists(nFile):
            raise IOError( f"file {nFile} does not exist" )
        return nFile

    def __str__(self):
        """
        Describe the current status

        """
        ret = f"tool: {self.name}\n"
        ret += f"executable: {self.executablePath}\n"
        ret += f"temp dir: {self.tempdir}\n"
        ret += f"nevents: {self.nevents}\n"
        return ret

    def unlink(self, unlinkdir=True):
        """
        Remove temporary files.

        :param unlinkdir: remove temp directory completely

        """
        if self.tempdir == None:
            return
        if self.keepTempDir:
            logger.warning("Keeping everything in " + self.tempdir)
            return
        logger.debug("Unlinking " + self.tempdir)
        for inputFile in ["fort.61", "fort.68", "log"]:
            if os.path.exists(self.tempdir + "/" + inputFile):
                os.unlink(self.tempdir + "/" + inputFile)
        if unlinkdir:
            for inputFile in ["temp.cfg"]:
                os.unlink(self.tempdir + "/" + inputFile)
            if os.path.exists(self.tempdir):
                os.rmdir(self.tempdir)
                self.tempdir = None

    def checkInstallation ( self, compile : bool = True ):
        # super().checkInstallation(compile)
        exists = os.path.exists ( self.includeFile )
        xmldoc = self.getXmldoc()
        sleep = 0.
        while not os.path.exists ( xmldoc ) or not os.path.exists ( self.executablePath ): # if this disappears, start from scratch
            import time
            sleep += .5
            time.sleep ( sleep )
            if sleep > .5 and not os.path.exists ( xmldoc ) or not os.path.exists ( self.executablePath ):
                if compile:
                    # after a few seconds, delete, if compile is true
                    import shutil
                    p = xmldoc.find ( "share" )
                    rm = xmldoc[:p-1]
                    if False:
                        shutil.rmtree ( rm, ignore_errors = True )
                    self.compile()
                exists = False
                break

        if xmldoc == None:
            exists = False
        if exists:
            return True
        if compile:
            self.compile()
        exists = os.path.exists ( self.includeFile )
        return exists

    def getXmldoc ( self ):
        """ get the content of xml.doc """
        xmldoc = self.executablePath.replace( "pythia8.exe", "xml.doc" )
        logger.debug( f"exe path={self.executablePath}" )
        if not os.path.exists ( xmldoc ):
            return None
        if os.path.exists(xmldoc):
            logger.debug(f"xml.doc found at {xmldoc}.")
            with open(xmldoc) as f:
                xmlDir = f.read()
                toadd = os.path.join(os.path.dirname(xmldoc), xmlDir.strip())
        #if not os.path.exists ( toadd ):
        #    return None
        return toadd

    def run(self, slhaFile, lhefile=None, unlink=True):
        """
        Run pythia8.

        :param slhaFile: SLHA file
        :param lhefile: option to write LHE output to file; if None, do not write
                        output to disk. If lhe file exists, use its events for
                        xsecs calculation.
        :param unlink: clean up temporary files after run?
        :returns: List of cross sections

        """
        if self.maycompile:
            self.checkInstallation( compile = True )
        # Change pythia configuration file, if defined:
        if self.pythiacard:
            pythiacard_default = self.cfgfile
            self.cfgfile = self.pythiacard

        self.xsecs = {}
        logger.debug("wrapper.run()")
        slha = self.checkFileExists(slhaFile)
        logger.debug("file check: " + slha)
        cfg = self.absPath(self.cfgfile)
        logger.debug("running with cfgfile " + str(cfg))
        lhefile = self.tempDirectory() + "/events.lhe"
        cmd = f"{self.executablePath} -n {self.nevents} -f {slha} -s {self.sqrts} -c {cfg} -l {lhefile}"
        toadd = self.getXmldoc()
        if toadd != None and os.path.exists ( toadd ):
            logger.debug( f"adding -x {toadd}" )
            cmd += f" -x {toadd}"
        logger.debug( f"Now running ''{cmd}''" )
        out = executor.getoutput(cmd)
        logger.debug( f"out={out}" )
        if not os.path.isfile(lhefile):
            raise SModelSError( f"LHE file {lhefile} not found" )
        lheF = open(lhefile, "r")
        lhedata = lheF.read()
        lheF.close()
        os.remove(lhefile)
        if not "<LesHouchesEvents" in lhedata:
            raise SModelSError("No LHE events found in pythia output")
        if not unlink:
            tempfile = self.tempDirectory() + "/log"
            f = open(tempfile, "w")
            f.write(cmd + "\n\n\n")
            f.write(out + "\n")
            f.write(lhedata + "\n")
            f.close()
            logger.info( f"stored everything in {tempfile}" )

        # Create memory only file object
        if sys.version[0] == "2":
            lhedata = unicode(lhedata)
        lheFile = io.StringIO(lhedata)
        ret = getXsecFromLHEFile(lheFile)

        # Reset pythia card to its default value
        if self.pythiacard:
            self.cfgfile = pythiacard_default

        if unlink:
            shutil.rmtree(self.tempDirectory())
            # print ( "rmtree", self.tempDirectory() )

        return ret

    def chmod(self):
        """
        chmod 755 on pythia executable, if it exists.
        Do nothing, if it doesnt exist.
        """
        if not os.path.exists(self.executablePath):
            logger.error( f"{self.executablePath} doesnt exist" )
            return False
        import stat

        mode = stat.S_IRWXU | stat.S_IRWXG | stat.S_IXOTH | stat.S_IROTH
        os.chmod(self.executablePath, mode)
        return True


if __name__ == "__main__":
    setLogLevel("debug")
    tool = Pythia8Wrapper()
    tool.nevents = 10
    logger.info("installed: " + str(tool.installDirectory()))
    logger.info("check: " + wrapperBase.ok(tool.checkInstallation()))
    logger.info( f"seconds per event: {tool.secondsPerEvent}" )
    slhafile = "inputFiles/slha/simplyGluino.slha"
    slhapath = os.path.join(installation.installDirectory(), slhafile)
    logger.info("slhafile: " + slhapath)
    output = tool.run(slhapath, unlink=True)
    logger.info( f"done: {output}" )
