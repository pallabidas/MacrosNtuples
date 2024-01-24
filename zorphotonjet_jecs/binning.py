from array import array

jetetaBins = [0.0, 1.3, 2.5, 3.0, 3.5, 4.0, 5.0]
alphaBins = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00]
jetptBins = array('f', [20, 35, 50, 65, 85, 115, 150, 200, 300, 500, 1000 ])
ptbalanceBins = array('f',[0.+float(i)/100. for i in range(200)] )
