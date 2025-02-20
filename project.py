import itertools
import random
from collections import deque
import gurobipy as gp
from gurobipy import GRB
import os

def read_input(file_path):
    #séparation des photos verticales et horizontales
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    N = int(lines[0].strip())
    photos = []
    vertical_photos = []
    
    for i in range(1, N + 1):
        parts = lines[i].strip().split()
        orientation = parts[0]
        tags = set(parts[2:])
        if orientation == 'H':
            photos.append((i - 1, tags))
        else:
            vertical_photos.append((i - 1, tags))
    
    return photos, vertical_photos

def pair_vertical_photos_optimized(vertical_photos):
    #associer les photos veritcales en paires
    model = gp.Model("vertical_pairing")
    
    paired_slides = []
    while len(vertical_photos) > 1:
        p1 = vertical_photos.pop()
        p2 = vertical_photos.pop()
        combined_tags = p1[1].union(p2[1])
        paired_slides.append(((p1[0], p2[0]), combined_tags))
    
    return paired_slides

def optimize_slideshow(slides):
    #optimiser l'odre des diapos
    model = gp.Model("slideshow_ordering")
    model.setParam('OutputFlag', 0)
    
    x = model.addVars(len(slides), vtype=GRB.BINARY, name="x")
    
    model.setObjective(gp.quicksum(x[i] for i in range(len(slides))), GRB.MAXIMIZE)
    
    for i in range(len(slides)):
        model.addConstr(x[i] <= 1)
    
    model.optimize()
    
    ordered_slides = [slides[i] for i in range(len(slides)) if x[i].x > 0.5]
    return ordered_slides

def generate_output(slides, output_file):
    #fichier de sortie
    with open(output_file, 'w') as f:
        f.write(f"{len(slides)}\n")
        for slide in slides:
            if isinstance(slide[0], int):
                f.write(f"{slide[0]}\n")
            else:
                f.write(f"{slide[0][0]} {slide[0][1]}\n")

def solve_hashcode_problem_optimized(input_file, output_file):
    #résolution du problème
    photos, vertical_photos = read_input(input_file)
    vertical_pairs = pair_vertical_photos_optimized(vertical_photos)
    slides = photos + vertical_pairs
    optimized_slides = optimize_slideshow(slides)
    generate_output(optimized_slides, output_file)

def process_all_files(input_folder, output_folder):
    #traitement des fichiers
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name.replace(".txt", "_output.txt"))
            print(f"Traitement de {file_name}...")
            solve_hashcode_problem_optimized(input_path, output_path)
            print(f"Résultat enregistré : {output_path}")

#run
input_folder = "diapo"
output_folder = "outputs"
process_all_files(input_folder, output_folder)
