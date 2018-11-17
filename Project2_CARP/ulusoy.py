# ulusoy split 
from math import inf
from itertools import product
import numpy as np
class ulusoySpliter:
    dist = []
    Capacity = 0
    depot = 0
    def __init__(self,  dist, depot, capacity):
        self.dist = dist
        self.depot = depot
        self.Capacity = capacity
    def toDirectedGraph(self, taskList, depot,dist):
        length = len(taskList)
        DG = np.full((2*length+1,2*length+1),inf)
        incoming = []
        outgoing = []
        for i in range (2*length+1):
            incoming.append([])
            outgoing.append([])
        for i in range(length):
            load = 0
            x = 2*i+1
            task = taskList[i]
            cost = dist[self.depot][task[0]] + task[3] + dist[task[1]][self.depot]
            DG[x][x+1] = cost
            incoming[x+1].append([x,x+1,cost])
            outgoing[x].append([x,x+1,cost])
            if(x > 1):
                incoming[x].append([x-1,x,0])
                outgoing[x-1].append([x-1,x,0])
            load = task[2]
            cost = dist[self.depot][task[0]] + task[3]
            j = i + 1
            while(True):
                if(j == length):
                    j -= 1
                    break
                if(load + taskList[j][2] <= self.Capacity):
                    load += taskList[j][2]
                    cost += dist[taskList[j-1][1]][taskList[j][0]] + taskList[j][3]
                    DG[x][2*j+2] = cost+dist[taskList[j][1]][self.depot]
                    incoming[2*j+2].append([x,2*j+2,DG[x][2*j+2]])
                    outgoing[x].append([x,2*j+2,DG[x][2*j+2]])
                    j += 1
                    
                else:
                    j -= 1
                    break
            cost += dist[taskList[j][1]][depot]
            DG[x][2*j+2] = cost
            incoming[2*j+2][len(incoming[2*j+2]) - 1 ] = [x,2*j+2,cost]
            outgoing[x][len(outgoing[x]) - 1]=[x,2*j+2,cost]
        return DG, incoming, outgoing
    def getPath(self, DG, incoming, outgoing):
        print("call getPath")
        print(len(DG))
        nodeCost=[0]*(len(DG)+1)
        bestPath = [[]]*(len(DG)+1)
        bestPath[1] = []
        for i in range(1,len(DG)):
            minCost = inf
            bestEdge =[]
            # find incoming edge with min cost
            if(i > 1):
                for edge in incoming[i]:
                    if(edge[2] < minCost):
                        minCost = edge[2]
                        bestEdge = edge
                if(i%2 == 0):
                    preBestPath = list(bestPath[bestEdge[0]])
                    preBestPath.append([bestEdge[0],bestEdge[1]])
                    bestPath[i] = preBestPath
                else:
                    bestPath[i] = bestPath[i-1]
            else:
                minCost = 0
            nodeCost[i] += minCost
            # release node, update outgoing edge
            for edge in outgoing[i]:
                index = incoming[edge[1]].index(edge)
                edge[2] += nodeCost[i]
                incoming[edge[1]][index] = edge
        return bestPath[len(DG)-1], nodeCost[len(DG)-1]
    def split(self,tasks):
        DG, incoming, outgoing = self.toDirectedGraph(tasks,self.depot,self.dist)
        path, score = self.getPath(DG,incoming, outgoing)
        return path, score