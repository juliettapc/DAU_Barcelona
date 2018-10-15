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
import bootstrapping


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


  #  R=10
   # P=5


    #######  to select results only from given rounds  (both ends included)
    min_round=1
    max_round=18

   

  
    ######### input file
    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)
   




    ######### output files  
    clustering_filename1="../Results/DAU_for_cluster_analysis_by_quadrants.dat"
    file_cluster1=open(clustering_filename1, 'wt')
   

    clustering_filename2="../Results/DAU_for_cluster_analysis_by_SminusT.dat"
    file_cluster2=open(clustering_filename2, 'wt')
   





 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]
    
    

  
    dict_dict_user_region_list_actions={}
    dict_user_list_actions_H={}
    dict_user_list_actions_higherH={}
    dict_user_list_actions_lowerH={}
    dict_user_list_actions_SD={}
    dict_user_list_actions_SH={}
    dict_user_list_actions_PD={}
    dict_user_list_actions_lowerPD={}
    dict_user_list_actions_higherPD={}
 
    dict_dict_user_SminusT_list_actions={}
    dict_user_list_puntosTS={}



    list_regions=["H","higherH","lowerH","SD","SH","PD","higherPD","lowerPD"]

    list_all_users=[]

    ##### loop over different users
    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
       


        nickname=unidecode(dictionary['nickname']).replace(" ", "_")
        user_id=dictionary['id']

    
        payoff_total=float(dictionary['guany_total'])   # this is calculated only up to round #13  !!
        partida=dictionary['partida']


      

        gender=dictionary['genere']
        if gender =="h":
            gender=1            
        elif gender == "d":
            gender=0

       

        num_elecciones=int(dictionary['num_eleccions'])
        age=int(dictionary['edat'])
        avg_racionalidad=dictionary['rationality']
        avg_ambicion=dictionary['ambition']
        num_rondas=len(dictionary['rondes'])       
      
        list_dict_rondas=dictionary['rondes']


      

          

        ######## list of rounds for a given user_id
        for dict_ronda in list_dict_rondas:
          ##  cada diccionario de ronda tiene: {'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}



            T=int(dict_ronda['T'])
            S=int(dict_ronda['S'])           
            punto_TS=(T,S)
            SminusT=S-T
           

            round_number=dict_ronda['numronda']


            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
            # si no ha elegido nada, es None
            

            if action != None:                    

                if user_id not in list_all_users:
                    list_all_users.append(user_id)


                if user_id not in dict_dict_user_SminusT_list_actions:
                    dict_dict_user_SminusT_list_actions[user_id]={}
                if SminusT not in dict_dict_user_SminusT_list_actions[user_id]:
                    dict_dict_user_SminusT_list_actions[user_id][SminusT]=[]
                dict_dict_user_SminusT_list_actions[user_id][SminusT].append(action)




                if user_id not in dict_user_list_puntosTS:
                    dict_user_list_puntosTS[user_id]=[]
                dict_user_list_puntosTS[user_id].append(punto_TS)





                if user_id not in dict_dict_user_region_list_actions:
                    dict_dict_user_region_list_actions[user_id]={}
                for region in list_regions:
                    if region not in dict_dict_user_region_list_actions[user_id]:
                        dict_dict_user_region_list_actions[user_id][region]=[]





            num_ronda=dict_ronda['numronda']
            quadrant=dict_ronda['cuadrant'].replace(" ", "_").replace("'", "")

                

            action_oponent=dict_ronda['seleccio_oponent']
            if action_oponent =="C":
                action_oponent=1.
            elif action_oponent=="D":
                action_oponent=0.           
             # si no ha elegido nada, es None
           







            ####### i get the list of action per zone, for a given user
            ########
            if S >= 5 and S <=10:   # Harmony
                  if T >=5 and T <=10:            
                          region= "H"
                          if user_id not in dict_user_list_actions_H:
                              dict_user_list_actions_H[user_id]= []
     
                          if action != None:
                              dict_user_list_actions_H[user_id].append(action)  
                              dict_dict_user_region_list_actions[user_id][region].append(action)
                            




            if S >= 5 and S <=10:   #lowerHarmony
                  if T >=5 and T <=10:
                     if S <= T: 
                          region= "lowerH"
                          if user_id not in dict_user_list_actions_lowerH:
                              dict_user_list_actions_lowerH[user_id]= []
     
                          if action != None:
                              dict_user_list_actions_lowerH[user_id].append(action)  
                              dict_dict_user_region_list_actions[user_id][region].append(action)


                             
           
            if S >= 5 and S <=10:    #higherHarmony
                  if T >=5 and T <=10:
                     if S > T: 
                         region= "higherH"
                         if user_id not in dict_user_list_actions_higherH:
                             dict_user_list_actions_higherH[user_id]= []
     
                         if action != None:
                             dict_user_list_actions_higherH[user_id].append(action)
                             dict_dict_user_region_list_actions[user_id][region].append(action)


            
            if S >= 0 and S <= 5:
                    if T >= 10 and T <=15:    #PD
                        region= "PD"
                        if user_id not in dict_user_list_actions_PD:
                            dict_user_list_actions_PD[user_id]= []
     
                        if action != None:
                            dict_user_list_actions_PD[user_id].append(action)
                            dict_dict_user_region_list_actions[user_id][region].append(action)


           
            if S >= 0 and S <= 5:   #higherPD
                    if T >= 10 and T <=15:
                       if S >= -10 + T:   
                           region= "higherPD"
                           if user_id not in dict_user_list_actions_higherPD:
                               dict_user_list_actions_higherPD[user_id]= []
     
                           if action != None:
                               dict_user_list_actions_higherPD[user_id].append(action)
                               dict_dict_user_region_list_actions[user_id][region].append(action)


              
            if S >= 0 and S <= 5:    #lowerPD
                    if T >= 10 and T <=15:
                       if S < -10 + T:    
                         region= "lowerPD"
                         if user_id not in dict_user_list_actions_lowerPD:
                             dict_user_list_actions_lowerPD[user_id]= []
     
                         if action != None:
                             dict_user_list_actions_lowerPD[user_id].append(action)
                             dict_dict_user_region_list_actions[user_id][region].append(action)


               
            if S >= 0 and S <= 5:    #SH
                    if T >= 5 and T <=10: 
                        region= "SH"
                        if user_id not in dict_user_list_actions_SH:
                            dict_user_list_actions_SH[user_id]= []
     
                        if action != None:
                            dict_user_list_actions_SH[user_id].append(action)
                            dict_dict_user_region_list_actions[user_id][region].append(action)



            if S >= 5 and S <= 10:     #SD
                    if T >= 10 and T <=15:  
                        region= "SD"    
                        if user_id not in dict_user_list_actions_SD:
                            dict_user_list_actions_SD[user_id]= []
                            
                        if action != None:
                            dict_user_list_actions_SD[user_id].append(action)
                            dict_dict_user_region_list_actions[user_id][region].append(action)





    ###### end loop over user_ids in the main dict   

    print >> file_cluster1, "user_id", 
    for region in list_regions:
        print >> file_cluster1, region, 
    print >> file_cluster1, ""


    for user_id in list_all_users:        
            print >> file_cluster1, user_id, 
            for region in list_regions:
                print  >> file_cluster1, numpy.mean(dict_dict_user_region_list_actions[user_id][region]),
            print   >> file_cluster1, ""



    print "written file:",clustering_filename1




    list_SminusT=[-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5]
    print >> file_cluster2, "user_id", "  <c> at S-T=-15",  "  <c> at S-T=-14",  "  <c> at S-T=-13",  "  <c> at S-T=-12",  "  <c> at S-T=-11",  "  <c> at S-T=-10",  "  <c> at S-T=-9",  "  <c> at S-T=-8",  "  <c> at S-T=-7",  "  <c> at S-T=-6",  "  <c> at S-T=-5", "  <c> at S-T=-4",  "  <c> at S-T=-3",  "  <c> at S-T=-2",  "  <c> at S-T=-1",  "  <c> at S-T=0",  "  <c> at S-T=1",  "  <c> at S-T=2",  "  <c> at S-T=3",  "  <c> at S-T=4",  "  <c> at S-T=5"
    for user_id in list_all_users:   
        print >> file_cluster2, user_id,
        for SminusT in list_SminusT:
            if SminusT in dict_dict_user_SminusT_list_actions[user_id]:               
                print  >> file_cluster2, numpy.mean(dict_dict_user_SminusT_list_actions[user_id][SminusT]),
            else:               
                print >> file_cluster2, "NA",
        print >> file_cluster2, ""
       

    print "written file:", clustering_filename2

######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

