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
import scipy.stats
import random
import bootstrapping
import math

def main():

    small_additive_cte=0.01   # to add to every value, so the clustering doesnt ELIMINATE entries with value 0   !!!


    flag_randomization= "total"  #"by_region"  or "total"

    print  "type of randomization:", flag_randomization

    list_SminusT_group=[1,2,3,4]
    list_SminusT=[-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5]
    list_regions=["H","SD","SH","PD"]#,"higherH","lowerH", "higherPD","lowerPD"]





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
    clustering_filename1="../Results/DAU_for_cluster_analysis_by_quadrants_and_groupsSminusT_excluding_borders.dat"
    file_cluster1=open(clustering_filename1, 'wt')
  
    if flag_randomization== "by_region" : #"by_region"  or "total"
        clustering_filename5="../Results/DAU_for_cluster_analysis_by_quadrants_and_groupsSminusT_random_by_region_excluding_borders.dat"

    elif  flag_randomization=="total":
        clustering_filename5="../Results/DAU_for_cluster_analysis_by_quadrants_and_groupsSminusT_random_total_excluding_borders.dat"

    file_cluster5=open(clustering_filename5, 'wt')
  
 

    clustering_filename2="../Results/DAU_for_cluster_analysis_by_SminusT_excluding_borders.dat"
    file_cluster2=open(clustering_filename2, 'wt')
   


    clustering_filename3="../Results/DAU_for_cluster_analysis_by_quadrants_distance_matrix_excluding_borders.dat"
    file_cluster3=open(clustering_filename3, 'wt')
   


    pickle_file_rationals="../Results/list_rationals_excluding_borders.pickle"
    pickle_file_altruists="../Results/list_altruists_excluding_borders.pickle"
    pickle_file_mostly_def="../Results/list_mostly_def_excluding_borders.pickle"
    pickle_file_weirdos="../Results/list_weirdos_excluding_borders.pickle"
 




 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]
    
    
    list_all_actions=[]
    list_all_actions_with_NAN=[]
    
    dict_region_list_all_actions={}
    dict_SminusT_group_list_all_actions={}

    list_all_users=[]


    dict_region_list_actions={}
    for region in list_regions:
        dict_region_list_actions[region]=[]



    dict_SminusT_group_list_actions={}
    for SminusT_group in list_SminusT_group:
        dict_SminusT_group_list_actions[SminusT_group]=[]




    dict_user_list_actions={}


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
    dict_dict_user_SminusTgroup_list_actions={}
    dict_user_list_puntosTS={}


    list_H_all=[]
    list_SD_all=[]
    list_SH_all=[]
    list_PD_all=[]

   
    for region in list_regions:
        dict_region_list_all_actions[region]=[]
    for SminusT_group in list_SminusT_group:
        dict_SminusT_group_list_all_actions[SminusT_group]=[]



    ##### loop over different users
    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
       


        nickname=unidecode(dictionary['nickname']).replace(" ", "_")
        user_id=int(dictionary['id'])

    
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
           

            SminusT_group="NA"

            if SminusT >= -15  and SminusT < -10:
                SminusT_group=1
            elif  SminusT >= -10  and SminusT < -5:
                SminusT_group=2
            elif  SminusT >= -5  and SminusT < 0:
                SminusT_group=3
            elif  SminusT >=  0  and SminusT <=5:
                SminusT_group=4
            else:
                print "wrong SminusT!", SminusT


          

            round_number=dict_ronda['numronda']

            oponent=dict_ronda['oponent']





            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
            # si no ha elegido nada, es None
            
            list_all_actions_with_NAN.append(action)   
            if action != None:                    

                if user_id not in list_all_users:
                    list_all_users.append(user_id)
                list_all_actions.append(action)   # for the randomized version



                if user_id not in dict_user_list_actions:
                    dict_user_list_actions[user_id]=[]
                dict_user_list_actions[user_id].append(action)



                # for S-T values
                if user_id not in dict_dict_user_SminusT_list_actions:
                    dict_dict_user_SminusT_list_actions[user_id]={}
                if SminusT not in dict_dict_user_SminusT_list_actions[user_id]:
                    dict_dict_user_SminusT_list_actions[user_id][SminusT]=[]
                dict_dict_user_SminusT_list_actions[user_id][SminusT].append(action)



                ## for S-T grouped values
                if user_id not in dict_dict_user_SminusTgroup_list_actions:
                    dict_dict_user_SminusTgroup_list_actions[user_id]={}
                if SminusT_group not in dict_dict_user_SminusTgroup_list_actions[user_id]:
                    dict_dict_user_SminusTgroup_list_actions[user_id][SminusT_group]=[]
                dict_dict_user_SminusTgroup_list_actions[user_id][SminusT_group].append(action)





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
            if S > 5 and S <=10:   # Harmony
                  if T >=5 and T <10:            
                      region= "H"
                      if user_id not in dict_user_list_actions_H:
                          dict_user_list_actions_H[user_id]= []
     
                      if action != None:
                          dict_user_list_actions_H[user_id].append(action)  
                          dict_dict_user_region_list_actions[user_id][region].append(action)
                            
                          list_H_all.append(action)
   


           # if S > 5 and S <=10:   #lowerHarmony
               #    if T >=5 and T <10:
                     # if S <= T: 
                        #   region= "lowerH"
                         #  if user_id not in dict_user_list_actions_lowerH:
                            #   dict_user_list_actions_lowerH[user_id]= []
     
                         #  if action != None:
                            #   dict_user_list_actions_lowerH[user_id].append(action)  
                            #   dict_dict_user_region_list_actions[user_id][region].append(action)


                             
           
            # if S > 5 and S <=10:    #higherHarmony
                  # if T >=5 and T <10:
                    #  if S > T: 
                        #  region= "higherH"
                        #  if user_id not in dict_user_list_actions_higherH:
                         #     dict_user_list_actions_higherH[user_id]= []
     
                        #  if action != None:
                          #    dict_user_list_actions_higherH[user_id].append(action)
                           #   dict_dict_user_region_list_actions[user_id][region].append(action)


            
            if S >= 0 and S < 5:
                    if T > 10 and T <=15:    #PD
                        region= "PD"
                        if user_id not in dict_user_list_actions_PD:
                            dict_user_list_actions_PD[user_id]= []
     
                        if action != None:
                            dict_user_list_actions_PD[user_id].append(action)
                            dict_dict_user_region_list_actions[user_id][region].append(action)

                            list_PD_all.append(action)


   
           
           #  if S >= 0 and S < 5:   #higherPD
                   #  if T > 10 and T <=15:
                      #  if S >= -10 + T:   
                         #   region= "higherPD"
                         #   if user_id not in dict_user_list_actions_higherPD:
                            #    dict_user_list_actions_higherPD[user_id]= []
     
                          #  if action != None:
                          #      dict_user_list_actions_higherPD[user_id].append(action)
                          #      dict_dict_user_region_list_actions[user_id][region].append(action)


              
            # if S >= 0 and S < 5:    #lowerPD
                   #  if T > 10 and T <=15:
                      #  if S < -10 + T:    
                         # region= "lowerPD"
                        #  if user_id not in dict_user_list_actions_lowerPD:
                            #  dict_user_list_actions_lowerPD[user_id]= []
     
                         # if action != None:
                           #   dict_user_list_actions_lowerPD[user_id].append(action)
                            #  dict_dict_user_region_list_actions[user_id][region].append(action)


               
            if S >= 0 and S < 5:    #SH
                if T >= 5 and T <10: 
                    region= "SH"
                    if user_id not in dict_user_list_actions_SH:
                        dict_user_list_actions_SH[user_id]= []
     
                    if action != None:
                        dict_user_list_actions_SH[user_id].append(action)
                        dict_dict_user_region_list_actions[user_id][region].append(action)


                        list_SH_all.append(action)
  

            if S > 5 and S <= 10:     #SD
                if T > 10 and T <=15:  
                    region= "SD"    
                    if user_id not in dict_user_list_actions_SD:
                        dict_user_list_actions_SD[user_id]= []
                        
                    if action != None:
                        dict_user_list_actions_SD[user_id].append(action)
                        dict_dict_user_region_list_actions[user_id][region].append(action)

                        list_SD_all.append(action)


            if action != None:                    
                dict_region_list_all_actions[region].append(action)
                dict_SminusT_group_list_all_actions[SminusT_group].append(action)


                dict_region_list_actions[region].append(action)
                dict_SminusT_group_list_actions[SminusT_group].append(action)



    ###### end loop over user_ids in the main dict   



    print "\navg cooperation values:"
    print "H:", numpy.mean(list_H_all),"  SD:",numpy.std(list_H_all), " SEM:",scipy.stats.sem(list_H_all)
    print "SD:", numpy.mean(list_SD_all)," SD:",numpy.std(list_SD_all), " SEM:",scipy.stats.sem(list_SD_all)
    print "SH:", numpy.mean(list_SH_all)," SD:",numpy.std(list_SH_all), " SEM:",scipy.stats.sem(list_SH_all)
    print "PD:", numpy.mean(list_PD_all)," SD:",numpy.std(list_PD_all), " SEM:",scipy.stats.sem(list_PD_all)

    print "ALL:", numpy.mean(list_all_actions)," SD:",numpy.std(list_all_actions), " SEM:",scipy.stats.sem(list_all_actions),"\n\n"

    #### i generate a RANDOMIZED  version of the data  (same events, randomized by people and regions)
    dict_dict_user_region_list_actions_random={}   
    dict_dict_user_SminusT_list_actions_random={}
    dict_user_id_type_random={}
    valid=0.
    list_unclassified=[]

    list_rationals_rand=[]
    list_altruists_rand=[]
    list_mostly_def_rand=[]
    list_weirdos_rand=[]

    for user_id in  list_all_users:  
        dict_dict_user_region_list_actions_random[user_id]={}      

        for region in list_regions:             
            dict_dict_user_region_list_actions_random[user_id][region]=[]
            
            # every user has as many (random) actions in each region as real actions             
            for i in range(len(dict_dict_user_region_list_actions[user_id][region])): 
 
                if flag_randomization=="by_region":
                    random_action=random.choice(dict_region_list_all_actions[region]) # sampling with replacement   
                elif flag_randomization=="total":
                    random_action=random.choice(list_all_actions) # sampling with replacement          

                dict_dict_user_region_list_actions_random[user_id][region].append(random_action)

     
      
        dict_dict_user_SminusT_list_actions_random[user_id]={}      
        for SminusT_group in list_SminusT_group:
            dict_dict_user_SminusT_list_actions_random[user_id][SminusT_group]=[]

            for i in range(len(dict_dict_user_SminusT_list_actions)):

                
                if flag_randomization=="by_region":                    
                      random_action=random.choice(dict_SminusT_group_list_all_actions[SminusT_group])                
                elif flag_randomization=="total":
                    random_action=random.choice(list_all_actions)   # sampling with replacement               

                dict_dict_user_SminusT_list_actions_random[user_id][SminusT_group].append(random_action)



        dict_user_id_type_random[user_id]="NA"
        
        list_H_rand=[]
        list_SD_rand=[]
        list_SH_rand=[]
        list_PD_rand=[]

       
        try:
            list_H_rand =  dict_dict_user_region_list_actions_random[user_id]["H"]
        except KeyError:   pass

        try:
            list_SD_rand = dict_dict_user_region_list_actions_random[user_id]["SD"]
        except KeyError: pass  
        
        try:
            
            list_SH_rand = dict_dict_user_region_list_actions_random[user_id]["SH"]
        except KeyError: pass  
        
        try:
            list_PD_rand = dict_dict_user_region_list_actions_random[user_id]["PD"]
        except KeyError:  pass



        if len(list_H_rand) >0   and len(list_PD_rand) >0:
            valid +=1.
       
            if 0. not in list_H_rand   and 1.0 not in list_PD_rand:
                list_rationals_rand.append(user_id)
                dict_user_id_type_random[user_id]="rational"
                
            elif  0. not in list_H_rand   and 1. in list_PD_rand:            
                list_altruists_rand.append(user_id)
                dict_user_id_type_random[user_id]="altruist"
                
            elif  1. not in list_PD_rand   and 0. in list_H_rand:
                list_mostly_def_rand.append(user_id)
                dict_user_id_type_random[user_id]="mostly_defector"
                
            elif  1. in list_PD_rand  and 0. in list_H_rand:
                list_weirdos_rand.append(user_id)
                dict_user_id_type_random[user_id]="weirdo"
            else:
                print "unclassified player!!"
                raw_input()
        else:
            dict_user_id_type_random[user_id]="NA"

     



    print "rand valid (with games both in H and PD):", valid

    print  "rand rationals", len(list_rationals_rand),  float(len(list_rationals_rand))/ valid*100.
    print  "rand altruists", len(list_altruists_rand),  float(len(list_altruists_rand))/ valid*100.
    print  "rand mostly defectors", len(list_mostly_def_rand),  float(len(list_mostly_def_rand))/ valid*100.
    print  "rand weirdos", len(list_weirdos_rand),  float(len(list_weirdos_rand))/ valid*100.



# several randomizations   TOTAL:
#rand rationals 12 2.43902439024     8 1.62601626016          5 1.0162601626         15 3.0487804878       5 1.0162601626
#rand altruists 81 16.4634146341     67 13.6178861789         62 12.6016260163       64 13.0081300813      62 12.6016260163
#rand mostly defectors 82 16.66666    87 17.6829268293         75 15.243902439       79 16.0569105691      75 15.243902439
#rand weirdos 317 64.4308943089     330 67.0731707317         350  71.1382113821       334 67.8861788618   350 71.1382113821




# several randomizations   BY REGION:

# rand rationals 66 13.4146341463      60 12.1951219512    68 13.821138      58 11.78861  
# rand altruists 196 39.837398374      225 45.7317073171    197 40.04065     200 40.65040
# rand mostly defectors 62 12.601626   101 20.5284552846    75 15.2439       61 12.39837 
# rand weirdos 168 34.1463414634        109 22.1544715447   152 30.894308     173 35.16260





#valid (with games both in H and PD): 492.0

#rationals 128 26.0162601626
#altruists 154 31.3008130081
#mostly defectors 101 20.5284552846
#weirdos 109 22.1544715447



   ######## i get the list of users in Rationals, Altruists, Mostly defectors and Weirdos
    
    list_rationals=[]
    list_altruists=[]
    list_mostly_def=[]
    list_weirdos=[]

    valid=0.
    dict_user_id_type={}
    for user_id in   list_all_users:   #list_valid_users:
        dict_user_id_type[user_id]="NA"
        

        list_H=[]
        list_SD=[]
        list_SH=[]
        list_PD=[]

       
        try:
            list_H = dict_user_list_actions_H[user_id]
        except KeyError: 
            pass

        try:
            list_SD = dict_user_list_actions_SD[user_id]
        except KeyError: pass  
        
        try:
            
            list_SH = dict_user_list_actions_SH[user_id]
        except KeyError: pass  
        
        try:
            list_PD = dict_user_list_actions_PD[user_id]
        except KeyError:  
            pass


        if len(list_H) >0   and len(list_PD) >0:
            valid +=1.
       
            if 0. not in list_H   and 1.0 not in list_PD:
                list_rationals.append(user_id)
                dict_user_id_type[user_id]="rational"
                
            elif  0. not in list_H   and 1. in list_PD:            
                list_altruists.append(user_id)
                dict_user_id_type[user_id]="altruist"
                
            elif  1. not in list_PD   and 0. in list_H:
                list_mostly_def.append(user_id)
                dict_user_id_type[user_id]="mostly_defector"
                
            elif  1. in list_PD  and 0. in list_H:
                list_weirdos.append(user_id)
                dict_user_id_type[user_id]="weirdo"
            else:
                print "unclassified player!!"
                raw_input()
        else:
            dict_user_id_type[user_id]="NA"
            list_unclassified.append(user_id)

    print      
    print "valid (with games both in H and PD):", valid

    print  "rationals", len(list_rationals),  float(len(list_rationals))/ valid*100.
    print  "altruists", len(list_altruists),  float(len(list_altruists))/ valid*100.
    print  "mostly defectors", len(list_mostly_def),  float(len(list_mostly_def))/ valid*100.
    print  "weirdos", len(list_weirdos),  float(len(list_weirdos))/ valid*100.

    print "# unclassified players", len(list_unclassified)


    pickle.dump(list_rationals, open(pickle_file_rationals, 'wb'))
    print "written pickle:", pickle_file_rationals

    pickle.dump(list_altruists, open(pickle_file_altruists, 'wb'))
    print "written pickle:", pickle_file_altruists

    pickle.dump(list_mostly_def, open(pickle_file_mostly_def, 'wb'))
    print "written pickle:", pickle_file_mostly_def

    pickle.dump(list_weirdos, open(pickle_file_weirdos, 'wb'))
    print "written pickle:", pickle_file_weirdos


    print 

    dict_type_player_numerical_value={"rational":0.0001,"altruist":0.3334,"mostly_defector":0.6667,"weirdo":1.0001,"NA":"nan"}



    ##### file for clustering analysis by quadrants  
    print >> file_cluster1, "user_id", "avg_tot_coop" ,
    for region in list_regions:
        print >> file_cluster1, region,

    print >> file_cluster1,  "S-T[-15,-10)","S-T[-10,-5)","S-T[-5,0)", "S-T[0,5]","type_player","type_player_numerical"


    for user_id in list_all_users:  
         
        print >> file_cluster1, user_id,  numpy.mean(dict_user_list_actions[user_id])+small_additive_cte,
        for region in list_regions:
            print  >> file_cluster1, numpy.mean(dict_dict_user_region_list_actions[user_id][region])+small_additive_cte,
           

        for SminusT_group in list_SminusT_group:
            if SminusT_group in dict_dict_user_SminusTgroup_list_actions[user_id]:               
                print  >> file_cluster1, numpy.mean(dict_dict_user_SminusTgroup_list_actions[user_id][SminusT_group])+small_additive_cte,
            else:               
                print >> file_cluster1, "NA",
               
        print   >> file_cluster1, dict_user_id_type[user_id],float(dict_type_player_numerical_value[dict_user_id_type[user_id]])

      

    print "written file:",clustering_filename1


   


    for region in dict_region_list_actions:
       
        print region,len( dict_region_list_actions[region]), numpy.mean(dict_region_list_actions[region])


    print 
    for SminusT_group in  list_SminusT_group:
        print  SminusT_group, len(dict_SminusT_group_list_actions[SminusT_group]), numpy.mean(dict_SminusT_group_list_actions[SminusT_group])



    ##### file for RANDOMIZED clustering analysis by quadrants    
    print >> file_cluster5, "user_id",
    for region in list_regions:
        print >> file_cluster5, region, 

    print >> file_cluster5,  "S-T[-15,-10)","S-T[-10,-5)","S-T[-5,0)", "S-T[0,5]","type_player","type_player_numerical"


    for user_id in list_all_users:  
         
        print >> file_cluster5, user_id, 
        for region in list_regions:
            print  >> file_cluster5, numpy.mean(dict_dict_user_region_list_actions_random[user_id][region])+small_additive_cte,
           

        for SminusT_group in list_SminusT_group:
            if SminusT_group in dict_dict_user_SminusT_list_actions_random[user_id]:               
                print  >> file_cluster5, numpy.mean(dict_dict_user_SminusT_list_actions_random[user_id][SminusT_group])+small_additive_cte,
            else:               
                print >> file_cluster5, "NA",

               
        print   >> file_cluster5, dict_user_id_type_random[user_id],float(dict_type_player_numerical_value[dict_user_id_type_random[user_id]])
      

    print "written file:",clustering_filename5















     ##### file for clustering analysis by S-T values   
    print >> file_cluster2, "user_id", "  <c> at S-T=-15",  "  <c> at S-T=-14",  "  <c> at S-T=-13",  "  <c> at S-T=-12",  "  <c> at S-T=-11",  "  <c> at S-T=-10",  "  <c> at S-T=-9",  "  <c> at S-T=-8",  "  <c> at S-T=-7",  "  <c> at S-T=-6",  "  <c> at S-T=-5", "  <c> at S-T=-4",  "  <c> at S-T=-3",  "  <c> at S-T=-2",  "  <c> at S-T=-1",  "  <c> at S-T=0",  "  <c> at S-T=1",  "  <c> at S-T=2",  "  <c> at S-T=3",  "  <c> at S-T=4",  "  <c> at S-T=5"
    for user_id in list_all_users:   
        print >> file_cluster2, user_id,
        for SminusT in list_SminusT:
            if SminusT in dict_dict_user_SminusT_list_actions[user_id]:               
                print  >> file_cluster2, numpy.mean(dict_dict_user_SminusT_list_actions[user_id][SminusT]),#+small_additive_cte,
            else:               
                print >> file_cluster2, "NA",
        print >> file_cluster2, ""
       
    print "written file:", clustering_filename2








    ######### to get the distance matrix between pair of players
    list_incomplete_users=[]

    dict_user_list_4values={}  # 4 values of coop. in the four quadrants
    for user_id in dict_dict_user_region_list_actions:
      #  print user_id, dict_dict_user_region_list_actions[user_id]["H"], dict_dict_user_region_list_actions[user_id]["SD"], dict_dict_user_region_list_actions[user_id]["SH"], dict_dict_user_region_list_actions[user_id]["PD"]
        dict_user_list_4values[user_id]=[]
        dict_user_list_4values[user_id].append(numpy.mean(dict_dict_user_region_list_actions[user_id]["H"]))
        dict_user_list_4values[user_id].append(numpy.mean(dict_dict_user_region_list_actions[user_id]["SD"]))
        dict_user_list_4values[user_id].append(numpy.mean(dict_dict_user_region_list_actions[user_id]["SH"]))
        dict_user_list_4values[user_id].append(numpy.mean(dict_dict_user_region_list_actions[user_id]["PD"]))
     
        if len(dict_dict_user_region_list_actions[user_id]["H"])==0:           
            dict_dict_user_region_list_actions[user_id]["H"]=None           
            list_incomplete_users.append(user_id)

        if len(dict_dict_user_region_list_actions[user_id]["SD"])==0:
            dict_dict_user_region_list_actions[user_id]["SD"]=None
            list_incomplete_users.append(user_id)
        if len(dict_dict_user_region_list_actions[user_id]["SH"])==0:
            dict_dict_user_region_list_actions[user_id]["SH"]=None
            list_incomplete_users.append(user_id)
        if len(dict_dict_user_region_list_actions[user_id]["PD"])==0:
            dict_dict_user_region_list_actions[user_id]["PD"]=None
            list_incomplete_users.append(user_id)


    list_valid_users= list(set(dict_user_list_4values.keys())-set(list_incomplete_users))

    print "# valid users:",len(list_valid_users)
    for  user1 in list_valid_users:

        for user2 in list_valid_users:           
                if user1 != user2:
                    
                    x1=dict_user_list_4values[user1][0]
                    x2=dict_user_list_4values[user2][0]
                      
                    y1=dict_user_list_4values[user1][1]
                    y2=dict_user_list_4values[user2][1]
                    
                    z1=dict_user_list_4values[user1][2]
                    z2=dict_user_list_4values[user2][2]
                    
                    w1=dict_user_list_4values[user1][3]
                    w2=dict_user_list_4values[user2][3]
                                  

                    dist=math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2) + (w1-w2)*(w1-w2))
                     
                    
                    print >> file_cluster3, dist,
                else:
                    print >> file_cluster3, 0,

        print >> file_cluster3,""


    file_cluster3.close()
    print "written file:", clustering_filename3





    








######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

