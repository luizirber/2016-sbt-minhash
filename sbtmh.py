from glob import glob
import os

from sourmash_lib import signature
from sbt import SBT, GraphFactory, Leaf


class SigLeaf(Leaf):
    def __str__(self):
        return '**Leaf:{name} -> {metadata}'.format(
                name=self.name, metadata=self.metadata)

    def save(self, filename):
        from sourmash_lib import signature
        with open(filename, 'w') as fp:
            signature.save_signatures([self.data], fp)

    def update(self, parent):
        for v in self.data.estimator.mh.get_mins():
            parent.data.count(v)

    @staticmethod
    def load(info):
        from sourmash_lib import signature
        with open(info['filename'], 'r') as fp:
            data = signature.load_signatures(fp)[0]
        return SigLeaf(info['metadata'], data, name=info['name'])


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

    #tree.print()

    print('*' * 60)
    print("{}:".format(to_search.metadata))
    old_result = [str(s) for s in tree.find(search_minhashes, to_search.data, 0.1)]
    print(*old_result, sep='\n')

    tree.save('urchin')

    tree = SBT.load('urchin.sbt.json', leaf_loader=SigLeaf.load)

    print('*' * 60)
    print("{}:".format(to_search.metadata))
    new_result = [str(s) for s in tree.find(search_minhashes, to_search.data, 0.1)]
    print(*new_result, sep='\n')

    assert old_result == new_result


if __name__ == "__main__":
    test_tree()
