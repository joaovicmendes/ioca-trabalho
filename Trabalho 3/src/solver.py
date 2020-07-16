# Universidade Federal de São Carlos – UFSCar
# Departamento de Computação
# Introdução a Otimização Combinatória Aplicada – Trabalho 3
# Prof. Dr. Mário César San Felice
# Aluno: João Victor Mendes Freire
# RA: 758943

from collections import deque

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

    nodes = []
    for i in range(node_count):
        nodes.append({'index': i, 'degree': 0, 'edges': []})

    for edge in edges:
        v, u = edge[0], edge[1]
        nodes[v]['edges'].append(u)
        nodes[u]['edges'].append(v)
    
    for node in nodes:
        node['degree'] = len(node['edges'])

    return ColoringGreedy(node_count, edge_count, nodes)


def ColoringGreedy(node_count, edge_count, nodes):

    color_count = 0
    colors = [-1]*node_count
    available_colors = [True]*node_count

    # Ordena por ordem de grau dos vértices
    nodes.sort(key=node_key, reverse=True)

    queue = deque(nodes)
    
    # O primeiro vétice pode ter qualquer cor
    colors[queue.popleft()['index']] = 0

    # Para os demais vétices
    while queue:
        # Verifica quais cores estão disponiveis, olhando os adjacentes
        node = queue.popleft()
        for edge in node['edges']:
            if colors[edge] != -1:
                available_colors[colors[edge]] = False
        
        # Colore com a primeira cor disponível
        for j in range(node_count):
            if available_colors[j] == True:
                colors[node['index']] = j
                break
        
        # Reseta a lista de cores disponíveis para a próxima iteração
        for j in range(node_count):
            available_colors[j] == True  

    aux = [0]*node_count
    for i in range(node_count):
        aux[colors[i]] += 1
    for i in range(node_count):
        if aux[i] > 0:
            color_count += 1

    # prepare the solution in the specified output format
    output_data = str(color_count) + '\n'
    output_data += ' '.join(map(str, colors))

    return output_data

def node_key(node):
    return node['degree']

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
