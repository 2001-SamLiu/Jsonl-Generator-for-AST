import matplotlib.pyplot as plt
from tree_sitter import Language, Parser
from collections import namedtuple
import json
import argparse
Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    [
        'tree-sitter-python',
        'tree-sitter-java',
        'tree-sitter-javascript',
    ]
)
PY_LANGUAGE = Language('build/my-languages.so', 'python')
JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
parser = Parser()

Node = namedtuple('Node', ['type', 'start', 'end', 'id'])


def read_to_ast(filename,language):
    if language=='java':
        parser.set_language(JAVA_LANGUAGE)
    elif language=='python':
        parser.set_language(PY_LANGUAGE)
    elif language=='javascript':
        parser.set_language(JS_LANGUAGE)
    else:
        print("not supporting language")
        return None
    with open(filename, "r") as f:
        data = f.read()
    tree = parser.parse(bytes(data, "utf8"))
    return tree


def save_in_dict(tree, filename):  # use breadth-first search to create the tree
    if tree==None:
        return
    root_node = tree.root_node
    whole_tree = {}
    # child_value={}
    total_node_number = get_total_number(root_node)
    # print(total_node_number)
    root = str(Node(type=root_node.type, start=root_node.start_point,
               end=root_node.end_point, id=0))
    node_list=[]
    relation_matrix=[]
    for row in range(total_node_number):
        relation_matrix.append([])
        for column in range(total_node_number):
            relation_matrix[row].append(0)
    relation_matrix[0][0]=1
    whole_tree[root] ,total_node_number,node_list,relation_matrix= breadth_search(root_node, 0,node_list,relation_matrix)
    plt.matshow(relation_matrix)
    plt.show()
    # print(relation_matrix)
    # print(whole_tree)
    with open("%s" % filename, "w") as f:
        json.dump(whole_tree, f, indent=2)

    # print (root_node.sexp())#need to use sexp to create the tree
def get_total_number(node):
    number=1
    for i in range(len(node.children)):
        number+=get_total_number(node.children[i])
    return number

def breadth_search(node, index,node_list,relation_matrix):
    child_value = {}
    parent_id=index
    node_list.append(node)
    for i in range(len(node.children)):
        # print(node.children[i])
        index += 1
        child_node = (str(Node(
            type=node.children[i].type, start=node.children[i].start_point, end=node.children[i].end_point, id=index)))
        # print("%s,%s"%(parent_id,index))
        relation_matrix[parent_id][index]=1
        relation_matrix[index][index]=1
        relation_matrix[index][parent_id]=1
        child_value[child_node],index, node_list, relation_matrix= breadth_search(node.children[i], index, node_list, relation_matrix)
    return child_value , index, node_list, relation_matrix


if __name__ == '__main__':
    parser_ = argparse.ArgumentParser(description='transform ast to json file')
    parser_.add_argument('--data_dir', type=str, help='txt file directory')
    parser_.add_argument('--save_dir', type=str, help='json file saving directory')
    parser_.add_argument('--language', type=str, help='language you would like to transform')
    args = parser_.parse_args()
    filename = args.data_dir

    tree = read_to_ast(filename,args.language)
    save_in_dict(tree, args.save_dir)
