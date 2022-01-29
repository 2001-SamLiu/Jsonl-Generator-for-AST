from genericpath import exists
import imp
import matplotlib.pyplot as plt
from tree_sitter import Language, Parser
from collections import namedtuple
import json
import argparse
import os
import jsonlines
import numpy as np
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


def get_dict(tree,saving_matrix,saving_dir,filename):  # use breadth-first search to create the tree
    if tree==None:
        return
    root_node = tree.root_node
    whole_tree = {}
    # child_value={}
    total_node_number = get_total_number(root_node)
    # print(total_node_number)
    root = str(Node(type=root_node.type, start=root_node.start_point,
               end=root_node.end_point, id=0))
    relation_matrix=[]
    if(saving_matrix):
        for row in range(total_node_number):
            relation_matrix.append([])
            for column in range(total_node_number):
                relation_matrix[row].append(0)
        relation_matrix[0][0]=1
    whole_tree[root] ,total_node_number,relation_matrix,saving_matrix= breadth_search(root_node, 0,relation_matrix,saving_matrix)
    print (relation_matrix)
    if(saving_matrix):
        matrix=np.array(relation_matrix)
        if not os.path.exists('%s/matrix'%(saving_dir)):
            os.mkdir('%s/matrix'%(saving_dir))
        filename=filename.split('.')[0]
        np.save('%s/matrix/%s'%(saving_dir,filename),matrix)
    # plt.matshow(relation_matrix)
    # plt.show()
    # with open("%s" % filename, "w") as f:
    #     json.dump(whole_tree, f, indent=2)
    return whole_tree

    # print (root_node.sexp())#need to use sexp to create the tree
def get_total_number(node):
    number=1
    for i in range(len(node.children)):
        number+=get_total_number(node.children[i])
    return number

def breadth_search(node, index,relation_matrix,saving_matrix):
    child_value = {}
    parent_id=index
    for i in range(len(node.children)):
        # print(node.children[i])
        index += 1
        child_node = (str(Node(
            type=node.children[i].type, start=node.children[i].start_point, end=node.children[i].end_point, id=index)))
        # print("%s,%s"%(parent_id,index))
        if saving_matrix:
            relation_matrix[parent_id][index]=1
            relation_matrix[index][index]=1
            relation_matrix[index][parent_id]=1 
        child_value[child_node],index, relation_matrix,saving_matrix= breadth_search(node.children[i], index, relation_matrix,saving_matrix)
    return child_value , index,  relation_matrix, saving_matrix


if __name__ == '__main__':
    parser_ = argparse.ArgumentParser(description='transform ast to json file')
    parser_.add_argument('--data_dir', type=str, help='txt file directory')
    parser_.add_argument('--save_dir', type=str, help='json file saving directory')
    parser_.add_argument('--language', type=str, help='language you would like to transform')
    parser_.add_argument('--saving_matrix', type=bool, help='to decide whether you want to generate adjacent matrix')
    args = parser_.parse_args()
    txt_dir = args.data_dir
    txt_file=sorted(os.listdir('%s' % (txt_dir)))
    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)
    jsonl_file=jsonlines.open('%s/saving.jsonl'%(args.save_dir),"w")
    for i, item in enumerate(txt_file):
        tree = read_to_ast('%s/%s'%(txt_dir,item),args.language)
        tree_dict=get_dict(tree,args.saving_matrix,args.save_dir,item)
        jsonlines.Writer.write(jsonl_file,tree_dict)
