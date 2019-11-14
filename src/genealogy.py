import networkx as nx
from _version import __version__
from gedcom.structures import Individual, Header, Family, ChildToFamilyLink,\
    SpouseToFamilyLink
from gedcom.gedcom_file import GedcomFile
import re

class Genealogy(object):
    RELATIONSHIP_FATHER = "Father"
    RELATIONSHIP_MOTHER = "Mother"
    RELATIONSHIP_PARTNER = "Partner"
    RELATIONSHIP_CHILD = "Child"

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

    def add_and_link_individual(self, new_individual, existing_individual, relationship):
        self.add_individual(new_individual)
        self.link_individual(new_individual, existing_individual, relationship)
    
    def link_partner(self, individual_a, individual_b):
        if self.individual_has_family(individual_b):
                family = individual_b.spouse_to_family_links[0]
                # this spouse_to_family_links[0] is an assumption
                if (family.husband_reference and individual_a.sex == "M") or (family.wife_reference and individual_a.sex == "F"):
                    # if this family has already a partner different from individual_a then a new family has to be created
                    family = Family()
                    if individual_a.sex == "M":
                        family.husband_reference = individual_a.reference
                        family.wife_reference = individual_b.reference
                    elif individual_a.sex == "F":
                        family.wife_reference = individual_a.reference
                        family.husband_reference = individual_b.reference
                    family_reference = self.add_family(family)
                else:
                    family_reference = family.reference
                # link individual_a to the family (either new or already existing)
                spouse_to_family_link = SpouseToFamilyLink()
                spouse_to_family_link.family_reference = family_reference
                individual_a.spouse_to_family_links.append(spouse_to_family_link)
        self.__spouses[individual_a.reference] = individual_b
        self.__spouses[individual_b.reference] = individual_a
    
    def individual_has_family(self, individual):
        return len(individual.spouse_to_family_links) > 0
    
    def link_child_to_existing_family(self, child, family_reference):
        child_to_family_link = ChildToFamilyLink()
        child_to_family_link.family_reference = family_reference
        child.child_to_family_links.append(child_to_family_link)
        self.__families[family_reference].children_references.append(child.reference)
        self.__families[family_reference].number_children += 1

    def link_child(self, child, parent):
        if self.individual_has_family(parent):
            family_reference = parent.spouse_to_family_links[0].family_reference
            # this spouse_to_family_links[0] is an assumption
        else:
            # create a new family
            family = Family()
            family_reference = self.add_family(family)
            family.reference = family_reference
        self.link_child_to_existing_family(child, family_reference)
        if parent.sex == "M":
            self.G.add_edge(parent, child, relationship = self.RELATIONSHIP_FATHER)
        elif parent.sex == "F":
            self.G.add_edge(parent, child, relationship = self.RELATIONSHIP_MOTHER)
    
    def link_individual(self, individual_a, individual_b, new_relationship):
        # Links individual_a to individual_b with new_relationship
        if new_relationship == self.RELATIONSHIP_FATHER and self.get_father(individual_b):
            # if a father is already present, then return
            return
        elif new_relationship == self.RELATIONSHIP_MOTHER and self.get_mother(individual_b):
            # if a mother is already present, then return
            return
        elif new_relationship == self.RELATIONSHIP_PARTNER and self.get_spouse(individual_b):
            # if the same partner already present as partner, then return
            return
        elif new_relationship == self.RELATIONSHIP_CHILD and individual_a in self.get_children(individual_b):
            # if individual_a is already a child of individual_b, then return
            return
            
        if new_relationship in (self.RELATIONSHIP_FATHER, self.RELATIONSHIP_MOTHER):
            self.link_child(individual_b, individual_a)
        elif new_relationship == self.RELATIONSHIP_PARTNER:
            self.link_partner(individual_a, individual_b)
        elif new_relationship == self.RELATIONSHIP_CHILD:
            self.link_child(individual_a, individual_b)
    
    def add_family(self, new_family):
        new_family.reference = "@F" + str(self.get_next_available_gedcom_id(self.__families)) + "@"
        self.__families[new_family.reference] = new_family
        return new_family.reference
    
    def add_individual(self, new_individual):
        new_individual.reference = "@I" + str(self.get_next_available_gedcom_id(self.__individuals)) + "@"
        self.__individuals[new_individual.reference] = new_individual
        self.__G.add_node(new_individual)
        return new_individual.reference
    
    def get_next_available_gedcom_id(self, records):
        # returns the first available GEDCOM ID number for a new record
        # TODO: optimize get_next_available_gedcom_id, very slow
        numbers = [int(re.search(r'\d+', record_id).group()) for record_id in records]
        return next(iter([next_id for next_id in range(numbers[0], numbers[-1]+1) if next_id not in numbers]), numbers[-1]+2)
    
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

    def get_branch(self, individuals):
        return self.G.subgraph(individuals)
        
    def get_g(self):
        return self.__G
    def set_g(self, value):
        self.__G = value
    def del_g(self):
        del self.__G
    G = property(get_g, set_g, del_g, "Graph containing the individuals of family tree")
