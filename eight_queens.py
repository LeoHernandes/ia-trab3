import random
import matplotlib.pyplot as plt
from tqdm import tqdm
from statistics import mean
import time


# Horario de inicio da simulação
start_timestamp = time.strftime("%Y%m%d-%H%M%S")

# Pega um dos melhores indivíduos de uma população
def get_best_of_pop(pop):
    return sorted(pop, key= lambda x : evaluate(x))[0]

# Obtém dados da fitness de uma população
def get_pop_fitness(pop):
    ind_fitness = [evaluate(i) for i in pop]
    return max(ind_fitness), mean(ind_fitness), min(ind_fitness)

def log_training():
    with open(f'logs/eight_queens/training.txt', 'a') as f:
        b_max, b_mean, b_min = get_pop_fitness(pop_history[-1])
        f.write(f'[{start_timestamp}]\n')
        f.write(f'PARAMETERS:\n')
        f.write(f'gens={generations}\nindivs={individuals}\nt_size={tournament_size}\nmut={mutation}\nelite={elitism}\n')
        f.write(f'LAST GEN: {len(pop_history)}\n')
        f.write(f'BEST: {get_best_of_pop(pop_history[-1])}\n')
        f.write(f'Fitness: MAX={b_max}; MIN={b_min}; MEAN={b_mean};\n')
        f.write('\n\n\n')    

def plot_generations():
    # Lista de listas de avaliações dos indivíduos de uma geração
    max_fit = [0]
    mean_fit = [0]
    min_fit = [0]
    for p in pop_history:
        p_max, p_mean, p_min = get_pop_fitness(p)
        max_fit.append(p_max)
        mean_fit.append(p_mean)
        min_fit.append(p_min)

    plt.xlabel('Gerações')
    plt.ylabel('Ataques')
    plt.plot(max_fit, 'g', label = 'Max. Ataques')
    plt.plot(mean_fit, 'b', label = 'Média Ataques')
    plt.plot(min_fit, 'r', label = 'Mín. Ataques')
    plt.legend()
    plt.savefig(f'logs/eight_queens/{start_timestamp}_plot.png', bbox_inches='tight')
    plt.show()









def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 10.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    count = 0
    # Só é necessário olhar numa direção
    for i, v1 in enumerate(individual):
        right_cols = individual[i+1:]
        for j, v2 in enumerate(right_cols):
            # Mesma linha ou diagonal
            if (v1 == v2) or (abs(v2 - v1) == (j + 1)):
                # print(f'Attack: {i+1}, {i+j+2}')
                count += 1
    return count

def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    # Avalia todos participantes e retorna o melhor
    return min([(evaluate(i), i) for i in participants], key= lambda i : i[0])[1]

def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    parent1[index:], parent2[index:] = parent2[index:], parent1[index:]
    return parent1, parent2


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    if random.random() < m:
        individual[random.randint(0, 7)] = random.randint(1, 8)
    
    return individual

pop_history = []

def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:int - número de indivíduos no elitismo
    :return:list - melhor individuo encontrado
    """
    # Gera indivíduos aleatórios
    population = [[random.randint(1,8) for j in range(8)] for i in range(n)]

    print('Rodando algoritmo genético...')
    for gen in tqdm(range(g)):
        # Nova população já começa com a elite
        # Embaralha-se a população de modo a mudar a ordem em que os melhores
        # indivíduos são escolhidos no sort
        random.shuffle(population)
        sorted_pop = sorted(population, key= lambda x : evaluate(x))
        elite = sorted_pop[:e]
        population = sorted_pop[e:]

        gen_pop = []

        # Gera nova população
        for i in range(n):
            # Seleciona melhores indivíduos
            o1 = tournament(random.choices(population, k=k))
            o2 = tournament(random.choices(population, k=k))
            # Crossover
            crossover(o1, o2, random.randint(1, 8))
            # Mutações
            mutate(o1, m)
            mutate(o2, m)
            # Adiciona os novos indivíduos à nova geração
            gen_pop.append(o1)
            gen_pop.append(o2)
        
        # Atualiza população
        population = gen_pop + elite

        pop_history.append(population)
        #plot_queue.put(population)

    
    # Retorna melhor indivíduo
    return get_best_of_pop(population)




if __name__ == '__main__':
    generations = 300
    individuals = 400
    tournament_size = 20
    mutation = 0.8
    elitism = 30

    try:
        best = run_ga(generations, individuals, tournament_size, mutation, elitism)
    except KeyboardInterrupt:
        print(f'Interrompendo algoritmo na geração {len(pop_history)}')
        best = get_best_of_pop(pop_history[-1])
    finally:
        log_training()
        plot_generations()

    print(f'Melhor jogada: {best} ({evaluate(best)} attacks)')
    

