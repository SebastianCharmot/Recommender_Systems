'''
UPDATED 14-Feb-20

LOOCV results for critics data using 
Similarity methods: sim_distance(), sim_pearson()
Recommender: User-based CF

Author: Carlos Seminario

Currently, the best answer is .. MSE for Pearson: 0.44640825000017764

The variations in results for LOOCV using Pearson on the critics U-I matrix 
are due to a couple of factors:
(1) The getRecommendations() function returns formatted ratings using '%.3f' 
and this impacts the results. I would like everyone to synchronize on NOT using
the '%.3f' format specifier, i.e., in the original getRecommendations(), change
this ..
rankings=[(float('%.3f'%(total/simSums[item])),item) for item,total in totals.items()]
to this .. 
rankings=[(total/simSums[item],item) for item,total in totals.items()]

(2) The LOOCV code removes a rating from a user profile, requests a 
recommendation/prediction, calculates the error (actual - predicted), 
restores the rating that was removed, and then repeats the process. 
Some LOOCV code solutions (including mine!) were not restoring the rating 
that was removed when no viable recommendation/prediction was returned. 

Here are the actions required ..

(i) Using .. rankings=[(total/simSums[item],item) for item,total in totals.items()]!
MSE for Pearson: 0.44640825000017764 ==> this is the result you should be getting.

(ii) Using rankings=[(float('%.3f'%(total/simSums[item])),item) for item,total in totals.items()]
MSE for Pearson: 0.4464328235294117 ==> if you got this result, please change 
the getRecommendations() code as explained in (1) above.

(iii) Using .. rankings=[(float('%.3f'%(total/simSums[item])),item) for item,total in totals.items()]
MSE for Pearson: 0.444159970588 ==> if you got this result, please change the 
getRecommendations() code as explained in (1) above, and check your LOOCV code 
as indicated in (2) above.

(iv) Using .. rankings=[(total/simSums[item],item) for item,total in totals.items()]
MSE for Pearson: 0.444120767982 ==> if you got this result, please check your 
LOOCV code as indicated in (2) above.


'''

import pickle

def print_loocv_results(sq_diffs_info):
    ''' Print LOOCV results '''

    error_list = []
    for user in sq_diffs_info:
        for item in sq_diffs_info[user]:
            for data_point in sq_diffs_info[user][item]:
                print ('User: %s, Item: %s, Prediction: %.5f, Actual: %.5f, Error: %.5f' %\
	              (user, item, data_point[0], data_point[1], data_point[2]))                
                error_list.append(data_point[2]) # save for MSE calc
                
    print()
    print ('MSE =', sum(error_list)/len(error_list))
                
                
def main():
    ''' User interface for Python console '''
    
    print()
    # Load LOOCV results from file, print
    print('Results for sim_distance:')
    sq_diffs_info = pickle.load(open( "save_sq_diffs_info_distance.p", "rb" ))
    print_loocv_results(sq_diffs_info)   
    print()
    # Load LOOCV results from file, print
    print('Results for sim_pearson:')
    sq_diffs_info = pickle.load(open( "save_sq_diffs_info_pearson.p", "rb" ))
    print_loocv_results(sq_diffs_info) 
     
if __name__ == '__main__':
    main()
    