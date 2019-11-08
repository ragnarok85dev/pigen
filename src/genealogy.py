import networkx as nx
from _version import __version__
from gedcom.structures import Individual, Header
from gedcom.gedcom_file import GedcomFile

class Genealogy(object):
    RELATIONSHIP_FAMILY_MEMBER = "Family member"
    RELATIONSHIP_FATHER = "Father"
    RELATIONSHIP_MOTHER = "Mother"
    RELATIONSHIP_CHILD = "Child"
    RELATIONSHIP_SPOUSE = "Spouse"

    def __init__(self, gedcom_file = None):
        self.__G = nx.DiGraph()
        self.__individuals = {}
        self.__families = {}
        self.__notes = {}
        self.__sources = {}
        self.__objects = {}
        self.__repositories = {}

        self.__spouses = {}
        if gedcom_file:
            self.import_gedcom_file(gedcom_file)

    def import_gedcom_file(self, gedcom_file: GedcomFile):
        self.__individuals = gedcom_file.individuals
        self.__families = gedcom_file.families
        self.__notes = gedcom_file.notes
        self.__sources = gedcom_file.sources
        self.__objects = gedcom_file.objects
        self.__repositories = gedcom_file.repositories
        for key, individual in gedcom_file.individuals.items():
            self.G.add_node(individual)
            if len(individual.child_to_family_links) > 0:
                for cfl in individual.child_to_family_links:
                    if (gedcom_file.families[cfl.family_reference].husband_reference):
                        individual_father = gedcom_file.individuals[gedcom_file.families[cfl.family_reference].husband_reference]
                        self.G.add_node(individual_father)
                        self.G.add_edge(individual_father, individual, relationship = self.RELATIONSHIP_FATHER)
                    if (gedcom_file.families[cfl.family_reference].wife_reference):
                        individual_mother = gedcom_file.individuals[gedcom_file.families[cfl.family_reference].wife_reference]
                        self.G.add_node(individual_mother)
                        self.G.add_edge(individual_mother, individual, relationship = self.RELATIONSHIP_MOTHER)
            if len(individual.spouse_to_family_links) > 0:
                for sfl in individual.spouse_to_family_links:
                    family = gedcom_file.families[sfl.family_reference]
                    if key != family.husband_reference:
                        spouse = self.get_individual_by_reference(family.husband_reference)
                        self.__spouses[key] = spouse
                        self.__spouses[family.husband_reference] = individual

    def export_gedcom_file(self) -> GedcomFile:
        gedcom_file = GedcomFile()
        gedcom_file.header = Header(__version__, "pigen", "5.5")
        gedcom_file.records = {}
        for records in (self.__individuals, self.__families, self.__notes, self.__sources, self.__objects, self.__repositories): gedcom_file.records.update(records)
        return gedcom_file

    def get_spouse(self, individual: Individual) -> Individual:
        return self.__spouses.get(individual.reference)

    def get_individual_by_reference(self, reference: str) -> Individual:
        return self.__individuals[reference]

    def get_parents(self, individual):
        return self.G.predecessors(individual)

    def get_children(self, individual):
        return self.G.successors(individual)

    def get_father(self, individual: Individual) -> Individual:
        try:
            return next((i for i in self.G.predecessors(individual) if i.sex == 'M'), None)
        except:
            return None

    def get_mother(self, individual: Individual) -> Individual:
        try:
            return next((i for i in self.G.predecessors(individual) if i.sex == 'F'), None)
        except:
            return None

    def get_siblings(self, individual):
        siblings = []
        for parent in self.get_parents(individual):
            siblings += self.get_children(parent)
        siblings = list(dict.fromkeys(list(siblings)))
        siblings.remove(individual)
        return siblings

    def get_descendants(self, individual):
        descendants = []
        if individual in self.G:
            for child in self.get_children(individual):
                descendants += [child] + list(self.get_descendants(child))
        return descendants

    def get_ancestors(self, individual):
        if individual in self.G:
            mother = self.get_mother(individual)
            father = self.get_father(individual)
            return list(filter(None, [mother, father])) + list(self.get_ancestors(mother)) + list(self.get_ancestors(father))
        return []

    def get_g(self):
        return self.__G
    def set_g(self, value):
        self.__G = value
    def del_g(self):
        del self.__G
    G = property(get_g, set_g, del_g, "Graph containing the individuals of family tree")
