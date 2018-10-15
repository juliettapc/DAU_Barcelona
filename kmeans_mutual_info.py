#!/usr/bin/env python


'''
Code to obtain the cluster scheme of any number of clusters, and its corresponding DB index

Created by Julia Poncela, on April 2015.

'''

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import Imputer
import histograma_gral
import sklearn
import numpy
import sklearn.metrics
import histogram_bins_increasing
import random



def main():
          

  tot_Num_clusters=20
  Niter=2000
  histogr_flag="NO"  # for the cluster sizes for a given partition


  type_data="random"    #"actual"   or   "random"


  pairing= "half" # "half" or "all_pairs"


  print "Num_clusters, avg_norm_mutual,std, avg_adjusted_mutual_info, std"

  for Num_clusters in range(tot_Num_clusters):
    Num_clusters  +=1

    #print "\nCalculating clustering analysis for", Num_clusters, " (", type_data, "data)"

    ####### output files

    if type_data=="actual" :
        filename_hist_cluster_sizes="../Results/hist_cluster_sizes_"+str(Num_clusters)+"clusters"+str(Niter)+"iter.dat"
        data_file='../Results/DAU_data_for_Jordi_kmeans.dat'




    elif type_data=="random" :
        filename_hist_cluster_sizes="../Results/hist_cluster_sizes_RANDOM_"+str(Num_clusters)+"clusters"+str(Niter)+"iter.dat"
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
              # para mas o menos variables (dimensiones), aki



        user_id=d['user_id']
        dict_user_id_cooperation_quadrants[user_id]={'H':d['H'], 'SD':d['SD'], 'SH':d['SH'], 'PD':d['PD']  }
        dict_cont_user_id[cont]= user_id

        cont +=1




    ######## i transform the data to deal with Nans and transform then into the mean of the whole dataset
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    X_new = imp.fit_transform(X)     # X_new es array numpy, una lista de listas:   [[ 0.71428571  0.5         0.454657    0.5       ],[],[],...]

   
    list_lists_clusternumber_for_users=[]  ## if 5 clusters and 10 Niter: [[2,1,4,0,3,2,2,2,1,0,...,0],[2,2,2,4,1,0,0,3,0,2,0,1,0,4,0,0,0,0,...,1],[],[],[],[...],[...],[...],[...],[...]]  # same order-user in all lists to be able to calculate mutual info!!!!!
    list_mutual_info_values=[]



    list_cluster_sizes=[]
    list_dict_analysis=[]
    
    for i in range(Niter):
        
      #  print "Iter:", i


        dict_user_id_clusternumber={}  #for the mutual info calculation

        dict_clusternumber_list_users={}
        kmeans_algorithm_and_grouping(dict_clusternumber_list_users,dict_cont_user_id, X_new,Num_clusters)
        
        
        list_dict_analysis.append(dict_clusternumber_list_users)
       
        
        ####### i print out the list of users in each cluster
        for key in dict_clusternumber_list_users:          

            list_H=[]
            list_SD=[]
            list_SH=[]
            list_PD=[]

            current_cluster=dict_clusternumber_list_users[key]
            list_cluster_sizes.append(len(current_cluster))

            if type_data=="actual" :
                name0="../Results/Niter_clustering/list_clusters_kmeans"+str(Num_clusters)+"-"+str(key+1)+"_"+str(i)+"iter.txt"
            elif type_data=="random" :
                name0="../Results/Niter_clustering/list_clusters_kmeans_random"+str(Num_clusters)+"-"+str(key+1)+"_"+str(i)+"iter.txt"


#            print "\n\n",key

            file0=open(name0, 'wt')    
            print >> file0, "Original_row user_id H SD SH PD"   # the header


            for user_id in current_cluster:

                dict_user_id_clusternumber[user_id]=key



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


                print >> file0, user_id, user_id, H , SD , SH  , PD
            file0.close()
#            print "written clustering file:",name0



          #  print key,"centroid:    H:", numpy.mean(list_H), "  SD:", numpy.mean(list_SD), "  SH:", numpy.mean(list_SH), "  PD:",numpy.mean(list_PD)



        lista=[]
        for key in sorted(dict_user_id_clusternumber):
           # print key, dict_user_id_clusternumber[key]
            lista.append(dict_user_id_clusternumber[key])
        list_lists_clusternumber_for_users.append(lista)


    list_norm_mutual_info_values=[] 
    list_adjusted_mutual_info_values=[] 

    if  pairing== "all_pairs":   # i try all N*(N-1)/2 possible pairs  
        for i in range(len(list_lists_clusternumber_for_users)):
            for j in range(len(list_lists_clusternumber_for_users)):
                if j> i:   # i test all pairs of ITER results
                    #print i, j
                    lista1=list_lists_clusternumber_for_users[i]
                    lista2=list_lists_clusternumber_for_users[j]
                    # for k in range(len(lista1)):
                    #    print lista1[k], lista2[k], "    Iters:", i, j

                            
                    norm_mutual_info_value= sklearn.metrics.normalized_mutual_info_score(lista1, lista2)        
                    list_norm_mutual_info_values.append(norm_mutual_info_value)

              
                    adjusted_mutual_info_value= sklearn.metrics.adjusted_mutual_info_score(lista1, lista2)        
                    list_adjusted_mutual_info_values.append(adjusted_mutual_info_value)



    elif pairing== "half":  # i pair them just in  N/2 pairs
        

        for i in range(int(len(list_lists_clusternumber_for_users)/2.)):
            random.shuffle(list_lists_clusternumber_for_users)  # randomize list of runs
            lista1=list_lists_clusternumber_for_users.pop()  # pick the last one (and remove it from the original list)
            
            random.shuffle(list_lists_clusternumber_for_users)
            lista2=list_lists_clusternumber_for_users.pop()
            
        
            norm_mutual_info_value= sklearn.metrics.normalized_mutual_info_score(lista1, lista2)        
            list_norm_mutual_info_values.append(norm_mutual_info_value)
        

            adjusted_mutual_info_value= sklearn.metrics.adjusted_mutual_info_score(lista1, lista2)        
            list_adjusted_mutual_info_values.append(adjusted_mutual_info_value)



    ######## end of Niter loop
    if histogr_flag=="YES":
        histograma_gral.histograma(list_cluster_sizes, filename_hist_cluster_sizes,None)





   

    Nbins=20
    name_h="../Results/histogram_norm_mutual_info_values_"+str(Num_clusters)+"clusters_"+str(Niter)+"iter_"+type_data+"_"+pairing+".txt"
    histogram_bins_increasing.histogram(list_norm_mutual_info_values,Nbins, name_h)
    avg_norm_mutual=numpy.mean(list_norm_mutual_info_values)
   
    #print "avg. norm mutual info value:", avg_norm_mutual, "  sd:",numpy.std(list_norm_mutual_info_values) #, "  gen. R2:",1.- numpy.exp(-(2.*avg_norm_mutual)) 


    #print "avg. adjusted mutual info value:", numpy.mean(list_adjusted_mutual_info_values), "  sd:",numpy.std(list_adjusted_mutual_info_values) #, "  gen. R2:",1.- numpy.exp(-(2.*avg_norm_mutual)) 



    print Num_clusters, avg_norm_mutual, numpy.std(list_norm_mutual_info_values), numpy.mean(list_adjusted_mutual_info_values), numpy.std(list_adjusted_mutual_info_values) 

####





##################
###################
###################


def kmeans_algorithm_and_grouping (dict_clusternumber_list_users, dict_cont_user_id, X_new, Num_clusters):




    ###### Kmeans algorithm
    kmeans = KMeans( n_clusters=Num_clusters, n_init=10)  # i define the algorithm i want to run
    kmeans.fit(X_new)   # i run it
   # print sklearn.metrics.silhouette_score(X_new, kmeans.labels_, metric='euclidean')
#    raw_input()


# silhouette_score is the score is bounded between -1 for incorrect clustering and +1 for highly dense clustering. Scores around zero indicate overlapping clusters.  # The score is higher when clusters are dense and well separated, which relates to a standard concept of a cluster.

   
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




######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "


