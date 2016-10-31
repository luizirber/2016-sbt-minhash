from sbt import GraphFactory, Leaf, NodePos

from .conftest import SBTImplementation


def test_simple(SBTImplementation):
    factory = GraphFactory(5, 100, 3)
    root = SBTImplementation(factory)

    leaf1 = Leaf("a", factory())
    leaf1.data.count('AAAAA')
    leaf1.data.count('AAAAT')
    leaf1.data.count('AAAAC')

    leaf2 = Leaf("b", factory())
    leaf2.data.count('AAAAA')
    leaf2.data.count('AAAAT')
    leaf2.data.count('AAAAG')

    leaf3 = Leaf("c", factory())
    leaf3.data.count('AAAAA')
    leaf3.data.count('AAAAT')
    leaf3.data.count('CAAAA')

    leaf4 = Leaf("d", factory())
    leaf4.data.count('AAAAA')
    leaf4.data.count('CAAAA')
    leaf4.data.count('GAAAA')

    leaf5 = Leaf("e", factory())
    leaf5.data.count('AAAAA')
    leaf5.data.count('AAAAT')
    leaf5.data.count('GAAAA')

    root.add_node(leaf1)
    root.add_node(leaf2)
    root.add_node(leaf3)
    root.add_node(leaf4)
    root.add_node(leaf5)

    def search_kmer(obj, seq):
        return obj.data.get(seq)

    leaves = [leaf1, leaf2, leaf3, leaf4, leaf5]
    kmers = ["AAAAA", "AAAAT", "AAAAG", "CAAAA", "GAAAA"]

    def search_kmer_in_list(kmer):
        x = []
        for l in leaves:
            if l.data.get(kmer):
                x.append(l)

        return set(x)

    for kmer in kmers:
        assert set(root.find(search_kmer, kmer)) == search_kmer_in_list(kmer)

    print('-----')
    print([x.metadata for x in root.find(search_kmer, "AAAAA")])
    print([x.metadata for x in root.find(search_kmer, "AAAAT")])
    print([x.metadata for x in root.find(search_kmer, "AAAAG")])
    print([x.metadata for x in root.find(search_kmer, "CAAAA")])
    print([x.metadata for x in root.find(search_kmer, "GAAAA")])


def test_longer_search(SBTImplementation):
    ksize = 5
    factory = GraphFactory(ksize, 100, 3)
    root = SBTImplementation(factory)

    leaf1 = Leaf("a", factory())
    leaf1.data.count('AAAAA')
    leaf1.data.count('AAAAT')
    leaf1.data.count('AAAAC')

    leaf2 = Leaf("b", factory())
    leaf2.data.count('AAAAA')
    leaf2.data.count('AAAAT')
    leaf2.data.count('AAAAG')

    leaf3 = Leaf("c", factory())
    leaf3.data.count('AAAAA')
    leaf3.data.count('AAAAT')
    leaf3.data.count('CAAAA')

    leaf4 = Leaf("d", factory())
    leaf4.data.count('AAAAA')
    leaf4.data.count('CAAAA')
    leaf4.data.count('GAAAA')

    leaf5 = Leaf("e", factory())
    leaf5.data.count('AAAAA')
    leaf5.data.count('AAAAT')
    leaf5.data.count('GAAAA')

    root.add_node(leaf1)
    root.add_node(leaf2)
    root.add_node(leaf3)
    root.add_node(leaf4)
    root.add_node(leaf5)

    def kmers(k, seq):
        for start in range(len(seq) - k + 1):
            yield seq[start:start + k]

    def search_transcript(node, seq, threshold):
        presence = [node.data.get(kmer) for kmer in kmers(ksize, seq)]
        if sum(presence) >= int(threshold * (len(seq) - ksize + 1)):
            return 1
        return 0

    try1 = [x.metadata for x in root.find(search_transcript, "AAAAT", 1.0)]
    assert set(try1) == set(['a', 'b', 'c', 'e']), try1  # no 'd'

    try2 = [x.metadata for x in root.find(search_transcript, "GAAAAAT", 0.6)]
    assert set(try2) == set(['a', 'b', 'c', 'd', 'e'])

    try3 = [x.metadata for x in root.find(search_transcript, "GAAAA", 1.0)]
    assert set(try3) == set(['d', 'e']), try3


def test_child(SBTImplementation):
    tree = SBTImplementation(lambda: True)
    tree.nodes = [True] * 31

    assert tree.children(0) == [NodePos(1, True), NodePos(2, True)]
    assert tree.children(1) == [NodePos(3, True), NodePos(4, True)]

    tree = SBTImplementation(lambda: True, d=5)
    tree.nodes = [True] * 31

    assert tree.children(0) == [NodePos(c, True) for c in range(1, 6)]
    assert tree.children(1) == [NodePos(c, True) for c in range(6, 11)]
