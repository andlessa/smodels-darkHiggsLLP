#!/usr/bin/env python3

"""
.. module:: runCompleteTestSuite
   :synopsis: Runs all test suites.

.. moduleauthor:: Wolfgang Magerl <wolfgang.magerl@gmail.com>
.. moduleauthor:: Wolfgang Waltenberger <wolfgang.waltenberger@gmail.com>

"""

from __future__ import print_function
import sys, subprocess, os
sys.path.insert(0,"../")
from smodels.base.smodelsLogging import colors
colors.on = True

v=sys.version_info
if v[0] > 2 or ( v[0]==2 and v[1] > 6 ):
    import unittest
if v[0]==2 and v[1] < 7 and v[1] > 3:
    try:
        import unittest2 as unittest
    except ImportError as e:
        print ( "Error: python v",sys.version,"needs unittest2. Please install." )
        sys.exit()
from smodels.base.smodelsLogging import setLogLevel
setLogLevel ( "fatal" )

def isInReducedSet ( t ):
    """ is t in the reduced set of unit tests? """
    t = str(t).lower()
    keywords = [ "cpp", "nllfast", "pythia", "xsec", "interactiveplot",
                 "server", "loadlatest", "notebook", "recipes", "resummino", "toolbox" ]
    for keyword in keywords:
        if keyword in t:
            return False
    return True

def run(filter=None, testNotebooks=False, reduced=False ):

    tests = unittest.TestLoader().discover("./")
    if not testNotebooks:
        tests._tests = [t for t in tests._tests[:] if not 'notebook' in str(t).lower()]
        tests._tests = [t for t in tests._tests[:] if not 'recipes' in str(t).lower()]
    if reduced:
        tests._tests = [t for t in tests._tests[:] if isInReducedSet(t) ]
    if filter is not None:
        tests._tests = [t for t in tests._tests[:] if filter in str(t)]

    ret = unittest.TextTestRunner().run(tests)
    if not ret.wasSuccessful():
        raise AssertionError("%i tests failed" %len(ret.failures))


def verbose_run( filter=None, testNotebooks=False, reduced=False ):
    alltests = unittest.TestLoader().discover("./")

    if not testNotebooks:
        alltests._tests = [t for t in alltests._tests[:] if not 'notebook' in str(t).lower()]
        alltests._tests = [t for t in alltests._tests[:] if not 'recipes' in str(t).lower()]
    if reduced:
        alltests._tests = [t for t in alltests._tests[:] if isInReducedSet(t) ]

    n_tests, n_failed = 0, 0
    n_test = 0
    for series in alltests:
        for test in series:
            if type(test)!=unittest.suite.TestSuite:
                print ( f"{colors.error}Error: could not import ``{test}'' {type(test)}" )
                print ( test._exception, colors.reset )
                continue
            for t in test:
                n_test += 1 
                # if n_test < 190: # we can speed things up here
                #    continue
                if filter and (not filter in str(t)):
                    continue
                n_tests += 1
                print ( "[#%3d] %s ... " % ( n_tests, t.id() ), end="" )
                sys.stdout.flush()
                try:
                    a=t.debug()
                except Exception as e:
                    n_failed += 1
                    print ( "%s FAILED: %s,%s%s" % \
                            ( colors.error, type(e), str(e), colors.reset ) )
                    continue
                print ( "%sok%s" % ( colors.info, colors.reset ) )

                #a=t.run() ## python3
                # print ( "a=",a )
    print( f"[runCompleteTestSuite] {n_failed}/{n_tests} tests failed." )
    if n_failed > 0:
        raise AssertionError( f"{n_failed} tests failed" )


def parallel_run ( verbose, testNotebooks=False, reduced=False ):
    if verbose:
        print ("[runCompleteTestSuite] verbose run not implemented "
               "for parallel version" )
        return
    try:
        from concurrencytest import ConcurrentTestSuite, fork_for_tests
    except ImportError as e:
        print ( "Need to install the module concurrencytest." )
        print ( "pip install concurrencytest" )
        return
    from smodels.base import runtime

    alltests = unittest.TestLoader().discover("./")

    if not testNotebooks:
        alltests._tests = [t for t in alltests._tests[:] if not 'notebook' in str(t).lower()]
    if reduced:
        alltests._tests = [t for t in alltests._tests[:] if isInReducedSet(t) ]

    ncpus = runtime.nCPUs()
    ncpus = max(1,ncpus-2)
    ## "shuffle" the tests, so that the heavy tests get distributed
    ## more evenly among threads (didnt help, so I commented it out)
    #suite._tests = [ item for sublist in [ suite._tests[x::ncpus] \
    #    for x in range(ncpus) ] for item in sublist ]
    concurrent_suite = ConcurrentTestSuite(alltests, fork_for_tests( ncpus ))
    runner = unittest.TextTestRunner()
    ret = runner.run(concurrent_suite)
    if not ret.wasSuccessful():
        raise AssertionError("%i tests failed" %len(ret.failures))


def cleanDatabase ():
    """ remove database pickle files """
    databaseFolders = ['./database', './databaseBroken','./tinydb',
                       './database_extra', './database_simple', './dbadd1']
    for db in databaseFolders:
        for dirpath,_,filenames in os.walk(db):
            for f in filenames:
                if os.path.splitext(f)[1] != '.pcl':
                    continue
                filename = os.path.join(dirpath,f)
                os.remove(filename)

if __name__ == "__main__":

    import argparse
    ap = argparse.ArgumentParser('runs the complete test suite')
    ap.add_argument('-c','--clean_database', help='remove database pickle files',
                    action='store_true')
    ap.add_argument('-v','--verbose', help='run verbosely',action='store_true')
    ap.add_argument('-f','--filter', help='run only tests that have <FILTER> in name. Works only with verbose and not parallel. case sensitive.',type=str,default=None)
    ap.add_argument('-p','--parallel', help='run in parallel',action='store_true')
    ap.add_argument('-n','--notebooks', help='also test notebooks',action='store_true',default=False)
    ap.add_argument('-r','--reduced', help='run reduced set of tests (no C++ interface, no xsec computation or notebook tests)',
                    action='store_true', default = False)
    args = ap.parse_args()

    if args.clean_database:
        print('Deleting database pickle files.')
        cleanDatabase()
    else:
        if not args.notebooks:
            print('Notebooks WILL NOT be tested.')
        if args.reduced:
            print('Reduced set of unit tests')

        if args.parallel:
            parallel_run(args.verbose, args.notebooks, args.reduced)
            sys.exit()
        elif args.verbose:
            verbose_run(args.filter, args.notebooks, args.reduced)
            sys.exit()
        else:
            run(args.filter, args.notebooks, args.reduced)
