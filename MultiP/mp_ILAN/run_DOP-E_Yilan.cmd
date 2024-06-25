#!/bin/sh
# schimmel@ictja.csic.es
#==============================================#
#
#################################
#   PROVIDE 3-C data (SAC files): 
#################################
sta=$(cat ./station_number.txt)
echo ${sta}
Z=${sta}.Z.sac
N=${sta}.N.sac
E=${sta}.E.sac


##############################
#   SET PARAMETERS FOR POLFRE:
##############################
##### DOP power:
pow=3
#pow=3     # 3
##### freq. dependent stability window for DOP:
#wlen=17
wlen=8
##### minimum DOP:
dopm=0.75   # 0.75
#dopm=0.75
##### Gauss window for ST: cycle*T=2*std
cycle=1  #1
##### frequency range:
#f1=0.033   
f1=0.2
#f2=0.5   	
f2=9.8

##### neighbouring frequencies to average: 2+nflen+1:
nflen=2     #2
##### numb. of frequencies in band f1-f2:
nfr=100  
#nfr=50
#nfr=20
##### max number samples to process:
#nsp=32000
nsp=7200
#nsp=100
#nsp=8192
##### average spectral matrix rather than spectra (keep as it is):
ave=ave
##### frequencies are spaced on a log scale (default is linear)
#flog=flog

 
par1=" wlenf="$wlen" pow="$pow" "$ave" dopm="$dopm" nsp="$nsp" "
par2=" f1="$f1" f2="$f2" nflen="$nflen" cycle="$cycle" nfr="$nfr""

echo $Z $N $E
#############
# EXECUTE PG
#############
cd /home/angela__kang/work/mpitest_ILAN
rm -f ${sta}_azi_dopm.asc
/home/angela__kang/work/mpitest_ILAN/bin/DOP-E_v1.2 $Z $N $E $par1 $par2 hv wdeg=10 zdeg=10
cat ${sta}_azi_dopm.asc >> ${sta}_output_file.asc


exit






