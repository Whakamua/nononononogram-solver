from cmath import inf
import numpy as np
import copy
from typing import List
import matplotlib.pylab as plt
np.set_printoptions(edgeitems=30, linewidth=100000)
import time
from bs4 import BeautifulSoup
from selenium import webdriver
#<3 <3 <3 <3

class NonogramSolver:
    def __init__(self, row_hints, col_hints):
        
        self.height = len(row_hints)
        self.width = len(col_hints)

        self.row_hints = row_hints
        self.col_hints = col_hints

        print(f"Solving a {self.height}x{self.width} nonogram")

        self.nonogram = np.zeros((height, width)).astype(int)
    
    def print(self):
        nonogram_print = copy.deepcopy(self.nonogram).tolist()
        for row in nonogram_print:
            for col_idx in range(len(row)):
                if row[col_idx] == 0:
                    row[col_idx] = ""
                if row[col_idx] == -1:
                    row[col_idx] = "."
                if row[col_idx] == 1:
                    row[col_idx] = "X"
        print('\n'.join([''.join(['{:2}'.format(item) for item in row]) 
        for row in nonogram_print]))

    def solve(self):
        time_now = time.time()
        self.generate_all_candidates()
        print(f"time take to generate candidates: {time.time()-time_now}")
        # initialize that nothing is known with Nones
        self.ground_truth = np.full((self.height, self.width), None)

        solved_rows = [False]*self.height
        solved_cols = [False]*self.width

        counter = 0

        while not all(solved_rows) and not all(solved_cols):
            time_now = time.time()
            for row_num in range(self.height):
                if not solved_rows[row_num]:
                    
                    self.row_candidates[row_num] = self.eliminate_line_candidates(self.ground_truth[row_num], self.row_candidates[row_num])
                    self.ground_truth[row_num] = self.update_ground_truth_line(self.ground_truth[row_num], self.row_candidates[row_num])

                    if len(self.row_candidates[row_num]) == 1:
                        solved_rows[row_num] = True

            for col_num in range(self.width):
                if not solved_cols[col_num]:
                    self.col_candidates[col_num] = self.eliminate_line_candidates(self.ground_truth[:, col_num], self.col_candidates[col_num])
                    self.ground_truth[:, col_num] = self.update_ground_truth_line(self.ground_truth[:, col_num], self.col_candidates[col_num])

                    if len(self.col_candidates[col_num]) == 1:
                        solved_cols[col_num] = True

            counter += 1
            print(f"it: counter, time taken: {time.time()-time_now}")
            if counter >= 125:
                break

    def update_ground_truth_line(self, ground_truth_line, line_candidates):
        is_true = np.prod(line_candidates,axis=0).astype(bool)
        ground_truth_line[is_true] = True

        is_false = np.prod(~line_candidates,axis=0).astype(bool)
        ground_truth_line[is_false] = False

        return ground_truth_line

    def eliminate_line_candidates(self, ground_truth_line, line_candidates):
        legal_candidates = np.equal(ground_truth_line[ground_truth_line != None], line_candidates[:, ground_truth_line != None]).all(1)
        return line_candidates[legal_candidates.astype(bool)]
        

    def generate_all_candidates(self,):
        self.row_candidates = []
        self.col_candidates = []

        for i, row_hint in enumerate(self.row_hints):
            print(f"possible row candidates for row_hints {i}: {row_hint}")
            self.row_candidates.append(self.generate_line_candidates(row_hint, self.width))

        for i, col_hint in enumerate(self.col_hints):
            print(f"possible row candidates for col_hints {i}: {col_hint}")
            self.col_candidates.append(self.generate_line_candidates(col_hint, self.height))
        

    def generate_line_candidates(self, hints: List[int], length):
        time_now = time.time()
        moving_space = length - (sum(hints) + len(hints)-1)
        self.hint_blocks = []
        current_hint_leftmost_pos = 0
        for hint in hints:
            self.hint_blocks.append(list(range(current_hint_leftmost_pos, current_hint_leftmost_pos+moving_space+1)))
            current_hint_leftmost_pos += hint+1

        self.candidates = []
        self.hints = hints
        self.line_length = length

        self.crazy_line_candidate_generator_recursorinator([None]*len(hints), 0)
        candidates = np.vstack(self.candidates)
        print(f"candidates found: {len(self.candidates)}, time taken: {time.time()-time_now}")
        return candidates

    def candidate_to_bool_list(self, candidate):
        bool_list = np.zeros(self.line_length).astype(bool)
        for i in range(len(candidate)):
            bool_list[candidate[i]:candidate[i]+self.hints[i]] = True
        return bool_list            

    def crazy_line_candidate_generator_recursorinator(self, candidate: List[int], hint_block_index: int):
        
        if hint_block_index == 0:
            first_valid_block_pos = 0
        else:
            first_valid_block_pos = (candidate[hint_block_index-1]+self.hints[hint_block_index-1]+1)
        last_valid_block_pos = self.hint_blocks[hint_block_index][-1]


        for i in range(first_valid_block_pos, last_valid_block_pos+1):
            candidate[hint_block_index] = i
            if hint_block_index == (len(self.hint_blocks)-1):
                self.candidates.append(self.candidate_to_bool_list(candidate))
            else:
                self.crazy_line_candidate_generator_recursorinator(candidate, hint_block_index+1)

    def show_solution(self):
        plt.imshow(~self.ground_truth.astype(bool), cmap=plt.cm.gray)
        plt.show()

height = 20
width = 20

rows = [
    [3,3],
    [3,3],
    [3,3],
    [3,10,3],
    [20],
    [1,2,6,2,1],
    [5,2,5],
    [6,6],
    [2,1,1,2],
    [3,1,1,3],
    [4,4],
    [1,1],
    [14],
    [2,2],
    [1,3,3,1],
    [2,3,3,2],
    [3,3],
    [3,3],
    [12],
    [8],
]

columns = [
    [3],
    [2,1],
    [2,2,4],
    [2,2,2,3],
    [9,3],
    [5,4,1,2],
    [5,1,2,1,2,2],
    [6,1,1,1,2,2],
    [1,3,2,1,2,2],
    [4,1,2],
    [4,1,2],
    [1,3,2,1,2,2],
    [6,1,1,1,2,2],
    [5,1,2,1,2,2],
    [5,4,1,2],
    [9,3],
    [2,2,2,3],
    [2,2,4],
    [2,1],
    [3],
]

# rows = [
#     [3, 1, 2],
#     [2, 1, 1],
#     [2, 1, 1],
#     [2, 1],
#     [3, 2],
#     [4, 3],
#     [1, 2, 4],
#     [1, 5, 1],
#     [1, 5, 1],
#     [7, 1]
# ]

# columns = [
#     [6, 1, 1],
#     [7, 2],
#     [1, 2, 1, 1],
#     [5],
#     [4],
#     [1, 3],
#     [4],
#     [2, 2, 1],
#     [1, 4, 1],
#     [7, 1]
# ]

# rows = [
#         [7, 2, 2, 7],
#         [1, 1, 1, 2, 1, 1],
#         [1, 3, 1, 3, 1, 1, 3, 1],
#         [1, 3, 1, 2, 1, 1, 3, 1],
#         [1, 3, 1, 2, 1, 3, 1],
#         [1, 1, 2, 2, 1, 1],
#         [7, 1, 1, 1, 7],
#         [2],
#         [2, 3, 2, 1, 4],
#         [1, 1, 3, 3, 2, 1],
#         [3, 1, 3, 2, 2],
#         [1, 1, 1, 3, 1, 1],
#         [1, 5, 1, 1, 1, 1],
#         [1, 1, 1, 1, 3, 1],
#         [7, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 3, 1, 1, 1, 2, 2],
#         [1, 3, 1, 2, 1, 2, 1, 1],
#         [1, 3, 1, 1, 1, 2],
#         [1, 1, 2, 1, 1],
#         [7, 1, 3, 1]
#       ]
# columns = [
#         [7, 1, 2, 7],
#         [1, 1, 1, 1, 1, 1],
#         [1, 3, 1, 1, 1, 3, 1],
#         [1, 3, 1, 1, 1, 1, 3, 1],
#         [1, 3, 1, 1, 1, 1, 3, 1],
#         [1, 1, 2, 1, 1],
#         [7, 1, 1, 1, 7],
#         [4],
#         [4, 2, 2, 2, 2, 2],
#         [1, 2, 1, 1, 1, 2, 3],
#         [1, 2, 2, 2],
#         [2, 3, 1, 1, 1, 1, 1],
#         [3, 3, 2, 3, 1, 1],
#         [1, 1, 3, 2],
#         [7, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1],
#         [1, 3, 1, 3, 2, 3],
#         [1, 3, 1, 2, 2, 1, 1],
#         [1, 3, 1, 1, 1, 1, 1],
#         [1, 1, 5, 3],
#         [7, 1, 1, 2, 1]
#       ]

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

# URL = "https://www.nonograms.org/nonograms/i/21251"
# URL = "https://www.nonograms.org/nonograms/i/62953"
# URL = "https://www.nonograms.org/nonograms/i/63536" # parrot
# URL = "https://www.nonograms.org/nonograms/i/63530" # fotter
# URL = "https://www.nonograms.org/nonograms/i/63546" #
URL = "https://www.nonograms.org/nonograms/i/57640" # kittycat

page = driver.get(URL)

content = driver.page_source
soup = BeautifulSoup(content)

table = soup.findAll(id = "nonogram_table")
col_hints = table[0].findAll(class_ = "nmtt")
row_hints = table[0].findAll(class_ = "nmtl")

width = len(col_hints[0].findAll('tr')[0].findAll('td'))
height = len(row_hints[0].findAll('tr'))


rows = [[] for _ in range(height)]
columns = [[] for _ in range(width)]

for col in col_hints[0].findAll('tr'):
    cells = col.findAll('td')
    for i,cell in enumerate(cells):
        hint = cell.find('div').contents[0]
        if hint != '\xa0':
            columns[i].append(int(hint))

for i, row in enumerate(row_hints[0].findAll('tr')):
    cells = row.findAll('td')
    for cell in cells:
        hint = cell.find('div').contents[0]
        if hint != '\xa0':
            rows[i].append(int(hint))


nonogram = NonogramSolver(rows, columns)
time_now = time.time()
nonogram.solve()
print(f"time taken to solve: {time.time()-time_now} seconds")
nonogram.show_solution()
