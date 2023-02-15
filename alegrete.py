import numpy as np

def compute_theta_0_derivative(theta_0: float, theta_1: float, data: np.array) -> float:
    """
    Calcula a derivada parcial relativa ao intercepto da reta (theta_0)
    :param theta_0: float - intercepto da reta
    :param theta_1: float - inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    coord_x = 0
    coord_y = 1
    
    sum = 0
    for data_point in data:
        h_theta = theta_0 + theta_1 * data_point[coord_x]
        sum += h_theta - data_point[coord_y]
    
    return (2 * sum)/len(data)

def compute_theta_1_derivative(theta_0: float, theta_1: float, data: np.array) -> float:
    """
    Calcula a derivada parcial relativa à inclinação da reta (theta_1)
    :param theta_0: float - intercepto da reta
    :param theta_1: float - inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    coord_x = 0
    coord_y = 1
    
    sum = 0
    for data_point in data:
        h_theta = theta_0 + theta_1 * data_point[coord_x]
        sum += (h_theta - data_point[coord_y]) * data_point[coord_x]
    
    return (2 * sum)/len(data)

def compute_mse(theta_0: float, theta_1: float, data: np.array) -> float:
    """
    Calcula o erro quadratico medio
    :param theta_0: float - intercepto da reta
    :param theta_1: float - inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    coord_x = 0
    coord_y = 1
    
    sum = 0
    for data_point in data:
        h_theta = theta_0 + theta_1 * data_point[coord_x]
        sum += (h_theta - data_point[coord_y]) ** 2
    
    return sum/len(data)


def step_gradient(theta_0:float, theta_1:float, data: np.array, alpha:float):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de theta_0 e theta_1.
    :param theta_0: float - intercepto da reta
    :param theta_1: float - inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de theta_0 e theta_1, respectivamente
    """
    new_theta_0 = theta_0 - alpha * compute_theta_0_derivative(theta_0, theta_1, data)
    new_theta_1 = theta_1 - alpha * compute_theta_1_derivative(theta_0, theta_1, data)
    
    return new_theta_0, new_theta_1
    

def fit(data, theta_0, theta_1, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de theta_0 e theta_1.
    Ao final, retorna duas listas, uma com os theta_0 e outra com os theta_1
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param theta_0: float - intercepto da reta
    :param theta_1: float - inclinacao da reta
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os theta_0 e outra com os theta_1 obtidos ao longo da execução
    """
    raise NotImplementedError  # substituir pelo seu codigo

if __name__ == '__main__':
    print(compute_mse(1, 1, np.array([[1, 3], [2, 4], [3, 4], [4, 2]])))