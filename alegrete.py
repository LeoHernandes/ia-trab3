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


def step_gradient(theta_0: float, theta_1: float, data: np.array, alpha: float):
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
    

def fit(data: np.array, theta_0: float, theta_1: float, alpha: float, num_iterations: int):
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
    theta_0_list = []
    theta_1_list = []
    theta_0_list.append(theta_0)
    theta_1_list.append(theta_1)
    
    for i in range(num_iterations):
        theta_0, theta_1 = step_gradient(theta_0, theta_1, data, alpha)
        theta_0_list.append(theta_0)
        theta_1_list.append(theta_1)

    return theta_0_list, theta_1_list


def standardize_data(data: np.array):
    """
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: a matriz data normalizada
    """
    data[:, 0] = (data[:, 0] - data[:, 0].mean())/data[:, 0].std()
    data[:, 1] = (data[:, 1] - data[:, 1].mean())/data[:, 1].std()

    return data


def unstandardize_data(prediction: np.array, data: np.array):
    """
    :param prediction: np.array - a matriz de predição do modelo
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: a predição com os valores reais (não normalizados)
    """
    return prediction * data[:, 1].std() + data[:, 1].mean()


if __name__ == '__main__':
    quiz_data = standardize_data(np.genfromtxt('alegrete.csv', delimiter=','))
    theta_0s, theta_1s = fit(quiz_data, theta_0=0, theta_1=0, alpha=0.01, num_iterations=150)
    print(compute_mse(theta_0s[-1], theta_1s[-1], quiz_data))