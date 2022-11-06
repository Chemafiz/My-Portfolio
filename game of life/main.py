import numpy as np
import copy
import time
import os


class GameOfLife:
    '''Game of life class'''
    def __init__(self, N, start_size, iterations_number):
        self.N = N
        self.iterations_number = iterations_number
        self.table = np.zeros((N,N), dtype=np.int8)

        index = round((N - start_size)/2)
        self.table[index:(index + start_size), index:(index + start_size)] = 1


    def print_state(self, symbol):
        print("_"*self.N*2)
        for row in self.table:
            print("|", end="")
            print(" ".join(list(map(lambda x: " " if x==0 else symbol, row))), end="")
            print("|")
        print("_" * self.N*2)

    def evolution(self):
        for _ in range(self.iterations_number):
            kopia = copy.deepcopy(self.table)
            self.print_state("#")
            for i, row in enumerate(kopia):
                for j, element in enumerate(row):
                    if element == 0 and self.neighbors_counter(kopia, (i,j)) == 3:
                       self.table[i,j] = 1
                    elif element == 1 and self.neighbors_counter(kopia, (i,j)) != 2 and self.neighbors_counter(kopia, (i,j)) != 3:
                        self.table[i,j] = 0 
            time.sleep(0.2)
            if os.name =="nt":
                os.system("cls")
            else:
                os.system("clear")
                
            

    def neighbors_counter(self,kopia, position):
        counter = kopia[position[0] - 1, position[1] - 1] + \
                  kopia[position[0] - 1, position[1]] + \
                  kopia[position[0] - 1, (position[1] + 1) % self.N]
        
        counter += kopia[position[0], position[1] - 1] + \
                   kopia[position[0], (position[1] + 1) % self.N]

        counter += kopia[(position[0] + 1) % self.N, position[1] - 1] + \
                   kopia[(position[0] + 1) % self.N, position[1]] + \
                   kopia[(position[0] + 1) % self.N, (position[1] + 1) % self.N] 
        return counter



if __name__ == "__main__":
    game= GameOfLife(30, 11, 2000)
    game.evolution()
