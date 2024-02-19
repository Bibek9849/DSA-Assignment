class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def closest_values(root, k, x):
    result = []

    # Helper function to perform inorder traversal and update the result list
    def inorder(node):
        if not node:
            return

        inorder(node.left)
        if len(result) < x:
            result.append(node.val)
        elif abs(node.val - k) < abs(result[0] - k):
            result.pop(0)
            result.append(node.val)
        else:
            return
        inorder(node.right)

    inorder(root)
    return result


# Example usage:
root = TreeNode(5)
root.left = TreeNode(4)
root.right = TreeNode(9)
root.left.left = TreeNode(3)
root.left.right = TreeNode(6)

k = 3.8
x = 2
print(closest_values(root, k, x))
