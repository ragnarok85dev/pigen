import gedcom.tags
from abc import abstractclassmethod
from gedcom.gedcom_file import split_text_for_gedcom
import re

gedcom_line_format = re.compile("^(?P<level>[0-9]+) ((?P<id>@[-a-zA-Z0-9]+@) )?(?P<tag>[_A-Z0-9]+)( (?P<value>.*))?$")

class Line(object):
    """
    Each GEDCOM line has the following syntax:
    gedcom_line := level + ' ' + [pointer + ' ' +] tag + [' ' + line_value]
    where:
        level is an integer number from 0 to 99, without leading zero
        optional_pointer is an optional pointer followed by delim, where point has the form @alphanum@
        tag is an alphanumeric string
        optional_line_value is the value associated to the tag
        terminator is carriage return and/or line feed
        implicit delimiter of elements is the space character
    """
    
    def __init__(self, line_content, index=0):
        self.__content = line_content
        self.__gedcom_index = index
        match = re.match(gedcom_line_format, line_content)
        if match:
            self.__level = int(match[1])
            if match[2]:
                self.__pointer = match[2].strip()
            else:
                self.__pointer = ""
            self.__tag = match[4].strip()
            if match[5]:
                self.__value = match[5].strip()
            else:
                self.__value = ""

    def is_last_gedcom_line(self):
        return self.__content == '0 '+ gedcom.tags.GEDCOM_TAG_TRAILER
    
    def is_user_defined_tag(self):
        return self.__tag[0:1] == '_'

    def get_content(self):
        return self.__content

    def get_gedcom_index(self):
        return self.__gedcom_index

    def get_level(self):
        return self.__level

    def get_pointer(self):
        return self.__pointer

    def get_tag(self):
        return self.__tag

    def get_value(self):
        return self.__value

    def get_line_content(self):
        return self.__content

    def set_content(self, value):
        self.__content = value

    def set_gedcom_index(self, value):
        self.__gedcom_index = value

    def set_level(self, value):
        self.__level = value

    def set_pointer(self, value):
        self.__pointer = value

    def set_tag(self, value):
        self.__tag = value

    def set_value(self, value):
        self.__value = value

    def set_line_content(self, value):
        self.__content = value

    def del_content(self):
        del self.__content

    def del_gedcom_index(self):
        del self.__gedcom_index

    def del_level(self):
        del self.__level

    def del_pointer(self):
        del self.__pointer

    def del_tag(self):
        del self.__tag

    def del_value(self):
        del self.__value

    def del_line_content(self):
        del self.__content
        
    def __str__(self):
        return self.__content

    def __repr__(self):
        return self.__content
    
    content = property(get_content, set_content, del_content, "content's docstring")
    gedcom_index = property(get_gedcom_index, set_gedcom_index, del_gedcom_index, "gedcom_index's docstring")
    level = property(get_level, set_level, del_level, "level's docstring")
    pointer = property(get_pointer, set_pointer, del_pointer, "pointer's docstring")
    tag = property(get_tag, set_tag, del_tag, "tag's docstring")
    value = property(get_value, set_value, del_value, "value's docstring")
    line_content = property(get_line_content, set_line_content, del_line_content, "line_content's docstring")

class Record():
    def __init__(self):
        pass
    
    def get_relevant_lines(self, gedcom_lines, valid_top_level_tags = None):
        '''
        Return a subset of GEDCOM lines belonging to the structure starting in gedcom_lines[0]
        :param gedcom_lines: list of GEDCOM lines containing the record
        :param valid_top_level_tags: if the GEDCOM structure does not have a hierarchical structure of levels (e.g. ADDRESS_STRUCTURE)
                                     then this is a list of valid top level tags (e.g.['ADDR', 'PHON', 'EMAIL', 'FAX', 'WWW'] ) 
        '''
        
        # TODO: restructure into a more pythonic fashion
        relevant_lines = []
        if gedcom_lines and len(gedcom_lines)>0:
                element = None
                for line in gedcom_lines[1:]:
                    if line.level > gedcom_lines[0].level or (valid_top_level_tags and line.tag in valid_top_level_tags and line.level == gedcom_lines[0].level):
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
        self.__notes = []
        self.__sources = []
        self.__multimedia_links = []
        super().__init__()
    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        index = 0
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_RESTRICTION and (line.level == 1):
                self.__restriction_notice = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NAME and (line.level == 1):
                personal_name = PersonalNameStructure()
                parsed_lines = personal_name.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__personal_name_structures.append(personal_name)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_SEX and (line.level == 1):
                self.__sex = line.value
#             elif line.tag in gedcom.tags.INDIVIDUAL_EVENT_STRUCTURE_TAGS and (line.level == 1):
#                 self.__individual_event_structures.append(IndividualEventStructure(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.INDIVIDUAL_ATTRIBUTE_STRUCTURE_TAGS and (line.level == 1): 
#                 self.__individual_attribute_structures.append(IndividualAttributeStructure(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.GEDCOM_TAG_FAMILY_CHILD and (line.level == 1):
#                 self.__child_to_family_links.append(ChildToFamilyLink(gedcom_lines[index:]))
#             elif line.tag in gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE and (line.level == 1):
#                 self.__spouse_to_family_links.append(SpouseToFamilyLink(gedcom_lines[index:]))
            elif line.tag == gedcom.tags.GEDCOM_TAG_SUBMITTER and (line.level == 1):
                self.__submitter_records.append(line.value)
#             elif line.tag in gedcom.tags.GEDCOM_TAG_ASSOCIATES and (line.level == 1):
#                 self.__associations_structures.append(AssociationStructure(gedcom_lines[index:]))
            elif line.tag == gedcom.tags.GEDCOM_TAG_ALIAS and (line.level == 1):
                self.__aliases.append(line.value)
            elif line.tag == gedcom.tags.GEDCOM_TAG_ANCES_INTEREST and (line.level == 1):
                self.__interest_more_research_ancestors.append(line.value)
            elif line.tag == gedcom.tags.GEDCOM_TAG_DESCENDANT_INT and (line.level == 1):
                self.__interest_more_research_descendants.append(line.value)
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_FILE_NUMBER and (line.level == 1):
                self.__permanent_record_file_number = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_ANCESTRAL_FILE_NUMBER and (line.level == 1):
                self.__ancestral_file_number = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_REFERENCE and (line.level == 1):
                if gedcom_lines[index+1].get_tag() == gedcom.tags.GEDCOM_TAG_TYPE:
                    self.__user_reference_numbers.append((gedcom_lines[index].get_value(), gedcom_lines[index+1].get_value()))
                else:
                    self.__user_reference_numbers.append((gedcom_lines[index].get_value(), ""))
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER and (line.level == 1):
                self.__automated_record_id = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE and (line.level == 1):
                change_date = ChangeDate()
                parsed_lines = change_date.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__change_date = change_date
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and (line.level == 1):
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_SOURCE and (line.level == 1):
                source = SourceCitation()
                parsed_lines = source.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__sources.append(source)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_OBJECT and (line.level == 1):
                multimedia = MultimediaLink()
                parsed_lines = multimedia.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__multimedia_links.append(multimedia)
                    index += parsed_lines
                    continue
            index += 1
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
        for note_structure in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note_structure.get_gedcom_repr(level+1))
        for source_citation in self.__sources:
            gedcom_repr = "%s\n%s" % (gedcom_repr, source_citation.get_gedcom_repr(level+1))
        for multimedia_link in self.__multimedia_links:
            gedcom_repr = "%s\n%s" % (gedcom_repr, multimedia_link.get_gedcom_repr(level+1))    
        return gedcom_repr    

# Substructures

class AddressStructure(Record):
    def __init__(self):
        self.__address_line = ""
        self.__address_line1 = ""
        self.__address_line2 = ""
        self.__address_line3 = ""
        self.__address_city = ""
        self.__address_state = ""
        self.__address_postal_code = ""
        self.__address_country = ""
        self.__phone_number = []
        self.__address_email = []
        self.__address_fax = []
        self.__address_web_page = []
        super().__init__()
    
    def parse_gedcom(self, gedcom_lines):
        valid_top_level_tags = [gedcom.tags.GEDCOM_TAG_ADDRESS, gedcom.tags.GEDCOM_TAG_PHONE, gedcom.tags.GEDCOM_TAG_EMAIL, gedcom.tags.GEDCOM_TAG_FAX, gedcom.tags.GEDCOM_TAG_WEB]
        relevant_lines = super().get_relevant_lines(gedcom_lines, valid_top_level_tags)
        index = 0
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_ADDRESS:
                if len(self.__address_line) == 0:
                    self.__address_line = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_CONTINUED:
                self.__address_line = self.__address_line + "\n" + line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_ADDRESS_LINE1:
                self.__address_line1 = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_ADDRESS_LINE2:
                self.__address_line2 = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_ADDRESS_LINE3:
                self.__address_line3 = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_CITY:
                self.__address_city = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_STATE:
                self.__address_state = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_POSTAL_CODE:
                self.__address_postal_code = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_COUNTRY:
                self.__address_country = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_PHONE:
                self.__phone_number.append(line.value)
            elif line.tag == gedcom.tags.GEDCOM_TAG_EMAIL:
                self.__address_email.append(line.value)
            elif line.tag == gedcom.tags.GEDCOM_TAG_FAX:
                self.__address_fax.append(line.value)
            elif line.tag == gedcom.tags.GEDCOM_TAG_WEB:
                self.__address_web_page.append(line.value)
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = split_text_for_gedcom(self.__address_line, gedcom.tags.GEDCOM_TAG_ADDRESS, level, gedcom.tags.MAX_TEXT_LENGTH)
        if self.__address_line1:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level+1, gedcom.tags.GEDCOM_TAG_ADDRESS_LINE1, self.__address_line1)
        if self.__address_line2:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level+1, gedcom.tags.GEDCOM_TAG_ADDRESS_LINE2, self.__address_line2)
        if self.__address_line3:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level+1, gedcom.tags.GEDCOM_TAG_ADDRESS_LINE3, self.__address_line3)
        if self.__address_city:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level+1, gedcom.tags.GEDCOM_TAG_CITY, self.__address_city)
        if self.__address_state:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level+1, gedcom.tags.GEDCOM_TAG_STATE, self.__address_state)
        if self.__address_postal_code:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level+1, gedcom.tags.GEDCOM_TAG_POSTAL_CODE, self.__address_postal_code)
        if self.__address_country:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level+1, gedcom.tags.GEDCOM_TAG_COUNTRY, self.__address_country)
        for line in self.__phone_number:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level, gedcom.tags.GEDCOM_TAG_PHONE, line)
        for line in self.__address_email:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level, gedcom.tags.GEDCOM_TAG_EMAIL, line)
        for line in self.__address_fax:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level, gedcom.tags.GEDCOM_TAG_FAX, line)
        for line in self.__address_web_page:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr,level, gedcom.tags.GEDCOM_TAG_WEB, line)
        return gedcom_repr.strip()

class ChangeDate(Record):
    def __init__(self):
        self.__date = ""
        self.__time = ""
        self.__notes = []
        super().__init__()

    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__date = relevant_lines[1].value
        index = 2
        starting_level = relevant_lines[0].level
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_TIME and line.level == starting_level+2:
                self.__time = relevant_lines[index].value
                index += 1
                continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level+1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s" % (level, gedcom.tags.GEDCOM_TAG_DATE_CHANGE)
        gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_DATE, self.__date)
        if self.__time:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_TIME, self.__time)
        for note_structure in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note_structure.get_gedcom_repr(level+1))
        return gedcom_repr

class EventDetail(Record):
    def __init__(self):
        self._type = ""
        self._date = ""
        self._place_name = ""
        self._place_hierarchy = ""
#         self._place_phonetic_variation = ""
#         self._place_phonetic_variation_type = ""
#         self._place_romanized_variation = ""
#         self._place_romanized_variation_type = ""
        self._place_latitude = ""
        self._place_longitude = ""
        self._place_notes = []
        self._address = None
        self._responsible_agency = ""
        self._religious_affiliation = ""
        self._cause = ""
        self._restriction_notice = ""
        self._notes = []
        self._sources = []
        self._multimedia_links = []
        super().__init__()
    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines, gedcom.tags.EVENT_DETAIL_TAGS)
        index = 0
        starting_level = relevant_lines[0].level
        scope = ""
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_TYPE and line.level == starting_level:
                self._type = line.value
                scope = line.tag
            elif line.tag == gedcom.tags.GEDCOM_TAG_DATE:
                self._date = line.value
                scope = line.tag
            elif line.tag == gedcom.tags.GEDCOM_TAG_PLACE:
                self._place_name = line.value
                scope = line.tag
            elif line.tag == gedcom.tags.GEDCOM_TAG_FORMAT and scope == gedcom.tags.GEDCOM_TAG_PLACE:
                self._place_hierarchy = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_LATITUDE and scope == gedcom.tags.GEDCOM_TAG_PLACE:
                self._place_latitude = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_LONGITUDE and scope == gedcom.tags.GEDCOM_TAG_PLACE:
                self._place_longitude = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and scope == gedcom.tags.GEDCOM_TAG_PLACE:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self._place_notes.append(note)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_ADDRESS:
                scope = line.tag
                address = AddressStructure()
                parsed_lines = address.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self._address = address
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_AGENCY:
                scope = line.tag
                self._responsible_agency = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_RELIGION:
                scope = line.tag
                self._religious_affiliation = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_CAUSE:
                scope = line.tag
                self._cause = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_RESTRICTION:
                scope = line.tag
                self._restriction_notice = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level:
                scope = line.tag
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self._notes.append(note)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_SOURCE and line.level == starting_level:
                scope = line.tag
                source = SourceCitation()
                parsed_lines = source.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self._sources.append(source)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_OBJECT and line.level == starting_level:
                scope = line.tag
                multimedia = MultimediaLink()
                parsed_lines = multimedia.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self._multimedia_links.append(multimedia)
                    index += parsed_lines
                    continue
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = ""
        if self._type:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_TYPE, self._type)
        if self._date:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_DATE, self._date)
        if self._place_name:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_PLACE, self._place_name)
        if self._place_hierarchy:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_FORMAT, self._place_hierarchy)
        if self._place_latitude:
            gedcom_repr = "%s\n%s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_MAP)
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_LATITUDE, self._place_latitude)
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_LONGITUDE, self._place_longitude)
        for note in self._place_notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note.get_gedcom_repr(level+1))
        if self._address:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self._address.get_gedcom_repr(level))
        if self._responsible_agency:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_AGENCY, self._responsible_agency)
        if self._religious_affiliation:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_RELIGION, self._religious_affiliation)
        if self._cause:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_CAUSE, self._cause)
        if self._restriction_notice:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_RESTRICTION, self._restriction_notice)
        for note_structure in self._notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note_structure.get_gedcom_repr(level))
        for source_citation in self._sources:
            gedcom_repr = "%s\n%s" % (gedcom_repr, source_citation.get_gedcom_repr(level))
        for multimedia_link in self._multimedia_links:
            gedcom_repr = "%s\n%s" % (gedcom_repr, multimedia_link.get_gedcom_repr(level))
        return gedcom_repr.strip()

class IndividualEventDetail(EventDetail):
    def __init__(self):
        self._age_at_event = ""
        super().__init__()

    def parse_gedcom(self, gedcom_lines):
        parsed_lines = super().parse_gedcom(gedcom_lines)
        if len(gedcom_lines) > parsed_lines and gedcom_lines[parsed_lines].tag == gedcom.tags.GEDCOM_TAG_AGE:
            self._age_at_event = gedcom_lines[parsed_lines].value
            parsed_lines += 1
        return parsed_lines
    
    def get_gedcom_repr(self, level):
        gedcom_repr = super().get_gedcom_repr(level)
        if self._age_at_event:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_AGE, self._age_at_event)
        return gedcom_repr

class IndividualEventStructure(IndividualEventDetail):
    def __init__(self):
        self.__tag = ""
        self.__birth_christening_yes = ""
        self.__birth_christening_family_reference = ""
        self.__death_yes = ""
        self.__adopting_family_reference = ""
        self.__adopting_parent = ""
        super().__init__()

    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__tag = relevant_lines[0].tag
        index = 0
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if self.__tag in (gedcom.tags.GEDCOM_TAG_BIRTH, gedcom.tags.GEDCOM_TAG_CHRISTENING):
                self.__birth_christening_yes = relevant_lines[0].value
                if len(relevant_lines) > index+1 and (relevant_lines[index+1].level == line.level+1):
                    parsed_lines = super().parse_gedcom(relevant_lines[1:])
                    index += parsed_lines
                    if relevant_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_FAMILY_CHILD:
                        self.__birth_christening_family_reference = relevant_lines[index+1].value
                        index += 1
            elif self.__tag == gedcom.tags.GEDCOM_TAG_DEATH:
                self.__death_yes = relevant_lines[0].value
                if len(relevant_lines) > index+1 and (relevant_lines[index+1].level == line.level+1):
                    parsed_lines = super().parse_gedcom(relevant_lines[1:])
                    index += parsed_lines
            elif self.__tag == gedcom.tags.GEDCOM_TAG_ADOPTION:
                if len(relevant_lines) > index+1 and (relevant_lines[index+1].level == line.level+1):
                    parsed_lines = super().parse_gedcom(relevant_lines[1:])
                    index += parsed_lines
                    if len(relevant_lines) > index+2 and relevant_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_FAMILY_CHILD:
                        self.__adopting_family_reference = relevant_lines[index+1].value
                        index += 1
                        if len(relevant_lines) > index+1 and relevant_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_ADOPTION:
                            self.__adopting_parent = relevant_lines[index+1].value
                            index += 1
            elif self.__tag in (gedcom.tags.INDIVIDUAL_EVENT_STRUCTURE_TAGS):
                if len(relevant_lines) >= index+1 and (relevant_lines[index+1].level == line.level+1):
                    parsed_lines = super().parse_gedcom(relevant_lines[1:])
                    index += parsed_lines
            else:
                return
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s" % (level, self.__tag)
        if self.__birth_christening_yes:
            gedcom_repr = "%s %s" % (gedcom_repr, self.__birth_christening_yes)
        elif self.__death_yes:
            gedcom_repr = "%s %s" % (gedcom_repr, self.__death_yes)
        if super().get_gedcom_repr(level + 1):
            gedcom_repr = "%s\n%s" % (gedcom_repr, super().get_gedcom_repr(level + 1))
        if self.__birth_christening_family_reference:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, (level + 1), gedcom.tags.GEDCOM_TAG_FAMILY_CHILD,self.__birth_christening_family_reference)
        elif self.__adopting_family_reference:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, (level + 1), gedcom.tags.GEDCOM_TAG_FAMILY_CHILD,self.__adopting_family_reference)
            if self.__adopting_parent:
                gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, (level + 2), gedcom.tags.GEDCOM_TAG_ADOPTION, self.__adopting_parent)
        return gedcom_repr

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
                    self.__multimedia_file = line.value
                elif tag == gedcom.tags.GEDCOM_TAG_FORMAT:
                    self.__multimedia_format = line.value
                elif tag == gedcom.tags.GEDCOM_TAG_MEDIA:
                    self.__multimedia_type = line.value
                elif tag == gedcom.tags.GEDCOM_TAG_TITLE:
                    self.__multimedia_title = line.value
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
                if line.tag == gedcom.tags.GEDCOM_TAG_CONTINUED:
                    self.__text += "\n" + line.value
                else:
                    self.__text += line.value
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
        self.__notes = []
        self.__sources = []
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
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_SOURCE and level == starting_level + 1:
                source = SourceCitation()
                parsed_lines = source.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__sources.append(source)
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
        for note in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note.get_gedcom_repr(level+1))        
        for source in self.__sources:
            gedcom_repr = "%s\n%s" % (gedcom_repr, source.get_gedcom_repr(level+1))
        return gedcom_repr.strip()

class SourceCitation(Record):
    def __init__(self):
        self.__pointer_source_record = False       
        # pointer to source record
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
        self.__notes = []
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
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_QUALITY_OF_DATA:
                self.__certainty_assessment = line.value
            else:
                if self.__pointer_source_record:
                    if tag == gedcom.tags.GEDCOM_TAG_PAGE and (level == starting_level + 1):
                        self.__page = line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_EVENT and (level == starting_level + 1):
                        self.__event = line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_ROLE and (level == starting_level + 2):
                        self.__event_role = line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_DATA and (level == starting_level + 1):
                        self.__data = True
                    elif tag == gedcom.tags.GEDCOM_TAG_DATE and (level == starting_level + 2):
                        self.__data_date = line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_TEXT and (level == starting_level + 2):
                        self.__text = line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and (level == starting_level + 3):
                        self.__text = self.__text + line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and (level == starting_level + 3):
                        self.__text = self.__text + "\n" + line.value
                    elif tag != gedcom.tags.GEDCOM_TAG_SOURCE:
                        return
                else:
                    if tag == gedcom.tags.GEDCOM_TAG_SOURCE:
                        self.__description = line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and (level == starting_level + 1) and (scope == gedcom.tags.GEDCOM_TAG_SOURCE):
                        self.__description = self.__description + line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and (level == starting_level + 1) and (scope == gedcom.tags.GEDCOM_TAG_SOURCE):
                        self.__description = self.__description + "\n" + line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_TEXT and (level == starting_level + 1):
                        self.__text = line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and (level == starting_level + 2):
                        self.__text = self.__text + line.value
                    elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and (level == starting_level + 2):
                        self.__text = self.__text + "\n" + line.value
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
        for note in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note.get_gedcom_repr(level+1))
        if self.__certainty_assessment:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_QUALITY_OF_DATA, self.__certainty_assessment)
        return gedcom_repr