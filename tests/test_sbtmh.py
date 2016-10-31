from glob import glob
import os

from sourmash_lib import signature

from sbt import GraphFactory, NodePos
from sbtmh import SigLeaf, search_minhashes

from .conftest import SBTImplementation


def test_tree_save_load(SBTImplementation):
    factory = GraphFactory(31, 1e5, 4)
    tree = SBTImplementation(factory)
    for f in glob("urchin/lividus*.sig"):
        with open(f, 'r') as data:
            sig = signature.load_signatures(data)
        leaf = SigLeaf(os.path.basename(f), sig[0])
        tree.add_node(leaf)
        to_search = leaf

    print('*' * 60)
    print("{}:".format(to_search.metadata))
    old_result = [str(s) for s in tree.find(search_minhashes, to_search.data, 0.1)]
    print(*old_result, sep='\n')

    tree.save('urchin')

    tree = SBTImplementation.load('urchin.sbt.json', leaf_loader=SigLeaf.load)

    print('*' * 60)
    print("{}:".format(to_search.metadata))
    new_result = [str(s) for s in tree.find(search_minhashes, to_search.data, 0.1)]
    print(*new_result, sep='\n')

    assert old_result == new_result
    assert len(old_result) > 0


def test_binary_nary_tree(SBTImplementation):
    factory = GraphFactory(31, 1e5, 4)
    trees = {}
    trees[2] = SBTImplementation(factory)
    trees[5] = SBTImplementation(factory, d=5)
    trees[10] = SBTImplementation(factory, d=10)

    for f in glob("urchin/lividus*.sig"):
        with open(f, 'r') as data:
            sig = signature.load_signatures(data)
        leaf = SigLeaf(os.path.basename(f), sig[0])
        for tree in trees.values():
            tree.add_node(leaf)
        to_search = leaf

    results = {}
    print('*' * 60)
    print("{}:".format(to_search.metadata))
    for d, tree in trees.items():
        results[d] = [str(s) for s in tree.find(search_minhashes, to_search.data, 0.1)]
    print(*results[2], sep='\n')

    assert set(results[2]) == set(results[5])
    assert set(results[5]) == set(results[10])
    assert len(results) > 0
