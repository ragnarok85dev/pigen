import networkx as nx
from _version import __version__
from gedcom.structures import Individual, Header, Family, ChildToFamilyLink,\
    SpouseToFamilyLink
from gedcom.gedcom_file import GedcomFile
import re

class Genealogy(object):
    RELATIONSHIP_FATHER = "0"
    RELATIONSHIP_MOTHER = "1"
    RELATIONSHIP_CHILD = "2"
    RELATIONSHIP_PARTNER = "3"

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
                        spouse = self.get_individual_by_ref(family.husband_reference)
                        self.__spouses[key] = spouse
                        self.__spouses[family.husband_reference] = individual


    def add_family(self, new_family):
        new_family.reference = "@F" + str(self.get_next_available_gedcom_id(self.__families.keys())) + "@"
        self.__families[new_family.reference] = new_family
        return new_family.reference
    
    def add_individual(self, new_individual):
        new_individual.reference = "@I" + str(self.get_next_available_gedcom_id(self.__individuals.keys())) + "@"
        self.__individuals[new_individual.reference] = new_individual
        self.__G.add_node(new_individual)
        return new_individual.reference
    
    def remove_family(self, family):
        if family.reference in self.__families.keys():
            del self.__families[family.reference]
    
    def remove_individual(self, individual):
        # remove reference from the family having individual as child
        for ctfl in individual.child_to_family_links:
            family = self.__families[ctfl.family_reference]
            family.remove_individual_reference(individual.reference)
        # remove reference from the family having individual as partner
        for stfl in individual.spouse_to_family_links:
            family = self.__families[stfl.family_reference]
            family.remove_individual_reference(individual.reference)
            if family.is_empty():
                self.remove_family(family)
        if individual.reference in self.__individuals.keys():
            del self.__individuals[individual.reference]
        if individual.reference in self.__spouses.keys():
            del self.__spouses[individual.reference]
        if individual in self.G:
            self.G.remove_node(individual)
    
    def add_and_link_individual(self, new_individual, existing_individual, relationship):
        self.add_individual(new_individual)
        self.link_individual(new_individual, existing_individual, relationship)
    
    def create_new_family_with_partners(self, individual_a, individual_b):
        family = Family()
        family.add_partner_reference(individual_a)
        family.add_partner_reference(individual_b)
        family_reference = self.add_family(family)
        family.reference = family_reference
        individual_a.add_family_reference_as_partner(family_reference)
        individual_b.add_family_reference_as_partner(family_reference)
        return family_reference

    def create_new_family_with_parent_child(self, parent, child):
        family = Family()
        family_reference = self.add_family(family)
        family.reference = family_reference
        self.link_parent_to_existing_family(parent, family_reference)
        self.link_child_to_existing_family(child, family_reference)
        return family_reference

    def link_partner(self, individual_a, individual_b):
        # if both invidual_a and individual_b do not have families, then create a new one and add them both
        # if individual_a has a family and individual_b not, then:
        #    if family of invidual_a has partner different from individual_b, then create a new family and add them both
        #    if family of invidual_a has no partner, then 
        #        add individual_b to that family
        # if both individual_a and individual_b have (different) families, then:
        #    create a new family and add them both
        #    if family of individual_a has children and no partner, then 
        #        move children to new family
        #        delete that family
        #    if family of individual_b has children and no partner, then 
        #        move children to new family
        #        delete that family
        if (not individual_a.has_family()) and (not individual_b.has_family()):
            self.create_new_family_with_partners(individual_a, individual_b)
        elif individual_a.has_family() and (not individual_b.has_family()):
            for family in [self.get_family_by_ref(stfl.family_reference) for stfl in individual_a.spouse_to_family_links]:
                family_other_partner = family.get_partner(individual_a).reference
                if family_other_partner and family_other_partner != individual_b.reference:
                    self.create_new_family_with_partners(individual_a, individual_b)
                elif not family_other_partner:
                    family.add_partner_reference(individual_b)
                    individual_b.add_family_reference_as_partner(family.reference)
        elif (not individual_a.has_family()) and individual_b.has_family():
            for family in [self.get_family_by_ref(stfl.family_reference) for stfl in individual_b.spouse_to_family_links]:
                family_other_partner = family.get_partner(individual_b).reference
                if family_other_partner and family_other_partner != individual_a.reference:
                    self.create_new_family_with_partners(individual_b, individual_a)
                elif not family_other_partner:
                    family.add_partner_reference(individual_a)
                    individual_a.add_family_reference_as_partner(family.reference)
        elif individual_a.has_family() and individual_b.has_family():
            new_family_ref = self.create_new_family_with_partners(individual_a, individual_b)
            new_family = self.get_family_by_ref(new_family_ref)
            for family in [self.get_family_by_ref(stfl.family_reference) for stfl in individual_a.spouse_to_family_links if self.get_family_by_ref(stfl.family_reference).reference != new_family_ref]:
                if family.has_children() and not family.get_partner(individual_a):
                    for child in [self.get_individual_by_ref(child_ref) for child_ref in family.children_references]:
                        child.move_family(family.reference, new_family_ref)
                        family.remove_individual_reference(child.reference)
                        new_family.add_child(child)
                    if not family.has_children() and not family.get_partner(individual_a):
                        self.remove_family(family)
                        individual_a.remove_family_as_partner(family.reference)
            for family in [self.get_family_by_ref(stfl.family_reference) for stfl in individual_b.spouse_to_family_links if self.get_family_by_ref(stfl.family_reference).reference != new_family_ref]:
                if family.has_children() and not family.get_partner(individual_b):
                    for child in [self.get_individual_by_ref(child_ref) for child_ref in family.children_references]:
                        child.move_family(family.reference, new_family_ref)
                        family.remove_individual_reference(child.reference)
                        new_family.add_child(child)
                    if not family.has_children() and not family.get_partner(individual_b):
                        self.remove_family(family)
                        individual_b.remove_family_as_partner(family.reference)  
        self.__spouses[individual_a.reference] = individual_b
        self.__spouses[individual_b.reference] = individual_a
    
    def link_child_to_existing_family(self, child, family_reference):
        child_to_family_link = ChildToFamilyLink()
        child_to_family_link.family_reference = family_reference
        child.child_to_family_links.append(child_to_family_link)
        self.__families[family_reference].children_references.append(child.reference)
        self.__families[family_reference].number_children += 1
    
    def link_parent_to_existing_family(self, parent, family_reference):
        spouse_to_family_link = SpouseToFamilyLink()
        spouse_to_family_link.family_reference = family_reference
        if family_reference not in [stfl.family_reference for stfl in parent.spouse_to_family_links]:
            parent.spouse_to_family_links.append(spouse_to_family_link)
        self.__families[family_reference].add_partner_reference(parent)

    def link_child(self, child, parent):
        if parent.has_family():
            family_reference = parent.spouse_to_family_links[0].family_reference
            # this spouse_to_family_links[0] is an assumption
            self.link_child_to_existing_family(child, family_reference)
        else:
            # create a new family and add it to the parent
            self.create_new_family_with_parent_child(parent, child)
        if parent.is_male():
            self.G.add_edge(parent, child, relationship = self.RELATIONSHIP_FATHER)
        elif parent.is_female():
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
    
    def get_next_available_gedcom_id(self, records):
        # returns the first available GEDCOM ID number for a new record
        # TODO: optimize get_next_available_gedcom_id, very slow
        if len(records) == 0:
            return 1
        numbers = [int(re.search(r'\d+', record_id).group()) for record_id in records]
        return next(iter([next_id for next_id in range(numbers[0], numbers[-1]+1) if next_id not in numbers]), numbers[-1]+1)
    
    def export_gedcom_file(self) -> GedcomFile:
        gedcom_file = GedcomFile()
        gedcom_file.header = Header(__version__, "pigen", "5.5")
        gedcom_file.records = {}
        for records in (self.__individuals, self.__families, self.__notes, self.__sources, self.__objects, self.__repositories): gedcom_file.records.update(records)
        return gedcom_file

    def get_spouse(self, individual: Individual) -> Individual:
        return self.__spouses.get(individual.reference)

    def get_individual_by_ref(self, reference: str) -> Individual:
        return self.__individuals[reference]

    def get_family_by_ref(self, reference: str) -> Family:
        return self.__families[reference]

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
