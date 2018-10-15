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
import bootstrapping
import math

def main():


    num_clusters=6

    for cluster in range(num_clusters):
        #file_cluster="../Results/list_clusters_kmeans"+str(num_clusters)+"_dist_notypes-"+str(cluster+1)+".txt"
                      


        file_cluster="../Results/Niter_clustering/list_clusters_kmeans"+str(num_clusters)+"-"+str(cluster+1)+"_109iter.txt"



        pickle_file_cluster=file_cluster.split("txt")[0]+"pickle"


      
        print file_cluster
        list_users_cluster=[]
        file1=open(file_cluster,'r')
        list_lines=file1.readlines()
        cont=0
        for line in list_lines:                          
            if cont > 0:  # i skip the header
               
                try:
                    list_values_one_line=line.strip("\n").split("	")  
                    user_id=int(list_values_one_line[1])  # field 0 is "original row"

                except IndexError:  # some files are separated by space, not tab
                    list_values_one_line=line.strip("\n").split(" ")  
                    user_id=int(list_values_one_line[1])  # field 0 is "original row"



                H=float(list_values_one_line[2])
                SD=float(list_values_one_line[3])
                SH=float(list_values_one_line[4])
                PD=float(list_values_one_line[5])

                list_users_cluster.append(user_id)
              
            cont +=1
     

        pickle.dump(list_users_cluster, open(pickle_file_cluster, 'wb'))
        print "written pickle:", pickle_file_cluster






######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

