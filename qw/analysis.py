import numpy as np
import matplotlib.pyplot as plt

def fitting(t: np.ndarray, consts: list, powers: list, si=None, sf=None, linewidth=None, linestyle=None):
    
    fitting_line = []
    for const, power in zip(consts, powers):
        fitting_line.append(const*t**power)
    fitting_line = np.array(fitting_line)
    
    for i, (const, power) in enumerate(zip(consts, powers)):
        plt.plot(t[si:sf], fitting_line[i,si:sf], linewidth=linewidth, linestyle=linestyle, label=f'{const}*t^{power:.2f}')
    
    return 0

def validity(counts_list: list, steps: int) -> np.ndarray:
    
    displacement_dict = {
        "000000001":0, "000000010":1, "000000100":1, 
        "000001000":9, "000010000":7, "000100000":4,
        "001000000":9, "010000000":4, "100000000":7
    }
    
    valid_counts_list = []
    
    for i in range(steps):
        valid_counts = 0
        for bit, count in counts_list[i].items():
            valid_counts += (displacement_dict.get(bit, -1) > -1) * count
        valid_counts_list.append(valid_counts)
    
    return np.array(valid_counts_list, dtype=np.float64)

def inrprod(qpu_counts_list: list, sim_counts_list: list, steps: int, shots: int=4000) -> np.ndarray:
    
    inrprod_list = []
    valid_counts = validity(qpu_counts_list, steps)
    
    for i in range(steps):
        _inrprod = 0.
        for bit, count in sim_counts_list[i].items():
            temp_sim = np.sqrt(count/shots)
            temp_qpu = np.sqrt(dict(qpu_counts_list[i].items()).get(bit, 0)/valid_counts[i])
            _inrprod += temp_sim*temp_qpu
        inrprod_list.append(_inrprod)
    
    return np.array(inrprod_list)

def transform_counts_list(counts_list):
    
    place_dict = {
        "000000001":0, "000000010":1, "000000100":2, 
        "000001000":3, "000010000":4, "000100000":5, 
        "001000000":6, "010000000":7, "100000000":8
    }
    place_dict = {
        "0000":0, "0001":1, "0010":2, 
        "0011":3, "0100":4, "0101":5,
        "0110":6, "0111":7, "1000":8
    }
    
    trans_list = []
    
    for i, counts in enumerate(counts_list):
        trans_counts = np.zeros(9)
        for bits, number in counts.items():
            if place_dict.get(bits, -1) > -1:
                trans_counts[place_dict.get(bits)] = number
        trans_list.append(trans_counts/trans_counts.sum())
    
    return np.array(trans_list)