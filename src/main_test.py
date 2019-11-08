from gedcom.gedcom_file import GedcomFile
from genealogy import Genealogy
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


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
    input_filepath = "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage.ged"
    parsed_gedcom_file = GedcomFile()
    parsed_gedcom_file.parse_gedcom(input_filepath)
#     output_filepath = "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen.ged"
#     f = open(output_filepath, "w")
#     f.write(parsed_gedcom_file.get_gedcom_repr())
#     f.close()

    g = Genealogy(parsed_gedcom_file)
#     exported_gedcom = g.export_gedcom_file()
#     output_filepath = "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen.ged"
#     f = open(output_filepath, "w")
#     f.write(exported_gedcom.get_gedcom_repr())
#     f.close()

    print ("Sposo/a di " + str(g.get_individual_by_reference("@I500048@")) + ":")
    print (g.get_spouse(g.get_individual_by_reference("@I500048@"))) # Maria Musizzano
    print("------------")

    print ("Padre di " + str(g.get_individual_by_reference("@I500384@")) + ":")
    print (g.get_father(g.get_individual_by_reference("@I500384@"))) # Alessandro Ricca
    print("------------")
      
    print ("Madre di " + str(g.get_individual_by_reference("@I500384@")) + ":")
    print (g.get_mother(g.get_individual_by_reference("@I500384@"))) # Alessandro Ricca
    print("------------")
      
    print ("Fratelli/sorelle di " + str(g.get_individual_by_reference("@I500384@")) + ":")
    for sibling in g.get_siblings(g.get_individual_by_reference("@I500384@")): # Alessandro Ricca
        print (sibling)
    print("------------")
      
    print ("Figli di " + str(g.get_individual_by_reference("@I500048@")) + ":")
    for child in g.get_children(g.get_individual_by_reference("@I500048@")): # Lorenzo Tagliatore
        print (child)
    print("------------")
      
    print ("Genitori di " + str(g.get_individual_by_reference("@I500048@")) + ":")
    for parent in g.get_parents(g.get_individual_by_reference("@I500048@")): # Lorenzo Tagliatore
        print (parent)
    print("------------")
      
    print ("Antenati di " + str(g.get_individual_by_reference("@I500048@")) + ":")
    for ancestor in g.get_ancestors(g.get_individual_by_reference("@I500048@")): # Lorenzo Tagliatore
        print (ancestor)
    print("------------")
       
    print ("Discendenti di " + str(g.get_individual_by_reference("@I500048@")) + ":")
    for descendant in g.get_descendants(g.get_individual_by_reference("@I500048@")): # Lorenzo Tagliatore
        print (descendant)
    descendants = g.G.subgraph(g.get_descendants(g.get_individual_by_reference("@I500048@")))
    print("------------")
    plot_tree(descendants)
    

if __name__ == '__main__':
    main()