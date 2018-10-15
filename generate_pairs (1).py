#!/usr/bin/env python

'''
Code to create random pairs of users (Nusers), in Nrounds of the game, with their corresponding payoff matrix.

Input: list of users' ids
Output: Nrounds lists of pairing among the Nusers, with their corresponding payoff matrix (different per pair and per round of the game)

Created by Julia Poncela, on November 2014.

'''

import random


def main():


    list_users=[1,2,3,4,5]#,6,7,8,9,10,11]#58,9,32,84,10,2,3,3,65,5,7,4]    
    print "Users' ids:",list_users, len(list_users)


    list_users=list(set(list_users))   # i remove duplicates
    print "Users' ids (after removing duplicates):",list_users, len(list_users)





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
    print "Nrounds:",Nrounds


   ###### i define the ranges for the parameters in the payoff matrix
   ## 1<T<3 and 0<S<2,  (while R=2  , P=1  are fixed)
    T_values=[1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3]
    S_values=[0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0]
    R=2
    P=1
    
    
    
    create_pairing_and_TS(list_users,Nrounds, T_values, S_values, R, P)
    


def create_pairing_and_TS(list_users,Nrounds, T_values, S_values, R, P):

    list_of_lists_parameters_all_rounds=[]
   
    for i in range (Nrounds):

        lists_parameters_this_round_all_users=[]
        print "\nround:", i, "   users:",list_users

        random.shuffle(list_users)  # this reshuffles the list of users in place
       
        N_users=len(list_users)
        half_number_users=N_users/2   # this truncates the division (parte entera)

        print "# users:", N_users, " half:", half_number_users



        if half_number_users*2 == N_users:   # even number of users
            print "even!"
            i=0
            pairs=[]
            while i<N_users:
                
                u1=list_users[i]
                u2=list_users[i+1]

                pair=[u1, u2]
                pairs.append(pair)

                i +=2
                
                pair_TS=[]
                T=random.choice(T_values)
                S=random.choice(S_values)
                pair_TS.append(T)
                pair_TS.append(S)
                lists_parameters_this_round_all_users.append(pair_TS)


        elif half_number_users*2 < N_users:   # odd number of user
            print "odd!"

            i=0
            pairs=[]
            while i< (N_users-1):
                
                u1=list_users[i]
                u2=list_users[i+1]

                pair=[u1, u2]
                pairs.append(pair)

                i +=2

                
                pair_TS=[]
                T=random.choice(T_values)
                S=random.choice(S_values)
                pair_TS.append(T)
                pair_TS.append(S)
                lists_parameters_this_round_all_users.append(pair_TS)
                
            last_pair=[list_users[-1], "Dummy"]
            pairs.append(last_pair)
     
        

        pair_TS=[]
        T=random.choice(T_values)
        S=random.choice(S_values)
        pair_TS.append(T)
        pair_TS.append(S)
        lists_parameters_this_round_all_users.append(pair_TS)

        print "list of pairs:",pairs, "\n"
        print "corresponding parameters for each pair in this round:",lists_parameters_this_round_all_users
        
        list_of_lists_parameters_all_rounds.append(lists_parameters_this_round_all_users)
        
        
    print "total list of lists:",list_of_lists_parameters_all_rounds
        
######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py path/network.gml"

