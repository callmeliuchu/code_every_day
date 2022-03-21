import heapq

import numpy as np
from collections import defaultdict


class Edge:

    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def other(self,u):
        if self.u == u:
            return self.v
        elif self.v == u:
            return self.u


class Graph:

    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.n = len(vertices)
        self.faces = faces
        self.graph = defaultdict(list)
        for i, j, k in faces:
            egde1 = Edge(i, j, np.sqrt(vertices[i].T.dot(vertices[j])))
            egde2 = Edge(i, k, np.sqrt(vertices[i].T.dot(vertices[k])))
            egde3 = Edge(k, j, np.sqrt(vertices[k].T.dot(vertices[j])))
            self.graph[i].append(egde1)
            self.graph[i].append(egde2)
            self.graph[j].append(egde1)
            self.graph[j].append(egde3)
            self.graph[k].append(egde2)
            self.graph[k].append(egde3)

    def set_graph(self,edges):
        self.graph = defaultdict(list)
        for u,v,w in edges:
            edge = Edge(u,v,w)
            self.graph[u].append(edge)
            self.graph[v].append(edge)
        self.n = len(self.graph)

    def shortest_path(self,u,v):
        dist = [10000000]*self.n
        dist[u] = 0
        min_q = [[0,u]]
        path = [-1]*self.n
        while min_q:
            w,p = heapq.heappop(min_q)
            if p == v:
                break
            for edge in self.graph[p]:
                q = edge.other(p)
                if dist[q] > dist[p] + edge.w:
                    dist[q] = dist[p] + edge.w
                    path[q] = p
                    heapq.heappush(min_q,[dist[q],q])
        ans = []
        vv = v
        faces = []
        while path[vv] != -1:
            ans.append(list(self.vertices[vv]))
            faces.append([path[vv],vv])
            vv = path[vv]
        return np.array(ans),np.array(faces)
