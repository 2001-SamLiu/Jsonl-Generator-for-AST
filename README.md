# Transform_AST_to_JSON

This repository provides program for transforming AST to JSON file.

## Prerequisite

To use the program, you are required to install some needed libraries.

```
pip3 install tree_sitter
git clone https://github.com/tree-sitter/tree-sitter-javascript
git clone https://github.com/tree-sitter/tree-sitter-java
git clone https://github.com/tree-sitter/tree-sitter-python
```

Besides, you need to save your code in a txt file that is more convenient for input.

## Usage

To run this program, here is the usage.

```
python3 transform_ast_to_json.py --data_dir (txt file that you want to transform) --save_dir (the place you want to save the json file) --language (your code's language)
e.g. python3 transform_ast_to_json.py --data_dir test_py.txt --save_dir test_py.json --language python
```

The program currently supports python, java, and javascript. If you want to transform other languages, you may need to git clone the library you need and edit the source code of the program. 