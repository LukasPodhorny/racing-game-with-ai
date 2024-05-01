import math
import pygame
from settings import *
import csv

def lerp(a: float, b: float, percentage: float) -> float:
    return a + (b-a) * percentage 

def calculateOffsets (A, B, C, D):   
    
    top = (D[1] - C[1]) * (A[0] - C[0]) - (D[0] - C[0]) * (A[1] - C[1])
    bottom = (D[0] - C[0]) * (B[1] - A[1]) - (D[1] - C[1]) * (B[0] - A[0])
    if bottom != 0.0:
        offset = top / bottom
        if (offset >= 0 and offset <= 1):
            return offset
    
    return None

def getIntersection(A, B, C, D):
    t = calculateOffsets(A, B, C, D)
    u = calculateOffsets(C, D, A, B)
    
    if t and u:
        interp_x = lerp(A[0], B[0], t)
        interp_y = lerp(A[1], B[1], t)
        return (interp_x,interp_y)
                    
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
            data.append((float(row['x'])*world_pos, float(row['y'])*world_pos))
    
    return data
