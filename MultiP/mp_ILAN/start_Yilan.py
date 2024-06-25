import os
import sys
import glob
from calendar import monthrange
import datetime
import math
from multiprocessing import Process, Pool
import multiprocessing
import natsort
import sys

sta = sys.argv[1]
mode = sys.argv[2]
print(sta)
print(mode)
main_folder = "/home/angela__kang/work/mpitest_ILAN"
data_folder = "/home/angela__kang/work/mpitest_ILAN/Sorted_oneday_ILAN/"

DatePeriod = []
if mode == "1":
    begin = datetime.datetime(2022, 7, 27)
    end = datetime.datetime(2022, 8, 29)
    step = datetime.timedelta(days=1)
 
    while begin <= end:
        DatePeriod.append(begin.strftime('%Y%m%d'))
        begin += step

elif mode == "2":
    begin = datetime.datetime(2022, 8, 29)
    end = datetime.datetime(2022, 10, 2)
    step = datetime.timedelta(days=1)

    while begin <= end:
        DatePeriod.append(begin.strftime('%Y%m%d'))
        begin += step

elif mode == "3":
    begin = datetime.datetime(2022, 10, 2)
    end = datetime.datetime(2022, 11, 5)
    step = datetime.timedelta(days=1)

    while begin <= end:
        DatePeriod.append(begin.strftime('%Y%m%d'))
        begin += step

elif mode == "4":
    begin = datetime.datetime(2022, 11, 5)
    end = datetime.datetime(2022, 12, 9)
    step = datetime.timedelta(days=1)

    while begin <= end:
        DatePeriod.append(begin.strftime('%Y%m%d'))
        begin += step

elif mode == "5":
    begin = datetime.datetime(2022, 12, 9)
    end = datetime.datetime(2023, 1, 12)
    step = datetime.timedelta(days=1)

    while begin <= end:
        DatePeriod.append(begin.strftime('%Y%m%d'))
        begin += step
#------------------------------Separate station groups--------------------------------------------

# sta_list=[]
# sta_list2=[]
# f=open("./stations.csv").readlines()[1:]
# for i in range(len(f)):
#     sta_list.append(f[i].split(",")[0])
# sta_list=sorted(sta_list)

# sta_task=[]
# seg=5   

# index=math.floor(len(sta_list)/seg)
# for i in range(int(seg)+1):
#     if i != int(seg):
#         sta_task.append(sta_list[i*index:index*(i+1)])
#     else:
#         sta_task.append(sta_list[index*seg:])

#-------------------------------------Start multiprocessing----------------------------------------------------

#sta_list=[]
#f=open("./stations.csv").readlines()[1:]
#for i in range(len(f)):
    #sta_list.append(f[i].split(",")[0])
    #for s in range(len(sta_list)):
    #    sta=sta_list[s]
        #print(sta)    
for d in range(len(DatePeriod)):
#    try:

    day_folder = data_folder + DatePeriod[d] + "/" +sta 
    if os.path.isdir(day_folder):
        output_file = day_folder +"/" + DatePeriod[d] + "."+ sta +".asc"
        os.system("cp run_DOP-E_Yilan.cmd " + day_folder+"/")

        f=open(data_folder + DatePeriod[d] + '/'+ sta +'/station_number.txt', 'w')
        f.write(sta+'_'+str(mode))
        f.close()



        if not os.path.isfile(output_file):
            filelist = glob.glob(day_folder+"/"+sta+"*.DPZ.*sps.SAC")
            filelist = natsort.natsorted(filelist)
            for i in range(0,len(filelist)):
                f = filelist[i]
                Zfile = f
                Nfile = f.replace("DPZ","DPN")
                Efile = f.replace("DPZ","DPE")
                if os.path.isfile(Zfile) and os.path.isfile(Zfile) and os.path.isfile(Zfile):
                    print(Zfile)
                    print(Nfile)
                    print(Efile)
                    print("---------------")
                    os.system("cp " + Zfile + " "+sta+'_'+str(mode)+".Z.sac")
                    os.system("cp " + Nfile + " "+sta+'_'+str(mode)+".N.sac")
                    os.system("cp " + Efile + " "+sta+'_'+str(mode)+".E.sac")

                    os.chdir(day_folder)
                    os.system("sh "+day_folder+"/run_DOP-E_Yilan.cmd")
                    os.chdir(main_folder)
                    os.system("rm "+sta+'_'+str(mode)+".Z.sac")
                    os.system("rm "+sta+'_'+str(mode)+".N.sac")
                    os.system("rm "+sta+'_'+str(mode)+".E.sac")
    
            os.system("cp "+sta+'_'+str(mode)+"_output_file.asc " + output_file)
            os.system("rm "+sta+'_'+str(mode)+"_output_file.asc")
            os.system("rm "+sta+'_'+str(mode)+"_azi_dopm.asc")

    #os.system("cp run_DOP-E.cmd " + day_folder)
        else:
            pass
    #print(output_file)
        os.system("cat " + output_file+ " >> " + data_folder + sta+'_mode'+str(mode)+"_total_Yilan_wlen8.asc")
#    except:
#        pass
#print('Station: '+sta+' done')

#-----------------------------------------Just do it!---------------------------------------------
