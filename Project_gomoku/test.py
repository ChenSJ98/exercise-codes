import numpy as np
import sys
import queue as Q
import time

black = 10
white = -10
null = 0
def otherColor(color):
    if color == black:
        return white
    else:
        return black
point_black = {
    (black,black,black,black,black):10000000,
    (null,black,black,black,black,null):10000,
    (null,black,black,black,black):1000,
    (black,null,black,black,black):1000,
    (black,black,null,black,black):1000,
    (black,black,black,null,black):1000,
    (black,black,black,black,null):1000,
    (null,null,black,black,black,null):1000,
    (null,black,black,black,null,null):1000,
    (null,black,black,null,black,null):1000,
    (null,black,null,black,black,null):1000,
    (null,null,black,black,null,null):100,
    (null,null,black,null,black,null):100,
    (null,black,null,black,null,null):100,
    (null,null,null,black,null,null):10,
    (null,null,black,null,null,null):10
}
point_white = {
    (white,white,white,white,white):10000000,
    (null,white,white,white,white,null):10000,
    (null,white,white,white,white):1000,
    (white,null,white,white,white):1000,
    (white,white,null,white,white):1000,
    (white,white,white,null,white):1000,
    (white,white,white,white,null):1000,
    (null,null,white,white,white,null):1000,
    (null,white,white,null,white,null):1000,
    (null,white,null,white,white,null):1000,
    (null,null,white,white,null,null):100,
    (null,null,white,null,white,null):100,
    (null,white,null,white,null,null):100,
    (null,null,null,white,null,null):10,
    (null,null,white,null,null,null):10
}
danger_black = {
    (null,black,black,black,black,null):1000000,
    (null,black,black,black,black,white):1000000,
    (white,black,black,black,black,null):1000000
}
danger_white = {
    (null,white,white,white,white,null):1000000,
    (null,white,white,white,white,black):1000000,
    (white,white,white,white,null,black):1000000
}
#class gobang:
def console (color):
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
def show (board):
        for row in range(lRow):
            for col in range(lCol):
                ch = board[row][col]
                if ch == null: 
                    console(-1)
                    print ("%3s"%'.',end=""),
                elif ch == black:
                    console(black)
                    print ("%3s"%'O',end=""),
                    #console(-1)
                elif ch == white:
                    console(13)
                    print ("%3s"%'X',end=""),
                elif ch == 3:
                    console(9)
                    print ("%3s"%'$',end=""),
                
            console(-1)
            print()
        print()
        return 0

def genSet(board):
    SearchSet =[]
    for i in range(0,15):
        for j in range(0,15):
            if(board[i][j]==0):
                board[i][j]=null
            if(board[i][j]==black) or (board[i][j]==white):
                if(i-1>=0) and (board[i-1][j]!=black)and (board[i-1][j]!=white):
                    board[i-1][j]=3
                    # SearchSet.append([i-1,j])
                if(j-1>=0) and (board[i][j-1]!=black)and (board[i][j-1]!=white):
                    board[i][j-1]=3
                    # SearchSet.append([i,j-1])
                if(i+1<=lRow-1) and (board[i+1][j]!=black)and (board[i+1][j]!=white):
                    board[i+1][j]=3
                    # SearchSet.append([i+1,j])
                if(j+1<=lCol-1) and (board[i][j+1]!=black)and (board[i][j+1]!=white):
                    board[i][j+1]=3
                    # SearchSet.append([i,j+1])
                if(j+1<=lCol-1) and (i+1<=lRow-1) and (board[i+1][j+1]!=black)and (board[i+1][j+1]!=white):
                    board[i+1][j+1]=3
                    # SearchSet.append([i+1,j+1])
                if(j+1<=lCol-1) and (i-1>=0)and (board[i-1][j+1]!=black)and (board[i-1][j+1]!=white):
                    board[i-1][j+1]=3
                    # SearchSet.append([i-1,j+1])
                if(j-1>=0) and (i+1<=lRow-1)and (board[i+1][j-1]!=black)and (board[i+1][j-1]!=white):
                    board[i+1][j-1]=3
                    # SearchSet.append([i+1,j-1])
                if(j-1>=0)and (i-1>=0) and (board[i-1][j-1]!=black)and (board[i-1][j-1]!=white):
                    board[i-1][j-1]=3
                    # SearchSet.append([i-1,j-1])
    for i in range(0,15):
        for j in range(0,15):
            if board[i][j]==3:
                SearchSet.append([i,j]) 
    return SearchSet
def getStr(cb2,pos,color):
    row = pos[0]
    col=pos[1]
    cb2[row][col] = color
    rMin = max(row-4,0)
    rMax = min(row+4,lRow-1)
    cMin = max(col-4,0)
    cMax = min(col+4,lCol-1)
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
    cb2[row][col] = null
    return horizontal,vertical,s1,s2
def getScore(horizontal,vertical,s1,s2,color):
    length = max(0,max(len(horizontal),len(vertical),len(s1),len(s2))-5)
    total = 0
    if(color == black):
        for i in range(length):
            if i+5<=len(horizontal):
                if(tuple(horizontal[i:i+5]) in point_black.keys()):
                    total = total + point_black.get(tuple(horizontal[i:i+5]))
            if i+6<=len(horizontal):
                if(tuple(horizontal[i:i+6]) in point_black.keys()):
                    total = total + point_black.get(tuple(horizontal[i:i+6]))
            if i+5<=len(vertical):
                if(tuple(vertical[i:i+5]) in point_black.keys()):
                    total = total + point_black.get(tuple(vertical[i:i+5]))
            if i+6<=len(vertical):
                if(tuple(vertical[i:i+6]) in point_black.keys()):
                    total = total + point_black.get(tuple(vertical[i:i+6]))
            if i+5<=len(s1):
                if(tuple(s1[i:i+5]) in point_black.keys()):
                    total = total + point_black.get(tuple(s1[i:i+5]))
            if i+6<=len(s1):
                if(tuple(s1[i:i+6]) in point_black.keys()):
                    total = total + point_black.get(tuple(s1[i:i+6]))
            if i+5<=len(s2):
                if(tuple(s2[i:i+5]) in point_black.keys()):
                    total = total + point_black.get(tuple(s2[i:i+5]))
            if i+6<=len(s2):
                if(tuple(s2[i:i+6]) in point_black.keys()):
                    total = total + point_black.get(tuple(s2[i:i+6]))     
    elif(color == white):
        for i in range(length):
            if i+5<=len(horizontal):
                if(tuple(horizontal[i:i+5]) in point_white.keys()):
                    total = total + point_white.get(tuple(horizontal[i:i+5]))
            if i+6<=len(horizontal):
                if(tuple(horizontal[i:i+6]) in point_white.keys()):
                    total = total + point_white.get(tuple(horizontal[i:i+6]))
            if i+5<=len(vertical):
                if(tuple(vertical[i:i+5]) in point_white.keys()):
                    total = total + point_white.get(tuple(vertical[i:i+5]))
            if i+6<=len(vertical):
                if(tuple(vertical[i:i+6]) in point_white.keys()):
                    total = total + point_white.get(tuple(vertical[i:i+6]))
            if i+5<=len(s1):
                if(tuple(s1[i:i+5]) in point_white.keys()):
                    total = total + point_white.get(tuple(s1[i:i+5]))
            if i+6<=len(s1):
                if(tuple(s1[i:i+6]) in point_white.keys()):
                    total = total + point_white.get(tuple(s1[i:i+6]))
            if i+5<=len(s2):
                if(tuple(s2[i:i+5]) in point_white.keys()):
                    total = total + point_white.get(tuple(s2[i:i+5]))
            if i+6<=len(s2):
                if(tuple(s2[i:i+6]) in point_white.keys()):
                    total = total + point_white.get(tuple(s2[i:i+6]))
    return total
def getDanger(horizontal,vertical,s1,s2,color):
    total = 0
    length = max(0,max(len(horizontal),len(vertical),len(s1),len(s2))-5)
    if(color == black):
        for i in range(length):
            if i+5<=len(horizontal):
                if(tuple(horizontal[i:i+5]) in danger_white.keys()):
                    total = total + danger_white.get(tuple(horizontal[i:i+5]))
            if i+6<=len(horizontal):
                if(tuple(horizontal[i:i+6]) in danger_white.keys()):
                    total = total + danger_white.get(tuple(horizontal[i:i+6]))
            if i+5<=len(vertical):
                if(tuple(vertical[i:i+5]) in danger_white.keys()):
                    total = total + danger_white.get(tuple(vertical[i:i+5]))
            if i+6<=len(vertical):
                if(tuple(vertical[i:i+6]) in danger_white.keys()):
                    total = total + danger_white.get(tuple(vertical[i:i+6]))
            if i+5<=len(s1):
                if(tuple(s1[i:i+5]) in danger_white.keys()):
                    total = total + danger_white.get(tuple(s1[i:i+5]))
            if i+6<=len(s1):
                if(tuple(s1[i:i+6]) in danger_white.keys()):
                    total = total + danger_white.get(tuple(s1[i:i+6]))
            if i+5<=len(s2):
                if(tuple(s2[i:i+5]) in danger_white.keys()):
                    total = total + danger_white.get(tuple(s2[i:i+5]))
            if i+6<=len(s2):
                if(tuple(s2[i:i+6]) in danger_white.keys()):
                    total = total + danger_white.get(tuple(s2[i:i+6]))
            
    else:
        for i in range(length):
            if i+5<=len(horizontal):
                if(tuple(horizontal[i:i+5]) in danger_black.keys()):
                    total = total + danger_black.get(tuple(horizontal[i:i+5]))
            if i+6<=len(horizontal):
                if(tuple(horizontal[i:i+6]) in danger_black.keys()):
                    total = total + danger_black.get(tuple(horizontal[i:i+6]))
            if i+5<=len(vertical):
                if(tuple(vertical[i:i+5]) in danger_black.keys()):
                    total = total + danger_black.get(tuple(vertical[i:i+5]))
            if i+6<=len(vertical):
                if(tuple(vertical[i:i+6]) in danger_black.keys()):
                    total = total + danger_black.get(tuple(vertical[i:i+6]))
            if i+5<=len(s1):
                if(tuple(s1[i:i+5]) in danger_black.keys()):
                    total = total + danger_black.get(tuple(s1[i:i+5]))
            if i+6<=len(s1):
                if(tuple(s1[i:i+6]) in danger_black.keys()):
                    total = total + danger_black.get(tuple(s1[i:i+6]))
            if i+5<=len(s2):
                if(tuple(s2[i:i+5]) in danger_black.keys()):
                    total = total + danger_black.get(tuple(s2[i:i+5]))
            if i+6<=len(s2):
                if(tuple(s2[i:i+6]) in danger_black.keys()):
                    total = total + danger_black.get(tuple(s2[i:i+6]))
    return total
def getValue(cb2,pos,color):
    # print(pos[0],",",pos[1])
    # print(point)
    # print((0,0,10,10,10,0)in point.keys())s
    total = 0
    score = 0
    danger = 0
    horizontal, vertical, s1, s2 = getStr(cb2,pos,color)
    score = getScore(horizontal,vertical,s1,s2,color)
    horizontal, vertical, s1, s2 = getStr(cb2,pos,otherColor(color))
    danger = getDanger(horizontal,vertical,s1,s2,color)
    total = score + danger
    return total
def h(cbx,searchSet,color):
    candidates = Q.PriorityQueue()
    for pos in searchSet:
        score = getValue(cbx,pos,color)
        candidates.put([-score,pos])
    return candidates.get(0)

def minimax(cbx,searchSet,color,depth,maxPlayer):
    if depth==0 or len(searchSet) == 1:
        return h(cbx,searchSet,color)
    if (maxPlayer == True):
        value = -1000000000
        for pos in searchSet:
            cbx[pos[0]][pos[1]] =color
            value = max(value, minimax(cbx,genSet(cbx),color,depth-1,False))
    return
   
#initiate chessboard
lRow = 15
lCol = 15
cb=(np.zeros((lRow,lCol),dtype=np.int))
i = 0
while i < 20:
    x=np.random.random_integers(lRow-1)
    y=np.random.random_integers(lCol-1)
    if cb[x][y] == null:
        cb[x][y]=black
        i=i+1
i = 0
while i < 20:
    x=np.random.random_integers(lRow-1)
    y=np.random.random_integers(lCol-1)
    if cb[x][y] == null:
        cb[x][y]=white
        i = i+1
color = white
if (color == white):
    print("color: X")

cbx=tuple(cb)
show(cbx)

searchSet = genSet(cbx)
danger = 0
candidates=Q.PriorityQueue()
start = time.time()
print("size: ", len(searchSet))

#evaluate search set
candidate=h(cbx,searchSet,color)


best=candidate
print(best)
print(getStr(cbx,best[1],color))

#show best solution
pos = best[1]
cb[pos[0],pos[1]]=3
show(cbx)

run_time = (time.time() - start)
print("runtime:  ", run_time)