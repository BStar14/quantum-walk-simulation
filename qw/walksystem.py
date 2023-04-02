from typing import Optional
import numpy as np
import csv
import pickle

class WalkSystem:
    
    """Create a walk system.
    
    Args:
        folder (str): refer to _folder_dict
        sys (str): refer to _sys_dict
        network (str): refer to _network_dict
        walktype (str): rw, qw or 3tqw
        encoding (str): ex, un or bin
        order (int): the order of a fractal network
        length (int): the length of a triangular network
        layers (int): the number of layers
        qw (bool): if the system is quantum walk or random walk
    """
    
    def __init__(self, 
                 folder: str, 
                 sys: Optional[str]=None, 
                 network: Optional[str]=None, 
                 walktype: Optional[str]=None, 
                 encoding: Optional[str]=None, 
                 order: Optional[int]=None, 
                 length: Optional[int]=None, 
                 layers: Optional[int]=None, 
                 **kwargs
                ):
                
        # Initialize
        self.sys = None
        self.network = None
        self.walktype = walktype
        self.encoding = encoding
        self.order = None
        self._name = None
        self._ly = None
        
        # Unpack kwags
        for key, value in kwargs.items():
            if key == 'name':
                self._name = value
        
        # Save folder, sys and network information according to dictionaries
        self._folder_dict = {'ex':'data/exact/', 'sim':'data/simulator/', 'qpu':'data/qpu/'}
        self._sys_dict = {'ex':'exact', 'qasm':'ibmq_qasm_simulator', 
                          'montreal':'ibmq_montreal', 'mumbai':'ibmq_mumbai', 'auckland':'ibm_auckland', 'hanoi':'ibm_hanoi', 
                          'ionq_sim':'ionq_simulator'}
        self._network_dict = {'tri':'tri', 'sg':'sg', 'dsg':'dsg'}
        self.folder = self._folder_dict[folder]
        if sys != None: 
            self.sys = self._sys_dict[sys]
        elif folder == 'ex':
            self.sys = 'exact'
        if network != None: self.network = self._network_dict[network]
        
        # Set default walktype according to folder
        if self.walktype == None:
            if self.folder == 'data/exact/':
                self.walktype = 'qw'
            else:
                self.walktype = '3tqw'
        
        # Set default encoding according to folder
        if self.encoding == None:
            if self.folder == 'data/exact/':
                self.encoding = 'ex'
            else:
                self.encoding = 'un'
        
        # Set default order or length, according to the network
        if self.network == 'tri' and length != None:
            self.order = f'l{length}'
        elif self.network != 'tri' and order != None:
            self.order = f'o{order}'
        elif self.network != 'tri':
            self.order = f'o2'
        
        # If the system is exact, the number of simulating steps is fixed to 1500
        # If not, it is 300
        if self.folder == 'data/exact/':
            self._steps = 1500
        else:
            self._steps = 300
        
        # dt = .01
        self._dt = .01
        
        # t = steps*dt
        self._t = self._steps*self._dt
        
        # Save layer information to be variational if the system is exact
        if self.folder == 'data/exact/':
            self._ly = '1500vly'
        elif layers != None:
            self._ly = f'{layers}ly'
        
    @property
    def name(self):
        if self._name == None:
            return f'{self.sys}_{self.network}_{self.walktype}_{self.encoding}_{self.order}_{self._t:.1f}s_{self._ly}'
        else:
            return self._name
    
    @property
    def dict_list(self) -> list:
        """Return dictionary list.
        """
        return list[self._folder_dict, self._network_dict, self._sys_dict]
    
    def read_msd_list(self, **kwargs) -> np.ndarray:
        
        for key, value in kwargs.items():
            if key == 'name':
                self._name = value
            elif key == 'sys':
                self.sys = self._sys_dict[value]
            elif key == 'order' and self.network != 'tri':
                self.order = f'o{value}'
            elif key == 'length' and self.network == 'tri':
                self.order = f'l{value}'
            elif key == 'layers' and self.folder != 'data/exact/':
                self._ly = f'{value}ly'
        
        if self._name == None and (self.sys == None 
                                   or self.order == None 
                                   or self._ly == None):
            raise SyntaxError
        
        msd_list = []
        with open(f'{self.folder}{self.name}_msd_list.csv','r') as file :
            read = csv.reader(file)
            for row in read:
                for item in row:
                    msd_list.append(float(item))
        
        return np.array(msd_list)
    
    def read_counts_list(self, **kwargs):
        
        for key, value in kwargs.items():
            if key == 'name':
                self._name = value
            elif key == 'sys':
                self.sys = self._sys_dict[value]
            elif key == 'order' and self.network != 'tri':
                self.order = f'o{value}'
            elif key == 'length' and self.network == 'tri':
                self.order = f'l{value}'
            elif key == 'layers' and self.folder != 'data/exact/':
                self._ly = f'{value}ly'
        
        if self._name == None and (self.sys == None 
                                   or self.order == None 
                                   or self._ly == None):
            raise SyntaxError
        
        with open(f'{self.folder}{self.name}_counts_list.pkl','rb') as file :
            counts_list = pickle.load(file)
        
        return counts_list
    
    def read_all_msd(self, **kwargs) -> np.ndarray:
        
        msd_by_kwargs = []
        for key, arg_list in kwargs.items():
            for arg in arg_list:
                if key == 'name':
                    msd_by_kwargs.append(self.read_msd_list(name=arg))
                elif key == 'sys':
                    msd_by_kwargs.append(self.read_msd_list(sys=arg))
                elif key == 'order':
                    msd_by_kwargs.append(self.read_msd_list(order=arg))
                elif key == 'length':
                    msd_by_kwargs.append(self.read_msd_list(length=arg))
                elif key == 'layers':
                    msd_by_kwargs.append(self.read_msd_list(layers=arg))
        
        return np.array(msd_by_kwargs)
    
    def read_all_counts(self, **kwargs):
        
        counts_by_kwargs = []
        for key, arg_list in kwargs.items():
            for arg in arg_list:
                if key == 'name':
                    msd_by_kwargs.append(self.read_msd_list(name=arg))
                elif key == 'sys':
                    counts_by_kwargs.append(self.read_counts_list(sys=arg))
                elif key == 'order':
                    counts_by_kwargs.append(self.read_counts_list(order=arg))
                elif key == 'length':
                    counts_by_kwargs.append(self.read_counts_list(length=arg))
                elif key == 'layers':
                    counts_by_kwargs.append(self.read_counts_list(layers=arg))
        
        return counts_by_kwargs