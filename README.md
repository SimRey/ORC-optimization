# Multi-objective optimization of ORC Using NSGA-II Algorithm with Python-ASPEN Hybrid Platform

This repository presents an approach to optimize Organic Rankine Cycle (ORC) systems using the NSGA-II algorithm within a hybrid platform bridging Python and Aspen Plus. In this  framework, Python and Aspen Plus communicate seamlessly through a COM (Component Object Model) connection, enabling efficient data exchange and integration of optimization algorithms with process simulation.

### General formulation

This problem aims to minimize the environmental impact of the ORC while maximizing its efficiency.

$$
\begin{align}
\begin{split}
\min_{x_i, P_P} \;\; & env = \sum_i{x_i}*GWP_i*MW_i*F \\[2mm]
\max_{x_i, P_P} \;\; &  \eta = \frac{W_{turb} - W_{pump}}{Q_{in}} \\[1mm]
\text{s.t.} \;\; & \sum_i{x_i} = 1 \\[1mm]
& 0 \leq x_i \leq 1 \\
& 0 \leq P_P \leq 10\\[1mm]
& x_i, P_P \in \mathbb{R}
\end{split}
\end{align}
$$

Where:

- $x_i$ represents the molar fraction of the components.
- $GWP_i$ represents the Global Warming potential in $\frac{kg_{CO_2}}{kg_i}$
- $P_P$ stands for the Pump pressure in $bar$
- $F$ stands for the total molar flowrate in $\frac{kmol}{s}$

### Case study 1

For this case study, butane, pentane, isobutane, and isopentane were chosen as working fluids. To replicate the results, run `main.ipynb` in the `Case study 1` folder.

### Case study 2

For this case, in addition to the working fluids butane, pentane, isobutane, and isopentane, the refrigerants R113, R114, R123, and R124 were also used. To replicate the results, run `main.ipynb` in the `Case study 2` folder.


### Conclusion

This work demonstrates the significant capability of connecting Python with ASPEN, enabling optimization of the intriguing ORC technology using a model-free method. It is worth noting that this work could be further expanded and enhanced, considering factors such as net profit or operational risks (e.g., flammability, toxicity).
