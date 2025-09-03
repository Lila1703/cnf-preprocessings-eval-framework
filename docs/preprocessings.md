# Preprocessors

This file describes the preprocessors currently integrated in the framework.

## Unit Propagation

### Description

A unit clause is a clause $U$ that contains only a single literal $U = \{l\}$. Because all clauses must evaluate to true, this literal $l$ must be satisfied. The unit clause $U$ can therefore be removed from the clause list and all clauses where $l$ or $\bar{l}$ occur can be simplified (in the case of $\bar{l}$) or removed (in the case of $l$).

### #SAT Behaviour

Unit propagation results in a _logically equivalent_ formula and does therefore not change the number of solutions.

### Implementation

A simple implementation can be found in the [unitprop](../unitprop) directory.

## Subsumption

### Description

If the clause list contains two clauses $C_1 \subset C_2$, then every assignment that satisfies $C_1$ will also satisfy $C_2$. The clause $C_2$ can thus be removed.

### SAT# Behaviour

Like unit propagation, subsumption results in a _logically equivalent_ formula and doesn't change the number of solutions.

### Implementation

A simple implementation can be found in the [subsump](../subsump) directory.

## [Equivalent Literal Elimination](https://link.springer.com/article/10.1007/s10472-005-0433-5)

### Description

Assume the clause list contains a binary clause $B = l \lor m$. From this clause it follows that $\bar{l} \implies m$ and $\bar{m} \implies l$. Given all binary clauses we can build a directed graph $G = (V, E)$ with  the node set $V = \{l : l appears in a binary clause\} \cup \{\bar{l} : l appears in a binary clause\}$. The edge $(l, m)$ exists in the graph if and only if $\bar{l} \lor m$ (which is equivalent to $l \implies m$) is in the clause list.

Assume now that the literals $l_1, \dots, l_m$ form a _strongly connected component_ of this graph, i.e. there is a path from $l_i$ to $l_j$ for all $i, j \in \{1, \dots, m\}$. Because implication is transitive, it follows that $l_i \implies l_j$ and because a path from $l_j$ to $l_i$ also exists it follows $l_i \iff l_j$.

The literals of all strongly connected components of the implication graph are therefore equivalent and can be replaced by a single literal.

Strongly connected components can be calculated using [Kosaraju-Sharir's algorithm](https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm) or [Tarjan's strongly connected components algorithm](https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm).

### SAT# Behaviour

Care has to be taken when replacing literals that the number of solutions is not altered. If a literal was replaced, it needs to be removed from the literal list or the number of solutions will be doubled.

### Implementation

A simple implementation can be found in the [equivalentliteralelimination](../equivalentliteralelimination) directory.

## [Probing](https://ieeexplore.ieee.org/document/1250177)

### Description

Probing is a collection of preprocessings that make use of boolean constraint propagation. Assume $\phi$ is a formula, and $\alpha$ is an assignment of some of the variables in $\phi$, then $BCP(\phi, \alpha)$ denotes result of boolean constraint propagation. $BCP(\phi, \alpha)$ thus contains the assignments that can be inferred from $\alpha$ using unit propagation.

The following simplifications can be made:

- Given a formula $\phi$ and a variable $x$, the assignments $BCP(\phi, x) \cap BCP(\phi, \bar{x})$ are implied by $x$ and by $\bar{x}$ and are therefore necessary for the formula to be true.
- Given a formula $\phi$ and a clause $C$, the assignments $\bigcap_\{l \in C\} BCP(\phi, l)$ are also necessary, because they are implied by every literal in the clause $C$.
- Given a formula $\phi$ and a variable $x$, then the assigment $\bar{x}$ is necessary if $BCP(\phi, x)$ leads to a conflict (i.e. $BCP(\phi, x) = \{l, \bar{l}\}).

It is furthermore possible to infer equivalent literals. Two variables $x$ and $y$ are equivalent if either
- $\bar{y} \in BCP(\phi, \bar{x})$ and $y \in BCP(\phi, x)$ or
- $\bar{y} \in BCP(\phi, \bar{x})$ and $\bar{x} \in BCP(\phi, \bar{y})$.

Utilizing these rules the following algorithm is used:

1. Calculate $BCP(\phi, x)$ for every $x$.
2. Identify necessary assignments using the first three rules.
3. Identify equivalent literals using the last two rules.
4. If equivalent literals were found, go to step 1.

### SAT# Behaviour

Probing results in a _logically equivalent_ formula and doesn't change the number of solutions.

### Implementation

An implementation can be found in the [coprocessor](https://github.com/nmanthey/riss-solver/blob/master/coprocessor/techniques/Probing.cc) tool.

## [Hidden Tautology Elimination](https://www.cs.utexas.edu/~marijn/publications/LPAR17.pdf)

### Description

Given a formula $\phi$ and a clause $C$ we can compute a new clause $HLA(\phi, C)$ by repeating the following: If there is a literal $l_0 \in C$ such that $(l_0 \lor l) \in \phi \setminus C$ then set $C = C \cup \{\bar{l}\}$.

For every $l \in HLA(\phi, C) \setminus C$ there is for some $l_0 \in C$ a chain $(l_0 \lor \bar{l_1}), (l_1 \lor \bar{l_2}), \dots, (l_{k-1} \lor \bar{l_k})$ which is equivalent to $l_k \implies l_{k-1}, \dots, l_1 \implies l_0$.

The formulas $\phi$ and $(\phi \setminus C) \cup \{HLA(\phi, C)\}$ are logically equivalent:
Assume that $\tau$ is a satisfying assignment for $\phi$ then $\phi \setminus C$ is obviously satisfied. And since $C \subset HLA(\phi, C)$, the clause $HLA(\phi, C)$ must also be satisfied.
Assume now that $\tau$ is a satisfying assignment for $(\phi \setminus C) \cup \{HLA(\phi, C)}$. There must be a literal $l_k$ in $HLA(\phi, C)$ with $\tau(l_k) = 1$ and since a chain $l_k \implies l_{k-1}, \dots, l_1 \implies l_0$ exists, $\tau(l_0)$ will be $1$ and $C$ must therefore be satisfied.

Notice that the clause $HLA(\phi, C)$ can be tautological, i.e. it can contain both $l$ and $\bar{l}$. In this case $\phi$ and $\phi \setminus C$ are equivalent. We can thus simplify the formula $\phi$ by repeatedly computing $HLA(\phi, C)$ and removing $C$ from $\phi$ if $HLA(\phi, C)$ is tautological.

### SAT# Behaviour

Hidden tautology elimination results in a _logically equivalent_ formula and doesn't change the number of solutions.

### Implementation

An implementation can be found in the [coprocessor](https://github.com/nmanthey/riss-solver/blob/master/coprocessor/techniques/HiddenTautologyElimination.cc) tool.

## sharpSAT Preprocessor

### Description

The sharpSAT solver uses the following preprocessing steps:

1. Unit propagation
2. Failed literal testing
3. Compaction

Unit propagation works exactly as explained earlier. The failed literal testing is a special case of probing: If setting $x$ to true and applying boolean constraint propagation leads to a conflict, $x$ must be set to false. Similarly, if setting $x$ to false leads to a conflict, $x$ must be set to true. sharpSAT tries this for every variable in the input formula. The final step of sharpSAT's preprocessor is compaction. In this step unused variables are removed from the formula.

### SAT# Behaviour

Unit propagation and failed literal testing result in a logically equivalent formula. Care has to be taken however, that variables that are removed in the compaction step are accounted for. If an unused variable is removed, the number of solutions will be cut in half.

### Implementation

The implementation can be found in the `Solver::simplePreProcess` function of [sharpSAT](https://github.com/marcthurley/sharpSAT/blob/master/src/solver.cpp).

## Adding Binary Resolvents

### Description

For some solvers it may prove beneficial to add redundant clauses. Assume $\phi$ is a formula and $l_0$ is a literal, then redundant clauses can be added by finding some $l_1 \in BCP(\phi, l_0)$ and adding the clause $\bar{l_0} \lor l_1$, which encodes the implication $l_0 \implies l_1$.

### #SAT Behaviour

Adding binary resolvents only adds redundant clauses and therefore doesn't change the number of solutions.

### Implementation

An implementation can be found in the [coprocessor](https://github.com/nmanthey/riss-solver/blob/master/coprocessor/techniques/Resolving.cc) tool.

## Hyper Binary Resolution

### Description

Assume $\phi$ is a formula and $C = l \lor l_1 \dots \lor l_k$ and $C_i = l' \lor \bar{l_i}$ are clauses for $i = 1, \dots, k$. Then the clause $l' \lor l$ is implied by $\phi$ and can be added.

### #SAT Behaviour

Adding clauses computed by hyper binary resolution only adds redundant clauses and therefore doesn't change the number of solutions.

### Implementation

An implementation can be found in the [coprocessor](https://github.com/nmanthey/riss-solver/blob/master/coprocessor/techniques/HBR.cc) tool.

## Preprocessors that don't work for #SAT

The following preprocessors change the number of solutions and are thus not suitable for use in a #SAT-solver:

- Bounded Variable Elimination
- Bounded Variable Addition
- Blocked Clause Elimination
- Covered Clause Elimination