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

def main():
        
    

    Num_clusters=2
    Niter=20
    histogr_flag="NO"  # for the cluster sizes for a given partition


    type_data="actual"#"actual"   or   "random"

    print "\nCalculating clustering analysis for", Num_clusters, " (", type_data, "data)"





  
    exclude_first_rounds="YES"   # YES or NO
    label_exclude=""
    first_round_to_include=1 
    if  exclude_first_rounds=="YES" :
        first_round_to_include=3   # until this one, i exclude  (or   =1 and i exclude nothing)
        label_exclude="_excluding_rounds_1_to_"+str(first_round_to_include-1)





    ####### input files

    if type_data=="actual" :
        filename_hist_cluster_sizes="../Results/hist_cluster_sizes_"+str(Num_clusters)+"clusters"+str(Niter)+"iter.dat"
        #data_file='../Results/DAU_data_for_Jordi_kmeans.dat'
        data_file= "../Results/DAU_for_cluster_analysis_by_quadrants_and_groupsSminusT"+str(label_exclude)+".dat"


    elif type_data=="random" :
        filename_hist_cluster_sizes="../Results/hist_cluster_sizes_RANDOM_"+str(Num_clusters)+"clusters"+str(Niter)+"iter.dat"
        data_file="../Results/DAU_for_cluster_analysis_by_quadrants_and_groupsSminusT_random_total"+str(label_exclude)+".dat"





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
                         'avg_Coop' : parts[1],
                         'H' : parts[2],
                         'SD' : parts[3],
                         'SH' : parts[4],
                         'PD' : parts[5],                        
                         'S-T[-15,-10)' : parts[6],
                         'S-T[-10,-5)' : parts[7],
                         'S-T[-5,0)' : parts[8],
                         'S-T[0,5]' : parts[9],
                         'type_player' : parts[10],
                         'type_player_numerical' : parts[11]})


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

   

    list_cluster_sizes=[]
    list_dict_analysis=[]
    for i in range(Niter):
        
        print "Iter:", i

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
                name0="../Results/Niter_clustering/list_clusters_kmeans"+str(Num_clusters)+"-"+str(key+1)+"_"+str(i)+"iter"+str(label_exclude)+".txt"
            elif type_data=="random" :
                name0="../Results/Niter_clustering/list_clusters_kmeans_random"+str(Num_clusters)+"-"+str(key+1)+"_"+str(i)+"iter"+str(label_exclude)+".txt"


#            print "\n\n",key

            file0=open(name0, 'wt')    
            print >> file0, "Original_row user_id H SD SH PD"   # the header


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


                print >> file0, user_id, user_id, H , SD , SH  , PD
            file0.close()
#            print "written clustering file:",name0



            print key,"centroid:    H:", numpy.mean(list_H), "  SD:", numpy.mean(list_SD), "  SH:", numpy.mean(list_SH), "  PD:",numpy.mean(list_PD)

    if histogr_flag=="YES":
        histograma_gral.histograma(list_cluster_sizes, filename_hist_cluster_sizes,None)













    exit()



















    ####### exploring overlap between clusters
    for iter1 in range(Niter):
        for iter2 in range(Niter):  
            if iter2 >= iter1:          
                for j in range(Num_clusters):
                    for k in range(Num_clusters):
                        if k >= j:
                            print "iters:",iter1, iter2, "  clusters:",k, j
                            
                            cluster1=list_dict_analysis[iter1][j]  # first index is iter, second is cluster
                            cluster2=list_dict_analysis[iter2][k]
                            

                            print  cluster1, len(cluster1) 
                            print  cluster2, len(cluster2) 
                            

                            intersect=len(list(set(cluster1) & set(cluster2)))
                            print "intersection size:",intersect,"  ",  float(intersect)/max(len(cluster1), len(cluster2))*100,"%"

                       

 #   print  list_dict_analysis[0][0], len( list_dict_analysis[0][0])  # first index is iter, second is cluster
  #  print 
   # print  list_dict_analysis[1][0], len( list_dict_analysis[1][0])
    #print "intersection size:",len(list(set(list_dict_analysis[1][0]) & set(list_dict_analysis[1][0])))








####





##################
###################
###################


def kmeans_algorithm_and_grouping (dict_clusternumber_list_users, dict_cont_user_id, X_new, Num_clusters):




    ###### Kmeans algorithm
    kmeans = KMeans( n_clusters=Num_clusters, n_init=10)  # i define the algorithm i want to run
    kmeans.fit(X_new)   # i run it
    print sklearn.metrics.silhouette_score(X_new, kmeans.labels_, metric='euclidean')
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


