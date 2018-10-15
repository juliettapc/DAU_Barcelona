#!/usr/bin/env python

'''
Code to read Carlo's list for the partition into the ad-hoc definitions, and get pickles for them

Created by Julia Poncela, on April 2015

'''

import pickle
import histograma_bines_gral
import numpy
from  scipy import stats

def main():
#1,2,3,4 (resp., rationalPlayers, altruists, defectors, weirds)


    dict_number_type_player={1:"rationals", 2:"altruists",3:"mostly_def",4:"weirdos"}

    #file_name="../Results/dau2014_partition_treshold0.8_Carlos.dat"   # 497 players
    file_name="../Results/dau2014_partition_Carlos.dat"                   # 497 players

    # ojo! estas listas NO incluyen a los que no estan clasificados en ninguna de las 4 def  !!!


    file1=open(file_name,'r')
    list_lines=file1.readlines()
   

    list_rationals=[]
    list_altruists=[]
    list_mostly_def=[]
    list_weirdos=[]

    list_unclassified=[]
    for line in list_lines:                          
        
        list_values_one_line=line.strip("\n").split(" ")  # some files separated by space, not tab
        user_id=int(list_values_one_line[0])
        num_def=int(list_values_one_line[1])
        type_def=dict_number_type_player[num_def]
      #  print user_id, num_def, type_def
     
        if type_def =="rationals":
            list_rationals.append(user_id)

        elif type_def =="altruists":
            list_altruists.append(user_id)

        elif type_def =="mostly_def":
            list_mostly_def.append(user_id)

        elif type_def =="weirdos":
            list_weirdos.append(user_id)
       


    file_name_rationals=file_name.split(".dat")[0]+"_rationals.pickle"
    pickle.dump(list_rationals, open(file_name_rationals, 'wb'))
    print "written", file_name_rationals


    file_name_altruists=file_name.split(".dat")[0]+"_altruists.pickle"
    pickle.dump(list_altruists, open(file_name_altruists, 'wb'))
    print "written", file_name_altruists

    file_name_mostly_def=file_name.split(".dat")[0]+"_mostly_def.pickle"
    pickle.dump(list_mostly_def, open(file_name_mostly_def, 'wb'))
    print "written", file_name_mostly_def

    file_name_weirdos=file_name.split(".dat")[0]+"_weirdos.pickle"
    pickle.dump(list_weirdos, open(file_name_weirdos, 'wb'))
    print "written", file_name_weirdos





######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "
