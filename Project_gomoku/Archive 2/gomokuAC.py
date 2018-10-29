import numpy as np
import random
import time
import sys
import queue as Q
import copy
searchSize = 4 # number of subnodes investigated at each step
depth = 6 # search depth
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
toChar = {
    1:"a",
    -1:"b",
    0:"c"
}
aKeys = ["aaaaa","caaaac","caaaab","baaaac","caaac"]
bKeys = ["bbbbb","cbbbbc","cbbbba","abbbbc","cbbbc"]
aScoreDict = {
    "aaaaa":1000000000000,
    "caaaac":3000000000,
    "caaac":1000000,
    "caaaab":1000000,
    "baaaac":1000000
}
bScoreDict = {
    "bbbbb":1000000000000,
    "cbbbbc":3000000000,
    "cbbbc":1000000,
    "cbbbba":1000000,
    "abbbbc":1000000
}
# a: white
# b: black
# c: blank
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
        (COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK):1000000000000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):3000000000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_WHITE):41000000,
        (COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK):41000000,
        (COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_BLACK):41000000,
        (COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_BLACK):41000000,
        (COLOR_WHITE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):41000000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_NONE):1000000,
        (COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):1000000,
        (COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK):1000000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE):100000,
        (COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):100000,
        (COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_NONE):1500,
        (COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_NONE):10,
        (COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_NONE,COLOR_NONE):10
    }
    point_COLOR_WHITE = {
        (COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE):1000000000000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):3000000000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_BLACK):41000000,
        (COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE):41000000,
        (COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE):41000000,
        (COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE):41000000,
        (COLOR_BLACK,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):41000000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_NONE):1000000,
        (COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):1000000,
        (COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE):1000000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE):100000,
        (COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):100000,
        (COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_NONE):1500,
        (COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_NONE):1000,
        (COLOR_NONE,COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_NONE):10,
        (COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_NONE,COLOR_NONE):10
    }
    point_danger_COLOR_BLACK = {
        (COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK):900000000000,
        # (COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_NONE):2100000000,
        # (COLOR_NONE,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK):2100000000,
        (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE):2100000000
    }
    point_danger_COLOR_WHITE = {
        (COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE):900000000000,
        # (COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_NONE):2100000000,
        # (COLOR_NONE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE):2100000000,
        (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE):2100000000
    }
    #class gobang:
    def if33white(self,str):
        x1 = 0
        if(str == ((COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE))):
            x1= 1
        if(str == ((COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE))):
            x1= 1
        if(str == (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE)):
            x1= 1
        if(str == (COLOR_WHITE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_NONE)):
            x1= 1
        if(str == (COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE)):
            x1= 1
        if(str==(COLOR_NONE,COLOR_WHITE,COLOR_NONE,COLOR_WHITE,COLOR_WHITE)):
            x1= 1
        if(str == ((COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_NONE))):
            x1= 10
        if(str == (COLOR_NONE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE,COLOR_WHITE)):
            x1= 10
        # x1= 0
        # if(x1 > 0):
            # #print("33, str:", str)
        return x1
    def if33black(self,str):
        x1 = 0
        if(str == ((COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE))):
            x1= 1
        if(str == ((COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK))):
            x1= 1
        if(str == (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_BLACK)):
            x1= 1
        if(str == (COLOR_BLACK,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_NONE)):
            x1= 1
        if(str == (COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_NONE)):
            x1= 1
        if(str==(COLOR_NONE,COLOR_BLACK,COLOR_NONE,COLOR_BLACK,COLOR_BLACK)):
            x1= 1
        if(str == ((COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_NONE))):
            x1= 10
        if(str == (COLOR_NONE,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK,COLOR_BLACK)):
            x1= 10
        return x1
    def genSet(self,cb,color):
        SearchSet =[]
        board = copy.deepcopy(cb)
        for i in range(0,self.chessboard_size):
            for j in range(0,self.chessboard_size):
                if(board[i][j]==0):
                    board[i][j]=COLOR_NONE
                if(board[i][j]==COLOR_BLACK) or (board[i][j]==COLOR_WHITE):
                    if(i-1>=0) and (board[i-1][j]!=COLOR_BLACK)and (board[i-1][j]!=COLOR_WHITE):
                        board[i-1][j]=3
                    if(j-1>=0) and (board[i][j-1]!=COLOR_BLACK)and (board[i][j-1]!=COLOR_WHITE):
                        board[i][j-1]=3
                    if(i+1<=self.chessboard_size-1) and (board[i+1][j]!=COLOR_BLACK)and (board[i+1][j]!=COLOR_WHITE):
                        board[i+1][j]=3
                    if(j+1<=self.chessboard_size-1) and (board[i][j+1]!=COLOR_BLACK)and (board[i][j+1]!=COLOR_WHITE):
                        board[i][j+1]=3
                    if(j+1<=self.chessboard_size-1) and (i+1<=self.chessboard_size-1) and (board[i+1][j+1]!=COLOR_BLACK)and (board[i+1][j+1]!=COLOR_WHITE):
                        board[i+1][j+1]=3
                    if(j+1<=self.chessboard_size-1) and (i-1>=0)and (board[i-1][j+1]!=COLOR_BLACK)and (board[i-1][j+1]!=COLOR_WHITE):
                        board[i-1][j+1]=3
                    if(j-1>=0) and (i+1<=self.chessboard_size-1)and (board[i+1][j-1]!=COLOR_BLACK)and (board[i+1][j-1]!=COLOR_WHITE):
                        board[i+1][j-1]=3
                    if(j-1>=0)and (i-1>=0) and (board[i-1][j-1]!=COLOR_BLACK)and (board[i-1][j-1]!=COLOR_WHITE):
                        board[i-1][j-1]=3
        for i in range(0,self.chessboard_size):
            for j in range(0,self.chessboard_size):
                if board[i][j]==3:
                    SearchSet.append(tuple([i,j,self.getValue(cb,[i,j],color)])) 
                    board[i][j] = COLOR_NONE
        if (len(SearchSet) > searchSize):
            SearchSet.sort(key=lambda x:x[2],reverse = True)
            SearchSet = SearchSet[0:searchSize]
        return SearchSet
    def getStr(self,cb2,pos):
        row = pos[0]
        col=pos[1]
        # cb2[row][col] = color
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
        # cb2[row][col] = COLOR_NONE
        return horizontal,vertical,s1,s2
    def getScore(self,horizontal,vertical,s1,s2,color):
        total = 0
        length = max(0,max(len(horizontal),len(vertical),len(s1),len(s2))-5) + 1
        n33 = 0
        val33 = 0
        count = 0
        c1=0
        c2=0
        c3=0
        c4=0
        if(color == COLOR_BLACK):
            for i in range(length):
                if i+5<=len(horizontal):
                    if(tuple(horizontal[i:i+5]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(horizontal[i:i+5]))
                    val33=self.if33black(tuple(horizontal[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c1=1
                        # #print("call hori", tuple(horizontal[i:i+5]))
                if i+6<=len(horizontal):
                    if(tuple(horizontal[i:i+6]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(horizontal[i:i+6]))
                if i+5<=len(vertical):
                    if(tuple(vertical[i:i+5]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(vertical[i:i+5]))
                    val33=self.if33black(tuple(vertical[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c2=1
                        # #print("call vert ", tuple(vertical[i:i+5]))
                if i+6<=len(vertical):
                    if(tuple(vertical[i:i+6]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(vertical[i:i+6]))
                if i+5<=len(s1):
                    if(tuple(s1[i:i+5]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(s1[i:i+5]))
                    val33=self.if33black(tuple(s1[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c3=1
                if i+6<=len(s1):
                    if(tuple(s1[i:i+6]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(s1[i:i+6]))
                if i+5<=len(s2):
                    if(tuple(s2[i:i+5]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(s2[i:i+5]))
                    val33=self.if33black(tuple(s2[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c4=1
                if i+6<=len(s2):
                    if(tuple(s2[i:i+6]) in self.point_COLOR_BLACK.keys()):
                        total = total + self.point_COLOR_BLACK.get(tuple(s2[i:i+6]))      
        else:
            for i in range(length):
                if i+5<=len(horizontal):
                    if(tuple(horizontal[i:i+5]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(horizontal[i:i+5]))
                    val33=self.if33black(tuple(horizontal[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c1=1
                        # #print("call hori", tuple(horizontal[i:i+5]))
                if i+6<=len(horizontal):
                    if(tuple(horizontal[i:i+6]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(horizontal[i:i+6]))
                if i+5<=len(vertical):
                    if(tuple(vertical[i:i+5]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(vertical[i:i+5]))
                    val33=self.if33black(tuple(vertical[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c2=1
                        # #print("call vert ", tuple(vertical[i:i+5]))
                if i+6<=len(vertical):
                    if(tuple(vertical[i:i+6]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(vertical[i:i+6]))
                if i+5<=len(s1):
                    if(tuple(s1[i:i+5]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(s1[i:i+5]))
                    val33=self.if33black(tuple(s1[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c3=1
                if i+6<=len(s1):
                    if(tuple(s1[i:i+6]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(s1[i:i+6]))
                if i+5<=len(s2):
                    if(tuple(s2[i:i+5]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(s2[i:i+5]))
                    val33=self.if33black(tuple(s2[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c4=1
                if i+6<=len(s2):
                    if(tuple(s2[i:i+6]) in self.point_COLOR_WHITE.keys()):
                        total = total + self.point_COLOR_WHITE.get(tuple(s2[i:i+6]))      
        count = c1+c2+c3+c4
        # #print("Point calculationg ends. n33:",n33)
        # #print("score 33 count:",count)
        if(count > 1):
            if(n33 > 10):
                # #print("33 big")
                total = total + 2000000000
            else:
                # #print("33 normal")
                total = total + 300000000
        return total
    def getScoreAC(self, cb,color):
        cbx = copy.deepcopy(cb)
        strs = []
        strs = self.genStr(cbx)
        aScore = 0
        bScore = 0
        aAC = acmation()
        bAC = acmation()
        # add keys for "a"
        for x in aKeys:
            aAC.insert(x)
        aAC.ac_automation()
        for x in bKeys:
            bAC.insert(x)
        bAC.ac_automation()
        for strings in strs:
            for string in strings:
                
                da = aAC.runkmp(string)
                db = bAC.runkmp(string)
                # #print ("AC finish")                               #打印
                if(len(da.keys()) != 0):
                    # #print(string)
                    # #print(da)
                    for i in da.keys():
                        # #print(aKeys[i-1],da[i])
                        aScore += aScoreDict[aKeys[i - 1]]
                if(len(db.keys()) != 0):
                    # #print(string)
                    # #print(db)
                    for i in db.keys():
                        # #print(bKeys[i-1],db[i])
                        bScore += bScoreDict[bKeys[i - 1]]
        score = 0
        if(self.color == COLOR_WHITE):
            score = aScore - bScore
        if(self.color == COLOR_BLACK):
            score = bScore - aScore
        return score
    def getDanger(self,horizontal,vertical,s1,s2,color):
        
        total = 0
        length = max(0,max(len(horizontal),len(vertical),len(s1),len(s2))-5) + 1
        n33 = 0
        count = 0
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
        if(color == COLOR_BLACK):
            for i in range(length):
                if i+5<=len(horizontal):
                    if(tuple(horizontal[i:i+5]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(horizontal[i:i+5]))
                    val33=self.if33white(tuple(horizontal[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c1=1
                        # #print("call hori", tuple(horizontal[i:i+5]))
                if i+6<=len(horizontal):
                    if(tuple(horizontal[i:i+6]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(horizontal[i:i+6]))
                if i+5<=len(vertical):
                    if(tuple(vertical[i:i+5]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(vertical[i:i+5]))
                    val33=self.if33white(tuple(vertical[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c2=1
                        # #print("call vert ", tuple(vertical[i:i+5]))
                if i+6<=len(vertical):
                    if(tuple(vertical[i:i+6]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(vertical[i:i+6]))
                if i+5<=len(s1):
                    if(tuple(s1[i:i+5]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(s1[i:i+5]))
                    val33=self.if33white(tuple(s1[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c3=1
                if i+6<=len(s1):
                    if(tuple(s1[i:i+6]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(s1[i:i+6]))
                if i+5<=len(s2):
                    if(tuple(s2[i:i+5]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(s2[i:i+5]))
                    val33=self.if33white(tuple(s2[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c4=1
                if i+6<=len(s2):
                    if(tuple(s2[i:i+6]) in self.point_danger_COLOR_WHITE.keys()):
                        total = total + self.point_danger_COLOR_WHITE.get(tuple(s2[i:i+6]))            
        else:
            for i in range(length):
                if i+5<=len(horizontal):
                    if(tuple(horizontal[i:i+5]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(horizontal[i:i+5]))
                    val33=self.if33black(tuple(horizontal[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c1=1
                        # #print("call hori", tuple(horizontal[i:i+5]))
                if i+6<=len(horizontal):
                    if(tuple(horizontal[i:i+6]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(horizontal[i:i+6]))
                if i+5<=len(vertical):
                    if(tuple(vertical[i:i+5]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(vertical[i:i+5]))
                    val33=self.if33black(tuple(vertical[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c2=1
                        # #print("call vert ", tuple(vertical[i:i+5]))
                if i+6<=len(vertical):
                    if(tuple(vertical[i:i+6]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(vertical[i:i+6]))
                if i+5<=len(s1):
                    if(tuple(s1[i:i+5]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(s1[i:i+5]))
                    val33=self.if33black(tuple(s1[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c3=1
                if i+6<=len(s1):
                    if(tuple(s1[i:i+6]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(s1[i:i+6]))
                if i+5<=len(s2):
                    if(tuple(s2[i:i+5]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(s2[i:i+5]))
                    val33=self.if33black(tuple(s2[i:i+5]))
                    n33=n33+val33
                    if(val33>0):
                        c4=1
                if i+6<=len(s2):
                    if(tuple(s2[i:i+6]) in self.point_danger_COLOR_BLACK.keys()):
                        total = total + self.point_danger_COLOR_BLACK.get(tuple(s2[i:i+6]))      
        count = c1+c2+c3+c4
        # #print("Danger calculationg ends. n33:",n33)
        # #print("danger 33 count:",count)
        if(count > 1):
            if(n33 > 10):
                # #print("33 big")
                total = total + 2000000000
            else:
                # #print("33 normal")
                total = total + 300000000
        
        return total 
    def getValue(self,cb2,pos,color):
        score = 0
        cb2[pos[0]][[pos[1]]] = color
        horizontal, vertical, s1, s2 = self.getStr(cb2,pos)
        score = self.getScore(horizontal,vertical,s1,s2,color)
        cb2[pos[0]][[pos[1]]] = self.otherColor(color)
        horizontal, vertical, s1, s2 = self.getStr(cb2,pos)
        score = score +self.getDanger(horizontal,vertical,s1,s2,color)
        cb2[pos[0]][pos[1]] = COLOR_NONE
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
                        #print ("%3s"%'.',end=""),
                    elif ch == COLOR_BLACK:
                        self.console(COLOR_BLACK)
                        #print ("%3s"%'O',end=""),
                        #self.console(-1)
                    elif ch == COLOR_WHITE:
                        self.console(13)
                        #print ("%3s"%'X',end=""),
                    elif ch == 3:
                        self.console(9)
                        #print ("%3s"%'$',end=""),
                    
                self.console(-1)
                #print()
            #print()
            return 0
    def minimax(self,chessboard,depth):
        solutions = []
        alpha = float("inf")
        beta = float("-inf")
        best = float("-inf")
        searchSet = self.genSet(chessboard,self.color)
        for posE in searchSet:
            # #print(searchSet)
            pos = [posE[0],posE[1]]
            #print(pos)
            cb = copy.deepcopy(chessboard)
            cb[pos[0]][pos[1]] = self.color
            score = self.minP(cb,depth-1,alpha,beta)
            if(score == best):
                solutions.append(pos)
            if(score > best):
                best = score
                solutions = []
                solutions.append(pos)
        return solutions
    def maxP(self,cb,depth,alpha,beta):
        value = self.getScoreAC(cb,self.color)
        if (depth == 0 or value >=900000000000 ): 
            return value
        cboard = copy.deepcopy(cb)
        searchSet = self.genSet(cboard,self.color)
        best = float("-inf")
        for posE in searchSet: 
            pos = [posE[0],posE[1]]
            subBoard = copy.deepcopy(cboard)
            subBoard[pos[0],pos[1]] = self.color
            score = self.minP(subBoard, depth-1,alpha,max(best,beta))
            if(best < score):
                best = score
            if(score > alpha):
                break
        return best
    def minP(self,cb,depth,alpha,beta):
        value = self.getScoreAC(cb,self.color)
        if (depth == 0 or value >=900000000000 ): 
            return value
        else:
            cboard = copy.deepcopy(cb)
            searchSet = self.genSet(cboard,self.otherColor(self.color))
            best =float("inf")
            for posE in searchSet: # maximize player
                pos = [posE[0],posE[1]]
                subBoard = copy.deepcopy(cboard)
                subBoard[pos[0],pos[1]] = self.otherColor(self.color)
                # #print("call max, "pos[0],",",pos[1])
                score = self.maxP(subBoard, depth-1,min(best,alpha),beta)
                if(best > score):
                    best = score
                if(score < beta):
                    break
            return best
    def genStr(self,cbx): 
        strs = []
        cb = copy.deepcopy(cbx)
        verticalStrs = []
        horizontalStrs = []  
        s1Strs = []# ///
        s2Strs = []# \\\
        l = len(cb)
        for i in range(l):
            s = ""
            for j in range(l):
                s = s + toChar[cb[i][j]]
            horizontalStrs.append(s)
        for j in range(l):
            s = ""
            for i in range(l):
                s = s + toChar[cb[i][j]]
            verticalStrs.append(s)
        for i in range(l):
            s = ""
            for j in range(l - i):
                s = s+toChar[cb[i+j][j]]
            s1Strs.append(s)
        for j in range(1,l):
            s = ""
            for i in range(l - j):
                s = s + toChar[cb[i][j+i]]
            s1Strs.append(s)
        for i in range(l):
            s = ""
            for j in range(i + 1):
                s = s+toChar[cb[i - j][j]]
            s2Strs.append(s)
        for j in range(1,l):
            s = ""
            for i in range(l - j):
                s = s + toChar[cb[l-1-i][j + i]]
            s2Strs.append(s)
        strs.append(tuple(verticalStrs))
        strs.append(tuple(horizontalStrs))
        strs.append(tuple(s1Strs))
        strs.append(tuple(s2Strs))
        return strs

    def go(self, chessboard):
        self.candidate_list.clear()
        #==================================================================
        #Write your algorithm here
        #Here is the simplest sample:Random decision
        searchSet = self.genSet(chessboard,self.color)
        if len(searchSet) == 0:
            size =len(chessboard)
            new_pos=tuple([int(size/2),int(size/2)])
        else:
            candidate=self.minimax(chessboard,depth)
            best=candidate[0]
            new_pos=tuple(best)
        #==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        #If not, return error.
        assert chessboard[new_pos[0],new_pos[1]]== COLOR_NONE
        #Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)

# node for AC automata
class node:  
    def __init__(self,ch):  
        self.ch = ch            #结点值  
        self.fail = None        #Fail指针  
        self.tail = 0           #尾标志：标志为 i 表示第 i 个模式串串尾  
        self.child = []         #子结点  
        self.childvalue = []    #子结点的值  

# AC automata copied from https://www.ctolib.com/topics-106266.html. Used for pattern maching in evaluation of the whole board
class acmation:           
    def __init__(self):                   
        self.root = node("")                      #初始化根结点  
        self.count = 0                            #模式串个数  
          
    #第一步：模式串建树  
    def insert(self,strkey):       
        self.count += 1                             #插入模式串，模式串数量加一  
        p = self.root  
        for i in strkey:  
            if i not in p.childvalue:               #若字符不存在，添加子结点  
                child = node(i)  
                p.child.append(child)  
                p.childvalue.append(i)  
                p = child  
            else :                                  #否则，转到子结点  
                p = p.child[p.childvalue.index(i)]  
        p.tail = self.count                         #修改尾标志  
          
    #第二步：修改Fail指针  
    def ac_automation(self):                                                  
        queuelist = [self.root]                     #用列表代替队列  
        while len(queuelist):                       #BFS遍历字典树  
            temp = queuelist[0]  
            queuelist.remove(temp)                  #取出队首元素  
            for i in temp.child:  
                if temp == self.root:               #根的子结点Fail指向根自己  
                    i.fail = self.root  
                else:  
                    p = temp.fail                   #转到Fail指针  
                    while p:                          
                        if i.ch in p.childvalue:    #若结点值在该结点的子结点中，则将Fail指向该结点的对应子结点  
                            i.fail = p.child[p.childvalue.index(i.ch)]  
                            break  
                        p = p.fail                  #否则，转到Fail指针继续回溯  
                    if not p:                       #若p==None，表示当前结点值在之前都没出现过，则其Fail指向根结点  
                        i.fail = self.root  
                queuelist.append(i)                 #将当前结点的所有子结点加到队列中  
                
    #第三步：模式匹配  
    def runkmp(self,strmode):
        p = self.root  
        cnt = {}                                    #使用字典记录成功匹配的状态                               
        for i in strmode:           #遍历目标串
            while i not in p.childvalue and p is not self.root:  
                p = p.fail  
            if i in p.childvalue:                   #若找到匹配成功的字符结点，则指向那个结点，否则指向根结点  
                p = p.child[p.childvalue.index(i)]  
            else :                                    
                p = self.root  
            temp = p  
            while temp is not self.root:              
                if temp.tail:                    #尾标志为0不处理           
                    if temp.tail not in cnt:  
                        cnt.setdefault(temp.tail)  
                        cnt[temp.tail] = 1  
                    else:  
                        cnt[temp.tail] += 1  
                temp = temp.fail
        return cnt                                  #返回匹配状态   
