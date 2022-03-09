import numpy as np
import json
import integral_calculation
from datetime import datetime
import lymbda

class Experiment():
    def __init__(self, path_start_json):
        with open(path_start_json, "r") as read_file:
            start_data = json.load(read_file)
        with open("global_test_info.json", "r") as gl:
            test_number_info = json.load(gl)

        self.start = datetime.now()
        self.duration = None
        self.type = start_data["type"]
        self.number = test_number_info[self.type]
        self.start_data = start_data
        self.__21component__ = {(0,0):(0,0,0,0),(0,1):(0,0,1,1),(0,2):(0,0,2,2),
                                (0,3):(0,0,1,2),(0,4):(0,0,0,2),(0,5):(0,0,0,1),
                                (1,1):(1,1,1,1),(1,2):(1,1,2,2),(1,3):(1,1,1,2),
                                (1,4):(1,1,0,2),(1,5):(1,1,0,1),(2,2):(2,2,2,2),
                                (2,3):(2,2,1,2),(2,4):(2,2,0,2),(2,5):(2,2,0,1),
                                (3,3):(1,2,1,2),(3,4):(1,2,0,2),(3,5):(1,2,0,1),
                                (4,4):(0,2,0,2),(4,5):(0,2,0,1),(5,5):(0,1,0,1)}

        test_number_info[self.type] += 1    
        with open("global_test_info.json", "w") as gl:
            gl.write(json.dumps(test_number_info, indent=4, default=str))

    # направлени того, что у всех компонент одинаковые пределы интегрирования и одинаковая сетка
    
    def run_test(self, func):
        if self.type == "one":
            integral_data = integral_calculation.integral(self.start_data)
            integral_data.get_axes()
            integral_data.get_array(func, args = [integral_data.rock_parametrs,*self.start_data["component"]])
            square = integral_data.integral_square()
            return {"square": square}
        if self.type == "all":
            result_tensor = np.zeros((6,6))
            integral_data = integral_calculation.integral(self.start_data)
            integral_data.get_axes()
            for comp6x6, comp3x3x3x3 in self.__21component__.items():
                integral_data.get_array(func, args = [integral_data.rock_parametrs,*comp3x3x3x3])
                square = integral_data.integral_square()
                result_tensor[comp6x6[0]][comp6x6[1]] = square
            
            result_tensor += result_tensor.T - np.diag(np.diag(result_tensor))
            return result_tensor
            

    def log_data(self, data_from_calculation):
        """LOG DATA AFTER COMPLITE PROGRAM"""
        if self.type == "one":
            result_json = {}
            result_json["experiment_number"] = self.number
            result_json["experiment_type"] = self.type
            result_json["start"] = self.start
            result_json["duration"] = (datetime.now() - self.start).total_seconds()
            result_json["square"] = data_from_calculation["square"]
            result_json.update(self.start_data)


            with open(f"tests_json\\{self.type}_{self.number}.json", "w") as log:
                log.write(json.dumps(result_json, indent=4, default=str))
        
        if self.type == "all":
            result_json = {}
            result_json["experiment_number"] = self.number
            result_json["experiment_type"] = self.type
            result_json["start"] = self.start
            result_json["duration"] = (datetime.now() - self.start).total_seconds()
            result_json["square"] = list(np.round(data_from_calculation,6))

            with open(f"tests_json\\{self.type}_{self.number}.json", "w") as log:
                log.write(json.dumps(result_json, indent=4, default=str))

def get_value(x, y, rock, n, m, k, l):
    
    linv = lymbda.LYAMBDA(rock.Ckmln, x, y, rock.a1, rock.a2, rock.a3)
    return  linv[k, l] * lymbda.Nmn(x, y, rock.a1, rock.a2, rock.a3, n = n, m = m)

test = Experiment("data_all_test.json")
data = test.run_test(get_value)
test.log_data(data)



