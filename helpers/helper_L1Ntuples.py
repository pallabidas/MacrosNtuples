import ROOT
from array import array
jetEtaBins = [0., 1.3, 2.5, 3., 3.5, 4., 5.]
egEtaBins = [0., 1.479, 2.5]
muEtaBins = [0., 0.83, 1.24, 2.4]


ht_bins = array('f', [ i*10 for i in range(30) ] + [ 300+ i*20 for i in range(10) ])
leptonpt_bins = array('f',[ i for i in range(50) ] + [ 50+2*i for i in range(10) ] + [ 70+3*i for i in range(10) ] + [100+10*i for i in range(10) ] + [200, 250, 300, 400, 500])
jetmetpt_bins = array('f',[ i*2.5 for i in range(40) ] +  [ 100+i*5 for i in range(40) ])

from runsBinning import *
runnb_bins = array('f', runbinning())
print(type(runnb_bins))
print(runnb_bins)
response_bins = array('f',[0.+float(i)/100. for i in range(200)] )

#String printing stuff for a few events
stringToPrint = '''
if(EventsToPrint <100) {

cout << "*********New Event********"<<endl;
cout << "_runNb " << _runNb<<endl;

for(unsigned int i = 0;i< (_lPt).size();i++ ){
cout << "Lepton Pt, Eta, Phi: " << (_lPt)[i]<<", "<<(_lEta)[i]<<", "<<(_lPhi)[i]<<endl;
cout << "Lepton pdgId: " << (_lpdgId)[i]<<endl;
}
for(unsigned int i = 0;i< (_phPt).size();i++ ){
cout << "Photon Pt, Eta, Phi: " << (_phPt)[i]<<", "<<(_phEta)[i]<<", "<<(_phPhi)[i]<<endl;
}
for(unsigned int i = 0;i< (_jetPt).size();i++ ){
cout << "jet Pt, Eta, Phi: " << (_jetPt)[i]<<", "<<(_jetEta)[i]<<", "<<(_jetPhi)[i]<<endl;
cout << "jet PassID, MUEF, CEEF, CHEF: " << (_jetPassID)[i]<<", "<<(_jet_MUEF)[i]<<", "<<(_jet_CEEF)[i]<<", "<<  (_jet_CHEF)[i]<<endl;
}

for(unsigned int i = 0;i< (_L1eg_pt).size();i++ ){
cout << "L1 EG Pt, Eta, Phi: " << (_L1eg_pt)[i]<<", "<<(_L1eg_eta)[i]<<", "<<(_L1eg_phi)[i]<<endl;
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










stringToPrintHF = '''
if(EventsToPrint <100) {

cout << "*********New Event********"<<endl;
cout << "_runNb " << _runNb<<endl;
cout << "met, met_phi " << _met <<", "<<_met_phi<<endl;
for(unsigned int i = 0;i< (_lPt).size();i++ ){
cout << "Lepton Pt, Eta, Phi: " << (_lPt)[i]<<", "<<(_lEta)[i]<<", "<<(_lPhi)[i]<<endl;
cout << "Lepton pdgId: " << (_lpdgId)[i]<<endl;
}
for(unsigned int i = 0;i< (_phPt).size();i++ ){
cout << "Photon Pt, Eta, Phi: " << (_phPt)[i]<<", "<<(_phEta)[i]<<", "<<(_phPhi)[i]<<endl;
}
for(unsigned int i = 0;i< (_jetPt).size();i++ ){
cout << "jet Pt, Eta, Phi: " << (_jetPt)[i]<<", "<<(_jetEta)[i]<<", "<<(_jetPhi)[i]<<endl;
cout << "jet PassID, MUEF, CEEF, CHEF, NHEF: " << (_jetPassID)[i]<<", "<<(_jet_MUEF)[i]<<", "<<(_jet_CEEF)[i]<<", "<<  (_jet_CHEF)[i]<<", "<<  (_jet_NHEF)[i]<<endl;
cout << "jethfsigmaEtaEta jethfsigmaPhiPhi jethfcentralEtaStripSize "<< (_jethfsigmaEtaEta)[i]<<", "<<  (_jethfsigmaPhiPhi)[i]<<", "<<(_jethfcentralEtaStripSize)[i]<<endl;
}


for(unsigned int i = 0;i< (_L1jet_pt).size();i++ ){
cout << "L1 JET Pt, Eta, Phi, Bx: " << (_L1jet_pt)[i]<<", "<<(_L1jet_eta)[i]<<", "<<(_L1jet_phi)[i]<<", " << (_L1jet_bx)[i]<<endl;
}



cout <<endl;

EventsToPrint++;
} 
return true;
'''


    
def MuonJet_MuonSelection(df):
    '''
    Select events with >= 1 muon with pT>25 GeV.
    The event must pass a single muon trigger. 
    '''

    df = df.Define('goodmuonPt25','Muon.pt>25&&Muon.isMediumMuon')
    df = df.Filter('Sum(goodmuonPt25)>=1','>=1 muon with p_{T}>25 GeV')
    df = df.Define('badmuonPt10','Muon.pt>10&&Muon.isLooseMuon==0')
    df = df.Filter('Sum(badmuonPt10)==0','No bad quality muon')
    return df
    
    


def CleanJets(df):
    #List of cleaned jets (noise cleaning + lepton/photon overlap removal)
    df = df.Define('isCleanJet','Jet.et>30&&Jet.mef<0.2')
    #df = df.Define('isCleanJet','Jet.et>30')
    df = df.Define('cleanJet_Pt','Jet.et[isCleanJet]')
    df = df.Define('cleanJet_Eta','Jet.eta[isCleanJet]')
    df = df.Define('cleanJet_Phi','Jet.phi[isCleanJet]')
    
    df = df.Filter('Sum(isCleanJet)>=1','>=1 clean jet with p_{T}>30 GeV')

    return df



def EtSum(df):
    histos = {}
    #HT=scalar pt sum of all jets with pt>30 and |eta|<2.5 
    df = df.Define('iscentraljet','cleanJet_Pt>30&&abs(cleanJet_Eta)<2.5')
    #df = df.Filter('Sum(iscentraljet)>0')
    df = df.Define('HT','Sum(cleanJet_Pt[cleanJet_Pt>30&&abs(cleanJet_Eta)<2.5])')

    df = df.Define('MetNoMu','Sums.pfMetNoMu')
    df = df.Define('L1_ETMHF80','L1uGT.m_algoDecisionInitial[419]')
    df = df.Define('L1_ETMHF90','L1uGT.m_algoDecisionInitial[420]')
    df = df.Define('L1_ETMHF100','L1uGT.m_algoDecisionInitial[421]')

    histos['h_MetNoMu_Denominator'] = df.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_Denominator', '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu') 
    
    dfmetl1 = df.Filter('L1uGT.m_algoDecisionInitial[419]')
    histos['L1_ETMHF80'] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF80', '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('L1uGT.m_algoDecisionInitial[420]')
    histos['L1_ETMHF80'] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF90', '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')
    dfmetl1 = df.Filter('L1uGT.m_algoDecisionInitial[421]')
    histos['L1_ETMHF100'] = dfmetl1.Histo1D(ROOT.RDF.TH1DModel('h_MetNoMu_ETMHF100', '', len(jetmetpt_bins)-1, array('d',jetmetpt_bins)), 'MetNoMu')

    histos['h_HT_Denominator'] = df.Filter('Sums.met<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_Denominator', '', len(ht_bins)-1, array('d',ht_bins)), 'HT') 
    histos['L1_HTT200er'] = df.Filter('L1uGT.m_algoDecisionInitial[400]').Filter('Sums.met<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT200er', '', len(ht_bins)-1, array('d',ht_bins)), 'HT')  
    histos['L1_HTT280er'] = df.Filter('L1uGT.m_algoDecisionInitial[402]').Filter('Sums.met<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT280er', '', len(ht_bins)-1, array('d',ht_bins)), 'HT')
    histos['L1_HTT360er'] = df.Filter('L1uGT.m_algoDecisionInitial[404]').Filter('Sums.met<50').Histo1D(ROOT.RDF.TH1DModel('h_HT_L1_HTT360er', '', len(ht_bins)-1, array('d',ht_bins)), 'HT')
    #histos['HLT_PFHT1050'] =  df.Filter('HLT_PFHT1050').Filter('Sums.met<50').Histo1D(ROOT.RDF.TH1DModel('h_HLT_PFHT1050', '', len(ht_bins)-1, array('d',ht_bins)), 'HT')

    return df, histos

def AnalyzeCleanJets(df, JetRecoPtCut, L1JetPtCut):    
    histos = {}
    #Find L1 jets matched to the offline jet
    df = df.Define('cleanJet_idxL1jet','FindL1ObjIdx(L1Upgrade.jetEta, L1Upgrade.jetPhi, cleanJet_Eta, cleanJet_Phi)')
    df = df.Define('cleanJet_L1Pt','GetVal(cleanJet_idxL1jet,L1Upgrade.jetEt)')
    df = df.Define('cleanJet_L1Bx','GetVal(cleanJet_idxL1jet,L1Upgrade.jetBx)')
    df = df.Define('cleanJet_L1PtoverRecoPt','cleanJet_L1Pt/cleanJet_Pt')
    #Now some plotting (turn ons for now)
    L1PtCuts = [30., 40., 60., 80., 100., 120., 140., 160., 170., 180., 200.]


    df = makehistosforturnons_inprobeetaranges(df, histos, etavarname='cleanJet_Eta', phivarname='cleanJet_Phi', ptvarname='cleanJet_Pt', responsevarname='cleanJet_L1PtoverRecoPt', etabins=jetEtaBins, l1varname='cleanJet_L1Pt', l1thresholds=L1PtCuts, prefix="Jet_plots", binning=jetmetpt_bins, l1thresholdforeffvsrunnb = L1JetPtCut, offlinethresholdforeffvsrunnb = JetRecoPtCut )


    
    df = df.Define('cleanHighPtJet_Eta','cleanJet_Eta[cleanJet_Pt>{}]'.format(JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Phi','cleanJet_Phi[cleanJet_Pt>{}]'.format(JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Eta_PassL1Jet','cleanJet_Eta[cleanJet_L1Pt>={}&&cleanJet_Pt>{}]'.format(L1JetPtCut, JetRecoPtCut))
    df = df.Define('cleanHighPtJet_Phi_PassL1Jet','cleanJet_Phi[cleanJet_L1Pt>={}&&cleanJet_Pt>{}]'.format(L1JetPtCut, JetRecoPtCut))
    
    histos["L1JetvsEtaPhi_Numerator"] = df.Histo2D(ROOT.RDF.TH2DModel('h_L1Jet{}vsEtaPhi_Numerator'.format(int(L1JetPtCut)), '', 100,-5,5,100,-3.1416,3.1416), 'cleanHighPtJet_Eta_PassL1Jet','cleanHighPtJet_Phi_PassL1Jet')
    histos["L1JetvsEtaPhi_EtaRestricted"] = df.Histo2D(ROOT.RDF.TH2DModel('h_L1Jet{}vsEtaPhi_EtaRestricted'.format(int(L1JetPtCut)), '', 100,-5,5,100,-3.1416,3.1416), 'cleanHighPtJet_Eta','cleanHighPtJet_Phi')
    


    df = df.Define('probeL1Jet100to150Bxmin1_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==-1]')
    df = df.Define('probeL1Jet100to150Bxmin1_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==-1]')
    df = df.Define('probeL1Jet100to150Bx0_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==0]')
    df = df.Define('probeL1Jet100to150Bx0_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==0]')
    df = df.Define('probeL1Jet100to150Bxplus1_Eta','cleanJet_Eta[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==1]')
    df = df.Define('probeL1Jet100to150Bxplus1_Phi','cleanJet_Phi[cleanJet_Pt>90&&cleanJet_Pt<160&&cleanJet_L1Pt>100&&cleanJet_L1Pt<=150&&cleanJet_L1Bx==1]')




    histos['L1Jet100to150_bxmin1_etaphi'] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bxmin1_etaphi', '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bxmin1_Eta', 'probeL1Jet100to150Bxmin1_Phi')
    histos['L1Jet100to150_bx0_etaphi'] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bx0_etaphi', '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bx0_Eta', 'probeL1Jet100to150Bx0_Phi')
    histos['L1Jet100to150_bxplus1_etaphi'] = df.Histo2D(ROOT.RDF.TH2DModel('L1Jet100to150_bxplus1_etaphi', '', 100, -5,5, 100, -3.1416, 3.1416), 'probeL1Jet100to150Bxplus1_Eta', 'probeL1Jet100to150Bxplus1_Phi')



    return df, histos



def HFNoiseStudy(df):
    histos={}
    #debugging what happens in the HF 
    dfhfnoise = df.Define('isHFJet','cleanJet_Pt>30&&((cleanJet_Eta>3.0&&cleanJet_Eta<5)||(cleanJet_Eta>-5&&cleanJet_Eta<-3.))' )
    dfhfnoise = dfhfnoise.Define('nHFJets','Sum(isHFJet)')
    dfhfnoise = dfhfnoise.Define('isHFJetPt250','cleanJet_Pt>250&&((cleanJet_Eta>3.0&&cleanJet_Eta<5)||(cleanJet_Eta>-5&&cleanJet_Eta<-3.))' )
    dfhfnoise = dfhfnoise.Filter('Sum(isHFJetPt250)>0')
    dfhfnoise = dfhfnoise.Define('passL1Pt80','cleanJet_L1Pt>80')
    
    dfhfnoise = dfhfnoise.Define('HighPtHFJet_Pt','cleanJet_Pt[isHFJetPt250]')
    dfhfnoise = dfhfnoise.Define('HighPtHFJet_Eta','cleanJet_Eta[isHFJetPt250]')

    dfhfnoise = dfhfnoise.Define('HighPtJet_HFSEtaEta','_jethfsigmaEtaEta[_jetPt>250&&((_jetEta>3.0&&_jetEta<5)||(_jetEta>-5&&_jetEta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFSPhiPhi','_jethfsigmaPhiPhi[_jetPt>250&&((_jetEta>3.0&&_jetEta<5)||(_jetEta>-5&&_jetEta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFCentralEtaStripSize','_jethfcentralEtaStripSize[_jetPt>250&&((_jetEta>3.0&&_jetEta<5)||(_jetEta>-5&&_jetEta<-3.))]')
    dfhfnoise = dfhfnoise.Define('HighPtJet_HFAdjacentEtaStripSize','_jethfadjacentEtaStripsSize[_jetPt>250&&((_jetEta>3.0&&_jetEta<5)||(_jetEta>-5&&_jetEta<-3.))]')
    
    

    
    

    suffix = ['failL1Jet80', 'passL1Jet80']
    df_passvsfailL1 = [dfhfnoise.Filter('Sum(passL1Pt80&&isHFJetPt250)==0'), dfhfnoise.Filter('Sum(passL1Pt80&&isHFJetPt250)>=1')]
    
    for i, s in enumerate(suffix):
        if i == 0:
            df_passvsfailL1[i] = df_passvsfailL1[i].Filter(stringToPrintHF)
        

        histos[s+'_nhfjets'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_nhfjets', '', 100, 0, 100), 'nHFJets')
        histos[s+'_npv'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_npv', '', 100, 0, 100), '_n_PV')
        histos[s+'_runnb'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_runnb', '', len(runnb_bins)-1, runnb_bins), '_runNb')
        '''
        histos[s+'_photonpt'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_photonpt', '', 100, 0, 1000), 'ref_Pt')
        histos[s+'_ptbalance'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_ptbalance', '', len(response_bins)-1, response_bins), 'ptbalance')
        histos[s+'_ptbalanceL1'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_ptbalanceL1', '', len(response_bins)-1, response_bins), 'ptbalanceL1')
        '''
        histos[s+'_HighPtHFJet_Eta'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_HighPtHFJet_Eta', '', 1000, -5, 5), 'HighPtHFJet_Eta')
        histos[s+'_HighPtHFJet_Pt'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_HighPtHFJet_Pt', '', 80, 100, 500), 'HighPtHFJet_Pt')
        histos[s+'_HighPtJet_HFSEtaEtavsPhiPhi'] = df_passvsfailL1[i].Histo2D(ROOT.RDF.TH2DModel(s+'_HighPtJet_HFSEtaEtavsPhiPhi', '', 100, 0, 0.2, 100, 0, 0.2), 'HighPtJet_HFSEtaEta','HighPtJet_HFSPhiPhi')
        histos[s+'_HighPtJet_HFCentralVsAdjacentEtaStripSize'] = df_passvsfailL1[i].Histo2D(ROOT.RDF.TH2DModel(s+'_HighPtJet_HFCentralVsAdjacentEtaStripSize', '', 10, 0, 10, 10, 0, 10), 'HighPtJet_HFCentralEtaStripSize', 'HighPtJet_HFAdjacentEtaStripSize')

        histos[s+'_met'] = df_passvsfailL1[i].Histo1D(ROOT.RDF.TH1DModel(s+'_met', '', 100,0,500), 'Sums.met')





    return df, histos
    










def makehistosforturnons_inprobeetaranges(df, histos, etavarname, phivarname, ptvarname, responsevarname, etabins, l1varname, l1thresholds, prefix, binning, l1thresholdforeffvsrunnb, offlinethresholdforeffvsrunnb):
    '''Make histos for turnons vs pt (1D histos for numerator and denominator) in ranges of eta
    Also look at response vs run number (2D histo) '''
    for i in range(len(etabins)-1):
        str_bineta = "eta{}to{}".format(etabins[i],etabins[i+1]).replace(".","p")
        #Define columns corresponding to pt and response for the selected eta range 
        df_etarange = df.Define('inEtaRange','abs({})>={}'.format(etavarname, etabins[i])+'&&abs({})<{}'.format(etavarname, etabins[i+1]))
        df_etarange = df_etarange.Filter('Sums.met<100')
        df_etarange = df_etarange.Define('denominator_pt',ptvarname+'[inEtaRange]')
        df_etarange = df_etarange.Define('response',responsevarname+'[inEtaRange]')
        df_etarange = df_etarange.Define('runnb',"return ROOT::VecOps::RVec<int>(response.size(), Event.run);")

        #Response vs pt and vs runnb (2d)
        histos[prefix+str_bineta] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_{}_{}'.format(prefix, str_bineta), '', len(binning)-1, binning), 'denominator_pt')
        histos[prefix+str_bineta+'_ResponseVsPt'] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsPt_{}_{}'.format(prefix, str_bineta), '', 200, 0, 200, 100, 0, 2), 'denominator_pt', 'response')
        histos[prefix+str_bineta+'_ResponseVsRunNb'] = df_etarange.Histo2D(ROOT.RDF.TH2DModel('h_ResponseVsRunNb_{}_{}'.format(prefix, str_bineta), '', len(runnb_bins)-1, runnb_bins, len(response_bins)-1, response_bins), 'runnb', 'response')

        if i ==1 and prefix == 'EGNonIso_plots':
            df_etarange = df_etarange.Filter(stringToPrint)

            
        #Numerator/denominator for plateau eff vs runnb
        df_etarange = df_etarange.Define('inplateau','{}>={}&&inEtaRange'.format(ptvarname,offlinethresholdforeffvsrunnb))
        df_etarange = df_etarange.Define('N_inplateau','Sum(inplateau)')
        df_etarange = df_etarange.Define('runnb_inplateau',"return ROOT::VecOps::RVec<int>(N_inplateau, Event.run);")
        df_etarange = df_etarange.Define('inplateaupassL1','inplateau && {}>={}'.format(l1varname,l1thresholdforeffvsrunnb))
        df_etarange = df_etarange.Define('N_inplateaupassL1','Sum(inplateaupassL1)')
        df_etarange = df_etarange.Define('runnb_inplateaupassL1',"return ROOT::VecOps::RVec<int>(N_inplateaupassL1, Event.run);")
        histos[prefix+"_plateaueffvsrunnb_numerator_"+str_bineta] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_PlateauEffVsRunNb_Numerator_{}_{}'.format(prefix, str_bineta), '', len(runnb_bins)-1, runnb_bins),'runnb_inplateaupassL1')
        histos[prefix+"_plateaueffvsrunnb_denominator_"+str_bineta] = df_etarange.Histo1D(ROOT.RDF.TH1DModel('h_PlateauEffVsRunNb_Denominator_{}_{}'.format(prefix, str_bineta), '', len(runnb_bins)-1, runnb_bins),'runnb_inplateau')

        for ipt in l1thresholds:
            str_binetapt = "eta{}to{}_l1thrgeq{}".format(etabins[i], etabins[i+1],ipt).replace(".","p")
            df_loc = df_etarange.Define('passL1Cond','{}>={}'.format(l1varname, ipt))
            df_loc = df_loc.Define('numerator_pt',ptvarname+'[inEtaRange&&passL1Cond]')
            histos[prefix+str_binetapt] = df_loc.Histo1D(ROOT.RDF.TH1DModel('h_{}_{}'.format(prefix, str_binetapt), '', len(binning)-1, binning), 'numerator_pt')

        

    return df #, histos

