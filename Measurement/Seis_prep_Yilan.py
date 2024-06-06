import obspy
import os
from obspy.io.xseed import Parser
from obspy import UTCDateTime
from obspy.signal.invsim import corn_freq_2_paz
from obspy.io.sac.sacpz import attach_paz
from multiprocessing import Process, Pool
import math
import multiprocessing
import datetime
#------------------------------------------------------------------------------------
data_folder="./Sorted_oneday_ILAN_array/"

nsp=7200 #nsp in run_DOP-E.cmd
downsamp_rate=20.0
n=int(86400*downsamp_rate/nsp) 
dt=float(86400/n)

#ori_date=UTCDateTime("2022-07-27 T00:00:00")
begin = datetime.datetime(2022, 11, 20)
end = datetime.datetime(2023, 1, 12)
step = datetime.timedelta(days=1)
DatePeriod = []

while begin <= end:
    DatePeriod.append(begin.strftime('%Y%m%d'))
    begin += step

print(DatePeriod)

#-----------------------Read PZ files-------------------------------------
sensitivity_resp = 306846
corner_freq = 5
damping = 0.7
gain = 1
pre_filt = (0.05, 0.1, 110, 125)
paz_1hz=corn_freq_2_paz(corner_freq, damp=damping)
paz_1hz['sensitivity'] = sensitivity_resp
paz_1hz['gain'] = gain

#-------------------------------Multiprocessing settings-----------------------------------
sta_list=[]

f=open("./stalst_ILAN").readlines()[:]
for i in range(len(f)):
    sta_list.append(f[i].split(" ")[0])
sta_list=sorted(sta_list)

sta_task=[]
seg=30
index=math.floor(len(sta_list)/seg)
for i in range(int(seg)+1):
    if i != int(seg):
        sta_task.append(sta_list[i*index:index*(i+1)])
    else:
        sta_task.append(sta_list[index*seg:])
print(sta_task)
sta_list=[]
#----------------------------Strat SAC preprocessing-----------------------------

def Start_preprocess(sta_list):
    for d in range(len(DatePeriod)):
        date=DatePeriod[d]
        year=date[0:4]
        month=date[4:6]
        day=date[6:8]
        my_date = datetime.datetime.strptime(date, '%Y%m%d')
        juliand = my_date.strftime('%j') # '312'

        for s in range(len(sta_list)):
            sta=sta_list[s]
            print(sta)
            sta_dir=data_folder+DatePeriod[d]+"/"+sta+"/"
            data0=sta_dir+sta+".FM.00.DPE."+year+"."+juliand+"."+date+".SAC"
            data1=sta_dir+sta+".FM.00.DPN."+year+"."+juliand+"."+date+".SAC"
            data2=sta_dir+sta+".FM.00.DPZ."+year+"."+juliand+"."+date+".SAC"
            #Check 3 components all exist
            if os.path.isfile(data0) and os.path.isfile(data1) and os.path.isfile(data2):

                #Read, detrend and demean
                st=obspy.read(sta_dir+sta+".FM*DP*.SAC")
                begin_time=st[0].stats.starttime

                #Correct to consistent start time
                st.trim(begin_time, begin_time+86400.0,pad=True, fill_value=0)
                st.taper(0.05)
                st.detrend("linear")
                st.detrend("demean")
                
                chan1 = st[0].stats.channel
                chan2 = st[1].stats.channel
                chan3 = st[2].stats.channel

                #Remove instrument response
                attach_paz(st[0], './Yilan_info/PZs/'+chan1)
                attach_paz(st[1], './Yilan_info/PZs/'+chan2)
                attach_paz(st[2], './Yilan_info/PZs/'+chan3)

                st.simulate(paz_remove=paz_1hz, pre_filt=pre_filt)

                #Band-pass filter for resample (freqmax=resample)
                st.filter("bandpass",freqmin=0.01, freqmax=50.0,corners=4)
                st.resample(downsamp_rate)

                #Trim daily data into several parts
                for i in range(n):
                        st2 = st.copy()
                        chan1 = st2[0].stats.channel
                        chan2 = st2[1].stats.channel
                        chan3 = st2[2].stats.channel
                        st2.trim(begin_time,begin_time+dt,pad=True, fill_value=0)
                        st2[0].write(sta_dir + sta +"."+ chan1 +"."+ str(i) +"sps.SAC")
                        st2[1].write(sta_dir + sta +"."+ chan2 +"."+ str(i) +"sps.SAC")
                        st2[2].write(sta_dir + sta +"."+ chan3 +"."+ str(i) +"sps.SAC")

                        begin_time = begin_time + dt                
                print('Station: '+sta+' done')
            else:
                pass
                print("N")

pool = multiprocessing.Pool(processes= seg + 1)
result = pool.map(Start_preprocess, sta_task)
