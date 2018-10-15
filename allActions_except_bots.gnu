#!/usr/bin/gnuplot

set terminal postscript enhanced color eps size 3,3.5
set out "Dau2014_Cooperation_Overall.eps"
#set multiplot

set rmargin 2
set lmargin 2
set tmargin 2
set bmargin 2

set palette defined (0 "blue", 1 "red")

#set xtics 0.5
#set ytics 0.5
#set ztics 20

set xlabel "T"
set ylabel "S"
#set cblabel "C"

set view map
#set size ratio .9

#set object 1 rect from graph 0, graph 0 to graph 1, graph 1 back
#set object 1 rect fc rgb "black" fillstyle solid 1.0

#set origin 0.1,0.735
set size 1.1,1
#set label 10 at graph 0.245, graph 1.1 LABEL #front center
set yrange[-1:11]
set xrange[4.:16.]
set cbrange[0.:1.]

splot '../Results/Cooperation_TSplane_All_ages_rounds1_18.dat' using 3:2:1 with points palette pointsize 5  pointtype 5 notitle
#unset label

