count="1"
while [ $count -lt 2 ] 
do

echo count $count

line=$(sed -n "${count}p" < filelist.txt)

input_filename=$(echo $line | awk '{print $1}')

sh SubmitToCondor_nano.sh output_eos_${count} MuonJet ${input_filename} /eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_eraC_367095_368823_Golden.json

count=$[$count+1]

done

exit 0
