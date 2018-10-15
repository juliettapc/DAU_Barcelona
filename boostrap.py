#!/usr/bin/env python


def bootstrap(first_x,last_x,list_of_lists_for_bootstrap):
    
    last_x +=1
    x_positions=[]
    for x in range(first_x,last_x):
        x_positions.append(x)
        print x


    list_slopes=[]
    list_intersections=[]
    for iter in range (100):

        y_positions=[]
        for list in list_of_lists_for_bootstrap:
            if len(list)>1:
                list_synth=sample_with_replacement(list,len(list))
                y_positions.append(numpy.mean(list_synth))
            else:
                y_positions.append(numpy.mean(list_synth))

        
        slope, intercept, Corr_coef, p_value, std_err =stats.linregress(x_positions,y_positions)  # least squeares polinomial fit
        list_slopes.append(slope)
        list_intersections.append(intercept)


  

    return numpy.mean(list_slopes),numpy.std(list_slopes)

