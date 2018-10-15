#!/usr/bin/env python


'''
Code to validate the clustering scheme obtained by kmeans

Created by Julia Poncela, on April 2015.

'''

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import Imputer
import histograma_gral
import sklearn
import random


def main():
        
    




  type_data="actual"#"actual"   or   "random"


    ####### input files
  if type_data=="actual" :      
        data_file='../Results/DAU_data_for_Jordi_kmeans.dat'
  elif type_data=="random" :
              data_file='../Results/DAU_for_cluster_analysis_by_quadrants_and_groupsSminusT_random_total.dat'



    ######### i read the csv  file:  (all columns)
  data = []   # list of dictionaries: one dict per user
  
  with open(data_file, 'r') as infile:
        count = 0
        for line in infile:
            count += 1
            if count == 1: continue   # i skip the header

            parts = line.strip().split(' ')
            if type_data=="actual" :
                data.append({'user_id' : parts[0],
                         'H' : parts[1],
                         'SD' : parts[2],
                         'SH' : parts[3],
                         'PD' : parts[4],
                         'higherH' : parts[5],
                         'lowerH' : parts[6],
                         'higherPD' : parts[7],
                         'lowerPD' : parts[8],
                         'S-T[-15,-10)' : parts[9],
                         'S-T[-10,-5)' : parts[10],
                         'S-T[-5,0)' : parts[11],
                         'S-T[0,5]' : parts[12],
                         'type_player' : parts[13]})


            elif type_data=="random" :
                data.append({'user_id' : parts[0],
                         'H' : parts[1],
                         'SD' : parts[2],
                         'SH' : parts[3],
                         'PD' : parts[4],                        
                         'S-T[-15,-10)' : parts[5],
                         'S-T[-10,-5)' : parts[6],
                         'S-T[-5,0)' : parts[7],
                         'S-T[0,5]' : parts[8],
                         'type_player' : parts[9],
                         'type_player_numerical' : parts[10]})



    ###### i select here the columns i want to include for my analysis
  X = []
  cont=0
  dict_cont_user_id={}
  dict_user_id_cooperation_quadrants={}
  
  for d in data:   #  data is a list of dict
        X.append([np.nan if d['H'] == 'nan' else float(d['H']),
                  np.nan if d['SD'] == 'nan' else float(d['SD']),
                  np.nan if d['SH'] == 'nan' else float(d['SH']),
                  np.nan if d['PD'] == 'nan' else float(d['PD'])])
              # para mas o menos variables (dimensiones), AKI

        user_id=d['user_id']
        dict_user_id_cooperation_quadrants[user_id]={'H':d['H'], 'SD':d['SD'], 'SH':d['SH'], 'PD':d['PD']  }
        dict_cont_user_id[cont]= user_id

        cont +=1




    ######## i transform the data to deal with Nans and transform then into the mean of the whole dataset
  imp = Imputer(missing_values='NaN', strategy='mean', axis=0)   # substitute the missing values for the mean in the population
  X_new = imp.fit_transform(X)     # X_new es array numpy, una lista de listas:   [[ 0.71428571  0.5         0.454657    0.5       ],[],[],...]










  for Num_clusters in range(2,21,1):

    

     print "\nCalculating clustering analysis for", Num_clusters, " (", type_data, "data)"


     list_errors=[]  # defined for a given person as the sum of dist*dist between its coord. and all centroids
     list_distances_removed_to_centroids=[]
   
    ##### leave-one-out cross validation      
     list_indexes=range(len(X_new))
     list_dict_iter_centroids=[]
     for i in range(len(X_new)):  # i remove one person at the time
        
#        print X_new
 #       print "old",len(X_new), type(X_new)               

        index_removed_person=list_indexes.pop(0)
      #  print "index for removed person",index_removed_person


        X_new_aux = X_new[list_indexes,:]  # X_new_aux is like X_new but without the index-th elemnt

  #      print X_new_aux
   #     print "new:",len(X_new_aux), type(X_new_aux)

        coord_removed_person=X_new[index_removed_person]

        dict_coord_removed_person={'H':coord_removed_person[0], 'SD':coord_removed_person[1], 'SH':coord_removed_person[2], 'PD':coord_removed_person[3]  }    ##  values of cooperation in order: [H, SD, SH, PD]

        #print "coord. for removed person:",coord_removed_person
        #print dict_coord_removed_person



        ### kmeans for the data with one person removed
        dict_clusternumber_list_users={}
        kmeans_algorithm_and_grouping(dict_clusternumber_list_users,dict_cont_user_id, X_new_aux,Num_clusters)  # this function fills in the dict dict_clusternumber_list_users
        
       
        
        sum_distances_squared=0.
        dict_clusternumber_dist_centroid_removed_person={}
        dict_clusternumber_centroids={}
        ####### i get the centriods of each cluster
        for key in dict_clusternumber_list_users:          

            list_H=[]
            list_SD=[]
            list_SH=[]
            list_PD=[]

            current_cluster=dict_clusternumber_list_users[key]   # list users in current cluster

            dict_clusternumber_centroids[key]={}

            for user_id in current_cluster:

                dict_coop_quadrants_user=dict_user_id_cooperation_quadrants[user_id]

                H=dict_coop_quadrants_user['H']
                SD=dict_coop_quadrants_user['SD']
                SH=dict_coop_quadrants_user['SH']
                PD= dict_coop_quadrants_user['PD']

                if H!= "nan":
                    list_H.append(float(H))
                if SD!= "nan":
                    list_SD.append(float(SD))
                if SH!= "nan":
                    list_SH.append(float(SH))
                if PD!= "nan":
                    list_PD.append(float(PD))

            centroid_H= np.mean(list_H)
            centroid_SD= np.mean(list_SD)
            centroid_SH= np.mean(list_SH)
            centroid_PD= np.mean(list_PD)

            dict_clusternumber_centroids[key]["H"]=centroid_H
            dict_clusternumber_centroids[key]["SD"]=centroid_SD
            dict_clusternumber_centroids[key]["SH"]=centroid_SH
            dict_clusternumber_centroids[key]["PD"]=centroid_PD


          #  print key,"centroid:    H:", centroid_H, "  SD:",centroid_SD , "  SH:",centroid_SH , "  PD:",centroid_PD
            distance_to_centroid=distance(dict_clusternumber_centroids[key], dict_coord_removed_person)
            dict_clusternumber_dist_centroid_removed_person[key]= distance_to_centroid

            sum_distances_squared += distance_to_centroid*distance_to_centroid


        min_dist=min(dict_clusternumber_dist_centroid_removed_person.values())
            
     #   print dict_clusternumber_dist_centroid_removed_person, min_dist
        list_distances_removed_to_centroids.append(min_dist)  # the error will be the distance to the closest centroid (i assume it belongs to that one), and i get a dispersion of values for all people removed one by one 
        

        list_errors.append(sum_distances_squared)

        list_indexes.append(index_removed_person)  # i add again the removed person (to remove a different one in the next iter)





     print Num_clusters, np.mean(list_distances_removed_to_centroids), np.std(list_distances_removed_to_centroids), np.mean(list_errors), np.std(list_errors)


##################
###################
###################


def kmeans_algorithm_and_grouping (dict_clusternumber_list_users, dict_cont_user_id, X_new, Num_clusters):




    ###### Kmeans algorithm
    kmeans = KMeans( n_clusters=Num_clusters, n_init=10)  # i define the algorithm i want to run
    kmeans.fit(X_new)   # i run it
  

   
    ###### i get a dict for user_id: cluster_label
    dict_user_clusternumber={}
    cont=0
    for i in kmeans.labels_:  # lista del group-index al que pertenece cada usuario (en el mismo orden que en X)


        user_id= dict_cont_user_id[cont]
        dict_user_clusternumber[user_id]=i
        cont +=1



    ###### i get a dict for cluster_label: list_members          
    for user_id in dict_user_clusternumber:
        label_cluster=dict_user_clusternumber[user_id]
        
        try:
            dict_clusternumber_list_users[label_cluster].append(user_id)
        except KeyError :
            dict_clusternumber_list_users[label_cluster]=[]
            dict_clusternumber_list_users[label_cluster].append(user_id)



##################################
###############################

def distance(vector1, vector2):

   
    dist=0.
    if len(vector1)==len(vector2):
        for key in vector1:  # sum over 4 dimensions
            #print key, vector1[key]  , vector2[key]
            try:
                dist = dist +  (vector2[key] - vector1[key])*(vector2[key] - vector1[key])
               
            except:   # if one of the vectors has a missing value for a coordenate
                pass
#                print "ignoring coordenate", key, vector1, vector2
                  # i ignore that component

               # print "v1, v2",vector1[key], vector2[key]
                #raw_input()

        return np.sqrt(dist)

    else:

        print "i can't calculate distance between", vector1, vector2, "  diff. dimensionalities"
        exit()
    

######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

