from graph_generator import make_graph

if __name__ == "__main__":
    # Name of file to save bee program
    program_filename = "test.bee"
    # Name of file with raw graph
    graph_filename = "graph.json"
    # Name of file to save solved SAT problem
    bee_result_filename = "result.txt"
    # Name of file to save labaled graph
    graph_result_filename = "graph.png"
    make_graph(program_filename,graph_filename,bee_result_filename,graph_result_filename)