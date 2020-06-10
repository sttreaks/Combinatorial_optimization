#!/bin/python3

import os
import sys


bucket = {}
Nodes = {}


def to_bin(num: int) -> str:
    return str(bin(num))[2:]


def descend(parent, node, indx):
        total = 1

        for edge in node:
            if parent is not None and (edge == parent or indx == parent):
                continue

            target = Nodes[edge]

            if bucket.get((edge, indx), -1) != -1:
                bucket[(edge, indx)] = descend(indx, target, edge)
            else:
                bucket[(indx, edge)] = descend(indx, target, edge)

            if bucket.get((edge, indx), -1) != -1:
                total += bucket[(edge, indx)]
            else:
                total += bucket[(indx, edge)]

        return total


def roadsInHackerland(n, roads):
    roads_ = [[-1 for _ in range(n)] for __ in range(n)]

    for road in roads:
        roads_[road[0] - 1][road[1] - 1] = 2 ** road[2]
        roads_[road[1] - 1][road[0] - 1] = 2 ** road[2]

    dp = {}
    for i in range(0, n):
        dp[i] = [None, None]
    dp[0] = 0

    v = 0
    q = [i for i in range(1, n)]

    while len(q) > 0:
        for vertex in range(0, n):
            if roads_[v][vertex] != -1:
                if vertex in q and (dp[vertex][0] is None or dp[vertex][0] > roads_[v][vertex]):
                    dp[vertex][0] = roads_[v][vertex]
                    dp[vertex][1] = v

        v = q[0]
        q = q[1:]

    for i in range(n):
        Nodes[i] = []

    for i in dp.keys():
        if dp[i] != 0:
            bucket[(dp[i][1], i)] =  0
            Nodes[i].append(dp[i][1])
            Nodes[dp[i][1]].append(i)

    descend(None, Nodes[list(bucket.keys())[0][0]], list(bucket.keys())[0][0])

    print(bucket)

    ans = 0
    for i in bucket.keys():
        ans += bucket[i] * (n - bucket[i]) * roads_[i[0]][i[1]]

    print(ans)

    return to_bin(ans)


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nm = input().split()

    n = int(nm[0])

    m = int(nm[1])

    roads = []

    for _ in range(m):
        roads.append(list(map(int, input().rstrip().split())))

    result = roadsInHackerland(n, roads)

    # fptr.write(result + '\n')
    #
    # fptr.close()

