from gedcom.gedcom_file import GedcomFile
from genealogy import Genealogy
import matplotlib.pyplot as plt
import networkx as nx
import ete3
from ete3.treeview.main import TreeStyle
import os
import kanren

def print_gedcom(genealogy, filepath):
    exported_gedcom = genealogy.get_gedcom()
    f = open(filepath, "w")
    f.write(exported_gedcom.get_gedcom_repr())
    f.close()

def plot_tree(graph):
    pos = nx.spring_layout(graph)
    labels = nx.get_edge_attributes(graph,'relationship')
    nx.draw_networkx_nodes(graph, pos, cmap=plt.get_cmap('jet'), node_size = 500)
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color='r', arrows=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()

#     # write dot file to use with graphviz
#     # run "dot -Tpng test.dot >test.png"
#     nx.nx_agraph.write_dot(graph,'test.dot')
#     
#     # same layout using matplotlib with no labels
#     plt.title('draw_networkx')
#     pos = graphviz_layout(graph, prog='dot')
#     nx.draw(graph, pos, with_labels=False, arrows=False)


def main():
#     input_filepath = "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage.ged"
#     parsed_gedcom_file = GedcomFile()
#     parsed_gedcom_file.parse_gedcom(input_filepath)
#     genealogy = Genealogy(parsed_gedcom_file)
#     print_gedcom(genealogy, "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen.ged")
#     
#     new_genealogy = Genealogy(GedcomFile(input_filepath))
#     genealogy.add_disconnected_genealogy(new_genealogy)
#     
#     print_gedcom(genealogy, "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen_updated.ged")  

#     parsed_gedcom_file = GedcomFile("C:\\Users\\gricca4\\LocalData\\pigen\\pigen\\src\\tests\\gedcom_files\\sample_family.ged")
#     genealogy = Genealogy(parsed_gedcom_file)
#     root = genealogy.get_individual_by_ref("@I6@")
#     subtrees = {node:ete3.Tree(name=node) for node in genealogy.G.nodes()}
#     [*map(lambda edge:subtrees[edge[0]].add_child(subtrees[edge[1]]), genealogy.G.edges())]
#     tree = subtrees[root]
#     print(tree)

    genealogy = Genealogy(GedcomFile("C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage.ged"))
    giacomo_ricca = genealogy.get_individual_by_ref("@I500008@")
    gb_ricca = genealogy.get_individual_by_ref("@I500001@")
    giuseppe_ricca = genealogy.get_individual_by_ref("@I500004@")
    giorgio_ricca = genealogy.get_individual_by_ref("@I500003@")
    patric_dolmeta = genealogy.get_individual_by_ref("@I500011@")
    marco_corradi = genealogy.get_individual_by_ref("@I500719@")
    
#     parent = kanren.Relation()
#     partner = kanren.Relation()
#     
#     for (u, v, d) in genealogy.G.edges(data=True):
#         if u and v:
#             if d['relationship'] == Genealogy.RELATIONSHIP_PARENT:
#                 kanren.facts(parent, (u, v))
#             elif d['relationship'] == Genealogy.RELATIONSHIP_PARTNER:
#                 kanren.facts(partner, (u, v))
#                 kanren.facts(partner, (v, u))
# 
#     def grandparent(x, z):
#         y = kanren.var()
#         return kanren.conde((parent(x, y), parent(y, z)))
#     
#     x = kanren.var()
#     solution = kanren.run(1, x, parent(x, giacomo_ricca))
#     for i in solution:
#         print (i)
#     solution = kanren.run(2, x, grandparent(x, giacomo_ricca))
#     for i in solution:
#         print (i)

#     result = genealogy.get_relationship(giorgio_ricca, patric_dolmeta)
#     print (result)
    

#     f = open("C:\\Users\\gricca4\\LocalData\\pigen\\all_trees.txt", "w")
#     for individual in genealogy.individuals.values():
#         print("Printing tree for: " + str(individual))
#         root = genealogy.get_individual_by_ref(individual.reference)
#         subtrees = {node:ete3.Tree(name=node) for node in genealogy.G.nodes()}
#         [*map(lambda edge:subtrees[edge[0]].add_child(subtrees[edge[1]]), genealogy.G.edges())]
#         tree = subtrees[root]
#         f.write('\n')
#         f.write('****************************************************************************************************************************************************************************************')
#         f.write(tree.get_ascii())
#         f.write('****************************************************************************************************************************************************************************************')
#         f.write('\n')
#     f.close()
   
#     root = genealogy.get_individual_by_ref("@I500048@")
#     subtrees = {node:ete3.Tree(name=node) for node in genealogy.get_individuals()}
#     [*map(lambda edge:subtrees[edge[0]].add_child(subtrees[edge[1]]), genealogy.G.edges())]
#     tree = subtrees[root]
#     ts = TreeStyle()
#     ts.show_leaf_name = True
#     ts.mode = "c"
#     ts.arc_start = -180 # 0 degrees = 3 o'clock
#     ts.arc_span = 180
#     tree.show(tree_style=ts)
    
    
#     print_gedcom(g, "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen.ged")

    
    

if __name__ == '__main__':
    main()