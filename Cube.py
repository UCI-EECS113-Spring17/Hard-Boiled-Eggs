import random
#import queue
import copy

class Cube:

    def __init__(self, preset = []):
        if(len(preset) == 0):
            self.face = self._get_solved();
        else:
            self.face = preset;
        self.last_move = (0, 0);
        self.move_list = []

    def rotate(self, color, amount):
        self.last_move = (color, amount)
        self.move_list.append( (color,amount) )
        self._rotate_face(color, amount)
        self._rotate_sides(color, amount)

    def rotate_random(self, turns):
        for i in range(turns):
            rand_move = self.random_move()
            self.rotate(rand_move[0], rand_move[1])

    def random_move(self):
        while True:
            rand_move = (random.randint(0,5), random.choice([-1,1]))
            if rand_move != self.last_move:
                return rand_move;
    def int_to_color(self, color):
        if color == 0:
            return "G"
        elif color == 1:
            return "O"
        elif color == 2:
            return "B"
        elif color == 3:
            return "R"
        elif color == 4:
            return "Y"
        elif color == 5:
            return "W"
            
    def solve(self):
        self._solve_cross()

    def _solve_cross(self):
        print("Solving for cross...")
        temp = copy.deepcopy(self)
        visited = [temp]
        #q = queue.Queue()
        #q.put(temp)
        q = []
        q.append(temp)
        stage = 0
        it = 0
        deleted = 0
        while(len(q) != 0):
            #child = q.get()
            child = q.pop(0)
            count = ((child.face[0][0][1] == 0 and child.face[3][2][1] == 3)
                    +(child.face[0][1][0] == 0 and child.face[4][1][2] == 4)
                    +(child.face[0][2][1] == 0 and child.face[1][0][1] == 1)
                    +(child.face[0][1][2] == 0 and child.face[5][1][0] == 5))
            it += 1

            if (stage < 1 and count == 1):
                print("Stage 1")
                print("iteration: " + str(it))
                it = 0
                stage = 1
                child.print_cube()
                #q = queue.Queue()
                q = []
            if (stage < 2 and count == 2):
                print("Stage 2")
                print("iteration: " + str(it))
                it = 0
                stage = 2
                child.print_cube()
                #q = queue.Queue()
                q = []
            if (stage < 3 and count == 3):
                stage = 3
                print("Stage 3")
                print("iteration: " + str(it))
                print("deleted: " + str(deleted))
                it = 0
                deleted = 0
                child.print_cube()
                #q = queue.Queue()
                q = []
            if (count == 4):
                print("This next one is it")
                print("iteration: " + str(it))
                print("deleted: " + str(deleted))
                child.print_cube()
                self.face = child.face
                print(self.move_list)
                return

            for color in range(6):
                temp = copy.deepcopy(child)
                temp.rotate(color, -1)
                if (stage >= 2):
                    if ( (child.face[0][0][1] == 0) + (child.face[0][1][0] == 0) + (child.face[0][2][1] == 0) + (child.face[0][1][2] == 0) < stage ):
                        deleted += 1
                        break
                if(not temp in visited):
                    visited.append(temp)
                    #q.put(temp)
                    q.append(temp)

    def _rotate_face(self, color, amount):
        temp = [[0]*3 for i in range(3)];
        for i in range(3):
            for j in range(3):
                if(amount == 1):
                    temp[2-j][i] = self.face[color][i][j];
                elif(amount == -1):
                    temp[j][2-i] = self.face[color][i][j];
        self.face[color] = temp;

    def _get_solved(self):
        solved = [];
        for j in range(6):
            solved.append([[j]*3 for i in range(3)]);
        return solved;

    def _rotate_sides(self, color, amount):
        if(color == 0): #WHITE
            if(amount == 1): #CLOCKWISE
                temp0 = self.face[1][0][0];
                temp1 = self.face[1][0][1];
                temp2 = self.face[1][0][2];
                
                self.face[1][0][0] = self.face[4][0][2];
                self.face[1][0][1] = self.face[4][1][2];
                self.face[1][0][2] = self.face[4][2][2];

                self.face[4][0][2] = self.face[3][2][2];
                self.face[4][1][2] = self.face[3][2][1];
                self.face[4][2][2] = self.face[3][2][0];

                self.face[3][2][2] = self.face[5][2][0];
                self.face[3][2][1] = self.face[5][1][0];
                self.face[3][2][0] = self.face[5][0][0];

                self.face[5][2][0] = temp0;
                self.face[5][1][0] = temp1;
                self.face[5][0][0] = temp2;

            elif(amount == -1): #COUNTER-CLOCKWISE
                temp0 = self.face[1][0][0];
                temp1 = self.face[1][0][1];
                temp2 = self.face[1][0][2];

                self.face[1][0][0] = self.face[5][2][0];
                self.face[1][0][1] = self.face[5][1][0];
                self.face[1][0][2] = self.face[5][0][0];

                self.face[5][2][0] = self.face[3][2][2];
                self.face[5][1][0] = self.face[3][2][1];
                self.face[5][0][0] = self.face[3][2][0];

                self.face[3][2][2] = self.face[4][0][2];
                self.face[3][2][1] = self.face[4][1][2];
                self.face[3][2][0] = self.face[4][2][2];

                self.face[4][0][2] = temp0;
                self.face[4][1][2] = temp1;
                self.face[4][2][2] = temp2;

        elif(color == 1): #ORANGE
            if(amount == 1): #CLOCKWISE
                temp0 = self.face[2][0][0];
                temp1 = self.face[2][0][1];
                temp2 = self.face[2][0][2];

                self.face[2][0][0] = self.face[4][2][2];
                self.face[2][0][1] = self.face[4][2][1];
                self.face[2][0][2] = self.face[4][2][0];

                self.face[4][2][2] = self.face[0][2][2];
                self.face[4][2][1] = self.face[0][2][1];
                self.face[4][2][0] = self.face[0][2][0];

                self.face[0][2][2] = self.face[5][2][2];
                self.face[0][2][1] = self.face[5][2][1];
                self.face[0][2][0] = self.face[5][2][0];

                self.face[5][2][2] = temp0;
                self.face[5][2][1] = temp1;
                self.face[5][2][0] = temp2;

            elif(amount == -1): #COUNTER-CLOCKWISE
                temp0 = self.face[2][0][0];
                temp1 = self.face[2][0][1];
                temp2 = self.face[2][0][2];

                self.face[2][0][0] = self.face[5][2][2];
                self.face[2][0][1] = self.face[5][2][1];
                self.face[2][0][2] = self.face[5][2][0];

                self.face[5][2][2] = self.face[0][2][2];
                self.face[5][2][1] = self.face[0][2][1];
                self.face[5][2][0] = self.face[0][2][0];

                self.face[0][2][2] = self.face[4][2][2];
                self.face[0][2][1] = self.face[4][2][1];
                self.face[0][2][0] = self.face[4][2][0];

                self.face[4][2][2] = temp0;
                self.face[4][2][1] = temp1;
                self.face[4][2][0] = temp2;

        elif(color == 2): #YELLOW
            if(amount == 1): #CLOCKWISE
                temp0 = self.face[3][0][0];
                temp1 = self.face[3][0][1];
                temp2 = self.face[3][0][2];

                self.face[3][0][0] = self.face[4][2][0];
                self.face[3][0][1] = self.face[4][1][0];
                self.face[3][0][2] = self.face[4][0][0];

                self.face[4][2][0] = self.face[1][2][2];
                self.face[4][1][0] = self.face[1][2][1];
                self.face[4][0][0] = self.face[1][2][0];

                self.face[1][2][2] = self.face[5][0][2];
                self.face[1][2][1] = self.face[5][1][2];
                self.face[1][2][0] = self.face[5][2][2];

                self.face[5][0][2] = temp0;
                self.face[5][1][2] = temp1;
                self.face[5][2][2] = temp2;

            elif(amount == -1): #COUNTER-CLOCKWISE
                temp0 = self.face[3][0][0];
                temp1 = self.face[3][0][1];
                temp2 = self.face[3][0][2];

                self.face[3][0][0] = self.face[5][0][2];
                self.face[3][0][1] = self.face[5][1][2];
                self.face[3][0][2] = self.face[5][2][2];

                self.face[5][0][2] = self.face[1][2][2];
                self.face[5][1][2] = self.face[1][2][1];
                self.face[5][2][2] = self.face[1][2][0];

                self.face[1][2][2] = self.face[4][2][0];
                self.face[1][2][1] = self.face[4][1][0];
                self.face[1][2][0] = self.face[4][0][0];

                self.face[4][2][0] = temp0;
                self.face[4][1][0] = temp1;
                self.face[4][0][0] = temp2;

        elif(color == 3): #RED
            if(amount == 1): #CLOCKWISE
                temp0 = self.face[0][0][0];
                temp1 = self.face[0][0][1];
                temp2 = self.face[0][0][2];

                self.face[0][0][0] = self.face[4][0][0];
                self.face[0][0][1] = self.face[4][0][1];
                self.face[0][0][2] = self.face[4][0][2];

                self.face[4][0][0] = self.face[2][2][2];
                self.face[4][0][1] = self.face[2][2][1];
                self.face[4][0][2] = self.face[2][2][0];

                self.face[2][2][2] = self.face[5][0][0];
                self.face[2][2][1] = self.face[5][0][1];
                self.face[2][2][0] = self.face[5][0][2];

                self.face[5][0][0] = temp0;
                self.face[5][0][1] = temp1;
                self.face[5][0][2] = temp2;

            elif(amount == -1): #COUNTER-CLOCKWISE
                temp0 = self.face[0][0][0];
                temp1 = self.face[0][0][1];
                temp2 = self.face[0][0][2];

                self.face[0][0][0] = self.face[5][0][0];
                self.face[0][0][1] = self.face[5][0][1];
                self.face[0][0][2] = self.face[5][0][2];

                self.face[5][0][0] = self.face[2][2][2];
                self.face[5][0][1] = self.face[2][2][1];
                self.face[5][0][2] = self.face[2][2][0];

                self.face[2][2][2] = self.face[4][0][0];
                self.face[2][2][1] = self.face[4][0][1];
                self.face[2][2][0] = self.face[4][0][2];

                self.face[4][0][0] = temp0;
                self.face[4][0][1] = temp1;
                self.face[4][0][2] = temp2;            

        elif(color == 4): #GREEN
            if(amount == 1): #CLOCKWISE
                temp0 = self.face[0][0][0];
                temp1 = self.face[0][1][0];
                temp2 = self.face[0][2][0];

                self.face[0][0][0] = self.face[1][0][0];
                self.face[0][1][0] = self.face[1][1][0];
                self.face[0][2][0] = self.face[1][2][0];

                self.face[1][0][0] = self.face[2][0][0];
                self.face[1][1][0] = self.face[2][1][0];
                self.face[1][2][0] = self.face[2][2][0];

                self.face[2][0][0] = self.face[3][0][0];
                self.face[2][1][0] = self.face[3][1][0];
                self.face[2][2][0] = self.face[3][2][0];

                self.face[3][0][0] = temp0;
                self.face[3][1][0] = temp1;
                self.face[3][2][0] = temp2;

            elif(amount == -1): #COUNTER-CLOCKWISE
                temp0 = self.face[0][0][0];
                temp1 = self.face[0][1][0];
                temp2 = self.face[0][2][0];

                self.face[0][0][0] = self.face[3][0][0];
                self.face[0][1][0] = self.face[3][1][0];
                self.face[0][2][0] = self.face[3][2][0];

                self.face[3][0][0] = self.face[2][0][0];
                self.face[3][1][0] = self.face[2][1][0];
                self.face[3][2][0] = self.face[2][2][0];

                self.face[2][0][0] = self.face[1][0][0];
                self.face[2][1][0] = self.face[1][1][0];
                self.face[2][2][0] = self.face[1][2][0];

                self.face[1][0][0] = temp0;
                self.face[1][1][0] = temp1;
                self.face[1][2][0] = temp2;

        elif(color == 5): #BLUE
            if(amount == 1): #CLOCKWISE
                temp0 = self.face[0][0][2];
                temp1 = self.face[0][1][2];
                temp2 = self.face[0][2][2];

                self.face[0][0][2] = self.face[3][0][2];
                self.face[0][1][2] = self.face[3][1][2];
                self.face[0][2][2] = self.face[3][2][2];

                self.face[3][0][2] = self.face[2][0][2];
                self.face[3][1][2] = self.face[2][1][2];
                self.face[3][2][2] = self.face[2][2][2];

                self.face[2][0][2] = self.face[1][0][2];
                self.face[2][1][2] = self.face[1][1][2];
                self.face[2][2][2] = self.face[1][2][2];

                self.face[1][0][2] = temp0;
                self.face[1][1][2] = temp1;
                self.face[1][2][2] = temp2;

            elif(amount == -1): #COUNTER-CLOCKWISE
                temp0 = self.face[0][0][2];
                temp1 = self.face[0][1][2];
                temp2 = self.face[0][2][2];

                self.face[0][0][2] = self.face[1][0][2];
                self.face[0][1][2] = self.face[1][1][2];
                self.face[0][2][2] = self.face[1][2][2];

                self.face[1][0][2] = self.face[2][0][2];
                self.face[1][1][2] = self.face[2][1][2];
                self.face[1][2][2] = self.face[2][2][2];

                self.face[2][0][2] = self.face[3][0][2];
                self.face[2][1][2] = self.face[3][1][2];
                self.face[2][2][2] = self.face[3][2][2];

                self.face[3][0][2] = temp0;
                self.face[3][1][2] = temp1;
                self.face[3][2][2] = temp2;

    def print_cube(self):
        print("Printing cube...")
        print("      {} {} {}".format(self.face[4][0][0], self.face[4][1][0], self.face[4][2][0]))
        print("      {} {} {}".format(self.face[4][0][1], self.face[4][1][1], self.face[4][2][1]))
        print("      {} {} {}".format(self.face[4][0][2], self.face[4][1][2], self.face[4][2][2]))
        print("{} {} {} {} {} {} {} {} {} {} {} {}".format(self.face[3][0][0], self.face[3][1][0], self.face[3][2][0],
                                                           self.face[0][0][0], self.face[0][1][0], self.face[0][2][0],
                                                           self.face[1][0][0], self.face[1][1][0], self.face[1][2][0],
                                                           self.face[2][0][0], self.face[2][1][0], self.face[2][2][0]))
        print("{} {} {} {} {} {} {} {} {} {} {} {}".format(self.face[3][0][1], self.face[3][1][1], self.face[3][2][1],
                                                           self.face[0][0][1], self.face[0][1][1], self.face[0][2][1],
                                                           self.face[1][0][1], self.face[1][1][1], self.face[1][2][1],
                                                           self.face[2][0][1], self.face[2][1][1], self.face[2][2][1]))
        print("{} {} {} {} {} {} {} {} {} {} {} {}".format(self.face[3][0][2], self.face[3][1][2], self.face[3][2][2],
                                                           self.face[0][0][2], self.face[0][1][2], self.face[0][2][2],
                                                           self.face[1][0][2], self.face[1][1][2], self.face[1][2][2],
                                                           self.face[2][0][2], self.face[2][1][2], self.face[2][2][2]))
        print("      {} {} {}".format(self.face[5][0][0], self.face[5][1][0], self.face[5][2][0]))
        print("      {} {} {}".format(self.face[5][0][1], self.face[5][1][1], self.face[5][2][1]))
        print("      {} {} {}".format(self.face[5][0][2], self.face[5][1][2], self.face[5][2][2]))