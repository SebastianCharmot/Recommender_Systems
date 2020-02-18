'''
Recommender System
Source info: PCI, TS, 2007, 978...

Author/Collaborator: Carlos Seminario

Researcher: << Sebastian Charmot >>

'''

import os
import numpy as np
import pandas as pd 
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from math import sqrt 
from itertools import combinations
import pickle


def from_file_to_dict(path, datafile, itemfile):
    ''' Load user-item matrix from specified file 
        
        Parameters:
        -- path: directory path to datafile and itemfile
        -- datafile: delimited file containing userid, itemid, rating
        -- itemfile: delimited file that maps itemid to item name
        
        Returns:
        -- prefs: a nested dictionary containing item ratings for each user
    
    '''
    
    # Get movie titles, place into movies dictionary indexed by itemID
    movies={}
    try:
        with open (path + '/' + itemfile) as myfile: 
            # this encoding is required for some datasets: encoding='iso8859'
            for line in myfile:
                (id,title)=line.split('|')[0:2]
                movies[id]=title.strip()
    
    # Error processing
    except UnicodeDecodeError as ex:
        print (ex)
        print (len(movies), line, id, title)
        return {}
    except Exception as ex:
        print (ex)
        print (len(movies))
        return {}
    
    # Load data into a nested dictionary
    prefs={}
    for line in open(path+'/'+ datafile):
        #print(line, line.split('\t')) #debug
        (user,movieid,rating,ts)=line.split('\t')
        user = user.strip() # remove spaces
        movieid = movieid.strip() # remove spaces
        prefs.setdefault(user,{}) # make it a nested dicitonary
        prefs[user][movies[movieid]]=float(rating)
    
    #return a dictionary of preferences
    return prefs

def data_stats(prefs, fn):
    num_users = len(prefs)
    movies = []
    ratings = []
    # Adds all movies into movies and adds all ratings into ratings
    for user in prefs:
        for item in prefs[user]:
            movies.append(item)
            ratings.append(prefs[user][item])
    movies = set(movies)
    num_items = len(movies)
    num_ratings = len(ratings)
    overall_avg = round(np.mean(np.array(ratings)),2)
    overall_std = round(np.std(np.array(ratings)),2)
    avg_each_movie = []
    # Calculates the average for each movie and adds into avg_each_movie
    for movie in movies:
        avg = []
        for user in prefs:    
            if movie in prefs[user]:
                avg.append(prefs[user][movie])
        avg_each_movie.append(np.mean(np.array(avg)))
    avg_item_rating = round(np.mean(np.array(avg_each_movie)),2)
    avg_item_std = round(np.std(np.array(avg_each_movie)),2)
    avg_each_user = []
    # Calculates the average rating each user gave and adds it to avg_each_user
    for user in prefs:
        avg = []
        for item in prefs[user]:
            avg.append(prefs[user][item])
        avg_each_user.append(np.mean(np.array(avg)))
    avg_user_rating = round(np.mean(np.array(avg_each_user)),2)
    avg_user_std = round(np.std(np.array(avg_each_user)),2)
    
    print("Number of users: " + str(num_users))
    print("Number of items: " + str(num_items))
    print("Number of ratings: " + str(num_ratings))
    print("Overall average rating: " + str(overall_avg) + " out of 5, and std dev of " + str(overall_std))
    print("Average item rating: " + str(avg_item_rating) + " out of 5, and std dev of " + str(avg_item_std)) 
    print("Average user rating: " + str(avg_user_rating) + " out of 5, and std dev of " + str(avg_user_std))               
    print("User-Item Matrix Sparsity: " + str(round((1-(len(ratings)/(num_users*len(movies))))*100,2)) + "%")

    # Matplotlib histogram for ratings
    num_bins = len(set(ratings))
    n, bins, patches = plt.hist(ratings, num_bins, alpha=0.5)
    plt.show()

def popular_items(prefs, fn):
    ui_matrix = {}
    movies = []
    # Creates set of movies
    for user in prefs:
        for item in prefs[user]:
            movies.append(item)
    movies = set(movies)
    # Creates the data structure for ui-matrix where a movie maps to all of its ratings and total ratings
    for movie in movies:
        ui_matrix[movie] = [[],[]]
    # Adds all the ratings for movies into its corresponding place in ui-matrix
    for user in prefs:
        for item in prefs[user]:
            ui_matrix[item][0].append(prefs[user][item])
    for movie in ui_matrix:
        ui_matrix[movie][1] = len(ui_matrix[movie][0])
        ui_matrix[movie][0] = round(np.mean(np.array(ui_matrix[movie][0])),2)
    # We turn our ui_matrix into a pandas dataframe for visualizing
    df = pd.DataFrame(ui_matrix).T
    df.columns = ['Avg Rating','Total Ratings']
    df['Total Ratings'] = df['Total Ratings'].astype(int)
    # This is the number of results desired
    n = 5
    # Here we print our desired fields
    print()
    print("Popular items -- most rated: ")
    print()
    df.sort_values(by=['Total Ratings'], inplace=True, ascending=False)
    print(df[:5])
    print()
    print("Popular items -- highest rated: ")
    print()
    df.sort_values(by=['Avg Rating'], inplace=True, ascending=False)
    print(df[:5])
    print()
    print("Overall best rated items (number of ratings >= 5): ")
    print()
    df.sort_values(by=['Avg Rating'], inplace=True, ascending=False)
    print(df[:5])
    
def sim_distance(prefs,person1,person2):
    '''
        Calculate Euclidean distance similarity 

        Parameters:
        -- prefs: dictionary containing user-item matrix
        -- person1: string containing name of user 1
        -- person2: string containing name of user 2
        
        Returns:
        -- Euclidean distance similarity as a float
        
    '''
    
    # Get the list of shared_items
    si={}
    for item in prefs[person1]: 
        if item in prefs[person2]: 
            si[item]=1
    
    # if they have no ratings in common, return 0
    if len(si)==0: 
        return 0
    
    # Add up the squares of all the differences
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                        for item in prefs[person1] if item in prefs[person2]])
    
    sum_of_squares = 0
    for item in prefs[person1]:
        if item in prefs[person2]:
            #print(item, prefs[person1][item], prefs[person2][item])
            sq = pow(prefs[person1][item]-prefs[person2][item],2)
            #print (sq)
            sum_of_squares += sq
        
    return 1/(1+sqrt(sum_of_squares))

def euclidean_distance(prefs):
    print("Euclidean Distance Between Users in Descending Order:")
    print()
    # Creating our list of users
    users = []
    for user in prefs.keys():
        users.append(user)
    # Generating combinations of size two for euclidean distance
    user_comparisons = list(combinations(users, 2))
    # Empty data frame
    df = pd.DataFrame({"Person_1":[], "Person_2":[], "Euclidean_Distance":[]}) 
    # Populating the data frame with the users and their euclidean distance
    for pair in user_comparisons:
        df_current = pd.DataFrame({"Person_1":[pair[0]], "Person_2":[pair[1]], "Euclidean_Distance":[str(round(sim_distance(prefs,pair[0],pair[1]),2))]})
        # print(pair[0] + " vs. " + pair[1] + ": " + str(round(sim_distance(prefs,pair[0],pair[1]),2)))
        df = df.append(df_current, ignore_index=True)
    # Sort the data frame by euclidean distance in descending order
    df.sort_values(by=['Euclidean_Distance'], inplace=True, ascending=False)
    print(df.to_string(index = False))

def sim_pearson(prefs, p1,p2):
    si=[]
    for item in prefs[p1]: 
        if item in prefs[p2]: 
            si.append(item)
    
    # if they have no ratings in common, return 0
    if len(si)==0: 
        return 0
    
    #We are adding the ratings of the users to calc average
    p1_ratings = []
    p2_ratings = []
    for movie in si:
         p1_ratings.append(prefs[p1][movie])
         p2_ratings.append(prefs[p2][movie])
    p1_avg = np.average(p1_ratings)
    p2_avg = np.average(p2_ratings)

    # Here we are calculating the numerator for Pearson
    num = float(0)
    for sim_movie in si:
        num += (prefs[p1][sim_movie]-p1_avg)*(prefs[p2][sim_movie]-p2_avg)

    # Here we are calculating the denominator for Pearson
    den_lft = float(0)
    den_rht = float(0)
    for si_movie in si:
        den_lft += (prefs[p1][si_movie]-p1_avg)**2
        den_rht += (prefs[p2][si_movie]-p2_avg)**2
    den = sqrt(den_lft)*sqrt(den_rht)

    if den != 0:
        return float(num/den)
    else:
        return 0

def calc_pearson(prefs):

    print("Pearson Correlation For All Users:")
    print()
    # Creating our list of users
    users = []
    for user in prefs.keys():
        users.append(user)
    # Generating combinations of size two for euclidean distance
    user_comparisons = list(combinations(users, 2))
    # Empty data frame
    df = pd.DataFrame({"Person_1":[], "Person_2":[], "Pearson_Correlation":[]}) 
    # Populating the data frame with the users and their euclidean distance

    for pair in user_comparisons:
        df_current = pd.DataFrame({"Person_1":[pair[0]], "Person_2":[pair[1]], "Pearson_Correlation":[str(round(sim_pearson(prefs,pair[0],pair[1]),3))]})
        df = df.append(df_current, ignore_index=True)

    # Sort the data frame by euclidean distance in descending order
    df.sort_values(by=['Pearson_Correlation'], inplace=True, ascending=False)
    print(df.to_string(index = False))
    ## place your code here!
    ##
    ## REQUIREMENT! For this function, calculate the pearson correlation
    ## "longhand", i.e, calc both numerator and denominator as indicated in the
    ## formula. You can use sqrt (from math module), and average from numpy.
    ## Look at the sim_distance() function for ideas.
    ##

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
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
  
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

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
    # Copy and nested copy
    copy = prefs.copy()
    sq_error = 0
    abs_error = 0
    err_list = []
    for user in prefs:
        copy[user] = prefs[user].copy()
    for user in prefs:
        for item in prefs[user]:
            to_restore = copy[user].pop(item)
            # del prefs[user][item]
            recs = getRecommendations(copy,user,sim)
            for rec in recs:
                if rec[1] == item:
                    err_list.append(to_restore - rec[0])
                    sq_error += (to_restore - rec[0])**2
                    abs_error += abs(to_restore - rec[0])
            copy[user][item] = to_restore
    MSE = sq_error / len(err_list)
    MAE = abs_error / len(err_list)

    print("MSE : " + str(MSE))
    print("RMSE : " + str(sqrt(MSE)))
    print("MAE :" + str(MAE))

def topMatches(prefs,person,similarity=calc_pearson, n=5):
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

def calculateSimilarItems(prefs,n=10,similarity=calc_pearson):

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

    for user in prefs:
        print("Item-based CF recs for " + user + " , " + str(sim_method) + " : " + str(getRecommendedItems(prefs, itemsim, user)))

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

    # error_total, error_list  = loo_cv_sim(prefs, metric, sim, algo, itemsim)

    copy = prefs.copy()
    sq_error = 0
    ab_error = 0
    err_list = []
    for user in prefs:
        copy[user] = prefs[user].copy()
    for user in prefs:
        for item in prefs[user]:
            to_restore = copy[user].pop(item)
            # del prefs[user][item]
            recs = algo(copy,sim_matrix,user)
            for rec in recs:
                if rec[1] == item:
                    err_list.append(to_restore - rec[0])
                    sq_error += (to_restore - rec[0])**2
                    ab_error += abs(to_restore - rec[0])
            copy[user][item] = to_restore
    MSE = sq_error / len(err_list)
    MAE = ab_error / len(err_list)

    if metric == "RMSE":
        return sqrt(MSE), err_list
    elif metric == "MAE":
        return MAE, err_list
    else:
        return MSE, err_list

def main():
    ''' User interface for Python console '''
    
    # Load critics dict from file
    path = os.getcwd() # this gets the current working directory
                       # you can customize path for your own computer here
    print('\npath: %s' % path) # debug
    done = False
    prefs = {}
    itemsim = {}

    while not done: 
        print()
        # Start a simple dialog
        file_io = input('R(ead) critics data from file?, '
                        'P(rint) the U-I matrix?, '
                        'V(alidate) the dictionary?, '
                        'S(tats) for key statistics,'
                        'I(tems) that are popular,'
                        'D(istance) critics data, '
                        'PC(earson Correlation) critics data?, '
                        'U(ser-based CF Recommendations)?, '
                        'LCV(eave one out cross-validation)?, '
                        'Sim(ilarity matrix) calc for Item-based recommender?, '
                        'IT(em-based CF Recommendations)?, '
                        'LCVSIM(eave one out cross-validation)?, ')
        
        if file_io == 'R' or file_io == 'r':
            print()
            file_dir = 'data/'
            datafile = 'critics_ratings.data'
            itemfile = 'critics_movies.item'
            print ('Reading "%s" dictionary from file' % datafile)
            prefs = from_file_to_dict(path, file_dir+datafile, file_dir+itemfile)
            print('Number of users: %d\nList of users:' % len(prefs), 
                  list(prefs.keys()))

        elif file_io == 'S' or file_io == 's':
            print("you typed s")
            file_dir = 'data/'
            datafile = 'critics_ratings.data'
            itemfile = 'critics_movies.item'
            print ('Reading "%s" dictionary from file' % datafile)
            prefs = from_file_to_dict(path, file_dir+datafile, file_dir+itemfile)
            print(data_stats(prefs,itemfile))

        elif file_io == 'I' or file_io == 'i':
            print("you typed i")
            file_dir = 'data/'
            datafile = 'critics_ratings.data'
            itemfile = 'critics_movies.item'
            print ('Reading "%s" dictionary from file' % datafile)
            prefs = from_file_to_dict(path, file_dir+datafile, file_dir+itemfile)
            print(popular_items(prefs,itemfile))

        elif file_io == 'P' or file_io == 'p':
            # print the u-i matrix
            print()
            if len(prefs) > 0:
                print ('Printing "%s" dictionary from file' % datafile)
                print ('User-item matrix contents: user, item, rating')
                for user in prefs:
                    for item in prefs[user]:
                        print(user, item, prefs[user][item])
            else:
                print ('Empty dictionary, R(ead) in some data!')
                
        elif file_io == 'V' or file_io == 'v':      
            print()
            if len(prefs) > 0:
                # Validate the dictionary contents ..
                print ('Validating "%s" dictionary from file' % datafile)
                print ("critics['Lisa']['Lady in the Water'] =", 
                       prefs['Lisa']['Lady in the Water']) # ==> 2.5
                print ("critics['Toby']:", prefs['Toby']) 
                # ==> {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 
                #      'Superman Returns': 4.0}
            else:
                print ('Empty dictionary, R(ead) in some data!')

        elif file_io == 'D' or file_io == 'd':
            print()
            if len(prefs) > 0:     
                print(euclidean_distance(prefs))       
           
        elif file_io == 'PC' or file_io == 'pc':
            print()
            if len(prefs) > 0:    
                calc_pearson(prefs)
                print()
                
            else:
                print ('Empty dictionary, R(ead) in some data!')          

        elif file_io == 'U' or file_io == 'u':
            print()
            if len(prefs) > 0:    
                print("Recommendations Using Pearson: ")  
                for user in prefs.keys():
                    print(user + ": " + str(getRecommendations(prefs,user)))
                print()
                print("Recommendations Using Euclidean Distance: ")  
                for user in prefs.keys():
                    print(user + ": " + str(getRecommendations(prefs,user,sim_distance)))
                print()
            else:
                print ('Empty dictionary, R(ead) in some data!')   

        elif file_io == 'LCV' or file_io == 'lcv':
            print()
            if len(prefs) > 0:             
                print("distance")
                loo_cv(prefs, "MSE", sim_distance,"user-based")
                print()
                print("pearson")
                loo_cv(prefs, "MSE", sim_pearson,"user-based")
            else:
                print ('Empty dictionary, R(ead) in some data!')         
        
        elif file_io == 'Sim' or file_io == 'sim':
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
                        pickle.dump(itemsim, open( "save_itemcalc_pearson.p", "wb" )) 
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
                    print(itemsim)
                print()
                
            else:
                print ('Empty dictionary, R(ead) in some data!') 

        elif file_io == 'IT' or file_io == 'it':
            print()
            if len(prefs) > 0 and len(itemsim) > 0:                

                print()
                
                print('Item-based CF recommendations for all users:')
                    
                get_all_II_recs(prefs, itemsim, sim_method) # num_users=10, and top_N=5 by default  '''
                
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