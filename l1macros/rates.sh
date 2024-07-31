for variable in L1EmulLeadingJet_pt L1EmulHT L1EmulMHTHF; do

cat>test.C<<EOF
{
  TCanvas *c1 =new TCanvas("c1", " ", 0, 0, 700, 800);

  c1->Range(0, 0, 1, 1);
  c1->SetFillColor(0);
  c1->SetBorderMode(0);
  c1->SetBorderSize(2);
  c1->SetFrameBorderMode(0);
  c1->SetGrid();
  c1->SetLogy();
  c1->Draw();
  gStyle->SetOptStat(0);

  TFile *g1 =TFile::Open("test1.root");
  TH1F *nvtx1 = (TH1F*)g1->Get("h_nvtx");
  int num1 = nvtx1->GetEntries();
  TH1F *h1 = (TH1F*)g1->Get("h_${variable}");
  int nBins = h1->GetSize();
  float xMin = h1->GetBinLowEdge(0);
  float xMax = (h1->GetBinLowEdge(nBins) + h1->GetBinWidth(nBins));
  
  TH1F* ratesHist1 = new TH1F("", "", nBins+2, xMin, xMax);
  ratesHist1->Sumw2();
  int Sum1=0;
  
  for (int i = nBins; i > 0; i--){
          Sum1 += h1->GetBinContent(i);
          ratesHist1->SetBinContent(i, Sum1);
  }
  
  float firstBin1 = ratesHist1->GetBinContent(1);
  ratesHist1->Scale((double) 1.00 / firstBin1);
  ratesHist1->Scale((h1->GetEntries()/num1) * 40.0 * 1000000.0 / 1000.0);
  ratesHist1->GetXaxis()->SetTitle("${variable} [GeV]");
  ratesHist1->GetXaxis()->SetTitleSize(0.045);
  ratesHist1->GetYaxis()->SetTitle("Rate [kHz]");
  ratesHist1->GetYaxis()->SetTitleOffset(1.1);
  ratesHist1->GetYaxis()->SetTitleSize(0.045);
  ratesHist1->SetLineWidth(2.);
  ratesHist1->SetLineColor(kBlack);
  ratesHist1->Draw();

  TFile *g2 =TFile::Open("test2.root");
  TH1F *nvtx2 = (TH1F*)g2->Get("h_nvtx");
  int num2 = nvtx2->GetEntries();
  TH1F *h2 = (TH1F*)g2->Get("h_${variable}");

  TH1F* ratesHist2 = new TH1F("", "", nBins+2, xMin, xMax);
  ratesHist2->Sumw2();
  int Sum2=0;

  for (int i = nBins; i > 0; i--){
          Sum2 += h2->GetBinContent(i);
          ratesHist2->SetBinContent(i, Sum2);
  }

  float firstBin2 = ratesHist2->GetBinContent(1);
  ratesHist2->Scale((double) 1.00 / firstBin1);
  ratesHist2->Scale((h1->GetEntries()/num1) * 40.0 * 1000000.0 / 1000.0);
  ratesHist2->SetLineWidth(2.);
  ratesHist2->SetLineColor(kRed);
  ratesHist2->Draw();
 
  TLegend *legend1 = new TLegend(0.45, 0.68, 0.85, 0.88);
  legend1->SetTextFont(42);
  legend1->SetLineColor(0);
  legend1->SetTextSize(0.04);
  legend1->SetFillColor(0);
  legend1->AddEntry(ratesHist1, "HCAL corr. + 2023 JEC", "l");
  legend1->AddEntry(ratesHist2, "HCAL corr. + JEC with HFZS", "l");
  legend1->Draw();
  
  TLatex *t2a = new TLatex(0.5,0.91," #bf{CMS} #it{Preliminary}         X fb^{-1} (2024E, 13.6 TeV) ");
  t2a->SetNDC();
  t2a->SetTextFont(42);
  t2a->SetTextSize(0.04);
  t2a->SetTextAlign(20);
  t2a->Draw("same");
  
  c1->SaveAs("emulated_rate_${variable}.pdf");

}

EOF

root -l -b -q test.C

rm test.C

done
