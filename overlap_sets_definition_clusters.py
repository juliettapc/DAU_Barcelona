#!/usr/bin/env python

'''
Code to read the pickle files for the ad-hoc strategy difinitions and 
the clustering analysis groups, for comparison of overlap. Also to get
age distributions of each

Created by Julia Poncela, on April 2015.

'''

import pickle
from unidecode import unidecode   # to transform whatever unicode special characters into just plain ascii  (otherwise networkx complains)

import histograma_bines_gral
import numpy
from  scipy import stats

def main():
    
  threshold_flag=   "_treshold0.8"   # "_treshold0.8"  or ""


  gral_filename="../Results/dau2014_partition"+threshold_flag+"_Carlos_"
#  gral_filename="../Results/list_"



  Num_clusters=6

#../Results/dau2014_partition_Carlos_rationals.pickle
#../Results/dau2014_partition_treshold0.8_Carlos_rationals.pickle
#../Results/list_rationals.pickle   # mia


  list_lists_def=[]
  list_names=["weirdos","rationals","mostly_def","altruists"]

  file_weirdos=gral_filename+"weirdos.pickle"
  list_weirdos=pickle.load(open(file_weirdos, 'rb'))  
  list_lists_def.append(list_weirdos)

  file_rationals=gral_filename+"rationals.pickle"
  list_rationals=pickle.load(open(file_rationals, 'rb'))  
  list_lists_def.append(list_rationals)

  file_mostly_def=gral_filename+"mostly_def.pickle"
  list_mostly_def=pickle.load(open(file_mostly_def, 'rb'))  
  list_lists_def.append(list_mostly_def)
  
  file_altruists=gral_filename+"altruists.pickle"
  list_altruists=pickle.load(open(file_altruists, 'rb'))  
  list_lists_def.append(list_altruists)

  filename_all="../Results/list_all_users.pickle"
  list_all_users=pickle.load(open(filename_all, 'rb'))  





  print len(list_weirdos)/float(len(list_all_users)), len(list_rationals)/float(len(list_all_users)),len(list_mostly_def)/float(len(list_all_users)),len(list_altruists)/float(len(list_all_users)),len(list_weirdos)/float(len(list_all_users))+ len(list_rationals)/float(len(list_all_users))+len(list_mostly_def)/float(len(list_all_users))+len(list_altruists)/float(len(list_all_users)) , "\n\n"




  for cluster in range(Num_clusters):

   
   
                  
    file_cluster="../Results/Niter_clustering/list_clusters_kmeans"+str(Num_clusters)+"-"+str(cluster+1)+"_109iter.pickle"
    
   
    
  #  file_cluster="../Results/list_clusters_kmeans5_dist_notypes-1.pickle  # the MeV data


    list_current_cluster=pickle.load(open(file_cluster, 'rb'))  

    print "size of cluster",cluster+1, " is",len(list_current_cluster)

    for i in range(len(list_lists_def)):

      list_def=list_lists_def[i]
      name=list_names[i]
      

      intersect=len(list(set(list_def) & set(list_current_cluster)))
      print "intersect between:",name, "and cluster",cluster+1," (of size",len(list_def),") is:", intersect,"  ",  float(intersect)/min(len(list_def), len(list_current_cluster))*100,"%"


    print 


######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

