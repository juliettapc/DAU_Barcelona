#!/usr/bin/env python

'''
Code to create random pairs of users (Nusers), in Nrounds of the game, with their corresponding payoff matrix.

Input: list of users' ids
Output: Nrounds lists of pairing among the Nusers, with their corresponding payoff matrix (different per pair and per round of the game)

Created by Julia Poncela, on November 2014.

'''

import random


def main():


    list_users=[1,2,3,4,5,6,7]#,8,9,10,11]#58,9,32,84,10,2,3,3,65,5,7,4]    
    print "Users' ids:",list_users,  len(list_users)


    list_users=list(set(list_users))   # i remove duplicates
    print "Users' ids (after removing duplicates):",list_users, len(list_users)

    list_colors=["Red","Blue","Orange","Green", "Purple", "Yellow", "Brown"]   # to randomly designate the strategies C and D



    #### give the maximum and minimum number or rounds (these limits are fixed for the whole experiment)   
    min_number_rounds=13
    max_number_rounds=18
    range_number_rounds=[]    
    print "minimum number of rounds:", min_number_rounds, ", and maximum:", max_number_rounds
    i=min_number_rounds
    while i <= max_number_rounds:
        range_number_rounds.append(i)
        i +=1
    print "range of number of rounds:", range_number_rounds


    ##### i determine the number of rounds (Nrounds) for this particular game
    Nrounds=random.choice(range_number_rounds)
    print "Nrounds:",Nrounds, "\n"


    ######### i define the ranges for the parameters in the payoff matrix
    ##### 5<=T<=15 and 0<S<10,  (while R=10  , P=5  are fixed)
    T_values=[5,6,7,8,9,10,11,12,13,14,15]
    S_values=[0,1,2,3,4,5,6,7,8,9,10]
    R=10
    P=5
    
    ######## the payoffs correspond to the following situations:
    #  C against C  earns:  R
    #  C against D  earns:  S
    #  D against C  earns:  T
    #  D against D  earns:  P





## FATA HACER EL  ORDEN DE LA MATRIZ (FILA C O D) ALEATORIO TB!
    
    
    create_pairing_and_TS(list_users, list_colors,Nrounds, T_values, S_values, R, P)
    



#################

def create_pairing_and_TS(list_users, list_colors,Nrounds, T_values, S_values, R, P):

    list_of_lists_parameters_TS_all_rounds=[]
    list_of_lists_pairs_all_rounds=[]
    list_of_lists_strategies_colors_all_rounds=[]
  
   

    for i in range (Nrounds):
        
       # print "\nround:", i, "   users:",list_users

        random.shuffle(list_users)  # this reshuffles the list of users in place
       
        N_users=len(list_users)
        half_number_users=N_users/2   # this truncates the division (parte entera)

       # print "# users:", N_users, " half:", half_number_users



        if half_number_users*2 == N_users:   # even number of users
           # print "even!"
            i=0
            pairs=[]
            while i<N_users:
                
                u1=list_users[i]
                u2=list_users[i+1]

                pair=[u1, u2]
                pairs.append(pair)

                i +=2                              


        elif half_number_users*2 < N_users:   # odd number of user
         #   print "odd!"

            i=0
            pairs=[]
            while i< (N_users-1):
                
                u1=list_users[i]
                u2=list_users[i+1]

                pair=[u1, u2]
                pairs.append(pair)

                i +=2
                                
                
            last_pair=[list_users[-1], "Dummy"]
            pairs.append(last_pair)
     

        Npairs=len(pairs)

        ##### i generate  the list of TS values for every pair in this round
        lists_parameters_this_round_all_users=[]   
        lists_strategy_color_assignement_this_round_all_users=[]
        for u in range(len(pairs)):
            pair_TS=[]
            T=random.choice(T_values)
            S=random.choice(S_values)
            pair_TS.append(T)
            pair_TS.append(S)
           


            #####  i find out the name of the game (quadrant)  
            game=""
            if T >= 5 and T <10:
               if S >=0 and S <5:
                   game="Stag-Hunt"
               elif S>5  and S<=10:
                   game="Harmony"              
               else: # S==5
                   game="border Harmony/Stag-Hunt"

            elif T >10  and T<= 15:
                if S >=0 and S <5:
                    game="Prisoner's Dilemma"
                elif S>5  and S<=10:
                    game="Snow Drift"
                else: # S==5
                   game="border Snow Drift/Prisoner's Dilemma"

            else:    # T==10
                if S >=0 and S <5:
                    game="border Stag-Hunt/Prisoner's Dilemma"
                elif S>5  and S<=10:
                    game="border Harmony/Snow Drift"
                else: # S==5
                   game="center of the TS plane"

            pair_TS.append(game)
            lists_parameters_this_round_all_users.append(pair_TS)


            ##### i randomly assigne colors to C and D strategies
            random.shuffle(list_colors)
            color_C=list_colors[0]
            color_D=list_colors[1]



            assignement_C=["C", color_C]
            assignement_D=["D", color_D]

            pair_assignement=[assignement_C,assignement_D]
            lists_strategy_color_assignement_this_round_all_users.append(pair_assignement)

        #print "list of pairs:",pairs, "\n"
        #print "corresponding parameters for each pair in this round:",lists_parameters_this_round_all_users
        
        list_of_lists_parameters_TS_all_rounds.append(lists_parameters_this_round_all_users)
        list_of_lists_pairs_all_rounds.append(pairs)
        list_of_lists_strategies_colors_all_rounds.append(lists_strategy_color_assignement_this_round_all_users)
  



   # print "total list of lists:",list_of_lists_parameters_TS_all_rounds, "\n"

    for i in range(Nrounds):
        print "round:",i
        for j in range(Npairs):
            print "pair:",list_of_lists_pairs_all_rounds[i][j], "  T,S values:", list_of_lists_parameters_TS_all_rounds[i][j], " R:", R, " P:",P,"   Strategy-color assignement:",list_of_lists_strategies_colors_all_rounds[i][j]
        print "\n"





######################################

######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

