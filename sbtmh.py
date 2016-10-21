from glob import glob
import os

from khmer import Nodegraph, khmer_args
from sourmash_lib import signature
from sbt import SBT, GraphFactory, SigLeaf


def test_tree():
    factory = GraphFactory(31, 1e4, 4)
    tree = SBT(factory)
    for f in glob("urchin/*.sig"):
        with open(f, 'r') as data:
            sig = signature.load_signatures(data)
        leaf = SigLeaf(os.path.basename(f), sig[0])
        tree.add_node(leaf)
