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

main_folder = "/PATH/DOP-E/Measurement"
data_folder = "/PATH/DOP-E/Measurement/ILAN_array/"

begin = datetime.datetime(YY, MM, DD)
end = datetime.datetime(YY, MM, DD)
step = datetime.timedelta(days=1)

DatePeriod = []
while begin <= end:
    DatePeriod.append(begin.strftime('%Y%m%d'))
    begin += step

print(DatePeriod)
#------------------------------Separate station groups--------------------------------------------

sta_list=[]
sta_list2=[]
f=open("./station_name_list").readlines()[:]
for i in range(len(f)):
    sta_list.append(f[i].split(" ")[0])
sta_list=sorted(sta_list)

sta_task=[]
seg=10   

index=math.floor(len(sta_list)/seg)
for i in range(int(seg)+1):
    if i != int(seg):
        sta_task.append(sta_list[i*index:index*(i+1)])
    else:
        sta_task.append(sta_list[index*seg:])

#-------------------------------------Start multiprocessing----------------------------------------------------

def Start_multiprocess(sta_list):
    for s in range(len(sta_list)):
        sta=sta_list[s]  

        for d in range(len(DatePeriod)):
            print(DatePeriod[d])
            f=open(data_folder + DatePeriod[d] + '/'+ sta +'/station_number.txt', 'w')
            f.write(sta)
            f.close()

            day_folder = data_folder + DatePeriod[d] + "/" +sta 
            output_file = day_folder +"/" + DatePeriod[d] + "."+ sta +".asc"
            os.system("cp run_DOP-E_Yilan.cmd " + day_folder+"/")

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
                        os.system("cp " + Zfile + " "+sta+".Z.sac")
                        os.system("cp " + Nfile + " "+sta+".N.sac")
                        os.system("cp " + Efile + " "+sta+".E.sac")

                        os.chdir(day_folder)
                        os.system("sh ./run_DOP-E_Yilan.cmd")
                        os.chdir(main_folder)
                        os.system("rm "+sta+".Z.sac")
                        os.system("rm "+sta+".N.sac")
                        os.system("rm "+sta+".E.sac")
            
                os.system("cp "+sta+"_output_file.asc " + output_file)
                os.system("rm "+sta+"_output_file.asc")
                os.system("rm "+sta+"_azi_dopm.asc")

                os.system("cp run_DOP-E.cmd " + day_folder)
            else:
                pass
            print(output_file)
            os.system("cat " + output_file+ " >> " + data_folder + sta+"_total_Yilan_wlen8.asc")
        print('Station: '+sta+' done')

#-----------------------------------------Just do it!---------------------------------------------
pool = multiprocessing.Pool(processes= seg+1)
result = pool.map(Start_multiprocess, sta_task)