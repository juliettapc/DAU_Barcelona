#!/usr/bin/env python

'''
Code to calculate the scores of rationality and ambition for each player in each round of the game

Created by Julia Poncela, on December 2014.

'''
import numpy as np
import random

def main():

    
    ###### for a given user and a given point in the TS plane:
    user_T=6
    user_S=7
    R=10
    P= 5   

    user_action= "C"     ######  translated into 1 or 0 later on
    opponent_action="D"





######### THIS IS JUST FOR TESTING!  REMOVE IT FOR YOUR FINAL VERSION
    random_list_T=[5,6,7,8,9,10,11,12,13,14,15]
    random_list_S=[0,1,2,3,4,5,6,7,8,9,10]
    user_T=random.choice(random_list_T)
    user_S=random.choice(random_list_S)
    user_action= random.choice([0,1])     ######  where 1: cooperation,  0: defection
###########################






    #############  translate C or D into  1: cooperation,  0: defection
    if   user_action== "C":
        user_action= 1
    elif   user_action== "D":
        user_action= 0


    if  opponent_action=="C":
        opponent_action= 1
    elif  opponent_action=="D":
        opponent_action= 0




    ########### TS points correspoinding to each game
    T_values_Harmony =[5,6,7,8,9,10]
    S_values_Harmony =[5,6,7,8,9,10]       # quadrant 1


    T_values_SnowDrift =[10,11,12,13,14,15]
    S_values_SnowDrift =[5,6,7,8,9,10]         # quadrant 2


    T_values_StagHunt =[5,6,7,8,9,10]
    S_values_StagHunt =[0,1,2,3,4,5]      # quadrant 3


    T_values_PD =[10,11,12,13,14,15]    # quadrant 4
    S_values_PD =[0,1,2,3,4,5]




 

    perfect_rationality={}   # dict. to storage the perfect values (to compare users to)
    perfect_ambition={}




    ######### i get the values of perfect-ambition for each point in quadrants 2 (Snowdrift) and 3(Stag-Hunt) of the TS plane
    file_stag_hunt_snowdrift="./SH_SG.csv"            
    file1=open(file_stag_hunt_snowdrift,'r')
    list_lines=file1.readlines()

    for line in list_lines:                          
                        
            list_values_one_line=line.strip("\n").split(",")   # it is a csv file, line example: 10,6,1 
            T=int(list_values_one_line[0])
            S=int(list_values_one_line[1])
            Ambition=float(list_values_one_line[2])

            point_TS=(T, S)
            perfect_ambition[point_TS]=Ambition


  #  print "dict of perfect ambition:"
   # for key in  perfect_ambition:
    #    print key, perfect_ambition[key]

 


    ##########  i get the values of perfect-rationality for PrisonersDilemma game
    for T in T_values_PD:
        for S in S_values_PD:
            point_TS=(T, S)
            perfect_rationality[point_TS]=0.   #to defect is the rational thing to do


    ##########  i get the values of perfect-rationality for Harmony game
    for T in T_values_Harmony:
        for S in S_values_Harmony:
            point_TS=(T, S)
            perfect_rationality[point_TS]=1.   # to cooperate is the rational thing to do


    #print "dict of perfect rationality:"
    #for key in  perfect_rationality:
     #   print key, perfect_rationality[key]




    

    #######
    #######  i obtain which trait (rationality or ambition) that applies for the particular TS point the user played on
    trait=""
   
 

    if user_T in T_values_Harmony     and     user_S in S_values_Harmony:
        trait="Rationality"
        game="Harmony"
      
    elif user_T in T_values_SnowDrift     and    user_S in S_values_SnowDrift:
        trait="Ambition"
        game="SnowDrift"       

    elif user_T in T_values_StagHunt     and     user_S in S_values_StagHunt:
        trait="Ambition"
        game="StagHunt"
       
    elif user_T in T_values_PD     and     user_S in S_values_PD:
        trait="Rationality"
        game="PrisonersDilemma"      

    else:

        print "trait not found!!", user_T, user_S
        exit()

 


    print "T:",user_T, "  S:",user_S,  "  R:",R,   "P:",P,game
    print  "trait:",trait
    print  "user's action",user_action, "opponent's action",opponent_action





    ########  i calculate the user's values for rationality or ambition
    if trait=="Rationality":
        user_rationality=calculate_rationality(perfect_rationality, user_T, user_S, user_action)
       
        print "   users' rationality:", user_rationality

    elif  trait=="Ambition":
        user_ambition=calculate_ambition(perfect_ambition,  user_T, user_S, user_action)
        print "   users' ambition:", user_ambition
   





    ######### i calculate the payoff of the user and his opponent
    payoff_user, payoff_oppenent= calculate_payoffs(user_T, user_S, R, P,  user_action, opponent_action)

    print "payoff user:",payoff_user, "payoff opponent:", payoff_oppenent


##############
##############

def calculate_payoffs(user_T, user_S, R, P,  user_action, opponent_action):

    payoff_user=0
    payoff_opponent=0

    if user_action == 1:
        if opponent_action == 1:
            payoff_user= R
            payoff_opponent=R
        elif  opponent_action == 0:
            payoff_user=user_S
            payoff_opponent=user_T

    elif  user_action == 0:
        if opponent_action == 1:
            payoff_user= user_T
            payoff_opponent=user_S
        elif  opponent_action == 0:
            payoff_user= P
            payoff_opponent=P



    return (payoff_user, payoff_opponent)



##############
##############
def calculate_rationality(perfect_rationality, user_T, user_S, user_action):

    point_TS=(user_T, user_S)
    user_rationality=1. - np.fabs( float(user_action)-perfect_rationality[point_TS] )

    print " perfect action:", perfect_rationality[point_TS]
    return user_rationality*100.

##############
##############

def calculate_ambition(perfect_ambition, user_T, user_S, user_action):
    
    point_TS=(user_T, user_S)
    user_ambition=1. - np.fabs( float(user_action)-perfect_ambition[point_TS] )
    print " perfect action:", perfect_ambition[point_TS]
    return user_ambition*100.


###############
###############




######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python "

