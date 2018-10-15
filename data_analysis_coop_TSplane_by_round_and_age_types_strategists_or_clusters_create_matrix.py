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


    R=10
    P=5


    #######  to select results only from given rounds  (both ends included)
    min_round=1
    max_round=18






    type_strategists="clusters"  #  altruists   rationals   mostly_def    weirdos  or "clusters"    "all_users"

    TOTcluster_num=5

    cluster_num=1




    ######### input file
    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)



    filename_strategists="../Results/list_"+str(type_strategists)+".pickle"
                         

    
    if type_strategists== "clusters":  # type of strategists from the kmeans analysis
                              
        #        filename_strategists="../Results/list_clusters_kmeans"+str(TOTcluster_num)+"_dist_notypes-"+str(cluster_num)+".pickle"


        filename_strategists="../Results/Niter_clustering/list_clusters_kmeans"+str(TOTcluster_num)+"-"+str(cluster_num)+"_109iter.pickle"

                              
        type_strategists=type_strategists+str(TOTcluster_num)+"_"+str(cluster_num)




    list_strategists=pickle.load(open(filename_strategists, 'rb'))
    print "filename strategists:", filename_strategists
   
    ######### 





    ######### output files 
   
    output_filename1="../Results/Cooperation_TSplane_"+str(type_strategists)+"_kmeanspython.dat"
    output1= open(output_filename1,'wt')


    output_filename2="../Results/SEM_cooperation_TSplane_"+str(type_strategists)+"_kmeanspython.dat"
    output2= open(output_filename2,'wt')

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

    
    dict_TSplane_list_payoff_norm={}  # normalized payoff by the maximun possible in that TS point
    dict_TSplane_avg_payoff_norm={}
    dict_TSplane_std_payoff_norm={}
    dict_TSplane_sem_payoff_norm={}  

    dict_TSplane_num_actions={}  







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
       
       
       if user_id in list_strategists:


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
                              dict_TSplane_list_payoff_norm[punto_TS].append(payoff_norm)
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

                            dict_TSplane_list_payoff_norm[punto_TS]=[]
                            dict_TSplane_list_payoff_norm[punto_TS].append(payoff_norm)



    ###### done reading the data


    ####### the the avg cooperation per TS point
    for punto_TS in sorted(dict_TSplane_list_actions):

      
        
        dict_TSplane_avg_coop[punto_TS]=numpy.mean(dict_TSplane_list_actions[punto_TS])
        dict_TSplane_std_coop[punto_TS]=numpy.std(dict_TSplane_list_actions[punto_TS])
        dict_TSplane_sem_coop[punto_TS]=stats.sem(dict_TSplane_list_actions[punto_TS])   # standard error =std / sqrt(num points)



        dict_TSplane_num_actions[punto_TS]=len(dict_TSplane_list_actions[punto_TS])


  


   
    print_values_dict_for_matrix_plotting(dict_TSplane_avg_coop, output_filename1)   
    print_values_dict_for_matrix_plotting(dict_TSplane_sem_coop,output_filename2)
  








######################################

######################################


def print_values_dict_for_matrix_plotting(dict_TSplane_avg_values, filename):

    filename=filename.split(".dat")[0]+"_MATRIX.dat"
    output= open(filename,'wt')

    filename2="../Results/SminusT_MATRIX.dat"
    output2= open(filename2,'wt')




    list_T_values=[]
    list_S_values=[]
    for key in dict_TSplane_avg_values:
        T=key[0]
        S=key[1]

        if T not in list_T_values:
            list_T_values.append(T)
        if S not in list_S_values:
            list_S_values.append(S)

    listT=sorted(list_T_values)
    listT.reverse()

    listS=sorted(list_S_values)
    listS.reverse()

    for T in listT:
        for S in listS:
            tupla=(T,S)
            try:
                print >> output, dict_TSplane_avg_values[tupla],
                print >> output2, S-T,              

            except KeyError:
                print >> output, "nan",
                print >> output2, S-T, 
                print "ojo! missing (T,S):" ,tupla

        print  >> output
        print  >> output2
       
    output.close()
    print "written matrix file:", filename

    output2.close()
    print "written matrix file:", filename2





######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

