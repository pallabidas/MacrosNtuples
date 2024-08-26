#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TH1.h>
#include <TFile.h>
#include <TEfficiency.h>
#include <TTree.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include "fstream"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
using namespace std;

double deltaR (double eta1, double phi1, double eta2, double phi2){
  double dp = std::abs(phi1 - phi2);
  if (dp > double(M_PI)) dp -= double(2 * M_PI);
  double deltaR2 = (eta1 - eta2) * (eta1 - eta2) + dp * dp;
  return std::sqrt(deltaR2);
};

void calc_jet_rate(const char *inFile, const char *outFile){
  TH1F* h_all = new TH1F("h_all", "h_all", 5, 0, 5);
  TH1F* h_emuJetEt = new TH1F("h_emuJetEt", "h_emuJetEt", 50, 0, 1100);
  TH1F* h_emuLeadingJetEt = new TH1F("h_emuLeadingJetEt", "h_emuLeadingJetEt", 100, 0, 1100);
  TH1F* h_emuLeadingJetEta = new TH1F("h_emuLeadingJetEta", "h_emuLeadingJetEta", 100, -5, 5);
  TH1F* h_emuJetEta = new TH1F("h_emuJetEta", "h_emuJetEta", 50, -5, 5);
  TH1F* h_emuJetPhi = new TH1F("h_emuJetPhi", "h_emuJetPhi", 50, -M_PI, M_PI);
  TH1F* h_emuHT = new TH1F("h_emuHT", "h_emuHT", 100, 0, 1100);
  TH1F* h_emuMHTHF = new TH1F("h_emuMHTHF", "h_emuMHTHF", 100, 0, 400);

  TH1F* h_jetEt = new TH1F("h_jetEt", "h_jetEt", 50, 0, 1100);
  TH1F* h_leadingJetEt = new TH1F("h_leadingJetEt", "h_leadingJetEt", 100, 0, 1100);
  TH1F* h_leadingJetEta = new TH1F("h_leadingJetEta", "h_leadingJetEta", 100, -5, 5);
  TH1F* h_jetEta = new TH1F("h_jetEta", "h_jetEta", 50, -5, 5);
  TH1F* h_jetPhi = new TH1F("h_jetPhi", "h_jetPhi", 50, -M_PI, M_PI);
  TH1F* h_HT = new TH1F("h_HT", "h_HT", 100, 0, 1100);
  TH1F* h_MHTHF = new TH1F("h_MHTHF", "h_MHTHF", 100, 0, 400);

  TFile* f = new TFile(inFile);
  TTree* t = (TTree*)(f->Get("l1UpgradeTree/L1UpgradeTree"));
  TTreeReader myReader(t);
  TTreeReaderValue<vector<float>> jetEt(myReader, "jetEt");
  TTreeReaderValue<vector<float>> jetEta(myReader, "jetEta");
  TTreeReaderValue<vector<float>> jetPhi(myReader, "jetPhi");
  TTreeReaderValue<vector<short>> jetBx(myReader, "jetBx");
  TTreeReaderValue<vector<float>> sumEt(myReader, "sumEt");
  TTreeReaderValue<vector<short>> sumType(myReader, "sumType");
  TTreeReaderValue<vector<float>> sumBx(myReader, "sumBx");

  TTree* t_emu = (TTree*)(f->Get("l1UpgradeEmuTree/L1UpgradeTree"));
  TTreeReader myReader_emu(t_emu);
  TTreeReaderValue<vector<float>> jetEt_emu(myReader_emu, "jetEt");
  TTreeReaderValue<vector<float>> jetEta_emu(myReader_emu, "jetEta");
  TTreeReaderValue<vector<float>> jetPhi_emu(myReader_emu, "jetPhi");
  TTreeReaderValue<vector<short>> jetBx_emu(myReader_emu, "jetBx");
  TTreeReaderValue<vector<float>> sumEt_emu(myReader_emu, "sumEt");
  TTreeReaderValue<vector<short>> sumType_emu(myReader_emu, "sumType");
  TTreeReaderValue<vector<float>> sumBx_emu(myReader_emu, "sumBx");

  TTree* t_evt = (TTree*)(f->Get("l1EventTree/L1EventTree"));
  TTreeReader myReader_evt(t_evt);
  TTreeReaderValue<UInt_t> run(myReader_evt, "run");
  TTreeReaderValue<ULong64_t> event(myReader_evt, "event");
  TTreeReaderValue<UInt_t> lumi(myReader_evt, "lumi");

  double refEt, refEta, refPhi, matchEt, matchEta, matchPhi;

  while (myReader_emu.Next()) {
	  h_all->Fill(1);
	  myReader.Next();
          myReader_evt.Next();
	  refEt = -99.; refEta = -99.; refPhi = -99.; matchEt = -99.; matchEta = -99.; matchPhi = -99.;
	  if (jetEt_emu->size() != 0) { 
		  for (int i = 0; i < jetEt_emu->size(); i ++){
			  if (jetBx_emu->at(i) == 0) { h_emuLeadingJetEt->Fill(jetEt_emu->at(i)); h_emuLeadingJetEta->Fill(jetEta_emu->at(i)); refEt = jetEt_emu->at(i); refEta = jetEta_emu->at(i); refPhi = jetPhi_emu->at(i); break; }
		  }
	  }
	  if (sumEt_emu->size() != 0) {
		  for (int i = 0; i < sumEt_emu->size(); i ++){
			  if(sumBx_emu->at(i) == 0 && sumType_emu->at(i) == 1) { h_emuHT->Fill(sumEt_emu->at(i)); }
			  if(sumBx_emu->at(i) == 0 && sumType_emu->at(i) == 20) { h_emuMHTHF->Fill(sumEt_emu->at(i)); }
		  }
	  }
	  if (jetEt->size() != 0) { 
		  for (int i = 0; i < jetEt->size(); i ++){
			  if (jetBx->at(i) == 0) { h_leadingJetEt->Fill(jetEt->at(i)); h_leadingJetEta->Fill(jetEta->at(i)); break; }
		  }
	  }
	  if (sumEt->size() != 0) {
		  for (int i = 0; i < sumEt->size(); i ++){
			  if(sumBx->at(i) == 0 && sumType->at(i) == 1) { h_HT->Fill(sumEt->at(i)); }
			  if(sumBx->at(i) == 0 && sumType->at(i) == 20) { h_MHTHF->Fill(sumEt->at(i)); }
		  }
	  }
	  if (refEt < 1000.) continue;
	  else {
		  for (int i = 0; i < jetEt->size(); i ++){
			  if(jetBx->at(i) == 0 && jetEta->at(i) == refEta && jetPhi->at(i) == refPhi) { matchEt = jetEt->at(i); matchEta = jetEta->at(i); matchPhi = jetPhi->at(i); }
		  }
		  //std::cout<<refEt<<"\t"<<refEta<<"\t"<<refPhi<<"\t"<<matchEt<<"\t"<<matchEta<<"\t"<<matchPhi<<std::endl;
		  //if(matchEt < 0) std::cout<<*run<<"\t"<<*lumi<<"\t"<<*event<<std::endl;
		  h_emuJetEt->Fill(refEt);
		  h_emuJetEta->Fill(refEta);
		  h_emuJetPhi->Fill(refPhi);
		  h_jetEt->Fill(matchEt);
		  h_jetEta->Fill(matchEta);
		  h_jetPhi->Fill(matchPhi);
	  }
  }

  delete t, t_emu;
  f->Close();
  delete f;

  TFile out(outFile, "RECREATE");
  out.cd();
  h_all->Write();
  h_emuJetEt->Write();
  h_emuLeadingJetEt->Write();
  h_emuLeadingJetEta->Write();
  h_emuJetEta->Write();
  h_emuJetPhi->Write();
  h_emuHT->Write();
  h_emuMHTHF->Write();
  h_jetEt->Write();
  h_leadingJetEt->Write();
  h_leadingJetEta->Write();
  h_jetEta->Write();
  h_jetPhi->Write();
  h_HT->Write();
  h_MHTHF->Write();
  out.Close();
}

int main(int argc, char *argv[])
{
  if(argc > 1)
    {
      calc_jet_rate(argv[1], argv[2]);
    }
  return 0;
}
