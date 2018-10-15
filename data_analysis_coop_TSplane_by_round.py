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



    #######  to select results only from given rounds  (both ends included)
    min_round=1
    max_round=18




    ######### input file
    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)
    ######### 



    ######### output files
    Nbins_ages=15
    name_h_ages="../Results/histogram_ages.dat"

    Nbins_payoffs=20
    name_h_payoffs="../Results/histogram_payoffs_"+str(pupulation_age)+"_ages_rounds"+str(min_round)+"_"+str(max_round)+".dat"



    output_filename1="../Results/Cooperation_TSplane_"+str(pupulation_age)+"_ages_rounds"+str(min_round)+"_"+str(max_round)+".dat"
    output1= open(output_filename1,'wt')



    output_filename2="../Results/Racionality_TSplane_"+str(pupulation_age)+"_ages_rounds"+str(min_round)+"_"+str(max_round)+".dat"
    output2= open(output_filename2,'wt')



    output_filename3="../Results/Ambition_TSplane_"+str(pupulation_age)+"_ages_rounds"+str(min_round)+"_"+str(max_round)+".dat"
    output3= open(output_filename3,'wt')




    ######### 




 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]


    dict_TSplane_list_actions={}
    dict_TSplane_avg_coop={}
    dict_TSplane_std_coop={}
    dict_TSplane_sem_coop={}   # error of the mean  =std/ sqrt(num points)

    dict_TSplane_list_rationality={}
    dict_TSplane_avg_rationality={}
    dict_TSplane_std_rationality={}


    dict_TSplane_list_ambition={}
    dict_TSplane_avg_ambition={}
    dict_TSplane_std_ambition={}


    dict_TSplane_list_payoff={}
    dict_TSplane_avg_payoff={}
    dict_TSplane_std_payoff={}
    dict_TSplane_sem_payoff={}  




    list_ages=[]
    list_payoff_tot=[]  # calculated (by Jordi) up to round #13



    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
       
        payoff_total=float(dictionary['guany_total'])   # this is calculated only up to round #13  !!
        partida=dictionary['partida']


        list_payoff_tot.append(payoff_total)



        genero=dictionary['genere']
        if genero =="h":
            genero=1            
        elif genero == "d":
            genero=0

        num_elecciones=dictionary['num_eleccions']
        age=int(dictionary['edat'])
        avg_racionalidad=dictionary['rationality']
        avg_ambicion=dictionary['ambition']
        num_rondas=len(dictionary['rondes'])
        nickname=unidecode(dictionary['nickname']).replace(" ", "_")
        user_id=dictionary['id']

       
      
        list_dict_rondas=dictionary['rondes']

      


        list_ages.append(age)


        for dict_ronda in list_dict_rondas:
          ##  cada diccionario de ronda tiene: {'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}

            payoff=float(dict_ronda['guany'])
            payoff_oponent=dict_ronda['guany_oponent']
            rationality=dict_ronda['rationality']
            ambition=dict_ronda['ambition']

            if rationality !=None:
                rationality=float(rationality)*100.              
            if ambition !=None:
                ambition=float(ambition)*100.
     


            round_number=dict_ronda['numronda']


            action=dict_ronda['seleccio']
            if action =="C":
                action=1.
            elif action=="D":
                action=0.
            # si no ha elegido nada, es None
              

            num_ronda=dict_ronda['numronda']
            quadrant=dict_ronda['cuadrant'].replace(" ", "_").replace("'", "")

                
            action_oponent=dict_ronda['seleccio_oponent']
            if action_oponent =="C":
                action_oponent=1.
            elif action_oponent=="D":
                action_oponent=0.           
             # si no ha elegido nada, es None
           

            oponent_id=dict_ronda['oponent']
         
            T=int(dict_ronda['T'])
            S=int(dict_ronda['S'])

            punto_TS=(T,S)

          
            if punto_TS in  dict_TSplane_list_actions:
                if action !=None:
                      if age >= min_age_threshold and age <=  max_age_threshold:
                          if round_number <= max_round   and round_number >= min_round :

                              dict_TSplane_list_actions[punto_TS].append(action)  # 1:C,  0:D
                              if rationality !=None:
                                  dict_TSplane_list_rationality[punto_TS].append(rationality)
                              if ambition !=None:
                                  dict_TSplane_list_ambition[punto_TS].append(ambition)

                          dict_TSplane_list_payoff[punto_TS].append(payoff)

            else:
                if action !=None:

                    if age >= min_age_threshold and age <=  max_age_threshold:
                        if round_number <= max_round   and round_number >= min_round :

                            dict_TSplane_list_actions[punto_TS]=[]          
                            dict_TSplane_list_actions[punto_TS].append(action)

                            if rationality !=None:
                                dict_TSplane_list_rationality[punto_TS]=[]
                                dict_TSplane_list_rationality[punto_TS].append(rationality)

                            if ambition !=None:
                                dict_TSplane_list_ambition[punto_TS]=[]
                                dict_TSplane_list_ambition[punto_TS].append(ambition)

   
                            dict_TSplane_list_payoff[punto_TS]=[]
                            dict_TSplane_list_payoff[punto_TS].append(payoff)

          
             
    old_T=None
    ####### the the avg cooperation per TS point
    for punto_TS in sorted(dict_TSplane_list_actions):
        
        dict_TSplane_avg_coop[punto_TS]=numpy.mean(dict_TSplane_list_actions[punto_TS])
        dict_TSplane_std_coop[punto_TS]=numpy.std(dict_TSplane_list_actions[punto_TS])
        dict_TSplane_sem_coop[punto_TS]=stats.sem(dict_TSplane_list_actions[punto_TS])   # standard error =std / sqrt(num points)




        dict_TSplane_avg_payoff[punto_TS]=numpy.mean(dict_TSplane_list_payoff[punto_TS])
        dict_TSplane_std_payoff[punto_TS]=numpy.std(dict_TSplane_list_payoff[punto_TS])
        dict_TSplane_sem_payoff[punto_TS]=stats.sem(dict_TSplane_list_payoff[punto_TS])


        if old_T != punto_TS[0]:
            print >> output1
           

        print >> output1,punto_TS[0],punto_TS[1], dict_TSplane_avg_coop[punto_TS], dict_TSplane_std_coop[punto_TS], dict_TSplane_sem_coop[punto_TS]
        old_T=punto_TS[0]



    old_T=None
    for punto_TS in sorted(dict_TSplane_list_rationality):
        
        dict_TSplane_avg_rationality[punto_TS]=numpy.mean(dict_TSplane_list_rationality[punto_TS])
        dict_TSplane_std_rationality[punto_TS]=numpy.std(dict_TSplane_list_rationality[punto_TS])

        if old_T != punto_TS[0]:
            print >> output2
          
        print >> output2,punto_TS[0],punto_TS[1], dict_TSplane_avg_rationality[punto_TS], dict_TSplane_std_rationality[punto_TS], dict_TSplane_std_rationality[punto_TS]/numpy.sqrt(len(dict_TSplane_list_rationality[punto_TS]))
        old_T=punto_TS[0]                                                                 



    old_T=None
    for punto_TS in sorted(dict_TSplane_list_ambition):

        dict_TSplane_avg_ambition[punto_TS]=numpy.mean(dict_TSplane_list_ambition[punto_TS])
        dict_TSplane_std_ambition[punto_TS]=numpy.std(dict_TSplane_list_ambition[punto_TS])   

        if old_T != punto_TS[0]:
            print >> output3
                 
        print >> output3,punto_TS[0],punto_TS[1], dict_TSplane_avg_ambition[punto_TS], dict_TSplane_std_ambition[punto_TS],  dict_TSplane_std_ambition[punto_TS]/numpy.sqrt(len(dict_TSplane_list_ambition[punto_TS]))

        old_T=punto_TS[0]                                                                 
        old_T=punto_TS[0]





    histograma_bines_gral.histograma_bins(list_ages,Nbins_ages, name_h_ages)   #x_position , norm_count, count, norm_cumulat_count, cumulat_count ,  float(hist[b])/float(len(lista))   
    
    histograma_bines_gral.histograma_bins(list_payoff_tot,Nbins_payoffs, name_h_payoffs)  






    output1.close()
    print "written output datafile:", output_filename1
    print "written output datafile:", output_filename2
    print "written output datafile:", output_filename3
######################################

######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

