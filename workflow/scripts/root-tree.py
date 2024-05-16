from ete3 import Tree
import argparse


def binarize_tree(tree_path):
    
    """
    Binarizes a tree by resolving polytomies starting from a specified node.

    Args:
        tree_path (str): The path to the input tree file in Newick format.
        node (str): The label of the target node to start binarization from.

    Returns:
        None

    Raises:
        IndexError: If the target node is not found in the tree.

    """
    tree = Tree(tree_path)

    node_to_binarize = tree.search_nodes(name=node)[0]

    # Resolve polytomies recursively, starting from the target node
    node_to_binarize.resolve_polytomy(recursive=True)

    # Output the binarized tree to a new newick file
    output_path = tree_path.replace('.fa.treefile', '_binarized.newick')
    tree.write(format=2, outfile=output_path)

def root_tree(tree_path):
    
    """
    Roots a tree at a specified node.

    Args:
        tree_path (str): The path to the input tree file in Newick format.
        node (str): The label of the target node to root the tree at.

    Returns:
        None

    Raises:
        IndexError: If the target node is not found in the tree.

    """
    tree = Tree(tree_path)
    # Find the node with the longest branch length
    max_branch_length = 0
    max_branch_node = None
    for node in tree.traverse():
        if node.dist > max_branch_length:
            max_branch_length = node.dist
            max_branch_node = node

    #node_to_root = tree.search_nodes(name=max_branch_node)[0]

    # Root the tree at the target node
    tree.set_outgroup(max_branch_node)

    # Output the rooted tree to a new newick file
    output_path = tree_path.replace('.treefile', '_rooted.newick')
    tree.write(format=2, outfile=output_path)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--tree_path", help="Path to the newick tree file")
    parser.add_argument('-n', "--node_name", help="Name of the node to binarize")
    args = parser.parse_args()

    #binarize_tree(args.tree_path, args.node_name)
    root_tree(args.tree_path)

if __name__ == "__main__":
    main()