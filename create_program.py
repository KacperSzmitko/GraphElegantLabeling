from typing import Counter
import matplotlib.pyplot as plt
import networkx as nx
import json
import time

def get_edges(graph):
    edges = []
    for vertex in graph.keys():
        for edge in graph[vertex]:
            if edge['k'] not in edges:
                edges.append(edge['k'])
    return edges

def count_time(func):
    def inner(filename):
        t = time.time()
        func(filename)
        print(time.time() - t)
    return inner
        

def make_program(filename):
    with open("graph.json") as file:
        graph = json.load(file)

    q = len(graph.keys())
    vertexes = graph.keys() 
    program = ""
    for vertex in vertexes:
        program += f"new_int({vertex},{0},{q})\n"

    program += "\n"

    edges = get_edges(graph)
    cleaned_list = []
    for i,edge in enumerate(edges):
        splited = edge.split("-")
        cleaned = splited[0] + splited[1]
        program += f"new_int({cleaned},{1},{q+1})\n"
        program += f"new_int(t{i},0,{2*q})\n"
        program += f"int_plus({splited[0]},{splited[1]},t{i})\n"
        program += f"int_mod(t{i},{q+1},{cleaned})\n"
        program += "\n"
        if cleaned not in cleaned_list:
            cleaned_list.append(cleaned)

    program += "int_array_allDiff(["
    for cleaned in cleaned_list:
        program += f"{cleaned},"
    program = program[:-1]
    program += "])\n"
    program += "solve satisfy"

    with open(filename,"w") as file:
        file.write(program)

make_program("test.bee")