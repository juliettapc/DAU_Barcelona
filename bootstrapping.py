#!/usr/bin/env python

import random
import numpy

def sample_with_replacement(population, k):
    "Chooses k random elements (with replacement) from a population"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result



def  zscore(list_values_population, subset_size, Niter, real_value):

    list_artificial_avg_coop_values=[]
    for i in range(Niter):

        sample_list=sample_with_replacement(list_values_population, subset_size)
        avg_coop_sample=numpy.mean(sample_list)
        list_artificial_avg_coop_values.append(avg_coop_sample)


     

    avg_coop_random_samples=numpy.mean(list_artificial_avg_coop_values)
    std_coop_random_samples=numpy.std(list_artificial_avg_coop_values)

    zscore=(real_value-avg_coop_random_samples)/std_coop_random_samples
    print "z-score:", zscore, "    population size:", len(list_values_population), " subset size: ", subset_size
    return zscore
