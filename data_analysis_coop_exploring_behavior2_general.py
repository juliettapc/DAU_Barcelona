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

    umbral_coop= 0.75  # to saparate good people from bastards in the lower Harmony
    Niter=5000  # for the bootstrapping


    type_definition="Harmony"       # "lowerPD"  "higherPD"# #   #"higherHarmony"   #"lowerHarmony"  #"SD"  # or "PD" "SH" "Harmony"


    print "Cooperation threshold for good people in", type_definition, umbral_coop
    print "Niter for bootstrapping:", Niter


    ######### input file
    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)
   



    ######### output files  
    pickle_file_good_people="../Results/list_good_guys_"+str(type_definition)+"_threshold_coop"+str(umbral_coop)+".pickle"
    pickle_file_bad_people="../Results/list_bad_guys_"+str(type_definition)+"_threshold_coop"+str(umbral_coop)+".pickle"

    pickle_file_all="../Results/list_all_users.pickle"

    Nbins_avg_coop=20
    name_h_avg_coop="../Results/histogram_general_avg_coop.dat"


    ######### 




 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]
    
    num_valid_actions=0.
    num_actions_in_focus_region=0

    num_coop_actions_in_focus_region =0   

  

    dict_user_list_actions_in_focus_region={}  # that region is either the lower Harmony or the whole PD
    dict_user_avg_coop_in_focus_region={}
 
    dict_user_list_actions={}
    dict_user_avg_coop={}

    num_users=float(len(master_list))

    list_cooperators_in_focus_region=[]   # if the cooperate at least once in the region      
    list_defectors_in_focus_region=[]


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

           

            round_number=dict_ronda['numronda']


            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
            # si no ha elegido nada, es None
            

            if action != None:
                num_valid_actions +=1              

                if user_id not in list_all_users:
                    list_all_users.append(user_id)


            num_ronda=dict_ronda['numronda']
            quadrant=dict_ronda['cuadrant'].replace(" ", "_").replace("'", "")

                

            action_oponent=dict_ronda['seleccio_oponent']
            if action_oponent =="C":
                action_oponent=1.
            elif action_oponent=="D":
                action_oponent=0.           
             # si no ha elegido nada, es None
           


            #### for the general histogram of cooperation
            if user_id not in dict_user_list_actions:
                dict_user_list_actions[user_id]=[]
            if action != None:
                dict_user_list_actions[user_id].append(action) 




            if  type_definition == "Harmony":  

                if S >= 5 and S <=10:
                  if T >=5 and T <=10:                   
                          if user_id not in dict_user_list_actions_in_focus_region:
                            dict_user_list_actions_in_focus_region[user_id]= []

                          if action ==1:
                            if user_id not in list_cooperators_in_focus_region:
                                list_cooperators_in_focus_region.append(user_id)   
                            num_coop_actions_in_focus_region +=1 
                          elif action ==0:
                             if user_id not in list_defectors_in_focus_region:
                                 list_defectors_in_focus_region.append(user_id)

     
                          if action != None:
                            dict_user_list_actions_in_focus_region[user_id].append(action)  
                            num_actions_in_focus_region +=1
               
                                       
            elif  type_definition == "lowerHarmony":  

                if S >= 5 and S <=10:
                  if T >=5 and T <=10:
                     if S <= T:  # the lower triangle of the Harmony game:
                          if user_id not in dict_user_list_actions_in_focus_region:
                            dict_user_list_actions_in_focus_region[user_id]= []

                          if action ==1:
                            if user_id not in list_cooperators_in_focus_region:
                                list_cooperators_in_focus_region.append(user_id)    
                            num_coop_actions_in_focus_region +=1 
                          elif action ==0:
                             if user_id not in list_defectors_in_focus_region:
                                 list_defectors_in_focus_region.append(user_id)

     
                          if action != None:
                            dict_user_list_actions_in_focus_region[user_id].append(action)  
                            num_actions_in_focus_region +=1
                

                             
            elif  type_definition == "higherHarmony":  

                if S >= 5 and S <=10:
                  if T >=5 and T <=10:
                     if S > T:  # the higher triangle of the Harmony game:
                          if user_id not in dict_user_list_actions_in_focus_region:
                            dict_user_list_actions_in_focus_region[user_id]= []

                          if action ==1:
                            if user_id not in list_cooperators_in_focus_region:
                                list_cooperators_in_focus_region.append(user_id)  
                            num_coop_actions_in_focus_region +=1 
                          elif action ==0:
                             if user_id not in list_defectors_in_focus_region:
                                 list_defectors_in_focus_region.append(user_id)

                          if action != None:
                            dict_user_list_actions_in_focus_region[user_id].append(action)  
                            num_actions_in_focus_region +=1
                



            elif type_definition == "PD":    
                if S >= 0 and S <= 5:
                    if T >= 10 and T <=15:

                         if user_id not in dict_user_list_actions_in_focus_region:
                            dict_user_list_actions_in_focus_region[user_id]= []

                         if action ==1:
                            if user_id not in list_cooperators_in_focus_region:
                                list_cooperators_in_focus_region.append(user_id)            
                            num_coop_actions_in_focus_region +=1 
                         elif action ==0:
                             if user_id not in list_defectors_in_focus_region:
                                 list_defectors_in_focus_region.append(user_id)

     
                         if action != None:
                            dict_user_list_actions_in_focus_region[user_id].append(action)  
                            num_actions_in_focus_region +=1



            elif type_definition == "higherPD":    
                if S >= 0 and S <= 5:
                    if T >= 10 and T <=15:
                       if S >= -10 + T:   
                         if user_id not in dict_user_list_actions_in_focus_region:
                            dict_user_list_actions_in_focus_region[user_id]= []


                         if action ==1:
                            if user_id not in list_cooperators_in_focus_region:
                                list_cooperators_in_focus_region.append(user_id)            
                            num_coop_actions_in_focus_region +=1 
                         elif action ==0:
                             if user_id not in list_defectors_in_focus_region:
                                 list_defectors_in_focus_region.append(user_id)

     
                         if action != None:
                            dict_user_list_actions_in_focus_region[user_id].append(action)  
                            num_actions_in_focus_region +=1


            elif type_definition == "lowerPD":    
                if S >= 0 and S <= 5:
                    if T >= 10 and T <=15:
                       if S < -10 + T:    
                         if user_id not in dict_user_list_actions_in_focus_region:
                            dict_user_list_actions_in_focus_region[user_id]= []


                         if action ==1:
                            if user_id not in list_cooperators_in_focus_region:
                                list_cooperators_in_focus_region.append(user_id)            
                            num_coop_actions_in_focus_region +=1 
                         elif action ==0:
                             if user_id not in list_defectors_in_focus_region:
                                 list_defectors_in_focus_region.append(user_id)
     
                         if action != None:
                            dict_user_list_actions_in_focus_region[user_id].append(action)  
                            num_actions_in_focus_region +=1




            elif type_definition == "SH":    
                if S >= 0 and S <= 5:
                    if T >= 5 and T <=10:

                         if user_id not in dict_user_list_actions_in_focus_region:
                            dict_user_list_actions_in_focus_region[user_id]= []

                         if action ==1:
                            if user_id not in list_cooperators_in_focus_region:
                                list_cooperators_in_focus_region.append(user_id)            
                            num_coop_actions_in_focus_region +=1 
                         elif action ==0:
                             if user_id not in list_defectors_in_focus_region:
                                 list_defectors_in_focus_region.append(user_id)
     
                         if action != None:
                            dict_user_list_actions_in_focus_region[user_id].append(action)  
                            num_actions_in_focus_region +=1




            elif type_definition == "SD":    
                if S >= 5 and S <= 10:
                    if T >= 10 and T <=15:

                         if user_id not in dict_user_list_actions_in_focus_region:
                            dict_user_list_actions_in_focus_region[user_id]= []

                         if action ==1:
                            if user_id not in list_cooperators_in_focus_region:
                                list_cooperators_in_focus_region.append(user_id)            
                            num_coop_actions_in_focus_region +=1 
                         elif action ==0:
                             if user_id not in list_defectors_in_focus_region:
                                 list_defectors_in_focus_region.append(user_id)

     
                         if action != None:
                            dict_user_list_actions_in_focus_region[user_id].append(action)  
                            num_actions_in_focus_region +=1










    ###### end loop over user_ids in the main dict   




   
    ######## obtaining the subset of user_id who cooperated > umbral_coop in the focus region

    list_avg_defectors_in_focus_region=[]
    list_avg_cooperators_in_focus_region=[]
    for user_id in dict_user_list_actions_in_focus_region: #over all user_ids who played in that region
         dict_user_avg_coop_in_focus_region[user_id] = numpy.mean(dict_user_list_actions_in_focus_region[user_id])
  
         if dict_user_avg_coop_in_focus_region[user_id] > umbral_coop :
             list_avg_cooperators_in_focus_region.append(user_id)
         else:
             list_avg_defectors_in_focus_region.append(user_id)

  

    ###### for the histogram of general cooperation
    list_avg_coop=[]
    for user_id in dict_user_list_actions:
        list_avg_coop.append(numpy.mean(dict_user_list_actions[user_id]))

    histograma_bines_gral.histograma_bins(list_avg_coop,Nbins_avg_coop, name_h_avg_coop)
   # print "avg coop this group:", numpy.mean(list_avg_coop), "median:",numpy.median(list_avg_coop), min(list_avg_coop),  max(list_avg_coop)
   


    print "# user_ids that play in", type_definition,  len(dict_user_list_actions_in_focus_region), " who cooperated >",umbral_coop*100,"%:", len(list_avg_cooperators_in_focus_region)
  
    

   
    print "# items in the pickle (tot # users):",len(master_list)

    print "\n# unique defectors in",  type_definition, "(defect at least once):",len(list_defectors_in_focus_region), "  # avg-defectors:",len(list_avg_defectors_in_focus_region)
    

    print "\n# unique coop in", type_definition, "(cooperate at least once):",len(list_cooperators_in_focus_region), "  # actions in",  type_definition, ":",num_actions_in_focus_region, " fract_coop:",  num_coop_actions_in_focus_region/float(num_actions_in_focus_region)," # avg cooperators (> coop_threshold) in",  type_definition, ":",  len(list_avg_cooperators_in_focus_region)  , "  # avg-cooperators:" ,len(list_avg_cooperators_in_focus_region)
    
 


   # print "\nintersection unique users cooperators and defectors in lower Harmony", len(list(set(list_cooperators_in_focus_region) & set(list_defectors_in_focus_region)))
    
   
    
    print "  tot # valid actions:",num_valid_actions, "  tot # users:",num_users


    pickle.dump(list_avg_cooperators_in_focus_region, open(pickle_file_good_people, 'wb'))
    print "written pickle:", pickle_file_good_people


    pickle.dump(list_avg_defectors_in_focus_region, open(pickle_file_bad_people, 'wb'))
    print "written pickle:", pickle_file_bad_people







    pickle.dump(list_all_users, open(pickle_file_all, 'wb'))
    print "written pickle:", pickle_file_all





    ####### i read the master dict again to compare levels of cooperations for some sets of users
    list_actions_all_users=[]
    list_actions_coop_in_focus_region=[]
    list_actions_NO_coop_in_focus_region=[]



    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
              
        user_id=dictionary['id']
        list_dict_rondas=dictionary['rondes']

        for dict_ronda in list_dict_rondas:         
          

            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
         
  

            if action != None:                
                list_actions_all_users.append(action)                
                if user_id in list_avg_cooperators_in_focus_region:
                    list_actions_coop_in_focus_region.append(action)
                elif user_id in list_avg_defectors_in_focus_region:
                    list_actions_NO_coop_in_focus_region.append(action)

              

    avg_real_coop_among_coop_in_focus_region=numpy.mean(list_actions_coop_in_focus_region)
    avg_real_coop_among_NONcoop_in_focus_region=numpy.mean(list_actions_NO_coop_in_focus_region)
   


    print "\nAvg coop all users all TS-plane:", numpy.mean(list_actions_all_users), "  tot # actions:",len(list_actions_all_users)
    
    print "\n Bootstrapping..."

    ########## bootstrapping  to see if the cooperators (def as coop > umbral_coop) in focus region are special
    print "\nCooperators in", type_definition," vs all:"
    bootstrapping.zscore(list_actions_all_users, len(list_actions_coop_in_focus_region), Niter,avg_real_coop_among_coop_in_focus_region)
    print "  # users in", type_definition,":", len(list_avg_cooperators_in_focus_region)
    print "Avg coop this set users in all TS-plane:", avg_real_coop_among_coop_in_focus_region,  "  # actions:", len(list_actions_coop_in_focus_region)





    ########## bootstrapping  to see if the defectors (def as coop <umbral_coop)  in focus region are special
    print "\nDefectors in", type_definition, " vs all:"
    bootstrapping.zscore(list_actions_all_users, len(list_actions_NO_coop_in_focus_region), Niter,avg_real_coop_among_NONcoop_in_focus_region)
    print "  # users in", type_definition,":", len(list_avg_defectors_in_focus_region)
    print "Avg coop this set in all TS-plane:",avg_real_coop_among_NONcoop_in_focus_region,  "  # actions:",len(list_actions_NO_coop_in_focus_region)




######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

