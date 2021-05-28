from create_program import create_program
from pathlib import Path
from subprocess import check_output
import networkx as nx
import re
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

programs_folder_path = Path("./bee/data")
graphs_folder_path = Path("./graphs")
bee_results_folder_path = Path("./bee_results")
graphs_result_folder_path = Path("./result_graphs")

def solve_program(program_filename,graph_filename,bee_result_filename):
    ''' Creates program from given graph and solves it'''
    bee_folder_path = "./bee/BumbleBEE.exe"
    # Create folders if doesnt exist
    
    programs_folder_path.mkdir(parents=True,exist_ok=True)
    graphs_folder_path.mkdir(parents=True,exist_ok=True)
    bee_results_folder_path.mkdir(parents=True,exist_ok=True)

    program_path = programs_folder_path / program_filename
    graph_path = graphs_folder_path / graph_filename
    bee_result_path = bee_results_folder_path / bee_result_filename

    create_program(graph_path,program_path)

    result = check_output([bee_folder_path,str(program_path)])
    with open(bee_result_path,'wb') as file:
        file.write(result)
    return result.decode('utf-8')

def make_graph(program_filename,graph_filename,bee_result_filename,graph_result_filename) -> int:
    ''' Solving program from given graph_filename and creates labaled graph '''
    graphs_result_folder_path.mkdir(parents=True,exist_ok=True)
    graph_result_path = graphs_result_folder_path / graph_result_filename

    raw_program = solve_program(program_filename,graph_filename,bee_result_filename)
    raw_program = raw_program.splitlines()[7:-2]

    nodes = []
    edges = []
    nodes_labels = {}
    edge_labels = {}

    reg = re.compile(r"x[0-9]+")
    for line in raw_program:
        splited = line.split('=')
        # It is node
        if splited[0].count('x') == 1:
            connection = reg.findall(splited[0])
            nodes.append(connection[0])
            nodes_labels[connection[0]] = int(splited[1])
        # It is node
        elif splited[0].count('x') == 2:
            connection = reg.findall(splited[0])
            edges.append(connection)
            edge_labels[(connection[0],connection[1])] = int(splited[1])


    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    pos = nx.spring_layout(G)
    plt.figure()    
    colors = list(mcolors.BASE_COLORS)[1:-2]
    colors_map = [colors[nodes_labels[node]%len(colors)] for node in nodes_labels]

    nx.draw(G,pos,edge_color='black',width=1,linewidths=1,\
    node_size=500,node_color=colors_map,alpha=0.9)
    nx.draw_networkx_labels(G, pos, nodes_labels, font_size=16)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color='red')
    plt.axis("off")
    plt.savefig(graph_result_path,format="PNG")
    return len(edges)
