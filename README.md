# Sequence Bloom Trees meet MinHashes!

This repository has the initial exploration for using [MinHashes][1] as leaves
in a [Sequence Bloom Tree][2].
You can check the [notebook][3] describing the features,
but nowadays this code lives in the [sourmash module][4].

C. Titus Brown is also writing blog posts about using this for indexing
genomic data and searching it efficiently, check it out:

- http://ivory.idyll.org/blog/2016-sourmash-sbt.html
- http://ivory.idyll.org/blog/2016-sourmash-sbt-more.html

[1]: http://mash.readthedocs.io/en/latest/
[2]: https://www.cs.cmu.edu/~ckingsf/software/bloomtree/
[3]: notebooks/SBT%20with%20MinHash%20leaves.ipynb
[4]: http://sourmash.readthedocs.io/en/latest/
