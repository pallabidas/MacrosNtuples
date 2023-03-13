#!/bin/bash

cd /user/hevard/CMSSW_12_4_8/src/
cmsenv 
cd /user/hevard/CMSSW_12_4_8/src/MacrosNtuples/l1macros/

python3 performances.py --max_events -1 -i $1 -o $2 -c $3

