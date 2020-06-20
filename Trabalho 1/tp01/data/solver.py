    # Universidade Federal de São Carlos – UFSCar
    # Departamento de Computação
    # Introdução a Otimização Combinatória Aplicada – Trabalho 1
    # Prof. Dr. Mário César San Felice
    # Aluno: João Victor Mendes Freire
    # RA: 758943

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

DEBUG = 0

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    conflict_count = int(firstLine[2])

    items = []
    conflicts = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    for i in range(1, conflict_count+1):
        line = lines[item_count + i]
        parts = line.split()
        conflicts.append((int(parts[0]), int(parts[1])))

    return knapsackNaive(item_count, items, capacity, conflict_count, conflicts)


def knapsackNaive(num_items, items, capacity, num_conflicts, conflicts):

    if DEBUG >= 1:
        print(f"numero de itens = {num_items}")
        print(f"capacidade da mochila = {capacity}")
        print(f"numero de conflitos = {num_conflicts}")

    if DEBUG >= 2:
        print("Itens na ordem em que foram lidos")
        for item in items:
            print(item)
        print()

    if DEBUG >= 2:
        print("Conflitos na ordem em que foram lidos")
        for conflict in conflicts:
            print(conflict)
        print()

    # Modify this code to run your optimization algorithm

    solution = [0]*num_items
    solution_value = 0
    solution_weight = 0

    # item list sorted by value per weight
    items.sort(reverse=True, key=item_key)

    for item in items:
        if solution_weight + item.weight <= capacity:
            solution[item.index] = 1
            solution_value += item.value
            solution_weight += item.weight
            for conflict in conflicts:
                if item.index == conflict[0]:
                    remove_index(items, conflict[1])
                elif item.index == conflict[1]:
                    remove_index(items, conflict[0])         

    # prepare the solution in the specified output format
    output_data = str(solution_value) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

############## Custom Aux Functions

# remove the 'Item' with given index from list
def remove_index(items, index):
    for item in items:
        if item.index == index:
            items.remove(item)
            break

# returns key of given 'Item' for sorting purposes
def item_key(item):
    return item.value/item.weight

##############

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
