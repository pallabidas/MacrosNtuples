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

void prefiring(){
   vector<string>* file_list = new vector<string>();
   ifstream all_files;
   all_files.open("filelist.txt");
   while(true){
      string file;
      all_files>>file;
      if(all_files.eof()) break;
      file_list->push_back(file);
   }

   vector<int> bunchlist;
   bunchlist.clear();
   ifstream bunch_file;
   bunch_file.open("bunchlist.txt");
   while(true){
      int firstbunch;
      bunch_file>>firstbunch;
      if(bunch_file.eof()) break;
      bunchlist.push_back(firstbunch);
   }
   std::cout<<bunchlist.size()<<std::endl;

   TFile* outfile = TFile::Open("test.root","recreate");
   TH1F *n1 = new TH1F("nJets","Number of jets",15,0,15);
   TH1F *n2 = new TH1F("nJetTh","Jets passing E_{T} threshold", 5, -0.5, 4.5);
   TH1F *n3 = new TH1F("nJetPre60","Jets passing Pre-trigger threshold 60 GeV", 5, -0.5, 4.5);
   TH1F *n4 = new TH1F("nJetPre90","Jets passing Pre-trigger threshold 90 GeV", 5, -0.5, 4.5);
   TH1F *n5 = new TH1F("nJetPre120","Jets passing Pre-trigger threshold 120 GeV", 5, -0.5, 4.5);
   TH1F *n6 = new TH1F("nJetPre150","Jets passing Pre-trigger threshold 150 GeV", 5, -0.5, 4.5);
   TH1F *n7 = new TH1F("nJetPre180","Jets passing Pre-trigger threshold 180 GeV", 5, -0.5, 4.5);
   TH2F *n8 = new TH2F("EtaPhi","#eta vs #phi of jets passing Pre-trigger threshold", 40, -5, 5, 40, -M_PI, M_PI);

   TH1F *h1 = new TH1F("JetEtbx0","Jet E_{T} at BX = 0", 40, 0, 250);
   TH1F *h2 = new TH1F("JetEtbxm1","Jet E_{T} at BX = -1", 40, 0, 250);
   TH1F *h3 = new TH1F("LeadJetEtbx0","Leading Jet E_{T} at BX = 0", 40, 0, 500);
   TH1F *h4 = new TH1F("LeadJetEtbxm1","Leading Jet E_{T} at BX = -1", 40, 0, 200);
   TH1F *h5 = new TH1F("LeadJetEtbxm2","Leading Jet E_{T} at BX = -2", 40, 0, 200);
   TH1F *h6 = new TH1F("LeadJetEtabx0","Leading Jet #eta at BX = 0", 40, -5, 5);
   TH1F *h7 = new TH1F("LeadJetEtabxm1","Leading Jet #eta at BX = -1", 40, -5, 5);

   TH1F *h8 = new TH1F("nJetHT","Jets sum passing H_{T} threshold", 5, -0.5, 4.5);
   TH1F *h9 = new TH1F("nJetHTPre150","Jets sum passing Pre-trigger H_{T} threshold 150 GeV", 5, -0.5, 4.5);
   TH1F *h10 = new TH1F("nJetHTPre200","Jets sum passing Pre-trigger H_{T} threshold 200 GeV", 5, -0.5, 4.5);
   TH1F *h11 = new TH1F("nJetHTPre250","Jets sum passing Pre-trigger H_{T} threshold 250 GeV", 5, -0.5, 4.5);
   TH1F *h12 = new TH1F("nJetHTPre300","Jets sum passing Pre-trigger H_{T} threshold 300 GeV", 5, -0.5, 4.5);
   TH1F *h13 = new TH1F("nJetHTPre350","Jets sum passing Pre-trigger H_{T} threshold 350 GeV", 5, -0.5, 4.5);
   TH1F *h14 = new TH1F("HTbx0","H_{T} at at BX = 0", 40, 0, 1000.);
   TH1F *h15 = new TH1F("HTbxm1","H_{T} at at BX = -1", 40, 0, 500.);

   float HT0, HTM1;
   float jetEtBx0, jetEtBxM1, jetEtaBx0, jetEtaBxM1, jetPhiBx0, jetPhiBxM1, jetEtBxM2;

   for(int ifile=0; ifile<file_list->size(); ifile++){
      string file = (*file_list)[ifile];
      cout<<"processing "<<file<<endl;
      TFile* f = new TFile(file.data());
      TTree* t1 = (TTree*)(f->Get("l1UpgradeTree/L1UpgradeTree"));
      TTree* t2 = (TTree*)(f->Get("l1EventTree/L1EventTree"));
      t1->AddFriend(t2);

      TTreeReader myReader(t1);
      TTreeReaderValue<UInt_t> test_bx(myReader, "bx");
      TTreeReaderValue<UShort_t> test_nJets(myReader, "nJets");
      TTreeReaderValue<vector<float>> jetEt(myReader, "jetEt");
      TTreeReaderValue<vector<float>> jetEta(myReader, "jetEta");
      TTreeReaderValue<vector<float>> jetPhi(myReader, "jetPhi");
      TTreeReaderValue<vector<short>> jetBx(myReader, "jetBx");

      int count = 0;
      while (myReader.Next()) {
         UInt_t bx = *test_bx; // because we need un-prefirable bunches
         auto firstbx = std::find(begin(bunchlist), end(bunchlist), bx);
         //(firstbx != std::end(bunchlist)) ? cout << "bunchlist contains " << bx <<endl : std::cout << "v does not contain " << bx <<endl;
         if(firstbx == std::end(bunchlist)) continue;

         UShort_t nJets = *test_nJets; 
         HT0 = 0.; HTM1 = 0.;
         jetEtBx0=0.; jetEtBxM1=0.; jetEtaBx0=-99.; jetEtaBxM1=-99.; jetPhiBx0=-99.; jetPhiBxM1=-99.; jetEtBxM2=0.;

         for(int i = 0; i < nJets; i++){
            if(jetBx->at(i) == 0){ 
               h1->Fill(jetEt->at(i));
               HT0 = HT0+jetEt->at(i);
            }
            if(jetBx->at(i) == -1){
               h2->Fill(jetEt->at(i));
               HTM1 = HTM1+jetEt->at(i);
            }
         }
         h14->Fill(HT0);
         h15->Fill(HTM1);

         //HT
         for(int ibin = 0; ibin < 5; ibin++){   //loop over # of thresholds
            float j = 300. + ibin*50.;    //HT thresholds at BX=0
            std::string s = std::to_string(j);
            char const *pchar = s.c_str();
            h8->GetXaxis()->SetBinLabel(ibin+1, pchar);
            h9->GetXaxis()->SetBinLabel(ibin+1, pchar);
            h10->GetXaxis()->SetBinLabel(ibin+1, pchar);
            h11->GetXaxis()->SetBinLabel(ibin+1, pchar);
            h12->GetXaxis()->SetBinLabel(ibin+1, pchar);
            h13->GetXaxis()->SetBinLabel(ibin+1, pchar);
            if(HT0 > j){
               h8->Fill(ibin);   //fill the BX=0 denominator
               float k = 150. + ibin*50.;    //HT thresholds at BX=-1
               if(HTM1 > k){   //fill the BX=-1 numerators
                  h9->Fill(ibin);
                  h10->Fill(ibin);
                  h11->Fill(ibin);
                  h12->Fill(ibin);
                  h13->Fill(ibin);
               }
            }
         }

         //Jet
         for(int i = 0; i < nJets; i++){
            if(jetBx->at(i) == 0 && jetEt->at(i) > jetEtBx0){
               jetEtBx0 = jetEt->at(i);
               jetEtaBx0 = jetEta->at(i);
               jetPhiBx0 = jetPhi->at(i);
            }
            if(jetBx->at(i) == -1 && jetEt->at(i) > jetEtBxM1){
               jetEtBxM1 = jetEt->at(i);
               jetEtaBxM1 = jetEta->at(i);
               jetPhiBxM1 = jetPhi->at(i);
            }
            if(jetBx->at(i) == -2 && jetEt->at(i) > jetEtBxM2){
               jetEtBxM2 = jetEt->at(i);
            }
         }
   
         if(jetEtBx0 > 0.){
            if(jetEtBx0 > 120. && jetEtBxM1 > 60.) n8->Fill(jetEtaBxM1, jetPhiBxM1);
            for(int ibin = 0; ibin < 5; ibin++){   //loop over # of thresholds
               float j = 120. + ibin*30.;    //jet pt thresholds at BX=0
               std::string s = std::to_string(j);
               char const *pchar = s.c_str();
               n2->GetXaxis()->SetBinLabel(ibin+1, pchar);
               n3->GetXaxis()->SetBinLabel(ibin+1, pchar);
               n4->GetXaxis()->SetBinLabel(ibin+1, pchar);
               n5->GetXaxis()->SetBinLabel(ibin+1, pchar);
               n6->GetXaxis()->SetBinLabel(ibin+1, pchar);
               n7->GetXaxis()->SetBinLabel(ibin+1, pchar);
               if(jetEtBx0 > j){
                  n2->Fill(ibin);   //fill the BX=0 denominator
                  float k = 60. + ibin*30.;    //jet pt thresholds at BX=-1
                  if(jetEtBxM1 > k){   //fill the BX=-1 numerators
                     n8->Fill(jetEtaBxM1, jetPhiBxM1);
                     if(jetEtBxM1 > k) n3->Fill(ibin);
                     if(jetEtBxM1 > k) n4->Fill(ibin);
                     if(jetEtBxM1 > k) n5->Fill(ibin);
                     if(jetEtBxM1 > k) n6->Fill(ibin);
                     if(jetEtBxM1 > k) n7->Fill(ibin);
                  }
               }
            }
         }
         if(jetEtBxM1 > 60. ) std::cout<<"jetEtBx0: "<<jetEtBx0<<"\t"<<"jetEtBxM1: "<<jetEtBxM1<<std::endl;
         n1->Fill(nJets);
         h3->Fill(jetEtBx0);
         h4->Fill(jetEtBxM1);
         h5->Fill(jetEtBxM2);
         h6->Fill(jetEtaBx0);
         h7->Fill(jetEtaBxM1);

      }
      h8->Sumw2(); h9->Sumw2(); h10->Sumw2(); h11->Sumw2(); h12->Sumw2(); h13->Sumw2();
      h9->Divide(h8); h10->Divide(h8); h11->Divide(h8); h12->Divide(h8); h13->Divide(h8);
   
      n2->Sumw2(); n3->Sumw2(); n4->Sumw2(); n5->Sumw2(); n6->Sumw2(); n7->Sumw2();
      n3->Divide(n2); n4->Divide(n2); n5->Divide(n2); n6->Divide(n2); n7->Divide(n2);
   
      outfile->cd();
      h1->Write(); h2->Write(); h3->Write(); h4->Write(); h5->Write(); h6->Write(); h7->Write();
      delete h1; delete h2; delete h3; delete h4; delete h5; delete h6; delete h7;
   
      h8->Write(); h9->Write(); h10->Write(); h11->Write(); h12->Write(); h13->Write(); h14->Write(); h15->Write();
      delete h8; delete h9; delete h10; delete h11; delete h12; delete h13; delete h14; delete h15;
   
      n1->Write(); n2->Write(); n3->Write(); n4->Write(); n5->Write(); n6->Write(); n7->Write(); n8->Write();
      delete n1; delete n2; delete n3; delete n4; delete n5; delete n6; delete n7; delete n8;
   
      delete outfile;

      delete t1; delete t2; //delete jetEt; delete jetEta; delete jetPhi; delete jetBx;
      f->Close();
      delete f;
   }
   delete file_list;
   bunchlist.clear();
}

int main(int argc, char *argv[])
{
   prefiring();
   return 0;
}
