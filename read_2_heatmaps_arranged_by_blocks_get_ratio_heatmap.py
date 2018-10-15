#!/usr/bin/env python

'''
Code to read two heatmaps (file formated as blocks of lines, NOT matrix), 
and calculate their ratio


Created by Julia Poncela, on September 2015

'''

import pickle
from unidecode import unidecode   # to transform whatever unicode special characters into just plain ascii  (otherwise networkx complains)
import datetime as dt
import histograma_bines_gral
import histograma_gral
import numpy
from  scipy import stats
import networkx as nx
import itertools
#from progressbar import ProgressBar


def main():




    ######## input files for the comparison
   # filename1="../Results/Cooperation_TSplane_gender_1.dat"    #columns:   T  S  <Coop>  STD
    #filename2="../Results/Cooperation_TSplane_gender_0.dat"


    #filename1="../Results/Cooperation_TSplane_All_ages_rounds1_3.dat"
    filename1="../Results/Cooperation_TSplane_All_ages_rounds4_10.dat"
    filename2="../Results/Cooperation_TSplane_All_ages_rounds11_18.dat"




    #filename1="../Results/Cooperation_TSplane_young_ages.dat"
    #filename2="../Results/Cooperation_TSplane_adult_ages.dat"



    print "comparing files:"
    print "  ", filename1
    print "  ", filename2
    



    ####### output ratio file
    if "gender" in filename1:
        filename_ratio="../Results/Ratio_Cooperation_TSplane_genders_1_div_0.dat"
        filename_diff_relat="../Results/Diff_relat_Cooperation_TSplane_genders_1_div_0.dat"


    elif "ages.dat" in filename1:
        filename_ratio="../Results/Ratio_Cooperation_TSplane_ages_young_div_adult.dat"
        filename_diff_relat="../Results/Diff_relat_Cooperation_TSplane_ages_young_div_adult.dat"

    elif "round" in filename1:
        filename_ratio="../Results/Ratio_Cooperation_TSplane_rounds_"+filename1.split("rounds")[1].split(".")[0]+"_div_"+filename2.split("rounds")[1].split(".")[0]+".dat"
        filename_diff_relat="../Results/Diff_relat_Cooperation_TSplane_rounds_"+filename1.split("rounds")[1].split(".")[0]+"_div_"+filename2.split("rounds")[1].split(".")[0]+".dat"

    else:
        exit()

    file_ratio=open(filename_ratio, 'wt')
    file_diff_relat=open(filename_diff_relat, 'wt')


    print filename_ratio
    print filename_diff_relat





    ####### i read file1 and save it
    dict_file1_avg={}
    dict_file1_std={}
   
    list_order_tuplas=[]
    file1=open(filename1,'r')    
    for line_aux in file1:  # ASI LEO LINEA POR LINEA,EN LUGAR DE CARGARLAS  TODAS EN MEMORIA PRIMERO (en lugar de:  for line in list_lines )!!  
        try:
            line=line_aux.split(" ")           
            T=line[0]
            S=line[1]
            tupla=(T, S)
            list_order_tuplas.append(tupla)

            avg_Coop=line[2]
            std_Coop=line[3]
            
            dict_file1_avg[tupla]=float(avg_Coop)
            dict_file1_std[tupla]=float(std_Coop)
        except IndexError: # empty line
             list_order_tuplas.append(" ")


  

   
    ####### i read file2 and save it
    dict_file2_avg={}
    dict_file2_std={}

    file2=open(filename2,'r')   
    for line_aux in file2:    
        try:
            line=line_aux.split(" ")
           
            T=line[0]
            S=line[1]
            tupla=(T, S)
            
            avg_Coop=line[2]
            std_Coop=line[3]
            
            dict_file2_avg[tupla]=float(avg_Coop)
            dict_file2_std[tupla]=float(std_Coop)
        except IndexError: # empty line
            pass


    list_ratios=[]

    ######### i print out the ratio file with the same block structure
    for tupla in list_order_tuplas:
        if tupla != " ":  # i added a space arificially to separate blocks
            ratio=dict_file1_avg[tupla]/dict_file2_avg[tupla]

            diff_relat=(dict_file1_avg[tupla]-dict_file2_avg[tupla])/dict_file2_avg[tupla]


         #   print tupla[0], tupla[1], dict_file1_avg[tupla], dict_file2_avg[tupla], "  ratio:",ratio
            print   >> file_ratio, tupla[0], tupla[1], ratio
            print   >> file_diff_relat, tupla[0], tupla[1], diff_relat

            list_ratios.append(ratio)
            list_ratios.append(diff_relat)

        else:          
            print   >> file_ratio
            print   >> file_diff_relat


         
       
      

    print "written file:",filename_ratio
    print "written file:",filename_diff_relat


    if "gender" in filename1:
        name_h="../Results/histogram_Ratios_Cooperation_TSplane_genders_1_div_0.dat"
    elif "ages.dat" in filename1:
        name_h="../Results/histogram_Ratios_Cooperation_TSplane_ages_young_div_adult.dat"
    elif "round" in filename1:
        name_h="../Results/histogram_Ratios_Cooperation_TSplane_rounds_"+filename1.split("rounds")[1].split(".")[0]+"_div_"+filename2.split("rounds")[1].split(".")[0]+".dat"

    histograma_bines_gral.histograma_bins(list_ratios,20, name_h)


######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

