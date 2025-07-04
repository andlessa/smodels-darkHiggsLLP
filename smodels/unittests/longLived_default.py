smodelsOutputDefault = {
'OutputStatus' : {
    'sigmacut' : 0.03,
    'minmassgap' : 5.0,
    'minmassgapisr' : 5.0,
    'maxcond' : 0.2,
    'ncpus' : -6,
    'model' : 'share.models.mssm',
    'checkinput' : True,
    'doinvisible' : True,
    'docompress' : True,
    'computestatistics' : False,
    'testcoverage' : True,
    'combineanas' : 'CMS-SUS-13-012,ATLAS-SUSY-2018-31,ATLAS-CONF-2013-037',
    'file status' : 1,
    'decomposition status' : 1,
    'warnings' : 'Input file ok',
    'input file' : './testFiles/slha/longLived.slha',
    'database version' : 'unittest211',
    'smodels version' : '2.2.0'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.1335974,
        'upper limit (fb)' : 0.16,
        'expected upper limit (fb)' : 0.16,
        'TxNames' : ['THSCPM1', 'THSCPM2'],
        'Mass (GeV)' : None,
        'AnalysisID' : 'CMS-EXO-13-006',
        'DataSetID' : 'c200track',
        'AnalysisSqrts (TeV)' : 8.0,
        'lumi (fb-1)' : 18.8,
        'dataType' : 'efficiencyMap',
        'r' : 0.8349838,
        'r_expected' : 0.8349838,
        'Width (GeV)' : None,
        'nll' : 1.783294994187348,
        'nll_min' : -0.728336219734454,
        'nll_SM' : -0.728336
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.003205744,
        'upper limit (fb)' : 0.4,
        'expected upper limit (fb)' : 0.35,
        'TxNames' : ['T2tt'],
        'Mass (GeV)' : [[1061.5, 351.7], [1061.5, 351.7]],
        'AnalysisID' : 'ATLAS-CONF-2013-037',
        'DataSetID' : 'SRtN3',
        'AnalysisSqrts (TeV)' : 8.0,
        'lumi (fb-1)' : 20.7,
        'dataType' : 'efficiencyMap',
        'r' : 0.008014361,
        'r_expected' : 0.00915927,
        'Width (GeV)' : [[2.37186555, 'stable'], [2.37186555, 'stable']],
        'nll' : 3.6989164567229924,
        'nll_min' : 3.5158761779589756,
        'nll_SM' : 3.712189842416584
    }
],
'Total xsec for missing topologies (fb)' : 0.6027619,
'missing topologies' : [
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.3356614,
        'element' : '[[[l]],[[l]]]  (MET,MET)'
    },
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.2016084,
        'element' : '[[],[[l]]]  (MET,MET)'
    },
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.03292622,
        'element' : '[[],[[jet]]]  (MET,MET)'
    },
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.03256586,
        'element' : '[[],[]]  (MET,MET)'
    }
],
'Total xsec for missing topologies with displaced decays (fb)' : 0.0,
'missing topologies with displaced decays' : [],
'Total xsec for missing topologies with prompt decays (fb)' : 0.6027619,
'missing topologies with prompt decays' : [
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.3356614,
        'element' : '[[[l]],[[l]]]  (MET,MET)'
    },
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.2016084,
        'element' : '[[],[[l]]]  (MET,MET)'
    },
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.03292622,
        'element' : '[[],[[jet]]]  (MET,MET)'
    },
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.03256586,
        'element' : '[[],[]]  (MET,MET)'
    }
],
'Total xsec for topologies outside the grid (fb)' : 0.3697722,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 8.0,
        'weight (fb)' : 0.3697722,
        'element' : '[[[jet]],[[jet]]]  (MET,MET)'
    }
],
'CombinedRes' : [
    {
        'AnalysisID' : 'ATLAS-CONF-2013-037',
        'r' : 0.008014361,
        'r_expected' : 0.00915927,
        'nll' : 3.6989164567229924,
        'nll_min' : 3.5158761779589756,
        'nll_SM' : 3.712189842416584
    }
]
}

