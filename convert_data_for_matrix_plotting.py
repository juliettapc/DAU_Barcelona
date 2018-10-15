#!/usr/bin/env python

'''
Code to read the pickle file with the raw data from the DAU experiments,
and make it into a csv file.

Created by Julia Poncela, on December 2014.

'''

import pickle
from unidecode import unidecode   # to transform whatever unicode special characters into just plain ascii  (otherwise networkx complains)

import histograma_bines_gral
import numpy
from  scipy import stats

def main():

    reverse_flag=0  # depending on the ordering of the data, it inverts the representation...  (try and error)




   # name0="../Results/ST_replicator_simus.dat" # ojo!!! en este archivo esta primero la S y luego la T!!!!!!!!!!

#    name0="../Results/Ratio_Cooperation_TSplane_genders.dat"
    #name0="../Results/Ratio_Cooperation_TSplane_rounds_4_10_div_11_18.dat"
    name0="../Results/Diff_relat_Cooperation_TSplane_rounds_4_10_div_11_18.dat"


    file0=open(name0,'r')
    list_lines=file0.readlines()
    
    dict_TSplane_avg_coop={}
   
   

    for line in list_lines:
        print line
        try:
            list_elements=line.strip("\n").split(" ")


            if name0=="../Results/ST_replicator_simus.dat":
                T=int(list_elements[1])# ojo!!! en este archivo esta primero la S y luego la T!!!!!
                S=int(list_elements[0])    

            else:   
                T=int(list_elements[0])
                S=int(list_elements[1])   


            avg_coop=float(list_elements[2])
            punto_TS=(T,S)
            
            dict_TSplane_avg_coop[punto_TS]=avg_coop
           
        except: 
          pass


    print_values_dict_for_matrix_plotting(dict_TSplane_avg_coop, name0,reverse_flag)
    
  



######################################

######################################


def print_values_dict_for_matrix_plotting(dict_TSplane_avg_values, filename, reverse_flag):

    filename=filename.split(".dat")[0]+"_MATRIX.dat"
    output= open(filename,'wt')

 


    list_T_values=[]
    list_S_values=[]
    for key in dict_TSplane_avg_values:
        T=key[0]
        S=key[1]

        if T not in list_T_values:
            list_T_values.append(T)
        if S not in list_S_values:
            list_S_values.append(S)

    listT=sorted(list_T_values)
 
    listS=sorted(list_S_values)


    if reverse_flag== 1:
        listT.reverse()        
        listS.reverse()
        
    for T in listT:
        for S in listS:
            tupla=(T,S)
            try:
                print >> output, dict_TSplane_avg_values[tupla],
                           

            except KeyError:
                pass
        print  >> output
        

    output.close()
    print "written matrix file:", filename




######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

