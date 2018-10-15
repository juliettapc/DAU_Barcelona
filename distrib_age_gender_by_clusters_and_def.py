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
import itertools
from  scipy import stats
import random

def main():
    
    Nbins=12
 
    
    Num_clusters=5


    Niter=200  # for bootstraping the gender distributions by cluster vs all




#####Clusters from kmeans k=5, (iter109)

#####Cluster1: cooperate only in up triangle H   (Competidores)
#####Cluster2: cooperate in left half of plane   (Cazarecompensas)
#####Cluster3: rarunos
#####Cluster4: cooperate everywhere  (Cooperators) 
#####Cluster5: cooperate in top half of plane (Conservadores)



    dict_cluster_number_name={1:"Competitive",2:"Greedy", 3:"Clueless", 4:"Altruists", 5:"Conservative"}

    ######### input masterfile
    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))  #### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]

   


 
 #   threshold_flag=   "_treshold0.8"   # "_treshold0.8"  or ""
   # gral_filename="../Results/dau2014_partition"+threshold_flag+"_Carlos_"


    gral_filename="../Results/list_"
    
   
    
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





    dict_user_id_info={}
    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
        
        partida=dictionary['partida']
        num_elecciones=int(dictionary['num_eleccions'])
        age=int(dictionary['edat'])       
        num_rondas=len(dictionary['rondes'])
        tot_earnings=int(dictionary['guany_total'])   
        nickname=unidecode(dictionary['nickname']).replace(" ", "_")

        earnings_by_round=tot_earnings/float(num_elecciones)

        print tot_earnings,float(num_elecciones),earnings_by_round
        gender=dictionary['genere']
        if gender== 'h':
            gender=1
        elif gender == 'd':
            gender=0


        user_id=int(dictionary['id']       )

        dict_user_id_info[user_id]={}

        dict_user_id_info[user_id]['num_elecciones']=num_elecciones
        dict_user_id_info[user_id]['age']=age
        dict_user_id_info[user_id]['gender']=gender
        dict_user_id_info[user_id]['tot_earnings']=tot_earnings
        dict_user_id_info[user_id]['earnings_by_round']= earnings_by_round


#        print user_id, dict_user_id_info[user_id]['age'], dict_user_id_info[user_id]['gender'], dict_user_id_info[user_id]['tot_earnings'], nickname
       
  
    dict_cluster_number_list_ages_in_clusters={}  # for the pairwise KS-test comparison
    list_cluster_numbers=[]


    list_age_all=[]
    list_gender_all=[]
    list_tot_earnings_all=[]
    list_norm_earnings_by_round_all=[]
    
    for cluster in range(Num_clusters):
        cluster +=1    
        print "\ncluster", cluster, dict_cluster_number_name[cluster]
        list_age_current_cluster=[]
        list_gender_current_cluster=[]
        list_tot_earnings_current_cluster=[]
        list_norm_earnings_by_round_current_cluster=[]
                 

        file_cluster="../Results/Niter_clustering/list_clusters_kmeans"+str(Num_clusters)+"-"+str(cluster)+"_109iter.pickle"
        
        
        
#  file_cluster="../Results/list_clusters_kmeans5_dist_notypes-1.pickle  # the MeV data
        
        
        list_current_cluster=pickle.load(open(file_cluster, 'rb'))  
       

        for user_id in list_current_cluster:
            list_age_current_cluster.append(dict_user_id_info[user_id]['age'])
            list_gender_current_cluster.append(dict_user_id_info[user_id]['gender'])
            list_tot_earnings_current_cluster.append(dict_user_id_info[user_id]['tot_earnings'])
            list_norm_earnings_by_round_current_cluster.append(dict_user_id_info[user_id]['earnings_by_round'])       

            list_age_all.append(dict_user_id_info[user_id]['age'])
            list_gender_all.append(dict_user_id_info[user_id]['gender'])
            list_tot_earnings_all.append(dict_user_id_info[user_id]['tot_earnings'])
            list_norm_earnings_by_round_all.append(dict_user_id_info[user_id]['earnings_by_round'])           


        dict_cluster_number_list_ages_in_clusters[cluster]=list_age_current_cluster
       



        ######## i calculate the z-score of a cluster's gender distribution vs the total pupulation        
        list_avg_gender_in_synthetic_cluster=[]
        for iter in range(Niter):   # bootstrapping the age distribution vs all            
            list_synth=sample_with_replacement(list_gender_all, len(list_gender_current_cluster))
            list_avg_gender_in_synthetic_cluster.append(numpy.mean(list_synth))
          
        z_score=( numpy.mean(list_gender_current_cluster)-numpy.mean(list_avg_gender_in_synthetic_cluster) )/numpy.std(list_avg_gender_in_synthetic_cluster)

        print "z-score of gender distributions of cluster", dict_cluster_number_name[cluster],"vs all:", z_score

        raw_input()



        histograma_bines_gral.histograma_bins(list_age_current_cluster,Nbins, "../Results/Hist_age_cluster"+str(Num_clusters)+"_"+str(cluster)+".dat" )

        print "avg. age:", numpy.mean(list_age_current_cluster), "std:",  numpy.std(list_age_current_cluster)


        histograma_bines_gral.histograma_bins(list_tot_earnings_current_cluster,Nbins, "../Results/Hist_tot_earnings_cluster"+str(Num_clusters)+"_"+str(cluster)+".dat" )
        print "avg. earnings:", numpy.mean(list_tot_earnings_current_cluster), "std:",  numpy.std(list_tot_earnings_current_cluster)
       


        histograma_bines_gral.histograma_bins(list_norm_earnings_by_round_current_cluster,Nbins, "../Results/Hist_norm_earnings_by_round_cluster"+str(Num_clusters)+"_"+str(cluster)+".dat" )
        print "avg. earnings/num_rounds:", numpy.mean(list_norm_earnings_by_round_current_cluster), "std:",  numpy.std(list_norm_earnings_by_round_current_cluster)
 


        print "avg. gender:", numpy.mean(list_gender_current_cluster), numpy.std(list_gender_current_cluster), "   (1: male, 0: female)"


        print "cluster size:", len(list_current_cluster)

 


    for i in range(len(list_lists_def)):

        name_def= list_names[i] 
        print  name_def
        list_age_current_cluster=[]
        list_gender_current_cluster=[]
        list_tot_earnings_current_cluster=[]                                   
        list_norm_earnings_by_round_current_cluster=[]
        


        list_current_cluster=list_lists_def[i]


        for user_id in list_current_cluster:
            list_age_current_cluster.append(dict_user_id_info[user_id]['age'])
            list_gender_current_cluster.append(dict_user_id_info[user_id]['gender'])
            list_tot_earnings_current_cluster.append(dict_user_id_info[user_id]['tot_earnings'])
            list_norm_earnings_by_round_current_cluster.append(dict_user_id_info[user_id]['earnings_by_round'])
       

  



        histograma_bines_gral.histograma_bins(list_age_current_cluster,Nbins, "../Results/Hist_age_cluster_"+str( name_def)+".dat" )

        print "avg. age:", numpy.mean(list_age_current_cluster), "std:",  numpy.std(list_age_current_cluster)

        histograma_bines_gral.histograma_bins(list_tot_earnings_current_cluster,Nbins, "../Results/Hist_tot_earnings_cluster_"+str( name_def)+".dat" )

        print "avg. earnings:", numpy.mean(list_tot_earnings_current_cluster), "std:",  numpy.std(list_tot_earnings_current_cluster)



        histograma_bines_gral.histograma_bins(list_norm_earnings_by_round_current_cluster,Nbins, "../Results/Hist_norm_earnings_by_round_cluster_"+str( name_def)+".dat" )
        print "avg. earnings/num_rounds:", numpy.mean(list_norm_earnings_by_round_current_cluster), "std:",  numpy.std(list_norm_earnings_by_round_current_cluster)
       


        print "avg. gender:", numpy.mean(list_gender_current_cluster), numpy.std(list_gender_current_cluster), "   (1: male, 0: female)"

        print "cluster size:", len(list_current_cluster)


        print 

    histograma_bines_gral.histograma_bins(list_age_all,Nbins, "../Results/Hist_age_all.dat" )

    print "general avg. age:", numpy.mean(list_age_all), "std:",  numpy.std(list_age_all)


    histograma_bines_gral.histograma_bins(list_tot_earnings_all,Nbins, "../Results/Hist_tot_earnings_all.dat" )

    print "general avg. earnings:", numpy.mean(list_tot_earnings_all), "std:",  numpy.std(list_tot_earnings_all)
    


    histograma_bines_gral.histograma_bins(list_norm_earnings_by_round_all,Nbins, "../Results/Hist_norm_earnings_by_round_all.dat" )
    print "avg. earnings/num_rounds:", numpy.mean(list_norm_earnings_by_round_all), "std:",  numpy.std(list_norm_earnings_by_round_all)
     


    print "general avg. gender:", numpy.mean(list_gender_all), numpy.std(list_gender_all), "   (1: male, 0: female)"



    print "tot population:", len(list_age_all)




    ######## KS test
    #This tests whether 2 samples are drawn from the same distribution. Note that, like in the case of the one-sample K-S test, the distribution is assumed to be continuous.

    #This is the two-sided test, one-sided tests are not implemented. The test uses the two-sided asymptotic Kolmogorov-Smirnov distribution.

    #If the K-S statistic is small or the p-value is high, then we cannot reject the hypothesis that the distributions of the two samples are the same.

    print "\nKS-tests for age distributions by cluster:"
    for item in  itertools.combinations(dict_cluster_number_list_ages_in_clusters, 2):
             

        list_ages_cluster1=dict_cluster_number_list_ages_in_clusters[item[0]]
        list_ages_cluster2=dict_cluster_number_list_ages_in_clusters[item[1]]
  
        print "for clusters:",dict_cluster_number_name[item[0]],dict_cluster_number_name[item[1]],"  (KS,p):",stats.ks_2samp(list_ages_cluster1,list_ages_cluster2)  


        print "  for cluster:",dict_cluster_number_name[item[0]],"vs all   (KS,p):",stats.ks_2samp(list_ages_cluster1,list_age_all)
        print "  for cluster:",dict_cluster_number_name[item[1]],"vs all   (KS,p):",stats.ks_2samp(list_ages_cluster2,list_age_all)
     


    print "\n   **If the K-S statistic is small or the p-value is high, then we cannot reject the hypothesis that the distributions of the two samples are the same."





        
##########################
def sample_with_replacement(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result














######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

