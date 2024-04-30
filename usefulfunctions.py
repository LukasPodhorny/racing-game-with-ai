import math
import pygame
from settings import *
import csv


def distance(point1, point2):
    return math.sqrt(math.pow(point1[0] - point2[0],2) + math.pow(point1[1] - point2[1],2))

def make_track(parameters):
    return pygame.transform.smoothscale_by(pygame.image.load(parameters[0]).convert_alpha(), parameters[1]*world_pos)

def read_col_data(route):
    data = []
    
    with open(route, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((row['x'], row['y']))
    
    return data

def read_col_scalar(route):
    with open(route, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader[0]['scalar'])