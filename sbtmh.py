from sourmash_lib import signature
from sbt import SBT, GraphFactory, Leaf


class SigLeaf(Leaf):
    def __str__(self):
        return '**Leaf:{name} -> {metadata}'.format(
                name=self.name, metadata=self.metadata)

    def save(self, filename):
        with open(filename, 'w') as fp:
            signature.save_signatures([self.data], fp)

    def update(self, parent):
        for v in self.data.estimator.mh.get_mins():
            parent.data.count(v)

    @staticmethod
    def load(info):
        with open(info['filename'], 'r') as fp:
            data = signature.load_signatures(fp)[0]
        return SigLeaf(info['metadata'], data, name=info['name'])


def search_minhashes(node, sig, threshold, results=None):
    mins = sig.estimator.mh.get_mins()

    if isinstance(node, SigLeaf):
        matches = node.data.estimator.count_common(sig.estimator)
    else:  # Node or Leaf, Nodegraph by minhash comparison
        matches = sum(1 for value in mins if node.data.get(value))

    if results is not None:
        results[node.name] = matches / len(mins)

    if matches / len(mins) >= threshold:
        return 1
    return 0
