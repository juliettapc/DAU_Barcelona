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
  


    type_strategist="clusters"      #  altruists   rationals   mostly_def    weirdos  or "clusters"

    cluster_num=5
   

    ######### input file
    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)
   

    filename2="../Results/list_"+str(type_strategist)+".pickle"

    if type_strategist == "clusters":  # type of strategists from the kmeans analysis
         filename2="../Results/list_clusters_kmeans5_dist_notypes-"+str(cluster_num)+".pickle"

    list_strategists=pickle.load(open(filename2, 'rb')) 



    print list_strategists

    ######### output files   

    output_filename1="../Results/Cooperation_vs_SminusT_all.dat"
    output1= open(output_filename1,'wt')


    output_filename2="../Results/Cooperation_vs_SminusT_"+str(type_strategist)+".dat"
    if type_strategist== "clusters":  # type of strategists from the kmeans analysis
        output_filename2="../Results/Cooperation_vs_SminusT_"+str(type_strategist)+str(cluster_num)+".dat"
        
    output2= open(output_filename2,'wt')

 

    ######### 

    

 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]




    dict_SminusT_list_actions={}
    dict_SminusT_avg_coop={}
    dict_SminusT_std_coop={}
    dict_SminusT_sem_coop={}   # error of the mean  =std/ sqrt(num points)




    dict_SminusT_list_actions_strategists={}
    dict_SminusT_avg_coop_strategists={}
    dict_SminusT_std_coop_strategists={}
    dict_SminusT_sem_coop_strategists={}   # error of the mean  =std/ sqrt(num points)


    valid_actions =0.


    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
                  
        partida=dictionary['partida']
        num_elecciones=dictionary['num_eleccions']
        age=int(dictionary['edat'])       
        num_rondas=len(dictionary['rondes'])
        nickname=unidecode(dictionary['nickname']).replace(" ", "_")
        user_id=int(dictionary['id']       )


       
      
        list_dict_rondas=dictionary['rondes']

      

        for dict_ronda in list_dict_rondas:
          ##  cada diccionario de ronda tiene: {'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}



            T=int(dict_ronda['T'])
            S=int(dict_ronda['S'])

          
            
            SminusT=S-T



            round_number=dict_ronda['numronda']
           
            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
            # si no ha elegido nada, es None
              

            if action !=None:
                valid_actions+=1.
           


            ####### cooperation vs S-T for everybody
            if SminusT in dict_SminusT_list_actions:
                if action !=None:
                     # if age >= min_age_threshold and age <=  max_age_threshold:
                         # if round_number <= max_round   and round_number >= min_round :       
                    dict_SminusT_list_actions[SminusT].append(action)   
            else:
                if action !=None:
                  #  if age >= min_age_threshold and age <=  max_age_threshold:
                       # if round_number <= max_round   and round_number >= min_round :                            
                    dict_SminusT_list_actions[SminusT]=[]
                    dict_SminusT_list_actions[SminusT].append(action)  




            ####### cooperation vs S-T for strategists
            if SminusT in dict_SminusT_list_actions_strategists:
                if action !=None:
                     # if age >= min_age_threshold and age <=  max_age_threshold:
                          #if round_number <= max_round   and round_number >= min_round :      
                    if user_id in list_strategists:
                        dict_SminusT_list_actions_strategists[SminusT].append(action)
                           
            else:
                if action !=None:

                   # if age >= min_age_threshold and age <=  max_age_threshold:
                      #  if round_number <= max_round   and round_number >= min_round :    
                    if user_id in  list_strategists:
                        dict_SminusT_list_actions_strategists[SminusT]=[]
                        dict_SminusT_list_actions_strategists[SminusT].append(action)
                     
                        






   
    ####### the the avg cooperation per (T-S) point
    for SminusT  in sorted(dict_SminusT_list_actions):      
       
        dict_SminusT_avg_coop_strategists[SminusT]=numpy.mean(dict_SminusT_list_actions_strategists[SminusT])
        dict_SminusT_std_coop_strategists[SminusT]=numpy.std(dict_SminusT_list_actions_strategists[SminusT])
        dict_SminusT_sem_coop_strategists[SminusT]=stats.sem(dict_SminusT_list_actions_strategists[SminusT])# error of the mean  =std/ sqrt(num points)
        
        
        dict_SminusT_avg_coop[SminusT]=numpy.mean(dict_SminusT_list_actions[SminusT])
        dict_SminusT_std_coop[SminusT]=numpy.std(dict_SminusT_list_actions[SminusT])
        dict_SminusT_sem_coop[SminusT]=stats.sem(dict_SminusT_list_actions[SminusT])# error of the mean  =std/ sqrt(num points)
        
        
        print >> output1, SminusT, dict_SminusT_avg_coop[SminusT], dict_SminusT_std_coop[SminusT], dict_SminusT_sem_coop[SminusT]
        
        
        print >> output2, SminusT, dict_SminusT_avg_coop_strategists[SminusT], dict_SminusT_std_coop_strategists[SminusT], dict_SminusT_sem_coop_strategists[SminusT]
      


        
        

   
    output1.close()     
    print "written output datafile:", output_filename1  
   
    output2.close()     
    print "written output datafile:", output_filename2
   
  
    print "# valid actions:", valid_actions 

######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

