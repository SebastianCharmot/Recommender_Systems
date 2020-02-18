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

import pickle ## add this to the list of import statements

## add these functions to the other set of functions in your recommendations.py

def topMatches(prefs,person,similarity=sim_pearson, n=5):
    '''
        Returns the best matches for person from the prefs dictionary

        Parameters:
        -- prefs: dictionary containing user-item matrix
        -- person: string containing name of user
        -- similarity: function to calc similarity (sim_pearson is default)
        -- n: number of matches to find/return (5 is default)
        
        Returns:
        -- A list of similar matches with 0 or more tuples, 
           each tuple contains (similarity, item name).
           List is sorted, high to low, by similarity.
           An empty list is returned when no matches have been calc'd.
        
    '''     
    scores=[(similarity(prefs,person,other),other) 
                    for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def transformPrefs(prefs):
    '''
        Transposes U-I matrix (prefs dictionary) 

        Parameters:
        -- prefs: dictionary containing user-item matrix
        
        Returns:
        -- A transposed U-I matrix, i.e., if prefs was a U-I matrix, 
           this function returns an I-U matrix
        
    '''     
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # Flip item and person
            result[item][person]=prefs[person][item]
    return result

def calculateSimilarItems(prefs,n=10,similarity=sim_pearson):

    '''
        Creates a dictionary of items showing which other items they are most 
        similar to. 

        Parameters:
        -- prefs: dictionary containing user-item matrix
        -- n: number of similar matches for topMatches() to return
        -- similarity: function to calc similarity (sim_pearson is default)
        
        Returns:
        -- A dictionary with a similarity matrix
        
    '''     
    result={}
    # Invert the preference matrix to be item-centric
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
      # Status updates for larger datasets
        c+=1
        if c%100==0: 
            print ("%d / %d") % (c,len(itemPrefs))
            
        # Find the most similar items to this one
        scores=topMatches(itemPrefs,item,similarity,n=n)
        result[item]=scores
    return result
                
def main():

    done = False ## make sure this in your main()
    prefs = {}   ## make sure this in your main()
    itemsim = {} ## make sure this in your main()
    
    while not done:
        print()
        
        file_io = input('Sim(ilarity matrix) calc for Item-based recommender? ') ## insert into the input() dialog
        
        ## add this new command to the list of commands as an elif
        
        if file_io == 'Sim' or file_io == 'sim':
            print()
            if len(prefs) > 0: 
                ready = False # sub command in progress
                sub_cmd = input('RD(ead) distance or RP(ead) pearson or WD(rite) distance or WP(rite) pearson? ')
                try:
                    if sub_cmd == 'RD' or sub_cmd == 'rd':
                        # Load the dictionary back from the pickle file.
                        itemsim = pickle.load(open( "save_itemsim_distance.p", "rb" ))
                        sim_method = 'sim_distance'
    
                    elif sub_cmd == 'RP' or sub_cmd == 'rp':
                        # Load the dictionary back from the pickle file.
                        itemsim = pickle.load(open( "save_itemsim_pearson.p", "rb" ))  
                        sim_method = 'sim_pearson'
                        
                    elif sub_cmd == 'WD' or sub_cmd == 'wd':
                        # transpose the U-I matrix and calc item-item similarities matrix
                        itemsim = calculateSimilarItems(prefs,similarity=sim_distance)                     
                        # Dump/save dictionary to a pickle file
                        pickle.dump(itemsim, open( "save_itemsim_distance.p", "wb" ))
                        sim_method = 'sim_distance'
                        
                    elif sub_cmd == 'WP' or sub_cmd == 'wp':
                        # transpose the U-I matrix and calc item-item similarities matrix
                        itemsim = calculateSimilarItems(prefs,similarity=sim_pearson)                     
                        # Dump/save dictionary to a pickle file
                        pickle.dump(itemsim, open( "save_itemsim_pearson.p", "wb" )) 
                        sim_method = 'sim_pearson'
                    
                    else:
                        print("Sim sub-command %s is invalid, try again" % sub_cmd)
                        continue
                    
                    ready = True # sub command completed successfully
                    
                except Exception as ex:
                    print ('Error!!', ex, '\nNeed to W(rite) a file before you can R(ead) it!'
                           ' Enter S(im) again and choose a Write command')
                    print()
                

                if len(itemsim) > 0 and ready == True: 
                    # Only want to print if sub command completed successfully
                    print ('Similarity matrix based on %s, len = %d' 
                           % (sim_method, len(itemsim)))
                    print()
                    ##
                    ## enter new code here, or call a new function, 
                    ##    to print the sim matrix
                    ##
                print()
                
            else:
                print ('Empty dictionary, R(ead) in some data!') 
                    
        else:
            done = True
            
    print('\nGoodbye!')
        
if __name__ == '__main__':
    main()