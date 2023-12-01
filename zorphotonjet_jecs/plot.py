from ROOT import TFile, TH2, TCanvas

infile = TFile('Test_2022C_JMENano_Photon.root')

jetEtaBins = [0.0, 1.3, 2.5, 3.0, 3.5, 4.0, 5.0]
keys = infile.GetListOfKeys()

histo1DProjY = []
for key in keys:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
#        print(key.GetName()) 
        histo1DProjY.append(histo2D.ProjectionY())

for index, histo in enumerate(histo1DProjY):
    c = TCanvas('eta=['+str(jetEtaBins[index])+','+str(jetEtaBins[index+1])+']','Canvas', 800, 800 )
    histo.SetTitle('p_{T} balance: #eta=['+str(jetEtaBins[index])+','+str(jetEtaBins[index+1])+']')
    histo.Draw();    
    str_bineta = "eta{}to{}".format(jetEtaBins[index], jetEtaBins[index+1]).replace(".","p")
    c.SaveAs(str_bineta+'.pdf')
