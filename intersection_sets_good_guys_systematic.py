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
    

    list_thresholds=[0.25,0.75]

  
    list_type_definitions=["Harmony","lowerHarmony","higherHarmony", "PD", "higherPD", "lowerPD", "SH","SD"]
    print "list types of def:", list_type_definitions
    good_or_bad=["good","bad"]

    filename_all="../Results/list_all_users.pickle"
    list_all_users=pickle.load(open(filename_all, 'rb'))  


    for i in range(len(list_type_definitions)):
        for att1 in good_or_bad:            
          group1=list_type_definitions[i]
        
          for threshold1 in list_thresholds:
           
              filename1="../Results/list_"+att1+"_guys_"+str(group1)+"_threshold_coop"+str(threshold1)+".pickle"
              list1=pickle.load(open(filename1, 'rb'))  
             
              print "\n\nintersec. between",att1, group1,"(",len(list1),") with threshold",threshold1," and:"
    
              for j in range(len(list_type_definitions)):
                for att2 in good_or_bad:
                    group2=list_type_definitions[j]                   
                    if j>i:  # as not to repeat pairs of groups                                                
                
                        for threshold2 in list_thresholds:                                                     
                            filename2="../Results/list_"+att2+"_guys_"+str(group2)+"_threshold_coop"+str(threshold2)+".pickle"
                            list2=pickle.load(open(filename2, 'rb'))
                            

                          #  print "   intersec. between ",att1, group1,"(",len(list1),") with threshold",threshold1,"&",att2, group2," (",len(list2),") with threshold",threshold2,":", len(list(set(list1)& set(list2))), " (of a max of:", min([len(list1),len(list2)]),")",int(float(len(list(set(list1)& set(list2))))/ min([len(list1),len(list2)])*100.), "%"
                    
                            print "   ",att2, group2," (",len(list2),") with threshold",threshold2,":", len(list(set(list1)& set(list2))), " (of a max of:", min([len(list1),len(list2)]),")",int(float(len(list(set(list1)& set(list2))))/ min([len(list1),len(list2)])*100.), "%"
                    


   
              print "  intersec. between All (",len(list_all_users),") &",att1, group1," (",len(list1),"): with threshold",threshold1,"   ", len(list(set(list_all_users)& set(list1))), " that is:",int(float(len(list1))/len(list_all_users)*100.),"%"

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

