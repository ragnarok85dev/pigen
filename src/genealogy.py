import networkx as nx
from _version import __version__
import gedcom.structures as gd
import gedcom.gedcom_file as gf
from gedcom import structures
import re
import gc
import gedcom.tags
from enum import Enum


class Relationship(Enum):
    PARENT = "0"
    CHILD = "1"
    PARTNER = "2"
    SIBLING = "3"


class RecordType(Enum):
    INDIVIDUALS = "INDIVIDUALS"
    FAMILIES = "FAMILIES"
    NOTES = "NOTES"
    SOURCES = "SOURCES"
    OBJECTS = "MULTIMEDIA"
    REPOSITORIES = "REPOSITORIES"  


class Genealogy(object):
    '''
    The Genealogy object contains all the data of a given genealogy
    
    Attributes
    ----------
    __G : networkx.DiGraph
        Directional graph containing father-to-child and mother-to-child relationships
    __individuals: dict of gedcom.structures.Individual
        Dictionary of individuals, whose keys are the individuals' references
    __families: dict of gedcom.structures.Family
        Dictionary of families, whose keys are the families' references
    __notes: dict of gedcom.structures.Note
        Dictionary of notes, whose keys are the notes' references
    __sources: dict of gedcom.structures.Source
        Dictionary of sources, whose keys are the sources' references
    __multimedia: dict of gedcom.structures.Multimedia
        Dictionary of multimedia objects, whose keys are the multimedia' references
    __repositories: dict of gedcom.structures.Repository
        Dictionary of repositories, whose keys are the repositories' references
    '''

    def __init__(self, input_path = None):
        '''
        Instantiates a Genealogy class, optionally starting from a GedcomFile object
        :param gedcom_file: GedcomFile object created starting from a GEDCOM file
        :type gedcom_file: gedcom.GedcomFile
        '''
        self.__G = nx.DiGraph()
        self.__individuals = {}
        self.__families = {}
        self.__notes = {}
        self.__sources = {}
        self.__multimedia = {}
        self.__repositories = {}
        self.__max_indexes = {RecordType.INDIVIDUALS: 0, 
                              RecordType.FAMILIES: 0, 
                              RecordType.NOTES: 0, 
                              RecordType.SOURCES: 0, 
                              RecordType.OBJECTS: 0, 
                              RecordType.REPOSITORIES: 0}
        if input_path:
            self.import_gedcom_file(input_path)


    def get_individuals_list(self):
        '''
        Return all the individuals of the genealogy as a list 
        '''
        return self.__individuals.values()


    def get_families_list(self):
        '''
        Return all the families of the genealogy as a list 
        '''
        return self.__families.values()


    def import_gedcom_file(self, input_path):
        '''
        It parses a GEDCOM file in input_path and populate header and records 
        GEDCOM version accepted is 5.5.1
        :param input_path: input file path of GEDCOM file (e.g. "C:\\users\\public\\mytree.ged")
        '''
        gedcom_lines_list = []
        with open(input_path, mode='r', encoding='utf-8-sig') as content_file:
            content = content_file.readlines()
        for index, line in enumerate(content):
            if gf.is_valid_gedcom_line(line):
                gedcom_lines_list.append(gf.GedcomLine(line, index))
        # HEADER record is mandatory and must be the first one; however in this implementation the content will be discarded
        parsed_lines = gd.Header().parse_gedcom(gedcom_lines_list)
        for line_zero_index in [line for line in gedcom_lines_list[parsed_lines:] if line.level==0]:
            # Submission record is optional
            if line_zero_index.tag == gedcom.tags.GEDCOM_TAG_INDIVIDUAL:
                record = gd.Individual()
                record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
                self.__individuals[record.reference] = record
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_FAMILY:
                record = gd.Family()
                record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
                self.__families[record.reference] = record
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_OBJECT:
                record = gd.Multimedia()
                record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
                self.__multimedia[record.reference] = record
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_NOTE:
                record = gd.Note()
                record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
                self.__notes[record.reference] = record
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_REPOSITORY:
                record = gd.Repository()
                record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
                self.__repositories[record.reference] = record
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_SOURCE:
                record = gd.Source()
                record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
                self.__sources[record.reference] = record
            # Content of SUBMISSION and SUBMITTER records will be discarded in this implementation
            # Content of user-defined tags will be discarded in this implementation
            elif line_zero_index.tag in (gedcom.tags.GEDCOM_TAG_SUBMITTER, gedcom.tags.GEDCOM_TAG_SUBMISSION) or line_zero_index.is_user_defined_tag():
                continue
            elif line_zero_index.is_last_gedcom_line():
                break
            else:
                break
        for individual in self.__individuals.values():
            self.populate_relationships_graph(individual, self.__individuals, self.__families)


    def link_genealogy(self, new_genealogy, existing_individual, new_genealogy_individual, relationship):
        '''
        Add another genealogy to the existing one, linking the existing_genealogy to new_genealogy_individual, the latter belonging to new_genealogy 
        :param new_genealogy: new genealogy
        :type new_genealogy: Genealogy
        :param existing_individual: individual belonging to current genealogy
        :type existing_individual: Individual
        :param new_genealogy_individual: individual belonging to the new genealogy
        :type new_genealogy_individual: Individual
        :param relationship: relationship linking existing_individual to new new_genealogy_individual
        :type relationship: str
        '''
        if isinstance(new_genealogy, Genealogy) and existing_individual in self.__individuals.values() and new_genealogy_individual in new_genealogy.individuals.values():
            self.add_disconnected_genealogy(new_genealogy)
            self.link_individual(existing_individual, new_genealogy_individual, relationship)


    def add_disconnected_genealogy(self, new_genealogy):
        '''
        Add another disconnected genealogy to the existing one.
        It renames all the reference IDs from the new_genealogy and add records to this Genealogy
        :param new_genealogy: new genealogy
        :type new_genealogy: Genealogy
        '''
        if isinstance(new_genealogy, Genealogy):
            for note in list(new_genealogy.notes.values()):
                new_ref = "@N" + str(self.get_next_available_gedcom_id(self.__notes, RecordType.NOTES)) + "@"
                new_genealogy.rename_note_reference(note.reference, new_ref)
                self.__notes[new_ref] = note
            for source in list(new_genealogy.sources.values()):
                new_ref = "@S" + str(self.get_next_available_gedcom_id(self.__sources, RecordType.SOURCES)) + "@"
                new_genealogy.rename_source_reference(source.reference, new_ref)
                self.__sources[new_ref] = source
            for multimedia in list(new_genealogy.multimedia.values()):
                new_ref = "@O" + str(self.get_next_available_gedcom_id(self.__multimedia, RecordType.OBJECTS)) + "@"
                new_genealogy.rename_multimedia_reference(multimedia.reference, new_ref)
                self.__multimedia[new_ref] = multimedia
            for repository in list(new_genealogy.repositories.values()):
                new_ref = "@R" + str(self.get_next_available_gedcom_id(self.__repositories, RecordType.REPOSITORIES)) + "@"
                new_genealogy.rename_repository_reference(repository.reference, new_ref)
                self.__repositories[new_ref] = repository
            for family in list(new_genealogy.families.values()):
                new_ref = "@F" + str(self.get_next_available_gedcom_id(self.__families, RecordType.FAMILIES)) + "@"
                new_genealogy.rename_family_reference(family.reference, new_ref)
                self.__families[new_ref] = family
            for individual in list(new_genealogy.individuals.values()):
                new_ref = "@I" + str(self.get_next_available_gedcom_id(self.__individuals, RecordType.INDIVIDUALS)) + "@"
                new_genealogy.rename_individual_reference(individual.reference, new_ref)
                self.__individuals[new_ref] = individual                
            for individual in new_genealogy.individuals.values():
                self.populate_relationships_graph(individual, self.__individuals, self.__families)


    def populate_relationships_graph(self, existing_individual, individuals, families):
        '''
        Adds an existing individual to the genealogy
        :param existing_individual: individual already present in the list of individuals but not in the graph
        :type existing_individual: Individual
        :param individuals: all the individuals of the genealogy
        :type individuals: dict of Individual
        :param families: all the families of the genealogy
        :type families: dict of Family
        '''
        self.G.add_node(existing_individual)
        for cfl in existing_individual.child_to_family_links:
            if (families[cfl.family_reference].husband_reference):
                individual_father = individuals[families[cfl.family_reference].husband_reference]
                self.G.add_node(individual_father)
                self.G.add_edge(individual_father, existing_individual, relationship = Relationship.PARENT)
            if (self.__families[cfl.family_reference].wife_reference):
                individual_mother = individuals[families[cfl.family_reference].wife_reference]
                self.G.add_node(individual_mother)
                self.G.add_edge(individual_mother, existing_individual, relationship = Relationship.PARENT)
        for sfl in existing_individual.spouse_to_family_links:
            family = families[sfl.family_reference]
            if family.husband_reference and existing_individual.reference != family.husband_reference:
                spouse = self.get_individual_by_ref(family.husband_reference)
                self.G.add_edge(existing_individual, spouse, relationship = Relationship.PARTNER)
                self.G.add_edge(spouse, existing_individual, relationship = Relationship.PARTNER)


    def add_new_record(self, new_record, records, reference_prefix, record_type):
        '''
        Add a new record to the genealogy
        :param new_record: One of the following: individual, family, note, object/multimedia, repository, source 
        :type new_record: One of the following: Individual, Family, Note, Multimedia, Repository, Source
        :param records: Genealogy dictionary of records
        :type records: Dict
        :param reference_prefix: @I for individual, @F for family, @N for note, @S for source, @O for multimedia, @R for repository
        :type reference_prefix: str
        :param record_type: One of the following: RecordType.INDIVIDUALS, RecordType.FAMILIES, RecordType.OBJECTS, RecordType.NOTES, RecordType.SOURCES, RecordType.REPOSITORIES
        :type record_type: RecordType
        '''
        new_record.reference = reference_prefix + str(self.get_next_available_gedcom_id(records.keys(), record_type)) + "@"
        records[new_record.reference] = new_record
        return new_record.reference


    def add_new_family(self, new_family):
        '''
        Add a new family to the genealogy
        :param new_family: new family to be added
        :type new_family: gedcom.Family
        :return: new family reference
        :rtype: str
        '''
        return self.add_new_record(new_family, self.__families, "@F", RecordType.FAMILIES)


    def add_new_individual(self, new_individual):
        '''
        Add a new individual to the genealogy
        :param new_individual: new individual to be added
        :type new_individual: gedcom.Individual
        :return: new individual reference
        :rtype: str
        '''
        self.__G.add_node(new_individual)
        return self.add_new_record(new_individual, self.__individuals, "@I", RecordType.INDIVIDUALS)


    def add_new_note(self, new_note):
        '''
        Add a new Note to the genealogy
        :param new_note: new note to be added
        :type new_individual: gedcom.Note
        :return: new note reference
        :rtype: str
        '''
        return self.add_new_record(new_note, self.__notes, "@N", RecordType.NOTES)


    def add_new_source(self, new_source):
        '''
        Add a new Source to the genealogy
        :param new_note: new source to be added
        :type new_individual: gedcom.Source
        :return: new source reference
        :rtype: str
        '''
        return self.add_new_record(new_source, self.__sources, "@S", RecordType.SOURCES)


    def add_new_multimedia(self, new_multimedia):
        '''
        Add a new Multimedia to the genealogy
        :param new_note: new multimedia to be added
        :type new_individual: gedcom.Multimedia
        :return: new multimedia reference
        :rtype: str
        '''
        return self.add_new_record(new_multimedia, self.__multimedia, "@M", RecordType.OBJECTS)


    def add_new_repository(self, new_repository):
        '''
        Add a new Repository to the genealogy
        :param new_note: new repository to be added
        :type new_individual: gedcom.Repository
        :return: new repository reference
        :rtype: str
        '''
        return self.add_new_record(new_repository, self.__repositories, "@R", RecordType.REPOSITORIES)


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
        if individual in self.G:
            self.G.remove_node(individual)


    def remove_note(self, note_to_be_removed):
        '''
        Removes a note from the genealogy, including all its references
        :param note: note to be removed
        :type note: Note
        '''
        for record in [record for record in gc.get_objects() if isinstance(record, structures.Record) and hasattr(record, 'notes')]:
            for i, note_structure in enumerate(record.notes):
                if note_structure.reference == note_to_be_removed.reference:
                    del record.notes[i]
        if note_to_be_removed.reference in self.__notes.keys():
            del self.__notes[note_to_be_removed.reference]


    def remove_source(self, source_to_be_removed):
        '''
        Removes a source from the genealogy, including all its references
        :param source: source to be removed
        :type source: Source
        '''
        for record in [record for record in gc.get_objects() if isinstance(record, structures.Record) and hasattr(record, 'sources')]:
            for i, source_citation in enumerate(record.sources):
                if source_citation.reference == source_to_be_removed.reference:
                    del record.sources[i]
        if source_to_be_removed.reference in self.__sources.keys():
            del self.__sources[source_to_be_removed.reference]


    def remove_multimedia(self, multimedia_to_be_removed):
        '''
        Removes a multimedia from the genealogy, including all its references
        :param multimedia: source to be removed
        :type multimedia: Multimedia
        '''
        for record in [record for record in gc.get_objects() if isinstance(record, structures.Record) and hasattr(record, 'multimedia_links')]:
            for i, multimedia_link in enumerate(record.multimedia_links):
                if multimedia_link.reference == multimedia_to_be_removed.reference:
                    del record.multimedia_links[i]
        if multimedia_to_be_removed.reference in self.__multimedia.keys():
            del self.__multimedia[multimedia_to_be_removed.reference]


    def remove_repository(self, repository_to_be_removed):
        '''
        Removes a source from the genealogy, including all its references
        :param source: source to be removed
        :type source: Source
        '''
        for record in [record for record in gc.get_objects() if isinstance(record, structures.Record) and hasattr(record, 'repositories')]:
            for i, repo in enumerate(record.repositories):
                if repo.reference == repository_to_be_removed.reference:
                    del record.repositories[i]
        if repository_to_be_removed.reference in self.__repositories.keys():
            del self.__repositories[repository_to_be_removed.reference]


    def rename_note_reference(self, old_reference, new_reference):
        '''
        Renames a note reference from old_reference to new_reference in the whole genealogy
        :param old_reference: old/current reference code (e.g. @N12@)
        :param new_reference: new/future reference code (e.g. @N23@)
        '''
        if old_reference in self.__notes.keys():
            note = self.__notes[old_reference]
            del self.__notes[old_reference]
            self.__notes[new_reference] = note
            note.reference = new_reference
            for note in [note for note in gc.get_objects() 
                         if (isinstance(note, structures.Note) or isinstance(note, structures.NoteStructure)) 
                         and note.reference == old_reference
                         and note in self.__notes]:
                note.reference = new_reference


    def rename_source_reference(self, old_reference, new_reference):
        '''
        Renames a source reference from old_reference to new_reference in the whole genealogy
        :param old_reference: old/current reference code (e.g. @S12@)
        :param new_reference: new/future reference code (e.g. @S23@)
        '''
        if old_reference in self.__sources.keys():
            source = self.__sources[old_reference]
            del self.__sources[old_reference]
            self.__sources[new_reference] = source
            source.reference = new_reference
            for source in [source for source in gc.get_objects() 
                           if (isinstance(source, structures.Source) or isinstance(source, structures.SourceCitation)) 
                           and source.reference == old_reference
                           and source in self.__sources]:
                source.reference = new_reference


    def rename_multimedia_reference(self, old_reference, new_reference):
        '''
        Renames a MultimediaLink reference from old_reference to new_reference in the whole genealogy
        :param old_reference: old/current reference code (e.g. @M12@)
        :param new_reference: new/future reference code (e.g. @M23@)
        '''
        if old_reference in self.__multimedia.keys():
            multimedia_link = self.__multimedia[old_reference]
            del self.__multimedia[old_reference]
            self.__multimedia[new_reference] = multimedia_link
            multimedia_link.reference = new_reference
            for multimedia_link in [multimedia_link for multimedia_link in gc.get_objects() 
                                    if isinstance(multimedia_link, structures.MultimediaLink) 
                                    and multimedia_link.reference == old_reference
                                    and multimedia_link in self.__multimedia]:
                multimedia_link.reference = new_reference


    def rename_repository_reference(self, old_reference, new_reference):
        '''
        Renames a repository reference from old_reference to new_reference in the whole genealogy
        :param old_reference: old/current reference code (e.g. @R12@)
        :param new_reference: new/future reference code (e.g. @R23@)
        '''
        if old_reference in self.__repositories.keys():
            repository = self.__repositories[old_reference]
            del self.__repositories[old_reference]
            self.__repositories[new_reference] = repository
            repository.reference = new_reference
            for repository in [repository for repository in gc.get_objects() 
                               if isinstance(repository, structures.Repository) 
                               and repository.reference == old_reference
                               and repository in self.__repositories]:
                repository.reference = new_reference


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
                for n, child_reference in enumerate(family.children_references):
                    if child_reference == old_reference:
                        family.children_references[n] = new_reference
    
    
    def add_and_link_individual(self, new_individual, existing_individual, relationship):
        '''
        Adds new_individual to the genealogy and links it to existing_individual with relationship
        :param new_individual: new Individual to be added
        :param existing_individual: existing Individual to be linked to
        :param relationship: relationship to be used to link new_individual to existing_individual
        '''
        self.add_new_individual(new_individual)
        self.link_individual(new_individual, existing_individual, relationship)


    def create_new_family_with_partners(self, individual_a, individual_b):
        '''
        Creates a new family with individual_a and individual_b as partners (depending on the sex, one is husband, the other is wife)
        :param individual_a: Individual as family partner, either husband or wife
        :param individual_b: Individual as family partner, either husband or wife
        '''
        family = gd.Family()
        family.add_partner_reference(individual_a)
        family.add_partner_reference(individual_b)
        family_reference = self.add_new_family(family)
        family.reference = family_reference
        individual_a.add_family_reference_as_partner(family_reference)
        individual_b.add_family_reference_as_partner(family_reference)
        return family_reference
    

    def get_list_of_linking_individuals(self, individual_a, individual_b):
        '''
        Returns a list of people connecting individual_a to individual_b
        :param individual_a: Starting individual
        :type individual_a: Individual
        :param individual_b: Target individual
        :type individual_b: Individual
        '''
        if individual_a == individual_b:
            return [individual_a]
        if nx.has_path(self.G.to_undirected(as_view=True), individual_a, individual_b):
            return nx.shortest_path(self.G.to_undirected(as_view=True), individual_a, individual_b)
        else:
            return []


    def create_new_family_with_parent_child(self, parent, child):
        '''
        Creates a new family with parent as either husband or wife (depending on sex) and child as
        :param parent: Individual as family partner, either husband or wife
        :param child:Individual as family child
        '''
        family = gd.Family()
        family_reference = self.add_new_family(family)
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
        self.G.add_edge(individual_a, individual_b, relationship = Relationship.PARTNER)
        self.G.add_edge(individual_b, individual_a, relationship = Relationship.PARTNER)
    

    def link_child_to_existing_family(self, child, family_reference):
        '''
        Links a child to an existing family
        :param child: Individual as child
        :param family_reference: reference of the family where child will be linked to
        '''
        if not child.reference in [child_ref for child_ref in self.__families[family_reference].children_references]:
            child_to_family_link = gd.ChildToFamilyLink()
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
        spouse_to_family_link = gd.SpouseToFamilyLink()
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
        self.G.add_edge(parent, child, relationship = Relationship.PARENT)
        

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
            self.G.add_edge(parent, individual_a, relationship = Relationship.PARENT)


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
        elif new_relationship == Relationship.PARTNER and self.get_partner_of(individual_b):
            # if the same partner already present as partner, then return
            return
        elif new_relationship == Relationship.CHILD and individual_a in self.get_children_of(individual_b):
            # if individual_a is already a child of individual_b, then return
            return
        elif new_relationship == Relationship.SIBLING and self.get_siblings_of(individual_a) == individual_b:
            # if individual_a is already a sibling of individual_b, then return
            return
        if new_relationship == Relationship.PARENT:
            self.link_child(individual_b, individual_a, family)
        elif new_relationship == Relationship.PARTNER:
            self.link_partner(individual_a, individual_b)
        elif new_relationship == Relationship.CHILD:
            self.link_child(individual_a, individual_b, family)
        elif new_relationship == Relationship.SIBLING:
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
        individual_a.spouse_to_family_links = [spouse_link for spouse_link in individual_a.spouse_to_family_links if spouse_link.family_reference != family.reference]
        self.__G.remove_edge(individual_a, individual_b)
        self.__G.remove_edge(individual_b, individual_a)
        
    
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
        elif relationship == Relationship.PARTNER and self.get_partner_of(individual_b) != individual_a:
            # if individual_a isn not partner of individual_b then return
            return
        elif relationship == Relationship.CHILD and not (individual_a in self.get_children_of(individual_b)):
            # if individual_a not a child of individual_b then return
            return
        elif relationship == Relationship.SIBLING and not (individual_b in self.get_siblings_of(individual_a)):
            # if individual_a is not a sibling of individual_b, then return
            return
        if relationship == Relationship.PARENT:
            self.un_link_child(individual_b, individual_a)
        elif relationship == Relationship.PARTNER:
            self.un_link_partner(individual_a, individual_b)
        elif relationship == Relationship.CHILD:
            self.un_link_child(individual_a, individual_b, family)
        elif relationship == Relationship.SIBLING:
            self.un_link_siblings(individual_a, individual_b)
    
    def get_next_available_gedcom_id(self, records, records_type):
        '''
        Returns the first available GEDCOM ID number for a new record
        :param records: genealogy records to be taken into account
        :param records_type: RecordType
        ''' 
        if len(records) == 0:
            return 1
        if self.__max_indexes[records_type] == 0:
            taken_numbers = [int(re.search(r'\d+', record_id).group()) for record_id in records]
            self.__max_indexes[records_type] = max(taken_numbers)
        self.__max_indexes[records_type] += 1
        return self.__max_indexes[records_type]
    
    
    def get_gedcom(self) -> str:
        '''
        Returns a GEDCOM representation of Genealogy as a string
        '''
        header = gd.Header(__version__, "pigen", "5.5")
        gedcom_repr = header.get_gedcom_repr(0)
        records = {**self.__individuals, **self.__families, **self.__notes, **self.__sources, **self.__multimedia, **self.__repositories}
        for record in (records.values()):
            gedcom_repr = "%s\n%s" % (gedcom_repr, record.get_gedcom_repr(0))
        gedcom_repr = "%s\n0 %s" % (gedcom_repr, gedcom.tags.GEDCOM_TAG_TRAILER)
        return gedcom_repr


    def get_partner_of(self, individual: gd.Individual) -> gd.Individual:
        '''
        Returns partner of individual
        :param individual: Individual to get partner of
        '''
        return next((i for i in self.G.neighbors(individual) if self.G.edges[(individual,i)]['relationship']==Relationship.PARTNER), None)


    def get_individual_by_ref(self, reference: str) -> gd.Individual:
        '''
        Returns the Individual identified by reference
        :param reference: reference of the individual
        '''
        return self.__individuals[reference]


    def get_family_by_ref(self, reference: str) -> gd.Family:
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
            return list((i for i in self.G.predecessors(individual) if self.G.edges[(i, individual)]['relationship'] == Relationship.PARENT))


    def get_children_of(self, individual):
        '''
        Returns a list of children of individual
        :param individual: Individual
        '''
        if individual in self.G:
            return list((i for i in self.G.successors(individual) if self.G.edges[(individual, i)]['relationship'] == Relationship.PARENT))


    def get_father_of(self, individual: gd.Individual) -> gd.Individual:
        '''
        Returns the father of individual as Individual, None if not present
        :param individual: Individual
        '''
        if individual in self.G:
            return next((i for i in self.G.predecessors(individual) if self.G.edges[(i, individual)]['relationship'] == Relationship.PARENT and i.is_male()), None)


    def get_mother_of(self, individual: gd.Individual) -> gd.Individual:
        '''
        Returns the mother of individual as Individual, None if not present
        :param individual: Individual
        '''
        if individual in self.G:
            return next((i for i in self.G.predecessors(individual) if self.G.edges[(i, individual)]['relationship'] == Relationship.PARENT and i.is_female()), None)


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
            return list(dict.fromkeys(list(filter(None, [mother, father])) + list(self.get_ancestors_of(mother)) + list(self.get_ancestors_of(father))))
        return []


    def get_branch(self, individuals):
        '''
        Returns a subgraph from a list of individuals
        :param individuals: list of Individual belonging to this object
        '''
        return self.G.subgraph(individuals)


    def get_g(self):
        return self.__G

    def get_individuals(self):
        return self.__individuals

    def get_families(self):
        return self.__families

    def get_notes(self):
        return self.__notes

    def get_sources(self):
        return self.__sources

    def get_multimedia(self):
        return self.__multimedia

    def get_repositories(self):
        return self.__repositories

    def set_g(self, value):
        self.__G = value

    def set_individuals(self, value):
        self.__individuals = value

    def set_families(self, value):
        self.__families = value

    def set_notes(self, value):
        self.__notes = value

    def set_sources(self, value):
        self.__sources = value

    def set_multimedia(self, value):
        self.__multimedia = value

    def set_repositories(self, value):
        self.__repositories = value

    def del_g(self):
        del self.__G

    def del_individuals(self):
        del self.__individuals

    def del_families(self):
        del self.__families

    def del_notes(self):
        del self.__notes

    def del_sources(self):
        del self.__sources

    def del_multimedia(self):
        del self.__multimedia

    def del_repositories(self):
        del self.__repositories

    G = property(get_g, set_g, del_g, "Directional graph containing father-to-child and mother-to-child relationships")
    individuals = property(get_individuals, set_individuals, del_individuals, "Dictionary of individuals, whose keys are the individuals' references")
    families = property(get_families, set_families, del_families, "Dictionary of families, whose keys are the families' references")
    notes = property(get_notes, set_notes, del_notes, "Dictionary of notes, whose keys are the notes' references")
    sources = property(get_sources, set_sources, del_sources, "Dictionary of sources, whose keys are the sources' references")
    multimedia = property(get_multimedia, set_multimedia, del_multimedia, "Dictionary of multimedia objects, whose keys are the multimedia' references")
    repositories = property(get_repositories, set_repositories, del_repositories, "Dictionary of repositories, whose keys are the repositories' references")
