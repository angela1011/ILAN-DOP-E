#!/bin/bash
#PBS -l nodes=1:ppn=48
#PBS -N period4_node9
#PBS -o period4_node9_output
#PBS -e period4_node9_error

# Change to the directory where your Python script is located
#cd /data/paui0615/TEST
#cd /home/angela__kang/work/Example-DOP-E/Measurement/mpitest
cd /home/angela__kang/work/mpitest_ILAN
echo "Running on node: $(hostname)"

# Print PBS-related environment variables
echo "PBS_NODEFILE: $PBS_NODEFILE"
echo "PBS_JOBID: $PBS_JOBID"

echo "Number of cores per node: $PBS_NUM_PPN"
echo "Number of nodes: $PBS_NUM_NODES"
# Activate your Python environment if necessary
# source activate your_environment
file_path="node9"

# Read the first column from the CSV file and store the values in a list
#values=($(head -n 10 "$file_path" | cut -d ' ' -f 1))
values=($(cat "$file_path" | cut -d ' ' -f 1))
#values=($(cut -d ',' -f 1 "$file_path"))

i=0
for argument in "${values[@]}"
do
    start_core=$i
    mpirun -np 1 python ./start_Yilan.py $argument 4 &

    ((i++))
    echo $argument
done
wait

#day_list=[]
#listf=date.list
#for fn in `cat $listf`
#do
#evf1=$node1
#evf2=$node2
#for line1 in `cat $evf1
#lines =open("./date.list").readlines()
#for i in range(len(lines)):
#    day_list.append(lines[i].split()[0])
#    date_list = day_list[i]
#    #print(day_list)

# listf=date.list
# for line in `cat $listf | gawk '{print $1}'`
# do
# evf1=$node1
# evf2=$node2
#     if [ $line -gt 20220727 ] && [ $line -le 20221019 ]
#     then
#         node1=`echo $line` 
#         #echo $mode1
#         elif [ $line -gt 20221019 ]
#         then
#             node2=`echo $line`
#             #echo $mode2
#         fi
# done

# #mpitest.py [station] 1
# if argument == 1:
#     if folder name <= 20221019:
#     ./node1
