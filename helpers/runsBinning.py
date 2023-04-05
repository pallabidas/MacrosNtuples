import json

def runbinning():
    '''Creates a dynamic binning on run number, based on runs in a JSON file, such that each run in the file is one bin and intervals between runs are merged into a single bin'''
    goodrunsandlumisections = {}
    with open('../json_csv_files/Cert_Collisions2016to2022_273158_357900_Golden.json', 'r', encoding='utf-8') as f_goodlumi:
        goodrunsandlumisections = json.load(f_goodlumi)
        
    runs_sorted = []
    for run in goodrunsandlumisections:
        runs_sorted.append(float(run))
    runs_sorted.sort()

    binsforrunnb = []
    for i, run in enumerate(runs_sorted):
        if i == 0:
            binsforrunnb.append(0.)
            binsforrunnb.append(1.)
        binsforrunnb.append(run)
        if i == len(runs_sorted)-1:
            binsforrunnb.append(run+1)
            binsforrunnb.append(363000)
        else:
            if runs_sorted[i+1] != run+1:
                binsforrunnb.append(run+1)

    return binsforrunnb

