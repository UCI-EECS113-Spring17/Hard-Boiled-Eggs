from Cube import Cube
import random
import sys

class InvalidMove:
    pass

class CubeSolver:

    def __init__(self, cube):
        self.cube = cube
        self.moves = []

    def execute_algorithm(self, algorithm, front):
        for move in algorithm:
            self._make_move(self._convert_move(front, move))

    def solve(self):
        self._solve_white_cross()
        self._solve_middle()
        self._solve_top_layer()
        self._optimize_moves()

    def print_cube(self):
        color_cube = Cube()
        for i in range(6):
            for x in range(3):
                for y in range(3):
                    color = color_cube.int_to_color(self.cube.face[i][x][y])
                    color_cube.face[i][x][y] = color
        color_cube.print_cube()
        
    def _solve_white_cross(self):
        top_to_bot = ("F2",)
        right_to_bot = ("F",)
        left_to_bot = ("F'",)
        right_top_to_bot = ("R'", "F", "R")
        left_top_to_bot = ("L", "F'", "L'")
        eff_right_top_to_bot = ("R'", "F")
        eff_left_top_to_bot = ("L", "F'")

        solved = [0, 0, 0, 0]
        
        for i in range(4):
            solved[i] = ((self.cube.face[5][1][0] == 5 and self.cube.face[0][1][2] == i) +
                         (self.cube.face[5][2][1] == 5 and self.cube.face[1][1][2] == (i+1)%4) +
                         (self.cube.face[5][1][2] == 5 and self.cube.face[2][1][2] == (i+2)%4) +
                         (self.cube.face[5][0][1] == 5 and self.cube.face[3][1][2] == (i+3)%4))

            if(solved[i] == max(solved)):
                offset = i

        #print("Offset: ", offset)

        count = ((self.cube.face[5][1][0] == 5 and self.cube.face[0][1][2] == offset) +
                 (self.cube.face[5][2][1] == 5 and self.cube.face[1][1][2] == (offset+1)%4) +
                 (self.cube.face[5][1][2] == 5 and self.cube.face[2][1][2] == (offset+2)%4) +
                 (self.cube.face[5][0][1] == 5 and self.cube.face[3][1][2] == (offset+3)%4))
                
        while count != 4:
            if ((self.cube.face[5][1][0] == 5 or self.cube.face[0][1][2] == 5) and
                (self.cube.face[5][2][1] == 5 or self.cube.face[1][1][2] == 5) and
                (self.cube.face[5][1][2] == 5 or self.cube.face[2][1][2] == 5) and
                (self.cube.face[5][0][1] == 5 or self.cube.face[3][1][2] == 5)):
        
                moves = ("F", "R", "B", "L")
                for i in range(4):
                    if self.cube.face[i][1][2] == 5 or self.cube.face[i][1][2] != (i+offset)%4:
                        #print("Getting unstuck")
                        self._make_move(moves[i])
                        break;
                continue

            top = (self.cube.face[4][1][2], self.cube.face[4][2][1], self.cube.face[4][1][0], self.cube.face[4][0][1])
            bot = (self.cube.face[5][1][0], self.cube.face[5][2][1], self.cube.face[5][1][2], self.cube.face[5][0][1])
            stuck = True

            for i in range(4):
                if top[i] == 5 and (count == 0 or self.cube.face[i][1][0] == (i+offset)%4):
                    #print(i, ": top_to_bot")
                    self.execute_algorithm(top_to_bot, i)
                    if count == 0:
                        self._solve_white_cross()
                        return
                    stuck = False
                    break;
                elif self.cube.face[(i+3)%4][2][1] == 5 and (count == 0 or self.cube.face[i][0][1] == (i+offset)%4):
                    #print(i, ": left_to_bot")
                    self.execute_algorithm(left_to_bot, i)
                    if count == 0:
                        self._solve_white_cross()
                        return
                    stuck = False
                    break;
                elif self.cube.face[(i+1)%4][0][1] == 5 and (count == 0 or self.cube.face[i][2][1] == (i+offset)%4):
                    #print(i, ": right_to_bot")
                    self.execute_algorithm(right_to_bot, i)
                    if count == 0:
                        self._solve_white_cross()
                        return
                    stuck = False
                    break;
                elif (count == 0 or top[(i+1)%4] == (i+offset)%4) and self.cube.face[(i+1)%4][1][0] == 5:
                    if count == 0 or not (bot[(i+1)%4] == 5 and self.cube.face[(i+1)%4][1][2] == (i+1+offset)%4):
                        #print(i, ": eff_right_top_to_bot")
                        self.execute_algorithm(eff_right_top_to_bot, i)
                    else:
                        #print(i, ": right_top_to_bot")
                        self.execute_algorithm(right_top_to_bot, i) # add case where last move isnt necessary
                    if count == 0:
                        self._solve_white_cross()
                        return
                    stuck = False
                    break;
                elif (count == 0 or top[(i+3)%4] == (i+offset)%4) and self.cube.face[(i+3)%4][1][0] == 5:
                    if count == 0 or (bot[(i+3)%4] == 5 and self.cube.face[(i+3)%4][1][2] == (i+3+offset)%4):
                        ##print(i, ": eff_left_top_to_bot")
                        self.execute_algorithm(eff_left_top_to_bot, i)
                    else:
                        #print(i, ": left_top_to_bot")
                        self.execute_algorithm(left_top_to_bot, i)
                    if count == 0:
                        self._solve_white_cross()
                        return
                    stuck = False
                    break;

            if stuck == True:
                #print("Twisting bottom")
                self._make_move("D'")
                offset = (offset+1)%4

            count = ((self.cube.face[5][1][0] == 5 and self.cube.face[0][1][2] == offset) +
                     (self.cube.face[5][2][1] == 5 and self.cube.face[1][1][2] == (offset+1)%4) +
                     (self.cube.face[5][1][2] == 5 and self.cube.face[2][1][2] == (offset+2)%4) +
                     (self.cube.face[5][0][1] == 5 and self.cube.face[3][1][2] == (offset+3)%4))

            #print("Count: ", count)
            #self.print()

        if self.cube.face[0][1][2] == 1:
            self._make_move("D")
        elif self.cube.face[0][1][2] == 2:
            self._make_move("D2")
        elif self.cube.face[0][1][2] == 3:
            self._make_move("D'")

        #self.print()

    def _solve_middle(self):
        alg_1 = ("R", "U'", "R'") #t
        alg_2 = ("F'", "U", "F") #t
        alg_3 = ("U'", "R", "U", "R'", "U2", "R", "U'", "R'") #
        alg_4 = ("U", "F'", "U'", "F", "U2", "F'", "U", "F") #
        alg_5 = ("U'", "R", "U2", "R'", "U2", "R", "U'", "R'") #
        alg_6 = ("U", "F'", "U2", "F", "U2", "F'", "U", "F") #
        alg_7 = ("F'", "U", "F", "U2", "R", "U", "R'") #
        alg_8 = ("R", "U'", "R'", "U2", "F'", "U'", "F") #
        alg_9 = ("F'", "U'", "F") #t                   
        alg_10 = ("R", "U", "R'") #t                               
        alg_11 = ("U", "F'", "U'", "F", "U'", "F'", "U'", "F") #
        alg_12 = ("U'", "R", "U", "R'", "U", "R", "U", "R'") #
        alg_13 = ("U'", "R", "U2", "R'", "U", "F'", "U'", "F") #
        alg_14 = ("U", "F'", "U2", "F", "U'", "R", "U", "R'") #
        alg_15 = ("U", "F'", "U", "F", "U'", "F'", "U'", "F") #
        alg_16 = ("U'", "R", "U'", "R'", "U", "R", "U", "R'") #
        alg_17 = ("R", "U2", "R'", "U'", "R", "U", "R'") #
        alg_18 = ("F'", "U2", "F", "U", "F'", "U'", "F") #
        alg_19 = ("U", "R", "U2", "R'", "U", "R", "U'", "R'") #
        alg_20 = ("U'", "F'", "U2", "F", "U'", "F'", "U", "F") #
        alg_21 = ("U2", "R", "U", "R'", "U", "R", "U'", "R'") #
        alg_22 = ("F'", "U", "F", "U2", "F'", "U'", "F") #
        alg_23 = ("U2", "R2", "U2", "R'", "U'", "R", "U'", "R2") #
        alg_24 = ("U2", "F2", "U2", "F", "U", "F'", "U", "F2") #
        alg_25 = ("U", "R", "U'", "R'") #x
        alg_26 = ("U'", "F'", "U", "F") #x
        alg_27 = ("F'", "U'", "F") #x
        alg_28 = ("R", "U", "R'") #x
        alg_29 = ("R", "U'", "R'") #x
        alg_30 = ("F'", "U", "F") #x
        alg_31 = ("U'", "R", "U'", "R'") #x
        alg_32 = ("U", "F'", "U", "F") #x
        alg_33 = ("U'", "R", "U", "R'") #x
        alg_34 = ("U", "F'", "U'", "F") #x
        alg_35 = ("R", "U'", "R'") #x
        alg_36 = ("R", "U", "R'", "U'", "R", "U", "R'") #x
        alg_37 = ("R", "U'", "R'", "U'", "R", "U", "R'") #x
        alg_38 = ("R", "U", "R'", "U2", "R", "U'", "R'") #x
        alg_39 = ("R", "U'", "R'", "U", "F'", "U'", "F") #x
        alg_40 = ("R", "U", "R'", "U'", "R", "U'", "R'") #x
        alg_41 = ("R", "U'", "R'", "U", "F'", "U2", "F") #x
        alg_42 = ("R", "U", "R'") #x (Special case: Stuck or solved but in wrong spot)


        count = 0
        while(True):
#            self.print()
            solved = 0
            for i in range(4):
                if (self.cube.face[i][2][1] == self.cube.face[i][2][2] == i and
                    self.cube.face[(i+1)%4][0][1] == self.cube.face[(i+1)%4][0][2] == (i+1)%4):
                    solved += 1
            modified = False
            count += 1
#            print(solved)

            if (solved == 4 or count > 20):
                break
            
            # Check for best cases (algorithms 1, 2, 9, 10)
            for turn in range(4):
                faces = self.cube.face
                top = (faces[4][0][2], faces[4][1][2],
                       faces[4][2][2], faces[4][2][1],
                       faces[4][2][0], faces[4][1][0],
                       faces[4][0][0], faces[4][0][1])
                
                for i in range(4):
                    if (faces[i][0][0] == faces[i][1][0] == (i+1)%4 and
                        top[2*i] == top[2*i+1] == i):
#                        print("Alg 1")
                        self.execute_algorithm(alg_1, i)
                        modified = True
                    elif (faces[(i+1)%4][1][0] == faces[(i+1)%4][2][0] == i and
                          top[(2*i+3)%8] == top[(2*i+4)%8] == (i+1)%4):
#                        print("Alg 2")
                        self.execute_algorithm(alg_2, i)
                        modified = True
                    elif (faces[(i+1)%4][0][0] == top[(2*i+7)%8] == (i+1)%4 and
                          top[(2*i+2)%8] == faces[(i+3)%4][1][0] == i):
#                        print("Alg 9")
                        self.execute_algorithm(alg_9, i)
                        modified = True
                    elif (faces[i][2][0] == top[(2*i+5)%8] == i and
                          top[(2*i+2)%8] == faces[(i+2)%4][1][0] == (i+1)%4):
#                        print("Alg 10")
                        self.execute_algorithm(alg_10, i)
                        modified = True
                        
                    if modified:
                        break
                    
                if modified:
                    break
                else:
                    self._make_move("U")
            
            if modified:
                continue

            # Check average case algorithms
            for turn in range(4):
                faces = self.cube.face
                top = (faces[4][0][2], faces[4][1][2],
                       faces[4][2][2], faces[4][2][1],
                       faces[4][2][0], faces[4][1][0],
                       faces[4][0][0], faces[4][0][1])
                bot = (faces[5][0][0], faces[5][1][0],
                       faces[5][2][0], faces[5][2][1],
                       faces[5][2][2], faces[5][1][2],
                       faces[5][0][2], faces[5][0][1])

                for i in range(4):
                    # Corner on top, white front
                    if (faces[i][2][0] == 5 and top[(2*i+2)%8] == i):
                        if (top[(2*i+5)%8] == i and faces[(i+2)%4][1][0] == (i+1)%4):
#                            print("Alg 3")
                            self.execute_algorithm(alg_3, i)
                            modified = True
                        elif (top[(2*i+7)%8] == i and faces[(i+3)%4][1][0] == (i+1)%4):
#                            print("Alg 5")
                            self.execute_algorithm(alg_5, i)
                            modified = True
                        elif (top[(2*i+1)%8] == i and faces[i][1][0] == (i+1)%4):
#                            print("Alg 7")
                            self.execute_algorithm(alg_7, i)
                            modified = True
                        elif (top[(2*i+5)%8] == (i+1)%4 and faces[(i+2)%4][1][0] == i):
#                            print("Alg 11")
                            self.execute_algorithm(alg_11, i)
                            modified = True
                        elif (top[(2*i+3)%8] == (i+1)%4 and faces[(i+1)%4][1][0] == i):
#                            print("Alg 13")
                            self.execute_algorithm(alg_13, i)
                            modified = True
                        elif (top[(2*i+1)%8] == (i+1)%4 and faces[i][1][0] == i):
#                            print("Alg 15")
                            self.execute_algorithm(alg_15, i)
                            modified = True

                    # Corner on top, white right   
                    elif (faces[i][2][0] == i and faces[(i+1)%4][0][0] == 5):
                        if (top[(2*i+7)%8] == (i+1)%4 and faces[(i+3)%4][1][0] == i):
#                            print("Alg 4")
                            self.execute_algorithm(alg_4, i)
                            modified = True
                        elif (top[(2*i+5)%8] == (i+1)%4 and faces[(i+2)%4][1][0] == i):
#                            print("Alg 6")
                            self.execute_algorithm(alg_6, i)
                            modified = True
                        elif (top[(2*i+3)%8] == (i+1)%4 and faces[(i+1)%4][1][0] == i):
#                            print("Alg 8")
                            self.execute_algorithm(alg_8, i)
                            modified = True
                        elif (top[(2*i+7)%8] == i and faces[(i+3)%4][1][0] == (i+1)%4):
#                            print("Alg 12")
                            self.execute_algorithm(alg_12, i)
                            modified = True
                        elif (top[(2*i+1)%8] == i and faces[i][1][0] == (i+1)%4):
#                            print("Alg 14")
                            self.execute_algorithm(alg_14, i)
                            modified = True
                        elif (top[(2*i+3)%8] == i and faces[(i+1)%4][1][0] == (i+1)%4):
#                            print("Alg 16")
                            self.execute_algorithm(alg_16, i)
                            modified = True

                    # Corner on top, white up
                    elif (top[(2*i+2)%8] == 5 and faces[i][2][0] == (i+1)%4):
                        if (top[(2*i+3)%8] == i and faces[(i+1)%4][1][0] == (i+1)%4):
#                            print("Alg 17")
                            self.execute_algorithm(alg_17, i)
                            modified = True
                        elif (top[(2*i+5)%8] == i and faces[(i+2)%4][1][0] == (i+1)%4):
#                            print("Alg 19")
                            self.execute_algorithm(alg_19, i)
                            modified = True
                        elif (top[(2*i+7)%8] == i and faces[(i+3)%4][1][0] == (i+1)%4):
#                            print("Alg 21")
                            self.execute_algorithm(alg_21, i)
                            modified = True
                        elif (top[(2*i+1)%8] == (i+1)%4 and faces[i][1][0] == i):
#                            print("Alg 18")
                            self.execute_algorithm(alg_18, i)
                            modified = True
                        elif (top[(2*i+7)%8] == (i+1)%4 and faces[(i+3)%4][1][0] == i):
#                            print("Alg 20")
                            self.execute_algorithm(alg_20, i)
                            modified = True
                        elif (top[(2*i+5)%8] == (i+1)%4 and faces[(i+2)%4][1][0] == i):
#                            print("Alg 22")
                            self.execute_algorithm(alg_22, i)
                            modified = True

                    else:
                        for j in range(4):
                            
                            # Corner on bot, white down
                            if (bot[(2*i+2)%8] == 5 and faces[i][2][2] == j):
                                if (top[(2*i+1)%8] == (j+1)%4 and faces[i][1][0] == j):
#                                    print("Alg 25")
                                    self.execute_algorithm(alg_25, i)
                                    modified = True
                                elif (top[(2*i+3)%8] == j and faces[(i+1)%4][1][0] == (j+1)%4):
#                                    print("Alg 26")
                                    self.execute_algorithm(alg_26, i)
                                    modified = True
                                elif (i != j and faces[i][2][1] == j and
                                      faces[(i+1)%4][0][1] == (j+1)%4):
#                                    print("Alg 42")
                                    self.execute_algorithm(alg_42, i)
                                    modified = True
                            # Corner on bot, white front
                            elif (faces[i][2][2] == 5 and faces[(i+1)%4][0][2] == j):
                                if (top[(2*i+1)%8] == (j+1)%4 and faces[i][1][0] == j):
#                                    print("Alg 27")
                                    self.execute_algorithm(alg_27, i)
                                    modified = True
                                elif (top[(2*i+3)%8] == j and faces[(i+1)%4][1][0] == (j+1)%4):
#                                    print("Alg 29")
                                    self.execute_algorithm(alg_29, i)
                                    modified = True
                            # Corner on bot, white right
                            elif (bot[(2*i+2)%8] == j and faces[(i+1)%4][0][2] == 5):
                                if (top[(2*i+3)%8] == j and faces[(i+1)%4][1][0] == (j+1)%4):
#                                    print("Alg 28")
                                    self.execute_algorithm(alg_28, i)
                                    modified = True
                                elif (top[(2*i+1)%8] == (j+1)%4 and faces[i][1][0] == j):
#                                    print("Alg 30")
                                    self.execute_algorithm(alg_30, i)
                                    modified = True
                            # Edge down and correctly oriented
                            elif (faces[i][2][1] == j and faces[(i+1)%4][0][1] == (j+1)%4):
                                if (faces[i][2][0] == 5 and top[(2*i+2)%8] == j):
#                                    print("Alg 31")
                                    self.execute_algorithm(alg_31, i)
                                    modified = True
                                elif (faces[i][2][0] == j and faces[(i+1)%4][0][0] == 5):
#                                    print("Alg 32")
                                    self.execute_algorithm(alg_32, i)
                                    modified = True
                            # Edge down and incorrectly oriented
                            elif (faces[i][2][1] == (j+1)%4 and faces[(i+1)%4][0][1] == j):
                                if (faces[i][2][0] == 5 and top[(2*i+2)%8] == j):
#                                    print("Alg 33")
                                    self.execute_algorithm(alg_33, i)
                                    modified = True
                                elif (faces[i][2][0] == j and faces[(i+1)%4][0][0] == 5):
#                                    print("Alg 34")
                                    self.execute_algorithm(alg_34, i)
                                    modified = True
                                elif (top[(2*i+2)%8] == 5 and faces[i][2][0] == (j+1)%4):
#                                    print("Alg 35")
                                    self.execute_algorithm(alg_35, i)
                                    modified = True
                            
                            if modified:
                                break
                                    
                    if modified:
                        break
               
                if modified:
                    break
                else:
                    self._make_move("U")
            
            if modified:
                continue

            # Check worst case algorithms
            for turn in range(4):
                faces = self.cube.face
                top = (faces[4][0][2], faces[4][1][2],
                       faces[4][2][2], faces[4][2][1],
                       faces[4][2][0], faces[4][1][0],
                       faces[4][0][0], faces[4][0][1])
                bot = (faces[5][0][0], faces[5][1][0],
                       faces[5][2][0], faces[5][2][1],
                       faces[5][2][2], faces[5][1][2],
                       faces[5][0][2], faces[5][0][1])

                for i in range(4):
                    if (faces[i][1][0] == faces[i][2][0] == (i+1)%4 and
                        top[(2*i+1)%8] == faces[(i+1)%4][0][0] == i):
#                        print("Alg 23")
                        self.execute_algorithm(alg_23, i)
                        modified = True
                    elif (faces[(i+1)%4][0][0] == faces[(i+1)%4][1][0] == i and
                          faces[i][2][0] == top[(2*i+3)%8] == (i+1)%4):
#                        print("Alg 24")
                        self.execute_algorithm(alg_24, i)
                        modified = True
                    else:
                        for j in range(4):
                            # Edge correctly orientated
                            if (faces[i][2][1] == j and faces[(i+1)%4][0][1] == (j+1)%4):
                                if (top[(2*i+2)%8] == 5 and faces[i][2][0] == (j+1)%4):
                                    #print("Alg 36")
                                    self.execute_algorithm(alg_36, i)
                                    modified = True
                                elif (faces[i][2][2] == 5 and bot[(2*i+2)%8] == (j+1)%4):
                                    #print("Alg 37")
                                    self.execute_algorithm(alg_37, i)
                                    modified = True
                                elif (bot[(2*i+2)%8] == j and faces[(i+1)%4][0][2] == 5):
                                    #print("Alg 38")
                                    self.execute_algorithm(alg_38, i)
                                    modified = True
                            # Edge incorrectly oriented
                            elif (faces[i][2][1] == (j+1)%4 and faces[(i+1)%4][0][1] == j):
                                if (faces[i][2][2] == 5 and bot[(2*i+2)%8] == (j+1)%4):
                                    #print("Alg 39")
                                    self.execute_algorithm(alg_39, i)
                                    modified = True
                                elif (bot[(2*i+2)%8] == j and faces[(i+1)%4][0][2] == 5):
                                    #print("Alg 40")
                                    self.execute_algorithm(alg_40, i)
                                    modified = True
                                elif (bot[(2*i+2)%8] == 5 and faces[i][2][2] == j):
                                    #print("Alg 41")
                                    self.execute_algorithm(alg_41, i)
                                    modified = True
                                    
                            if modified:
                                break

                    if modified:
                        break

                if modified:
                    break
                else:
                    self._make_move("U")

            if modified:
                continue

            # Stuck! Force out an unsolved corner and edge pair
            for i in range(4):
                if not (faces[i][2][1] == faces[i][2][2] == i and
                        faces[(i+1)%4][0][1] == faces[(i+1)%4][0][2] == (i+1)%4):
                    #print("Stuck! Alg 42")
                    self.execute_algorithm(alg_42, i)
                    break
            

    def _scramble(self):
        moves = ("F", "R", "B", "L", "U", "D")

        for i in range(50):
            self._make_move(moves[random.randint(0, 5)])
        self._optimize_moves()

    def _scramble_top(self):
        T_alg = ("F", "R", "U", "R'", "U'", "F'")
        L_alg = ("F", "U", "R", "U'", "R'", "F'")
        sune = ("L", "U", "L'", "U", "L", "U2", "L'")
        antisune = ("R'", "U'", "R", "U'", "R'", "U2", "R")
        alg_21 = ("R", "U2", "R'", "U'", "R", "U", "R'", "U'", "R", "U'", "R'")
        Aa_perm = ("R'", "F", "R'", "B2", "R", "F'", "R'", "B2", "R2")
        Ua_perm = ("R", "U'", "R", "U", "R", "U", "R", "U'", "R'", "U'", "R2")


        algs = (T_alg, L_alg, sune, antisune, alg_21, Aa_perm, Ua_perm)

        for i in range(20):
            self.execute_algorithm(algs[random.randint(0, 6)], random.randint(0, 4))
        
    def _orient_LL_edges(self):
        # http://www.rubiksplace.com/speedcubing/guide/
        T_alg = ("F", "R", "U", "R'", "U'", "F'")
        L_alg = ("F", "U", "R", "U'", "R'", "F'")
        
        solved_edges = (self.cube.face[4][1][2] == 4, self.cube.face[4][2][1] == 4,
                        self.cube.face[4][1][0] == 4, self.cube.face[4][0][1] == 4)

        if not False in solved_edges:
            print("Edges already oriented")
        elif not True in solved_edges:
            #print("L + T algorithm")
            self.execute_algorithm(L_alg, 0)
            self.execute_algorithm(T_alg, 1)
        else:
            index = solved_edges.index(True)
            if solved_edges[(index+2)%4]:
                #print("T algorithm")
                self.execute_algorithm(T_alg, (index+1)%4)
            else:
                #print("L algorithm")
                if solved_edges[(index+1)%4]:
                    self.execute_algorithm(L_alg, (index+2)%4)
                else:
                    self.execute_algorithm(L_alg, (index+1)%4)

    def _orient_LL_corners(self):
        # http://www.rubiksplace.com/speedcubing/OLL-algorithms/
        sune = ("L", "U", "L'", "U", "L", "U2", "L'")
        antisune = ("R'", "U'", "R", "U'", "R'", "U2", "R")
        alg_21 = ("R", "U2", "R'", "U'", "R", "U", "R'", "U'", "R", "U'", "R'")
        headlights = ("R", "U2", "R2", "U'", "R2", "U'", "R2", "U2", "R")
        superman = ("R2", "D", "R'", "U2", "R", "D'", "R'", "U2", "R'")
        alg_24 = ("L", "F", "R'", "F'", "L'", "F", "R", "F'") #your version
        alg_25 = ("R'", "F", "R", "B'", "R'", "F'", "R", "B")

        # Indices of faces (Top View):
        #
        #     7_____5
        #  8 |6  Y  3| 4
        #    |Y  Y  Y|
        #  10|9__Y__0| 2
        #     11    1
        #
        
        faces = self.cube.face
        corners = (faces[4][2][2] == 4, faces[0][2][0] == 4, faces[1][0][0] == 4,
                   faces[4][2][0] == 4, faces[1][2][0] == 4, faces[2][0][0] == 4,
                   faces[4][0][0] == 4, faces[2][2][0] == 4, faces[3][0][0] == 4,
                   faces[4][0][2] == 4, faces[3][2][0] == 4, faces[0][0][0] == 4)
        solved_corners = (corners[0], corners[3], corners[6], corners[9])
        num_solved = corners[0] + corners[3] + corners[6] + corners[9]

        if num_solved == 4:
            print("Corners already oriented")
        elif num_solved == 0:
            index = corners.index(True)
            if corners[(index+6)%12]:
                #print("Algorithm 21")
                self.execute_algorithm(alg_21, (index+1)%2)
            else:
                #print("Headlights")
                if corners[(index+4)%12]:
                    self.execute_algorithm(headlights, index//3)
                elif corners[(index+2)%12]:
                    self.execute_algorithm(headlights, ((index+4)//3)%4)
                elif corners[(index+8)%12]:
                    self.execute_algorithm(headlights, ((index+7)//3)%4)
                else:
                    self.execute_algorithm(headlights, ((index+2)//3)%4)
        elif num_solved == 1:
            index = solved_corners.index(True)
            if corners[(3*index+4)%12]:
                #print("Sune")
                self.execute_algorithm(sune, (index+3)%4)
            else:
                #print("Antisune")
                self.execute_algorithm(antisune, (index+2)%4)
        else:
            index = solved_corners.index(True)
            if solved_corners[(index+2)%4]:
                #print("Algorithm 25")
                if corners[(3*index+4)%12]:
                    self.execute_algorithm(alg_25, index)
                else:
                    self.execute_algorithm(alg_25, (index+2)%4)
            else:
                if solved_corners[(index+1)%4]:
                    index += 1
                if corners[(3*index+4)%12]:
                    #print("Algorithm 24")
                    self.execute_algorithm(alg_24, (index+3)%4)
                else:
                    #print("Algorithm 23")
                    self.execute_algorithm(superman, (index+2)%4)

    def _permute_LL_corners(self):
        Aa_perm = ("R'", "F", "R'", "B2", "R", "F'", "R'", "B2", "R2")
        E_perm = ("D", "R'", "D2", "F'", "D", "L", "D'", "F", "D2", "R",
                  "D'", "F'", "L'", "F")

        corners = (self.cube.face[0][0][0], self.cube.face[0][2][0],
                   self.cube.face[1][0][0], self.cube.face[1][2][0],
                   self.cube.face[2][0][0], self.cube.face[2][2][0],
                   self.cube.face[3][0][0], self.cube.face[3][2][0])

        if (corners[0] == corners[1] and corners[4] == corners[5] or
            corners[2] == corners[3] and corners[6] == corners[7]):
               print("Corners already permuted")
        elif corners[0] == corners[1]:
            #print("Aa permutation")
            self.execute_algorithm(Aa_perm, 2)
        elif corners[2] == corners[3]:
            #print("Aa permutation")
            self.execute_algorithm(Aa_perm, 3)
        elif corners[4] == corners[5]:
            #print("Aa permutation")
            self.execute_algorithm(Aa_perm, 0)
        elif corners[6] == corners[7]:
            #print("Aa permutation")
            self.execute_algorithm(Aa_perm, 1)
        else:
            #print("E permutation")
            self.execute_algorithm(E_perm, 0) 

    def _permute_LL_edges(self):
        Ua_perm = ("R", "U'", "R", "U", "R", "U", "R", "U'", "R'", "U'", "R2")
        Ub_perm = ("R2", "U", "R", "U", "R'", "U'", "R'", "U'", "R'", "U", "R'")
        Z_perm = ("U", "R'", "U'", "R", "U'", "R", "U", "R", "U'", "R'", "U",
                  "R", "U", "R2", "U'", "R'", "U")
        H_perm = ("R2", "L2", "D", "R2", "L2", "U2", "R2", "L2", "D", "R2", "L2")

        faces = self.cube.face
        layer = (faces[0][0][0], faces[0][1][0], faces[0][2][0],
                 faces[1][0][0], faces[1][1][0], faces[1][2][0],
                 faces[2][0][0], faces[2][1][0], faces[2][2][0],
                 faces[3][0][0], faces[3][1][0], faces[3][2][0])

        for i in range(0, 12, 3):
            if layer[i] == layer[i+1]:
                if layer[(i+6)%12] == layer[(i+7)%12]:
                    print("Edges already permuted")
                elif layer[(i+4)%12] == layer[(i+9)%12]:
                    #print("Ub permutation")
                    self.execute_algorithm(Ub_perm, ((i+6)%12)//3)
                else:
                    #print("Ua permutation")
                    self.execute_algorithm(Ua_perm, ((i+6)%12)//3)
                return
            
        if layer[1] == layer[6]:
            #print("H permutation")
            self.execute_algorithm(H_perm, 0)
        else:
            #print("Z permutation")
            if layer[1] == layer[3]:
                self.execute_algorithm(Z_perm, 0)
            else:
                self.execute_algorithm(Z_perm, 1)

    def _solve_top_layer(self):
        self._orient_LL_edges()
        self._orient_LL_corners()
        self._permute_LL_corners()
        self._permute_LL_edges()

        if self.cube.face[0][0][0] == 1:
            self._make_move("U'")
        elif self.cube.face[0][0][0] == 2:
            self._make_move("U2")
        elif self.cube.face[0][0][0] == 3:
            self._make_move("U")
    
    # Converts a move from a different cube orientation (Top color must be same)
    def _convert_move(self, front, move):
        face = move[0]
        if face not in ("U", "D") and front != 0:
            move_order = ("F", "R", "B", "L")
            index = move_order.index(face)
            face = move_order[(index+front)%4]

        try:
            move = face + move[1]
        except IndexError:
            move = face
        finally:
            return move

    # Performs a move on the cube and adds it to the move list        
    def _make_move(self, move):
        if   move == "F":
            self.cube.rotate(0, 1)
        elif move == "R":
            self.cube.rotate(1, 1)
        elif move == "B":
            self.cube.rotate(2, 1)
        elif move == "L":
            self.cube.rotate(3, 1)
        elif move == "U":
            self.cube.rotate(4, 1)
        elif move == "D":
            self.cube.rotate(5, 1)
            
        elif move == "F'":
            self.cube.rotate(0, -1)
        elif move == "R'":
            self.cube.rotate(1, -1)
        elif move == "B'":
            self.cube.rotate(2, -1)
        elif move == "L'":
            self.cube.rotate(3, -1)
        elif move == "U'":
            self.cube.rotate(4, -1)
        elif move == "D'":
            self.cube.rotate(5, -1)
            
        elif move == "F2":
            self.cube.rotate(0, 1)
            self.cube.rotate(0, 1)
        elif move == "R2":
            self.cube.rotate(1, 1)
            self.cube.rotate(1, 1)
        elif move == "B2":
            self.cube.rotate(2, 1)
            self.cube.rotate(2, 1)
        elif move == "L2":
            self.cube.rotate(3, 1)
            self.cube.rotate(3, 1)
        elif move == "U2":
            self.cube.rotate(4, 1)
            self.cube.rotate(4, 1)
        elif move == "D2":
            self.cube.rotate(5, 1)
            self.cube.rotate(5, 1)

        else:
            raise InvalidMove()

        self.moves.append(move)

    def _optimize_moves(self):
        num_old_moves = 1;
        num_new_moves = 0;
        while(num_old_moves != num_new_moves):
            prev_move = " "
            for i in range(len(self.moves)):
                move = self.moves[i]
                prev_letter = prev_move[0]
                curr_letter = move[0]
                if(prev_letter == curr_letter):
                    #print("at: ", i, ": ", curr_letter);
                    if(len(prev_move) == 2 and len(move) == 2):
                        if(prev_move[1] == "2" and move[1] == "2"):
                            self.moves[i] = " "
                            self.moves[i-1] = " "
                        elif(prev_move[1] == "2" or move[1] == "2"):
                            self.moves[i] = curr_letter
                            self.moves[i-1] = " "
                        else:
                            self.moves[i] = curr_letter + "2"
                            self.moves[i-1] = " "
                    elif(len(prev_move) == 2 and prev_move[1] == "2"):
                        self.moves[i] = curr_letter + "'"
                        self.moves[i-1] = " "
                    elif(len(move) == 2 and move[1] == "2"):
                        self.moves[i] = curr_letter + "'"
                        self.moves[i-1] = " "
                    elif(len(prev_move) == 1 and len(move) == 1):
                        self.moves[i] = curr_letter + "2"
                        self.moves[i-1] = " "
                    elif(not (len(prev_move) == 1 and len(move) == 1)):
                        self.moves[i] = " "
                        self.moves[i-1] = " "

                prev_move = self.moves[i]
                
            num_old_moves = len(self.moves)
            self.moves = [x for x in self.moves if not x == " "]
            num_new_moves = len(self.moves)