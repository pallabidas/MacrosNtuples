from ROOT import TFile, TH2, TCanvas

infile = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/EGamma/RunC/Test/All.root')

jetetaBins = [0.0, 1.3, 2.5, 3.0, 3.5, 4.0, 5.0]
alphaBins = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50, 1.00]

keys = infile.GetListOfKeys()

ptBalance = []
jetptResponse = []
for key in keys:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       ptBalance.append(histo2D.ProjectionY())
       jetptResponse.append(histo2D.ProfileX())

# To do: For jet pt response histos we need two addtional histos (for each eta region) : alpha<0.3 and alpha<1.0

# Template drawing for the pt balance plots
# To do: style/names/directories etc...
index = 0
for a in range(len(alphaBins)-1):
    for e in range(len(jetetaBins)-1):
       c = TCanvas('alpha=['+str(alphaBins[a])+','+str(alphaBins[a+1])+']' + ' , ' + 'eta=['+str(jetetaBins[e])+','+str(jetetaBins[e+1])+']','Canvas', 1000, 1000 )
       ptBalance[index].SetTitle('p_{T} balance: #alpha=['+str(alphaBins[a])+','+str(alphaBins[a+1])+'], '+' #eta=['+str(jetetaBins[e])+','+str(jetetaBins[e+1])+']')
       ptBalance[index].Draw()
       str_binalpha = "alpha{}to{}".format(alphaBins[a], alphaBins[a+1]).replace(".","p")
       str_bineta = "eta{}to{}".format(jetetaBins[e], jetetaBins[e+1]).replace(".","p")
       c.SaveAs('ptBalance_'+str_binalpha + '_' + str_bineta+'.pdf')
       index += 1

# Template drawing for jet pt response plots
# To do: style/names/directories etc...
index = 0
for a in range(len(alphaBins)-1):
    for e in range(len(jetetaBins)-1):
       c = TCanvas('alpha=['+str(alphaBins[a])+','+str(alphaBins[a+1])+']' + ' , ' + 'eta=['+str(jetetaBins[e])+','+str(jetetaBins[e+1])+']','Canvas', 1000, 1000 )
       jetptResponse[index].SetTitle('jet p_{T} response: #alpha=['+str(alphaBins[a])+','+str(alphaBins[a+1])+'], '+' #eta=['+str(jetetaBins[e])+','+str(jetetaBins[e+1])+']')
       jetptResponse[index].Draw()
       str_binalpha = "alpha{}to{}".format(alphaBins[a], alphaBins[a+1]).replace(".","p")
       str_bineta = "eta{}to{}".format(jetetaBins[e], jetetaBins[e+1]).replace(".","p")
       c.SaveAs('jetptReponse_'+str_binalpha + '_' + str_bineta+'.pdf')
       index += 1
