#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re, os, heapq, time
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# In[2]:


def heuristic(state):
    dist = 0
    
    for i, c in enumerate(state):
        if (c != end_word[i]): # state position is equivalent to end position
            dist += 1
        
    return dist


# In[3]:


def gen_succ(state):
    succ_list = []
    
    for i in range(len(state)):
        for j in range(26):
            if (state[i] != alphabet[j]):
                child = state[:i] + alphabet[j] + state[i+1:]
                
                if (child in words):
                    succ_list.append(child)
        
    return succ_list


# In[4]:


def print_succ(state):
    succ_list = gen_succ(state)
    
    for succ in succ_list:
        print(f"{succ} h={heuristic(succ)}")


# In[5]:


def print_solution(min_node, CLOSED, moves):
    # Recursively print each step in solution path
    if (min_node[2][2] != -1):
        moves = print_solution(CLOSED[min_node[2][2]], CLOSED, moves)
        
    print(f"{min_node[1]} h={heuristic(min_node[1])} moves: {moves}")    
    return moves + 1


# In[6]:


# A* Search Algorithm

def solve(init_state):
    OPEN =  [] 
    CLOSED = []
    master_states = []
    
    g = 0 # define root level
    h = heuristic(init_state) # define root node heuristic cost
    heapq.heappush(OPEN, (g+h, init_state, (g, h, -1))) # updates OPEN
    
    while bool(OPEN):          
        min_node = heapq.heappop(OPEN)
        parent_idx = len(CLOSED)
        CLOSED.append(min_node)
        master_states.append(min_node[1])
        
        if (min_node[2][1] == 0): # h cost of 0 = end word
            print_solution(min_node, CLOSED, 0)
            return
        
        succ_states = gen_succ(min_node[1])
        g_new = min_node[2][0] + 1 # increase depth
        
        for s_state in succ_states:
            h = heuristic(s_state)
            meta_node = (g_new+h, s_state, (g_new, h, parent_idx))
            
            if (s_state not in master_states): # succ is not already on CLOSED/OPEN
                heapq.heappush(OPEN, meta_node)
                master_states.append(s_state) # add new config to states
            else: # succ is already on CLOSED/OPEN, want to try and redirect
                g_old = 0
                
                for c_node in CLOSED:
                    if (c_node[1] == s_state):
                        g_old = c_node[2][0]
                        break
                for o_node in OPEN:
                    if (o_node[1] == s_state):
                        g_old = o_node[2][0]
                        break

                if (g_new < g_old):
                    heapq.heappush(OPEN, meta_node)


# In[7]:


# **Requires exception checking (words less than 3, entering legitimate words, numbers in entry...)


# In[8]:


def play():
    print("Welcome to The Morse Family Road Trip Word Swap Game (say that 5 times fast...)! I've created a program",
         "that optimizes game solutions provided 2 words of equal length; try it out.\n")

    # User word input
    start_word = input("Enter the first word: ").upper()
    global end_word
    end_word = input("Enter the second word: ").upper()
    
    # Check that lengths are equivalent
    while (len(start_word) != len(end_word)):
        end_word = input("That word was not the same length as the first word, try again: ").upper()
    
    print("\nI will attempt to transform", start_word, "->", end_word + ". Let's begin!\n")
    
    global words
    words = create_bank(start_word)
    
    begin = time.time()
    solve(start_word)
    print("\nSolution path found in", time.time()-begin, "secs.")


# In[9]:


def create_bank(start_word):
    w_length = re.compile('[a-z]{' + str(len(start_word)) + '}(\n)?$', re.I) # define RE to apply
    filename = "words.txt" # given file is in current directory
    words = set(x.strip().upper() for x in open(filename) if w_length.match(x))
    
    return words


# In[10]:


play()


# In[ ]:




