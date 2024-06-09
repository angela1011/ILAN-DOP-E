#!/bin/sh
gmt_dir=/raid1/PLOTDATA
range=121.46/121.9/24.45/24.9
well="well_all_loc_2.csv"
#Main map
gmt begin TW_MAP png
    gmt basemap -R$range -JM15c -BWSne+t"Study Area" -Bxaf+l"Longitude" -Byaf+l"Latitude" 
    #gmt coast -R121.46/121.9/24.5/24.9 -JM12c -Baf -BWSne -W0.5p -A10000 -Glightbrown -Sazure1 --FORMAT_GEO_MAP=dddF
    gmt grdimage @earth_relief_01s -R$range -I+d -CGray
    gmt plot $gmt_dir/TW_city_boundary.txt -W0.5,black 
    gmt psxy taiwan_river_mainstream.gmt -R$range -W0.5p,lightblue
    gmt coast -R$range -W0.2 -Slightblue -B1 -Df #-Ia/1.5p,lightblue 
    awk '{print$2,$3}' stalst_ILAN | gmt plot -St0.35 -W0.05 -Ggold
    awk '{print$2,$3}' stalst_HCL | gmt plot -St0.1 -W0.01 -Gchocolate
    awk -F, '{print$3,$4}' ${well}  | gmt plot -Ss0.1c -W0.01 -Gseagreen3
    # awk '{print $1,$2}' Vs.txt | gmt plot -Sa0.1 -W0.01 -Gred
    awk '{print$2,$3,$1}' stalst_ILAN  | gmt text -F+f5p,0.01,black -Y-0.2 -W0.01 -Gwhite
    # gmt plot $gmt_dir/TW_city_boundary.txt -W0.5,black -Y+0.2
    

    gmt inset begin -DjBL+w2.5c/3.5c+o0.1c -F+gwhite+p1p -Y+0.1
    gmt coast -R119.5/122.5/21.5/25.5 -W0.1p -A10000 -Glightbrown -Sazure1 -Ia/0.03p,lightblue 
    gmt psxy $gmt_dir/TW_city_boundary.txt -W0.03,black 
    gmt psxy $gmt_dir/fault.dat -W0.15,red
        echo 121.46 24.45 121.9 24.9 | gmt plot -Sr+s -W0.5p,blue
    gmt inset end
gmt end 
