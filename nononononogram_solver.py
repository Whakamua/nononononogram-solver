from cmath import inf
import numpy as np
import copy
from typing import List
import matplotlib.pylab as plt
np.set_printoptions(edgeitems=30, linewidth=100000)
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
        self.generate_all_candidates()

        # initialize that nothing is known with Nones
        self.ground_truth = np.full((self.height, self.width), None)

        solved_rows = [False]*self.height
        solved_cols = [False]*self.width

        counter = 0
        while not all(solved_rows) and not all(solved_cols):
            for row_num in range(self.height):
                if not solved_rows[row_num]:
                    # find which candidates do not violate the ground truth. So, if ground truth is
                    # true, then candidate should be true. If ground truth is None, then candidate,
                    # can be anything. (should also do this for the false scenario)
                    legal_candidates = np.logical_or(~self.ground_truth[row_num, :], self.row_candidates[row_num]).all(1)
                    self.row_candidates[row_num] = self.row_candidates[row_num][legal_candidates]

                    # np.prod finds which values should for sure be True, if that is the case, it 
                    # should be updated in the ground truth, anything in np.prod is False, then
                    # this should not be updated as false in the ground truth, this is because 
                    # false is considered to be unknown. (it doesn't work like this yet, so needs
                    # to be worked on).
                    # we should also do this for the opposite case, if we know for sure something 
                    # should be false then we update it a false in the ground truth.
                    self.ground_truth[row_num,:] = np.logical_or(self.ground_truth[row_num,:], np.prod(self.row_candidates[row_num],axis=0)).astype(bool)
                    if len(self.row_candidates[row_num]) == 1:
                        solved_rows[row_num] = True


            for col_num in range(self.width):
                if not solved_cols[col_num]:
                    legal_candidates = np.logical_or(~self.ground_truth[:, col_num], self.col_candidates[col_num]).all(1)
                    self.col_candidates[col_num] = self.col_candidates[col_num][legal_candidates]
                    self.ground_truth[:, col_num] = np.logical_or(self.ground_truth[:, col_num], np.prod(self.col_candidates[col_num],axis=0)).astype(bool)
                    if len(self.col_candidates[col_num]) == 1:
                        solved_cols[col_num] = True

            counter += 1
            print(counter)
            if counter >= 2:
                break
        plt.imshow(~self.ground_truth.astype(bool), cmap=plt.cm.gray)
        plt.show()
        breakpoint()


    def generate_all_candidates(self,):
        self.row_candidates = []
        self.col_candidates = []

        for row_hint in self.row_hints:
            self.row_candidates.append(self.generate_line_candidates(row_hint, self.width))

        for col_hint in self.col_hints:
            self.col_candidates.append(self.generate_line_candidates(col_hint, self.height))
        

    def generate_line_candidates(self, hints: List[int], length):
        moving_space = length - (sum(hints) + len(hints)-1)
        self.hint_blocks = []
        current_hint_leftmost_pos = 0
        for hint in hints:
            self.hint_blocks.append(list(range(current_hint_leftmost_pos, current_hint_leftmost_pos+moving_space+1)))
            current_hint_leftmost_pos += hint+1
        # print(self.hint_blocks)

        self.candidates = []
        self.hints = hints
        self.line_length = length

        self.crazy_line_candidate_generator_recursorinator([None]*len(hints), 0)
        return np.vstack(self.candidates)

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

    # def legal_candidate(candidate: List[int]) -> bool:






        # while True:
        #     for i in reversed(range(len(hints))):
        #         last_hint_idx = hint_start_indices[i] + hints[i] - 1
        #         if last_hint_idx == length-1:
        #             continue
        #         elif last_hint_idx == length-2:
        #             pass
        #         elif not current_solution[last_hint_idx + 1] and not current_solution[last_hint_idx + 2]:
        #             pass
        #         else
        #             continue
                
        #         current_solution = self.move_block(current_solution, hint_start_indices[i], last_hint_idx)

        #         hint_start_indices[i] += 1
        #         solutions = np.vstack([solutions, [current_solution]])
        #     print(solutions)
        #     break

    # def move_block(self, current_solution: List[bool], block_start: int, block_end: int):
    #     current_solution[block_start] = False
    #     current_solution[block_end+1] = True
    #     return current_solution
    

        


    # def get_clusters(self, array):
    #     clusters = []
    #     cluster_number = -1
    #     prev_one_idx = -np.inf
    #     for idx, value in enumerate(array):
    #         if value == 1:
    #             if prev_one_idx+1 == idx:
    #                 clusters[cluster_number].append(idx)
    #             if prev_one_idx+1 != idx:
    #                 clusters.append([idx])
    #                 cluster_number+=1
    #             prev_one_idx = idx
    #     return clusters
    
    # def find_dots(self, array, hints):
    #     ones = np.squeeze(np.argwhere(array==1), axis=1)
    #     if len(ones) == 0:
    #         return
    #     rightest_color_idx = ones[-1]
    #     leftest_color_idx = ones[0]
    #     rightest_hint = hints[-1]
    #     leftest_hint = hints[0]
    #     empty_cells_right = self.width-rightest_color_idx-1
    #     empty_cells_left = leftest_color_idx

    #     dots_right = max(empty_cells_right-rightest_hint, 1)
    #     dots_left = max(empty_cells_left - leftest_hint, 0)
        
    #     if empty_cells_right == rightest_hint:
    #         breakpoint()
    #         array[-dots_right:] = -1
    #     if empty_cells_left == leftest_hint:
    #         breakpoint()
    #         array[:dots_left] = -1

    #     return

        # [2, 8, 2]
        # [1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,0,0]
        # [_,_,_,_,_,_,1,1,1,1,1,_,_,_,_,_,_]
        # [_,_,_,-,-,-,-,-,-,-,-,-,-,-,_,_,_]

        # arraylen = 17
        # hint_len = 14
        # rest = 3
        # free_start = 3
        # free_end = 13
        # free_len = 11
        # unknown = 3
        # overlap_start = 6
        # overlap_end = 10

    # def create_subArray():


    # def find_color(self, array, hints):
    #     array_len = len(array)
    #     hint_len = sum(hints)+len(hints)-1
    #     rest = array_len - hint_len
    #     for i, hint in enumerate(hints):
    #         if hint >= rest:
    #             free_start = sum(hints[:i]) + len(hints[:i])
    #             if i == len(hints)-1:
    #                 free_end = array_len-1
    #             else:
    #                 free_end = array_len - (sum(hints[i+1:])+len(hints[i+1:])) - 1
    #             free_len = free_end-free_start + 1
    #             # 2*unknown+known = free_len
    #             # unknonw + unknown + known = free_len
    #             # unknown + known = hint
    #             # unknown + hint = free_len
    #             # unknown = free_len - hint
    #             unknown = free_len - hint
    #             overlap_start = free_start+unknown
    #             overlap_end = free_end - unknown
    #             array[overlap_start:overlap_end+1] = 1




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
    [2,2,1],
    [2,2,2,3],
    [9,3],
    [5,4,1,2],
    [5,1,2,1,2,2],
    [6,1,1,1,2,2],
    [1,3,2,1,2,2],
    [1,1,2],
    [1,1,2],
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

rows = [
    [3, 1, 2],
    [2, 1, 1],
    [2, 1, 1],
    [2, 1],
    [3, 2],
    [4, 3],
    [1, 2, 4],
    [1, 5, 1],
    [1, 5, 1],
    [7, 1]
]

columns = [
    [6, 1, 1],
    [7, 2],
    [1, 2, 1, 1],
    [5],
    [4],
    [1, 3],
    [4],
    [2, 2, 1],
    [1, 4, 1],
    [7, 1]
]

nonogram = NonogramSolver(rows, columns)

nonogram.solve()

# nonogram.solve()
# nonogram.print()

