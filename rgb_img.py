from PIL import Image
import random
import itertools
import math
import os
import os.path
# get image
def get_img():
    img = Image.open('dobby.jpg')  # take the image to be regenerated
    return img 

# converting image to 1-D vector
def img_to_vector(img):
    pixels = list(img.getdata())
    colors = list(itertools.chain(*pixels))
    return colors

# vector to image
def vec_to_image(colors, img):
    width, height = img.size
    img_bytes = bytes(colors)
    im = Image.frombytes("RGB", (width, height), img_bytes)
    im.show()

def the_first_generation(no_of_genes, population):
    population_dna = []
    for j in range(0,population):
        colors_dna = []
        for i in range(0,no_of_genes):
            colors_dna.append(random.randint(0, 255))
        population_dna.append(colors_dna)
        del(colors_dna)
    return population_dna

def fitness_score(dna, target):
    score = 0
    for gene in range(0,len(target)):
        if dna[gene]== target[gene]:
                score+=1
    fitness = score/len(target)*100            
    print("fitness=", fitness)     

def calculate_score(population_record, target):
    selection_probability = []
    for dna in population_record:
        score = 0
        for gene in range(0, len(target)):
            if dna[gene]== target[gene]:
                score+=1
        selection_probability.append(pow((score/len(target)*100), 3))
    return selection_probability     

def save_fittest_dna(fittest):
    with open('fittest.txt', 'a') as f:
        for item in fittest:
            f.write(str(item))
            f.write(" ")
        f.write("\n")    
        
def perform_natural_selection(population_record, selection_prob, mutation_extent):
    population = len(population_record)
    next_generation = []
    for i in range(0, population):  
        parents = random.choices(population_record, weights=selection_prob, k=2)
        child = crossover_slice(parents, mutation_extent) 
        next_generation.append(child)
    return next_generation    
        
def crossover_slice(parents, mutation_extent):
    infant = []
    parentA = parents[0]
    parentB = parents[1]
    midpoint = random.randint(0,len(parentA))
    for i in range(0,midpoint):
        infant.append(parentA[i])
    for i in range(midpoint, len(parentA)):
        infant.append(parentB[i])
    child = mutation(infant, mutation_extent)
    return child

def crossover_random(parents, mutation_extent):
    infant = []
    parentA = parents[0]
    parentB = parents[1]
    for i in range(0,len(parentA)):
        infant.append(random.choice([parentA[i], parentB[i]]))
    child = mutation(infant, mutation_extent)
    return child    

def mutation(infant, mutation_extent):
    chances = list(range(mutation_extent))
    genes_modify = math.floor(len(infant)*mutation_extent/100)
    if genes_modify == 0: 
        genes_modify+=1   
    if random.randint(0,100) in chances:
        for i in range(genes_modify):
            start = random.randint(0,len(infant)-1)
            infant[start] = random.randint(0,255)
    return infant 

def setup():
    mutation_extent = 3
    population = 1000
    generation_count = 0
    original_image = get_img()
    target_dna = img_to_vector(original_image)
    population_record = the_first_generation(len(target_dna), population)
    if os.path.isfile('fittest.txt'):
        os.remove("fittest.txt")
    while True:
        selection_prob = calculate_score(population_record, target_dna)
        population_record = perform_natural_selection(population_record, selection_prob, mutation_extent)
        fittest = population_record[selection_prob.index(max(selection_prob))]
        save_fittest_dna(fittest)
        generation_count += 1
        if generation_count % 500 == 0:
            vec_to_image(fittest,original_image)
        print("generation: ",generation_count)
        fitness_score(fittest,target_dna)   
        if fittest == target_dna:
            print(generation_count, "Generations")
            print("\n**** Image regenerated successfully ****\n")
            break  
setup()        

    
