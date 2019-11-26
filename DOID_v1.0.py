
# coding: utf-8
#
# PWB

# In[69]:


#Pandas for easy excel reading and list to csv conversion.  I couldn't find anything that isn't cumbersome
#to create a tsv but this seems to work fine.
import pandas as pd
import os



# In[70]:


#change your diractory

os.chdir(r"D:\Python\FlyBase_Py\doid_stuff\\")

#file variables for output.  Could just dump filenames directly into code.
file1 = "doid.181217.obo"
file2 = "doid.190301.obo"
outfile_general = "general_info.txt"
outfile_doids = 'doid_change_log.txt'
outfile_omims = 'omim_change_log.txt'
outfile_harv =  'harv_change_log.txt'
outfile_deleted = "deleted_ID_omims.txt"
outfile_added = "new_ID_omims.txt"
the_excel = "results.xlsx"


#variable to store file location of excel spreadsheet that contains OMIMs of interest.  
search_term_exfile = 'DO_imprecise_cases.xlsx'

#creates a pandas dataframe to capture column with OMIMs of interest.
df = pd.read_excel(search_term_exfile, sheet_name='Sheet1',converters={'OMIM':str})#need to convert
                                                                                    #data in columns from int 
                                                                                    #to str for later searching.


# In[71]:


#pulls the omims from the specified column in the excel file that will be used to search all changed omims.
#These are the omims that are of interest to Harvard.
list_harv_omims = df['OMIM']




# dict_builder takes file objects as input and extracts target data in order to build a dictionary.
# The dictionary will be constrtucted as follows, keys are DOIDs extracted after the [Term] and all lines following will be added to a set.  
#The set terminates upon reaching the first empty line after [Term].  
#Each set will then be assigned as a value to the corresponding key such that any DOID can be used to access the 
#infomation assocaited with it from the file. 
#
# dict-builder returns a dictionary.
# 
# TODO:  the first entry in the dictionary consists of None as key and an empty set as the value.  
#I would like to correct this so that the first entry is a DOID etc. 
#This problem arises from the fact that I needed to initialize the new_set and the new_id variables before the for loop 
#executes because if the for loop encounters an empty line before a DOID, an exception occurs unless those variables exist already. 
#Doesn't seem to have any effect on the reults but feels inelegant. 

# In[72]:


def dict_builder(file_in):

    copy = False
    new_set = set()
    new_id = None
    term_dict = {}

    for line in file_in:
        
        if "id: DOID:" in line.strip() and "alt_id" not in line.strip():
            copy = True
            new_set = set()
            new_id = line.strip()
            continue
            
        elif line == "\n":
            term_dict[new_id] = new_set
            copy = False
            continue
            
        elif copy:
            new_set.add(line.strip())
            
    return(term_dict)
            


# This function takes the list that contains the intersection of DOIDs from both obos as well as the two dictionaries of 
#DOIDs and assocaited term information.  
#Using the DOID as keys to the dictionaries, the function then compares each value from one dictionary to the other.  
#The values are sets, thus easily comparable with a set difference operator.  Returns a list containing a list of unchanged DOIDs 
#and a dict tracking all changes.
# 
# 
# 

# In[73]:


def change_analyzer(term_dict1, term_dict2, id_list):

    diff_terms = [] #list of DOIDs with some change in terms.
    no_change = [] #tracks DOIDs that did not change between releases.
    change_directory = {} #dictionary of changes, key is DOID, value is a set containing each line following DOID.
    

    for identity in id_list: #compare term info in DOIDs that exist across files.  
        
            
        if not term_dict1[identity] == term_dict2[identity]:
            diff_terms.append(identity) #append ID if the info associated with a DOID is different from one file to the next
        
        else:
            no_change.append(identity)
        
        
    for term in diff_terms: #Compare DOIDs across files that have been found to be changed, add changes to list.
        changed = []
        
        #list of items in old file but not in new
        #takes the set containing term info from a DOID in the old obo and looks at the differences with the corresponding
        #set in the new obo, appends these differences as a list to the 'changed' list in position [0]
        changed.append(list(term_dict1[term].difference(term_dict2[term])))
        
        #list of items in new file but not in old
        #takes the set containing term info from a DOID in the new obo and looks at the differences with the corresponding
        #set in the old obo, appends these differences as a list to the 'changed' list in position [1]
        changed.append(list(term_dict2[term].difference(term_dict1[term])))
        
        #creates a dictionary containing all changes in terms from DOIDs across files.
        #the dict values will be lists composed of two lists.  INCEPTION!!  
        change_directory[term]=changed

    return([no_change, change_directory])


# In[74]:


#This function compiles a list of OMIMs that have changed between releases.  

def omim_search(change_dict):


    all_omims = []  #list of OMIMs that have changed between releases.  

    for key in change_dict:
        old_omim_list = []
        new_omim_list = []
    
        for line in change_dict[key][0]:#checks old file data items that are not in new file data for 'xref: OMIM'
            if 'xref: OMIM' in line:
                old_omim_list.append(line.strip('xref: OMIM'))
    
        for line in change_dict[key][1]:#checks new file data items that are not in old file data for 'xref: OMIM'
            if 'xref: OMIM' in line:
                new_omim_list.append(line.strip('xref: OMIM'))
                #print(new_omim_list)
        if old_omim_list or new_omim_list:#checks existence.  If either or both lists have members, appends omims to all_omims
                                          #If neither list has members, ignores this DOID term.
            all_omims.append([key.lstrip('id: '), old_omim_list, new_omim_list])
            
    return(all_omims)

#Function to search for OMIMs of interest to Harv.


# In[75]:


def harv_search(all_omim_list, harv_omims):
    
    #list keeping the DOID, old omim, and new omim.  
    harv_found = []
    
    for thing in all_omim_list: #check item in big omim list, item has three elements, DOID, omims in old file, and 
                               #omims found in new file.
        for ident in harv_omims: #iterate through omims pulled from Harv excel spreadsheet.
            if ident in thing[1]: #“I know it is wet and the sun is not sunny, 
                                    #but we can have lots of good fun that is funny.”
                harv_found.append([thing[0], ident, ' '])
            elif ident in thing[2]:
                harv_found.append([thing[0], ' ' ,ident])
            else:
                continue
                
                
                
                #if omim of interst found append items to list.
                                                            #This has to be done as seperate arguments
                                                            #(vs append single item) or the
                                                            #data will not match the dataframe to_csv() function
                                                            #parameters.
        
    return harv_found


# This function searches for OMIMs in the list of deleted or new terms.  


def omims_new_del(term_dict, id_list, harv_omims):#searches new or deleted terms for omims.
                #term_dict is one of the two dictionaries created from the obo files
                #id_list is a list of DOIDs that are in either 1. the old obo but not the new,
                #or 2. in the new obo but not the old.  
                #harv_list is the list of omims of interest to Harv.
    new_del_omims = []
    for eyedee in id_list: #each id in this list is used as a key in the next line to access
                            #the corresponding dict value.  
        for line in term_dict[eyedee]:
            if 'xref: OMIM' in line:
                line = (line.strip('xref: OMIM'))
                if line in harv_omims.tolist():    #must ust .tolist() b/c harv_omims is a pandas Series object.
                    new_del_omims.append([eyedee, line.strip('xref: OMIM'), "Harv"]) #flag an omim as of interest to Harv.
                    
                else:
                    new_del_omims.append([eyedee, line.strip('xref: OMIM'), []])
    
    return (new_del_omims)


# In[77]:


#Compiles a list of all changes between DOIDs from old to new files.

def change_log(change_dict):

    df_change_log = []

    for key in change_dict.keys():
        
    
        if not change_dict[key][0]:#checks to see if list is empty for index 0 in change_directory.
                                    #Index 0 represents changed data from the older obo file and thus data that either
                                    #will have changed in the new obo or did not exist at all in the old one.
                                    #If the data does not exist (the list is empty), then the change directory is
                                    #capturing data that has been added in the new obo.
    
        
            df_change_log.append([key.lstrip('id:'), ' ', change_dict[key][1]]) #pulls new additions and adds them to
                                                                            #a list that can be placed in a data frame.
            
    
        elif not change_dict[key][1]:#checks to see if list is empty at index 1.  
                                            #Index 1 is changed data from the new obo.
       
            df_change_log.append([key.lstrip('id:'), change_dict[key][0], ' '])
    
            
        
        else:#all other changes between releases.
            df_change_log.append([key.lstrip('id:'), change_dict[key][0], change_dict[key][1]])
    
    return(df_change_log)


# In[78]:main
    


file1_ids = set() #set containing DOIDs from file 1.
file2_ids = set() #Same as above but with DOIDs from file 2.

with open (file1, 'r') as f1, open (file2, 'r') as f2: #build dictionaries for comparisons.

    term_dictionary1 = dict_builder(f1) 
    term_dictionary2 = dict_builder(f2)

for identity in term_dictionary1: #identity is the DOID from the dictionary created above.
    file1_ids.add(identity)

for identity in term_dictionary2: #same as above with file 2.
    file2_ids.add(identity)
    
shared_ids = list(file1_ids.intersection(file2_ids)) #Create a list of DOIDs in common between new and old obos.
                                                     #This list will be used to iterate over the dictionaries to compare
                                                     #the contents of each DOID term.


unchanged_terms = change_analyzer(term_dictionary1, term_dictionary2, shared_ids)[0] #list of unchanged DOID terms
                                                                                    #if interested.
    
what_has_changed = change_analyzer(term_dictionary1, term_dictionary2, shared_ids)[1]  #new dictionary tracking all
                                                                                        #changes between obos.
        
set1Diffset2 = list((file1_ids.difference(file2_ids))) #DOIDs that exist in the old file but not in the new file == Deleted IDs.
set2Diffset1 = list((file2_ids.difference(file1_ids))) #DOIDs that exist in the new file but not the old == New IDs.



# In[79]:


with open (outfile_general, 'w') as og1:  #writes a general info file for quick output check.
    
    og1.write(str(len(file1_ids)) + " Terms in older release.\n")
    og1.write(str(len(file2_ids)) + ' Terms in newer release.\n')

    og1.write(str(len(set1Diffset2)) + ' Deleted IDs.\n')
    og1.write(str(len(set2Diffset1)) + ' New IDs.\n')

    og1.write(str(len(unchanged_terms)) + ' Unchanged terms.\n')
    og1.write(str(len(what_has_changed)) + ' Terms with changes.\n')


# In[80]:


try: #in case absolutely no Harv IDs are found in the files.  Should add try blocks to other dataframe calls.
    harv_df = pd.DataFrame(harv_search(omim_search(what_has_changed), list_harv_omims), columns = ['DOID', 'Old', 'New'])
    harv_df.to_csv (outfile_harv, index = None, header=True)
    
except:
    print("No matches found.")
    
doid_df = pd.DataFrame(change_log(what_has_changed), columns = ['DOID', 'Old', 'New'])#dataframe for general changes.
omim_tracker = pd.DataFrame(omim_search(what_has_changed), columns = ['DOID', 'Old', 'New'])#dataframe for omims.

#need to check the deleted and new terms for omims of interest.
omims_in_deleted = pd.DataFrame(omims_new_del(term_dictionary1, set1Diffset2, list_harv_omims), columns = ['DOID', 'Old', 'New'])
omims_in_new = pd.DataFrame(omims_new_del(term_dictionary2, set2Diffset1,list_harv_omims), columns = ['DOID', 'Old', 'New'])



doid_df.to_csv (outfile_doids, index = None, header=True)
omim_tracker.to_csv (outfile_omims, index = None, header=True)



# In[82]:  
#One can either comment out all to_csv calls or this excel writer or neither depending on interest.


with pd.ExcelWriter(the_excel) as writer:
    doid_df.to_excel(writer, sheet_name='DOID term changes')
    omim_tracker.to_excel(writer, sheet_name='OMIMs')
    omims_in_deleted.to_excel(writer, sheet_name='OMIMs in deleted terms')
    omims_in_new.to_excel(writer, sheet_name='OMIMs in new terms')
    harv_df.to_excel(writer, sheet_name='Harvard OMIMs')

