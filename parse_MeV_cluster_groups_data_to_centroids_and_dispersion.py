

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
import random
import bootstrapping
import math

def main():





 Nclusters=20   # i run the DB index for the scenarios: 2,3,...Nclusters 

 type_data ="kmeans_python"     ###"random"  or "from_MeV" or "kmeans_python"

 Niter=1




 ##### output file  num_clusters vs DBindex
 if  type_data =="random" :
     nameDB="../Results/DB_vs_diff_clustering_scheme_pythonKmeans_random_"+str(Niter)+"iter.txt"  ###### totally randomized actions 
                                                                    #(preserving # actions)
 elif type_data =="from_MeV" :
     nameDB="../Results/DB_vs_diff_clustering_scheme.txt"

 elif  type_data =="kmeans_python" :
     nameDB="../Results/DB_vs_diff_clustering_scheme_pythonKmeans_"+str(Niter)+"iter.txt"

 fileDB=open(nameDB, 'wt')    
 




 for num_clusters in range(2,Nclusters+1 , 1):   # loop over different partitions (in 4, 5, 6 clusters)


  list_DB_current_partition=[]
  for iter in range(Niter):
 
    print "iter:", iter
    dict_cluster_size={}
    dict_cluster_centroid={}
    dict_cluster_dispersion={}


    for cluster in range(num_clusters):  # loop over the clusters of a given partition


        
        if type_data =="from_MeV" :
            file_cluster="../Results/list_clusters_kmeans"+str(num_clusters)+"_dist_notypes-"+str(cluster+1)+".txt"

        elif  type_data =="kmeans_python" :
            file_cluster="../Results/Niter_clustering/list_clusters_kmeans"+str(num_clusters)+"-"+str(cluster+1)+"_"+str(iter)+"iter.txt"
            
        elif  type_data =="random" :               
            file_cluster="../Results/Niter_clustering/list_clusters_kmeans_random"+str(num_clusters)+"-"+str(cluster+1)+"_"+str(iter)+"iter.txt"


   
                          

        #file_cluster="../Results/list_clusters_self_organized-"+str(cluster+1)+".txt"   # 9 clusters (given by the algorithm, not by me)
       

      #  file_cluster="../Results/list_clusters_cast-"+str(cluster+1)+".txt"    # 54
       


       # file_cluster="../Results/for_testing"+str(num_clusters)+"-"+str(cluster+1)+".txt" #list_clusters_kmeans"+str(num_clusters)+"_dist_notypes-"+str(cluster+1)+".txt"



        #### for a give cluster (and wirhin a give cluster scheme)
        list_H=[]
        list_SD=[]
        list_SH=[]
        list_PD=[]
        dict_user_id_cooperation_quadrants={}
        cont_nan=0

       
        print file_cluster
        file1=open(file_cluster,'r')
        list_lines=file1.readlines()
        cont=0
        for line in list_lines:                          
            if cont > 0:  # i skip the header
                # first field is: "original row"
               
                try:
                    list_values_one_line=line.strip("\n").split("	")
                    user_id=int(list_values_one_line[1]) 
                    #print list_values_one_line, "Mev"
                    
                except IndexError:
                    list_values_one_line=line.strip("\n").split(" ")  # some files separated by space, not tab
                    user_id=int(list_values_one_line[1])
                  #  print list_values_one_line, "kmeans python"
                

                dict_user_id_cooperation_quadrants[user_id]={}

                H=list_values_one_line[2].replace("NAN","NaN").replace("nan","NaN").replace("Nan","NaN")
                if H != "NaN" :
                    H=float(list_values_one_line[2])
                    list_H.append(H)
                    dict_user_id_cooperation_quadrants[user_id]["H"]=H
                else:
                    dict_user_id_cooperation_quadrants[user_id]["H"]= "NaN"
                    cont_nan +=1


                SD=list_values_one_line[3].replace("NAN","NaN").replace("nan","NaN").replace("Nan","NaN")
                if SD != "NaN":
                    SD=float(list_values_one_line[3])
                    list_SD.append(SD)
                    dict_user_id_cooperation_quadrants[user_id]["SD"]=SD
                else:
                    dict_user_id_cooperation_quadrants[user_id]["SD"]= "NaN"
                    cont_nan +=1


                SH=list_values_one_line[4].replace("NAN","NaN").replace("nan","NaN").replace("Nan","NaN")
                if SH != "NaN" :
                    SH=float(list_values_one_line[4])
                    list_SH.append(SH)
                    dict_user_id_cooperation_quadrants[user_id]["SH"]=SH
                else:
                    dict_user_id_cooperation_quadrants[user_id]["SH"]= "NaN"
                    cont_nan +=1



                PD=list_values_one_line[5].replace("NAN","NaN").replace("nan","NaN").replace("Nan","NaN")
                if PD != "NaN" :
                    PD=float(list_values_one_line[5])
                    list_PD.append(PD)
                    dict_user_id_cooperation_quadrants[user_id]["PD"]=PD
                else:
                    dict_user_id_cooperation_quadrants[user_id]["PD"]= "NaN"
                    cont_nan +=1


                
              
            cont +=1
          
        

        dict_cluster_size[cluster]=len(dict_user_id_cooperation_quadrants)

#        print "# nan in cluster:",cluster, "  is:", cont_nan 
       

        ###### i calculate the centroid of the cluster (avg of each coord.)
        centroid={}
        centroid["H"]=numpy.mean(list_H)
        centroid["SD"]=numpy.mean(list_SD)
        centroid["SH"]=numpy.mean(list_SH)        
        centroid["PD"]=numpy.mean(list_PD)

        
        dict_cluster_centroid[cluster]=centroid

      

        ###### i calculate the dispersion  within a cluster (avg distance between users' coords. and cluster's centroids)
        dispersion=0.
        for user_id in dict_user_id_cooperation_quadrants:  # sum over all datapoints (or users) in that cluster   
       
            dispersion = dispersion + distance(dict_user_id_cooperation_quadrants[user_id], centroid)          
         
           
        dispersion= dispersion / float(len(dict_user_id_cooperation_quadrants))   # i normalize by the size of the cluster
        dict_cluster_dispersion[cluster]=dispersion



        print cluster, "size:", dict_cluster_size[cluster]
        print  " centroid:", dict_cluster_centroid[cluster]
        print  " dispersion:",dict_cluster_dispersion[cluster] 

      

    ######## i calculate the separation between all pairs of clusters (centroids' distances)
    separation={}
    for cluster1 in range(num_clusters):
        for cluster2 in range(num_clusters):
            tupla=(cluster1, cluster2)

            dist=distance(dict_cluster_centroid[cluster1],dict_cluster_centroid[cluster2])
            separation[tupla]=dist
            print dict_cluster_centroid[cluster1],dict_cluster_centroid[cluster2], dist
          #  print cluster1, cluster2, "separation:",separation[tupla]


    
        #print
    print "separation",separation

    exit()
    
    ##### I calculate the Rij  and Di
    dict_cluster_Di={}
    R_ij={}
   
    for cluster1 in range(num_clusters):
        list_Rijs=[]
        for cluster2 in range(num_clusters):
            if cluster1 != cluster2:
                tupla=(cluster1, cluster2)
                R_ij[tupla]=(dict_cluster_dispersion[cluster1] + dict_cluster_dispersion[cluster2] )/ separation[tupla]
                #print tupla, R_ij[tupla]
                
                list_Rijs.append(R_ij[tupla])
        dict_cluster_Di[cluster1]=max(list_Rijs)
        #print "max Rij:",max(list_Rijs), cluster1, "\n\n"



    ########## i calculate the DB index of the cluster partion
    DB=0.
    for cluster in dict_cluster_Di:
        DB += dict_cluster_Di[cluster]
    DB=DB/float(num_clusters)

    print "DB:", DB, " # clusters:", num_clusters
    list_DB_current_partition.append(DB)



  print >> fileDB, num_clusters, numpy.mean(list_DB_current_partition),numpy.std(list_DB_current_partition) ,stats.sem(list_DB_current_partition) 


  

 fileDB.close()
 print "written DB-index file:", nameDB
 

##################################
###############################

def distance(vector1, vector2):

   
    dist=0.
    if len(vector1)==len(vector2):
        for key in vector1:  # sum over 4 dimensions
            #print key, vector1[key]  , vector2[key]

            if vector1[key] != "nan" and vector1[key] != "Nan" and vector1[key] != "NAN": 
                if vector2[key] != "nan" and vector2[key] != "Nan" and vector2[key] != "NAN": 

                    dist = dist +  (float(vector2[key]) - float(vector1[key]))*(float(vector2[key]) - float(vector1[key]))
               

            #try:
             #   dist = dist +  (float(vector2[key]) - vector1[key])*(vector2[key] - vector1[key])
               
            #except:   # if one of the vectors has a missing value for a coordenate
             #   pass
#                print "ignoring coordenate", key, vector1, vector2
                  # i ignore that component

               # print "v1, v2",vector1[key], vector2[key]
                #raw_input()

        return numpy.sqrt(dist)

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

