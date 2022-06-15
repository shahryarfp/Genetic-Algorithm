#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
import random
import math
import copy
from time import time

initial_population = 40
key_size = 14
Pc = 0.85
Pm = 0.05


# # Part 0
# ## Preprocessing and Creating set of words

# In[2]:


words_list = []

with open('global_text.txt', "r") as f:
    global_text_str = f.read()
    text_without_stop_chars = ""
    lowercase_letters = list(string.ascii_lowercase)
    uppercase_letters = list(string.ascii_uppercase)
    more = [" "]
    letters = lowercase_letters + uppercase_letters + more
    for i in range(len(global_text_str)):
        character = global_text_str[i]
        if character in letters:
            text_without_stop_chars += character
    text_without_stop_chars = text_without_stop_chars.upper()
    words_list = text_without_stop_chars.split()

#removing stop words
stop_words = set(stopwords.words('english'))
final_words = set()
for word in words_list:
    if word not in stop_words and len(word) != 1:
        final_words.add(word)
len(final_words)


# # Part 1
# ## chromosomes and genes defined in report

# In[3]:


#importing encoded text
len_encoded_text = 0
encoded_text_without_stop_chars = ""
encoded_words_list = []
with open('encoded_text.txt', "r") as f:
    encoded_text_str = f.read()
    lowercase_letters = list(string.ascii_lowercase)
    uppercase_letters = list(string.ascii_uppercase)
    more = [" "]
    letters = lowercase_letters + uppercase_letters + more
    for i in range(len(encoded_text_str)):
        character = encoded_text_str[i]
        if character in letters and character != ' ':
            len_encoded_text += 1
        if character in letters:
            encoded_text_without_stop_chars += character
    encoded_text_without_stop_chars = encoded_text_without_stop_chars.upper()
    encoded_words_list = encoded_text_without_stop_chars.split()


# In[4]:


#creating a sample chromosome
def creating_sample_chromosome():
    uppercase_letters = list(string.ascii_uppercase)
    sample_key = ""
    for i in range(key_size):
        num = random.randint(0, len(uppercase_letters)-1)
        sample_key += uppercase_letters[num]
    return sample_key

def extend_chromosome(chromosome_):
    sample_chromosome = copy.deepcopy(chromosome_)
    extended_chromosome = ""
    for i in range(math.floor(len_encoded_text/key_size)):
        extended_chromosome += sample_chromosome
    for i in range(len_encoded_text%key_size):
        extended_chromosome += sample_chromosome[i]
    return extended_chromosome

created_chromosome = creating_sample_chromosome()


# # Part 2

# In[5]:


#creating an initial population
def create_initial_population():
    chromosomes = []
    for i in range(initial_population):
        chromosomes.append(creating_sample_chromosome())
    return chromosomes


# ## Creating Decryptor

# In[6]:


def decrypt_letter(key, letter):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = alphabet.find(key)
    result = ""
    if letter != ' ':
        index = -(key - alphabet.find(letter)) % len(alphabet)
        result += alphabet[index]
    else:
        result += letter
    return result

def change_chromosome_shape(chromosome_, message):
    ans = ""
    chromosome = copy.deepcopy(chromosome_)
    for i in range(len(message)):
        if message[i] != ' ':
            chromosome, popped = chromosome[1:], chromosome[0]
            ans += popped
        else:
            ans += message[i]
    return ans

def decrypt_message(extended_chromosome, message):
    decoded_message = ""
    chromosome = change_chromosome_shape(extended_chromosome, message)
    for i in range(len(message)):
        if message[i] != ' ':
            decoded_message += decrypt_letter(chromosome[i], message[i])
        else:
            decoded_message += message[i]
    return decoded_message


# # Part 3

# In[7]:


# fitness_function
def fitness_function(decoded_message, final_words):
    value = 0
    decoded_words_list = decoded_message.split()
    for i in range(len(decoded_words_list)):
        if decoded_words_list[i] in final_words:
            value += 2
    return value


# # Part 4

# In[8]:


#Crossover and Mutation

def crossover(parent1, parent2):
    new_parent1 = copy.deepcopy(parent1)
    new_parent2 = copy.deepcopy(parent2)
    if random.uniform(0, 1) < Pc:
        splitter = random.randint(0, key_size-1)
        new_parent1 = parent1[0:splitter]+parent2[splitter:]
        new_parent2 = parent2[0:splitter]+parent1[splitter:]
    return new_parent1, new_parent2

def mutation(parent):
    uppercase_letters = list(string.ascii_uppercase)
    index = random.randint(0, len(uppercase_letters))
    mutated = ""
    for i in range(len(parent)):
        if random.uniform(0, 1) < Pm:
            position = random.randint(0, len(parent)-1)
            mutated = parent[:position] + uppercase_letters[index] + parent[position+1:]
    return mutated


# # Defining Decoder Class

# In[15]:


class Decoder:
    def __init__(self, global_text_str_, encoded_text_str_, keyLength):
        self.key_length = keyLength
        self.Dictionary = self.create_dictionary(global_text_str_)
        len_encoded_text_, encoded_text_without_stop_chars_ = self.prepare_encoded_data(encoded_text_str_)
        self.len_encoded_text = len_encoded_text_
        self.encoded_text_without_stop_chars = encoded_text_without_stop_chars_
        
    def create_dictionary(self, global_text_str):
        words_list = []
        text_without_stop_chars = ""
        lowercase_letters = list(string.ascii_lowercase)
        uppercase_letters = list(string.ascii_uppercase)
        more = [" "]
        letters = lowercase_letters + uppercase_letters + more
        for i in range(len(global_text_str)):
            character = global_text_str[i]
            if character in letters:
                text_without_stop_chars += character
        text_without_stop_chars = text_without_stop_chars.upper()
        words_list = text_without_stop_chars.split()

        #removing stop words
        stop_words = set(stopwords.words('english'))
        final_words = set()
        for word in words_list:
            if word not in stop_words and len(word) != 1:
                final_words.add(word)
        return final_words
    
    def create_initial_population(self):
        chromosomes = []
        for i in range(initial_population):
            chromosomes.append(self.creating_sample_chromosome())
        return chromosomes
    
    def creating_sample_chromosome(self):
        uppercase_letters = list(string.ascii_uppercase)
        sample_key = ""
        for i in range(key_size):
            num = random.randint(0, len(uppercase_letters)-1)
            sample_key += uppercase_letters[num]
        return sample_key

    def extend_chromosome(self, chromosome_):
        sample_chromosome = copy.deepcopy(chromosome_)
        extended_chromosome = ""
        for i in range(math.floor(len_encoded_text/key_size)):
            extended_chromosome += sample_chromosome
        for i in range(len_encoded_text%key_size):
            extended_chromosome += sample_chromosome[i]
        return extended_chromosome
    
    def prepare_encoded_data(self, encoded_text_str):
        len_encoded_text = 0
        encoded_text_without_stop_chars = ""
        lowercase_letters = list(string.ascii_lowercase)
        uppercase_letters = list(string.ascii_uppercase)
        more = [" "]
        letters = lowercase_letters + uppercase_letters + more
        for i in range(len(encoded_text_str)):
            character = encoded_text_str[i]
            if character in letters and character != ' ':
                len_encoded_text += 1
            if character in letters:
                encoded_text_without_stop_chars += character
        encoded_text_without_stop_chars = encoded_text_without_stop_chars.upper()
        return len_encoded_text, encoded_text_without_stop_chars
    
    def decrypt_letter(self, key, letter):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = alphabet.find(key)
        result = ""
        if letter != ' ':
            index = -(key - alphabet.find(letter)) % len(alphabet)
            result += alphabet[index]
        else:
            result += letter
        return result

    def change_chromosome_shape(self, chromosome_, message):
        ans = ""
        chromosome = copy.deepcopy(chromosome_)
        for i in range(len(message)):
            if message[i] != ' ':
                chromosome, popped = chromosome[1:], chromosome[0]
                ans += popped
            else:
                ans += message[i]
        return ans

    def decrypt_message(self, extended_chromosome, message):
        decoded_message = ""
        chromosome = self.change_chromosome_shape(extended_chromosome, message)
        for i in range(len(message)):
            if message[i] != ' ':
                decoded_message += self.decrypt_letter(chromosome[i], message[i])
            else:
                decoded_message += message[i]
        return decoded_message
    
    def fitness_function(self, decoded_message, final_words):
        value = 0
        decoded_words_list = decoded_message.split()
        for i in range(len(decoded_words_list)):
            if decoded_words_list[i] in final_words:
                value += 2
        return value
    
    def rank_chromosomes(self, chromosomes):
        sorted_chromosomes = []
        for chromosome in chromosomes:
            extended_chromosome = self.extend_chromosome(chromosome)
            decrypted_message = self.decrypt_message(extended_chromosome, self.encoded_text_without_stop_chars)
            sorted_chromosomes.append((self.fitness_function(decrypted_message, self.Dictionary), chromosome))
        sorted_chromosomes = sorted(sorted_chromosomes, key = lambda x:(x[0]), reverse = True)
        a = []
        for tuple_ in sorted_chromosomes:
            a.append(tuple_[1])
        return a

    def crossover(self, parent1, parent2):
        mode = False
        new_parent1 = copy.deepcopy(parent1)
        new_parent2 = copy.deepcopy(parent2)
        if random.uniform(0, 1) < Pc:
            splitter = random.randint(0, key_size-1)
            new_parent1 = parent1[0:splitter]+parent2[splitter:]
            new_parent2 = parent2[0:splitter]+parent1[splitter:]
            mode = True
        return mode, new_parent1, new_parent2

    def mutation(self, parent):
        mode = False
        uppercase_letters = list(string.ascii_uppercase)
        index = random.randint(0, len(uppercase_letters)-1)
        mutated = copy.deepcopy(parent)
        for i in range(len(parent)):
            if random.uniform(0, 1) < Pm:
                position = random.randint(0, len(parent)-1)
                mutated = mutated[:position] + uppercase_letters[index] + mutated[position+1:]
                mode = True
        return mode, mutated
    
    def is_finished(self, chromosome):
        value = 0
        print(chromosome)
        extended_chromosome = self.extend_chromosome(chromosome)
        decoded_message = self.decrypt_message(extended_chromosome, self.encoded_text_without_stop_chars)
        decoded_words_list = decoded_message.split()
        for word in decoded_words_list:
            if word in final_words:
                value += 1
        print(value/len(decoded_words_list)*100, '%')
        if value/len(decoded_words_list) > 0.7:
            return True
        else:
            return False
        
    def decode(self):
        chromosomes = self.create_initial_population()
        while not self.is_finished(chromosomes[0]):
            sorted_chromosomes = self.rank_chromosomes(chromosomes)
            next_gen = sorted_chromosomes[:int(0.1*len(sorted_chromosomes))]
            temp_gen = sorted_chromosomes[int(0.1*len(sorted_chromosomes)):]
            temp_gen_changed = set()
            #crossover
            for i in range(int(len(temp_gen)/2)):
                first_index_for_crossover = random.randint(0, len(temp_gen)-1)
                second_index_for_crossover = random.randint(0, len(temp_gen)-1)
                mode, child1, child2 = self.crossover(temp_gen[first_index_for_crossover], temp_gen[second_index_for_crossover])
                if mode == True:
                    temp_gen_changed.add(temp_gen[first_index_for_crossover])
                    temp_gen_changed.add(temp_gen[second_index_for_crossover])
                    next_gen.append(child1)
                    next_gen.append(child2)
            #mutation
            for i in range(len(temp_gen)):
                mode, child = self.mutation(temp_gen[i])
                if mode == True:
                    temp_gen_changed.add(temp_gen[i])
                    next_gen.append(child)
            #add not changed chromosomes to the next generation
            for gen in temp_gen:
                if gen not in temp_gen_changed:
                    next_gen.append(gen)
            sorted_next_gen = self.rank_chromosomes(next_gen)
            chromosomes = sorted_next_gen[:initial_population]
#             chromosomes = sorted_next_gen[:int(len(chromosomes)*1.05)]
            
        return chromosomes[0]


# In[16]:


encodedText = open('encoded_text.txt').read()
globalText = open('global_text.txt').read()
d = Decoder(globalText, encodedText, keyLength = 14)
start = time()
decodedText = d.decode()
end = time()

print(' ')
print('Duration: ', end-start, 's')
print('Answer: ', decodedText)


# In[ ]:




