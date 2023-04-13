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
    //double drmin = 0.4; 
    double drmin = 0.6; 
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
    //double drmin = 0.4; 
    double drmin = 0.6; 
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

float mll(ROOT::VecOps::RVec<float>l_pt, ROOT::VecOps::RVec<float>l_eta, ROOT::VecOps::RVec<float>l_phi, ROOT::VecOps::RVec<int>l_pdgId){
  /*
  Float_t mll(0),ptll(0),pzll(0),yll(0),phill(0),dphill(0),costhCSll(0);
  for(unsigned int i = 0; i < _lPt.size(); i++){
    if(_lPt.size() !=2) continue;
    if(_lPt[i]<3) continue;
      if(!_lPassVetoID[i])  continue;
      if(fabs(_lpdgId[i]) !=11 && fabs(_lpdgId[i])!=13 ) continue;
      for(unsigned int j = 0; j < i; j++){
        if(_lPt[j]<3) continue;
        if(!_lPassVetoID[j])  continue;
        if(fabs(_lpdgId[j]) !=11 && fabs(_lpdgId[j])!=13 ) continue;
        //if( _lpdgId[i] != -_lpdgId[j]  ) continue;
        CalcDileptonInfo(i,j, mll,ptll,pzll,yll,phill,dphill,costhCSll);
	_mll= mll; _ptll=ptll; _pzll=pzll; _yll=yll; _phill=phill; _dphill=dphill; _costhCSll=costhCSll;
	if(fabs(_lpdgId[j]) ==11 && fabs(_lpdgId[j])  ==11) _nElesll =2 ;
	else if(fabs(_lpdgId[j]) ==13 && fabs(_lpdgId[j])  ==13) _nElesll =0 ;
	else _nElesll = 1;
      }
  }
  */
  float mll = 0.;
  for(unsigned int i = 0; i < l_pt.size(); i++){
      if(l_pt.size() != 2) continue;
      if(l_pt[i] < 3) continue;
      // bypass  lPassVetoID
      if(fabs(l_pdgId[i]) != 11 && fabs(l_pdgId[i] != 13 )) continue;
      for(unsigned int j = 0; j < i; j++){
          if(l_pt[j] < 3) continue;
          if(fabs(l_pdgId[j]) != 11 && fabs(l_pdgId[j] != 13 )) continue;

          TLorentzVector lep1;
          TLorentzVector lep2;
          lep1.SetPtEtaPhiE(l_pt[i], l_eta[i], l_phi[i], l_pt[i] * cosh(l_eta[i]));
          lep2.SetPtEtaPhiE(l_pt[j], l_eta[j], l_phi[j], l_pt[j] * cosh(l_eta[j]));

          mll = (lep1+lep2).Mag();
      }
  }
  return mll;
}
