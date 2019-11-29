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
    RELATIONSHIP_SIBLING = "4"


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


    def get_individuals(self):
        '''
        Return all the individuals of the genealogy as a list 
        '''
        return self.__individuals.values()
    
    
    def get_families(self):
        '''
        Return all the families of the genealogy as a list 
        '''
        return self.__families.values()


    def import_gedcom_file(self, gedcom_file: GedcomFile):
        '''
        Populates a Genealogy object starting from a GedcomFile
        :param gedcom_file: GedcomFile object
        '''
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
        '''
        Add a new family to the genealogy
        :param new_family: new family to be added
        '''
        new_family.reference = "@F" + str(self.get_next_available_gedcom_id(self.__families.keys())) + "@"
        self.__families[new_family.reference] = new_family
        return new_family.reference
    
    
    def add_individual(self, new_individual):
        '''
        Add a new individual to the genealogy
        :param new_individual: new individual to be added
        '''
        new_individual.reference = "@I" + str(self.get_next_available_gedcom_id(self.__individuals.keys())) + "@"
        self.__individuals[new_individual.reference] = new_individual
        self.__G.add_node(new_individual)
        return new_individual.reference
    
    
    def remove_family(self, family):
        '''
        Removes a family from the genealogy
        :param family: family to be removed
        '''
        if family.reference in self.__families.keys():
            del self.__families[family.reference]
    
    
    def remove_individual(self, individual):
        '''
        Removes an individual from the genealogy
        :param individual: individual to be removed
        '''
        # remove reference from the family having individual as child
        for ctfl in individual.child_to_family_links:
            if ctfl.family_reference in self.__families.keys():
                family = self.__families[ctfl.family_reference]
                family.remove_individual_reference(individual.reference)
        # remove reference from the family having individual as partner
        for stfl in individual.spouse_to_family_links:
            if stfl.family_reference in self.__families.keys():
                family = self.__families[stfl.family_reference]
                family.remove_individual_reference(individual.reference)
                if family.has_no_parents():
                    self.remove_family(family)
        if individual.reference in self.__individuals.keys():
            del self.__individuals[individual.reference]
        if individual.reference in self.__spouses.keys():
            del self.__spouses[individual.reference]
        if individual in self.G:
            self.G.remove_node(individual)

    
    def rename_family_reference(self, old_reference, new_reference):
        '''
        Renames a family reference from old_reference to new_reference in the whole genealogy
        :param old_reference: old/current reference code (e.g. @F12@)
        :param new_reference: new/future reference code (e.g. @F23@)
        '''
        if old_reference in self.__families.keys():
            family = self.__families[old_reference]
            del self.__families[old_reference]
            self.__families[new_reference] = family
            family.reference = new_reference
            for individual in self.__individuals.values():
                for child_link in individual.child_to_family_links:
                    if child_link.family_reference == old_reference:
                        child_link.family_reference = new_reference
                for spouse_link in individual.spouse_to_family_links:
                    if spouse_link.family_reference == old_reference:
                        spouse_link.family_reference = new_reference


    def rename_individual_reference(self, old_reference, new_reference):
        '''
        Renames an individual reference from old_reference to new_reference in the whole genealogy
        :param old_reference: old/current reference code (e.g. @I12@)
        :param new_reference: new/future reference code (e.g. @I23@)
        '''
        if old_reference in self.__individuals.keys():
            individual = self.__individuals[old_reference]
            del self.__individuals[old_reference]
            self.__individuals[new_reference] = individual
            individual.reference = new_reference
            for family in self.__families.values():
                family.husband_reference = new_reference if family.husband_reference == old_reference else family.husband_reference
                family.wife_reference = new_reference if family.wife_reference == old_reference else family.wife_reference
                for child_reference in family.children_references:
                    child_reference = new_reference if child_reference == old_reference else child_reference
            if self.__spouses[old_reference]:
                spouse = self.__spouses[old_reference]
                del self.__spouses[old_reference]
                self.__spouses[new_reference] = spouse
                self.__spouses[spouse.reference] = individual
    
    
    def add_and_link_individual(self, new_individual, existing_individual, relationship):
        '''
        Adds new_individual to the genealogy and links it to existing_individual with relationship
        :param new_individual: new Individual to be added
        :param existing_individual: existing Individual to be linked to
        :param relationship: relationship to be used to link new_individual to existing_individual
        '''
        self.add_individual(new_individual)
        self.link_individual(new_individual, existing_individual, relationship)
    
    
    def create_new_family_with_partners(self, individual_a, individual_b):
        '''
        Creates a new family with individual_a and individual_b as partners (depending on the sex, one is husband, the other is wife)
        :param individual_a: Individual as family partner, either husband or wife
        :param individual_b: Individual as family partner, either husband or wife
        '''
        family = Family()
        family.add_partner_reference(individual_a)
        family.add_partner_reference(individual_b)
        family_reference = self.add_family(family)
        family.reference = family_reference
        individual_a.add_family_reference_as_partner(family_reference)
        individual_b.add_family_reference_as_partner(family_reference)
        return family_reference


    def create_new_family_with_parent_child(self, parent, child):
        '''
        Creates a new family with parent as either husband or wife (depending on sex) and child as
        :param parent: Individual as family partner, either husband or wife
        :param child:Individual as family child
        '''
        family = Family()
        family_reference = self.add_family(family)
        family.reference = family_reference
        self.link_parent_to_existing_family(parent, family_reference)
        self.link_child_to_existing_family(child, family_reference)
        return family_reference


    def link_partner(self, individual_a, individual_b):
        '''
        Links individual_a and individual_b as partners in the same family
        if both invidual_a and individual_b do not have families, then create a new one and add them both
        if individual_a has a family and individual_b not, then:
           if family of invidual_a has partner different from individual_b, then create a new family and add them both
           if family of invidual_a has no partner, then 
               add individual_b to that family
        if both individual_a and individual_b have (different) families, then:
           create a new family and add them both
           if family of individual_a has children and no partner, then 
               move children to new family
               delete that family
           if family of individual_b has children and no partner, then 
               move children to new family
               delete that family
        :param individual_a: Individual as partner
        :param individual_b: Individual as partner
        '''
        if (not individual_a.has_family()) and (not individual_b.has_family()):
            self.create_new_family_with_partners(individual_a, individual_b)
        elif individual_a.has_family() and (not individual_b.has_family()):
            for family in [self.get_family_by_ref(stfl.family_reference) for stfl in individual_a.spouse_to_family_links]:
                family_other_partner = family.get_partner_of(individual_a).reference
                if family_other_partner and family_other_partner != individual_b.reference:
                    self.create_new_family_with_partners(individual_a, individual_b)
                elif not family_other_partner:
                    family.add_partner_reference(individual_b)
                    individual_b.add_family_reference_as_partner(family.reference)
        elif (not individual_a.has_family()) and individual_b.has_family():
            for family in [self.get_family_by_ref(stfl.family_reference) for stfl in individual_b.spouse_to_family_links]:
                family_other_partner = family.get_partner_of(individual_b).reference
                if family_other_partner and family_other_partner != individual_a.reference:
                    self.create_new_family_with_partners(individual_b, individual_a)
                elif not family_other_partner:
                    family.add_partner_reference(individual_a)
                    individual_a.add_family_reference_as_partner(family.reference)
        elif individual_a.has_family() and individual_b.has_family():
            new_family_ref = self.create_new_family_with_partners(individual_a, individual_b)
            new_family = self.get_family_by_ref(new_family_ref)
            for family in [self.get_family_by_ref(stfl.family_reference) for stfl in individual_a.spouse_to_family_links if self.get_family_by_ref(stfl.family_reference).reference != new_family_ref]:
                if family.has_children() and not family.get_partner_of(individual_a):
                    for child in [self.get_individual_by_ref(child_ref) for child_ref in family.children_references]:
                        child.move_family(family.reference, new_family_ref)
                        family.remove_individual_reference(child.reference)
                        new_family.add_child(child)
                    if not family.has_children() and not family.get_partner_of(individual_a):
                        self.remove_family(family)
                        individual_a.remove_family_as_partner(family.reference)
            for family in [self.get_family_by_ref(stfl.family_reference) for stfl in individual_b.spouse_to_family_links if self.get_family_by_ref(stfl.family_reference).reference != new_family_ref]:
                if family.has_children() and not family.get_partner_of(individual_b):
                    for child in [self.get_individual_by_ref(child_ref) for child_ref in family.children_references]:
                        child.move_family(family.reference, new_family_ref)
                        family.remove_individual_reference(child.reference)
                        new_family.add_child(child)
                    if not family.has_children() and not family.get_partner_of(individual_b):
                        self.remove_family(family)
                        individual_b.remove_family_as_partner(family.reference)  
        self.__spouses[individual_a.reference] = individual_b
        self.__spouses[individual_b.reference] = individual_a
    

    def link_child_to_existing_family(self, child, family_reference):
        '''
        Links a child to an existing family
        :param child: Individual as child
        :param family_reference: reference of the family where child will be linked to
        '''
        if not child.reference in [child_ref for child_ref in self.__families[family_reference].children_references]:
            child_to_family_link = ChildToFamilyLink()
            child_to_family_link.family_reference = family_reference
            child.child_to_family_links.append(child_to_family_link)
            self.__families[family_reference].children_references.append(child.reference)
            self.__families[family_reference].number_children += 1
    

    def link_parent_to_existing_family(self, parent, family_reference):
        '''
        Links a parent to an existing family
        :param parent: Individual as a parent, either husband or wife (depending on sex)
        :param family_reference: reference of the family where parent will be linked to
        '''
        spouse_to_family_link = SpouseToFamilyLink()
        spouse_to_family_link.family_reference = family_reference
        if family_reference not in [stfl.family_reference for stfl in parent.spouse_to_family_links]:
            parent.spouse_to_family_links.append(spouse_to_family_link)
        self.__families[family_reference].add_partner_reference(parent)


    def link_child(self, child, parent, family=None):
        '''
        Links a child to a parent, using a specific family if specified
        :param child: Individual as a child
        :param parent: Individual as a parent
        :param family: <optional> parent's family
        '''
        if parent.has_family():
            if family:
                family_reference = family.reference
            else:
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


    def link_siblings(self, individual_a, individual_b, family=None):
        '''
        Links individual_a to individual_b as siblings, , using a specific family if specified
        :param individual_a: Individual to be linked to individual_b
        :param individual_b: Individual who's going to host individual_b as sibling
        :param family: <optional> individual_b's family
        '''
        if not family:
            # if the link is not specified on any family, then it takes the first of individual_b
            family = self.__families[individual_b.child_to_family_links[0].family_reference]
        family.add_child(individual_a)
        self.link_child_to_existing_family(individual_a, family.reference)
        for parent in self.get_parents_of(individual_b):
            if parent.is_male():
                self.G.add_edge(parent, individual_a, relationship = self.RELATIONSHIP_FATHER)
            elif parent.is_female():
                self.G.add_edge(parent, individual_a, relationship = self.RELATIONSHIP_MOTHER)


    def link_individual(self, individual_a, individual_b, new_relationship, family=None):
        '''
        Links individual_a to individual_b with a new relationship, using a specific family
        :param individual_a: Individual to be linked
        :param individual_b: Individual to be linked to
        :param new_relationship: type of relationship
        :param family: <optional> family of individual_b
        '''
        # Links individual_a to individual_b with new_relationship in family
        if individual_a == individual_b:
            return
        if new_relationship == self.RELATIONSHIP_FATHER and self.get_father_of(individual_b):
            # if a father is already present, then return
            return
        elif new_relationship == self.RELATIONSHIP_MOTHER and self.get_mother_of(individual_b):
            # if a mother is already present, then return
            return
        elif new_relationship == self.RELATIONSHIP_PARTNER and self.get_partner_of(individual_b):
            # if the same partner already present as partner, then return
            return
        elif new_relationship == self.RELATIONSHIP_CHILD and individual_a in self.get_children_of(individual_b):
            # if individual_a is already a child of individual_b, then return
            return
        elif new_relationship == self.RELATIONSHIP_SIBLING and self.get_siblings_of(individual_a) == individual_b:
            # if individual_a is already a sibling of individual_b, then return
            return
        if new_relationship in (self.RELATIONSHIP_FATHER, self.RELATIONSHIP_MOTHER):
            self.link_child(individual_b, individual_a, family)
        elif new_relationship == self.RELATIONSHIP_PARTNER:
            self.link_partner(individual_a, individual_b)
        elif new_relationship == self.RELATIONSHIP_CHILD:
            self.link_child(individual_a, individual_b, family)
        elif new_relationship == self.RELATIONSHIP_SIBLING:
            self.link_siblings(individual_a, individual_b, family)
    
    
    def un_link_child(self, child, parent, family=None):
        '''
        Unlinks child from parent, using a specific family
        :param child: Individual to be unlinked as child
        :param parent: Individual whose child is going to be unlinked from
        :param family: <optional> parent's family to be unlinked from
        '''
        if not family:
            family = self.__families[parent.spouse_to_family_links[0].family_reference]
        family.children_references = [child_ref for child_ref in family.children_references if child_ref != child.reference]
        child.child_to_family_links = [child_link for child_link in child.child_to_family_links if child_link.family_reference != family.reference]
        self.__G.remove_edge(parent, child)
    
    
    def un_link_partner(self, individual_a, individual_b, family=None):
        '''
        Unlinks individual_a from individual_b as partners, using a specific family
        :param individual_a: Individual
        :param individual_b: Individual
        :param family: <optional> individual_a's family to be unlinked from
        '''
        # if individual_a has children with individual_b, those remain with individual_b
        if not family:
            family = self.__families[individual_a.spouse_to_family_links[0].family_reference]
        family.remove_individual_reference(individual_a.reference)
        individual_a.spouse_to_family_links  = [spouse_link for spouse_link in individual_a.spouse_to_family_links if spouse_link.family_reference != family.reference]
        del self.__spouses[individual_a.reference]
        del self.__spouses[individual_b.reference]
        
    
    def un_link_siblings(self, individual_a, individual_b):
        '''
        Unlinks individual_a from individual_b as siblings, , using a specific family if specified
        :param individual_a: Individual to be unlinked to individual_b
        :param individual_b: Individual who's going to loose individual_b as sibling
        :param family: <optional> individual_b's family
        '''
        for parent in self.get_parents_of(individual_b):
            self.un_link_child(individual_a, parent)
    
    
    def un_link_individual(self, individual_a, individual_b, relationship, family=None):
        '''
        Unlinks individual_a from individual_b of the existing relationship
        :param individual_a: Individual to be unlinked
        :param individual_b: Individual to be unlinked from
        :param relationship: type of relationship
        :param family: <optional> family of individual_b
        '''
        if individual_a == individual_b:
            return
        if relationship == self.RELATIONSHIP_FATHER and self.get_father_of(individual_b) != individual_a:
            # if individual_a is not father of individual_b then return
            return
        elif relationship == self.RELATIONSHIP_MOTHER and self.get_mother_of(individual_b) != individual_a:
            # if individual_a is not mother of individual_b then return
            return
        elif relationship == self.RELATIONSHIP_PARTNER and self.get_partner_of(individual_b) != individual_a:
            # if individual_a isn not partner of individual_b then return
            return
        elif relationship == self.RELATIONSHIP_CHILD and not (individual_a in self.get_children_of(individual_b)):
            # if individual_a not a child of individual_b then return
            return
        elif relationship == self.RELATIONSHIP_SIBLING and not (individual_b in self.get_siblings_of(individual_a)):
            # if individual_a is not a sibling of individual_b, then return
            return
        if relationship in (self.RELATIONSHIP_FATHER, self.RELATIONSHIP_MOTHER, family):
            self.un_link_child(individual_b, individual_a)
        elif relationship == self.RELATIONSHIP_PARTNER:
            self.un_link_partner(individual_a, individual_b)
        elif relationship == self.RELATIONSHIP_CHILD:
            self.un_link_child(individual_a, individual_b, family)
        elif relationship == self.RELATIONSHIP_SIBLING:
            self.un_link_siblings(individual_a, individual_b)
    
    def get_next_available_gedcom_id(self, records):
        '''
        Returns the first available GEDCOM ID number for a new record
        :param records: genealogy records to be taken into account
        ''' 
        if len(records) == 0:
            return 1
        taken_numbers = [int(re.search(r'\d+', record_id).group()) for record_id in records]
        return next(iter([next_id for next_id in range(taken_numbers[0], taken_numbers[-1]+1) if next_id not in taken_numbers]), taken_numbers[-1]+1)
    
    
    def export_gedcom_file(self) -> GedcomFile:
        '''
        Returns a new GedcomFile starting from this object
        '''
        gedcom_file = GedcomFile()
        gedcom_file.header = Header(__version__, "pigen", "5.5")
        gedcom_file.records = {}
        for records in (self.__individuals, self.__families, self.__notes, self.__sources, self.__objects, self.__repositories): gedcom_file.records.update(records)
        return gedcom_file
    
    
    def get_gedcom(self):
        '''
        Returns the corresponding GedcomFile's GEDCOM representation
        '''
        return self.export_gedcom_file().get_gedcom_repr()


    def get_partner_of(self, individual: Individual) -> Individual:
        '''
        Returns partner of individual
        :param individual: Individual to get partner of
        '''
        return self.__spouses.get(individual.reference)


    def get_individual_by_ref(self, reference: str) -> Individual:
        '''
        Returns the Individual identified by reference
        :param reference: reference of the individual
        '''
        return self.__individuals[reference]


    def get_family_by_ref(self, reference: str) -> Family:
        '''
        Returns the Family identified by reference
        :param reference: reference of the family
        '''
        return self.__families[reference]


    def get_parents_of(self, individual):
        '''
        Returns a list of parents of individual
        :param individual: Individual
        '''
        if individual in self.G:
            return list(self.G.predecessors(individual))


    def get_children_of(self, individual):
        '''
        Returns a list of children of individual
        :param individual: Individual
        '''
        if individual in self.G:
            return list(self.G.successors(individual))


    def get_father_of(self, individual: Individual) -> Individual:
        '''
        Returns the father of individual as Individual, None if not present
        :param individual: Individual
        '''
        if individual in self.G:
            return next((i for i in self.G.predecessors(individual) if i.is_male()), None)


    def get_mother_of(self, individual: Individual) -> Individual:
        '''
        Returns the mother of individual as Individual, None if not present
        :param individual: Individual
        '''
        if individual in self.G:
            return next((i for i in self.G.predecessors(individual) if i.is_female()), None)


    def get_siblings_of(self, individual):
        '''
        Returns a list of siblings of individual
        :param individual: Individual
        '''
        siblings = []
        for parent in self.get_parents_of(individual):
            siblings += self.get_children_of(parent)
        siblings = list(dict.fromkeys(list(siblings)))
        if individual in siblings:
            siblings.remove(individual)
        return siblings


    def get_descendants_of(self, individual):
        '''
        Returns a list of descendants of individual
        :param individual: Individual
        '''
        descendants = []
        if individual in self.G:
            for child in self.get_children_of(individual):
                descendants += [child] + list(self.get_descendants_of(child))
        return descendants


    def get_ancestors_of(self, individual):
        '''
        Returns a list of ancestors of individual
        :param individual: Individual
        '''
        if individual in self.G:
            mother = self.get_mother_of(individual)
            father = self.get_father_of(individual)
            return list(filter(None, [mother, father])) + list(self.get_ancestors_of(mother)) + list(self.get_ancestors_of(father))
        return []


    def get_branch(self, individuals):
        '''
        Returns a subgraph from a list of individuals
        :param individuals: list of Individual belonging to this object
        '''
        return self.G.subgraph(individuals)


    def get_g(self):
        return self.__G
    def set_g(self, value):
        self.__G = value
    def del_g(self):
        del self.__G
    G = property(get_g, set_g, del_g, "Graph containing the individuals of family tree")
