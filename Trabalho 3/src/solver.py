
DEBUG = 0

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    if DEBUG >= 1:
        print(f"Numero de vertices = {node_count}")
        print(f"Numero de arestas = {edge_count}")

    if DEBUG >= 2:
        print("Arestas:")
        for edge in edges:
            print(edge)
        print()

    return ColoringNaive(node_count, edge_count, edges)


def ColoringNaive(node_count, edge_count, edges):

    # Modify this code to run your optimization algorithm

    # trivial solution: every node has its own color
    solution = range(0, node_count)

    # prepare the solution in the specified output format
    output_data = str(node_count) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        output_data = solve_it(input_data)
        print(output_data)
        solution_file = open(file_location + ".sol", "w")
        solution_file.write(output_data)
        solution_file.close()
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
