import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.extensions.unitary import UnitaryGate
from qiskit.quantum_info.operators import Operator


def staggered_dsg_circuit_3t(
    size_degree: int = 2,
    t: float = 1.,
    layers: int = 1,
    decompose: bool = False,
    linear_operation: bool = False
) -> QuantumCircuit:
    """
    Given size, time t, and the number of steps n, constructs the corresponding staggered quantum walk circuit on DSG.
    Still fixed size_degree at 2
    3 parts of tessellation
    Args:
        size_degree: The degree of DSG (size = 3**size_degree)
        t: Total simulation time
        layers: Number of layers
    Returns:
        QuantumCircuit
    """
    
    size = 3**size_degree
    node_list = np.arange(size)
    theta = np.pi*t/layers
    zeta = complex(np.cos(-2*theta), np.sin(-2*theta))
    
    interaction = UnitaryGate(
        Operator([
        [1, 0, 0, 0],
        [0, (zeta+1)/2, (-1*zeta+1)/2, 0],
        [0, (-1*zeta+1)/2, (zeta+1)/2, 0],
        [0, 0, 0, 1]])
    )

    def interaction_2(size, interaction, qubits, name=None, decompose=False):
        qc = QuantumCircuit(size)
        qc.append(interaction, qubits)
        if decompose: qc = transpile(qc, basis_gates=['u', 'cx'], optimization_level=2)
        if name!=None: qc.name = name
        return qc

    simulation = QuantumCircuit(size, size)

    simulation.x(0)

    for i in range(layers):
        
        simulation.barrier()
        
        # Staggered Quantum Walks tessellation 1
        for j in node_list[::3]:
            a = int(j+(j//3)%3)
            b = int(j+(j//3+1)%3)
            simulation.compose(
                interaction_2(size, interaction, [node_list[a], node_list[b]], 'tessel1', decompose),
                range(size),
                inplace=True
                )
            if linear_operation: simulation.barrier()
        for j in node_list[7::9]:
            simulation.compose(
                interaction_2(size, interaction, [j, node_list[j-5]], 'tessel1', decompose),
                range(size),
                inplace=True
                )
            if linear_operation: simulation.barrier()
        
        # Staggered Quantum Walks tessellation 2
        for j in node_list[::3]:
            a = int(j+(j//3+2)%3)
            b = int(j+(j//3)%3)
            simulation.compose(
                interaction_2(size, interaction, [node_list[a], node_list[b]], 'tessel2', decompose),
                range(size),
                inplace=True
                )
            if linear_operation: simulation.barrier()
        for j in node_list[1::9]:
            simulation.compose(
                interaction_2(size, interaction, [j, node_list[j-5]], 'tessel2', decompose),
                range(size),
                inplace=True
                )
            if linear_operation: simulation.barrier()
        
        # Staggered Quantum Walks tessellation 3
        for j in node_list[::3]:
            a = int(j+(j//3+1)%3)
            b = int(j+(j//3+2)%3)
            simulation.compose(
                interaction_2(size, interaction, [node_list[a], node_list[b]], 'tessel3', decompose),
                range(size),
                inplace=True
                )
            if linear_operation: simulation.barrier()
        for j in node_list[4::9]:
            simulation.compose(
                interaction_2(size, interaction, [j, node_list[j-5]], 'tessel3', decompose),
                range(size),
                inplace=True
                )
            if linear_operation: simulation.barrier()

    if not linear_operation: simulation.barrier()
    
    for i in node_list:
        simulation.measure(i, i)
       
    return simulation

def staggered_dsg_circuit_log3t(
    size_degree: int = 2,
    t: float = 1.,
    layers: int = 1,
    wrap: bool = False,
    barrier: bool = False
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
    
    interaction = UnitaryGate(
        Operator([
        [(zeta+1)/2, (-1*zeta+1)/2],
        [(-1*zeta+1)/2, (zeta+1)/2]]),
        label='U'
    ).control()
    
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
        
        tessel1.name = 'tessel_1'
        
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
        
        tessel2.name = 'tessel_2'
        
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
        
        tessel3.name = 'tessel_3'
        
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
        
        back.name = 'permute_back'
        
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