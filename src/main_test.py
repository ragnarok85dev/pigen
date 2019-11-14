from gedcom.gedcom_file import GedcomFile
from genealogy import Genealogy
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import gedcom
import time

def print_gedcom(genealogy, filepath):
    exported_gedcom = genealogy.export_gedcom_file()
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
    input_filepath = "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage.ged"
    parsed_gedcom_file = GedcomFile()
    parsed_gedcom_file.parse_gedcom(input_filepath)
#     output_filepath = "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen.ged"
#     f = open(output_filepath, "w")
#     f.write(parsed_gedcom_file.get_gedcom_repr())
#     f.close()

    g = Genealogy(parsed_gedcom_file)
    print_gedcom(g, "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen.ged")
#     exported_gedcom = g.export_gedcom_file()
#     output_filepath = "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen.ged"
#     f = open(output_filepath, "w")
#     f.write(exported_gedcom.get_gedcom_repr())
#     f.close()

    print ("Sposo/a di " + str(g.get_individual_by_reference("@I20@")) + ":")
    print (g.get_spouse(g.get_individual_by_reference("@I20@"))) # Chiara Ragnini
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
    print("------------")
    
    print ("Nuovo individuo #1: ") # Pinco Pallino, nato il 17-dic-1885, morto il 5-feb-1915
    new_guy = gedcom.structures.Individual("Pinco", "Pallino", "M", "17-dic-1885", "5-feb-1915") 
    ref = g.add_individual(new_guy)
    new_guy_retrieved = g.get_individual_by_reference(ref)
    print (new_guy.get_gedcom_repr(0))
    print ("------------")
    print ("Nuovo individuo #2: ") # Tizia Caia, nato il 18-dic-1885, morto il 6-feb-1915
    new_lady = gedcom.structures.Individual("Tizia", "Caia", "F", "18-dic-1885", "6-feb-1915") 
    ref_l = g.add_individual(new_lady)
    new_lady_retrieved = g.get_individual_by_reference(ref_l)
    print (new_lady_retrieved.get_gedcom_repr(0))
    print ("------------")
    print ("Nuovo individuo #3: ") # Sempronio Pallino, nato il 19-dic-1905, morto il 7-feb-1935
    new_son = gedcom.structures.Individual("Sempronio", "Pallino", "M", "19-dic-1905", "7-feb-1935") 
    ref_s = g.add_individual(new_son)
    new_son_retrieved = g.get_individual_by_reference(ref_s)
    print (new_son_retrieved.get_gedcom_repr(0))
    print ("------------")

    son = g.get_individual_by_reference("@I500335@") # Giancarlo Cassini
    print ("Aggiunta di " + str(new_guy_retrieved) + " come padre di " + str(son)) # Pinco Pallino padre di Giancarlo Cassini
    g.link_individual(new_guy, son, Genealogy.RELATIONSHIP_FATHER)
    print ("Aggiunta di " + str(new_lady_retrieved) + " come madre di " + str(son)) # Tizia Caia madre di Giancarlo Cassini
    g.link_individual(new_lady, son, Genealogy.RELATIONSHIP_MOTHER)
    print ("Aggiunta di " + str(new_lady_retrieved) + " come moglie di " + str(new_guy_retrieved)) # Tizia Caia partner di Pinco Pallino
    g.link_individual(new_lady, new_guy, Genealogy.RELATIONSHIP_PARTNER)
    print ("Aggiunta di " + str(new_son_retrieved) + " come figlio di " + str(new_guy_retrieved)) # Sempronio Pallino figlio di Pinco Pallino
    g.link_individual(new_son_retrieved, new_guy_retrieved, Genealogy.RELATIONSHIP_CHILD)

    print ("Antenati di " + str(g.get_individual_by_reference("@I500335@")) + ":")
    for ancestor in g.get_ancestors(g.get_individual_by_reference("@I500335@")): # Giancarlo Cassini
        print (ancestor)
    print("------------")
    print ("Discendenti di " + str(new_guy_retrieved) + ":")
    for descendant in g.get_descendants(new_guy_retrieved): # Pinco Pallino
        print (descendant)
    print("------------")
    print ("Sposo/a di " + str(new_guy) + ":")
    print (g.get_spouse(new_guy)) # Tizia Caia
    print("------------")
    
    print_gedcom(g, "C:\\Users\\gricca4\\LocalData\\pigen\\example_MyHeritage_pigen_updated.ged")
    
#     people = [g.get_individual_by_reference("@I500008@"), g.get_individual_by_reference("@I20@"), g.get_individual_by_reference("@I500384@"),
#               g.get_individual_by_reference("@I501112@"), g.get_individual_by_reference("@I500001@"), g.get_individual_by_reference("@I22@")]
#     branch = g.get_branch(people)

#     branch = g.get_branch(g.get_ancestors(g.get_individual_by_reference("@I500384@")))
#     branch2 = nx.DiGraph()
#     for u,v,d in branch.edges(data=True):
#         branch2.add_edge(str(u), str(v), relationship=d['relationship'])
# 
#     grafo_figo = Network(height=800, width=800, bgcolor="#222222", font_color='white', directed=True)
#     grafo_figo.barnes_hut()
#     grafo_figo.from_nx(branch2)
#     grafo_figo.show_buttons(filter_=['physics'])
#     grafo_figo.show('test.html')
    
    

if __name__ == '__main__':
    main()