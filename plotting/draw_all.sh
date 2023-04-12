#!/bin/bash
lumi_file=lumis/2023Mar29.txt

for dir in "2022RunCv1" "2022RunDv1" "2022RunDv2" "2022RunEv1" "2022RunFv1" "2022RunGv1" "all_2022" "2018D"
do
    case $dir in
        2022Run?v?)
            lumi=`awk -v d=$dir -F ' ' '{if ( $0 ~ d ){ printf "%.1f\n", $2 }}' $lumi_file`
            ;;

        all_2022*)
            lumi=`awk 'BEGIN{ sum = 0 } /2022/ { sum += $2 } END{ printf "%.1f\n", sum }' $lumi_file`
            #lumi="34"
            ##echo $dir $lumi
            ;;

        2018D)
            lumi=`awk -v d=$dir -F ' ' '{if ( $0 ~ d ){ printf "%.1f\n", $2 }}' $lumi_file`
            ;;
        *)
            lumi="X"
            ;;
    esac
    echo $dir
    ./make_mu_plots.sh $dir $lumi
    ./make_eg_plots.sh $dir $lumi
    ./make_jets_plots.sh $dir $lumi
    ./make_etsum_plots.sh $dir $lumi

    for nvtx in "_nvtx10to20" "_nvtx20to30" "_nvtx30to40" "_nvtx40to50" "_nvtx50to60"
    do
        echo $dir$nvtx
        ./make_mu_plots.sh $dir $lumi $nvtx
        ./make_eg_plots.sh $dir $lumi $nvtx
        ./make_jets_plots.sh $dir $lumi $nvtx
        ./make_etsum_plots.sh $dir $lumi $nvtx
    done
done 
