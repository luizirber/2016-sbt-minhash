from glob import glob
import os

from khmer import Nodegraph, khmer_args
from sourmash_lib import signature
from sbt import SBT, GraphFactory, SigLeaf, Node


def search_minhashes(node, sig, threshold):
    mins = sig.estimator.mh.get_mins()

    if isinstance(node, SigLeaf):
        matches = node.data.estimator.count_common(sig.estimator)
    else:  # Node or Leaf, Nodegraph by minhash comparison
        matches = sum(1 for value in mins if node.data.get(value))

    if matches / len(mins) >= threshold:
        return 1
    return 0


def test_tree():
    factory = GraphFactory(31, 1e5, 4)
    tree = SBT(factory)
    for f in glob("urchin/*.sig"):
        with open(f, 'r') as data:
            sig = signature.load_signatures(data)
        leaf = SigLeaf(os.path.basename(f), sig[0])
        tree.add_node(leaf)
        to_search = leaf

    tree.print()

    print('*' * 60)
    print("{}:".format(to_search.metadata))
    print(*[str(s) for s in tree.find(search_minhashes, to_search.data, 0.1)],
          sep='\n')


if __name__ == "__main__":
    test_tree()
