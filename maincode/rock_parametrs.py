import numpy as np


# example
# K - Isotropic rock bulk modulus/Модуль объемной упругости
K = 160 # Сталь 160 ГПа

# mu - Isotropic rock shear modulus/Модуль сдвига 
mu = 82 # сталь 82 ГПа


class rock():
    def __init__(self, a1, a2, a3 , k , mu):
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.k = k
        self.mu = mu
        self.__get_Cklmn()
    
    def __str__(self):
        return f"""Параметры пор: {self.a1, self.a2, self.a3}\nПараметры породы:\n\tОбъемный модуль упругости: {self.k}\n\tКоэффициэнт Пуассона: {self.mu}\nТензор упругости:\n{str(np.round((self.C6x6),2))}"""
        
    def from_6x6_to_3x3x3x3(data):
        result = np.zeros((3,3,3,3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for m in range(3):
                        if i == 0 and j == 0:
                            x = 0
                        elif i == 1 and j == 1:
                            x = 1
                        elif i == 2 and j == 2:
                            x = 2
                        elif (i == 1 and j == 2) or (i == 2 and j == 1):
                            x = 3
                        elif (i == 0 and j == 2) or (i == 2 and j == 0):
                            x = 4
                        elif (i == 0 and j == 1) or (i == 1 and j == 0):
                            x = 5


                        if k == 0 and m == 0:
                            y = 0
                        elif k == 1 and m == 1:
                            y = 1
                        elif k == 2 and m == 2:
                            y = 2
                        elif (k== 1 and m == 2) or (k == 2 and m == 1):
                            y = 3
                        elif (k == 0 and m == 2) or (k == 2 and m == 0):
                            y = 4
                        elif (k == 0 and m == 1) or (k == 1 and m == 0):
                            y = 5

                        result[i,j,k,m] = data[x,y]
            
        return result

    def from_3x3x3x3_to_6x6(data ,dict_components):
        result = np.zeros((6,6))

        for comp6x6, comp3x3x3x3 in dict_components.items():
            result[comp6x6] = data[comp3x3x3x3]
        result += result.T - np.diag(np.diag(result))
        return result
            

    def __get_Cklmn(self):
        lambda_ = self.k - 2 * self.mu / 3 
        c11 = lambda_ + 2 * self.mu
        c12 = lambda_
        c44 = self.mu

        self.C6x6 = np.zeros((6,6))
        self.C6x6[0,0] = c11
        self.C6x6[0,1] = c12
        self.C6x6[0,2] = c12
        self.C6x6[1,0] = c12
        self.C6x6[1,1] = c11
        self.C6x6[1,2] = c12
        self.C6x6[2,0] = c12
        self.C6x6[2,1] = c12
        self.C6x6[2,2] = c11
        self.C6x6[3,3] = c44
        self.C6x6[4,4] = c44
        self.C6x6[5,5] = c44
        self.Ckmln = np.zeros((3,3,3,3))

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for m in range(3):
                        if i == 0 and j == 0:
                            x = 0
                        elif i == 1 and j == 1:
                            x = 1
                        elif i == 2 and j == 2:
                            x = 2
                        elif (i == 1 and j == 2) or (i == 2 and j == 1):
                            x = 3
                        elif (i == 0 and j == 2) or (i == 2 and j == 0):
                            x = 4
                        elif (i == 0 and j == 1) or (i == 1 and j == 0):
                            x = 5


                        if k == 0 and m == 0:
                            y = 0
                        elif k == 1 and m == 1:
                            y = 1
                        elif k == 2 and m == 2:
                            y = 2
                        elif (k== 1 and m == 2) or (k == 2 and m == 1):
                            y = 3
                        elif (k == 0 and m == 2) or (k == 2 and m == 0):
                            y = 4
                        elif (k == 0 and m == 1) or (k == 1 and m == 0):
                            y = 5

                        self.Ckmln[i,j,k,m] = self.C6x6[x,y]
"""
    i,j,k,m - компоненты, но не связаны с компонентами k,l,m,n
    [0,0] - [0,0,0,0]
    [0,1] - [0,0,1,1]
    [0,2] - [0,0,2,2]
    [0,3] - [0,0,1,2]
    [0,4] - [0,0,0,2]
    [0,5] - [0,0,0,1]
    [1,1] - [1,1,1,1]
    [1,2] - [1,1,2,2]
    [1,3] - [1,1,1,2]
    [1,4] - [1,1,0,2]
    [1,5] - [1,1,0,1]
    [2,2] - [2,2,2,2]
    [2,3] - [2,2,1,2]
    [2,4] - [2,2,0,2]
    [2,5] - [2,2,0,1]
    [3,3] - [1,2,1,2]
    [3,4] - [1,2,0,2]
    [3,5] - [1,2,0,1]
    [4,4] - [0,2,0,2]
    [4,5] - [0,2,0,1]
    [5,5] - [0,1,0,1]
    """
    