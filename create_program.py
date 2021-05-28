import json
import time
import re

def get_edges(graph):
    """ Function that returns distinct list of edges names"""
    edges = []
    for vertex in graph.keys():
        for edge in graph[vertex]:
            if edge not in edges:
                edges.append(edge)
    return edges

def count_time(func):
    def inner(filename):
        t = time.time()
        func(filename)
        print(time.time() - t)
    return inner
        

def create_program(graph_filename,result_filename):
    """ Function that reads graph from graph.json """
    with open(graph_filename) as file:
        graph = json.load(file)
    edges = get_edges(graph)
    q = len(edges)
    vertexes = graph.keys() 
    program = ""
    for vertex in vertexes:
        program += f"new_int({vertex},{0},{q})\n"

    program += "\n"

    reg = re.compile(r"x[0-9]+")
    for i,edge in enumerate(edges):
        splited = reg.findall(edge)
        program += f"new_int({edge},{1},{q+1})\n"
        program += f"new_int(t{i},0,{2*q})\n"
        program += f"int_plus({splited[0]},{splited[1]},t{i})\n"
        program += f"int_mod(t{i},{q+1},{edge})\n"
        program += "\n"

    program += "int_array_allDiff(["
    for cleaned in edges:
        program += f"{cleaned},"
    program = program[:-1]
    program += "])\n"
    program += "solve satisfy"

    with open(result_filename,"w") as file:
        file.write(program)

