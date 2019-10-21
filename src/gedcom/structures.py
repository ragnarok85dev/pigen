import gedcom.tags
from abc import abstractclassmethod

def get_relevant_lines(gedcom_lines):
    relevant_lines = []
    if gedcom_lines and len(gedcom_lines)>0:
            element = None
            for line in gedcom_lines[1:]:
                if line.get_level() > gedcom_lines[0].get_level():
                    element = line
                else:
                    break
            if element == None:
                index = 0
            else:
                index = gedcom_lines.index(element)
            relevant_lines = gedcom_lines[:index+1]
    return relevant_lines

class Record():
    def __init__(self, gedcom_lines = None):
        if gedcom_lines:
            self.parse_gedcom(get_relevant_lines(gedcom_lines))
    
    @abstractclassmethod
    def parse_gedcom(self, gedcom_lines):
        pass

class Individual(Record):
    def __init__(self, gedcom_lines = None):
        super().__init__()
        self.__reference = ""
        self.__restriction_notice = ""
        self.__personal_name_structures = []
        self.__sex = ""
        self.__event_structures = []
        self.__attribute_structures = []
        # self.__lds_individual_ordinances = []
        self.__child_to_family_links = []
        self.__spouse_to_family_links= []
        self.__submitter_records = []
        self.__associations_structures = []
        self.__aliases = []
        self.__interest_more_research_ancestors = []
        self.__interest_more_research_descendants = []
        self.__permanent_record_file_number = ""
        self.__ancestral_file_number = ""
        self.__user_reference_numbers = []
        self.__automated_record_id = ""
        self.__change_date = None
        self.__note_structures = []
        self.__source_citations = []
        self.__multimedia_links = []
    
    def parse_gedcom(self, gedcom_lines):
        # assumed that gedcom_lines contains only relevant Individual lines
        self.__reference = gedcom_lines[0].value
        for index, line in enumerate(gedcom_lines):
            if line.tag == gedcom.tags.GEDCOM_TAG_RESTRICTION and (line.level == 1):
                self.__restriction_notice = line.get_value()
#             elif line.tag == gedcom.tags.GEDCOM_TAG_NAME and (line.level == 1):
#                 self.__personal_name_structures.append(PersonalNameStructure(gedcom_lines[index:]))
#             elif line.tag == gedcom.tags.GEDCOM_TAG_SEX and (line.level == 1):
#                 self.__sex = line.get_value()
#             elif line.tag in gedcom.tags.INDIVIDUAL_EVENT_STRUCTURE_TAGS and (line.level == 1):
#                 self.__individual_event_structures.append(IndividualEventStructure(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.INDIVIDUAL_ATTRIBUTE_STRUCTURE_TAGS and (line.level == 1): 
#                 self.__individual_attribute_structures.append(IndividualAttributeStructure(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.GEDCOM_TAG_FAMILY_CHILD and (line.level == 1):
#                 self.__child_to_family_links.append(ChildToFamilyLink(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE and (line.level == 1):
#                 self.__spouse_to_family_links.append(SpouseToFamilyLink(gedcom_lines[index:]))
#             elif line.tag == gedcom.tags.GEDCOM_TAG_SUBMITTER and (line.level == 1):
#                 self.__submitter_records.append(line.get_value())
#             elif line.tag in gedcom.tags.GEDCOM_TAG_ASSOCIATES and (line.level == 1):
#                 self.__associations_structures.append(AssociationStructure(gedcom_lines[index:]))
#             elif line.tag == gedcom.tags.GEDCOM_TAG_ALIAS and (line.level == 1):
#                 self.__aliases.append(line.get_value())
#             elif line.tag == gedcom.tags.GEDCOM_TAG_ANCES_INTEREST and (line.level == 1):
#                 self.__interest_more_research_ancestors.append(line.get_value())
#             elif line.tag == gedcom.tags.GEDCOM_TAG_DESCENDANT_INT and (line.level == 1):
#                 self.__interest_more_research_descendants.append(line.get_value())
#             elif line.tag == gedcom.tags.GEDCOM_TAG_REC_FILE_NUMBER and (line.level == 1):
#                 self.__permanent_record_file_number = line.get_value()
#             elif line.tag == gedcom.tags.GEDCOM_TAG_ANCESTRAL_FILE_NUMBER and (line.level == 1):
#                 self.__ancestral_file_number = line.get_value()
#             elif line.tag == gedcom.tags.GEDCOM_TAG_REFERENCE and (line.level == 1):
#                 if gedcom_lines[index+1].get_tag() == gedcom.tags.GEDCOM_TAG_TYPE:
#                     self.__user_reference_numbers.append((gedcom_lines[index].get_value(), gedcom_lines[index+1].get_value()))
#                 else:
#                     self.__user_reference_numbers.append((gedcom_lines[index].get_value(), ""))
#             elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER and (line.level == 1):
#                 self.__automated_record_id = line.get_value()
#             elif line.tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE and (line.level == 1):
#                 self.__change_date = ChangeDate(gedcom_lines[index:])
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and (line.level == 1):
                self.__note_structures.append(NoteStructure(gedcom_lines[index:]))
#             elif line.tag == gedcom.tags.GEDCOM_TAG_SOURCE and (line.level == 1):
#                 self.__source_citations.append(SourceCitation(gedcom_lines[index:]))
#             elif line.tag == gedcom.tags.GEDCOM_TAG_OBJECT and (line.level == 1):
#                 self.__multimedia_links.append(MultimediaLink(gedcom_lines[index:]))
    
    def get_gedcom_repr(self):
        level = 0
        gedcom_repr = "%s %s %s" % (level, self.__individual_reference, gedcom.tags.GEDCOM_TAG_INDIVIDUAL)
        if self.__restriction_notice:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_RESTRICTION, self.__restriction_notice)
        for personal_name in self.__personal_name_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, personal_name.get_gedcom_repr(level+1))
        if self.__sex:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SEX, self.__sex)
        for individual_event in self.__individual_event_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, individual_event.get_gedcom_repr(level+1))
        for individual_attribute in self.__individual_attribute_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, individual_attribute.get_gedcom_repr(level+1))
        for child_to_family_link in self.__child_to_family_links:
            gedcom_repr = "%s\n%s" % (gedcom_repr, child_to_family_link.get_gedcom_repr(level+1))
        for spouse_to_family_link in self.__spouse_to_family_links:
            gedcom_repr = "%s\n%s" % (gedcom_repr, spouse_to_family_link.get_gedcom_repr(level+1))
        for submitter_records in self.__submitter_records:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SUBMITTER, submitter_records)
        for association_structure in self.__associations_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, association_structure.get_gedcom_repr(level+1))
        for alias in self.__aliases:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_ALIAS, alias)
        for int_ances in self.__interest_more_research_ancestors:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_ANCES_INTEREST, int_ances)
        for int_desc in self.__interest_more_research_descendants:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_DESCENDANT_INT, int_desc)
        if self.__permanent_record_file_number:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REC_FILE_NUMBER, self.__permanent_record_file_number)
        if self.__ancestral_file_number:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_ANCESTRAL_FILE_NUMBER, self.__ancestral_file_number)
        for user_reference_number in self.__user_reference_numbers:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REFERENCE, user_reference_number[0])
            if user_reference_number[1]:
                gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_TYPE, user_reference_number[1])
        if self.__automated_record_id:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER, self.__automated_record_id)
        if self.__change_date:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__change_date.get_gedcom_repr(level+1))
        for note_structure in self.__note_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note_structure.get_gedcom_repr(level+1))
        for source_citation in self.__source_citations:
            gedcom_repr = "%s\n%s" % (gedcom_repr, source_citation.get_gedcom_repr(level+1))
        for multimedia_link in self.__multimedia_links:
            gedcom_repr = "%s\n%s" % (gedcom_repr, multimedia_link.get_gedcom_repr(level+1))    
        return gedcom_repr    

# Substructures
class NoteStructure(Record):
    def __init__(self, gedcom_lines):
        super().__init__(gedcom_lines)
        self.__reference = ""
        self.__text = ""
        if "@" in self._relevant_lines[0].get_value():
            self.__reference = self._relevant_lines[0].get_value()
        else:
            for line in self._relevant_lines:
                if line.get_tag() == gedcom.tags.GEDCOM_TAG_CONTINUED:
                    self.__text += "\n" + line.get_value()
                else:
                    self.__text += line.get_value()

    def get_gedcom_repr(self, level):
        if self.__reference:
            return "%s %s %s" % (level, gedcom.tags.GEDCOM_TAG_NOTE, self.__reference)
        else:
            return gedcom.gedcom_file.split_text_for_gedcom(self.__text, gedcom.tags.GEDCOM_TAG_NOTE, level, gedcom.tags.MAX_TEXT_LENGTH)