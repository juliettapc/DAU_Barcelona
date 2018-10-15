#!/usr/bin/env python

'''
Code to read the pickle files with the set of users that are good guys accorging
to different definitions, and calculate the intersections

Created by Julia Poncela, on January 2015.

'''

import pickle

import numpy
from  scipy import stats
import itertools
import random

def main():
    

    list_thresholds=[0.25,0.75]
    list_att=["good", "bad"]
    list_regions=["lowerHarmony","higherHarmony", "PD", "higherPD", "lowerPD", "SH","SD"]
  
    list_type_definitions= ["../Results/list_good_guys_lowerHarmony_threshold_coop0.75.pickle","../Results/list_good_guys_lowerHarmony_threshold_coop0.75.pickle","../Results/list_good_guys_lowerHarmony_threshold_coop0.75.pickle"]  #"lowerHarmony","higherHarmony", "PD", "higherPD", "lowerPD", "SH","SD"
    # example:   list_good_guys_lowerHarmony_threshold_coop0.75.pickle

    filename_all="../Results/list_all_users.pickle"
    list_all_users=pickle.load(open(filename_all, 'rb'))  


    list_files=[]
  
    for threshold in list_thresholds:
        for att in list_att:
            for region in list_regions:

              #  if "PD" in region:  # for the Harmony, i am only interested in these values
               #     if att=="good":
                #        threshold=0.75
                 #   else:
                  #      threshold=0.25


                file1="../Results/list_"+att+"_guys_"+region+"_threshold_coop"+str(threshold)+".pickle"
                if file1 not in list_files:
                    list_files.append(file1)

  
    
    cont=0
    for item in  itertools.combinations(list_files, 4):
             

        group1_name=item[0]
        group2_name=item[1]
        group3_name=item[2]
        group4_name=item[3]


        region1=group1_name.split("_guys_")[1].split("_threshold_coop")[0].replace("higher","").replace("lower","")
        region2=group2_name.split("_guys_")[1].split("_threshold_coop")[0].replace("higher","").replace("lower","")
        region3=group3_name.split("_guys_")[1].split("_threshold_coop")[0].replace("higher","").replace("lower","")
        region4=group4_name.split("_guys_")[1].split("_threshold_coop")[0].replace("higher","").replace("lower","")
       
         
        if region1 != region2 and region1  != region3 and region1  != region4  and region2  != region3 and region2  != region4   and region3  != region4:





            list1=pickle.load(open(group1_name, 'rb'))  
            list2=pickle.load(open(group2_name, 'rb'))  
            list3=pickle.load(open(group3_name, 'rb'))  
            list4=pickle.load(open(group4_name, 'rb'))  
            
            
             
         
            
            intersection=float(len(list(set(list1)& set(list2)& set(list3)& set(list4))))
            min_size=float(min([len(list1),len(list2),len(list3),len(list4)]))
            percent= intersection/min_size*100.

#            if percent >=75. or intersection >=100:
            if percent <=15. or intersection <=20:
                print item[0].replace("../Results/list_","").replace(".pickle",""), "  size:", len(list1)
                print item[1].replace("../Results/list_","").replace(".pickle",""), "  size:", len(list2)
                print item[2].replace("../Results/list_","").replace(".pickle",""), "  size:", len(list3)
                print item[3].replace("../Results/list_","").replace(".pickle",""), "  size:", len(list4)
                
              
                
                
                print " Intersection between them:   ", intersection, " (of a max of:",min_size ,")", percent, "% "
          
          
                list_random_intersection=[]
                list_random_min_size=[]
                list_random_percent=[]

                for i in range(1000):
                    
                    random_list1=random.sample(list_all_users, len(list1))
                    random_list2=random.sample(list_all_users, len(list2))
                    random_list3=random.sample(list_all_users, len(list3))
                    random_list4=random.sample(list_all_users, len(list4))
                    

                    random_intersection=float(len(list(set(random_list1)& set(random_list2)& set(random_list3)& set(random_list4))))
                    list_random_intersection.append(random_intersection)

                    random_min_size=float(min([len(random_list1),len(random_list2),len(random_list3),len(random_list4)]))
                    list_random_min_size.append(random_min_size)

                    random_percent=random_intersection/random_min_size*100.
                    list_random_percent.append(random_percent)
                    



                avg_random_intersection=numpy.mean(list_random_intersection)
                zscore_size=(intersection-avg_random_intersection)/numpy.std(list_random_intersection)


                print " Avg Intersection between random sets of same size:   ", avg_random_intersection, " (of a max of:",numpy.mean(list_random_min_size) ,")", numpy.mean(list_random_percent), "%  zscore of intersect. size:", zscore_size, "\n\n"
          




######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

