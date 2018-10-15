#!/usr/bin/env python

'''
Code to read the pickle files with the set of users that are good guys accorging
to different definitions, and calculate the intersections

Created by Julia Poncela, on January 2015.

'''

import pickle
from unidecode import unidecode   # to transform whatever unicode special characters into just plain ascii  (otherwise networkx complains)

import histograma_bines_gral
import numpy
from  scipy import stats

def main():




    coop_threshold=0.75

    print "cooperation threshold", coop_threshold


#    list_type_definitions=["All","lowerHarmony","higherHarmony", "PD", "higherPD", "lowerPD", "SH","SD"]


    filename="../Results/list_all_users.pickle"
    list_all_users=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_good_guys_lowerHarmony_threshold_coop"+str(coop_threshold)+".pickle"
    list_good_guys_lowerHarmony=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_bad_guys_lowerHarmony_threshold_coop"+str(coop_threshold)+".pickle"
    list_bad_guys_lowerHarmony=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_good_guys_higherHarmony_threshold_coop"+str(coop_threshold)+".pickle"
    list_good_guys_higherHarmony=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_bad_guys_higherHarmony_threshold_coop"+str(coop_threshold)+".pickle"
    list_bad_guys_higherHarmony=pickle.load(open(filename, 'rb'))  



    filename="../Results/list_good_guys_PD_threshold_coop"+str(coop_threshold)+".pickle"
    list_good_guys_PD=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_bad_guys_PD_threshold_coop"+str(coop_threshold)+".pickle"
    list_bad_guys_PD=pickle.load(open(filename, 'rb'))  



    filename="../Results/list_good_guys_SH_threshold_coop"+str(coop_threshold)+".pickle"
    list_good_guys_SH=pickle.load(open(filename, 'rb'))  



    filename="../Results/list_bad_guys_SH_threshold_coop"+str(coop_threshold)+".pickle"
    list_bad_guys_SH=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_good_guys_SD_threshold_coop"+str(coop_threshold)+".pickle"
    list_good_guys_SD=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_bad_guys_SD_threshold_coop"+str(coop_threshold)+".pickle"
    list_bad_guys_SD=pickle.load(open(filename, 'rb'))  




    coop_threshold=0.25

    
    filename="../Results/list_good_guys_lowerPD_threshold_coop"+str(coop_threshold)+".pickle"
    list_good_guys_lowerPD=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_bad_guys_lowerPD_threshold_coop"+str(coop_threshold)+".pickle"
    list_bad_guys_lowerPD=pickle.load(open(filename, 'rb'))  



    filename="../Results/list_good_guys_higherPD_threshold_coop"+str(coop_threshold)+".pickle"
    list_good_guys_higherPD=pickle.load(open(filename, 'rb'))  


    filename="../Results/list_bad_guys_higherPD_threshold_coop"+str(coop_threshold)+".pickle"
    list_bad_guys_higherPD=pickle.load(open(filename, 'rb'))  






    print 
    print "intersection between All (",len(list_all_users),") and good lowerHarmony (",len(list_good_guys_lowerHarmony),"):  ", len(list(set(list_all_users)& set(list_good_guys_lowerHarmony))), float(len(list_good_guys_lowerHarmony))/len(list_all_users)*100.,"%"

    print "intersection between All (",len(list_all_users),") and good higherHarmony (",len(list_good_guys_higherHarmony),"):  ", len(list(set(list_all_users)& set(list_good_guys_higherHarmony))), float(len(list_good_guys_higherHarmony))/len(list_all_users)*100.,"%"


    print "intersection between All (",len(list_all_users),") and good PD (",len(list_good_guys_PD),"):  ", len(list(set(list_all_users)& set(list_good_guys_PD))), float(len(list_good_guys_PD))/len(list_all_users)*100.,"%"


    print "intersection between All (",len(list_all_users),") and good lowerPD (",len(list_good_guys_lowerPD),"):  ", len(list(set(list_all_users)& set(list_good_guys_lowerPD))), float(len(list_good_guys_lowerPD))/len(list_all_users)*100.,"%"

    print "intersection between All (",len(list_all_users),") and bad lowerPD (",len(list_bad_guys_lowerPD),"):  ", len(list(set(list_all_users)& set(list_bad_guys_lowerPD))), float(len(list_bad_guys_lowerPD))/len(list_all_users)*100.,"%"


    print "intersection between All (",len(list_all_users),") and good higherPD (",len(list_good_guys_higherPD),"):  ", len(list(set(list_all_users)& set(list_good_guys_higherPD))), float(len(list_good_guys_higherPD))/len(list_all_users)*100.,"%"

    print "intersection between All (",len(list_all_users),") and bad higherPD (",len(list_bad_guys_higherPD),"):  ", len(list(set(list_all_users)& set(list_bad_guys_higherPD))), float(len(list_bad_guys_higherPD))/len(list_all_users)*100.,"%"




    print "intersection between All (",len(list_all_users),") and good SH (",len(list_good_guys_SH),"):  ", len(list(set(list_all_users)& set(list_good_guys_SH))), float(len(list_good_guys_SH))/len(list_all_users)*100.,"%"


    print "intersection between All (",len(list_all_users),") and good SD  (",len(list_good_guys_SD),"):  ", len(list(set(list_all_users)& set(list_good_guys_SD))), float(len(list_good_guys_SD))/len(list_all_users)*100.,"%"






    print 
    print



    print "intersection between good lowerHarmony (",len(list_good_guys_lowerHarmony),") and good higherHarmony (",len(list_good_guys_higherHarmony),"):  ", len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_higherHarmony))), "   (of a max of:", min([len(list_good_guys_lowerHarmony),len(list_good_guys_higherHarmony)]),")",float(len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_higherHarmony))))/ min([len(list_good_guys_lowerHarmony),len(list_good_guys_higherHarmony)])*100., "%"


    print "intersection between good lowerHarmony (",len(list_good_guys_lowerHarmony),") and good PD (",len(list_good_guys_PD),"):  ", len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_PD))), "   (of a max of:", min([len(list_good_guys_lowerHarmony),len(list_good_guys_PD)]),")",float(len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_PD))))/ min([len(list_good_guys_lowerHarmony),len(list_good_guys_PD)])*100., "%"


    print "intersection between good lowerHarmony (",len(list_good_guys_lowerHarmony),") and good SH (",len(list_good_guys_SH),"):  ", len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_SH))), "   (of a max of:", min([len(list_good_guys_lowerHarmony),len(list_good_guys_SH)]),")",float(len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_SH))))/ min([len(list_good_guys_lowerHarmony),len(list_good_guys_SH)])*100., "%"


    print "intersection between good lowerHarmony (",len(list_good_guys_lowerHarmony),") and good SD (",len(list_good_guys_SD),"):  ", len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_SD))), "   (of a max of:", min([len(list_good_guys_lowerHarmony),len(list_good_guys_SD)]),")",float(len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_SD))))/ min([len(list_good_guys_lowerHarmony),len(list_good_guys_SD)])*100., "%"



    print 
    print 






    print "intersection between good PD (",len(list_good_guys_PD),") and good SH (",len(list_good_guys_SH),"):  ", len(list(set(list_good_guys_PD)& set(list_good_guys_SH))), "   (of a max of:", min([len(list_good_guys_PD),len(list_good_guys_SH)]),")",float(len(list(set(list_good_guys_PD)& set(list_good_guys_SH))))/ min([len(list_good_guys_PD),len(list_good_guys_SH)])*100., "%"


    print "intersection between good PD (",len(list_good_guys_PD),") and good SD (",len(list_good_guys_SD),"):  ", len(list(set(list_good_guys_PD)& set(list_good_guys_SD))),float(len(list(set(list_good_guys_PD)& set(list_good_guys_SD))))/ min([len(list_good_guys_PD),len(list_good_guys_SD)])*100., "%"


    print 
    print 




    print "intersection between good SH (",len(list_good_guys_SH),") and good SD (",len(list_good_guys_SD),"):  ", len(list(set(list_good_guys_SH)& set(list_good_guys_SD))), "   (of a max of:", min([len(list_good_guys_SD),len(list_good_guys_SH)]),")",float(len(list(set(list_good_guys_SH)& set(list_good_guys_SD))))/ min([len(list_good_guys_SH),len(list_good_guys_SD)])*100., "%"

   
    print 
    print 


   ##### dummies:
    print "intersection between bad lower Harmony (",len(list_bad_guys_lowerHarmony),") and good higherPD (",len(list_good_guys_higherPD),"):  ", len(list(set(list_good_guys_higherPD)& set(list_bad_guys_lowerHarmony))), "   (of a max of:", min([len(list_bad_guys_lowerHarmony),len(list_good_guys_higherPD)]),")",float(len(list(set(list_bad_guys_lowerHarmony)& set(list_good_guys_higherPD))))/ min([len(list_bad_guys_lowerHarmony),len(list_good_guys_higherPD)])*100., "%"

    print 
    print 

    print "intersection between good lower Harmony (",len(list_good_guys_lowerHarmony),") and good higherPD (",len(list_good_guys_higherPD),"):  ", len(list(set(list_good_guys_higherPD)& set(list_good_guys_lowerHarmony))), "   (of a max of:", min([len(list_good_guys_lowerHarmony),len(list_good_guys_higherPD)]),")",float(len(list(set(list_good_guys_lowerHarmony)& set(list_good_guys_higherPD))))/ min([len(list_good_guys_lowerHarmony),len(list_good_guys_higherPD)])*100., "%"

    print 
    print 

    print "intersection between bad lower Harmony (",len(list_bad_guys_lowerHarmony),") and bad higherPD (",len(list_bad_guys_higherPD),"):  ", len(list(set(list_bad_guys_higherPD)& set(list_bad_guys_lowerHarmony))), "   (of a max of:", min([len(list_bad_guys_lowerHarmony),len(list_bad_guys_higherPD)]),")",float(len(list(set(list_bad_guys_lowerHarmony)& set(list_bad_guys_higherPD))))/ min([len(list_bad_guys_lowerHarmony),len(list_bad_guys_higherPD)])*100., "%"

    print 
  
######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

