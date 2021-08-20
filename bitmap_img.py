from PIL import Image
import itertools
import random
import math
import matplotlib.pyplot as plt
import os
import os.path


def get_img():
    img = Image.open('dobby.jpg')  
    return img 

def to_bitmap(img):
    threshold = 130
    pixels = list(img.getdata())
    newPixels = []
    for pixel in pixels:
        if pixel[0] <= threshold:
            newPixel = (0, 0, 0)
        else:
            newPixel = (255, 255, 255)
        newPixels.append(newPixel)
    newImg = Image.new(img.mode, img.size)
    newImg.putdata(newPixels)
    return newImg, newPixels

def bitmap_to_bit(newPixels):
    bit_pixels = []
    for pixel in newPixels:
        if pixel[0] == 255:
            bit_pixels.append(1)
        elif pixel[0] == 0:
            bit_pixels.append(0)
    return bit_pixels

def bit_pixel_to_bitmap(bit_pixel):
    bit_map = []
    for bit in bit_pixel:
        if bit == 0:
            bit_map.append((0,0,0))
        elif bit == 1:
            bit_map.append((255,255,255))
    return bit_map

def bitmap_to_image(bit_pixel, img):
    bit_map = bit_pixel_to_bitmap(bit_pixel)
    colors = list(itertools.chain(*bit_map))
    width, height = img.size
    img_bytes = bytes(colors)
    im = Image.frombytes("RGB", (width, height), img_bytes)
    im.show()
               
def the_first_generation(no_of_genes, population):
    population_dna = []
    for j in range(0,population):
        colors_dna = []
        for i in range(0,no_of_genes):
            colors_dna.append(random.choice([0,1]))
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
    return fitness   

def calculate_score(population_record, target):
    selection_probability = []
    for dna in population_record:
        score = 0
        for gene in range(0, len(target)):
            if dna[gene]== target[gene]:
                score+=1
        selection_probability.append(pow((score/len(target)*100), 3))
    return selection_probability   

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
            infant[start] = random.choice([0,1])
    return infant 

def save_fittest_dna(fittest):
    f = open('fittest_bit.txt', 'a')
    for items in fittest:
        f.write(str(items))
        f.write(" ")
    f.write("\n")
    f.close()

def analytics(fitness_record, img, view_gen):
    x=[]
    for i in range(1,len(fitness_record)+1):
        x.append(i) 
    plt.plot(x, fitness_record)
    plt.xlabel('Generations')
    plt.ylabel('Fitness Percentage')
    plt.title('** Evolution Curve **')
    f = open('fittest_bit.txt', 'r')   
    all_lines = f.readlines()
    bits = all_lines[view_gen-1]
    bit_list = list(map(int, bits.split()))
    plt.show()    
    bitmap_to_image(bit_list, img)
    
def setup():
    population = 500
    mutation_extent = 3
    generation_count = 0
    fitness_record = []
    compromise = 30
    if os.path.isfile('fittest_bit.txt'):
        os.remove("fittest_bit.txt")
    original_img = get_img()
    bitmap_image, bitmap_pixels = to_bitmap(original_img)
    target_bit_pixels = bitmap_to_bit(bitmap_pixels)
    population_record = the_first_generation(len(target_bit_pixels), population)
    while True:
        selection_prob = calculate_score(population_record, target_bit_pixels)
        population_record = perform_natural_selection(population_record, selection_prob, mutation_extent)
        fittest = population_record[selection_prob.index(max(selection_prob))]
        save_fittest_dna(fittest)
        generation_count += 1
        print("generation: ",generation_count)
        fitness_value = fitness_score(fittest,target_bit_pixels)
        fitness_record.append(fitness_value)  
        if fittest == target_bit_pixels or fitness_value >= 100-compromise:
            print(generation_count, "Generations")
            print("\n**** Image regenerated successfully ****\n")
            generation_to_visit = generation_count
            analytics(fitness_record, original_img, generation_to_visit)
            break
setup()    
   
