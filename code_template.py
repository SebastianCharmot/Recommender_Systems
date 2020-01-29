"""
Description of what this program does. Length of description is proportional to
the level of functionality in this program: one or two lines for a short program,
one or more paragraphs for a long program.

Author/Researcher/Collaborator: << Sebastian Charmot >>

"""

## ALL import statements go here

## ALL global constants go here

## All Classes go here
class My_class:
    """ brief description of what this class does
    
    Attributes: name the variables and describe what they contain (briefly)
                if none, write None
    
    class methods follow same documentation guidelines as functions (see below)

    """

## ALL functions go here -- no functions within functions

def my_function1():
    """ brief description of what this function does
    
    Parameters: name the variables and describe what they contain (briefly)
                if none, write None
    
    Returns: name the variables and describe what they contain (briefly) 
                if none, write None    
    
    """
    
    ## Your code here
    ## Add comments to clarify what the code is doing

def my_function2():
    """ brief description of what this function does
    
    Parameters: name the variables and describe what they contain (briefly)
                if none, write None
    
    Returns: name the variables and describe what they contain (briefly) 
                if none, write None    
    
    """
    
    ## Your code here
    ## Add comments to clarify what the code is doing
    return
        
    
## main() always goes last
'''
Change the code below, as required, to run the program
'''
def main():
    """
    A wrapper function that calls the functions above
    """
    
    ##
    ## Don't forget to add comments to clarify what the code is doing
    ##
    print()
    # example class instantiation
    my_instance = My_class()
    print('This is info about my_instance:', my_instance)
    
    # example function call
    my_function1()
    print('This is what my_function1 returns:', my_function1())
    
    # example function call
    print('This is what my_function2 returns:', my_function2())
    
    ## More code/comments here, as needed

'''
Do NOT change the code below
'''
    
if __name__ == "__main__":
    main() 