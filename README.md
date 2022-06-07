# Implementation of Quantum Walks on NISQ devices

## Abstract
Quantum walks play a crucial role in both physics modeling and computation algorithms. In this work, we present strategies to implement quantum walks on near-term quantum devices. We demonstrate that the staggered quantum walk model provides efficient Trotter-Suzuki decomposition in quantum walks simulation. We then state and compare two different encoding methods: qubit mapping and state mapping, thus showing how two encodings have different properties. Those strategies can be applied to any continuous-time quantum walks on a network, thus providing a standard methodology for quantum walks implementation.

## Simulations
### Comparison of random walks and quantum walks

https://user-images.githubusercontent.com/78784216/171912473-e310a429-6e7f-4d36-a126-cf61cb657381.mp4

https://user-images.githubusercontent.com/78784216/171912516-cc740394-9b08-4631-a8ba-32d9d5cb3512.mp4

### Comparison of quantum walks on triangular networks and fractal networks

https://user-images.githubusercontent.com/78784216/171912721-700ff204-345c-4220-96cc-7bac6bc81acb.mp4

### Comparison of quantum walk simulation with different Trotter steps

It seems that the videos are shuffled... (1-layer <-> 5-layer)

https://user-images.githubusercontent.com/78784216/171912891-c4afca70-4b21-42bc-91de-36f28a340571.mp4

### Comparison of simulator results and qpu results (IBMQ Mumbai)

https://user-images.githubusercontent.com/78784216/171913080-e5a1a598-1a56-4c11-a825-7f253aea428e.mp4

## Reference
1. X.-Y. Xu, X.-W. Wang, D.-Y. Chen, C. M. Smith, X.-M. Jin, Quantum transport in fractal networks, Nature Photonics 15 (9) (2021) 703-710. doi:10.1038/s41566-021-00845-4.
2. J. Kempe, Quantum random walks: An introductory overview, Contemporary Physics 44 (4) (2003) 307-327. arXiv:quant-ph/0303081, doi:10.1080/00107151031000110776.
3. O. Mülken, A. Blumen, Continuous-time quantum walks: Models for coherent transport on complex networks, Physics Reports 502 (2) (2011) 37-87. arXiv:1101.2572, doi:10.1016/j.physrep.2011.01.002.
4. F. Acasiete, F. P. Agostini, J. K. Moqadam, R. Portugal, Implementation of quantum walks on IBM quantum computers, Quantum Information Processing 19 (12) (2020) 426. doi:10.1007/s11128-020-02938-5.
5. P. Olivieri, M. Askarpour, E. di Nitto, Experimental implementation of discrete time quantum walk with the ibm qiskit library, in: 2021 IEEE/ACM 2nd International Workshop on Quantum Software Engineering (Q-SE), 2021, pp. 33–38. doi:10.1109/Q-SE52541.2021.00014.
6. R. Portugal, R. A. M. Santos, T. D. Fernandes, D. N. Gonc¸alves, The staggered quantum walk model, Quantum Information Processing 15 (1) (2016) 85–101. arXiv:1505.04761, doi:10.1007/s11128-015-1149-z.
7. R. Portugal, M. C. de Oliveira, J. K. Moqadam, Staggered quantum walks with hamiltonians, Phys. Rev. A 95 (2017) 012328. arXiv:1605.02774, doi:10.1103/PhysRevA.95.012328.
8. O. Katz, M. Cetina, C. Monroe, n-body interactions between trapped ion qubits via spindependent squeezing (2022). arXiv:2202.04230.
9. R. Orbach, Dynamics of fractal networks, Science 231 (4740) (1986) 814–819. doi:10.1126/science.231.4740.814.
10. Y. Salathé, M. Mondal, M. Oppliger, J. Heinsoo, P. Kurpiers, A. Potoˇcnik, A. Mezzacapo, U. Las Heras, L. Lamata, E. Solano, S. Filipp, A. Wallraff, Digital quantum simulation of spin models with circuit quantum electrodynamics, Phys. Rev. X 5 (2015) 021027. arXiv:1502.06778, doi:10.1103/PhysRevX.5.021027.
11. S. Lloyd, Universal quantum simulators, Science 273 (5278) (1996) 1073–1078. doi:10.1126/science.273.5278.1073.
12. M. A. Nielsen, I. L. Chuang, Quantum Computation and Quantum Information: 10th Anniversary Edition, Cambridge University Press, 2010. doi:10.1017/CBO9780511976667.
