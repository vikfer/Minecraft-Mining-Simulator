# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 04:40:05 2019

@author: victo_000
"""

#Minecraft diamond strat

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Chunk:
    def __init__(self):
        self.grid = np.zeros((15,16,16)).astype(int)
        self.diams_init = np.random.poisson(4)#3.7
        while self.diams_init == 0:
            self.diams_init = np.random.poisson(4)
        
        self.diams = self.diams_init
        
        
        self.init_xy = np.floor(np.random.uniform(16,0,2)).astype(int)
        self.init_z = np.floor(np.random.uniform(15)).astype(int)
        
        self.err = 0
        
        while self.diams > 0 and self.err < 1_000:
            seed = np.random.poisson(0.5,3)*np.random.choice([1,-1],3)
            try:
                if self.diams == self.diams_init:
                    self.grid[self.init_z][self.init_xy[0]][self.init_xy[1]] = 1
                    self.diams -= 1
                    #print('generated diam at',[self.init_z],[self.init_xy[0]],[self.init_xy[1]])
                
                elif self.grid[self.init_z + seed[0]][self.init_xy[0] + seed[1]][self.init_xy[1] + seed[2]] == 0:
                                    
                    if (self.grid[self.init_z + seed[0]+1][self.init_xy[0] + seed[1]][self.init_xy[1] + seed[2]] == 1 or
                        self.grid[self.init_z + seed[0]-1][self.init_xy[0] + seed[1]][self.init_xy[1] + seed[2]] == 1 or
                        self.grid[self.init_z + seed[0]][self.init_xy[0] + seed[1]+1][self.init_xy[1] + seed[2]] == 1 or
                        self.grid[self.init_z + seed[0]][self.init_xy[0] + seed[1]-1][self.init_xy[1] + seed[2]] == 1 or
                        self.grid[self.init_z + seed[0]][self.init_xy[0] + seed[1]][self.init_xy[1] + seed[2]+1] == 1 or
                        self.grid[self.init_z + seed[0]][self.init_xy[0] + seed[1]][self.init_xy[1] + seed[2]-1] == 1):
                        
                            self.grid[self.init_z + seed[0]][self.init_xy[0] + seed[1]][self.init_xy[1] + seed[2]] = 1
                            self.diams -= 1
                            #print('generated diam at',[self.init_z + seed[0]],[self.init_xy[0] + seed[1]],[self.init_xy[1] + seed[2]])
                            
                else:
                    self.err += 1
                    
            except IndexError:
                pass
        
        if self.err >= 1_000:
            Chunk() #Fixed, now will try until it works
            #raise GenerationError("Could not Generate Diamonds properly")

    def show(self):
        z,x,y = self.grid.nonzero()
        coords = (z,x,y)
        
        for each in range(len(coords[0])):
            print("Point {}: (x = {}, y = {}, z = {})".format(each+1,coords[2][each],coords[1][each],coords[0][each]))
        
        
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, zdir='z', c='blue')
        
        
        ax.plot([coords[1][0],coords[1][0]],[coords[2][0],coords[2][0]],[0,coords[0][0]],c='red',linestyle='dashed')
        ax.plot([0,coords[1][0]],[coords[2][0],coords[2][0]],[coords[0][0],coords[0][0]],c='red',linestyle='dashed')
        ax.plot([coords[1][0],coords[1][0]],[coords[2][0],16],[coords[0][0],coords[0][0]],c='red',linestyle='dashed')
        
        ax.plot([0,15],[8,8],[10,10],c='green')
        ax.plot([0,15],[8,8],[10,10],c='green')
        ax.plot([0,15],[8,8],[11,11],c='green')
        ax.plot([0,15],[8,8],[11,11],c='green')

        ax.set_xlim3d(0,16)
        ax.set_ylim3d(0,16)
        ax.set_zlim3d(0,16)
        
        ax.set_xlabel('x',fontsize='large')
        ax.set_ylabel('y',fontsize='large')
        ax.set_zlabel('z',fontsize='large')
        ax.set_title('Chunk',fontsize='x-large')

        plt.show()
        #plt.savefig("demo.png")

"""start"""

total_chunks = 100**2
rand = 8 #Mining roughly in middle of chunk

##############################################################################
##############################################################################
##############################################################################

fullplane = np.zeros((total_chunks))
found = 0
print("")
print("Technique 1: 1x2")
for i in range(total_chunks):
    a = Chunk()
    fullplane[i] = a.grid[8:15].sum()
    
    #strat 1: 2x1
    tunel = np.concatenate((a.grid[10][rand],
                            a.grid[11][rand]))
    
    sides = np.concatenate((a.grid[9][rand],   #Down
                            a.grid[12][rand],  #Up
                            a.grid[10][rand-1], #Footleft
                            a.grid[10][rand+1], #Footright
                            a.grid[11][rand-1], #Headleft
                            a.grid[11][rand+1] #Headright
                            ))
    
    if 1 in sides or 1 in tunel:
        found += a.diams_init

print("Total diams in layers 8-15 (7)", int(sum(fullplane)))
print("Total diams found", found)
print("Findrate: {}%".format( np.round(found/sum(fullplane)*100),2))
print("Efficiency (diam/bloc mined): {}%".format(np.round((found/(total_chunks*len(tunel)))*100,4)))

##############################################################################
##############################################################################
##############################################################################

fullplane = np.zeros((total_chunks))
found = 0
print("")
print("Technique 2: 2x2")
for i in range(total_chunks):
    a = Chunk() 
    fullplane[i] = a.grid[8:15].sum()
    
    #strat 1: 2x1
    tunel = np.concatenate((a.grid[10][rand],
                            a.grid[11][rand],
                            a.grid[10][rand+1],
                            a.grid[11][rand+1]))
    
    sides = np.concatenate((a.grid[9][rand],   #Down
                            a.grid[12][rand],  #Up
                            a.grid[10][rand-1], #Footleft
                            a.grid[11][rand-1], #Headleft
                            a.grid[9][rand+1],   #Down
                            a.grid[12][rand+1],  #Up
                            a.grid[10][rand+2], #Footright
                            a.grid[11][rand+2] #Headright
                            ))
    
    if 1 in sides or 1 in tunel:
        found += a.diams_init

print("Total diams in layers 8-15 (7)", int(sum(fullplane)))
print("Total diams found", found)
print("Findrate: {}%".format( np.round(found/sum(fullplane)*100),2))
print("Efficiency (diam/bloc mined): {}%".format(np.round((found/(total_chunks*len(tunel)))*100,4)))

##############################################################################
##############################################################################
##############################################################################

fullplane = np.zeros((total_chunks))
found = 0
print("")
print("Technique 2: 2x3")
for i in range(total_chunks):
    a = Chunk()
    fullplane[i] = a.grid[8:15].sum()
    
    #strat 1: 2x1
    tunel = np.concatenate((a.grid[10][rand],
                            a.grid[11][rand],
                            a.grid[12][rand],
                            a.grid[10][rand+1],
                            a.grid[11][rand+1],
                            a.grid[12][rand+1]))
    
    sides = np.concatenate((a.grid[9][rand],   #Down
                            a.grid[13][rand],  #Up
                            
                            a.grid[10][rand-1], #Footleft
                            a.grid[11][rand-1], #Midleft
                            a.grid[12][rand-1],#Headleft
                            
                            a.grid[9][rand+1],   #Down
                            a.grid[12][rand+1],  #Up
                            
                            a.grid[10][rand+2], #Footright
                            a.grid[11][rand+2], #Midright
                            a.grid[12][rand+2] #Headright
                            ))
    
    if 1 in sides or 1 in tunel:
        found += a.diams_init

print("Total diams in layers 8-15 (7)", int(sum(fullplane)))
print("Total diams found", found)
print("Findrate: {}%".format( np.round(found/sum(fullplane)*100),2))
print("Efficiency (diam/bloc mined): {}%".format(np.round((found/(total_chunks*len(tunel)))*100,4)))

