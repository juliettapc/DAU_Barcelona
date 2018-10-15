#!/usr/bin/env python


'''
Code to validate the clustering scheme obtained by kmeans

Created by Julia Poncela, on April 2015.

'''

import numpy 
from sklearn.cluster import KMeans
from sklearn.preprocessing import Imputer
import histograma_gral      #histograma(lista, path_name_h)
import sklearn
import random
from  scipy import stats
import networkx as nx

def main():
        
    

  leave_out=100   # number of datapoints excluded from clustering to test robustness of the partition
  Niter=20

  type_data="actual"#"actual"   or   "random"


    ####### input files
  if type_data=="actual" :      
        data_file='../Results/DAU_data_for_Jordi_kmeans.dat'
  elif type_data=="random" :
              data_file='../Results/DAU_for_cluster_analysis_by_quadrants_and_groupsSminusT_random_total.dat'


  ####### output file

  nameDB="../Results/DB_vs_diff_clustering_scheme_cross_validation_leave_"+str(leave_out)+"_out_"+str(Niter)+"iter.txt"
  fileDB=open(nameDB, 'wt')    
 



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
        X.append([numpy.nan if d['H'] == 'nan' else float(d['H']),
                  numpy.nan if d['SD'] == 'nan' else float(d['SD']),
                  numpy.nan if d['SH'] == 'nan' else float(d['SH']),
                  numpy.nan if d['PD'] == 'nan' else float(d['PD'])])
              # para mas o menos variables (dimensiones), AKI

        user_id=d['user_id']
        dict_user_id_cooperation_quadrants[user_id]={'H':d['H'], 'SD':d['SD'], 'SH':d['SH'], 'PD':d['PD']  }
        dict_cont_user_id[cont]= user_id

        cont +=1




    ######## i transform the data to deal with Nans and transform then into the mean of the whole dataset
  imp = Imputer(missing_values='NaN', strategy='mean', axis=0)   # substitute the missing values for the mean in the population
  X_new = imp.fit_transform(X)     # X_new es array numpy, una lista de listas:   [[ 0.71428571  0.5         0.454657    0.5       ],[],[],...]
  list_indexes=range(len(X_new))





  for Num_clusters in range(2,20,1):
     
     list_DB_current_partition=[]
     G_leave_p_out=nx.Graph()           
     G_all_data=nx.Graph()

     
     for i in range(Niter):  # i remove a set of people every time
        print i

        ###### first i get the network of people classified together with the original data
        dict_clusternumber_list_users={}
        kmeans_algorithm_and_grouping(dict_clusternumber_list_users,dict_cont_user_id, X_new,Num_clusters)
                              
        for cluster_index in dict_clusternumber_list_users:          
          cluster=dict_clusternumber_list_users[cluster_index]  
          for user1 in cluster:
              for user2 in cluster:
                  if user2 > user1:  # to avoid double counting                   
                      try:
                          G_all_data[user1][user2]["weight"] +=1.                          
                      except KeyError:
                           G_all_data.add_edge(user1, user2)
                           G_all_data[user1][user2]["weight"] =1.                       
        ################ 
        
      
        dict_cluster_size={}
        dict_cluster_centroid={}
        dict_cluster_dispersion={}



        ##### leave-p-out cross validation  procedure
        ################ 
        new_dict_cont_user_id={}
        list_out_indexes=random.sample(list_indexes, leave_out)         
        new_list_of_lists=[]

        if len( list_out_indexes)>0:
            cont=0
            new_cont=0
            for item in X_new:
                user_id=dict_cont_user_id[cont]
                if cont not in list_out_indexes:   # this messes up with the dict_cont_user_id!!!!!!!!!!!!!!!
                    new_list_of_lists.append(item)                    
                    new_dict_cont_user_id[new_cont]=user_id

                    new_cont +=1
                cont +=1
      
            X_new_aux=numpy.array(new_list_of_lists)

        else:
            new_dict_cont_user_id=dict_cont_user_id
            X_new_aux = X_new
            

        
        ### kmeans for the data with some people removed      
        dict_clusternumber_list_users={}
        kmeans_algorithm_and_grouping(dict_clusternumber_list_users,new_dict_cont_user_id, X_new_aux,Num_clusters)  # this function fills in the dict dict_clusternumber_list_users                
            

        ##### add links to the network of leave-p-out
        for cluster_index in dict_clusternumber_list_users:          
                
                cluster=dict_clusternumber_list_users[cluster_index]  
                
                for user1 in cluster:
                    for user2 in cluster:
                        if user2 > user1:  # to avoid double counting
                            
                            try:
                                G_leave_p_out[user1][user2]["weight"] +=1.                          
                            except KeyError:
                                G_leave_p_out.add_edge(user1, user2)
                                G_leave_p_out[user1][user2]["weight"] =1.
                                


       
        ####### i get the centriods of each cluster
        for cluster in dict_clusternumber_list_users:          

            list_H=[]
            list_SD=[]
            list_SH=[]
            list_PD=[]
            dict_user_id_cooperation_quadrants_cluster={}   # only users in that cluster
 

            current_cluster=dict_clusternumber_list_users[cluster]   # list users in current cluster



            for user_id in current_cluster:

                dict_user_id_cooperation_quadrants_cluster[user_id]=dict_user_id_cooperation_quadrants[user_id]
                dict_coop_quadrants_user=dict_user_id_cooperation_quadrants_cluster[user_id]

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



            dict_cluster_size[cluster]=len(current_cluster)

            ###### i calculate the centroid of the cluster (avg of each coord.)
            
            centroid={}
            centroid["H"]=numpy.mean(list_H)
            centroid["SD"]=numpy.mean(list_SD)
            centroid["SH"]=numpy.mean(list_SH)        
            centroid["PD"]=numpy.mean(list_PD)        

            
            dict_cluster_centroid[cluster]=centroid
            
#            print centroid
            
            ###### i calculate the dispersion  within a cluster (avg distance between users' coords. and cluster's centroids)
            dispersion=0.
            for user_id in dict_user_id_cooperation_quadrants_cluster:  # sum over all datapoints (or users) in that cluster   
                
                dispersion = dispersion + distance(dict_user_id_cooperation_quadrants_cluster[user_id], centroid)          
                
            dispersion= dispersion / float(len(dict_user_id_cooperation_quadrants_cluster))   # i normalize by the size of the cluster
            dict_cluster_dispersion[cluster]=dispersion
            
            
            
          #  print "dispersion",dispersion

        ######## i calculate the separation between all pairs of clusters (centroids' distances)
        separation={}
        for cluster1 in range(Num_clusters):
            for cluster2 in range(Num_clusters):
                tupla=(cluster1, cluster2)

                dist=distance(dict_cluster_centroid[cluster1],dict_cluster_centroid[cluster2])
                separation[tupla]=dist
              #  print dict_cluster_centroid[cluster1],dict_cluster_centroid[cluster2], dist


                      #  print cluster1, cluster2, "separation:",separation[tupla]


      

        ##### I calculate the Rij  and Di
        ###############
        dict_cluster_Di={}
        R_ij={}        
        for cluster1 in range(Num_clusters):
            list_Rijs=[]
            for cluster2 in range(Num_clusters):
                if cluster1 != cluster2:
                    tupla=(cluster1, cluster2)
                    R_ij[tupla]=(dict_cluster_dispersion[cluster1] + dict_cluster_dispersion[cluster2] )/ separation[tupla]
                #print tupla, R_ij[tupla]
                
                    list_Rijs.append(R_ij[tupla])
            dict_cluster_Di[cluster1]=max(list_Rijs)
        #print "max Rij:",max(list_Rijs), cluster1, "\n\n"



        ########## i calculate the DB index of the cluster partion
        ####################
        DB=0.
        for cluster in dict_cluster_Di:
            DB += dict_cluster_Di[cluster]
        DB=DB/float(Num_clusters)

       # print "DB:", DB, " # clusters:", Num_clusters
        list_DB_current_partition.append(DB)




     ####### i count the links weights for both networks
     list_weight_all=[]
     for edge in G_all_data.edges(data=True):
        

         G_all_data[edge[0]][edge[1]]["weight"]= G_all_data[edge[0]][edge[1]]["weight"]/ float(Niter)                 

         list_weight_all.append( G_all_data[edge[0]][edge[1]]["weight"])

     print "avg weight all-data network", numpy.mean(list_weight_all), numpy.std(list_weight_all)
#     histograma_gral.histograma(list_weight_all,"../Results/hist_weight_links_"+str(Num_clusters)+"clusters_all_data_"+str(Niter)+"iter.dat" )




    # list_errors=[]
     #list_weight=[]
     for edge in G_leave_p_out.edges(data=True):
        
         G_leave_p_out[edge[0]][edge[1]]["weight"]= G_leave_p_out[edge[0]][edge[1]]["weight"]/ float(Niter)     
         list_weight.append( G_leave_p_out[edge[0]][edge[1]]["weight"])         

       #  error=0.
       #  try:
         #    error= (G_leave_p_out[edge[0]][edge[1]]["weight"] - G_all_data[edge[0]][edge[1]]["weight"])*(G_leave_p_out[edge[0]][edge[1]]["weight"] - G_all_data[edge[0]][edge[1]]["weight"])
       #  except KeyError:

          #   try:
            #     error=G_leave_p_out[edge[0]][edge[1]]["weight"]*G_leave_p_out[edge[0]][edge[1]]["weight"]
           #  except KeyError:
              #   error=G_all_data[edge[0]][edge[1]]["weight"]*G_all_data[edge[0]][edge[1]]["weight"]

 
        # list_errors.append(error)



  
     print "avg weight leave-p-out", numpy.mean(list_weight), numpy.std(list_weight)
   #  histograma_gral.histograma(list_weight,"../Results/hist_weight_links_"+str(Num_clusters)+"clusters_leave_out_"+str(leave_out)+"_"+str(Niter)+"iter.dat" )

#
    # print "avg error  all-data vs  leave-p-out", sum(list_errors)


     print Num_clusters, numpy.mean(list_DB_current_partition),numpy.std(list_DB_current_partition) ,stats.sem(list_DB_current_partition) , "avg weight", numpy.mean(list_weight), numpy.std(list_weight)
     print >> fileDB, Num_clusters, numpy.mean(list_DB_current_partition),numpy.std(list_DB_current_partition) ,stats.sem(list_DB_current_partition), numpy.mean(list_weight_all), numpy.std(list_weight_all),  numpy.mean(list_weight), numpy.std(list_weight)

    
  fileDB.close()

  print "written file:", nameDB
 
##################
###################
###################


def kmeans_algorithm_and_grouping (dict_clusternumber_list_users, dict_cont_user_id, data, Num_clusters):




    ###### Kmeans algorithm
    kmeans = KMeans( n_clusters=Num_clusters, n_init=10)  # i define the algorithm i want to run
    kmeans.fit(data)   # i run it
  

   
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

#    print vector1, vector2
    dist=0.
    if len(vector1)==len(vector2):
        for key in vector1:  # sum over 4 dimensions
            
            if vector1[key] != "nan" and vector1[key] != "Nan" and vector1[key] != "NAN": 
                if vector2[key] != "nan" and vector2[key] != "Nan" and vector2[key] != "NAN": 

                    dist = dist +  ( float(vector2[key])-float(vector1[key]) )*( float(vector2[key])-float(vector1[key]) )
               
            
       
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

