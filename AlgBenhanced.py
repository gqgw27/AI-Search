import os
import sys
import time
import random

def read_file_into_string(input_file, from_ord, to_ord):
    # take a file "input_file", read it character by character, strip away all unwanted
    # characters with ord < "from_ord" and ord > "to_ord" and return the concatenation
    # of the file as the string "output_string"
    the_file = open(input_file,'r')
    current_char = the_file.read(1)
    output_string = ""
    while current_char != "":
        if ord(current_char) >= from_ord and ord(current_char) <= to_ord:
            output_string = output_string + current_char
        current_char = the_file.read(1)
    the_file.close()
    return output_string

def stripped_string_to_int(a_string):
    # take a string "a_string" and strip away all non-numeric characters to obtain the string
    # "stripped_string" which is then converted to an integer with this integer returned
    a_string_length = len(a_string)
    stripped_string = "0"
    if a_string_length != 0:
        for i in range(0,a_string_length):
            if ord(a_string[i]) >= 48 and ord(a_string[i]) <= 57:
                stripped_string = stripped_string + a_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def get_string_between(from_string, to_string, a_string, from_index):
    # look for the first occurrence of "from_string" in "a_string" starting at the index
    # "from_index", and from the end of this occurrence of "from_string", look for the first
    # occurrence of the string "to_string"; set "middle_string" to be the sub-string of "a_string"
    # lying between these two occurrences and "to_index" to be the index immediately after the last
    # character of the occurrence of "to_string" and return both "middle_string" and "to_index"
    middle_string = ""              # "middle_string" and "to_index" play no role in the case of error
    to_index = -1                   # but need to initialized to something as they are returned
    start = a_string.find(from_string,from_index)
    if start == -1:
        flag = "*** error: " + from_string + " doesn't appear"
        #trace_file.write(flag + "\n")
    else:
        start = start + len(from_string)
        end = a_string.find(to_string,start)
        if end == -1:
            flag = "*** error: " + to_string + " doesn't appear"
            #trace_file.write(flag + "\n")
        else:
            middle_string = a_string[start:end]
            to_index = end + len(to_string)
            flag = "good"
    return middle_string,to_index,flag

def string_to_array(a_string, from_index, num_cities):
    # convert the numbers separated by commas in the file-as-a-string "a_string", starting from index "from_index",
    # which should point to the first comma before the first digit, into a two-dimensional array "distances[][]"
    # and return it; note that we have added a comma to "a_string" so as to find the final distance
    # distance_matrix = []
    if from_index >= len(a_string):
        flag = "*** error: the input file doesn't have any city distances"
        #trace_file.write(flag + "\n")
    else:
        row = 0
        column = 1
        row_of_distances = [0]
        flag = "good"
        while flag == "good":
            middle_string, from_index, flag = get_string_between(",", ",", a_string, from_index)
            from_index = from_index - 1         # need to look again for the comma just found
            if flag != "good":
                flag = "*** error: there aren't enough cities"
                # trace_file.write(flag + "\n")
            else:
                distance = stripped_string_to_int(middle_string)
                row_of_distances.append(distance)
                column = column + 1
                if column == num_cities:
                    distance_matrix.append(row_of_distances)
                    row = row + 1
                    if row == num_cities - 1:
                        flag = "finished"
                        row_of_distances = [0]
                        for i in range(0, num_cities - 1):
                            row_of_distances.append(0)
                        distance_matrix.append(row_of_distances)
                    else:
                        row_of_distances = [0]
                        for i in range(0,row):
                            row_of_distances.append(0)
                        column = row + 1
        if flag == "finished":
            flag = "good"
    return flag

def make_distance_matrix_symmetric(num_cities):
    # make the upper triangular matrix "distance_matrix" symmetric;
    # note that there is nothing returned
    for i in range(1,num_cities):
        for j in range(0,i):
            distance_matrix[i][j] = distance_matrix[j][i]

# read input file into string

#######################################################################################################
############ now we read an input file to obtain the number of cities, "num_cities", and a ############
############ symmetric two-dimensional list, "distance_matrix", of city-to-city distances. ############
############ the default input file is given here if none is supplied via a command line   ############
############ execution; it should reside in a folder called "city-files" whether it is     ############
############ supplied internally as the default file or via a command line execution.      ############
############ if your input file does not exist then the program will crash.                ############

input_file = "AISearchfile175.txt"

#######################################################################################################

# you need to worry about the code below until I tell you; that is, do not touch it!

if len(sys.argv) == 1:
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
else:
    input_file = sys.argv[1]
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
file_string = file_string + ","         # we need to add a final comma to find the city distances
                                        # as we look for numbers between commas
print("I'm working with the file " + input_file + ".")
                                        
# get the name of the file

name_of_file,to_index,flag = get_string_between("NAME=", ",", file_string, 0)

if flag == "good":
    print("I have successfully read " + input_file + ".")
    # get the number of cities
    num_cities_string,to_index,flag = get_string_between("SIZE=", ",", file_string, to_index)
    num_cities = stripped_string_to_int(num_cities_string)
else:
    print("***** ERROR: something went wrong when reading " + input_file + ".")
if flag == "good":
    print("There are " + str(num_cities) + " cities.")
    # convert the list of distances into a 2-D array
    distance_matrix = []
    to_index = to_index - 1             # ensure "to_index" points to the comma before the first digit
    flag = string_to_array(file_string, to_index, num_cities)
if flag == "good":
    # if the conversion went well then make the distance matrix symmetric
    make_distance_matrix_symmetric(num_cities)
    print("I have successfully built a symmetric two-dimensional array of city distances.")
else:
    print("***** ERROR: something went wrong when building the two-dimensional array of city distances.")

#######################################################################################################
############ end of code to build the distance matrix from the input file: so now you have ############
############ the two-dimensional "num_cities" x "num_cities" symmetric distance matrix     ############
############ "distance_matrix[][]" where "num_cities" is the number of cities              ############
#######################################################################################################

# now you need to supply some parameters ...

#######################################################################################################
############ YOU NEED TO INCLUDE THE FOLLOWING PARAMETERS:                                 ############
############ "my_user_name" = your user-name, e.g., mine is dcs0ias                        ############

my_user_name = "gqgw27"

############ "my_first_name" = your first name, e.g., mine is Iain                         ############

my_first_name = "Daniel Reju"

############ "my_last_name" = your last name, e.g., mine is Stewart                        ############

my_last_name = "Thomas"

############ "alg_code" = the two-digit code that tells me which algorithm you have        ############
############ implemented (see the assignment pdf), where the codes are:                    ############
############    BF = brute-force search                                                    ############
############    BG = basic greedy search                                                   ############
############    BS = best_first search without heuristic data                              ############
############    ID = iterative deepening search                                            ############
############    BH = best_first search with heuristic data                                 ############
############    AS = A* search                                                             ############
############    HC = hilling climbing search                                               ############
############    SA = simulated annealing search                                            ############
############    GA = genetic algorithm                                                     ############

alg_code = "GA"

############ you can also add a note that will be added to the end of the output file if   ############
############ you like, e.g., "in my basic greedy search, I broke ties by always visiting   ############
############ the first nearest city found" or leave it empty if you wish                   ############

added_note = ""

############ the line below sets up a dictionary of codes and search names (you need do    ############
############ nothing unless you implement an alternative algorithm and I give you a code   ############
############ for it when you can add the code and the algorithm to the dictionary)         ############

codes_and_names = {'BF' : 'brute-force search',
                   'BG' : 'basic greedy search',
                   'BS' : 'best_first search without heuristic data',
                   'ID' : 'iterative deepening search',
                   'BH' : 'best_first search with heuristic data',
                   'AS' : 'A* search',
                   'HC' : 'hilling climbing search',
                   'SA' : 'simulated annealing search',
                   'GA' : 'genetic algorithm'}

#######################################################################################################
############    now the code for your algorithm should begin                               ############
#######################################################################################################

def check_tour_length(T):
    length = 0
    for i in range(len(T)-1):
        length += distance_matrix[T[i]][T[i+1]]
    length += distance_matrix[T[0]][T[-1]]
    return length

def generate_random_tour():
    T = []
    for i in range(num_cities):
        T.append(i)
    random.shuffle(T)
    return T

def select_parent(P): #P is probability distribution
    p = random.uniform(0,1)
    for i in range(len(P)-1):
        lower = P[i]
        upper = P[i+1]
        if lower <= p < upper:
            return i
    return len(P)-2

def mutate2(L):
    l = len(L)
    i = random.randint(0,l-2)
    j = random.randint(0,l-2)
    while j == i:
        j = random.randint(0,l-1)
    if j < i:
        ci = i
        i = j
        j = ci
   
    start = L[:i]
    middle = L[i:j+1]
    middle.reverse()
    end = L[j+1:]

    return (start+middle+end)

#Order Crossover Operator
def crossover1(P1,P2):
    L = len(P1)
    cut1 = random.randint(0,L-1)
    cut2 = random.randint(0,L-1)
    
    while cut2 == cut1:
        cut2 = random.randint(0,L-1)
    if cut2 < cut1:
        c2 = cut2
        cut2 = cut1
        cut1 = c2

    cent1 = P1[cut1+1:cut2+1]
    cent2 = P2[cut1+1:cut2+1]
    
    order1 = P1[cut2+1:]+P1[:cut2+1]
    order2 = P2[cut2+1:]+P2[:cut2+1]
    for v in cent1:
        order2.remove(v)
    for v in cent2:
        order1.remove(v)

    end1 = order2[:L-cut2-1]
    end2 = order1[:L-cut2-1]
    start1 = order2[L-cut2-1:]
    start2 = order1[L-cut2-1:]

    child1 = start1+cent1+end1
    child2 = start2+cent2+end2
    
    return (child1,child2)

def two_opt(T):
    l = len(T)
    prev = 0
    for rep in range(l):
        min_i = 0
        min_j = 1
        change = 0
        for i in range(l-1):
            s1 = distance_matrix[T[i]][T[i+1]]
            s2 = distance_matrix[T[i+1]][T[(i+2)%num_cities]]
            for j in range(i+1,l-1):
                s4 = distance_matrix[T[j]][T[j+1]]
                a1 = distance_matrix[T[i]][T[j]]
                a4 = distance_matrix[T[i+1]][T[j+1]]
                if j == i+2:
                    diff = a1+a4-s1-s4
                else:
                    s3 = distance_matrix[T[j-1]][T[j]]
                    a2 = distance_matrix[T[(i+2)%num_cities]][T[j]]
                    a3 = distance_matrix[T[i+1]][T[j-1]]
                    diff = a1+a2+a3+a4-s1-s2-s3-s4
                if diff < change:
                    change = diff
                    min_i,min_j = i,j
        if change == 0:
            break
        prev += change
        
        b = T[min_j]
        T[min_j] = T[min_i+1]
        T[min_i+1] = b
        
    return prev

def best(L1,L2,l1,l2):
    if l1 < l2:
        return (L1,l1)
    else:
        return (L2,l2)

def greedy(M):
    BEST = []
    LENGTH = -1
    
    cities = {}
    for i in range(num_cities):
        cities[i] = 0

    tour = []
    tour.append(0)
    tour_length = 0
    del cities[0]

    while cities != {}:
        last = tour[-1]
        neighbours = M[last]
        l = len(neighbours)
        best = -1
        node = -1
        for n in range(l):
            if n not in tour:
                d = neighbours[n]
                if best == -1:
                    best = d
                    node = n
                elif d < best:
                    best = d
                    node = n
        tour.append(node)
        tour_length += best
        del cities[node]

    tour_length += M[0][tour[-1]]

    if LENGTH == -1:
        LENGTH = tour_length
        BEST = tour
    elif tour_length < LENGTH:
        LENGTH = tour_length
        BEST = tour

    tour = BEST
    tour_length = LENGTH

    return tour,tour_length

# Setting up initial population,fitness and probabolity distribution
P_Size = 2000
Gen = 400
POP = []
Fitness = []

# Add a proportion of the population as mutated greedy to speed up
greed = int(P_Size/8)
for i in range(greed):
    t1,tl = greedy(distance_matrix)
    t1 = mutate2(t1)
    tl = check_tour_length(t1)
    POP.append(t1)
    Fitness.append(1/tl)

for i in range(P_Size-greed):
    T = generate_random_tour()
    POP.append(T)
    Fitness.append(1/check_tour_length(T))

BEST = POP[0]
SMALLEST = 1/Fitness[0]

# Repeat multiple times
for rep in range(Gen):
    SUM = 1/sum(Fitness)
    PROB = [0]

    for f in Fitness:
        PROB.append(PROB[-1]+SUM*f)

    Children = []
    Children_Fitness = []
    
    # Making children
    for i in range(P_Size):
        p1 = random.randint(0,P_Size-1)
        p2 = random.randint(0,P_Size-1)
        while p2 == p1:
            p2 = random.randint(0,P_Size-1)

        Parent1 = POP[p1]
        Parent2 = POP[p2]
        lp1 = round(1/Fitness[p1])
        lp2 = round(1/Fitness[p2])
        
        child1,child2 = crossover1(Parent1,Parent2)

        # Mutate each child with a fixed probability
        p_mutate = random.random()
        if p_mutate < 0.2:
            child1 = mutate2(child1)
        p_mutate = random.random()
        if p_mutate < 0.2:
            child2 = mutate2(child2)
  
        
        l1 = check_tour_length(child1)
        l2 = check_tour_length(child2)

        bestp,smallp = best(Parent1,Parent2,lp1,lp2)
        bestc,smallc = best(child1,child2,l1,l2)
        bst,small = best(bestp,bestc,smallp,smallc)
        
        Children.append(bst)
        Children_Fitness.append(1/small)

        if small < SMALLEST:
            SMALLEST = small
            BEST = bst

    POP = Children
    Fitness = Children_Fitness

tour = BEST
tour_length = SMALLEST
tour_length += two_opt(tour)

tour_length = check_tour_length(tour)

#######################################################################################################
############ the code for your algorithm should now be complete and you should have        ############
############ computed a tour held in the list "tour" of length "tour_length"               ############
#######################################################################################################

# you do not need to worry about the code below; that is, do not touch it

#######################################################################################################
############ start of code to verify that the constructed tour and its length are valid    ############
#######################################################################################################

check_tour_length = 0
for i in range(0,num_cities-1):
    check_tour_length = check_tour_length + distance_matrix[tour[i]][tour[i+1]]
check_tour_length = check_tour_length + distance_matrix[tour[num_cities-1]][tour[0]]
flag = "good"
if tour_length != check_tour_length:
    flag = "bad"
if flag == "good":
    print("Great! Your tour-length of " + str(tour_length) + " from your " + codes_and_names[alg_code] + " is valid!")
else:
    print("***** ERROR: Your claimed tour-length of " + str(tour_length) + "is different from the true tour length of " + str(check_tour_length) + ".")

#######################################################################################################
############ start of code to write a valid tour to a text (.txt) file of the correct      ############
############ format; if your tour is not valid then you get an error message on the        ############
############ standard output and the tour is not written to a file                         ############
############                                                                               ############
############ the name of file is "my_user_name" + mon-dat-hr-min-sec (11 characters);      ############
############ for example, dcs0iasSep22105857.txt; if dcs0iasSep22105857.txt already exists ############
############ then it is overwritten                                                        ############
#######################################################################################################

if flag == "good":
    local_time = time.asctime(time.localtime(time.time()))   # return 24-character string in form "Tue Jan 13 10:17:09 2009"
    output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
                                                             # output_file_time = mon + day + hour + min + sec (11 characters)
    output_file_name = my_user_name + output_file_time + ".txt"
    f = open(output_file_name,'w')
    f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + ")\n")
    f.write("ALGORITHM = " + alg_code + ", FILENAME = " + name_of_file + "\n")
    f.write("NUMBER OF CITIES = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + "\n")
    f.write(str(tour[0]))
    for i in range(1,num_cities):
        f.write("," + str(tour[i]))
    if added_note != "":
        f.write("\nNOTE = " + added_note)
    f.close()
    print("I have successfully written the tour to the output file " + output_file_name + ".")
    
    
