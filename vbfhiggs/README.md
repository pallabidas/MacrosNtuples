# Script for basic
## Introduction 

The script ```hinvchecks.py``` currently does two types of simple studies;

- ```GEN``` study: makes histograms of basic kinematic distributions (MET, mjj, ...) using gen level information. 
- ```L1``` study: study a set of L1 seeds targeting the VBF jets for the VBF -> Higgs process, with various thresholds on the leading/subleading jet, invariant mass, pseudorapidity/phi separation, and creates, for each a pass/fail histogram. 

At the moment the ```GEN``` study requires NANOAOD while the ```L1``` study requires a customized ntuple format (produced) with this code: 

https://github.com/iihe-cms-sw/GenericTreeProducerMINIAOD

## Running the code

```python3 hinvchecks.py -i INPUTFILE -o OUTPUTFILE -s STUDY -f DATAFORMAT``` 