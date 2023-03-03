from datetime import datetime
import ROOT
import json
import os
import sys
import argparse



leadingpt = [60, 70, 80, 90, 100, 110, 120, 130]
trailingpt = [30, 35, 40, 50, 60, 70]
deta = [2., 2.5, 3., 3.5, 4.0, 4.5, 5]
mjj = [400., 500., 550., 600., 650., 700.]
dphi = [0.8, 1.6, 2.4, 3.2]

valid_dataformats = ['NANO', 'CustomNtuple']
valid_studies = ['L1', 'GEN']

#In case you want to load an helper for C++ functions
ROOT.gInterpreter.Declare('#include "../helpers/Helper.h"')
ROOT.gInterpreter.Declare('#include "../helpers/Helper_InvariantMass.h"')
#Importing stuff from other python files
sys.path.insert(0, '../helpers')
from bins import * 

def main():
    ###Arguments 
    parser = argparse.ArgumentParser(
        description='''
        H invisible studies (L1 and gen info)
        GEN: Make simple event kinematics distribution (MET, mjj, dphijj,...)
        L1: Create various L1 seeds targeting the VBF signature.
        ''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--max_events", dest="max_events", help="Maximum number of events to analyze. Default=-1 i.e. run on all events.", type=int, default=-1)
    parser.add_argument("-i", "--input", dest="inputfile", help="Input file", type=str, default='')
    parser.add_argument("-o", "--output", dest="outputfile", help="Output file", type=str, default='output.root')
    parser.add_argument("-s", "--study", dest="study", help="Type of study (L1 or GEN)", type=str, default='L1')
    parser.add_argument("-f", "--format", dest="dataformat", help="Input format (NANO or CustomNtuple)", type=str, default='CustomNtuple')
    args = parser.parse_args() 

    if args.dataformat not in valid_dataformats:
        raise Exception('Invalid dataformat')
    if args.study not in valid_studies:
        raise Exception('Invalid study')
    if args.study == 'GEN' and args.dataformat != 'NANO' :
        raise Exception('GEN study only possible with NANO format')
    if args.study == 'L1' and args.dataformat != 'CustomNtuple' :
        raise Exception('L1 study only possible with CustomNtuple format')


    inputfile = args.inputfile
    if args.inputfile == '':
        if args.dataformat == 'NANO':
            inputfile = 'root://cmsxrootd-site.fnal.gov/store/mc/RunIISummer20UL18NanoAODv9/VBF_HToInvisible_M125_TuneCP5_withDipoleRecoil_13TeV_powheg_pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/230000/554B4E70-304E-3046-8C52-9513BE24AFDC.root'
            #If working on T2_BE_IIHE, the following is faster
            #inputfile = '/pnfs/iihe/cms/ph/sc4/store/mc/RunIISummer20UL18NanoAODv9/VBF_HToInvisible_M125_TuneCP5_withDipoleRecoil_13TeV_powheg_pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/230000/554B4E70-304E-3046-8C52-9513BE24AFDC.root'
        else: 
            inputfile = '/user/lathomas/PortingCodeToGitIIHECMS/CMSSW_12_4_8/src/GenericTreeProducerMINIAOD/Ntuplizer/python/outputvbfhinv.root'
            #raise Exception('No input file specified')
            #or uncomment the following line if working on T2_BE_IIHE
            

    ###Define the RDataFrame from the input tree
    df = None 
    if args.dataformat == 'NANO':
        df = ROOT.RDataFrame('Events', inputfile)

    else:
        df = ROOT.RDataFrame('ntuplizer/tree', inputfile)
    nEvents = df.Count().GetValue()
    print('There are {} events'.format(nEvents))
    
    #Max events to run on 
    max_events = min(nEvents, args.max_events) if args.max_events >=0 else nEvents
    df = df.Range(0, max_events)
    #Next line to monitor event loop progress
    df = df.Filter('if(tdfentry_ %100000 == 0) {cout << "Event is  " << tdfentry_ << endl;} return true;')
    

    out = ROOT.TFile(args.outputfile, "recreate")

    ####The sequence of filters/column definition starts here

    if args.dataformat == 'NANO': 
        df = df.Define("dijetvariables","(HighestMjj(GenJet_pt, GenJet_eta, GenJet_phi))")
        df = df.Define("mjj","dijetvariables[0]")
        df = df.Define("leading_pt","dijetvariables[1]")
        df = df.Define("subleading_pt","dijetvariables[2]")
        df = df.Define("deta","dijetvariables[3]")
        df = df.Define("dphi","dijetvariables[4]")
        
    elif args.dataformat == 'CustomNtuple':
        df = df.Define("dijetvariables","HighestMjj_L1(_L1jet_pt, _L1jet_eta, _L1jet_phi, _L1jet_bx)")
        df = df.Define("mjj","dijetvariables[0]")
        df = df.Define("leading_pt","dijetvariables[1]")
        df = df.Define("subleading_pt","dijetvariables[2]")
        df = df.Define("deta","dijetvariables[3]")
        df = df.Define("dphi","dijetvariables[4]")
        

        for h in dphi: 
            for i in leadingpt:
                for j in trailingpt:
                    if j > i:
                        continue
                    for k in deta:
                        df = df.Define("passL1_DoubleJetPt{}_{}_dEta{}_dPhi{}".format(i,j,k,h).replace(".","p"),"L1SeedDoubleJetEtaMin(_L1jet_pt, _L1jet_eta, _L1jet_phi, _L1jet_bx, {}, {}, {}, {})".format(i, j, k, h))
                    for k in mjj:
                        df = df.Define("passL1_DoubleJetPt{}_{}_Mjj{}_dPhi{}".format(i,j,k,h).replace(".","p"),"L1SeedDoubleJetMassMin(_L1jet_pt, _L1jet_eta, _L1jet_phi, _L1jet_bx, {}, {}, {}, {})".format(i, j, k, h))

    histos = {}
    if args.study == 'GEN':
        histos['met'] = df.Histo1D(ROOT.RDF.TH1DModel('hmet', '', 5000, 0, 5000), 'GenMET_pt')
        histos['subleadingpt_met100_leadpt120_mjj800'] = df.Filter('GenMET_pt>100').Filter('leading_pt>120').Filter('mjj>800').Histo1D(ROOT.RDF.TH1DModel('hsubleadingpt_met100', '', 1000, 0, 1000), 'subleading_pt')
    #df = df.Filter('passL1_DoubleJetPt100_30_Mjj500p0')
    histos['mjj'] = df.Histo1D(ROOT.RDF.TH1DModel('hmjj', '', 5000, 0, 5000), 'mjj')
    histos['leadingpt'] = df.Histo1D(ROOT.RDF.TH1DModel('hleadingpt', '', 1000, 0, 1000), 'leading_pt')
    histos['deta'] = df.Histo1D(ROOT.RDF.TH1DModel('hdeta', '', 1000, 0, 10), 'deta')
    histos['dphi'] = df.Histo1D(ROOT.RDF.TH1DModel('hdphi', '', 100, 0, 3.1416), 'dphi')
    histos['subleadingpt'] = df.Histo1D(ROOT.RDF.TH1DModel('hsubleadingpt', '', 1000, 0, 1000), 'subleading_pt')

    #The following creates a set of VBF dijet seeds requiring two jets with some minimum pt and optionally minimum invariant mass/minimum deta/max dphi conditions.
    if args.study == 'L1':
        for h in dphi:
            for i in leadingpt:
                for j in trailingpt:
                    print(i, j)
                    print('i> j', i > j)
                    if j > i :
                        continue
                    print('passing i, j', i, j)
                    for k in deta:
                        print('k', k)
                        print('passL1_DoubleJetPt{}_{}_dEta{}_dPhi{}'.format(i,j,k,h).replace(".","p"))
                        histos['passL1_DoubleJetPt{}_{}_dEta{}_dPhi{}'.format(i,j,k,h).replace(".","p")] = df.Histo1D(ROOT.RDF.TH1DModel('passL1_DoubleJetPt{}_{}_dEta{}_dPhi{}'.format(i,j,k,h).replace(".","p"), '', 2, 0, 2), 'passL1_DoubleJetPt{}_{}_dEta{}_dPhi{}'.format(i,j,k,h).replace(".","p"))
                    for k in mjj:
                        histos['passL1_DoubleJetPt{}_{}_Mkk{}_dPhi{}'.format(i,j,k,h).replace(".","p")] = df.Histo1D(ROOT.RDF.TH1DModel('passL1_DoubleJetPt{}_{}_Mjj{}_dPhi{}'.format(i,j,k,h).replace(".","p"), '', 2, 0, 2), 'passL1_DoubleJetPt{}_{}_Mjj{}_dPhi{}'.format(i,j,k,h).replace(".","p"))
    
    for i in histos:
        histos[i].Write()
    

if __name__ == '__main__':
    main()
