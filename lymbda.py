from numba import njit
import numpy as np
# пользователь должен задавть индексы как на бумажке, а не как номера в массивах

# расчет Nmn
def Nmn(tetta = 0, phi = 0, a1 = 1, a2 = 1 ,a3 = 1000, n = 0, m = 0):
    
    n_all = np.zeros(3)
    n_all[0] = np.sin(tetta) * np.cos(phi) / a1
    n_all[1] = np.sin(tetta) * np.sin(phi) / a2
    n_all[2] = np.cos(tetta) / a3
    
    return n_all[n] * n_all[m]

# расчет Lymbdaij (я вижу что лямбдаkl это тензор 3х3, а лямбда11, и или любой другой индекс, это конкретное число)
@njit
def LYAMBDAkl(Cklmn, k, l, n_all, *args):

    result = 0
    for m_i in range(3):
        for n_i in range(3):
            result += Cklmn[k,m_i,l,n_i] * n_all[n_i] * n_all[m_i]
    return result

# расчет Lymbdakl
@njit
def LYAMBDA(Cklmn, *args):
    
    result = np.zeros((3,3))

    n_0 = np.sin(args[0]) * np.cos(args[1]) / args[2]
    n_1 = np.sin(args[0]) * np.sin(args[1]) / args[3]
    n_2 = np.cos(args[0]) / args[4]
    n_all =(n_0, n_1, n_2)
    for k_i in range(3):
        for l_i in range(3):
            result[k_i, l_i] = LYAMBDAkl(Cklmn, k_i, l_i, n_all, *args)
    return np.linalg.inv(result)
