#!/usr/bin/env python
# coding: utf-8

# # The Merry Movie Montage
# 
# The goal is to come up with the shortest string that contains all permutations of these characters: 🎅🤶🦌🧝🎁🎄🎀
# 
# https://www.kaggle.com/c/santa-2021/data

# In[1]:


import numpy as np 
import pandas as pd 
import math
import operator
import time

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# # The Data Provided
# Let's explore the data that we are given.
# We have a list of all possible permutations of the symbols. There are 5,040 different combinations.

# In[2]:


permutations = pd.read_csv('/kaggle/input/santa-2021/permutations.csv')
print(permutations.head(122))
print(len(permutations))


# In[3]:


permutations.iloc[0]


# In[4]:


# the permutation at each position is a pandas series
type(permutations.iloc[0])


# In[5]:


# a series object with all elements in the first position
permutations.iloc[0][0]


# In[6]:


# the series object contains a string in the first position
type(permutations.iloc[0][0])


# In[7]:


# we can index into each string element
permutations.iloc[0][0][0]


# In[8]:


# we can use equality operators for string comparisons
permutations.iloc[0][0][0] == permutations.iloc[0][0][0]


# In[9]:


permutations.iloc[0][0][0] == permutations.iloc[0][0][1]


# We are given a distance matrix that shows the number of character changes across all permutations

# In[10]:


distance_matrix = pd.read_csv('/kaggle/input/santa-2021/distance_matrix.csv')
distance_matrix.head()


# We are allowed to use two wildcards (🌟) in our string

# In[11]:


wildcards = pd.read_csv('/kaggle/input/santa-2021/wildcards.csv')
wildcards.head(8)


# This is waht a submission should look like

# In[12]:


sample_submission = pd.read_csv('/kaggle/input/santa-2021/sample_submission.csv')
sample_submission


# In[ ]:


#TODO: sample submission baseline is 6985


# In[13]:


# we should be able to do better than 3,497 for a baseline
len(sample_submission.iloc[0][0])


# ## A Simple Brute Force Approach (no wildcards)
# Since there are only 5,040 permutation, we are going to begin by constructinge a simple brute force approach. \
# For every permutation that starts with 🎅, 🤶 add the permutation (from the remaining permutations to add) that results in the shortest string. Return the shortest overall string.

# In[ ]:


# since there are 5 spots after 🎅, 🤶 and we cannot repeat symbols
# we can calcualte the number of permutations that start with 🎅, 🤶  with 5!
math.factorial(5)


# In[18]:


# get all permutations
permutations_list = permutations.values.tolist()
# flatten out the permutations list to change from list of lists to list of strings
permutations_list = [item for sublist in permutations_list for item in sublist]
# all of the potential starting poitns for the final list
list_of_candidates = permutations_list[:math.factorial(5)]


# In[22]:


# get the number of characters added to sequence1 by overlapping sequence2
def get_added_length(sequence1, sequence2):
    for i in range(1, len(sequence2)):
        # best solution: ends with everything except the last character
        if sequence1.endswith(sequence2[:-i]):
            return i
    # otherwise return the entire length of the sequence; no overlap
    return len(sequence2)


# **One run through**: comparing all of the available permutations to add to the candidate permutations (ones that start with 🎅, 🤶) and adding the one that results in the shortest total added length to the candidate string

# In[23]:


i = 0
new_list = []
permutations_to_add = permutations_list
for current_sequence in list_of_candidates:
    # only print first 10 results
    if i < 10:
        print(f"First Candidate Sequence: {current_sequence}")
    best_permutation = None
    best_added_length = 7
    for permutation in permutations_to_add:
        # check if already in sequence
        if operator.contains(current_sequence, permutation):
            permutations_to_add.remove(permutation)
            continue
        added_length = get_added_length(current_sequence, permutation)
        if added_length < best_added_length:
            best_added_length = added_length
            best_permutation = permutation
    if i < 10:
        print(f"Best Permutation: {best_permutation}")
        print(f"String to append: {best_permutation[-best_added_length:]}")
        print(f"New Sequence: {current_sequence + best_permutation[-best_added_length:]}")
    new_list.append(current_sequence + best_permutation[-best_added_length:])
    permutations_to_add.remove(best_permutation)
    i += 1
        


# It would take a very long time to brute force this search over all candidates. This approach is not efficient or scalable. What if we had 5,000,000 instead of 5,040 permutations? What if the if the first two positions were not fixed and we had to search over all of the permutations? What if we incorporated wild cards? Can we come up with a way to search this space in a greedy manner?

# In[26]:


permutations_list = permutations.values.tolist()
permutations_list = [item for sublist in permutations_list for item in sublist]
list_of_candidates = permutations_list[:math.factorial(5)]


# In[27]:


# For each potential starting string generate a candidate output
start = time.time()
for i in range(0, 20):
    start_candidate_sequence = time.time()
    current_sequence = list_of_candidates[i]
    print(f"Processing Candidate #{i}: {current_sequence}")
    # candidate string must contain all of the permutations
    permutations_remaining = permutations_list.copy()
    permutations_remaining.remove(current_sequence)
    print(f"{len(permutations_remaining)} permutations to add")
    while len(permutations_remaining) > 0:
        if len(permutations_remaining) % 1000 == 0:
#             print(f"    current string length: {len(current_sequence)}")
            print(f"    Permutations remaining... {len(permutations_remaining)}")
        best_permutation = permutations_remaining[0]
        best_added_length = 7
        for permutation in permutations_remaining:
            # check if already in sequence
            if operator.contains(current_sequence, permutation):
                permutations_remaining.remove(permutation)
                continue
            added_length = get_added_length(current_sequence, permutation)
            if added_length < best_added_length:
                best_added_length = added_length
                best_permutation = permutation
        current_sequence = (current_sequence + best_permutation[-best_added_length:])
        permutations_remaining.remove(best_permutation)
    list_of_candidates[i] = current_sequence
    print(f"    Candidate processed!")
    print(f"    Total Permutation length: {len(current_sequence)}")
    # Test that all substrings are part of the lists
    print(f"    All permutations are included: {all(substring in current_sequence for substring in permutations_list)}")
    end_candidate_sequence = time.time()
    print(f"Time to process candidate: {round(end_candidate_sequence - start_candidate_sequence)} seconds\n")
end = time.time()
print(f"Total time to process 20 candidates: {round(end - start)/60} minutes")


# In[ ]:


# the shortest list of these 20 candidates is 5,913
# but it's only 1/6 of our potential candidates for submission
len(min(list_of_candidates[:20], key=len))


# In[ ]:


# indexes 0, 6, and 8 have thes shortest strings
# Our score will be the largest, 5,950
results = [(len(candidate), list_of_candidates.index(candidate)) for candidate in list_of_candidates[:20]]
results.sort()
print(results)


# # Baseline Submission
# Let's generate a submission that's above the sample submission. This will serve as our new baseline

# In[ ]:


baseline_submission = pd.DataFrame(data={"schedule": [list_of_candidates[0], list_of_candidates[6], list_of_candidates[8]]})


# In[ ]:


baseline_submission.head()


# In[ ]:


baseline_submission.to_csv("submission.csv", sep=',',index=False)


# # Recursion
# 
# But first, can we simplify our method with recursion?

# In[ ]:





# # Using the Distance Matrix
# 
# What are ways in which we can reduce the search space in our brute force approach?
# 1. Order searches by using the distance matrix
# 2. 

# In[ ]:





# # With Wildcards
# TODO: add the beggingin wild cards to the starting permutations

# In[ ]:





# # Shortest Common Super String

# In[ ]:




