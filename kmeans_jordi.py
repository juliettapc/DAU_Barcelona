data = []
playertypes = {}

with open('../Results/DAU_data_for_Jordi_kmeans.dat', 'r') as infile:
    count = 0
    num_playertypes = 0
    for line in infile:
        count += 1
        if count == 1: continue

        parts = line.strip().split(' ')
 
        data.append({'user_id' : parts[0],
                     'H' : parts[1],
                     'SD' : parts[2],
                     'SH' : parts[3],
                     'PD' : parts[4],
                     'higherH' : parts[5],
                     'lowerH' : parts[6],
                     'higherPD' : parts[7],
                     'lowerPD' : parts[8],
                     'S-T[-15,-10)' : parts[9],
                     'S-T[-10,-5)' : parts[10],
                     'S-T[-5,0)' : parts[11],
                     'S-T[0,5]' : parts[12],
                     'type_player' : parts[13]})


import numpy as np
X = []

for d in data:
    X.append([np.nan if d['H'] == 'nan' else float(d['H']),
              np.nan if d['SD'] == 'nan' else float(d['SD']),
              np.nan if d['SH'] == 'nan' else float(d['SH']),
              np.nan if d['PD'] == 'nan' else float(d['PD'])])
              # para mas o menos variables (dimensiones), aki


from sklearn.preprocessing import Imputer
imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
X_new = imp.fit_transform(X)



from sklearn.cluster import KMeans
kmeans = KMeans( n_clusters=4, n_init=10)
kmeans.fit(X_new)


for i in kmeans.labels_:
    print i # lista del group-index al que pertenece cada usuario (en el mismo orden que en X)




