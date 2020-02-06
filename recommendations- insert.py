'''
Calculate LOOCV

<< Insert the code below into your recommendations.py >>

'''

## add this function to the other set of functions
# Compute Leave_One_Out evaluation
def loo_cv(prefs, metric, sim, algo):
    """
    Leave_One_Out Evaluation: evaluates recommender system ACCURACY
     
     Parameters:
         prefs dataset: critics, ml-100K, etc.
	 metric: MSE, MAE, RMSE, etc.
	 sim: distance, pearson, etc.
	 algo: user-based recommender, item-based recommender, etc.
	 
    Returns:
         error_total: MSE, MAE, RMSE totals for this set of conditions
	 error_list: list of actual-predicted differences
    
    Create a temp copy of prefs
    For each user in prefs:
       for item in each user's profile:
          delete this item
          get recommendation (aka prediction) list
	  select the recommendation for this item from the list returned
          calc error, save into error list
	  restore this item
    return mean error, error list
    """
    
    return error, error_list
                
def main():

    done = False
    prefs = {}
    
    while not done:
        print()
        
        ## add this new command to the list of commands as an elif
        
        file_io = input('LCV(eave one out cross-validation)? ') 
        
        # Testing the code ..
        if file_io == 'LCV' or file_io == 'lcv':
            print()
            if len(prefs) > 0:             
                print ('Example:')            
                ## add some code here to calc LOOCV 
                ## write a new function to do this ..
                error, error_list = loo_cv(prefs, metric, sim, algo)
            else:
                print ('Empty dictionary, R(ead) in some data!')            
            
        else:
            done = True
            
    print('\nGoodbye!')
        
if __name__ == '__main__':
    main()