'''
Calculate Item-based CF Recommendations

<< Insert the code below into your recommendations.py >>

'''

################################################################################

## These two defs are here only to prevent a Python error message when running
## this code. Your code should already have completed versions of these functions,
## so you don't need to insert these def's into your recommendations.py!!
def sim_distance(prefs, person1, person2):
    pass
def sim_pearson(prefs, person1, person2):
    pass

################################################################################

## add tbis function to the other set of functions
# Gets recommendations for a person by using a weighted average
# of every other similar item's ratings

def getRecommendedItems(prefs,itemMatch,user):
    '''
        Calculates recommendations for a given user 

        Parameters:
        -- prefs: dictionary containing user-item matrix
        -- person: string containing name of user
        -- similarity: function to calc similarity (sim_pearson is default)
        
        Returns:
        -- A list of recommended items with 0 or more tuples, 
           each tuple contains (predicted rating, item name).
           List is sorted, high to low, by predicted rating.
           An empty list is returned when no recommendations have been calc'd.
        
    '''    
    userRatings=prefs[user]
    scores={}
    totalSim={}
    # Loop over items rated by this user
    for (item,rating) in userRatings.items( ):
  
      # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
    
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # ignore scores of zero or lower
            if similarity<=0: continue            
            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
  
    # Divide each total score by total weighting to get an average

    rankings=[(score/totalSim[item],item) for item,score in scores.items( )]    
  
    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings
           
def get_all_II_recs(prefs, itemsim, sim_method, num_users=10, top_N=5):
    ''' 
    Print item-based CF recommendations for all users in dataset

    Parameters
    -- prefs: U-I matrix (nested dictionary)
    -- itemsim: item-item similarity matrix (nested dictionary)
    -- sim_method: name of similarity method used to calc sim matrix (string)
    -- num_users: max number of users to print (integer, default = 10)
    -- top_N: max number of recommendations to print per user (integer, default = 5)

    Returns: None
    
    '''
    pass ## see comments in main() re coding this function

def loo_cv_sim(prefs, metric, sim, algo, sim_matrix):
    """
    Leave-One_Out Evaluation: evaluates recommender system ACCURACY
     
     Parameters:
         prefs dataset: critics, etc.
	 metric: MSE, or MAE, or RMSE
	 sim: distance, pearson, etc.
	 algo: user-based recommender, item-based recommender, etc.
         sim_matrix: pre-computed similarity matrix
	 
    Returns:
         error_total: MSE, or MAE, or RMSE totals for this set of conditions
	 error_list: list of actual-predicted differences
    """
    pass

def main():

    done = False
    prefs = {}
    
    while not done:
        print()
        
        ## add these new commands to the list of commands as an elif
        
        file_io = input('I(tem-based CF Recommendations)?, '
                        'LCVSIM(eave one out cross-validation)?, ') 
        
        # Testing the code ..
        if file_io == 'I' or file_io == 'i':
            print()
            if len(prefs) > 0 and len(itemsim) > 0:                
                print ('Example:')
                user_name = 'Toby'
    
                #print ('Item-based CF recs for %s, %s: ' % (user_name, sim_method), 
                       #getRecommendedItems(prefs, itemsim, user_name)) 
                
                ##
                ## Example:
                ## Item-based CF recs for Toby, sim_distance:  
                ##     [(3.1667425234070894, 'The Night Listener'), 
                ##      (2.9366294028444346, 'Just My Luck'), 
                ##      (2.868767392626467, 'Lady in the Water')]
                ##
                ## Example:
                ## Item-based CF recs for Toby, sim_pearson:  
                ##     [(3.610031066802183, 'Lady in the Water')]
                ##
    
                print()
                
                print('Item-based CF recommendations for all users:')
                # Calc Item-based CF recommendations for all users
        
                ## add some code above main() to calc Item-based CF recommendations 
                ## ==> write a new function to do this, as follows
                    
                get_all_II_recs(prefs, itemsim, sim_method) # num_users=10, and top_N=5 by default  '''
                # Note that the item_sim dictionry and the sim_method string are
                #   setup in the main() Sim command
                
                ## Expected Results ..
                
                ## Item-based CF recs for all users, sim_distance:  
                ## Item-based CF recommendations for all users:
                ## Item-based CF recs for Lisa, sim_distance:  []
                ## Item-based CF recs for Gene, sim_distance:  []
                ## Item-based CF recs for Michael, sim_distance:  [(3.2059731906295044, 'Just My Luck'), (3.1471787551061103, 'You, Me and Dupree')]
                ## Item-based CF recs for Claudia, sim_distance:  [(3.43454674373048, 'Lady in the Water')]
                ## Item-based CF recs for Mick, sim_distance:  []
                ## Item-based CF recs for Jack, sim_distance:  [(3.5810970647618663, 'Just My Luck')]
                ## Item-based CF recs for Toby, sim_distance:  [(3.1667425234070894, 'The Night Listener'), (2.9366294028444346, 'Just My Luck'), (2.868767392626467, 'Lady in the Water')]
                ##
                ## Item-based CF recommendations for all users:
                ## Item-based CF recs for Lisa, sim_pearson:  []
                ## Item-based CF recs for Gene, sim_pearson:  []
                ## Item-based CF recs for Michael, sim_pearson:  [(4.0, 'Just My Luck'), (3.1637361366111816, 'You, Me and Dupree')]
                ## Item-based CF recs for Claudia, sim_pearson:  [(3.4436241497684494, 'Lady in the Water')]
                ## Item-based CF recs for Mick, sim_pearson:  []
                ## Item-based CF recs for Jack, sim_pearson:  [(3.0, 'Just My Luck')]
                ## Item-based CF recs for Toby, sim_pearson:  [(3.610031066802183, 'Lady in the Water')]
                    
                print()
                
            else:
                if len(prefs) == 0:
                    print ('Empty dictionary, R(ead) in some data!')
                else:
                    print ('Empty similarity matrix, use Sim(ilarity) to create a sim matrix!')    
                    
                    
        elif file_io == 'LCVSIM' or file_io == 'lcvsim':
            print()
            if len(prefs) > 0 and itemsim !={}:             
                print('LOO_CV_SIM Evaluation')
                if len(prefs) == 7:
                    prefs_name = 'critics'

                metric = input ('Enter error metric: MSE, MAE, RMSE: ')
                if metric == 'MSE' or metric == 'MAE' or metric == 'RMSE' or \
		        metric == 'mse' or metric == 'mae' or metric == 'rmse':
                    metric = metric.upper()
                else:
                    metric = 'MSE'
                algo = getRecommendedItems ## Item-based recommendation
                
                if sim_method == 'sim_pearson': 
                    sim = sim_pearson
                    error_total, error_list  = loo_cv_sim(prefs, metric, sim, algo, itemsim)
                    print('%s for %s: %.5f, len(SE list): %d, using %s' 
			  % (metric, prefs_name, error_total, len(error_list), sim) )
                    print()
                elif sim_method == 'sim_distance':
                    sim = sim_distance
                    error_total, error_list  = loo_cv_sim(prefs, metric, sim, algo, itemsim)
                    print('%s for %s: %.5f, len(SE list): %d, using %s' 
			  % (metric, prefs_name, error_total, len(error_list), sim) )
                    print()
                else:
                    print('Run S(im) command to create/load Sim matrix!')
                if prefs_name == 'critics':
                    print(error_list)
            else:
                print ('Empty dictionary, run R(ead) OR Empty Sim Matrix, run Sim!')
            
        else:
            done = True
            
    print('\nGoodbye!')
        
if __name__ == '__main__':
    main()
    