import ROOT
from array import array
from math import floor, ceil

from bins import *

'''

jetEtaBins = [0., 1.3, 2.5, 3., 3.5, 4., 5.]
egEtaBins = [0., 1.479, 2.5]
muEtaBins = [0., 0.83, 1.24, 2.4]


ht_bins = array('f', [ i*10 for i in range(50) ] + [ 500+ i*20 for i in range(25) ] + [1000 + i*50 for i in range(10)] +[1500,1600,1700,1800,2000,2500,3000])
leptonpt_bins = array('f',[ i for i in range(50) ] + [ 50+2*i for i in range(10) ] + [ 70+3*i for i in range(10) ] + [100+10*i for i in range(10) ] + [200, 250, 300, 400, 500])
jetmetpt_bins = array('f',[ i*5 for i in range(50) ] +  [250+10*i for i in range(25) ]  + [500+20*i for i in range(10) ] + [700, 800, 900, 1000, 1200, 1500, 2000 ])
'''

#from runsBinning import *
#runnb_bins = array('f', runbinning())


response_bins = array('f',[0.+float(i)/100. for i in range(200)] )

runnb_bins = None

def set_runnb_bins(df):
    global runnb_bins
    if runnb_bins is None:
        # +1: to get [run, run+1] bin, +0.5 and floor to prevent float rounding errors + high bound
        # in range is excluded, so feed run, and run+2 to get [run, run+1]
        runNb_max = ceil(df.Max("run").GetValue() + 1.5)
        runNb_min = floor(df.Min("run").GetValue())
        runnb_bins = array('f', [r for r in range(runNb_min, runNb_max)])
    else:
        print("runnb_bins are already set")

#String printing stuff for a few events
stringToPrint = '''
if(EventsToPrint <100) {

cout << "*********New Event********"<<endl;
cout << "run " << run<<endl;

for(unsigned int i = 0;i< (_lPt).size();i++ ){
cout << "Lepton Pt, Eta, Phi: " << (_lPt)[i]<<", "<<(_lEta)[i]<<", "<<(_lPhi)[i]<<endl;
cout << "Lepton pdgId: " << (_lpdgId)[i]<<endl;
}
for(unsigned int i = 0;i< (Photon_pt).size();i++ ){
cout << "Photon Pt, Eta, Phi: " << (Photon_pt)[i]<<", "<<(Photon_eta)[i]<<", "<<(Photon_phi)[i]<<endl;
}
for(unsigned int i = 0;i< (Jet_pt).size();i++ ){
cout << "jet Pt, Eta, Phi: " << (Jet_pt)[i]<<", "<<(Jet_eta)[i]<<", "<<(Jet_phi)[i]<<endl;
cout << "jet PassID, MUEF, CEEF, CHEF: " << (_jetPassID)[i]<<", "<<(Jet_muEF)[i]<<", "<<(Jet_chEmEF)[i]<<", "<<  (Jet_chHEF)[i]<<endl;
}

for(unsigned int i = 0;i< (L1EG_pt).size();i++ ){
cout << "L1 EG Pt, Eta, Phi: " << (L1EG_pt)[i]<<", "<<(L1EG_eta)[i]<<", "<<(L1EG_phi)[i]<<endl;
}

cout << "probe_L1PtoverRecoPt probe_Pt sizes: "<<probe_L1PtoverRecoPt.size()<<", " <<probe_Pt.size()<<endl;
for(unsigned int i = 0;i< probe_Pt.size();i++ ){
cout << "probe_Pt, probe_L1PtoverRecoPt: "<<probe_L1PtoverRecoPt[i]<<", "<<probe_Pt[i]<<endl;
}

cout << "response, denominator_pt sizes: " << response.size()<<", " <<denominator_pt.size()<<endl;
for(unsigned int i = 0;i<response.size() ;i++ ){
cout <<"response, denominator_pt "<<response[i]<<", "<<denominator_pt[i]<<endl; 
} 
cout <<endl;

EventsToPrint++;
} 
return true;
'''


stringToPrintJets = '''
for(unsigned int i = 0;i< (cleanJet_MUEF).size();i++ ){ 
if((cleanJet_MUEF)[i]>0.5){
cout << "jet Pt, Eta, Phi: " << (cleanJet_Pt)[i]<<", "<<(cleanJet_Eta)[i]<<", "<<(cleanJet_Phi)[i]<<", " << (cleanJet_MUEF)[i]<<endl;

}
}
return true;
'''

stringFailingJets = '''

bool findbadjet = false;
for(unsigned int i = 0;i< (cleanJet_MUEF).size();i++ ){
if((cleanJet_Pt)[i]>300&&abs((cleanJet_Eta)[i])<2.5&&cleanJet_L1Pt[i]<50){
cout << "runNb: "<< run<<endl;
cout << "jet Pt, Eta, Phi: " << (cleanJet_Pt)[i]<<", "<<(cleanJet_Eta)[i]<<", "<<(cleanJet_Phi)[i]<< endl; 
cout << "jet NHEF, CHEF, NEEF, CEEF, MUEF: "<<(cleanJet_NHEF)[i]<< ", " << (cleanJet_CHEF)[i]<< ", " << (cleanJet_NEEF)[i]<< ", "<< (cleanJet_CEEF)[i]<< ", " << (cleanJet_MUEF)[i]<<endl;

findbadjet = true;
}
}
if(findbadjet){
for(unsigned int i = 0;i< (L1Jet_pt).size();i++ ){
cout << "L1 JET Pt, Eta, Phi, Bx: " << (L1Jet_pt)[i]<<", "<<(L1Jet_eta)[i]<<", "<<(L1Jet_phi)[i]<< ", "<<(L1Jet_bx)[i]<<endl;
}
}

return true;
'''

stringToPrintHF = '''
if(EventsToPrint <100) {

cout << "*********New Event********"<<endl;
cout << "run " << run<<endl;
cout << "met, met_phi " << MET_pt <<", "<<MET_phi<<endl;
for(unsigned int i = 0;i< (_lPt).size();i++ ){
cout << "Lepton Pt, Eta, Phi: " << (_lPt)[i]<<", "<<(_lEta)[i]<<", "<<(_lPhi)[i]<<endl;
cout << "Lepton pdgId: " << (_lpdgId)[i]<<endl;
}
for(unsigned int i = 0;i< (Photon_pt).size();i++ ){
cout << "Photon Pt, Eta, Phi: " << (Photon_pt)[i]<<", "<<(Photon_eta)[i]<<", "<<(Photon_phi)[i]<<endl;
}
for(unsigned int i = 0;i< (Jet_pt).size();i++ ){
cout << "jet Pt, Eta, Phi: " << (Jet_pt)[i]<<", "<<(Jet_eta)[i]<<", "<<(Jet_phi)[i]<<endl;
cout << "jet PassID, MUEF, CEEF, CHEF, NHEF: " << (_jetPassID)[i]<<", "<<(Jet_muEF)[i]<<", "<<(Jet_chEmEF)[i]<<", "<<  (Jet_chHEF)[i]<<", "<<  (Jet_neHEF)[i]<<endl;
cout << "jethfsigmaEtaEta jethfsigmaPhiPhi jethfcentralEtaStripSize "<< (Jet_hfsigmaEtaEta)[i]<<", "<<  (Jet_hfsigmaPhiPhi)[i]<<", "<<(Jet_hfcentralEtaStripSize)[i]<<endl;
}


for(unsigned int i = 0;i< (L1Jet_pt).size();i++ ){
cout << "L1 JET Pt, Eta, Phi, Bx: " << (L1Jet_pt)[i]<<", "<<(L1Jet_eta)[i]<<", "<<(L1Jet_phi)[i]<<", " << (L1Jet_bx)[i]<<endl;
}



cout <<endl;

EventsToPrint++;
} 
return true;
'''

highEnergyJet = '''
for( unsigned int i = 0; i < (Jet_pt).size(); i++){
    if(Jet_pt[i] * cosh(Jet_eta[i]) > 6000){
        return false;
    }
}
return true;
'''

def SinglePhotonSelection(df):
    '''
    Select events with exactly one photon with pT>20 GeV.
    The event must pass a photon trigger. 
    '''
#    df = df.Filter('MET_pt<50')
#    nEvents = df.Count().GetValue()
#    print("Before HLT_Photon110EB_TightID_TightIso", nEvents)

    df = df.Filter('HLT_Photon110EB_TightID_TightIso')

#    nEvents = df.Count().GetValue()
#    print("After HLT_Photon110EB_TightID_TightIso", nEvents)

    df = df.Define('photonsptgt20','Photon_pt>20')
    df = df.Filter('Sum(photonsptgt20)==1','=1 photon with p_{T}>20 GeV')

#    nEvents = df.Count().GetValue()
#    print("After Sum(photonsptgt20)==1", nEvents)

    # TEMPORARY: bypasses
    #df = df.Define("_phPassTightID", "true")
    #df = df.Define("_phPassIso", "true")
    #df = df.Define('isRefPhoton','_phPassTightID&&_phPassIso&&Photon_pt>115&&abs(Photon_eta)<1.479')

    df = df.Define('isRefPhoton','Photon_mvaID_WP80&&Photon_pt>115&&abs(Photon_eta)<1.479')

    # debug:
#    nEvents = df.Filter('Sum(isRefPhoton)>=1','Photon has p_{T}>115 GeV, passes tight ID and is in EB').Count().GetValue()
#    print("After Sum(isRefPhoton)>=1", nEvents)

    df = df.Filter('Sum(isRefPhoton)==1','Photon has p_{T}>115 GeV, passes tight ID and is in EB')
    
#    nEvents = df.Count().GetValue()
#    print("After Sum(isRefPhoton)==1", nEvents)

    df = df.Define('cleanPh_Pt','Photon_pt[isRefPhoton]')
    df = df.Define('cleanPh_Eta','Photon_eta[isRefPhoton]')
    df = df.Define('cleanPh_Phi','Photon_phi[isRefPhoton]')
    
    df = df.Define('ref_Pt','cleanPh_Pt[0]')
    df = df.Define('ref_Phi','cleanPh_Phi[0]')
    
    return df
    
    
    
    
def MuonJet_MuonSelection(df):
    '''
    Select events with >= 1 muon with pT>25 GeV.
    The event must pass a single muon trigger. 
    '''
    df = df.Filter('HLT_IsoMu24')

    #df = df.Define('goodmuonPt25','_lPt>25&&abs(_lpdgId)==13&&_lPassTightID')
    #df = df.Filter('Sum(goodmuonPt25)>=1','>=1 muon with p_{T}>25 GeV')
    #df = df.Define('badmuonPt10','_lPt>10&&abs(_lpdgId)==13&&_lPassTightID==0')
    #df = df.Filter('Sum(badmuonPt10)==0','No bad quality muon')
    df = df.Define('Muon_PassTightId','Muon_pfIsoId>=3&&Muon_mediumPromptId') 
    df = df.Define('goodmuonPt25','Muon_pt>25&&abs(Muon_pdgId)==13&&Muon_PassTightId')
    df = df.Filter('Sum(goodmuonPt25)>=1','>=1 muon with p_{T}>25 GeV')
    df = df.Define('badmuonPt10','Muon_pt>10&&abs(Muon_pdgId)==13&&Muon_PassTightId==0')
    df = df.Filter('Sum(badmuonPt10)==0','No bad quality muon')

    # reject events containing a jet with energy > 6000 GeV
#    df = df.Filter(highEnergyJet, 'No high energy jet')
    return df
    
    

def ZEE_EleSelection(df):
    '''
    Select Z->ee events passing a single electron trigger. Defines probe pt/eta/phi
    '''
#    nEvents = df.Count().GetValue()
#    print("Before HLT_Ele32_WPTight_Gsf", nEvents)
    df = df.Filter('HLT_Ele32_WPTight_Gsf')

#    nEvents = df.Count().GetValue()
#    print("After HLT_Ele32_WPTight_Gsf", nEvents)

    # Trigged on a Electron (probably redondant)
    df = df.Filter('''
    bool trigged_on_e = false;
    for (unsigned int i = 0; i < TrigObj_id.size(); i++){
        if(TrigObj_id[i] == 11) trigged_on_e = true;
    }
    return trigged_on_e;
    ''')

#    nEvents = df.Count().GetValue()
#    print("After trig on photon", nEvents)

    # TrigObj matching
    df = df.Define('Electron_trig_idx', 'MatchObjToTrig(Electron_eta, Electron_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 11)')

#    debug:
#    df = df.Filter('''
#    int max_val = -1;
#    for (unsigned int i = 0; i < Electron_trig_idx.size(); i++){
#        max_val = max(max_val, Electron_trig_idx[i]);
#    }
#    if(max_val==-1){
#        return false;
#    }
#    else{
#        return true;
#    }
#    ''')
#    nEvents = df.Count().GetValue()
#    print("Electron trig matching:", nEvents)
#    exit()

#    # Debugging the matching
#    df = df.Filter('''
#    cout << "TrigObj" << endl;
#    for (unsigned int i = 0; i < TrigObj_pt.size(); i++){
#        cout << i << ", " << TrigObj_pt[i] << ", " << TrigObj_eta[i] << ", " << TrigObj_phi[i] << ", " << TrigObj_id[i] << endl;
#    }
#    cout << "Electron" << endl;
#    for (unsigned int i = 0; i < Electron_pt.size(); i++){
#        cout << i << ", " << Electron_pt[i] << ", " << Electron_eta[i] << ", " << Electron_phi[i] << ", " << Electron_trig_idx[i] << endl;
#    }
#    return true;
#    ''')

#    nEvents = df.Count().GetValue()
#    print("After Sum(isTag) >0", nEvents)
#    exit()


    #df = df.Define('Electron_PassTightId','true') # BYPASS
    df = df.Define('Electron_passHLT_Ele32_WPTight_Gsf', 'trig_is_filterbit1_set(Electron_trig_idx, TrigObj_filterBits)')

    df = df.Define('isTag','_lPt>35&&abs(_lpdgId)==11&&Electron_mvaIso_WP90&&Electron_passHLT_Ele32_WPTight_Gsf==true')
    df = df.Filter('Sum(isTag)>0')

#    nEvents = df.Count().GetValue()
#    print("After Sum(isTag) >0", nEvents)

    df = df.Define('isProbe','_lPt>5&&abs(_lpdgId)==11&&Electron_mvaIso_WP90&&(Sum(isTag)>=2|| isTag==0)')

    df = df.Define('_mll', 'mll(Electron_pt, Electron_eta, Electron_phi, isTag, isProbe)')
    df = df.Filter('_mll>80&&_mll<100')

#    nEvents = df.Count().GetValue()
#    print("After 80 < _mll < 100", nEvents)

    df = df.Define('probe_Pt','_lPt[isProbe]')
    df = df.Define('probe_Eta','_lEta[isProbe]')
    df = df.Define('probe_Phi','_lPhi[isProbe]')

    #df = df.Define('probe_Charge', '_l
    
    return df


def ZMuMu_MuSelection(df):
    '''
    Selects Z->mumu events passing a single muon trigger. Defines probe pt/eta/phi
    '''
    df = df.Filter('HLT_IsoMu24')

    # Trigged on a Muon (probably redondant)
    df = df.Filter('''
    bool trigged_on_mu = false;
    for (unsigned int i = 0; i < TrigObj_id.size(); i++){
        if(TrigObj_id[i] == 13) trigged_on_mu = true;
    }
    return trigged_on_mu;
    ''')

    # charge 
    #df = df.Filter("L1Mu_hwCharge>-1")
    # from debugging, I found that
    # L1Mu_hwCharge = 0 corresponds to Muon_charge = +1
    # L1Mu_hwCharge = 1 corresponds to Muon_charge = -1
    df = df.Define('L1Mu_charge', 'charge_conversion(L1Mu_hwCharge)')
    #df.Display({"L1Mu_hwCharge", "L1Mu_charge"})


    # Match L1Mu to trig obj with id == 13 -> L1Mu_trig_idx
    # with L1Mu_trig_idx -> check filter bits -> L1Mu_passHLT

    # TrigObj matching
    df = df.Define('Muon_trig_idx', 'MatchObjToTrig(Muon_eta, Muon_phi, TrigObj_pt, TrigObj_eta, TrigObj_phi, TrigObj_id, 13)')

    # Debugging the matching, seems to be ok
#    df = df.Filter('''
#    cout << "TrigObj" << endl;
#    for (unsigned int i = 0; i < TrigObj_pt.size(); i++){
#        cout << i << ", " << TrigObj_pt[i] << ", " << TrigObj_eta[i] << ", " << TrigObj_phi[i] << ", " << TrigObj_id[i] << endl;
#    }
#    cout << "Muon" << endl;
#    for (unsigned int i = 0; i < Muon_pt.size(); i++){
#        cout << i << ", " << Muon_pt[i] << ", " << Muon_eta[i] << ", " << Muon_phi[i] << ", " << Muon_trig_idx[i] << endl;
#    }
#    return true;
#    ''')

    df = df.Define('Muon_passHLT_IsoMu24', 'trig_is_filterbit1_set(Muon_trig_idx, TrigObj_filterBits)')

    # Debugging the HLT firing, seems to be ok
#    df = df.Filter('''
#    cout << "pass HLT?" << endl;
#    for ( unsigned int i = 0; i < Muon_passHLT_IsoMu24.size(); i++) {
#        cout << i << ", " << Muon_passHLT_IsoMu24[i] << endl;
#    }
#    return true;
#    ''')

#    df = df.Filter('''
#    //cout << "new event" << endl;
#    //cout << Muon_pt.size() << ", " << Muon_passHLT_IsoMu24.size() << endl;
#    cout << (Muon_pt.size() == Muon_passHLT_IsoMu24.size()) << endl;
#    return true;
#    ''')

#    nEvents = df.Count().GetValue()
#    print(nEvents)
#    exit()

    df = df.Define('Muon_PassTightId','Muon_pfIsoId>=3&&Muon_mediumPromptId') 

    # some debugging the types of colums
    #cols = ["Muon_pt", "Muon_pdgId", "Muon_PassTightId", "Muon_passHLT_IsoMu24", "Muon_tightId"]
    #for c in cols:
    #    coltype = df.GetColumnType(c)
    #    print(c, coltype)
    #df.Describe().Print()
    #exit()

    df = df.Define('isTag','Muon_pt>25&&abs(Muon_pdgId)==13&&Muon_PassTightId&&Muon_passHLT_IsoMu24==true')
    df = df.Filter('Sum(isTag)>0')

    #nEvents = df.Count().GetValue()
    #print("There are {} events after Sum(isTag)>0".format(nEvents))

    df = df.Define('isProbe','Muon_pt>3&&abs(Muon_pdgId)==13&&Muon_PassTightId&& (Sum(isTag)>=2|| isTag==0)')
    df = df.Define('_mll', 'mll(Muon_pt, Muon_eta, Muon_phi, isTag, isProbe)')

    #df.Display("_mll").Print()
    #df.Filter("_mll>0").Display("_mll").Print()

    df = df.Filter('_mll>80&&_mll<100')


    #nEvents = df.Filter('_mll>0').Count().GetValue()
    #print("There are {} events after _mll>0".format(nEvents))
    #nEvents = df.Count().GetValue()
    #print("There are {} events after _mll>80&&_mll<100".format(nEvents))

    df = df.Define('probe_Pt','Muon_pt[isProbe]')
    df = df.Define('probe_Eta','Muon_eta[isProbe]')
    df = df.Define('probe_Phi','Muon_phi[isProbe]')
    
    # debug
    #df = df.Define('probe_Charge', 'Muon_charge[isProbe]')
    
    return df

def makehistosforturnons_inprobeetaranges(df, histos, etavarname, phivarname, ptvarname, responsevarname, etabins, l1varname, l1thresholds, prefix, binning, l1thresholdforeffvsrunnb, offlinethresholdforeffvsrunnb, suffix = ''):
    '''Make histos for turnons vs pt (1D histos for numerator and denominator) in ranges of eta
    Also look at response vs run number (2D histo) '''
    for i in range(len(etabins)-1):

        # check that runnb_bins are set
        if runnb_bins is None:
            set_runnbbins(df)

        str_bineta = "eta{}to{}".format(etabins[i],etabins[i+1]).replace(".","p")
        #Define columns corresponding to pt and response for the selected eta range 
        df_etarange = df.Define('inEtaRange','abs({})>={}'.format(etavarname, etabins[i])+'&&abs({})<{}'.format(etavarname, etabins[i+1]))
        df_etarange = df_etarange.Filter('MET_pt<100')
        df_etarange = df_etarange.Define('denominator_pt',ptvarname+'[inEtaRange]')
        df_etarange = df_etarange.Define('response',responsevarname+'[inEtaRange]')
        df_etarange = df_etarange.Define('runnb',"return ROOT::VecOps::RVec<int>(response.size(), run);")

        #Response vs pt and vs runnb (2d)
        histos[prefix+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_{}_{}'.format(prefix, str_bineta)+suffix, '', len(binning)-1, binning), 'denominator_pt')
        histos[prefix+str_bineta+'_ResponseVsPt'+suffix] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsPt_{}_{}'.format(prefix, str_bineta)+suffix, '', 200, 0, 200, 100, 0, 2), 'denominator_pt', 'response')
        histos[prefix+str_bineta+'_ResponseVsPt_big_bins'+suffix] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsPt_big_bins_{}_{}'.format(prefix, str_bineta)+suffix, '', 20, 0, 200, 100, 0, 2), 'denominator_pt', 'response')
        histos[prefix+str_bineta+'_ResponseVsRunNb'+suffix] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsRunNb_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'runnb', 'response')

        #if i ==1 and prefix == 'EGNonIso_plots':
        #    df_etarange = df_etarange.Filter(stringToPrint)

            
        #Numerator/denominator for plateau eff vs runnb
        df_etarange = df_etarange.Define('inplateau','{}>={}&&inEtaRange'.format(ptvarname,offlinethresholdforeffvsrunnb))
        df_etarange = df_etarange.Define('N_inplateau','Sum(inplateau)')
        df_etarange = df_etarange.Define('runnb_inplateau',"return ROOT::VecOps::RVec<int>(N_inplateau, run);")
        df_etarange = df_etarange.Define('inplateaupassL1','inplateau && {}>={}'.format(l1varname,l1thresholdforeffvsrunnb))
        df_etarange = df_etarange.Define('N_inplateaupassL1','Sum(inplateaupassL1)')
        df_etarange = df_etarange.Define('runnb_inplateaupassL1',"return ROOT::VecOps::RVec<int>(N_inplateaupassL1, run);")
        histos[prefix+"_plateaueffvsrunnb_numerator_"+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_PlateauEffVsRunNb_Numerator_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins),'runnb_inplateaupassL1')
        histos[prefix+"_plateaueffvsrunnb_denominator_"+str_bineta+suffix] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_PlateauEffVsRunNb_Denominator_{}_{}'.format(prefix, str_bineta)+suffix, '', len(runnb_bins)-1, runnb_bins),'runnb_inplateau')

        for ipt in l1thresholds:
            str_binetapt = "eta{}to{}_l1thrgeq{}".format(etabins[i], etabins[i+1],ipt).replace(".","p")
            df_loc = df_etarange.Define('passL1Cond','{}>={}'.format(l1varname, ipt))
            df_loc = df_loc.Define('numerator_pt',ptvarname+'[inEtaRange&&passL1Cond]')
            histos[prefix+str_binetapt+suffix] = df_loc.Histo1D(ROOT.RDF.TH1DModel('h_{}_{}'.format(prefix, str_binetapt)+suffix, '', len(binning)-1, binning), 'numerator_pt')


    return df

    

def ZEE_Plots(df, suffix = ''):
    histos = {}
    
    label = ['EGNonIso','EGLooseIso', 'EGTightIso']
    df_eg = [None, None, None]
    for i in range(3): 
        
        if i ==0:
            df_eg[i] = df.Define('probe_idxL1jet','FindL1ObjIdx(L1EG_eta, L1EG_phi, probe_Eta, probe_Phi)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bx0','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, 0)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxmin1','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, -1)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxplus1','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, 1)')
        if i ==1:
            df_eg[i] = df.Define('probe_idxL1jet','FindL1ObjIdx(L1EG_eta, L1EG_phi, probe_Eta, probe_Phi, L1EG_hwIso, 2)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bx0','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, 0, L1EG_hwIso, 2)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxmin1','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, -1, L1EG_hwIso, 2)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxplus1','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, 1, L1EG_hwIso, 2)')
        if i ==2:
            df_eg[i] = df.Define('probe_idxL1jet','FindL1ObjIdx(L1EG_eta, L1EG_phi, probe_Eta, probe_Phi, L1EG_hwIso, 3)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bx0','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, 0, L1EG_hwIso, 3)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxmin1','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, -1, L1EG_hwIso, 3)')
            df_eg[i] = df_eg[i].Define('probe_idxL1jet_Bxplus1','FindL1ObjIdx_setBx(L1EG_eta, L1EG_phi, L1EG_bx, probe_Eta, probe_Phi, 1, L1EG_hwIso, 3)')

        df_eg[i] = df_eg[i].Define('probe_L1Pt','GetVal(probe_idxL1jet, L1EG_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Bx','GetVal(probe_idxL1jet, L1EG_bx)')
        df_eg[i] = df_eg[i].Define('probe_L1PtoverRecoPt','probe_L1Pt/probe_Pt')

        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bx0', 'GetVal(probe_idxL1jet_Bx0, L1EG_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bxmin1', 'GetVal(probe_idxL1jet_Bxmin1, L1EG_pt)')
        df_eg[i] = df_eg[i].Define('probe_L1Pt_Bxplus1', 'GetVal(probe_idxL1jet_Bxplus1, L1EG_pt)')

        pt_binning = leptonpt_bins
        if suffix != '':
            pt_binning = coarse_leptonpt_bins
        
        df_eg[i] = makehistosforturnons_inprobeetaranges(df_eg[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=egEtaBins, l1varname='probe_L1Pt', l1thresholds=[5,10,15,20,25,30,36,37], prefix=label[i]+"_plots", binning=pt_binning, l1thresholdforeffvsrunnb = 30, offlinethresholdforeffvsrunnb = 35, suffix = suffix)
        
        
        df_eg[i] = df_eg[i].Define('probePt30_Eta','probe_Eta[probe_Pt>30]')
        df_eg[i] = df_eg[i].Define('probePt30_Phi','probe_Phi[probe_Pt>30]')
        df_eg[i] = df_eg[i].Define('probePt30PassL1EG25_Eta','probe_Eta[probe_Pt>30&&probe_L1Pt>25]')
        df_eg[i] = df_eg[i].Define('probePt30PassL1EG25_Phi','probe_Phi[probe_Pt>30&&probe_L1Pt>25]')
        histos['h_EG25_EtaPhi_Numerator'+label[i]+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('h_EG25_EtaPhi_Numerator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1EG25_Eta', 'probePt30PassL1EG25_Phi')
        histos['h_EG25_EtaPhi_Denominator'+label[i]+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('h_EG25_EtaPhi_Denominator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30_Eta', 'probePt30_Phi')

        
        if i ==0:
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxmin1_Eta', 'probe_Eta[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bxmin1>15&&probe_L1Pt_Bxmin1<=26&&probe_L1Bx==-1]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxmin1_Phi', 'probe_Phi[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bxmin1>15&&probe_L1Pt_Bxmin1<=26&&probe_L1Bx==-1]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bx0_Eta', 'probe_Eta[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bx0>15&&probe_L1Pt_Bx0<=26&&probe_L1Bx==0]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bx0_Phi', 'probe_Phi[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bx0>15&&probe_L1Pt_Bx0<=26&&probe_L1Bx==0]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxplus1_Eta', 'probe_Eta[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bxplus1>15&&probe_L1Pt_Bxplus1<=26&&probe_L1Bx==1]')
            df_eg[i] = df_eg[i].Define('probeL1EG15to26Bxplus1_Phi', 'probe_Phi[probe_Pt>12&&probe_Pt<23&&probe_L1Pt_Bxplus1>15&&probe_L1Pt_Bxplus1<=26&&probe_L1Bx==1]')
            
            
            histos['L1EG15to26_bxmin1_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bxmin1_Eta', 'probeL1EG15to26Bxmin1_Phi')
            histos['L1EG15to26_bx0_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bx0_Eta', 'probeL1EG15to26Bx0_Phi')
            histos['L1EG15to26_bxplus1_etaphi'+suffix] = df_eg[i].Histo2D(ROOT.RDF.TH2DModel('L1EG15to26_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1EG15to26Bxplus1_Eta', 'probeL1EG15to26Bxplus1_Phi')

            histos['L1EG15to26_bxmin1_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bxmin1_Eta')
            histos['L1EG15to26_bx0_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bx0_Eta')
            histos['L1EG15to26_bxplus1_eta'+suffix] = df_eg[i].Histo1D(ROOT.RDF.TH1DModel('L1EG15to26_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1EG15to26Bxplus1_Eta')

    return df, histos
    


def ZMuMu_Plots(df, suffix = ''):

    histos = {}
    label = ['AllQual', 'Qual8', 'Qual12']
    df_mu = [None, None, None]
    
    for i in range(3):
        if i == 0:
            df_mu[i] = df.Define('probe_idxL1jet','FindL1MuIdx(L1Mu_eta, L1Mu_phi, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bx0','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, 0)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxmin1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, -1)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxplus1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, 1)')
        if i == 1:
            df_mu[i] = df.Define('probe_idxL1jet','FindL1MuIdx(L1Mu_eta, L1Mu_phi, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, L1Mu_hwQual, 8)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bx0','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, 0, L1Mu_hwQual, 8)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxmin1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, -1, L1Mu_hwQual, 8)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxplus1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, 1, L1Mu_hwQual, 8)')
        if i == 2:
            df_mu[i] = df.Define('probe_idxL1jet','FindL1MuIdx(L1Mu_eta, L1Mu_phi, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, L1Mu_hwQual, 12)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bx0','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, 0, L1Mu_hwQual, 12)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxmin1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, -1, L1Mu_hwQual, 12)')
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_Bxplus1','FindL1MuIdx_setBx(L1Mu_eta, L1Mu_phi, L1Mu_bx, probe_Eta, probe_Phi, probe_Pt, L1Mu_charge, 1, L1Mu_hwQual, 12)')

            
        df_mu[i] = df_mu[i].Define('probe_L1Pt','GetVal(probe_idxL1jet, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Bx','GetVal(probe_idxL1jet, L1Mu_bx)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual','GetVal(probe_idxL1jet, L1Mu_hwQual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bx0', 'GetVal(probe_idxL1jet_Bx0, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bx0', 'GetVal(probe_idxL1jet_Bx0, L1Mu_hwQual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bxmin1', 'GetVal(probe_idxL1jet_Bxmin1, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bxmin1', 'GetVal(probe_idxL1jet_Bxmin1, L1Mu_hwQual)')

        df_mu[i] = df_mu[i].Define('probe_L1Pt_Bxplus1', 'GetVal(probe_idxL1jet_Bxplus1, L1Mu_pt)')
        df_mu[i] = df_mu[i].Define('probe_L1Qual_Bxplus1', 'GetVal(probe_idxL1jet_Bxplus1, L1Mu_hwQual)')

        df_mu[i] = df_mu[i].Define('probe_L1PtoverRecoPt','probe_L1Pt/probe_Pt')

        # debugging
        #print(label[i])
        #df_mu[i] = df_mu[i].Define('probe_L1charge', 'GetVal(probe_idxL1jet, L1Mu_charge)')
        #df_mu[i] = df_mu[i].Define('probe_L1eta', 'GetVal(probe_idxL1jet, L1Mu_eta)')
        #df_mu[i] = df_mu[i].Define('probe_L1phi', 'GetVal(probe_idxL1jet, L1Mu_phi)')
        #df_mu[i] = df_mu[i].Define('probe_L1charge_test', 'GetVal(probe_idxL1jet, L1Mu_charge)')
        #df_mu[i].Display({"probe_L1charge", "probe_L1charge_test", "probe_Charge"}).Print()
        #df_mu[i].Display({"probe_L1Pt", "probe_Pt", "probe_L1eta", "probe_Eta", "probe_L1phi", "probe_Phi"}).Print()
        
        pt_binning = leptonpt_bins
        if suffix != '':
            pt_binning = coarse_leptonpt_bins

        df_mu[i] = makehistosforturnons_inprobeetaranges(df_mu[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=muEtaBins, l1varname='probe_L1Pt', l1thresholds=[3, 5,10,15,20,22,26],  prefix=label[i]+"_plots" , binning = pt_binning, l1thresholdforeffvsrunnb = 22, offlinethresholdforeffvsrunnb = 27, suffix = suffix)
        df_mu[i] = makehistosforturnons_inprobeetaranges(df_mu[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=[0., 2.4], l1varname='probe_L1Pt', l1thresholds=[3, 5,10,15,20,22,26],  prefix=label[i]+"_plots_eta_inclusive" , binning = coarse_leptonpt_bins, l1thresholdforeffvsrunnb = 22, offlinethresholdforeffvsrunnb = 27, suffix = suffix)
        df_mu[i] = makehistosforturnons_inprobeetaranges(df_mu[i], histos, etavarname='probe_Eta', phivarname='probe_Phi', ptvarname='probe_Pt', responsevarname='probe_L1PtoverRecoPt', etabins=[0., 2.4], l1varname='probe_L1Pt', l1thresholds=[3, 5,10,15,20,22,26],  prefix=label[i]+"_plots_eta_inclusive2" , binning = coarse2_leptonpt_bins, l1thresholdforeffvsrunnb = 22, offlinethresholdforeffvsrunnb = 27, suffix = suffix)
        
        df_mu[i] = df_mu[i].Define('probePt30_Eta','probe_Eta[probe_Pt>30]')
        df_mu[i] = df_mu[i].Define('probePt30_Phi','probe_Phi[probe_Pt>30]')
        df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_Eta','probe_Eta[probe_Pt>30&&probe_L1Pt>22]')
        df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_Phi','probe_Phi[probe_Pt>30&&probe_L1Pt>22]')
        df_mu[i] = df_mu[i].Define('probePt30PassL1Mu22_L1Bx','probe_L1Bx[probe_Pt>30&&probe_L1Pt>22]')

        histos['h_Mu22_EtaPhi_Denominator'+label[i]+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('h_Mu22_EtaPhi_Denominator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30_Eta', 'probePt30_Phi')
        histos['h_Mu22_EtaPhi_Numerator'+label[i]+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('h_Mu22_EtaPhi_Numerator'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1Mu22_Eta', 'probePt30PassL1Mu22_Phi')
        
        
        if i == 2:
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxmin1_Eta','probe_Eta[probe_Pt>8&&probe_Pt<25&&probe_L1Pt>10&&probe_L1Pt<=21&&probe_L1Bx==-1&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxmin1_Phi','probe_Phi[probe_Pt>8&&probe_Pt<25&&probe_L1Pt>10&&probe_L1Pt<=21&&probe_L1Bx==-1&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bx0_Eta','probe_Eta[probe_Pt>8&&probe_Pt<25&&probe_L1Pt>10&&probe_L1Pt<=21&&probe_L1Bx==0&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bx0_Phi','probe_Phi[probe_Pt>8&&probe_Pt<25&&probe_L1Pt>10&&probe_L1Pt<=21&&probe_L1Bx==0&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxplus1_Eta','probe_Eta[probe_Pt>8&&probe_Pt<25&&probe_L1Pt>10&&probe_L1Pt<=21&&probe_L1Bx==1&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu10to21Bxplus1_Phi','probe_Phi[probe_Pt>8&&probe_Pt<25&&probe_L1Pt>10&&probe_L1Pt<=21&&probe_L1Bx==1&&probe_L1Qual>=12]')
            
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxmin1_Eta', 'probe_Eta[probe_Pt>20&&probe_L1Pt_Bxmin1>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxmin1_Phi', 'probe_Phi[probe_Pt>20&&probe_L1Pt_Bxmin1>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bx0_Eta', 'probe_Eta[probe_Pt>20&&probe_L1Pt_Bx0>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bx0_Phi', 'probe_Phi[probe_Pt>20&&probe_L1Pt_Bx0>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxplus1_Eta', 'probe_Eta[probe_Pt>20&&probe_L1Pt_Bxplus1>22&&probe_L1Qual>=12]')
            df_mu[i] = df_mu[i].Define('probeL1Mu22Bxplus1_Phi', 'probe_Phi[probe_Pt>20&&probe_L1Pt_Bxplus1>22&&probe_L1Qual>=12]')
                        
            histos['L1Mu10to21_bxmin1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bxmin1_Eta', 'probeL1Mu10to21Bxmin1_Phi')
            histos['L1Mu10to21_bx0_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bx0_Eta', 'probeL1Mu10to21Bx0_Phi')
            histos['L1Mu10to21_bxplus1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu10to21_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu10to21Bxplus1_Eta', 'probeL1Mu10to21Bxplus1_Phi')

            histos['L1Mu10to21_bxmin1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bxmin1_Eta')
            histos['L1Mu10to21_bx0_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bx0_Eta')
            histos['L1Mu10to21_bxplus1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu10to21_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu10to21Bxplus1_Eta')

            ###

            histos['L1Mu22_bxplus1_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu22_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxplus1_Eta', 'probeL1Mu22Bxplus1_Phi')
            histos['L1Mu22_bx0_etaphi'+suffix] = df_mu[i].Histo2D(ROOT.RDF.TH2DModel('L1Mu22_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')

            histos['L1Mu22_bxplus1_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxplus1_Eta')
            histos['L1Mu22_bx0_eta'+suffix] = df_mu[i].Histo1D(ROOT.RDF.TH1DModel('L1Mu22_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            #

            histos['L1Mu22_IsUnprefireable_bx0_etaphi'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_IsUnprefireable_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')
            histos['L1Mu22_IsUnprefireable_bx0_eta'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_IsUnprefireable_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            histos['L1Mu22_IsUnprefireable_bxmin1_etaphi'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_IsUnprefireable_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxmin1_Eta', 'probeL1Mu22Bxmin1_Phi')
            histos['L1Mu22_IsUnprefireable_bxmin1_eta'+suffix] = df_mu[i].Filter("L1_UnprefireableEvent").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_IsUnprefireable_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxmin1_Eta') 

            #

            histos['L1Mu22_FirstBunchInTrain_bx0_etaphi'+suffix] = df_mu[i].Filter("run>=361468").Filter("L1_FirstBunchInTrain").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_FirstBunchInTrain_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bx0_Eta', 'probeL1Mu22Bx0_Phi')
            histos['L1Mu22_FirstBunchInTrain_bx0_eta'+suffix] = df_mu[i].Filter("run>=361468").Filter("L1_FirstBunchInTrain").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_FirstBunchInTrain_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bx0_Eta') 

            histos['L1Mu22_FirstBunchInTrain_bxmin1_etaphi'+suffix] = df_mu[i].Filter("run>=361468").Filter("L1_FirstBunchInTrain").Histo2D(ROOT.RDF.TH2DModel('L1Mu22_FirstBunchInTrain_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Mu22Bxmin1_Eta', 'probeL1Mu22Bxmin1_Phi')

            histos['L1Mu22_FirstBunchInTrain_bxmin1_eta'+suffix] = df_mu[i].Filter("run>=361468").Filter("L1_FirstBunchInTrain").Histo1D(ROOT.RDF.TH1DModel('L1Mu22_FirstBunchInTrain_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Mu22Bxmin1_Eta') 

            '''
            #L1 prefiring measurement with unprefirable events
            
            #First find if there's a L1 mu in bx -1 and store its index
            df_mu[i] = df_mu[i].Define('probe_idxL1jet_inbxmin1','FindL1ObjBxMin1Idx(L1Mu_eta, L1Mu_phi, probe_Eta, probe_Phi, L1Mu_hwQual, 12)')
            df_mu[i] = df_mu[i].Define('probe_L1Pt_inbxmin1','GetVal(probe_idxL1jet, L1Mu_pt)')
            df_mu[i] = df_mu[i].Define('probeEta_L1Mu22_inbxmin1','probe_Eta[probe_Pt>30&&probe_L1Pt_inbxmin1>22]')
            df_mu[i] = df_mu[i].Define('probePhi_L1Mu22_inbxmin1','probe_Phi[probe_Pt>30&&probe_L1Pt_inbxmin1>22]')

            #Next lines are still WIP
            histos['L1Mu22_denforPrefiring_etaphi'] = df_mu[i].Filter('Flag_IsUnprefirable').Histo2D(ROOT.RDF.TH2DModel('', '', 100, -5,5, 100, -3.1416, 3.1416), 'probePt30PassL1Mu22_Eta', 'probePt30PassL1Mu22_Phi')
            histos['L1Mu22_numforPrefiring_etaphi'] = df_mu[i].Filter('Flag_IsUnprefirable').Histo2D(ROOT.RDF.TH2DModel('', '', 100, -5,5, 100, -3.1416, 3.1416), 'probeEta_L1Mu22_inbxmin1', 'probePhi_L1Mu22_inbxmin1')
            '''



    return df, histos
    




def CleanJets(df):
    #List of cleaned jets (noise cleaning + lepton/photon overlap removal)
    df = df.Define('_jetPassID', 'Jet_jetId>=4')
    #df = df.Define('_jetLeptonPhotonCleaned', 'true') 
    #df = df.Define('isCleanJet','_jetPassID&&_jetLeptonPhotonCleaned&&Jet_pt>30&&Jet_muEF<0.5&&Jet_chEmEF<0.5')
    # _jetLeptonPhotonCleaned redondant with _jetPassID
    df = df.Define('isCleanJet','_jetPassID&&Jet_pt>30&&Jet_muEF<0.5&&Jet_chEmEF<0.5')
    df = df.Define('cleanJet_Pt','Jet_pt[isCleanJet]')
    df = df.Define('cleanJet_Eta','Jet_eta[isCleanJet]')
    df = df.Define('cleanJet_Phi','Jet_phi[isCleanJet]')
    df = df.Define('cleanJet_NHEF','Jet_neHEF[isCleanJet]')
    df = df.Define('cleanJet_NEEF','Jet_neEmEF[isCleanJet]')
    df = df.Define('cleanJet_CHEF','Jet_chHEF[isCleanJet]')
    df = df.Define('cleanJet_CEEF','Jet_chEmEF[isCleanJet]')
    df = df.Define('cleanJet_MUEF','Jet_muEF[isCleanJet]')
    df = df.Filter(stringToPrintJets)
    df = df.Filter('Sum(isCleanJet)>=1','>=1 clean jet with p_{T}>30 GeV')

    return df

def lepton_ismuon(df):
    df = df.Define('_lPt', 'Muon_pt')
    df = df.Define('_lEta', 'Muon_eta')
    df = df.Define('_lPhi', 'Muon_phi')
    df = df.Define('_lpdgId', 'Muon_pdgId')
    return(df)

def lepton_iselectron(df):
    df = df.Define('_lPt', 'Electron_pt')
    df = df.Define('_lEta', 'Electron_eta')
    df = df.Define('_lPhi', 'Electron_phi')
    df = df.Define('_lpdgId', 'Electron_pdgId')
    return(df)

def EtSum(df, suffix = ''):
    histos = {}
    #HT=scalar pt sum of all jets with pt>30 and |eta|<2.5 
    df = df.Define('iscentraljet','cleanJet_Pt>30&&abs(cleanJet_Eta)<2.5')
    #df = df.Filter('Sum(iscentraljet)>0')
    df = df.Define('HT','Sum(cleanJet_Pt[cleanJet_Pt>30&&abs(cleanJet_Eta)<2.5])')

    df = df.Define('muons_px','Sum(_lPt[abs(_lpdgId)==13]*cos(_lPhi[abs(_lpdgId)==13]))')
    df = df.Define('muons_py','Sum(_lPt[abs(_lpdgId)==13]*sin(_lPhi[abs(_lpdgId)==13]))')
    df = df.Define('metnomu_x','MET_pt*cos(MET_phi)+muons_px')
    df = df.Define('metnomu_y','MET_pt*sin(MET_phi)+muons_py')
    df = df.Define('MetNoMu','sqrt(metnomu_x*metnomu_x+metnomu_y*metnomu_y)')
    #df = df.Define('L1_ETMHF80','L1_ETMHF80')
    #df = df.Define('L1_ETMHF90','L1_ETMHF90')
    #df = df.Define('L1_ETMHF100','L1_ETMHF100')
    #df = df.Define('L1_ETMHF110','L1_ETMHF110')

    # Dijet selections
    df = df.Define('hastwocleanjets', 'PassDiJet80_40_Mjj500(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('vbf_selection', 'PassDiJet140_70_Mjj900(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('hastwocentraljets', 'PassDiJet80_40_Mjj500_central(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('hastwoHFjets', 'PassDiJet80_40_Mjj500_HF(cleanJet_Pt, cleanJet_Eta, cleanJet_Phi)')

    histos['h_MetNoMu_Denominator'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    
    dfmetl1 = df.Filter('L1_ETMHF80')
    histos['L1_ETMHF80'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF80'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('L1_ETMHF90')
    histos['L1_ETMHF90'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF90'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('L1_ETMHF100')
    histos['L1_ETMHF100'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF100'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('L1_ETMHF110')
    histos['L1_ETMHF110'+suffix] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF110'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight'+suffix] =  df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60'+suffix] =  df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    

    histos['h_HT_Denominator'+suffix] = df.Filter('MET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_Denominator'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT') 
    histos['L1_HTT200er'+suffix] = df.Filter('L1_HTT200er').Filter('MET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT200er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')  
    histos['L1_HTT280er'+suffix] = df.Filter('L1_HTT280er').Filter('MET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT280er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')
    histos['L1_HTT360er'+suffix] = df.Filter('L1_HTT360er').Filter('MET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT360er'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')
    histos['HLT_PFHT1050'+suffix] =  df.Filter('HLT_PFHT1050').Filter('MET_pt<50').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFHT1050'+suffix, '', len(ht_bins)-1, array('d',ht_bins)), 'HT')

    # DiJet selections:

    # DiJet 80 40
    histos['h_MetNoMu_Denominator_DiJet80_40_Mjj500'+suffix] = df.Filter('hastwocleanjets').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_DiJet80_40_Mjj500'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight&&hastwocleanjets').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_DiJet80_40_Mjj500'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60&&hastwocleanjets').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_DiJet80_40_Mjj500'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # central dijet
    histos['h_MetNoMu_Denominator_DiJet80_40_Mjj500_central'+suffix] = df.Filter('hastwocentraljets').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_DiJet80_40_Mjj500_central'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500_central'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight&&hastwocentraljets').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500_central'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # HF dijets
    histos['h_MetNoMu_Denominator_DiJet80_40_Mjj500_HF'+suffix] = df.Filter('hastwoHFjets').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_DiJet80_40_Mjj500_HF'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500_HF'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight&&hastwoHFjets').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet80_40_Mjj500_HF'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # VBF selection (DiJet 140 70, mjj > 900 GeV) denominator
    histos['h_MetNoMu_Denominator_DiJet140_70_Mjj900'+suffix] = df.Filter('vbf_selection').Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator_DiJet140_70_Mjj900'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 

    # Normal (MET only) trigger
    histos['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet140_70_Mjj900'+suffix] = df.Filter('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight&&vbf_selection').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_DiJet140_70_Mjj900'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    # VBF (Met + jet) trigger
    histos['HLT_DiJet110_35_Mjj650_PFMET110_DiJet140_70_Mjj900'+suffix] =  df.Filter('HLT_DiJet110_35_Mjj650_PFMET110&&vbf_selection').Histo1D(ROOT.RDF.TH1DModel('h_HLT_DiJet110_35_Mjj650_PFMET110_DiJet140_70_Mjj900'+suffix, '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    return df, histos

def AnalyzeCleanJets(df, JetRecoPtCut, L1JetPtCut, suffix = ''):    
    histos = {}
    #Find L1 jets matched to the offline jet
    #df = df.Define('cleanJet_idxL1jet','FindL1ObjIdx(L1Jet_eta, L1Jet_phi, cleanJet_Eta, cleanJet_Phi)')
    # only take jets in bx 0
    df = df.Define('cleanJet_idxL1jet', 'FindL1ObjIdx_setBx(L1Jet_eta, L1Jet_phi, L1Jet_bx, cleanJet_Eta, cleanJet_Phi, 0)')
    df = df.Define('cleanJet_L1Pt','GetVal(cleanJet_idxL1jet,L1Jet_pt)')
    df = df.Define('cleanJet_L1Bx','GetVal(cleanJet_idxL1jet,L1Jet_bx)')
    df = df.Define('cleanJet_L1PtoverRecoPt','cleanJet_L1Pt/cleanJet_Pt')
    df = df.Filter(stringFailingJets)
    #Now some plotting (turn ons for now)
    L1PtCuts = [30., 40., 60., 80., 100., 120., 140., 160., 170., 180., 200.]


    df = makehistosforturnons_inprobeetaranges(df, histos, etavarname='cleanJet_Eta', phivarname='cleanJet_Phi', ptvarname='cleanJet_Pt', responsevarname='cleanJet_L1PtoverRecoPt', etabins=jetEtaBins, l1varname='cleanJet_L1Pt', l1thresholds=L1PtCuts, prefix="Jet_plots", binning=jetmetpt_bins, l1thresholdforeffvsrunnb = L1JetPtCut, offlinethresholdforeffvsrunnb = JetRecoPtCut, suffix = suffix) 

    # Make same histosgrams, in a single bin of eta (abs(eta) < 5)
    df = makehistosforturnons_inprobeetaranges(df, histos, etavarname='cleanJet_Eta', phivarname='cleanJet_Phi', ptvarname='cleanJet_Pt', responsevarname='cleanJet_L1PtoverRecoPt', etabins=[0., 5.], l1varname='cleanJet_L1Pt', l1thresholds=[40., 180.], prefix="Jet_plots_eta_inclusive", binning=jetmetpt_bins, l1thresholdforeffvsrunnb = L1JetPtCut, offlinethresholdforeffvsrunnb = JetRecoPtCut, suffix = suffix) 

    df = df.Define('cleanHighPtJet_Eta','cleanJet_Eta[cleanJet_Pt>{}]'.format(JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Phi','cleanJet_Phi[cleanJet_Pt>{}]'.format(JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Eta_PassL1Jet','cleanJet_Eta[cleanJet_L1Pt>={}&&cleanJet_Pt>{}]'.format(L1JetPtCut, JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Phi_PassL1Jet','cleanJet_Phi[cleanJet_L1Pt>={}&&cleanJet_Pt>{}]'.format(L1JetPtCut, JetRecoPtCut))
    
    histos["L1JetvsEtaPhi_Numerator"+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('h_L1Jet{}vsEtaPhi_Numerator'.format(int(L1JetPtCut))+suffix, '', 100,-5,5,100,-3.1416,3.1416), 'cleanHighPtJet_Eta_PassL1Jet','cleanHighPtJet_Phi_PassL1Jet')
    histos["L1JetvsEtaPhi_EtaRestricted"+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('h_L1Jet{}vsEtaPhi_EtaRestricted'.format(int(L1JetPtCut))+suffix, '', 100,-5,5,100,-3.1416,3.1416), 'cleanHighPtJet_Eta','cleanHighPtJet_Phi')
    


    df = df.Define('probeL1Jet100to150Bxmin1_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==-1]')
    df = df.Define('probeL1Jet100to150Bxmin1_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==-1]')
    df = df.Define('probeL1Jet100to150Bx0_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==0]')
    df = df.Define('probeL1Jet100to150Bx0_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==0]')
    df = df.Define('probeL1Jet100to150Bxplus1_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==1]')
    df = df.Define('probeL1Jet100to150Bxplus1_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==1]')

    histos['L1Jet100to150_bxmin1_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bxmin1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bxmin1_Eta', 'probeL1Jet100to150Bxmin1_Phi')
    histos['L1Jet100to150_bx0_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bx0_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bx0_Eta', 'probeL1Jet100to150Bx0_Phi')
    histos['L1Jet100to150_bxplus1_etaphi'+suffix] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bxplus1_etaphi'+suffix, '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bxplus1_Eta', 'probeL1Jet100to150Bxplus1_Phi')

    histos['L1Jet100to150_bxmin1_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('L1Jet100to150_bxmin1_eta'+suffix, '', 100, -5, 5), 'probeL1Jet100to150Bxmin1_Eta')
    histos['L1Jet100to150_bx0_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('L1Jet100to150_bx0_eta'+suffix, '', 100, -5, 5), 'probeL1Jet100to150Bx0_Eta')
    histos['L1Jet100to150_bxplus1_eta'+suffix] = df.Histo1D(ROOT.RDF.TH1DModel('L1Jet100to150_bxplus1_eta'+suffix, '', 100, -5, 5), 'probeL1Jet100to150Bxplus1_Eta')

    return df, histos

def HFNoiseStudy(df, suffix = ''):
    '''
    Offline study of HF noise.
    '''
    histos={}
    #debugging what happens in the HF 
    dfhfnoise = df.Define('isHFJet','cleanJet_Pt>30&&((cleanJet_Eta>3.0&&cleanJet_Eta<5)||(cleanJet_Eta>-5&&cleanJet_Eta<-3.))' )
    dfhfnoise = dfhfnoise.Define('nHFJets','Sum(isHFJet)')
    dfhfnoise = dfhfnoise.Define('isHFJetPt250','cleanJet_Pt>250&&((cleanJet_Eta>3.0&&cleanJet_Eta<5)||(cleanJet_Eta>-5&&cleanJet_Eta<-3.))' )
    dfhfnoise = dfhfnoise.Filter('Sum(isHFJetPt250)>0')
    dfhfnoise = dfhfnoise.Define('passL1Pt80','cleanJet_L1Pt>80')
    
    dfhfnoise = dfhfnoise.Define('HighPtHFJet_Pt','cleanJet_Pt[isHFJetPt250]')
    dfhfnoise = dfhfnoise.Define('HighPtHFJet_Eta','cleanJet_Eta[isHFJetPt250]')

    dfhfnoise = dfhfnoise.Define('HighPtJet_HFSEtaEta','Jet_hfsigmaEtaEta[Jet_pt>250&&((Jet_eta>3.0&&Jet_eta<5)||(Jet_eta>-5&&Jet_eta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFSPhiPhi','Jet_hfsigmaPhiPhi[Jet_pt>250&&((Jet_eta>3.0&&Jet_eta<5)||(Jet_eta>-5&&Jet_eta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFCentralEtaStripSize','Jet_hfcentralEtaStripSize[Jet_pt>250&&((Jet_eta>3.0&&Jet_eta<5)||(Jet_eta>-5&&Jet_eta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFAdjacentEtaStripSize','Jet_hfadjacentEtaStripsSize[Jet_pt>250&&((Jet_eta>3.0&&Jet_eta<5)||(Jet_eta>-5&&Jet_eta<-3.))]')
    
    
    prefix = ['failL1Jet80', 'passL1Jet80']
    df_passvsfailL1 = [dfhfnoise.Filter('Sum(passL1Pt80&&isHFJetPt250)==0'), dfhfnoise.Filter('Sum(passL1Pt80&&isHFJetPt250)>=1')]
    
    for i, p in enumerate(prefix):
        if i == 0:
            df_passvsfailL1[i] = df_passvsfailL1[i].Filter(stringToPrintHF)
        

        histos[p+'_nhfjets'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_nhfjets'+suffix, '', 100, 0, 100), 'nHFJets')
        histos[p+'_npv'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_npv'+suffix, '', 100, 0, 100), 'PV_npvs')
        histos[p+'_runnb'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_runnb'+suffix, '', len(runnb_bins)-1, runnb_bins), 'run')
        '''
        histos[p+'_photonpt'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_photonpt'+suffix, '', 100, 0, 1000), 'ref_Pt')
        histos[p+'_ptbalance'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_ptbalance'+suffix, '', len(response_bins)-1, response_bins), 'ptbalance')
        histos[p+'_ptbalanceL1'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_ptbalanceL1'+suffix, '', len(response_bins)-1, response_bins), 'ptbalanceL1')
        '''
        histos[p+'_HighPtHFJet_Eta'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_HighPtHFJet_Eta'+suffix, '', 1000, -5, 5), 'HighPtHFJet_Eta')
        histos[p+'_HighPtHFJet_Pt'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'_HighPtHFJet_Pt'+suffix, '', 80, 100, 500), 'HighPtHFJet_Pt')
        histos[p+'_HighPtJet_HFSEtaEtavsPhiPhi'+suffix] = df_passvsfailL1[i].Histo2D(ROOT.RDF.TH2DModel(p+'_HighPtJet_HFSEtaEtavsPhiPhi'+suffix, '', 100, 0, 0.2, 100, 0, 0.2), 'HighPtJet_HFSEtaEta','HighPtJet_HFSPhiPhi')
        histos[p+'_HighPtJet_HFCentralVsAdjacentEtaStripSize'+suffix] = df_passvsfailL1[i].Histo2D(ROOT.RDF.TH2DModel(p+'_HighPtJet_HFCentralVsAdjacentEtaStripSize'+suffix, '', 10, 0, 10, 10, 0, 10), 'HighPtJet_HFCentralEtaStripSize', 'HighPtJet_HFAdjacentEtaStripSize')

        histos[p+'MET_pt'+suffix] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(p+'MET_pt'+suffix, '', 100,0,500), 'MET_pt')





    return df, histos
    
def PtBalanceSelection(df):
    '''
    Compute pt balance = pt(jet)/pt(ref)
    ref can be a photon or a Z.
    '''
    
    #Back to back condition
    df = df.Filter('abs(acos(cos(ref_Phi-cleanJet_Phi[0])))>2.9','DeltaPhi(ph,jet)>2.9')

    # only one jet with pT > 30 GeV
    df = df.Filter('Sum(isCleanJet)==1','==1 clean jet with p_{T}>30 GeV')

    #Compute Pt balance = pt(jet)/pt(ref) => here ref is a photon
    #Reco first
    df = df.Define('ptbalance','cleanJet_Pt[0]/ref_Pt')
    df = df.Define('ptbalanceL1','L1Jet_pt[cleanJet_idxL1jet[0]]/ref_Pt')
    df = df.Define('probe_Eta','cleanJet_Eta[0]') 
    df = df.Define('probe_Phi','cleanJet_Phi[0]')
    return df

def AnalyzePtBalance(df, suffix = ''):
    histos = {}
    df_JetsBinnedInEta ={}
    histos['L1JetvsEtaPhi'+suffix] = df.Histo3D(ROOT.RDF.TH3DModel('h_L1PtBalanceVsEtaPhi'+suffix, 'ptbalanceL1', 100, -5, 5, 100, -3.1416, 3.1416, 100, 0, 2), 'probe_Eta','probe_Phi','ptbalanceL1')
    for i in range(len(jetEtaBins)-1):
        str_bineta = "eta{}to{}".format(jetEtaBins[i],jetEtaBins[i+1]).replace(".","p")
        df_JetsBinnedInEta[str_bineta] = df.Filter('abs(cleanJet_Eta[0])>={}&&abs(cleanJet_Eta[0])<{}'.format(jetEtaBins[i],jetEtaBins[i+1]))
        histos['RecoJetvsRunNb'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_PtBalanceVsRunNb_{}'.format(str_bineta)+suffix, 'ptbalance', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'run','ptbalance')
        histos['L1JetvsRunNb'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_L1PtBalanceVsRunNb_{}'.format(str_bineta)+suffix, 'ptbalanceL1', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'run','ptbalanceL1')
        histos['L1JetvsPU'+str_bineta+suffix] = df_JetsBinnedInEta[str_bineta].Histo2D(ROOT.RDF.TH2DModel('h_L1PtBalanceVsPU_{}'.format(str_bineta)+suffix, 'ptbalanceL1', 100, 0, 100, 100, 0, 2), 'PV_npvs','ptbalanceL1')

        
    return df, histos



    
