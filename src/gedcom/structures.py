import gedcom.tags
from abc import abstractclassmethod
from gedcom.gedcom_file import split_text_for_gedcom

class Record():
    def __init__(self):
        pass
    
    def get_relevant_lines(self, gedcom_lines):
        # TODO: restructur into a more pythonic fashion
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
    
    @abstractclassmethod
    def parse_gedcom(self, gedcom_lines):
        pass 
    
    @abstractclassmethod
    def get_gedcom_repr(self, level):
        pass

class Individual(Record):
    def __init__(self):
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
        super().__init__()
    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        for index, line in enumerate(relevant_lines):
            if line.tag == gedcom.tags.GEDCOM_TAG_RESTRICTION and (line.level == 1):
                self.__restriction_notice = line.get_value()
            elif line.tag == gedcom.tags.GEDCOM_TAG_NAME and (line.level == 1):
                self.__personal_name_structures.append(PersonalNameStructure(gedcom_lines[index:]))
            elif line.tag == gedcom.tags.GEDCOM_TAG_SEX and (line.level == 1):
                self.__sex = line.get_value()
#             elif line.tag in gedcom.tags.INDIVIDUAL_EVENT_STRUCTURE_TAGS and (line.level == 1):
#                 self.__individual_event_structures.append(IndividualEventStructure(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.INDIVIDUAL_ATTRIBUTE_STRUCTURE_TAGS and (line.level == 1): 
#                 self.__individual_attribute_structures.append(IndividualAttributeStructure(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.GEDCOM_TAG_FAMILY_CHILD and (line.level == 1):
#                 self.__child_to_family_links.append(ChildToFamilyLink(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE and (line.level == 1):
#                 self.__spouse_to_family_links.append(SpouseToFamilyLink(gedcom_lines[index:]))
            elif line.tag == gedcom.tags.GEDCOM_TAG_SUBMITTER and (line.level == 1):
                self.__submitter_records.append(line.get_value())
#             elif line.tag in gedcom.tags.GEDCOM_TAG_ASSOCIATES and (line.level == 1):
#                 self.__associations_structures.append(AssociationStructure(gedcom_lines[index:]))
            elif line.tag == gedcom.tags.GEDCOM_TAG_ALIAS and (line.level == 1):
                self.__aliases.append(line.get_value())
            elif line.tag == gedcom.tags.GEDCOM_TAG_ANCES_INTEREST and (line.level == 1):
                self.__interest_more_research_ancestors.append(line.get_value())
            elif line.tag == gedcom.tags.GEDCOM_TAG_DESCENDANT_INT and (line.level == 1):
                self.__interest_more_research_descendants.append(line.get_value())
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_FILE_NUMBER and (line.level == 1):
                self.__permanent_record_file_number = line.get_value()
            elif line.tag == gedcom.tags.GEDCOM_TAG_ANCESTRAL_FILE_NUMBER and (line.level == 1):
                self.__ancestral_file_number = line.get_value()
            elif line.tag == gedcom.tags.GEDCOM_TAG_REFERENCE and (line.level == 1):
                if gedcom_lines[index+1].get_tag() == gedcom.tags.GEDCOM_TAG_TYPE:
                    self.__user_reference_numbers.append((gedcom_lines[index].get_value(), gedcom_lines[index+1].get_value()))
                else:
                    self.__user_reference_numbers.append((gedcom_lines[index].get_value(), ""))
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER and (line.level == 1):
                self.__automated_record_id = line.get_value()
#             elif line.tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE and (line.level == 1):
#                 self.__change_date = ChangeDate(gedcom_lines[index:])
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and (line.level == 1):
                self.__note_structures.append(NoteStructure(gedcom_lines[index:]))
            elif line.tag == gedcom.tags.GEDCOM_TAG_SOURCE and (line.level == 1):
                self.__source_citations.append(SourceCitation(gedcom_lines[index:]))
            elif line.tag == gedcom.tags.GEDCOM_TAG_OBJECT and (line.level == 1):
                self.__multimedia_links.append(MultimediaLink(gedcom_lines[index:]))
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level=0):
        gedcom_repr = "%s %s %s" % (level, self.__reference, gedcom.tags.GEDCOM_TAG_INDIVIDUAL)
        if self.__restriction_notice:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_RESTRICTION, self.__restriction_notice)
        for personal_name in self.__personal_name_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, personal_name.get_gedcom_repr(level+1))
        if self.__sex:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SEX, self.__sex)
        for individual_event in self.__event_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, individual_event.get_gedcom_repr(level+1))
        for individual_attribute in self.__attribute_structures:
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

class MultimediaLink(Record):
    def __init__(self):
        self.__reference = ""
        self.__multimedia_file = ""
        self.__multimedia_format = ""
        self.__multimedia_type = ""
        self.__multimedia_title = ""
        super().__init__()

    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        if "@" in relevant_lines[0].value:
                self.__reference = relevant_lines[0].value
        else:
            for line in relevant_lines:
                tag = line.tag
                if tag == gedcom.tags.GEDCOM_TAG_FILE:
                    self.__multimedia_file = line.get_value()
                elif tag == gedcom.tags.GEDCOM_TAG_FORMAT:
                    self.__multimedia_format = line.get_value()
                elif tag == gedcom.tags.GEDCOM_TAG_MEDIA:
                    self.__multimedia_type = line.get_value()
                elif tag == gedcom.tags.GEDCOM_TAG_TITLE:
                    self.__multimedia_title = line.get_value()
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        if self.__reference:
            return "%s %s %s" % (level, gedcom.tags.GEDCOM_TAG_OBJECT, self.__reference)
        gedcom_repr = "%s %s" % (level, gedcom.tags.GEDCOM_TAG_OBJECT)
        if self.__multimedia_format:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_FORMAT, self.__multimedia_format)
        if self.__multimedia_file:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_FILE, self.__multimedia_file)
        if self.__multimedia_type:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_MEDIA, self.__multimedia_type)
        if self.__multimedia_title:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_TITLE, self.__multimedia_title)
        return gedcom_repr

class NoteStructure(Record):
    def __init__(self):
        self.__reference = ""
        self.__text = ""
        super().__init__()

    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        if "@" in relevant_lines[0].get_value():
            self.__reference = relevant_lines[0].get_value()
        else:
            for line in relevant_lines:
                if line.get_tag() == gedcom.tags.GEDCOM_TAG_CONTINUED:
                    self.__text += "\n" + line.get_value()
                else:
                    self.__text += line.get_value()
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        if self.__reference:
            return "%s %s %s" % (level, gedcom.tags.GEDCOM_TAG_NOTE, self.__reference)
        else:
            return split_text_for_gedcom(self.__text, gedcom.tags.GEDCOM_TAG_NOTE, level, gedcom.tags.MAX_TEXT_LENGTH)

class PersonalNameStructure(Record):
    def __init__(self, variation=""):
        self.__name = ""
        self.__name_type = ""
        self.__variation = variation
        self.__name_piece_prefix = ""
        self.__name_piece_given = ""
        self.__name_piece_nick = ""
        self.__name_piece_surname_prefix = ""
        self.__name_piece_surname = ""
        self.__name_piece_suffix = ""
        self.__note_structures = []
        self.__source_citations = []
        self.__phonetic_variations = []
        self.__romanized_variations = []
        super().__init__()
    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        starting_level = relevant_lines[0].level
        self.__name = relevant_lines[0].value
        index = 0
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            tag = line.tag
            level = line.level
            if tag == gedcom.tags.GEDCOM_TAG_TYPE and level == starting_level + 1:
                self.__name_type = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_NAME_PREFIX and level == starting_level + 1:
                self.__name_piece_prefix = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_GIVEN_NAME and level == starting_level + 1:
                self.__name_piece_given = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_NICKNAME and level == starting_level + 1:
                self.__name_piece_nick = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_SURN_PREFIX and level == starting_level + 1:
                self.__name_piece_surname_prefix = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_SURNAME and level == starting_level + 1:
                self.__name_piece_surname = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_NAME_SUFFIX and level == starting_level + 1:
                self.__name_piece_suffix = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_NOTE and level == starting_level + 1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__note_structures.append(note)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_SOURCE and level == starting_level + 1:
                source = SourceCitation()
                parsed_lines = source.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__source_citations.append(source)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_PHONETIC and level == starting_level + 1:
                phonetic_variation = PersonalNameStructure(gedcom.tags.GEDCOM_TAG_PHONETIC)
                parsed_lines = phonetic_variation.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__phonetic_variations.append(phonetic_variation)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_ROMANIZED and level == starting_level + 1:
                romanized_variation = PersonalNameStructure(gedcom.tags.GEDCOM_TAG_ROMANIZED)
                parsed_lines = romanized_variation.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__romanized_variations.append(romanized_variation)
                    index += parsed_lines
                    continue
            index += 1
        return len(relevant_lines)
            
    def get_gedcom_repr(self, level):
        if self.__variation:
            gedcom_repr = "%s %s %s" % (level, self.__variation, self.__name)
        else:
            gedcom_repr = "%s %s %s" % (level, gedcom.tags.GEDCOM_TAG_NAME, self.__name)
        if self.__name_type:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_TYPE, self.__name_type)
        if self.__name_piece_prefix:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_NAME_PREFIX, self.__name_piece_prefix)
        if self.__name_piece_given:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_GIVEN_NAME, self.__name_piece_given)
        if self.__name_piece_nick:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_NICKNAME, self.__name_piece_nick)
        if self.__name_piece_surname_prefix:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SURN_PREFIX, self.__name_piece_surname_prefix)
        if self.__name_piece_surname:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SURNAME, self.__name_piece_surname)
        if self.__name_piece_suffix:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_NAME_SUFFIX, self.__name_piece_suffix)
        for phonetic_variation in self.__phonetic_variations:
            gedcom_repr = "%s\n%s" % (gedcom_repr, phonetic_variation.get_gedcom_repr(level+1))
        for romanized_variation in self.__romanized_variations:
            gedcom_repr = "%s\n%s" % (gedcom_repr, romanized_variation.get_gedcom_repr(level+1))
        for note in self.__note_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note.get_gedcom_repr(level+1))        
        for source in self.__source_citations:
            gedcom_repr = "%s\n%s" % (gedcom_repr, source.get_gedcom_repr(level+1))
        return gedcom_repr.strip()

class SourceCitation(Record):
    def __init__(self):
        self.__pointer_source_record = False       
        # pointer to source record - preferred way
        self.__reference = ""
        self.__page = ""
        self.__event = ""
        self.__event_role = ""
        self.__data = ""
        self.__data_date = ""
        self.__data_text = ""
        # system not using source records
        self.__description = ""
        self.__text = ""
        # common to both options
        self.__multimedia_link = []
        self.__note_structures = []
        self.__certainty_assessment = ""
        super().__init__()
    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        if "@" in relevant_lines[0].value:
            # pointer to source record
            self.__reference = relevant_lines[0].value
            self.__pointer_source_record = True
        else:
            # system not using source records
            self.__description = relevant_lines[0].value
        starting_level = relevant_lines[0].level
        index = 0
        while (index < len(relevant_lines)):
            line = relevant_lines[index]
            tag = line.tag
            level = line.level
            scope = line.tag
            if tag == gedcom.tags.GEDCOM_TAG_OBJECT and (level == starting_level + 1):
                multimedialink = MultimediaLink()
                parsed_lines = multimedialink.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__multimedia_link.append(multimedialink)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_NOTE and (level == starting_level + 1):
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__note_structures.append(note)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_QUALITY_OF_DATA:
                self.__certainty_assessment = line.get_value()
            else:
                if self.__pointer_source_record:
                    if tag == gedcom.tags.GEDCOM_TAG_PAGE and (level == starting_level + 1):
                        self.__page = line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_EVENT and (level == starting_level + 1):
                        self.__event = line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_ROLE and (level == starting_level + 2):
                        self.__event_role = line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_DATA and (level == starting_level + 1):
                        self.__data = True
                    elif tag == gedcom.tags.GEDCOM_TAG_DATE and (level == starting_level + 2):
                        self.__data_date = line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_TEXT and (level == starting_level + 2):
                        self.__text = line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and (level == starting_level + 3):
                        self.__text = self.__text + line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and (level == starting_level + 3):
                        self.__text = self.__text + "\n" + line.get_value()
                    elif tag != gedcom.tags.GEDCOM_TAG_SOURCE:
                        return
                else:
                    if tag == gedcom.tags.GEDCOM_TAG_SOURCE:
                        self.__description = line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and (level == starting_level + 1) and (scope == gedcom.tags.GEDCOM_TAG_SOURCE):
                        self.__description = self.__description + line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and (level == starting_level + 1) and (scope == gedcom.tags.GEDCOM_TAG_SOURCE):
                        self.__description = self.__description + "\n" + line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_TEXT and (level == starting_level + 1):
                        self.__text = line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and (level == starting_level + 2):
                        self.__text = self.__text + line.get_value()
                    elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and (level == starting_level + 2):
                        self.__text = self.__text + "\n" + line.get_value()
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        if self.__pointer_source_record:
            gedcom_repr = "%s %s %s" % (level, gedcom.tags.GEDCOM_TAG_SOURCE, self.__reference)
            if self.__page:
                gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_PAGE, self.__page)
            if self.__event:
                gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_EVENT, self.__event)
            if self.__event_role:
                gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_ROLE, self.__event_role)
            if self.__data:
                gedcom_repr = "%s\n%s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_DATA)
            if self.__data_date:
                gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_DATE, self.__data_date)
            if self.__text:
                gedcom_repr = "%s\n%s" % (gedcom_repr, split_text_for_gedcom(self.__text, gedcom.tags.GEDCOM_TAG_TEXT, level+2, gedcom.tags.MAX_TEXT_LENGTH))
        else:                                
            gedcom_repr = gedcom.gedcom_file.split_text_for_gedcom(self.__description, gedcom.tags.GEDCOM_TAG_SOURCE, level, gedcom.tags.MAX_TEXT_LENGTH)
            if self.__text:
                gedcom_repr = gedcom_repr + '\n' + gedcom.gedcom_file.split_text_for_gedcom(self.__text, gedcom.tags.GEDCOM_TAG_TEXT, level+1, gedcom.tags.MAX_TEXT_LENGTH)
        for multimedia in self.__multimedia_link:
            gedcom_repr = "%s\n%s" % (gedcom_repr, multimedia.get_gedcom_repr(level+1))
        for note in self.__note_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note.get_gedcom_repr(level+1))
        if self.__certainty_assessment:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_QUALITY_OF_DATA, self.__certainty_assessment)
        return gedcom_repr