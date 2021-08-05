def InvertNodeClass(tree):
    if tree:
        left = tree.left
        right = tree.right
        tree.left = right
        tree.right = left
        InvertNodeClass(tree.left)
        InvertNodeClass(tree.right)
    if not tree:
        pass

class Node:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None

#EXAMPLE
EXAMPLE = """
     4 
   /  \
  2     5 
 / \   / \
1   3 4   6
"""