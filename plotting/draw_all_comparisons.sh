#!/bin/bash

# Code to make comparaison between eras
workdir_arr=( \
    "comparisons/2018Dvs2022E" "comparisons/2018Dvs2022F" "comparisons/2018Dvs2022G" "comparisons/2018DvsAll2022"\
    "comparisons/2022Cvs2022D" "comparisons/2022Dvs2022E" "comparisons/2022Evs2022F" "comparisons/2022Fvs2022G"\
    "comparisons/2022Evs2022G" )
#    "comparisons/MCvs2022E" "comparisons/MCvs2022F" "comparisons/MCvs2022G" "comparisons/MCvsAll2022")

dir_A_arr=( \
    "2018D" "2018D" "2018D" "2018D"\
    "2022RunCv1" "2022RunDv2" "2022RunEv1" "2022RunFv1"\
    "2022RunEv1" )
#    "MonteCarlo" "MonteCarlo" "MonteCarlo" "MonteCarlo")

dir_B_arr=( \
    "2022RunEv1" "2022RunFv1" "2022RunGv1" "all_2022"\
    "2022RunDv2" "2022RunEv1" "2022RunFv1" "2022RunGv1"\
    "2022RunGv1" )
#    "2022RunEv1" "2022RunFv1" "2022RunGv1" "all_2022")

suffix_A_arr=(\
    "2018D" "2018D" "2018D" "2018D"\
    "2022C" "2022D" "2022E" "2022F"\
    "2022E" )
#    "MC" "MC" "MC"\ "MC")

suffix_B_arr=(\
    "2022E" "2022F" "2022G" "2022(all)"\
    "2022D" "2022E" "2022F" "2022G"\
    "2022G" )
#    "2022E" "2022F" "2022G" "2022(all)")

l=$((${#workdir_arr[@]}-1))

for i in $(seq 0 $l)
do
    echo ${workdir_arr[$i]} ${dir_A_arr[$i]} ${dir_B_arr[$i]} ${suffix_A_arr[$i]} ${suffix_B_arr[$i]} 
    ./make_mu_comparisons.sh ${workdir_arr[$i]} ${dir_A_arr[$i]} ${dir_B_arr[$i]} ${suffix_A_arr[$i]} ${suffix_B_arr[$i]}
    ./make_eg_comparisons.sh ${workdir_arr[$i]} ${dir_A_arr[$i]} ${dir_B_arr[$i]} ${suffix_A_arr[$i]} ${suffix_B_arr[$i]}
    ./make_jets_comparisons.sh ${workdir_arr[$i]} ${dir_A_arr[$i]} ${dir_B_arr[$i]} ${suffix_A_arr[$i]} ${suffix_B_arr[$i]}
    ./make_etsum_comparisons.sh ${workdir_arr[$i]} ${dir_A_arr[$i]} ${dir_B_arr[$i]} ${suffix_A_arr[$i]} ${suffix_B_arr[$i]}
done
