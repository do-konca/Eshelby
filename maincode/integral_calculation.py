import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import rock_parametrs
from datetime import datetime

# TODO:  2. Сделать скрипт для тестов по нескольким json. 1. Научиться считать 36 компонент вместо 81.(возможно даже 21) 
# 4. еще раз посмотерть срезы 

class integral():
    def __init__(self, data_json):
        """создает оси с лимитами, параметры в json"""
        self.rock_parametrs = rock_parametrs.rock( data_json["a1"], # параметр горной породы уже заложен внутри интеграла
                                                   data_json["a2"], 
                                                   data_json["a3"], 
                                                   data_json["k"], 
                                                   data_json["mu"])
        self.limits = {}
        self.limits["tetta"] = []

        self.limits["phi"] = []
        for i in range(len(data_json["limits_tetta"])):
            self.limits["tetta"].append((data_json["limits_tetta"][i][0], 
                                         data_json["limits_tetta"][i][1], 
                                         data_json["limits_tetta"][i][2]))
        for i in range(len(data_json["limits_phi"])):
            self.limits["phi"].append((data_json["limits_phi"][i][0], 
                                       data_json["limits_phi"][i][1], 
                                       data_json["limits_phi"][i][2]))
        self.points = {}
    
    def __str__(self):
        rename_tetta = "Tetta Start Stop Step\n"
        rename_phi = "Phi Start Stop Step\n"
        for i in range(len(self.limits["tetta"])):
            rename_tetta += f"{i + 1}.\t{ self.limits['tetta'][i][0] }\t{self.limits['tetta'][i][1]}\t{self.limits['tetta'][i][2]}\n"
        for i in range(len(self.limits["phi"])):
            rename_phi += f"{i + 1}.\t{ self.limits['phi'][i][0] }\t{self.limits['phi'][i][1]}\t{self.limits['phi'][i][2]}\n"
        return str(self.rock_parametrs) +"\n"+ rename_tetta+rename_phi


    def get_axes(self):
        """ params: line_x это [(-np.pi/2, np.pi/, 0.001),(...)], где
            в каждом кортеже лежит начало конец и шаг по участку(граничные точки включаются 1 раз)
            return: возвращает сетку в которой нужно посчитать значения
            ____________________________________________________________
            записывает в поля grid_x1 и grid_x2 посчитанные точки для сетки
            """
        x = [np.array([self.limits["phi"][0][0]])]
        for part in self.limits["phi"]:
            data = np.arange(part[0]+part[2], part[1]+part[2], part[2])
            x.append(data)
        
        y = [np.array([self.limits["tetta"][0][0]])]
        for part in self.limits["tetta"]:
            data = np.arange(part[0]+part[2], part[1]+part[2], part[2])
            y.append(data)
        
        self.grid_x1 = np.concatenate( x, axis=0 )
        self.grid_x2 = np.concatenate( y, axis=0 )
        
    
    def get_array(self, func,  args = []):
        """
        Возвращает рассчитанные значения сетки
        """
        self.res = np.zeros((self.grid_x1.shape[0], self.grid_x2.shape[0]))
        for ix, x in enumerate(self.grid_x1):
            for iy, y in enumerate(self.grid_x2):
                self.res[ix][iy] = func(y, x, *args)
               

    def integral_square(self):
        """Расчет интеграла"""
        integ = 0
        self.res_abs = np.abs(self.res)
        for x in range(self.res.shape[0]-1):
            for y in range(self.res.shape[1]-1):
                mean = (self.res_abs[x][y] + self.res_abs[x+1][y] + self.res_abs[x][y+1] + self.res_abs[x+1][y+1])/4
                step_x = self.grid_x1[x+1] - self.grid_x1[x]
                step_y = self.grid_x2[y+1] - self.grid_x2[y]
                integ +=  mean*(step_x * step_y)
        return integ

    def get_3D_data(self, func, args = []):
        """
        calculate data in grid
        """
        self.points["phi"], self.points["tetta"] = integral.get_axes(self.limits["phi"], self.limits["tetta"])

        self.grid_x1, self.grid_x2 = np.meshgrid( self.points["phi"], self.points["tetta"])
        self.res = np.zeros((self.limits["tetta"][2], self.limits["phi"][2] ))

        for x1 in range(self.limits["phi"][2]):
            for x2 in range(self.limits["tetta"][2]):
                self.res[x2, x1] = func(self.points["tetta"][x2], self.points["phi"][x1],  *args)

    def get_2D_data(self, func, direction = "phi", const_point = 0, args = [], change_limits_data = []):
        self.direction = direction
        self.points[direction] = np.linspace(self.limits[self.direction][0], self.limits[self.direction][1], self.limits[self.direction][2])
        self.const_point = const_point
        self.x = np.linspace(self.limits[self.direction][0], self.limits[self.direction][1], self.limits[self.direction][2])
        self.res = np.zeros(self.limits[self.direction][2])
        if not change_limits_data:
            for i in range(self.limits[direction][2]):
                if self.direction == "phi":
                    self.res[i] = func(const_point, self.points["phi"][i], *args)
                elif self.direction == "tetta":
                    self.res[i] = func(self.points["tetta"][i], const_point, *args)
        else:
            self.x = np.linspace(*change_limits_data)
            self.res = np.zeros(self.x.shape[0])
            for i in range(self.x.shape[0]):
                if self.direction == "phi":
                    self.res[i] = func(const_point, self.x[i], *args)
                elif self.direction == "tetta":
                    self.res[i] = func(self.x[i], const_point, *args)
    
    def plot_2D_data(self, **kwargs):
        fig, ax = plt.subplots()
        self.res[np.abs(self.res) < 10**-12] = 'nan'
        ax.plot(self.x, self.res)
        ax.set_title(f"k = {kwargs['k']}, m = {kwargs['m']}, l = {kwargs['l']}, n = {kwargs['n']}, {self.direction}, const = {self.const_point}")
        ax.set_xlabel(self.direction)
        ax.set_ylabel("component value")
        plt.show()

    def save_2D_data(self, **kwargs):
        """save 2D data images"""
        fig, ax = plt.subplots()
        self.res[np.abs(self.res) < 10**-12] = 'nan'
        ax.plot(self.x, self.res)
        ax.set_title(f"k = {kwargs['k']}, m = {kwargs['m']}, l = {kwargs['l']}, n = {kwargs['n']}, {self.direction}, const = {self.const_point}")
        ax.set_xlabel(self.direction)
        ax.set_ylabel("component value")
        plt.savefig(f"test//k = {kwargs['k']}, m = {kwargs['m']}, l = {kwargs['l']}, n = {kwargs['n']}//k = {kwargs['k']}, m = {kwargs['m']}, l = {kwargs['l']}, n = {kwargs['n']}, phi = {self.const_point}, left1000points.png")

    def plot_3D_data(self, **kwargs):
        # ПРОИСХОДИТ ТРАНСПОНИРОВАНИЕ РЕЗУЛЬТАТА ДЛЯ ОТОБРАЖЕНИЯ 
        """plot 3d data"""
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
        self.grid_x1, self.grid_x2 = np.meshgrid(self.grid_x1, self.grid_x2)
        ax.plot_surface(self.grid_x1, self.grid_x2, self.res.T, cmap=cm.coolwarm)
        ax.set_title(f"k = {kwargs['k']}, m = {kwargs['m']}, l = {kwargs['l']}, n = {kwargs['n']}")
        ax.set_xlabel("phi")
        ax.set_ylabel("tetta")
        plt.show()
    
    def save_3D_data(self, **kwargs):
        """save 3d data images"""
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
        ax.plot_surface(self.grid_x1, self.grid_x2,self.res, cmap=cm.coolwarm)
        ax.set_title(f"k = {kwargs['k']}, m = {kwargs['m']}, l = {kwargs['l']}, n = {kwargs['n']}")
        ax.set_xlabel("phi")
        ax.set_ylabel("tetta")

        plt.savefig(f"test//k = {kwargs['k']}, m = {kwargs['m']}, l = {kwargs['l']}, n = {kwargs['n']}//k = {kwargs['k']}, m = {kwargs['m']}, l = {kwargs['l']}, n = {kwargs['n']}grid100x100.png")
    
    
