reset
set pm3d 
set pm3d map
set palette rgbformulae 22,13,-31   # rainbow
#set palette defined (0. "blue",0.1 "green", 0.15 "yellow", 0.2 "orange",0.3 "red")
#set cbrange[0.025:0.075]  # color bar
#set cbtics (0.025,0.05,0.075)   # number tics

sp [5:15][0:10]"../Results/Payoff_norm_TSplane_All_ages_rounds11_15.dat"   u 1:2:3
set xlabel "T"  
set ylabel "S"
set size square
unset key
rep

set term post enhanced color solid 26
set output "../Results/payoff_norm_TS_All_users_rounds_11_15.eps"
rep
set output
set term x11

