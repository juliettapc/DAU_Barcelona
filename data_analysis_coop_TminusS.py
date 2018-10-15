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
import random

def main():


    pupulation_age="All"   #"young"  # or "adult"   or "All"

    if pupulation_age== "young":
        min_age_threshold=0
        max_age_threshold=15
    elif pupulation_age== "adult":
        min_age_threshold=16
        max_age_threshold=100
    elif pupulation_age== "All":
        min_age_threshold=0
        max_age_threshold=100

    else:
        print "wrong age range"
        exit()


    R=10
    P=5


    #######  to select results only from given rounds  (both ends included)
    min_round=1
    max_round=18



    type_definition= "PD"   #"higherHarmony"   #"SD"  #"lowerHarmony"  # or "PD" "SH"   "SD"
    umbral_coop=0.75

    ######### input file
    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)

   


    filename2="../Results/list_good_guys_"+str(type_definition)+"_threshold_coop"+str(umbral_coop)+".pickle"
    aux_list_good_guys=pickle.load(open(filename2, 'rb'))   # list of players who cooperated in the lower half of the Harmony (obtained in code: data_analysis_coop_exploring_behavior2.py)

    list_good_guys=[]
    for element in aux_list_good_guys:
         list_good_guys.append(int(element))





    ######### output files   

    output_filename1="../Results/Cooperation_vs_SminusT_"+str(pupulation_age)+"_ages_rounds"+str(min_round)+"_"+str(max_round)+str(type_definition)+".dat"
    output1= open(output_filename1,'wt')


   
    output_filename2="../Results/Cooperation_vs_SminusT_"+str(pupulation_age)+"_ages_rounds"+str(min_round)+"_"+str(max_round)+"_good_guys_"+str(type_definition)+".dat"
    output2= open(output_filename2,'wt')
 

   
    output_filename3="../Results/Cooperation_vs_SminusT_"+str(pupulation_age)+"_ages_rounds"+str(min_round)+"_"+str(max_round)+"_bad_guys_"+str(type_definition)+".dat"
    output3= open(output_filename3,'wt')



    output_filename4="../Results/Cooperation_vs_SminusT_RANDOM_"+str(pupulation_age)+"_ages_rounds"+str(min_round)+"_"+str(max_round)+"_bad_guys_"+str(type_definition)+".dat"
    output4= open(output_filename4,'wt')
 


 

    ######### 

    

 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]



    dict_SminusT_list_actions={}
    dict_SminusT_avg_coop={}
    dict_SminusT_std_coop={}
    dict_SminusT_sem_coop={}   # error of the mean  =std/ sqrt(num points)




    dict_SminusT_list_actions_good_guys={}
    dict_SminusT_avg_coop_good_guys={}
    dict_SminusT_std_coop_good_guys={}
    dict_SminusT_sem_coop_good_guys={}   # error of the mean  =std/ sqrt(num points)



    dict_SminusT_list_actions_bad_guys={}
    dict_SminusT_avg_coop_bad_guys={}
    dict_SminusT_std_coop_bad_guys={}
    dict_SminusT_sem_coop_bad_guys={}   # error of the mean  =std/ sqrt(num points)

    dict_SminusT_list_random_actions={}
    dict_SminusT_avg_coop_random_actions={}
    dict_SminusT_std_coop_random_actions={}
    dict_SminusT_sem_coop_random_actions={}


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

            list_four_possible_values=[P,R,T,S]
            
            SminusT=S-T



            round_number=dict_ronda['numronda']
           
            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
            # si no ha elegido nada, es None
              


            ##### i generate a random action for comparison purposes
            if action !=None:  # to have exactly as many random actions as real ones 
                random_action= random.choice([0.,1.])   
                if SminusT not in  dict_SminusT_list_random_actions:
                    dict_SminusT_list_random_actions[SminusT]=[]
                dict_SminusT_list_random_actions[SminusT].append(random_action)



            ####### cooperation vs S-T for everybody
            if SminusT in dict_SminusT_list_actions:
                if action !=None:
                      if age >= min_age_threshold and age <=  max_age_threshold:
                          if round_number <= max_round   and round_number >= min_round :                            
                              dict_SminusT_list_actions[SminusT].append(action)   
            else:
                if action !=None:
                    if age >= min_age_threshold and age <=  max_age_threshold:
                        if round_number <= max_round   and round_number >= min_round :                            
                            dict_SminusT_list_actions[SminusT]=[]
                            dict_SminusT_list_actions[SminusT].append(action)  



            ####### cooperation vs S-T for good guys
            if SminusT in dict_SminusT_list_actions_good_guys:
                if action !=None:
                      if age >= min_age_threshold and age <=  max_age_threshold:
                          if round_number <= max_round   and round_number >= min_round :      
                              if user_id in list_good_guys:
                                  dict_SminusT_list_actions_good_guys[SminusT].append(action)
                           
            else:
                if action !=None:

                    if age >= min_age_threshold and age <=  max_age_threshold:
                        if round_number <= max_round   and round_number >= min_round :                                      
                            if user_id in list_good_guys:
                                dict_SminusT_list_actions_good_guys[SminusT]=[]
                                dict_SminusT_list_actions_good_guys[SminusT].append(action)
                            


            ####### cooperation vs S-T for bad guys
            if SminusT in dict_SminusT_list_actions_bad_guys:
                if action !=None:
                      if age >= min_age_threshold and age <=  max_age_threshold:
                          if round_number <= max_round   and round_number >= min_round :      
                              if user_id not in list_good_guys:                                 
                                  dict_SminusT_list_actions_bad_guys[SminusT].append(action)

            else:
                if action !=None:

                    if age >= min_age_threshold and age <=  max_age_threshold:
                        if round_number <= max_round   and round_number >= min_round :                                      
                            if user_id not in list_good_guys:                                
                                dict_SminusT_list_actions_bad_guys[SminusT]=[]
                                dict_SminusT_list_actions_bad_guys[SminusT].append(action)







   
    ####### the the avg cooperation per (T-S) point
    for SminusT  in sorted(dict_SminusT_list_actions):      
    
        dict_SminusT_avg_coop[SminusT]=numpy.mean(dict_SminusT_list_actions[SminusT])
        dict_SminusT_std_coop[SminusT]=numpy.std(dict_SminusT_list_actions[SminusT])
        dict_SminusT_sem_coop[SminusT]=stats.sem(dict_SminusT_list_actions[SminusT])# error of the mean  =std/ sqrt(num points)


        dict_SminusT_avg_coop_good_guys[SminusT]=numpy.mean(dict_SminusT_list_actions_good_guys[SminusT])
        dict_SminusT_std_coop_good_guys[SminusT]=numpy.std(dict_SminusT_list_actions_good_guys[SminusT])
        dict_SminusT_sem_coop_good_guys[SminusT]=stats.sem(dict_SminusT_list_actions_good_guys[SminusT])# error of the mean  =std/ sqrt(num points)

        dict_SminusT_avg_coop_bad_guys[SminusT]=numpy.mean(dict_SminusT_list_actions_bad_guys[SminusT])
        dict_SminusT_std_coop_bad_guys[SminusT]=numpy.std(dict_SminusT_list_actions_bad_guys[SminusT])
        dict_SminusT_sem_coop_bad_guys[SminusT]=stats.sem(dict_SminusT_list_actions_bad_guys[SminusT])# error of the mean  =std/ sqrt(num points)

             

        dict_SminusT_avg_coop_random_actions[SminusT]=numpy.mean(dict_SminusT_list_random_actions[SminusT])
        dict_SminusT_std_coop_random_actions[SminusT]=numpy.std(dict_SminusT_list_random_actions[SminusT])
        dict_SminusT_sem_coop_random_actions[SminusT]=stats.sem(dict_SminusT_list_random_actions[SminusT])# error of the mean  =std/ sqrt(num points)

    

        print >> output1,SminusT,dict_SminusT_avg_coop[SminusT], dict_SminusT_std_coop[SminusT], dict_SminusT_sem_coop[SminusT]
        print >> output2,SminusT,dict_SminusT_avg_coop_good_guys[SminusT], dict_SminusT_std_coop_good_guys[SminusT], dict_SminusT_sem_coop_good_guys[SminusT]
      
      
        print >> output3,SminusT,dict_SminusT_avg_coop_bad_guys[SminusT], dict_SminusT_std_coop_bad_guys[SminusT], dict_SminusT_sem_coop_bad_guys[SminusT]
      
      
        print >> output4,SminusT, dict_SminusT_avg_coop_random_actions[SminusT], dict_SminusT_std_coop_random_actions[SminusT], dict_SminusT_sem_coop_random_actions[SminusT]


   
    output1.close()     
    print "written output datafile:", output_filename1  
   
    output2.close()     
    print "written output datafile:", output_filename2
   
    output3.close()     
    print "written output datafile:", output_filename3
   
    output4.close()     
    print "written output datafile:", output_filename4
   
  


######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

