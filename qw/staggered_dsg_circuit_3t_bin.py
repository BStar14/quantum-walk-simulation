import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import RXGate
from qiskit.extensions.unitary import UnitaryGate
from qiskit.quantum_info.operators import Operator

def staggered_dsg_circuit_3t_bin(
    size_degree: int = 2,
    t: float = 1.,
    layers: int = 1,
    wrap: bool = False,
    barrier: bool = False,
    model: str = 'Heisenberg'
) -> QuantumCircuit:
    """
    Given size, time t, and the number of steps n, constructs the corresponding log size staggered quantum walk circuit on DSG.
    Size_degree is fixed at 2
    3 parts of tessellation
    Args:
        size_degree: The degree of DSG (size = 3**size_degree)
        t: Total simulation time
        layers: Number of layers
    Returns:
        QuantumCircuit
    """
    
    size = np.ceil(np.log2(3**size_degree)).astype(int)
    theta = np.pi*t/layers
    zeta = complex(np.cos(-2*theta), np.sin(-2*theta))
    
    if model == 'XY':
        interaction = RXGate(2*theta)
    elif model == 'Heisenberg':
        interaction = UnitaryGate(
            Operator([
            [(zeta+1)/2, (-1*zeta+1)/2],
            [(-1*zeta+1)/2, (zeta+1)/2]]),
            label='U'
        )
    else:
        raise NotImplementedError()
    
    interaction = interaction.control()
    
    def tessellation1(size, interaction):
        """Staggered Quantum Walks tessellation 1"""
        tessel1 = QuantumCircuit(size)
        
        tessel1.mct([0,1], 2)    # flip 0011 <-> 0111 (with R.C.)
        
        tessel1.mct([0,1,2], 3)    # shift +1 (with C.I.)
        tessel1.mct([0,1], 2)
        tessel1.cx(0, 1)
        
        tessel1.cx(3, 0)    # flip 1000 <-> 1001
        
        tessel1.cx(0, 1)    # shift -1 (with C.I.)
        tessel1.mct([0,1], 2)
        tessel1.mct([0,1,2], 3)
        
        tessel1.x(3)    # apply the interaction
        tessel1.append(interaction, [3,0])
        tessel1.x(3)
        
        tessel1.name = 'Tessel-1'
        
        return tessel1
    
    def tessellation2(size, interaction):
        """Staggered Quantum Walks tessellation 2"""
        tessel2 = QuantumCircuit(size)
        
        tessel2.x(0)    # flip 0010 <-> 0110 (with C.I.)
        tessel2.mct([0,1], 2)
        
        tessel2.x([2,3])    # flip 0000 <-> 0010 (with C.I.)
        tessel2.mct([0,2,3], 1)
        tessel2.x([2,3])
        
        tessel2.cx(0, 1)    # shift -1 (with C.I.)
        tessel2.mct([0,1], 2)
        tessel2.mct([0,1,2], 3)
        
        tessel2.x(3)    # apply the interaction
        tessel2.append(interaction, [3,2])
        tessel2.x(3)
        
        tessel2.name = 'Tessel-2'
        
        return tessel2
    
    def tessellation3(size, interaction):
        """Staggered Quantum Walks tessellation 3"""
        tessel3 = QuantumCircuit(size)
        
        tessel3.mct([0,1,2], 3)    # shift +1 (with C.I.)
        tessel3.mct([0,1], 2)
        tessel3.cx(0, 1)
        
        tessel3.x([2,3])    # flip 0000 <-> 0010 (with C.I.)
        tessel3.mct([0,2,3], 1)
        tessel3.x([2,3])
        
        tessel3.mct([0,1], 2)    # flip 0010 <-> 0110 (with C.I.)
        tessel3.x(0)
        
        tessel3.mct([0,1], 2)    # flip 0011 <-> 0111
        
        tessel3.mct([0,2], 1)    # flip 0101 <-> 0111
        
        tessel3.x(0)    # shift -1
        tessel3.cx(0, 1)
        tessel3.mct([0,1], 2)
        tessel3.mct([0,1,2], 3)
        
        tessel3.x(3)    # apply the interaction
        tessel3.append(interaction, [3,0])
        tessel3.x(3)
        
        tessel3.name = 'Tessel-3'
        
        return tessel3
    
    def permute_back(size, interaction):
        """Permute back to the initial order"""
        back = QuantumCircuit(size)
        
        back.mct([0,1,2], 3)    # shift +1
        back.mct([0,1], 2)
        back.cx(0, 1)
        back.x(0)
        
        back.mct([0,2], 1)    # flip 0101 <-> 0111
        
        back.mct([0,1], 2)    # flip 0011 <-> 0111
        
        back.mct([0,1,2], 3)    # shift +1 (with C.I.)
        back.mct([0,1], 2)
        back.cx(0, 1)
        
        back.cx(3, 0)    # flip 1000 <-> 1001
        
        back.cx(0, 1)    # shift -1 (with C.I.)
        back.mct([0,1], 2)
        back.mct([0,1,2], 3)
        
        back.mct([0,1], 2)
        
        back.name = 'Permute-back'
        
        return back
    
    # Assemble the circuit
    simulation = QuantumCircuit(size, size)
    
    for i in range(layers):
        simulation.compose(tessellation1(size, interaction), range(size), inplace=True, wrap=wrap)
        if barrier: simulation.barrier()
        simulation.compose(tessellation2(size, interaction), range(size), inplace=True, wrap=wrap)
        if barrier: simulation.barrier()
        simulation.compose(tessellation3(size, interaction), range(size), inplace=True, wrap=wrap)
        if barrier: simulation.barrier()
        simulation.compose(permute_back(size, interaction), range(size), inplace=True, wrap=wrap)
        simulation.barrier()
        
    for i in range(size):
        simulation.measure(i, i)
    
    return simulation