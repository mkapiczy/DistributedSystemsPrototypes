from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import numpy as np

# State of the art correct implementation by scipy
Xone = csr_matrix([[0, 8, 0, 3],
                [0, 0, 2, 5],
                [0, 0, 0, 6],
                [0, 0, 0, 0]])

Tcsr = minimum_spanning_tree(Xone)
sota = Tcsr.toarray().astype(int)
print(sota)

# Own implementation
Xtwo = np.array([[0, 8, 0, 3],
                [0, 0, 2, 5],
                [0, 0, 0, 6],
                [0, 0, 0, 0]])

# Get amount of nodes
n_nodes = Xtwo.shape[1]

# Get amount of edges
n_edges = n_nodes - 1

# Replace zeros or should be ignored values with below calculated
Vmax = Xtwo.max()+1000
Xtwo[Xtwo == 0]=Vmax

# Initialize index and vectors
Midx = np.zeros((n_nodes, n_nodes))
v1 = np.zeros((n_edges,n_nodes))

# Note - Row: [Edge Weight, From Node, To Node]
v_finale = np.zeros((n_edges,n_edges))

print(Midx > 0)
# For each node...
for i1 in range(0, n_nodes):
    # Maximize values we do not wish to evaluate.
    # We use the inverse index matrix to ensure mirrowed already taken
    # values are removed
    Xtwo[np.transpose(Midx) > 0] = Vmax
    # Find min and save value and column index
    (mn, idx) = min((v,i) for i,v in enumerate(Xtwo[i1,:]))
    v1[i1, 1] = idx
    v1[i1, 3] = mn
    # Save row index
    v1[i1, 2] = i1
    # Ensure we mark the edge as noted
    Midx[i1,v1[i1,3]] = 1;

    b=2


a = 2