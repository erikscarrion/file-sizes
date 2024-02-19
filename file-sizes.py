'''
Retrieve a list of files from a user provided directory
along with their respective sizes, sorted according to
user preference. 
'''

import pandas as pd, os
 
def main():
    

    # request arguments from the user
    func_args = get_args()

    # get results
    
    results = walk_directory(func_args[0],
                             func_args[1],
                             func_args[2],
                             func_args[3])
    print(results)

def get_args():
    '''
    retrieve user supplied arguments that are
    passed to walk_directory(). 

    users provide:
     - a path to scan,
     - the max num. records to return
     - the direction of sorting
     - whether to sort on name or size 
    '''

    # Directory to Scan
    while True:
        try:
            print('Please enter valid path...\n')
            scan_dir = input("Entry: ")
        # Catchall for any exception
        except Exception as exc:
            print("The error is:  ", exc)
        else:
            # is it a valid path?
            if os.path.isdir(scan_dir) == False: 
                print("Invalid Path")
            else: 
                break


    # Limit results
    while True:
        try:
            print("Enter the number of records to return.\nTo keep all records enter 0.\n")
            query_limit = int(input("Entry: "))
        
        except Exception as exc:
            print("The error is: ")
        else:
            if query_limit < 0:
                print("Imaginary amount of data requested.")
            break
    
   
    # ascending or descending
    while True:
        try:
            print("Would you like to sort in ascending or descending order?\nEnter A for ascending\nEnter D for descending\n")
            sort_order = input("Entry: ")
        except Exception as exc:
            print("Error is: ", exc)
        else:
            if sort_order not in ['A', 'a', 'D','d']:
                print("Please enter A or D\n")
        finally:
            break
    
    # Column to sort by 
    while True:
        try:
            print("Choose a column to sort by\nFile Name: Enter 0\nFile Size: Enter 1\n")
            sort_col = int(input("Entry: "))
        except ValueError:
            print("Please enter an integer\n")
        else:
            if sort_col > 1:
                print("Index out of bounds\n")
        finally:
            break
    all_args = [scan_dir, query_limit, sort_order, sort_col]

    return all_args

def walk_directory(dirname, lim = 0, desc = 'A', col = 0):
    '''
    Using the user supplied arguments, walk the directory,
    saving file names and file sizes along the way in a 
    temp dict we later convert into a df for ease of sorting and
    printing.  
    '''

    # storage dictionary
    file_sizes = {"File_Name" : [],
                  "File_Size" : []
                  }

    # loop through the directory, saving the filename
    # and its size to the above dictionary
    for top_dir, path, files in os.walk(dirname):
        for file in files:
            # os.path.getsize() req's full path
            full_path = os.path.abspath(os.path.join(top_dir, file))
            # get the size of the full path
            file_size = os.path.getsize(full_path)
            # then add to the dictionary
            file_sizes["File_Name"].append(file)
            file_sizes["File_Size"].append(file_size)

    # Convert to dataframe for ease of sorting and printing
    '''
    We can return the data sorted in one of two 
    different directions using one of two 
    different columns so we have 4 different 
    scenarios to consider.
    '''
    if col == 0: 
        sort_column = "File_Name"
    else:
        sort_column = "File_Size"
        
    if desc in ['D','d']:
        if lim > 0:
            sizes_df = pd.DataFrame(file_sizes).sort_values(by = sort_column, ascending = False).iloc[:lim,]
        else:
            sizes_df = pd.DataFrame(file_sizes).sort_values(by = sort_column, ascending = False)
    else:
        if lim > 0:
            sizes_df = pd.DataFrame(file_sizes).sort_values(by = sort_column).iloc[:lim,]
        else:
            sizes_df = pd.DataFrame(file_sizes).sort_values(by = sort_column)
 
    return sizes_df
    
        
if __name__ == "__main__":
    main()