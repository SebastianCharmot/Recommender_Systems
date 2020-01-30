'''
Calculate User-based CF Recommendations

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
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
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
    
    totals={}
    simSums={}
    for other in prefs:
      # don't compare me to myself
        if other==person: 
            continue
        sim=similarity(prefs,person,other)
    
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
            
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
  
    # Create the normalized list
    rankings=[(float('%.3f'%(total/simSums[item])),item) for item,total in totals.items()]
  
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings
                
def main():

    done = False
    prefs = {}
    
    while not done:
        print()
        
        ## add this new command to the list of commands as an elif
        
        file_io = input('U(ser-based CF Recommendations)? ') 
        
        # Testing the code ..
        if file_io == 'U' or file_io == 'u':
            print()
            if len(prefs) > 0:             
                print ('Example:')
                user_name = 'Toby'
                print ('User-based CF recs for %s, sim_pearson: ' % (user_name), 
                       getRecommendations(prefs, user_name)) 
                        # [(3.348, 'The Night Listener'), 
                        #  (2.833, 'Lady in the Water'), 
                        #  (2.531, 'Just My Luck')]
                print ('User-based CF recs for %s, sim_distance: ' % (user_name),
                       getRecommendations(prefs, user_name, similarity=sim_distance)) 
                        # [(3.457, 'The Night Listener'), 
                        #  (2.779, 'Lady in the Water'), 
                        #  (2.422, 'Just My Luck')]
                print()
                
                print('User-based CF recommendations for all users:')
                # Calc User-based CF recommendations for all users
        
                ## add some code here to calc User-based CF recommendations 
                ## write a new function to do this ..
                ## def get_all_UU_recs(prefs, sim=sim_pearson, num_users=10, top_N=5):
                ##    ''' 
                ##    Print user-based CF recommendations for all users in dataset
                ##
                ##    Parameters
                ##    -- prefs: nested dictionary containing a U-I matrix
                ##    -- sim: similarity function to use (default = sim_pearson)
                ##    -- num_users: max number of users to print (default = 10)
                ##    -- top_N: max number of recommendations to print per user (default = 5)
                ##
                ##    Returns: None
                ##    '''
                
                print()
                
            else:
                print ('Empty dictionary, R(ead) in some data!')            
            
        else:
            done = True
            
    print('\nGoodbye!')
        
if __name__ == '__main__':
    main()