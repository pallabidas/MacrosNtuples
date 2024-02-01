#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
 
using namespace ROOT;
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
int EventsToPrint = 0;

double deltaphi_offlinemustation2_l1mu(int charge, double mupt, double mueta, double muphi, double l1muphi){
    const double etaboundary_EMTF = 1.24;
    const double Bfield = 3.8; //in Tesla
    const double Z_CSC_station2 = 8.2; //in meters
    const double R_station2 =  (abs(mueta)<etaboundary_EMTF) ? 5 : abs(Z_CSC_station2*tan(2*atan(exp(-mueta)))); //in meters

    double corr = asin(0.5*0.3*Bfield*R_station2/mupt); 
    double muphi_station2 = (charge<0)? muphi+corr : muphi-corr; 
    double dphi = muphi_station2-l1muphi; 

    if(dphi> M_PI) dphi -= 2* M_PI;
    if(dphi<- M_PI) dphi += 2* M_PI;
    return dphi;
}  

vector<int> FindL1ObjIdx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){
    double drmin = 0.4; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      double dphi = abs(acos(cos(recoObj_Phi[i]-L1Obj_phi[j]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}

vector<int> FindL1MuIdx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, 
        ROOT::VecOps::RVec<float>recoObj_Pt, ROOT::VecOps::RVec<int>charge, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){
    double drmin = 0.4; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      double dphi = deltaphi_offlinemustation2_l1mu(charge[j], recoObj_Pt[i], recoObj_Eta[i], recoObj_Phi[i], L1Obj_phi[j]);
      double dr = sqrt(deta*deta+dphi*dphi);
      
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}

// Match objects only in a given bunch crossing
vector<int> FindL1MuIdx_setBx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>L1Obj_bx, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, 
        ROOT::VecOps::RVec<float>recoObj_Pt, ROOT::VecOps::RVec<int>charge, int bx, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){
    //double drmin = 0.4; 
    double drmin = 0.6; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      if(L1Obj_bx[j] != bx){
          continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      // Delta Phi correction at station 2
      double dphi = deltaphi_offlinemustation2_l1mu(charge[j], recoObj_Pt[i], recoObj_Eta[i], recoObj_Phi[i], L1Obj_phi[j]);
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}

vector<int> FindL1ObjIdx_setBx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>L1Obj_bx, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, int bx, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){
    //double drmin = 0.4; 
    double drmin = 0.6; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      if(L1Obj_bx[j] != bx){
          continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      double dphi = abs(acos(cos(recoObj_Phi[i]-L1Obj_phi[j]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}

ROOT::VecOps::RVec<float> GetVal(ROOT::VecOps::RVec<int>idxL1Obj, ROOT::VecOps::RVec<float>L1Obj_val){
  ROOT::VecOps::RVec<float> result ={}; 
  for(unsigned int i = 0; i<idxL1Obj.size(); i++){
    if(idxL1Obj[i]<0) result.push_back(-1);
    else result.push_back(L1Obj_val[idxL1Obj[i]]);
  }
  return result;
}



vector<float> HighestMjj_L1(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx){

  vector<float> result;
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<30.)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<30.)continue;
      if(bx[j]!=0)continue;
      TLorentzVector jet1, jet2;
      jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
      jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
      float mass = (jet1+jet2).Mag();
      if(mass>result[0]){
	result[0] = mass;
	result[3] = abs(eta[i]-eta[j]);
	result[4] = abs(acos(cos(phi[i]-phi[j])));
	if(pt[j]> pt[i]){ result[1] = pt[j] ; result[2] = pt[i] ;}
	else {  result[1] = pt[i] ; result[2] = pt[j] ; }
      }
    }
  }
  return result;
}





bool L1SeedDoubleJetEtaMin(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double detacut, double dphicut){
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<ptlead)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<pttrail)continue;
      if(bx[j]!=0)continue;
      float dphi = abs(acos(cos(phi[i]-phi[j])));
      if(abs(eta[i]-eta[j]) >= detacut&& dphi< dphicut )return true;
    }      
  }
  return false;
}


bool L1SeedDoubleJetMassMin(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double masscut, double dphicut){
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<ptlead)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<pttrail)continue;
      if(bx[j]!=0)continue;

      TLorentzVector jet1, jet2;
      jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
      jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
      float mass = (jet1+jet2).Mag();
      float dphi = abs(acos(cos(phi[i]-phi[j])));
      if(mass >= masscut && dphi< dphicut )return true;
    }      
  }
  return false;
}








vector<float> L1MHTHF(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx){
  vector<float> result;
  TVector2 mhthf(0.,0.);
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<30.)continue;
    if(bx[i]!=0)continue;
    TVector2 jetpt(0.,0.); 
    jetpt.SetMagPhi(pt[i], phi[i]);
    mhthf+=jetpt;
    
  }
  result.push_back(mhthf.Mod());
  result.push_back(mhthf.Phi());
  return result;
}

bool L1SeedDoubleJetMassMinNoOS(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double masscut, double dphicut){
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<ptlead)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      
      if(pt[j]<pttrail)continue;
      if(bx[j]!=0)continue;
      
      TLorentzVector jet1, jet2;
      jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
      jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
      float mass = (jet1+jet2).Mag();
      float dphi = abs(acos(cos(phi[i]-phi[j])));
      if(mass >= masscut && dphi< dphicut )return true;
    }      
  }
  return false;
}







bool L1SeedPtLeadDoubleJetMassMin(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double masscut, double dphicut){
  
  bool passleading = false;
  for(unsigned int i = 0; i<pt.size(); i++){
    if(bx[i]!=0)continue;
    if(pt[i]<ptlead)continue;
    passleading = true;
  }
  
  if(!passleading) return false;
  
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<pttrail)continue;
        if(bx[i]!=0)continue;
        for(unsigned int j = 0; j<pt.size(); j++){
            if(eta[i]*eta[j]>0) continue;
            if(pt[j]<pttrail)continue;
            if(bx[j]!=0)continue;

		      TLorentzVector jet1, jet2;
            jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
            jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
            float mass = (jet1+jet2).Mag();
            float dphi = abs(acos(cos(phi[i]-phi[j])));
            if(mass >= masscut && dphi< dphicut )return true;
          }      
      }
    return false;
  }

float mll(ROOT::VecOps::RVec<float>l_pt, ROOT::VecOps::RVec<float>l_eta, ROOT::VecOps::RVec<float>l_phi, ROOT::VecOps::RVec<bool>l_isTag, ROOT::VecOps::RVec<bool>l_isProbe){
  float mll = -1.;
  for(unsigned int i = 0; i < l_pt.size(); i++){
    if(l_pt.size() < 2) continue;
    if(l_isProbe[i] == false) continue;
    for(unsigned int j = 0; j < l_pt.size(); j++){
      if(i == j) continue;
      if(l_isTag[j] == false) continue;

      TLorentzVector lep1;
      TLorentzVector lep2;
      lep1.SetPtEtaPhiE(l_pt[i], l_eta[i], l_phi[i], l_pt[i] * cosh(l_eta[i]));
      lep2.SetPtEtaPhiE(l_pt[j], l_eta[j], l_phi[j], l_pt[j] * cosh(l_eta[j]));

      if(lep1.DeltaR(lep2) > 0.4){
	mll = (lep1+lep2).Mag();
      }
    }
  }
  return mll;
}

vector<vector<vector<float>>> dR_mll(ROOT::VecOps::RVec<float>l_pt, ROOT::VecOps::RVec<float>l_eta, ROOT::VecOps::RVec<float>l_phi, ROOT::VecOps::RVec<bool>l_isTag, ROOT::VecOps::RVec<bool>l_isProbe){
  //float mll = -1.;
  vector<vector<vector<float>>> result = {};
  if(l_pt.size() < 2){
    return result;
  }
  for(unsigned int i = 0; i < l_pt.size(); i++){
    vector<vector<float>> line = {};
    for(unsigned int j = 0; j < l_pt.size(); j++){

      float DeltaR = -1;
      float mll = -1;
      vector<float> pair = {};

      if((l_isProbe[i] == false)||(l_isTag[j] == false)||(i == j)){
	pair.push_back(DeltaR);
	pair.push_back(mll);
	line.push_back(pair);
	continue;
      }

      TLorentzVector lep1;
      TLorentzVector lep2;
      lep1.SetPtEtaPhiE(l_pt[i], l_eta[i], l_phi[i], l_pt[i] * cosh(l_eta[i]));
      lep2.SetPtEtaPhiE(l_pt[j], l_eta[j], l_phi[j], l_pt[j] * cosh(l_eta[j]));

      DeltaR = lep1.DeltaR(lep2);
      mll = (lep1+lep2).Mag();

      pair.push_back(DeltaR);
      pair.push_back(mll);
      line.push_back(pair);

    }
    result.push_back(line);
  }
  return result;
}

// Match offline object to TrigObj

vector<int> MatchObjToTrig(ROOT::VecOps::RVec<float>Obj_eta, ROOT::VecOps::RVec<float>Obj_phi, ROOT::VecOps::RVec<float>TrigObj_pt, ROOT::VecOps::RVec<float>TrigObj_eta, ROOT::VecOps::RVec<float>TrigObj_phi, ROOT::VecOps::RVec<int>TrigObj_id, int Target_id, ROOT::VecOps::RVec<int>filterBits){

  vector <int> result={};
  for(unsigned int i = 0; i<Obj_eta.size(); i++){
    //For HLT-reco matching => can use a small dR cone size. A larger cone size would be needed for L1-reco matching with muons. 
    double drmin = 0.2; 
    int idx = -1;
    for(unsigned int j = 0; j<TrigObj_eta.size(); j++){
      if (TrigObj_id[j] != Target_id) continue;

      double deta = abs(TrigObj_eta[j]-Obj_eta[i]);
      //double dphi = deltaphi_offlinemustation2_l1mu(Muon_charge[i], TrigObj_pt[j], TrigObj_eta[j], TrigObj_phi[j], Muon_phi[i]);
      double dphi = abs(acos(cos(TrigObj_phi[j]-Obj_phi[i]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	if((filterBits[j]>>1&1) == 1){
	  drmin = dr; 
	  idx = j;
	}
      }
    }
    result.push_back(idx);
  }
  return result;
}

// Recover triger decision from filterbit
ROOT::VecOps::RVec <Bool_t> trig_is_filterbit1_set(ROOT::VecOps::RVec<int>Trig_idx, ROOT::VecOps::RVec<int>filterBits){
    vector <bool> result = {};
    for( unsigned int i = 0; i <Trig_idx.size(); i++){
        if (Trig_idx[i] == -1) result.push_back(false);
        else {
            int idx = Trig_idx[i];
            if((filterBits[idx]>>1&1) == 1) result.push_back(true);
            else result.push_back(false);
        }
    }
    return result;
}


ROOT::VecOps::RVec <Bool_t> IsCleanJet(ROOT::VecOps::RVec<float>Obj_pt,  ROOT::VecOps::RVec<float>Obj_eta, ROOT::VecOps::RVec<float>Obj_phi, 
				       ROOT::VecOps::RVec<float>Lepton_pt, ROOT::VecOps::RVec<float>Lepton_eta, ROOT::VecOps::RVec<float>Lepton_phi, ROOT::VecOps::RVec<int>Lepton_passid,
				       ROOT::VecOps::RVec<float>Photon_pt, ROOT::VecOps::RVec<float>Photon_eta, ROOT::VecOps::RVec<float>Photon_phi, ROOT::VecOps::RVec<int>Photon_passid ){

  vector <bool> result={};
  for(unsigned int i = 0; i<Obj_eta.size(); i++){
    result.push_back(true);
    double drmin = 0.4; 
  
    for(unsigned int j = 0; j<Lepton_eta.size(); j++){
      if (! Lepton_passid[j] || Lepton_pt[j]<10  ) continue;
      double deta = abs(Lepton_eta[j]-Obj_eta[i]);
      double dphi = abs(acos(cos(Lepton_phi[j]-Obj_phi[i]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){
	result[i] =false;
	break;
      }
    }

    for(unsigned int j = 0; j<Photon_eta.size(); j++){
      if (! Photon_passid[j] || Photon_pt[j]<20  ) continue;
      double deta = abs(Photon_eta[j]-Obj_eta[i]);
      double dphi = abs(acos(cos(Photon_phi[j]-Obj_phi[i]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){
	result[i] =false;
	break;
      }
    }
  }

  return result;
}
