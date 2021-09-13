"""
Pseudocode: clrs chapter 21 (page 571)
When we use both union by rank and path compression, the worst-case running time is
O(m alpha(n)) for m disjoint-set operations on n elements, alpha is a very slowly growing function (inverse ackerman)
"""
class DisjointSets:
    def __init__(self, list_universe):
        self.universe = list_universe
        self.n = len(list_universe)
        self.rank = {}
        self.parent = {}
        self._make_set(list_universe)

    def _make_set(self, list):
        for x in list:
            self.parent[x] = x
            self.rank[x] = 0

    def find_set(self, x):      #find set with path compression
        """
        The FIND-SET procedure is a two-pass method: as it recurses, it makes one pass up the find path to find the root
        and as the recursion unwinds, it makes a second pass back down the find path
        to update each node to point directly to the root.
        """
        if x is not self.parent[x]:
            self.parent[x] = self.find_set(self.parent[x])
        return self.parent[x]

    def find_set_iter(self, x):
        px = x
        while px is not self.parent[px]:
            px = self.parent[px]        #trace to root

        while x != px:
            i = self.parent[x]
            self.parent[x] = px     #link to root
            x = i

        return px


    def link(self, x, y):
        root_x = self.find_set(x)
        root_y = self.find_set(y)
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[y] = root_x
        else:
            self.parent[x] = root_y
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[y] += 1

    def union(self, x, y):
        self.link(x, y)

    def __repr__(self):
        return str(self.parent)

    def print_sets(self):
        print([self.find_set(i) for i in self.universe])


univ = [1, 2, 3, 4, 5]
ds = DisjointSets(univ)
print('Disjoint sets: ', ds)
ds.print_sets()

print(ds.find_set(5))
print(ds.find_set_iter(5))

ds.union(4, 3)
print('Disjoint sets: ', ds)
ds.print_sets()

ds.union(2, 1)
print('Disjoint sets: ', ds)
ds.print_sets()

ds.union(4, 5)
print('Disjoint sets: ', ds)
ds.print_sets()

ds.union(1, 3)
print('Disjoint sets: ', ds)
print(ds.find_set_iter(2))
ds.print_sets()

"""
clrs Problems 21-3 Tarjan's off-line least common ancestors
The least common ancestor of two nodes u and v in a rooted tree T is the node w
that is an ancestor of both u and v, and that has the greatest depth in T
https://www.techiedelight.com/find-lowest-common-ancestor-lca-two-nodes-binary-tree/
"""
class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def isNodePresent(root, node):
    if root is None:
        return False
    if root == node:
        return True
    return isNodePresent(root.left, node) or isNodePresent(root.right, node)

def findLCA(root, x, y):
    lca = None
    if isNodePresent(root, x) and isNodePresent(root, y):
        _, lca = find_lca(root, lca, x, y)

        if lca:
            print("LCA is ", lca.data)
        else:
            print("LCA does not exist")

def find_lca(root, lca, x, y):
    if root is None:
        return False, lca
    if root == x or root == y:
        return True, root

    # recursively check if `x` or `y` exists in the left subtree
    left, lca = find_lca(root.left, lca, x, y)

    # recursively check if `x` or `y` exists in the right subtree
    right, lca = find_lca(root.right, lca, x, y)

    # if `x` is found in one subtree and `y` is found in the other subtree,
    # update lca to the current node
    if left and right:
        lca = root

    return (left or right), lca

"""
          1
        /   \
       /     \
      2       3
       \     / \
        4   5   6
           / \
          7   8
"""
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.right = Node(4)
root.right.left = Node(5)
root.right.right = Node(6)
root.right.left.left = Node(7)
root.right.right.right = Node(8)

findLCA(root, root.right.left.left, root.right.right)

