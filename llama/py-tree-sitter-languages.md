```shell
pip install Cython setuptools tree-sitter==0.21.3 wheel
curl -L -o tree-sitter-languages-1.10.2.tar.gz https://github.com/grantjenks/py-tree-sitter-languages/archive/refs/tags/v1.10.2.tar.gz
tar -x -f tree-sitter-languages-1.10.2.tar.gz
cd py-tree-sitter-languages-1.10.2
python build.py
cd ..
pip install -e py-tree-sitter-languages-1.10.2
rm -f tree-sitter-languages-1.10.2.tar.gz
```
