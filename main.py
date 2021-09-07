from numpy import inf
from operator import itemgetter
import queue
import time
import numpy as np
import math
import collections

def applyGravity(array, n, p):
    #print "In applyGravity function"
    noFruits = 0
    #print np.array(array)
    
    for j in range(0,n):
        noFruits = 0
        for i in range(n-1,-1, -1):
            #print i, j
            if(array[i][j] == -1):
                noFruits += 1
            else:
                array[i+noFruits][j] = array[i][j]
        
        for i in range(0, noFruits):
            array[i][j] = -1;
    #print "\n"

    #print "AFTER"
    #print np.array(array)
    return array

def hit(array, n, p, x, y):
    #print "hit", "x", x, "y", y
    value = array[x][y]
    #print "n", n, "p", p, "x", x, "y", y
    #print type(value)
    #print value
    
    #q = collections.deque()
    q = queue.Queue()
    q.put((x, y))
    child = array
    child[x][y] = -1
    #q.append((x,y))
    #print q
    
    while(not q.empty()):
        poppedPosition = q.get()
        x = poppedPosition[0]
        y = poppedPosition[1]
        #print "poppedPosition", x, y
        
        if(x > 0):
            if(child[x-1][y] == value):
                #print x-1, y
                q.put((x-1,y))
                child[x-1][y] = -1
    
        if(x < n-1):
            if(child[x+1][y] == value):
                #print x+1, y
                q.put((x+1,y))
                child[x+1][y] = -1

        if(y > 0):
            if(child[x][y-1] == value):
                #print x, y-1
                q.put((x,y-1))
                child[x][y-1] = -1
        
        if(y < n-1):
            if(child[x][y+1] == value):
                #print x, y+1
                q.put((x,y+1))
                child[x][y+1] = -1

    #print child
    return child


def generateChildren(array, n, p):
    #print array
    
    traversedArray = np.copy(array)
    
    #children = Queue.Queue()
    #children = Queue.PriorityQueue()
    children = []
    
    for i in range(0, n):
        for j in range(0, n):
            #print "\n\n", i, j
            childArray = np.copy(array)
            #print "before"
            #print childArray
            
            if(traversedArray[i][j] != -1):
                value = traversedArray[i][j]
                #print "n", n, "p", p, "x", x, "y", y
                #print type(value)
                #print value
                
                #q = collections.deque()
                q = queue.Queue()
                q.put((i, j))
                traversedArray[i][j] = -1
                childArray[i][j] = -1
                localScoreCount = 1
                #q.append((x,y))
                #print q
                
                while(not q.empty()):
                    poppedPosition = q.get()
                    x = poppedPosition[0]
                    y = poppedPosition[1]
                    #print "poppedPosition", x, y
                    
                    if(x > 0):
                        if(traversedArray[x-1][y] == value):
                            #print x-1, y
                            q.put((x-1,y))
                            traversedArray[x-1][y] = -1
                            childArray[x-1][y] = -1
                            localScoreCount += 1
                
                    if(x < n-1):
                        if(traversedArray[x+1][y] == value):
                            #print x+1, y
                            q.put((x+1,y))
                            traversedArray[x+1][y] = -1
                            childArray[x+1][y] = -1
                            localScoreCount += 1
        
                    if(y > 0):
                        if(traversedArray[x][y-1] == value):
                            #print x, y-1
                            q.put((x,y-1))
                            traversedArray[x][y-1] = -1
                            childArray[x][y-1] = -1
                            localScoreCount += 1
                
                    if(y < n-1):
                        if(traversedArray[x][y+1] == value):
                            #print x, y+1
                            q.put((x,y+1))
                            traversedArray[x][y+1] = -1
                            childArray[x][y+1] = -1
                            localScoreCount += 1
				#print "after", childArray
                #-localScoreCount**2,
                #children.put((-localScoreCount**2, childArray, i, j))
                children.append((localScoreCount**2, childArray, i, j, localScoreCount))

    #print type(children)
    #print "before"
    #print children[0]
    #print children
    #children = sorted(children, key=itemgetter(0), reverse=True)
    #children.sort(key=itemgetter(2, 3))
    children.sort(key=itemgetter(0), reverse=True)
    #print children
    #print "After"
    #print children
    return children


def minimax(array, n, p, depth, score, maximizingPlayer):
    #print "aaya", array
    
    doneFlag = True
    for arrayi in array:
        localArray = set(np.copy(arrayi))
        #print localArray
        if not (-1 in localArray and len(localArray) == 1):
            doneFlag = False
    if doneFlag == True or depth < 0:
        return score[0] - score[1]


    if(maximizingPlayer):
        #print "\nmaximizingPlayer"
        bestValue = -inf
        
        children = generateChildren(array, n, p)
        
        #while(not children.empty()):
        while(len(children) != 0):
            #childPackage = children.get()
            childPackage = children.pop()
            #print childPackage
            child = childPackage[0]
            localScore = childPackage[1]
            x = childPackage[2]
            y = childPackage[3]
            #print child, localScore, x, y
            #print array
            
            #print "score", score
            score = [score[0]+localScore, score[1]]
            #print "localScore", localScore, "score", score
            
            child = applyGravity(child, n, p)
            #print "after gravity", child
            v = minimax(child, n, p, depth-1, score, False)
            #print "v", v
            
            score = [score[0]-localScore, score[1]]
            
            if v > bestValue:
                bestValue = v
                #print bestValue
                global bestMoveX, bestMoveY
                bestMoveX = x
                bestMoveY = y
        #print bestMoveX, bestMoveY
        #bestValue = max(bestValue, v)
        #print "bestValue", bestValue
        return bestValue
    
    else:
        #print "\nminimizingPlayer"
        bestValue = inf
        
        children = generateChildren(array, n, p)
        
        #while(not children.empty()):
        while(len(children) != 0):
            #childPackage = children.get()
            childPackage = children.pop()
            child = childPackage[0]
            localScore = childPackage[1]
            x = childPackage[2]
            y = childPackage[3]
            #print child, localScore, x, y
            #print array
            
            #print "score", score
            score = [score[0], score[1]+localScore]
            #print "localScore", localScore, "score", score
            
            child = applyGravity(child, n, p)
            #print "after gravity", child
            v = minimax(child, n, p, depth-1, score, True)
            #print "v", v
            
            score = [score[0], score[1]-localScore]
            
            if v < bestValue:
                bestValue = v
                #print bestValue
                bestMoveX = x
                bestMoveY = y
        #print bestMoveX, bestMoveY
        #bestValue = min(bestValue, v)
        #print "bestValue", bestValue
        return bestValue


def alphabeta(array, n, p, depth, score, noFruits, alpha, beta, maximizingPlayer):
    global noOfNodesTraversed
    noOfNodesTraversed += 1
    #print "aaya", array
    
    if noFruits == n**2 or depth < 0:
        return score[0] - score[1]

    if(maximizingPlayer):
        #print "\nmaximizingPlayer"
        v = -inf
        
        children = generateChildren(array, n, p)
        
        #while(not children.empty()):
        #while(len(children) != 0):
        for childPackage in children:
            #print children
            #childPackage = children.get()
            #childPackage = children.pop()
            #print children
            #print childPackage
            localScore = childPackage[0]
            #localScore = 0-localScore
            child = childPackage[1]
            x = childPackage[2]
            y = childPackage[3]
            localNoFruits = childPackage[4]
            #print child, localScore, x, y
            #print child
            
            #print "score", score
            score = [score[0]+localScore, score[1]]
            #print "localScore", localScore, "score", score
            #print "score", score
            
            child = applyGravity(child, n, p)
            #print "after gravity", child
            #v = minimax(child, n, p, depth-1, score, False)
            v = max(v, alphabeta(child, n, p, depth-1, score, noFruits+localNoFruits, alpha, beta, False))
            #print "v", v
            
            score = [score[0]-localScore, score[1]]
            
            if v > alpha:
                alpha = v
                global bestMoveX, bestMoveY
                bestMoveX = x
                bestMoveY = y
            #print bestMoveX, bestMoveY
            
            if beta <= v:
                break

        #print bestMoveX, bestMoveY
        #bestValue = max(bestValue, v)
        #print "bestValue", bestValue
        return v
    
    else:
        #print "\nminimizingPlayer"
        v = inf
        
        children = generateChildren(array, n, p)
        
        #while(not children.empty()):
        for childPackage in children:
            #print children
            #childPackage = children.get()
            #childPackage = children.pop()
            #print children
            localScore = childPackage[0]
            #localScore = 0-localScore
            child = childPackage[1]
            x = childPackage[2]
            y = childPackage[3]
            localNoFruits = childPackage[4]
            #print child, localScore, x, y
            #print child
            
            #print "score", score
            score = [score[0], score[1]+localScore]
            #print "localScore", localScore, "score", score
            #print "score", score
            
            child = applyGravity(child, n, p)
            #print "after gravity", child
            #v = minimax(child, n, p, depth-1, score, True)
            v = min(v, alphabeta(child, n, p, depth-1, score, noFruits+localNoFruits, alpha, beta, True))
            #print "v", v
            
            score = [score[0], score[1]-localScore]
            
            if v < beta:
                beta = v
                bestMoveX = x
                bestMoveY = y
            #print bestMoveX, bestMoveY
            
            if v <= alpha:
                break

        #print bestMoveX, bestMoveY
        #bestValue = min(bestValue, v)
        #print "bestValue", bestValue
        return v


def depthHeuristic(array, n, p, t):
    #print "t", t
    #print t>=10
    if t == 300: #We can have first move with more depth research
        if n <= 5:
            depth = 5
        elif n <= 8:
            depth = 4
        elif n <= 11:
            depth = 3
        elif n <= 20:
            depth = 2
        else:
            depth = 1
            
    elif t >= 200:
        if n <= 5:
            depth = 5
        elif n <= 8:
            depth = 4
        elif n <= 11:
            depth = 3
        elif n <= 18:
            depth = 2
        else:
            depth = 1

    elif t >= 120:
        if n <= 5:
            depth = 5
        elif n <= 10:
            depth = 3
        elif n <= 18:
            depth = 2
        else:
            depth = 1
    
    elif t >= 10:
        if n <= 7:
            depth = 4
        elif n <= 10:
            depth = 2
        else:
            depth = 1
        
    else:
        if n <= 5:
            depth = 4
        elif n <= 10:
            depth = 2
        else:
            depth = 1
        
         
    #print "depth", depth
    return depth


def main():
    global bestMoveX, bestMoveY
    global noOfNodesTraversed
    noOfNodesTraversed = 0
    #bestMove = np.empty(0)
    noFruits = 0
    
    f = open("input.txt", 'r')
    lines = f.readlines()
    #print lines
    n = int(lines[0])
    p = int(lines[1])
    t = float(lines[2])
    #print("n", n, "p", p, "t", t)
    
    array = np.zeros((n, n))
    for (l, row) in zip(lines[3:], range(0, n)):
        #print "l", l, "row", row
        numbers = list(l)
        #print numbers
        for (col, num) in zip(range(0, n), numbers):
            #print "col", col, "num", num
            if num == "*":
                array[row][col] = -1#int(num)
                noFruits += 1
            else:
                array[row][col] = int(num)
    #print array
    f.close()

    storedArray = np.copy(array)
    
    #if 
    if t <= 5:
        children = generateChildren(array, n, p)
        #print(children)
        childPackage = children[0]
        #localScore = childPackage[0]
        #localScore = 0-localScore
        #child = childPackage[1]
        bestMoveX = childPackage[2]
        bestMoveY = childPackage[3]
    elif t <= 22 and n >= 17:
        children = generateChildren(array, n, p)
        childPackage = children[0]
        #localScore = childPackage[0]
        #localScore = 0-localScore
        #child = childPackage[1]
        bestMoveX = childPackage[2]
        bestMoveY = childPackage[3]
    else:
        depth = depthHeuristic(array, n, p, t)
        #if depth%2 != 0:
        #    depth = depth# - 1
        #print("depth", depth)
        #return
        #k = minimax(array, n, p, 4, [0, 0], True)#score: max - min
        k = alphabeta(array, n, p, depth, [0, 0], noFruits, -inf, +inf, True)#score: max - min
        #print "final result", k 
        
    
    #k = minimax(array, n, p, 4, [0, 0], True)#score: max - min
    #alphabeta(array, n, p, depth, score, alpha, beta, maximizingPlayer)
    #k = alphabeta(array, n, p, 3, [0, 0], noFruits, -inf, +inf, True)#score: max - min
    #print "final result", k
    
    f1 = open("output.txt", 'w')
    #print "bestMove"
    #print(bestMoveX, bestMoveY)
    #print(chr(65+bestMoveY) + str(bestMoveX+1))
    f1.write(chr(65+bestMoveY) + str(bestMoveX+1) + "\n")
    #print "Dicision", Max
    #array1 = [[1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    #print np.array(array1)
    #child = applyGravity(array1, n, p)
    #print np.array(child)
    
    fo = hit(storedArray, n, p, bestMoveX, bestMoveY)
    #print fo
    fo = applyGravity(fo, n, p)
    for i in range(0,n):
        for j in range(0,n):
            if(fo[i][j] == -1):
                #print '*'
                f1.write('*')
            else:
                #print int(fo[i][j])
                f1.write(str(int(fo[i][j])))
        #print
        f1.write("\n")
    f1.close()

if __name__ == "__main__":
    start = time.process_time()
    main()
    timeTaken = time.process_time()-start
    print("Total time taken:", timeTaken)
    #print "Total noOfNodesTraveresed", noOfNodesTraversed
    #print "noOfNodesTraveresed per second", noOfNodesTraversed/timeTaken
    #print "Output is ready"