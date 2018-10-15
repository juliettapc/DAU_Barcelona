#!/usr/bin/env python

'''
Code to read the pickle file with the raw data from the DAU experiments,
and make it into a csv file.

Created by Julia Poncela, on December 2014.

'''

import pickle
from unidecode import unidecode   # to transform whatever unicode special characters into just plain ascii  (otherwise networkx complains)
def main():

    filename="../Data/userdata.pickle"
    master_list=pickle.load(open(filename, 'rb'))   # es una lista: un elemento por jugador (541)



    output_filename="../Data/output_datafile_for_block_model.dat"
    output= open(output_filename,'wt')
    print >> output, "user_id TS_point C_1_or_D_0"
      



 ### master_list  tiene la forma: [{'guany_total': 110L, 'partida': 1L, 'genere': u'h', 'num_eleccions': 14, 'edat': 50L, 'rationality': 66.666666666666671, 'ambition': 100.0, 'rondes': [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0},...],      'nickname': u'Caesar', 'id': 2L}]


#la llave key tiene a su vez como valor una lista de diccionarios (uno por ronda)
   # [{'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}, {'guany_oponent': 6L, 'ambition': None, 'seleccio': u'D', 'oponent': 17L, 'S': 6L, 'T': 8L, 'seleccio_oponent': u'C', 'numronda': 2L, 'guany': 8L, 'cuadrant': u'Harmony', 'rationality': 0.0}, ...]


  
    for dictionary in master_list:   # cada elemento de la lista es a su vez un dict
       # print dictionary
        payoff_total=dictionary['guany_total']
        partida=dictionary['partida']
        genero=dictionary['genere']
        if genero =="h":
            genero=1            
        elif genero == "d":
            genero=0
        num_elecciones=dictionary['num_eleccions']
        edad=dictionary['edat']
        avg_racionalidad=dictionary['rationality']
        avg_ambicion=dictionary['ambition']
        num_rondas=len(dictionary['rondes'])
        nickname=unidecode(dictionary['nickname']).replace(" ", "_")
        user_id=dictionary['id']

       
      
        list_dict_rondas=dictionary['rondes']

       

        for dict_ronda in list_dict_rondas:
          ##  cada diccionario de ronda tiene: {'guany_oponent': 10L, 'ambition': None, 'seleccio': u'C', 'oponent': 7L, 'S': 6L, 'T': 5L, 'seleccio_oponent': u'C', 'numronda': 1L, 'guany': 10L, 'cuadrant': u'Harmony', 'rationality': 1.0}

            payoff=dict_ronda['guany']
            payoff_oponent=dict_ronda['guany_oponent']
            rationality=dict_ronda['rationality']
            ambition=dict_ronda['ambition']

            action=dict_ronda['seleccio']
            if action =="C":
                action=1
            elif action=="D":
                action=0
            # si no ha elegido nada, es None
              

                
            action_oponent=dict_ronda['seleccio_oponent']
            if action_oponent =="C":
                action_oponent=1
            elif action_oponent=="D":
                action_oponent=0            
             # si no ha elegido nada, es None
           

            oponent_id=dict_ronda['oponent']                 
            num_ronda=dict_ronda['numronda']
            quadrant=dict_ronda['cuadrant'].replace(" ", "_").replace("'", "")



            T=int(dict_ronda['T'])
            S=int(dict_ronda['S']) 

            T_str=str(T)
            S_str=str(S)
            if T<10:
                T_str="0"+str(T)
            if S<10:
                S_str="0"+str(S)


            punto_TS=T_str+S_str



            if action != None:   # solo imprimo las jugadas en las que el jugador ha elegido una accion

                print >> output, user_id, punto_TS, action
            



    output.close()
    print "written output datafile:", output_filename
      #  raw_input()

######################################

######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

