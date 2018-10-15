import numpy as np
import random
import time
import sys
import queue as Q
import copy
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
random.seed(0)
#don't change the class name
class AI(object):
#chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are COLOR_WHITE or COLOR_BLACK
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        # The input is current chessboard.
    def otherColor(self,color):
        if color == COLOR_BLACK:
            return COLOR_WHITE
        else:
            return COLOR_BLACK
    point_COLOR_BLACK = {
        (COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK):1000000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):200000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_WHITE):41000,
        (COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK):41000,
        (COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_BLACK):41000,
        (COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_BLACK):41000,
        (COLOR_WHITE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):41000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_NONE):100,
        (COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE):100,
        (COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_NONE):100,
        (COLOR_NONE,COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_NONE):10,
        (COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_NONE,COLOR_NONE):10
    }
    point_COLOR_WHITE = {
        (COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE):1000000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):200000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_BLACK):41000,
        (COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE):41000,
        (COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE):41000,
        (COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE):41000,
        (COLOR_BLACK,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):41000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_NONE):100,
        (COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE):100,
        (COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_NONE):100,
        (COLOR_NONE,COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_NONE):10,
        (COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_NONE,COLOR_NONE):10
    }
    point_danger_COLOR_BLACK = {
        (COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK):900000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):180000,
    }
    point_danger_COLOR_WHITE = {
        (COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE):900000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):180000,
    }
    #class gobang:
    def if33white(self,str):
        if(str == ((COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE))):
            # print("white33:")
            # print(str)
            return True
        else:
            return False
    def if33black(self,str):
        if(str == ((COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE))):
            # print("black33:")
            # print(str)
            return True
        else:
            return False
    def genSet(self,board):
        SearchSet =[]
        for i in range(0,self.chessboard_size):
            for j in range(0,self.chessboard_size):
                if(board[i][j]==0):
                    board[i][j]=COLOR_NONE
                if(board[i][j]==COLOR_BLACK) or (board[i][j]==COLOR_WHITE):
                    if(i-1>=0) and (board[i-1][j]!=COLOR_BLACK)and (board[i-1][j]!=COLOR_WHITE):
                        board[i-1][j]=3
                        # SearchSet.append([i-1,j])
                    if(j-1>=0) and (board[i][j-1]!=COLOR_BLACK)and (board[i][j-1]!=COLOR_WHITE):
                        board[i][j-1]=3
                        # SearchSet.append([i,j-1])
                    if(i+1<=self.chessboard_size-1) and (board[i+1][j]!=COLOR_BLACK)and (board[i+1][j]!=COLOR_WHITE):
                        board[i+1][j]=3
                        # SearchSet.append([i+1,j])
                    if(j+1<=self.chessboard_size-1) and (board[i][j+1]!=COLOR_BLACK)and (board[i][j+1]!=COLOR_WHITE):
                        board[i][j+1]=3
                        # SearchSet.append([i,j+1])
                    if(j+1<=self.chessboard_size-1) and (i+1<=self.chessboard_size-1) and (board[i+1][j+1]!=COLOR_BLACK)and (board[i+1][j+1]!=COLOR_WHITE):
                        board[i+1][j+1]=3
                        # SearchSet.append([i+1,j+1])
                    if(j+1<=self.chessboard_size-1) and (i-1>=0)and (board[i-1][j+1]!=COLOR_BLACK)and (board[i-1][j+1]!=COLOR_WHITE):
                        board[i-1][j+1]=3
                        # SearchSet.append([i-1,j+1])
                    if(j-1>=0) and (i+1<=self.chessboard_size-1)and (board[i+1][j-1]!=COLOR_BLACK)and (board[i+1][j-1]!=COLOR_WHITE):
                        board[i+1][j-1]=3
                        # SearchSet.append([i+1,j-1])
                    if(j-1>=0)and (i-1>=0) and (board[i-1][j-1]!=COLOR_BLACK)and (board[i-1][j-1]!=COLOR_WHITE):
                        board[i-1][j-1]=3
                        # SearchSet.append([i-1,j-1])
        for i in range(0,self.chessboard_size):
            for j in range(0,self.chessboard_size):
                if board[i][j]==3:
                    SearchSet.append([i,j]) 
                    board[i][j] = COLOR_NONE
        return SearchSet
    def getStr(self,cb2,pos,color):
        row = pos[0]
        col=pos[1]
        cb2[row][col] = color
        rMin = max(row-4,0)
        rMax = min(row+4,self.chessboard_size-1)
        cMin = max(col-4,0)
        cMax = min(col+4,self.chessboard_size-1)
        dr1 = rMax - row
        dr2 = row - rMin
        dc1 = cMax - col
        dc2 = col - cMin
        horizontal=[]
        vertical = []
        s1=[]
        s2=[]
        for i in range(dr1+dr2+1):
            vertical.append(cb2[rMin+i][col])
        for i in range(dc1+dc2+1):
            horizontal.append(cb2[row][cMin+i])
        for i in range(min(dr2,dc2)+min(dc1,dr1)+1):
            s1.append(cb2[row-min(dr2,dc2)+i][col-min(dc2,dr2)+i])
        for i in range(min(dr2,dc1)+min(dc2,dr1)+1):
            s2.append(cb2[row+min(dr1,dc2)-i][col-min(dr1,dc2)+i])
        cb2[row][col] = COLOR_NONE
        return horizontal,vertical,s1,s2
    def getScore(self,horizontal,vertical,s1,s2,color):
        total = 0
        length = max(0,max(len(horizontal),len(vertical),len(s1),len(s2))-5) + 1
        n33 = 0
        if(color == COLOR_BLACK):
            for i in range(length):
                if i+5<=len(horizontal):
                    if(tuple(horizontal[i:i+5]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(horizontal[i:i+5]))
                    if(self.if33black(tuple(horizontal[i:i+5]))):
                        n33 = n33 + 1
                        # print("call hori", tuple(horizontal[i:i+5]))
                if i+6<=len(horizontal):
                    if(tuple(horizontal[i:i+6]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(horizontal[i:i+6]))
                if i+5<=len(vertical):
                    if(tuple(vertical[i:i+5]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(vertical[i:i+5]))
                    if(self.if33black(tuple(vertical[i:i+5]))):
                        n33 = n33 + 1
                        # print("call vert ", tuple(vertical[i:i+5]))
                if i+6<=len(vertical):
                    if(tuple(vertical[i:i+6]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(vertical[i:i+6]))
                if i+5<=len(s1):
                    if(tuple(s1[i:i+5]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(s1[i:i+5]))
                    if(self.if33black(tuple(s1[i:i+5]))):
                        # print("call s1 ", tuple(s1[i:i+5]))
                        n33 = n33 + 1
                if i+6<=len(s1):
                    if(tuple(s1[i:i+6]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(s1[i:i+6]))
                if i+5<=len(s2):
                    if(tuple(s2[i:i+5]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(s2[i:i+5]))
                    if(self.if33black(tuple(s2[i:i+5]))):
                        n33 = n33 + 1
                        # print("call s2", tuple(s2[i:i+5]))
                if i+6<=len(s2):
                    if(tuple(s2[i:i+6]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(s2[i:i+6]))      
        else:
            for i in range(length):
                if i+5<=len(horizontal):
                    if(tuple(horizontal[i:i+5]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(horizontal[i:i+5]))
                    if(self.if33white(tuple(horizontal[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(horizontal):
                    if(tuple(horizontal[i:i+6]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(horizontal[i:i+6]))
                if i+5<=len(vertical):
                    if(tuple(vertical[i:i+5]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(vertical[i:i+5]))
                    if(self.if33white(tuple(vertical[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(vertical):
                    if(tuple(vertical[i:i+6]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(vertical[i:i+6]))
                if i+5<=len(s1):
                    if(tuple(s1[i:i+5]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(s1[i:i+5]))
                    if(self.if33white(tuple(s1[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(s1):
                    if(tuple(s1[i:i+6]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(s1[i:i+6]))
                if i+5<=len(s2):
                    if(tuple(s2[i:i+5]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(s2[i:i+5]))
                    if(self.if33white(tuple(s2[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(s2):
                    if(tuple(s2[i:i+6]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(s2[i:i+6]))
        if(n33 >= 2):
            total = total + 79000
        return total
    def getDanger(self,horizontal,vertical,s1,s2,color):
        total = 0
        length = max(0,max(len(horizontal),len(vertical),len(s1),len(s2))-5) + 1
        n33 = 0
        if(color == COLOR_BLACK):
            for i in range(length):
                if i+5<=len(horizontal):
                    # print("hori5:", horizontal[i:i+5])
                    if(tuple(horizontal[i:i+5]) in self.point_danger_COLOR_WHITE.keys()):
                        
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(horizontal[i:i+5]))
                    if(self.if33white(tuple(horizontal[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(horizontal):
                    if(tuple(horizontal[i:i+6]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(horizontal[i:i+6]))
                if i+5<=len(vertical):
                    if(tuple(vertical[i:i+5]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(vertical[i:i+5]))
                    if(self.if33white(tuple(vertical[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(vertical):
                    if(tuple(vertical[i:i+6]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(vertical[i:i+6]))
                if i+5<=len(s1):
                    if(tuple(s1[i:i+5]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(s1[i:i+5]))
                    if(self.if33white(tuple(s1[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(s1):
                    if(tuple(s1[i:i+6]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(s1[i:i+6]))
                if i+5<=len(s2):
                    if(tuple(s2[i:i+5]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(s2[i:i+5]))
                    if(self.if33white(tuple(s2[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(s2):
                    if(tuple(s2[i:i+6]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(s2[i:i+6]))      
        else:
            for i in range(length):
                if i+5<=len(horizontal):
                    if(tuple(horizontal[i:i+5]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(horizontal[i:i+5]))
                    if(self.if33black(tuple(horizontal[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(horizontal):
                    if(tuple(horizontal[i:i+6]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(horizontal[i:i+6]))
                if i+5<=len(vertical):
                    if(tuple(vertical[i:i+5]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(vertical[i:i+5]))
                    if(self.if33black(tuple(vertical[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(vertical):
                    if(tuple(vertical[i:i+6]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(vertical[i:i+6]))
                if i+5<=len(s1):
                    if(tuple(s1[i:i+5]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(s1[i:i+5]))
                    if(self.if33black(tuple(s1[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(s1):
                    if(tuple(s1[i:i+6]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(s1[i:i+6]))
                if i+5<=len(s2):
                    if(tuple(s2[i:i+5]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(s2[i:i+5]))
                    if(self.if33black(tuple(s2[i:i+5]))):
                        n33 = n33 + 1
                if i+6<=len(s2):
                    if(tuple(s2[i:i+6]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(s2[i:i+6]))
        if(n33 >= 2):
            total = total + 70000
        return total
    def getValue(self,cb2,pos,color):
        total = 0
        score = 0
        danger = 0
        horizontal, vertical, s1, s2 = self.getStr(cb2,pos,color)
        score = self.getScore(horizontal,vertical,s1,s2,color)
        # print(pos,'horizontal: ',horizontal,'vertical: ',vertical,"s1:: ",s1,"s2: ",s2,"score: ", score)
        horizontal, vertical, s1, s2 = self.getStr(cb2,pos,self.otherColor(color))
        danger = self.getDanger(horizontal,vertical,s1,s2,color)
        total = score + danger
        # print(pos,'horizontal: ',horizontal,'vertical: ',vertical,"s1:: ",s1,"s2: ",s2,"danger: ", danger)
        # print(pos,"value: ", score,' + ',danger,' = ',total)
        return total
    def h(self,cbx,color):
        # candidates = Q.PriorityQueue()
        score = 0
        # color = self.color
        sSet =self.genSet(cbx)
        for pos in sSet:
            score = score + self.getValue(cbx,pos,color)
            # candidates.put([-score,pos])
        # print("return h with score: ", score)
        return score
    def console (self,color):
        if sys.platform[:3] == 'win':
            try: import ctypes
            except: return 0
            kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')
            GetStdHandle = kernel32.GetStdHandle
            SetConsoleTextAttribute = kernel32.SetConsoleTextAttribute
            GetStdHandle.argtypes = [ ctypes.c_uint32 ]
            GetStdHandle.restype = ctypes.c_size_t
            SetConsoleTextAttribute.argtypes = \
                [ ctypes.c_size_t, ctypes.c_uint16 ]
            SetConsoleTextAttribute.restype = ctypes.c_long
            handle = GetStdHandle(0xfffffff5)
            if color < 0: color = 7
            result = 0
            if (color & 1): result |= 4
            if (color & 2): result |= 2
            if (color & 4): result |= 1
            if (color & 8): result |= 8
            if (color & 16): result |= 64
            if (color & 32): result |= 32
            if (color & 64): result |= 16
            if (color & 128): result |= 128
            SetConsoleTextAttribute(handle, result)
        else:
            if color >= 0:
                foreground = color & 7
                background = (color >> 4) & 7
                bold = color & 8
                sys.stdout.write(" \033[%s3%d;4%dm"%(bold \
                    and "01;" or "", foreground, background))
                sys.stdout.flush()
            else:
                sys.stdout.write(" \033[0m")
                sys.stdout.flush()
        return 0
    def show (self,board):
            for row in range(self.chessboard_size):
                for col in range(self.chessboard_size):
                    ch = board[row][col]
                    if ch == COLOR_NONE: 
                        self.console(-1)
                        print ("%3s"%'.',end=""),
                    elif ch == COLOR_BLACK:
                        self.console(COLOR_BLACK)
                        print ("%3s"%'O',end=""),
                        #self.console(-1)
                    elif ch == COLOR_WHITE:
                        self.console(13)
                        print ("%3s"%'X',end=""),
                    elif ch == 3:
                        self.console(9)
                        print ("%3s"%'$',end=""),
                    
                self.console(-1)
                print()
            print()
            return 0
    
    def minimax(self,chessboard,depth,maxPlayer,color):
        #  1 = X              -1 = O
        if(maxPlayer):
            print("call max, color:", color, "depth:",depth)
        else:
            print("call mini, color:", color, "depth:",depth)
        self.show(chessboard)
        cboard = copy.deepcopy(chessboard)
        # score = self.h(cboard,color)
        # if(score >= 900000):# winning situation
        #     return score, pos
        searchSet = self.genSet(chessboard)
        if (depth == 0 or len(searchSet) == 1): 
            print("end node")
            score = self.h(cboard,self.color)
            print("score: ",score)
            return score, searchSet[0]

            # print("ready to return")
            # return x[0],x[1]
        else:
            if(maxPlayer):
                value =float("-inf")
                solution = [0,0]
                for pos in searchSet: # maximize player
                    print("sSet size: ", len(searchSet), "loop")
                    subBoard = copy.deepcopy(cboard)
                    pointScore = self.getValue(subBoard,pos,color)
                    if(pointScore >= 900000):
                        return pointScore, pos
                    subBoard[pos[0],pos[1]] = color
                    # print("call recursively")
                    score, pos1 = self.minimax(subBoard, depth-1,False,self.otherColor(color))
                    # print("return from recursive call")
                    # score = -score
                    if(value < score):
                        value = score
                        solution = pos
                print("loop over")
                # print("solution: " + solution +"value: " + (value))
                return value, solution
            else:
                value = float("inf")
                solution = [0,0]
                for pos in searchSet: # minimize player
                    print("sSet size: ", len(searchSet), "loop")
                    subBoard = copy.deepcopy(cboard)
                    pointScore = self.getValue(subBoard,pos,color)
                    if(pointScore >= 900000):
                        return pointScore, pos
                    subBoard[pos[0],pos[1]] = color
                    score, pos1 = self.minimax(subBoard, depth-1,True,self.otherColor(color))
                    score = -score
                    if(value > score):
                        value = score
                        solution = pos
                print("loop over")
                # print("solution: " + solution +"value: " + (value))
                return value, solution
    
    
    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        #==================================================================
        #Write your algorithm here
        #Here is the simplest sample:Random decision
        print('color:',self.color)
        # print(chessboard)
        self.show(chessboard)
        searchSet = self.genSet(chessboard)
        # print(searchSet)
        if len(searchSet) == 0:
            size =len(chessboard)
            new_pos=tuple([int(size/2),int(size/2)])
        else:
            print("call minimax")
            candidate=self.minimax(chessboard,1,True,self.color)
            print("return minimax")
            best=candidate[1]
            new_pos=tuple(best)
        print("new post:",new_pos)
        # print(chessboard)
        #==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        #If not, return error.
        assert chessboard[new_pos[0],new_pos[1]]== COLOR_NONE
        #Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
        # print(self.candidate_list[-1])
