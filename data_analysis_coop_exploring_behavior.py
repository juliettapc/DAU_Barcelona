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




    ######### input file
    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)
    ######### 



    ######### output files
    Nbins_fraction_coop=15
    name_h_fraction_coop="../Results/histogram_fraction_coop_tot_users.dat"

    Nbins_tot_payoff=20
    name_h_tot_payoff="../Results/histogram_tot_payoff_users.dat"

    Nbins_avg_payoff=20
    name_h_avg_payoff="../Results/histogram_avg_payoff_users.dat"



    output_filename1="../Results/Scatter_plot_cooperation_tot_and_avg_payoff.dat"
    output1= open(output_filename1,'wt')

    ######### 




 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]
    
    num_valid_actions=0.
    num_lower_H_actions=0
    num_higher_H_actions=0
    coop_actions_higher  =0   
    coop_actions_lower  =0   

    dict_user_id_list_coop={}
    dict_user_id_list_tot_payoff={}

    dict_user_id_gender={}

    dict_user_list_actions_in_lower_Harmony={}
    dict_user_avg_coop_in_lower_Harmony={}

    dict_user_id_tot_numelections={}

    dict_user_id_list_strat={}

    num_users=float(len(master_list))

    list_cooperators_in_lower_Harmony=[]
    list_cooperators_in_higher_Harmony=[]



    list_defectors_in_lower_Harmony=[]
   
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

        dict_user_id_gender[user_id]=gender

        num_elecciones=int(dictionary['num_eleccions'])
        age=int(dictionary['edat'])
        avg_racionalidad=dictionary['rationality']
        avg_ambicion=dictionary['ambition']
        num_rondas=len(dictionary['rondes'])
      
     
        dict_user_id_tot_numelections[user_id]=num_elecciones


        if user_id not in dict_user_id_list_coop:
            dict_user_id_list_coop[user_id]=[]
            dict_user_id_list_tot_payoff[user_id]=[]
            dict_user_id_list_strat[user_id]=[]

      
        list_dict_rondas=dictionary['rondes']

       


        for dict_ronda in list_dict_rondas:
          ##  cada diccionario de ronda tiene: {'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}



            T=int(dict_ronda['T'])
            S=int(dict_ronda['S'])

            list_four_possible_values=[P,R,T,S]

            punto_TS=(T,S)



            try:
                payoff=float(dict_ronda['guany'])
                payoff_norm=float(dict_ronda['guany'])/float(max(list_four_possible_values))
            except TypeError:
                payoff=dict_ronda['guany']  # if payoff is None



            payoff_oponent=dict_ronda['guany_oponent']
            rationality=dict_ronda['rationality']
            ambition=dict_ronda['ambition']

        


            round_number=dict_ronda['numronda']


            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
            # si no ha elegido nada, es None
            

            if action != None:
                num_valid_actions +=1
                if user_id not in dict_user_list_actions_in_lower_Harmony:
                    dict_user_list_actions_in_lower_Harmony[user_id]= []
       
  
            if action != None:
                dict_user_id_list_coop[user_id].append(action)

            if payoff != None:
                dict_user_id_list_tot_payoff[user_id].append(payoff)




            num_ronda=dict_ronda['numronda']
            quadrant=dict_ronda['cuadrant'].replace(" ", "_").replace("'", "")

                
            action_oponent=dict_ronda['seleccio_oponent']
            if action_oponent =="C":
                action_oponent=1.
            elif action_oponent=="D":
                action_oponent=0.           
             # si no ha elegido nada, es None
           

            oponent_id=dict_ronda['oponent']
         
           
            random_action=random.choice([0,1])

           
          #  print "\nR:",R, " S:",S, " T:", T,  " P:",P, " action:",action, " payoff:",payoff
          



            strat=None
            strat1=None
            if action == 1:
                if R== max(R, S, T, P) or    S == max(R, S, T, P):
                    strat1="max_payoff"

            elif action ==0:
                if T == max(R, S, T, P) or    T == max(R, S, T, P):
                    strat1="max_payoff"

           



            max_diff=max(R-R, S-T, T-S, P-P)
            min_diff=min(R-R, S-T, T-S, P-P)
          

            strat2=None
            if action == 1:
                if   S-T  == max_diff:
                    strat2="max_diff"

            elif action ==0:
                if T-S == max_diff:
                    strat2="max_diff"




            if strat1 != None and  strat2  != None:
                if "payoff" in strat1:
                    strat=strat1+" "+strat2
                else:
                    strat=strat2+" "+strat1                
            else:
                if strat1 == None:
                    strat =strat2
                else:
                    strat =strat1
           
         

          

            dict_user_id_list_strat[user_id].append(strat)
                             
               

            if S >= 5 and S <=10:
                if T >=5 and T <=10:
                    if S <= T:  # the lower triangle of the Harmony game:
                        if action ==1:
                            if user_id not in list_cooperators_in_lower_Harmony:
                                list_cooperators_in_lower_Harmony.append(user_id)                                  
                            coop_actions_lower +=1 
                        elif action ==0:
                             if user_id not in list_defectors_in_lower_Harmony:
                                 list_defectors_in_lower_Harmony.append(user_id)
     
                        if action != None:
                            dict_user_list_actions_in_lower_Harmony[user_id].append(action)  
                            num_lower_H_actions +=1


                    else: # the upper triangle of the Harmony game:
                        if action ==1:
                            if user_id not in list_cooperators_in_higher_Harmony:                           
                                list_cooperators_in_higher_Harmony.append(user_id)
                            coop_actions_higher +=1   
                        num_higher_H_actions +=1

    ###### end loop over lines in the main dict
    list_frac_coop_users=[]
    list_tot_payoff_users=[]
    list_avg_payoff_users=[]
    dict_common_strat_num_users={}
    dict_strat_num_users={}

    for user_id in dict_user_id_list_coop:       
        fract_coop=numpy.mean(dict_user_id_list_coop[user_id])
        list_frac_coop_users.append(fract_coop)
       

        tot_payoff=sum(dict_user_id_list_tot_payoff[user_id])
        list_tot_payoff_users.append(tot_payoff)

        avg_payoff=numpy.mean(dict_user_id_list_tot_payoff[user_id])
        list_avg_payoff_users.append(avg_payoff)


        common_strat= max(set(dict_user_id_list_strat[user_id]), key=dict_user_id_list_strat[user_id].count)   # most common element in the list
        print >> output1, fract_coop, tot_payoff,avg_payoff,   dict_user_id_gender[user_id], dict_user_id_tot_numelections[user_id]

        

        ##### counting most common strategy per user
        if common_strat not in dict_common_strat_num_users:
            dict_common_strat_num_users[common_strat]=0
        dict_common_strat_num_users[common_strat] +=1

        ######## counting all strategies
        for strat in dict_user_id_list_strat[user_id]:
            if strat  not in dict_strat_num_users:
                dict_strat_num_users[strat] =0
            dict_strat_num_users[strat] +=1


    list_avg_cooperators_lower_H=[]
    for user_id in dict_user_list_actions_in_lower_Harmony:
         dict_user_avg_coop_in_lower_Harmony[user_id] = numpy.mean(dict_user_list_actions_in_lower_Harmony[user_id])
  
         print user_id, dict_user_list_actions_in_lower_Harmony[user_id],dict_user_avg_coop_in_lower_Harmony[user_id]

         if dict_user_avg_coop_in_lower_Harmony[user_id] >0.5:
             list_avg_cooperators_lower_H.append(user_id)


    print len(dict_user_list_actions_in_lower_Harmony), len(list_avg_cooperators_lower_H)
    raw_input()

    histograma_bines_gral.histograma_bins(list_frac_coop_users,Nbins_fraction_coop, name_h_fraction_coop)   #x_position , norm_count, count, norm_cumulat_count, cumulat_count ,  float(hist[b])/float(len(lista))   
    histograma_bines_gral.histograma_bins(list_tot_payoff_users,Nbins_tot_payoff, name_h_tot_payoff)  
    histograma_bines_gral.histograma_bins(list_avg_payoff_users,Nbins_avg_payoff, name_h_avg_payoff)  
    



    output1.close()
    print "written output file:", output_filename1

    print "common strategies within user:"
    for key in  dict_common_strat_num_users:
        print key, dict_common_strat_num_users[key], dict_common_strat_num_users[key]/num_users



    print "\nall strategies:"
    for key in  dict_strat_num_users:
        print key, dict_strat_num_users[key], dict_strat_num_users[key]/num_valid_actions



    print "# items in the pickle:",len(master_list)
    
    print "\n# unique coop in lower Harmony:",len(list_cooperators_in_lower_Harmony), "  # actions in lower H:",num_lower_H_actions, " fract_coop:",  coop_actions_lower/float(num_lower_H_actions)," # avg cooperatos (>0.5) in lower H:",  len(list_avg_cooperators_lower_H)
    
    
    
    
    print "\n# unique defectors in lower Harmony:",len(list_defectors_in_lower_Harmony)
    



    print "\nintersection unique users cooperators and defectors in lower Harmony", len(list(set(list_cooperators_in_lower_Harmony) & set(list_defectors_in_lower_Harmony)))
    
    print "\n# unique coop in higher Harmony:",len(list_cooperators_in_higher_Harmony), "  # actions in higher H:",num_higher_H_actions, " fract_coop:",     coop_actions_higher/float(num_higher_H_actions)
    
    print "  tot # valid actions:",num_valid_actions, "  tot # users:",num_users



    #output2= open("../Results/pickle_cooperators_lower_H.pickle",'wt')
    #pickle.dump(list_avg_cooperators_lower_H, output2)





    ####### i read the file again to compare levels of cooperations for some sets of users

    list_actions_all_users=[]
    list_actions_coop_in_lower_H=[]
    list_actions_NO_coop_in_lower_H=[]

    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
              
        user_id=dictionary['id']

        list_dict_rondas=dictionary['rondes']

        for dict_ronda in list_dict_rondas:


            try:
                payoff=float(dict_ronda['guany'])
                payoff_norm=float(dict_ronda['guany'])/float(max(list_four_possible_values))
            except TypeError:
                payoff=dict_ronda['guany']  # if payoff is None



            payoff_oponent=dict_ronda['guany_oponent']
          

            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
            # si no ha elegido nada, es None
            

            if action != None:
                
                list_actions_all_users.append(action)
                
                if user_id in list_cooperators_in_lower_Harmony:
                    list_actions_coop_in_lower_H.append(action)

                else:
                    list_actions_NO_coop_in_lower_H.append(action)
    print "avg coop all users:", numpy.mean(list_actions_all_users), len(list_actions_all_users),"    avg coop special set:", numpy.mean(list_actions_coop_in_lower_H), len(list_actions_coop_in_lower_H),"    avg coop NO special set:",numpy.mean(list_actions_NO_coop_in_lower_H), len(list_actions_NO_coop_in_lower_H)






######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

