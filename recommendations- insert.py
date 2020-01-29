'''
Calculate Pearson Correlation similarity 
'''

## add tbis function to the other set of functions
# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
    '''
        Calculate Pearson Correlation similarity 

        Parameters:
        -- prefs: dictionary containing user-item matrix
        -- person1: string containing name of user 1
        -- person2: string containing name of user 2
        
        Returns:
        -- Pearson Correlation similarity as a float
        
    '''
    
    pass ## place your code here!
    ##
    ## REQUIREMENT! For this function, calculate the pearson correlation
    ## "longhand", i.e, calc both numerator and denominator as indicated in the
    ## formula. You can use sqrt (from math module), and average from numpy.
    ## Look at the sim_distance() function for ideas.
    ##


                
def main():
    

    done = False
    prefs = {}
    
    while not done:
        print()
        
        ## add this new command to the list of commands as an elif
        
        file_io = input('PC(earson Correlation) critics data? ') 
        
            # Testing the code ..
        if file_io == 'PC' or file_io == 'pc':
            print()
            if len(prefs) > 0:             
                print ('Example:')
                print ('Pearson sim Lisa & Gene:', sim_pearson(prefs, 'Lisa', 'Gene')) # 0.39605901719066977
                print()
                
                print('Pearson for all users:')
                # Calc Pearson for all users
                
                ## add some code here to calc User-User Pearson Correlation similarities 
                ## for all users or add a new function to do this
                
                print()
                
            else:
                print ('Empty dictionary, R(ead) in some data!')            
            
        else:
            done = True
            
    print('\nGoodbye!')
        
if __name__ == '__main__':
    main()