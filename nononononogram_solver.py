from re import A
import numpy as np
import copy


class NonogramSolver:
    def __init__(self, height, width, row_hints, col_hints):
        
        assert len(row_hints) == height, f"len of rows: {len(row_hints)}, is not equal to height: {height}"
        assert len(col_hints) == width, f"len of columns: {len(col_hints)}, is not equal to width: {width}" 

        self.height = height
        self.width = width
        self.row_hints = row_hints
        self.col_hints = col_hints

        self.nonogram = np.zeros((height, width)).astype(int)
    
    def print(self):
        nonogram_print = copy.deepcopy(self.nonogram).tolist()
        for row in nonogram_print:
            for col in range(len(row)):
                if row[col] == 0:
                    row[col] = ""
                if row[col] == -1:
                    row[col] = "."
                if row[col] == 1:
                    row[col] = "X"
        print('\n'.join([''.join(['{:2}'.format(item) for item in row]) 
        for row in nonogram_print]))

    def solve(self):
        solved_rows = [False]*self.height
        solved_cols = [False]*self.width
        while not any(solved_rows) and not any(solved_cols):
            for row_num in range(self.height):
                if not solved_rows[row_num]:
                    self.find_dots(self.nonogram[row_num,:], self.row_hints[row_num])
                    self.find_color(self.nonogram[row_num,:], self.row_hints[row_num])
                    if not 0 in self.nonogram[row_num,:]:
                        solved_rows[row_num] = True

            for col_num in range(self.width):
                if not solved_cols[col_num]:
                    self.find_dots(self.nonogram[:, col_num], self.col_hints[col_num])
                    self.find_color(self.nonogram[:, col_num], self.col_hints[col_num])
                    if not 0 in self.nonogram[:, col_num]:
                        solved_cols[col_num] = True
            break
    
    def find_dots(self, array, hints):
        # hints_a = [int(x[:-1]) for x in hints]
        # zero_args = np.argwhere((array==-1) | (array==1))
        # sub_array = array[zero_args[0]: zero_args[-1]]
        # ones = np.argwhere(array==1)
        # if len(ones) == 0:
        #     return
        # largest = ones[:-1]
        # smallest = ones[0]
        return

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



    def find_color(self, array, hints):
        hints_a = [int(x[:-1]) for x in hints]
        array_len = len(array)
        hint_len = sum(hints_a)+len(hints_a)-1
        rest = array_len - hint_len
        for i, hint in enumerate(hints_a):
            if hint >= rest:
                free_start = sum(hints_a[:i]) + len(hints_a[:i])
                if i == len(hints_a)-1:
                    free_end = array_len-1
                else:
                    free_end = array_len - (sum(hints_a[i+1:])+len(hints_a[i+1:])) - 1
                free_len = free_end-free_start + 1
                # 2*unknown+known = free_len
                # unknonw + unknown + known = free_len
                # unknown + known = hint
                # unknown + hint = free_len
                # unknown = free_len - hint
                unknown = free_len - hint
                overlap_start = free_start+unknown
                overlap_end = free_end - unknown
                array[overlap_start:overlap_end+1] = 1




height = 20
width = 20

rows = [
    ["3a","3a"],
    ["3a","3a"],
    ["3a","3a"],
    ["3a", "10a", "3a"],
    ["20a"],
    ["1a","2a","6a","2a","1a"],
    ["5a","2a","5a"],
    ["6a","6a"],
    ["2a","1a","1a","2a"],
    ["3a","1a","1a","3a"],
    ["4a","4a"],
    ["1a","1a"],
    ["14a"],
    ["2a","2a"],
    ["1a","3a","3a","1a"],
    ["2a","3a","3a","2a"],
    ["3a","3a"],
    ["3a","3a"],
    ["12a"],
    ["8a"],
]

columns = [
    ["3a"],
    ["2a","1a"],
    ["2a","2a","1a"],
    ["2a","2a","2a","3a"],
    ["9a","3a"],
    ["5a","4a","1a","2a"],
    ["5a","1a","2a","1a","2a","2a"],
    ["6a","1a","1a","1a","2a","2a"],
    ["1a","3a","2a","1a","2a","2a"],
    ["1a","1a","2a"],
    ["1a","1a","2a"],
    ["1a","3a","2a","1a","2a","2a"],
    ["6a","1a","1a","1a","2a","2a"],
    ["5a","1a","2a","1a","2a","2a"],
    ["5a","4a","1a","2a"],
    ["9a","3a"],
    ["2a","2a","2a","3a"],
    ["2a","2a","4a"],
    ["2a", "1a"],
    ["3a"],
]

nonogram = NonogramSolver(height, width, rows, columns)

nonogram.solve()
nonogram.print()

