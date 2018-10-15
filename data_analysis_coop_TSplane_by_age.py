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

def main():


    pupulation_age="All"   #"young"  # or "adult"   or All

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





    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)




    ######### output files
    Nbins=15
    name_h="../Results/histogram_ages.dat"

    output_filename1="../Results/Cooperation_TSplane_"+str(pupulation_age)+"_ages.dat"
    output1= open(output_filename1,'wt')

    ######### 




 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]


    dict_TSplane_list_actions={}
    dict_TSplane_avg_coop={}
    dict_TSplane_std_coop={}






    list_ages=[]

    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
       
        payoff_total=dictionary['guany_total']
        partida=dictionary['partida']

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

            payoff=dict_ronda['guany']
            payoff_oponent=dict_ronda['guany_oponent']
            rationality=dict_ronda['rationality']
            ambition=dict_ronda['ambition']

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
                          dict_TSplane_list_actions[punto_TS].append(action)  # 1:C,  0:D

            else:
                if action !=None:

                    if age >= min_age_threshold and age <=  max_age_threshold:
                        dict_TSplane_list_actions[punto_TS]=[]          
                        dict_TSplane_list_actions[punto_TS].append(action)

                   



          
            if rationality !=None:
                rationality=rationality*100              
            if ambition !=None:
                ambition=ambition*100
         

    old_T=None
    ####### the the avg cooperation per TS point
    for punto_TS in sorted(dict_TSplane_list_actions):
        
        dict_TSplane_avg_coop[punto_TS]=numpy.mean(dict_TSplane_list_actions[punto_TS])
        dict_TSplane_std_coop[punto_TS]=numpy.std(dict_TSplane_list_actions[punto_TS])



        if old_T != punto_TS[0]:
            print >> output1
            print   
        print punto_TS[0],punto_TS[1], dict_TSplane_avg_coop[punto_TS], dict_TSplane_std_coop[punto_TS]
        print >> output1,punto_TS[0],punto_TS[1], dict_TSplane_avg_coop[punto_TS], dict_TSplane_std_coop[punto_TS]
        
           
        old_T=punto_TS[0]




    histograma_bines_gral.histograma_bins(list_ages,Nbins, name_h)   #x_position , norm_count, count, norm_cumulat_count, cumulat_count ,  float(hist[b])/float(len(lista))   





    output1.close()
    print "written output datafile:", output_filename1
     

######################################

######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

