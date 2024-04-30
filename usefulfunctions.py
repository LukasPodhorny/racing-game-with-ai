import math
import pygame
from settings import *
import csv
from scipy.interpolate import interp1d

def calculateOffsets (A, B, C, D):
        
    top = (D.y - C.y) * (A.x - C.x) - (D.x - C.x) * (A.y - C.y)
    bottom = (D.x - C.x) * (B.y - A.y) - (D.y - C.y) * (B.x - A.x)
    if bottom != 0.0:
        offset = top / bottom
        if (offset >= 0 and offset <= 1):
            return offset
    
    return None

def getIntersection(A, B, C, D):
    t = calculateOffsets(A, B, C, D)
    u = calculateOffsets(C, D, A, B)
    
    if t and u:
        interp = interp1d(A, B)
        return interp(t)
                    
    return None

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