###############################################################################
# randomize_beacon.py - part of the python beacon project
# used to randomize the variable and function names of the beacon so its
# signature changes each time
# Written by JCSteiner
# (VV Gorilla ASCII Art VV)
#               ...      
#            ..-+%*:.    
#         .:-++%@=.+:.   
#       .:++=*%%%#-#*.   
#   .+==*=:+%@@@@#....   
#  .+.:%@@@@@=+#@%.      
#  .+-#@@##*-+**@-.      
#   +%@@*--=.=+#%:       
#   =@@*:    =+=#:       
#   -*@*.    .+@=.       
#   .....    ....  
# 
###############################################################################

import random
import string

# gets random letters and numbers 
randletters = string.ascii_lowercase + string.ascii_uppercase

# opens files
inpath = input('What is the name of your template beacon: ')
outpath = input('What would you like to call the output file: ')
infile = open(inpath)
outfile = open(outpath, 'w')

# initializes dictionary
vars = dict()

# loops through each line of the python script
for line in infile:

    # stores a copy of the line so we can split up the variable from other delimiters
    line_copy = line
    line_copy = line_copy.replace('+', ' ')
    line_copy = line_copy.replace('-', ' ')
    line_copy = line_copy.replace(':', ' ')
    line_copy = line_copy.replace('+', ' ')
    line_copy = line_copy.replace('(', ' ')
    line_copy = line_copy.replace('[', ' ')
    line_copy = line_copy.replace(',', ' ')
    line_copy = line_copy.replace('.', ' ')
    line_copy = line_copy.replace(')', ' ')
    line_copy = line_copy.replace(']', ' ')

    # splits up the individual words in the lines
    words = line_copy.split()

    # if the line is a comment, remove it from the output
    if line[0] != "#":

        # loops through all the words in the line
        for word in words:

            # if the variable has the rand_ prefix to indicate it should be randomized
            isVar = "rand_" in word

            if isVar and word not in vars.keys(): 
                vars[word] =''.join(random.choice(randletters) for i in range(16))

            # if the current word is in the dictionary (why we loop through each word)
            if word in vars.keys():
                # replace it with its replacement
                line = line.replace(word, vars[word])   

        # writes the line to the output file
        outfile.write(line)

# prints the variables replaced
for var in vars:
    print('Variable', var, 'is replaced with',vars[var])

#closes file handles
infile.close()
outfile.close()
