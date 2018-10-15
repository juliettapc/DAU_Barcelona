#!/usr/bin/gnuplot

reset


set size square
set datafile missing 'nan'



#set title 'Males'  # Altruists   Rationals     Mostly defectors    Weirdos  

set border linewidth 0
unset key

set cbrange[-1.:1]  # color bar
#set cbrange[0.01:0.08]  # color bar
#set cbrange[-15:5]  # color bar      #values for avg_coop

#set cbrange[0.0:100]  # color bar
   
#set palette rgbformulae 22,13,-31


   
   set palette defined ( -1. "red", 0. "green",  1. "red")    # type in the gnuplot terminal: show colornames
#set palette defined ( 0 "black",  100 "yellow" )    # type in the gnuplot terminal: show colornames


set xrange [-0.5:10.5]			      
set yrange [-0.5:10.5]   # con esto ademas quito el reborde exterior grande


#unset colorbox  ###### unset to  hide colorbar


set xlabel "T"
set ylabel  "S"





#plot '../Results/Cooperation_TSplane_All_ages_rounds1_18_gender1_MATRIX.dat' matrix with image
#plot '../Results/Numer_actions_TSplane_All_ages_rounds1_18_genderAll_MATRIX.dat' matrix with image
     
#plot '../Results/ST_replicator_simus_MATRIX.dat' matrix with image
#plot '../Results/Ratio_Cooperation_TSplane_ages_young_div_adult_MATRIX.dat' matrix with image
plot '../Results/Diff_relat_Cooperation_TSplane_rounds_4_10_div_11_18_MATRIX.dat' matrix with image



   
set term post enhanced color solid 26

   
#set output "../Results/Number_of_actions_TSplane.eps"
set output "../Results/Diff_relat_Cooperation_TSplane_rounds_4_10_div_11_18.eps"

rep
set output
set term x11




######
######
   
###plot '../Results/Cooperation_TSplane_altruists_MATRIX.dat' matrix with image
###plot '../Results/Cooperation_TSplane_All_ages_rounds1_18_MATRIX.dat' matrix with image
###   plot '../Results/Cooperation_TSplane_clusters6_6_kmeanspython_MATRIX.dat' matrix with image