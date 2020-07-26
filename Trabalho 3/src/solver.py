# Universidade Federal de São Carlos – UFSCar
# Departamento de Computação
# Introdução a Otimização Combinatória Aplicada – Trabalho 3
# Prof. Dr. Mário César San Felice
# Aluno: João Victor Mendes Freire
# RA: 758943

from ortools.sat.python import cp_model
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

    if node_count >= 1000:
        return ColoringGreedy(node_count, edge_count, nodes)

    return ColoringILP(node_count, edge_count, edges)

def ColoringILP(node_count, edge_count, edges):
    colors = [-1 for i in range(node_count)]
    color_count = 0
    max_colors = node_count

    # Início do modelo
    m = cp_model.CpModel()

    # Variáveis indicadoras
    # Número de cores utilizadas
    y = []
    for k in range(max_colors):
        y.append(m.NewIntVar(0, 1, f'y[{k}]'))

    # Qual vértice foi colorido com qual cor
    x = [[] for i in range(node_count)]
    for i in range(node_count):
        for k in range(max_colors):
            x[i].append(m.NewIntVar(0, 1, f'x[{i},{k}]'))

    # Restrições
    # Apenas uma cor pode ser atribuída a cada vértice
    for i in range(node_count):
        m.Add(sum(x[i][k] for k in range(max_colors)) == 1)
    
    # Um vértice só pode ter uma cor atribuída caso ela seja utilizada
    for i, j in edges:
        for k in range(max_colors):
            m.Add(x[i][k]+x[j][k] <= y[k])

    # Restrição extra para remover simetria no espaço de busca
    for k in range(max_colors-1):
        m.Add(y[k] >= y[k+1])

    # Objetivo: minimizar o somatório das core utilizadas
    m.Minimize(sum(y[k] for k in range(max_colors)))
    
    solver = cp_model.CpSolver()
    status = solver.Solve(m)

    color_count = int(solver.ObjectiveValue())

    for i in range(node_count):
        for k in range(max_colors):
            if int(solver.Value(x[i][k])) == 1:
                colors[i] = k

    # prepare the solution in the specified output format
    output_data = str(color_count) + '\n'
    output_data += ' '.join(map(str, colors))

    return output_data

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
