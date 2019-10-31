import gedcom.tags
from abc import abstractclassmethod
import re

gedcom_line_format = re.compile("^(?P<level>[0-9]+) ((?P<id>@[-a-zA-Z0-9_]+@) )?(?P<tag>[_A-Z0-9]+)( (?P<value>.*))?$")

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
        self.__level = None
        self.__pointer = ""
        self.__value = ""
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
        return self.__content.strip() == ('0 '+ gedcom.tags.GEDCOM_TAG_TRAILER).strip()
    
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

class Header(Record):
    def __init__(self):
        super().__init__()
        self.__source_system_id = ""
        self.__source_system_version = ""
        self.__source_system_name = ""
        self.__source_system_corporate = ""
        self.__source_system_corporate_address = None
        self.__source_system_data = ""
        self.__source_system_data_date = ""
        self.__source_system_data_copyright = ""
        self.__destination_system = ""
        self.__transmission_date = ""
        self.__transmission_date_time = ""
        self.__submitter_record_reference = ""
        self.__submission_record_reference = ""
        self.__file_name = ""
        self.__copyright = ""
        self.__gedcom_version = ""
        self.__gedcom_form = ""
        self.__character_set = ""
        self.__character_set_version = ""
        self.__language = ""
        self.__place_form = ""
        self.__note = ""
        super().__init__()

    def get_source_system_id(self):
        return self.__source_system_id


    def get_source_system_version(self):
        return self.__source_system_version


    def get_source_system_name(self):
        return self.__source_system_name


    def get_source_system_corporate(self):
        return self.__source_system_corporate


    def get_source_system_corporate_address(self):
        return self.__source_system_corporate_address


    def get_source_system_data(self):
        return self.__source_system_data


    def get_source_system_data_date(self):
        return self.__source_system_data_date


    def get_source_system_data_copyright(self):
        return self.__source_system_data_copyright


    def get_destination_system(self):
        return self.__destination_system


    def get_transmission_date(self):
        return self.__transmission_date


    def get_transmission_date_time(self):
        return self.__transmission_date_time


    def get_submitter_record_reference(self):
        return self.__submitter_record_reference


    def get_submission_record_reference(self):
        return self.__submission_record_reference


    def get_file_name(self):
        return self.__file_name


    def get_copyright(self):
        return self.__copyright


    def get_gedcom_version(self):
        return self.__gedcom_version


    def get_gedcom_form(self):
        return self.__gedcom_form


    def get_character_set(self):
        return self.__character_set


    def get_character_set_version(self):
        return self.__character_set_version


    def get_language(self):
        return self.__language


    def get_place_form(self):
        return self.__place_form


    def get_note(self):
        return self.__note


    def set_source_system_id(self, value):
        self.__source_system_id = value


    def set_source_system_version(self, value):
        self.__source_system_version = value


    def set_source_system_name(self, value):
        self.__source_system_name = value


    def set_source_system_corporate(self, value):
        self.__source_system_corporate = value


    def set_source_system_corporate_address(self, value):
        self.__source_system_corporate_address = value


    def set_source_system_data(self, value):
        self.__source_system_data = value


    def set_source_system_data_date(self, value):
        self.__source_system_data_date = value


    def set_source_system_data_copyright(self, value):
        self.__source_system_data_copyright = value


    def set_destination_system(self, value):
        self.__destination_system = value


    def set_transmission_date(self, value):
        self.__transmission_date = value


    def set_transmission_date_time(self, value):
        self.__transmission_date_time = value


    def set_submitter_record_reference(self, value):
        self.__submitter_record_reference = value


    def set_submission_record_reference(self, value):
        self.__submission_record_reference = value


    def set_file_name(self, value):
        self.__file_name = value


    def set_copyright(self, value):
        self.__copyright = value


    def set_gedcom_version(self, value):
        self.__gedcom_version = value


    def set_gedcom_form(self, value):
        self.__gedcom_form = value


    def set_character_set(self, value):
        self.__character_set = value


    def set_character_set_version(self, value):
        self.__character_set_version = value


    def set_language(self, value):
        self.__language = value


    def set_place_form(self, value):
        self.__place_form = value


    def set_note(self, value):
        self.__note = value


    def del_source_system_id(self):
        del self.__source_system_id


    def del_source_system_version(self):
        del self.__source_system_version


    def del_source_system_name(self):
        del self.__source_system_name


    def del_source_system_corporate(self):
        del self.__source_system_corporate


    def del_source_system_corporate_address(self):
        del self.__source_system_corporate_address


    def del_source_system_data(self):
        del self.__source_system_data


    def del_source_system_data_date(self):
        del self.__source_system_data_date


    def del_source_system_data_copyright(self):
        del self.__source_system_data_copyright


    def del_destination_system(self):
        del self.__destination_system


    def del_transmission_date(self):
        del self.__transmission_date


    def del_transmission_date_time(self):
        del self.__transmission_date_time


    def del_submitter_record_reference(self):
        del self.__submitter_record_reference


    def del_submission_record_reference(self):
        del self.__submission_record_reference


    def del_file_name(self):
        del self.__file_name


    def del_copyright(self):
        del self.__copyright


    def del_gedcom_version(self):
        del self.__gedcom_version


    def del_gedcom_form(self):
        del self.__gedcom_form


    def del_character_set(self):
        del self.__character_set


    def del_character_set_version(self):
        del self.__character_set_version


    def del_language(self):
        del self.__language


    def del_place_form(self):
        del self.__place_form


    def del_note(self):
        del self.__note

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        scope = ""
        index = 0
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            tag = line.tag
            if tag == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_id = line.value
                scope = gedcom.tags.GEDCOM_TAG_SOURCE
            elif tag == gedcom.tags.GEDCOM_TAG_VERSION and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_version = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_NAME and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_name = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CORPORATE and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_corporate = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_ADDRESS and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                address = AddressStructure()
                parsed_lines = address.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__source_system_corporate_address = address
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_DATA and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_data = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_DATE and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_data_date = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_COPYRIGHT and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_data_copyright = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_data_copyright = self.__source_system_data_copyright + "\n" + line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and scope == gedcom.tags.GEDCOM_TAG_SOURCE:
                self.__source_system_data_copyright = self.__source_system_data_copyright + line.value
            elif tag == gedcom.tags.GEDCOM_TAG_DESTINATION:
                scope = ""
                self.__destination_system = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_DATE:
                scope = ""
                self.__transmission_date = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_TIME:
                scope = ""
                self.__transmission_date_time = line.value    
            elif tag == gedcom.tags.GEDCOM_TAG_SUBMITTER:
                scope = ""
                self.__submitter_record_reference = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_SUBMISSION:
                scope = ""
                self.__submission_record_reference = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_FILE:
                scope = ""
                self.__file_name = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_COPYRIGHT:
                scope = ""
                self.__copyright = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_GEDCOM:
                scope = gedcom.tags.GEDCOM_TAG_GEDCOM
            elif tag == gedcom.tags.GEDCOM_TAG_VERSION and scope == gedcom.tags.GEDCOM_TAG_GEDCOM:
                self.__gedcom_version = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_FORMAT and scope == gedcom.tags.GEDCOM_TAG_GEDCOM:
                self.__gedcom_form = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CHARACTER_SET:
                scope = gedcom.tags.GEDCOM_TAG_CHARACTER_SET
                self.__character_set = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_VERSION and scope == gedcom.tags.GEDCOM_TAG_CHARACTER_SET:
                self.__character_set_version = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_LANGUAGE:
                scope = ""
                self.__language = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_PLACE:
                scope = gedcom.tags.GEDCOM_TAG_PLACE
            elif tag == gedcom.tags.GEDCOM_TAG_FORMAT and scope == gedcom.tags.GEDCOM_TAG_PLACE:
                self.__place_form = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_NOTE:
                scope = gedcom.tags.GEDCOM_TAG_NOTE
                self.__note = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and scope == gedcom.tags.GEDCOM_TAG_NOTE:
                self.__note = self.__note + "\n" + line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and scope == gedcom.tags.GEDCOM_TAG_NOTE:
                self.__note = self.__note + line.value
            elif line.is_user_defined_tag():
                # current implementation ignores the the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
                    continue
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s" % (level, gedcom.tags.GEDCOM_TAG_HEADER)
        if self.__source_system_id:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SOURCE, self.__source_system_id)
        if self.__source_system_version:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_VERSION, self.__source_system_version)
        if self.__source_system_name:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_NAME, self.__source_system_name)
        if self.__source_system_corporate:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_CORPORATE, self.__source_system_corporate)
        if self.__source_system_corporate_address:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__source_system_corporate_address.get_gedcom_repr(level+3))
        if self.__source_system_data:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_DATA, self.__source_system_data)
        if self.__source_system_data_date:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+3, gedcom.tags.GEDCOM_TAG_DATE, self.__source_system_data_date)
        if self.__source_system_data_copyright:
            gedcom_repr = "%s\n%s" % (gedcom_repr, gedcom.gedcom_file.split_text_for_gedcom(self.__source_system_data_copyright, gedcom.tags.GEDCOM_TAG_COPYRIGHT, level+3, gedcom.tags.MAX_TEXT_LENGTH))
        if self.__destination_system:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_DESTINATION, self.__destination_system)
        if self.__transmission_date:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_DATE, self.__transmission_date)
        if self.__transmission_date_time:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_TIME, self.__transmission_date_time)
        if self.__submission_record_reference:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SUBMISSION, self.__submission_record_reference)    
        if self.__submitter_record_reference:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SUBMITTER, self.__submitter_record_reference)
        if self.__file_name:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_FILE, self.__file_name)
        if self.__copyright:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_COPYRIGHT, self.__copyright)
        gedcom_repr = "%s\n%s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_GEDCOM)
        if self.__gedcom_version:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_VERSION, self.__gedcom_version)
        if self.__gedcom_form:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_FORMAT, self.__gedcom_form)
        if self.__character_set:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_CHARACTER_SET, self.__character_set)
        if self.__character_set_version:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_VERSION, self.__character_set_version)
        if self.__language:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_LANGUAGE, self.__language)
        if self.__place_form:
            gedcom_repr = "%s\n%s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_PLACE)
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_FORMAT, self.__place_form)
        if self.__note:
            gedcom_repr = "%s\n%s" % (gedcom_repr, gedcom.gedcom_file.split_text_for_gedcom(self.__note, gedcom.tags.GEDCOM_TAG_NOTE, level+1, gedcom.tags.MAX_TEXT_LENGTH))
        return gedcom_repr
    source_system_id = property(get_source_system_id, set_source_system_id, del_source_system_id, "source_system_id's docstring")
    source_system_version = property(get_source_system_version, set_source_system_version, del_source_system_version, "source_system_version's docstring")
    source_system_name = property(get_source_system_name, set_source_system_name, del_source_system_name, "source_system_name's docstring")
    source_system_corporate = property(get_source_system_corporate, set_source_system_corporate, del_source_system_corporate, "source_system_corporate's docstring")
    source_system_corporate_address = property(get_source_system_corporate_address, set_source_system_corporate_address, del_source_system_corporate_address, "source_system_corporate_address's docstring")
    source_system_data = property(get_source_system_data, set_source_system_data, del_source_system_data, "source_system_data's docstring")
    source_system_data_date = property(get_source_system_data_date, set_source_system_data_date, del_source_system_data_date, "source_system_data_date's docstring")
    source_system_data_copyright = property(get_source_system_data_copyright, set_source_system_data_copyright, del_source_system_data_copyright, "source_system_data_copyright's docstring")
    destination_system = property(get_destination_system, set_destination_system, del_destination_system, "destination_system's docstring")
    transmission_date = property(get_transmission_date, set_transmission_date, del_transmission_date, "transmission_date's docstring")
    transmission_date_time = property(get_transmission_date_time, set_transmission_date_time, del_transmission_date_time, "transmission_date_time's docstring")
    submitter_record_reference = property(get_submitter_record_reference, set_submitter_record_reference, del_submitter_record_reference, "submitter_record_reference's docstring")
    submission_record_reference = property(get_submission_record_reference, set_submission_record_reference, del_submission_record_reference, "submission_record_reference's docstring")
    file_name = property(get_file_name, set_file_name, del_file_name, "file_name's docstring")
    copyright = property(get_copyright, set_copyright, del_copyright, "copyright's docstring")
    gedcom_version = property(get_gedcom_version, set_gedcom_version, del_gedcom_version, "gedcom_version's docstring")
    gedcom_form = property(get_gedcom_form, set_gedcom_form, del_gedcom_form, "gedcom_form's docstring")
    character_set = property(get_character_set, set_character_set, del_character_set, "character_set's docstring")
    character_set_version = property(get_character_set_version, set_character_set_version, del_character_set_version, "character_set_version's docstring")
    language = property(get_language, set_language, del_language, "language's docstring")
    place_form = property(get_place_form, set_place_form, del_place_form, "place_form's docstring")
    note = property(get_note, set_note, del_note, "note's docstring")

class Family(Record):
    def __init__(self):
        self.__reference = ""
        self.__restriction_notice = ""
        self.__family_event_structures = []
        self.__husband_reference = ""
        self.__wife_reference = ""
        self.__children_references = []
        self.__number_children = ""
        self.__submitter_records = []
        self.__user_reference_numbers = []
        self.__automated_record_id = ""
        self.__change_date = None
        self.__notes = []
        self.__sources = []
        self.__multimedia_links = []
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_restriction_notice(self):
        return self.__restriction_notice


    def get_family_event_structures(self):
        return self.__family_event_structures


    def get_husband_reference(self):
        return self.__husband_reference


    def get_wife_reference(self):
        return self.__wife_reference


    def get_children_references(self):
        return self.__children_references


    def get_number_children(self):
        return self.__number_children


    def get_submitter_records(self):
        return self.__submitter_records


    def get_user_reference_numbers(self):
        return self.__user_reference_numbers


    def get_automated_record_id(self):
        return self.__automated_record_id


    def get_change_date(self):
        return self.__change_date


    def get_notes(self):
        return self.__notes


    def get_sources(self):
        return self.__sources


    def get_multimedia_links(self):
        return self.__multimedia_links


    def set_reference(self, value):
        self.__reference = value


    def set_restriction_notice(self, value):
        self.__restriction_notice = value


    def set_family_event_structures(self, value):
        self.__family_event_structures = value


    def set_husband_reference(self, value):
        self.__husband_reference = value


    def set_wife_reference(self, value):
        self.__wife_reference = value


    def set_children_references(self, value):
        self.__children_references = value


    def set_number_children(self, value):
        self.__number_children = value


    def set_submitter_records(self, value):
        self.__submitter_records = value


    def set_user_reference_numbers(self, value):
        self.__user_reference_numbers = value


    def set_automated_record_id(self, value):
        self.__automated_record_id = value


    def set_change_date(self, value):
        self.__change_date = value


    def set_notes(self, value):
        self.__notes = value


    def set_sources(self, value):
        self.__sources = value


    def set_multimedia_links(self, value):
        self.__multimedia_links = value


    def del_reference(self):
        del self.__reference


    def del_restriction_notice(self):
        del self.__restriction_notice


    def del_family_event_structures(self):
        del self.__family_event_structures


    def del_husband_reference(self):
        del self.__husband_reference


    def del_wife_reference(self):
        del self.__wife_reference


    def del_children_references(self):
        del self.__children_references


    def del_number_children(self):
        del self.__number_children


    def del_submitter_records(self):
        del self.__submitter_records


    def del_user_reference_numbers(self):
        del self.__user_reference_numbers


    def del_automated_record_id(self):
        del self.__automated_record_id


    def del_change_date(self):
        del self.__change_date


    def del_notes(self):
        del self.__notes


    def del_sources(self):
        del self.__sources


    def del_multimedia_links(self):
        del self.__multimedia_links

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        index = 0
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_RESTRICTION and (line.level == 1):
                self.__restriction_notice = line.value
            elif line.tag in gedcom.tags.FAMILY_EVENT_STRUCTURE_TAGS and (line.level == 1):
                family_event = FamilyEventStructure()
                parsed_lines = family_event.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__family_event_structures.append(family_event)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_HUSBAND and (line.level == 1):
                self.__husband_reference = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_WIFE and (line.level == 1):
                self.__wife_reference = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_CHILD and (line.level == 1):
                self.__children_references.append(line.value)
            elif line.tag == gedcom.tags.GEDCOM_TAG_CHILDREN_COUNT and (line.level == 1):
                self.__number_children = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_SUBMITTER and (line.level == 1):
                self.__submitter_records.append(line.value)
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
            elif line.tag in (gedcom.tags.IGNORED_FAMILY_RECORD_TAGS) or line.is_user_defined_tag():
                # current implementation ignores the structures identified by tags in IGNORED_FAMILY_RECORD_TAGS and the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
                    continue
            index += 1
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s %s" % (level, self.__reference, gedcom.tags.GEDCOM_TAG_FAMILY)
        if self.__restriction_notice:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_RESTRICTION, self.__restriction_notice)
        for family_event_structure in self.__family_event_structures:
            gedcom_repr = "%s\n%s" % (gedcom_repr, family_event_structure.get_gedcom_repr(level+1))
        if self.__husband_reference:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_HUSBAND, self.__husband_reference)
        if self.__wife_reference:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_WIFE, self.__wife_reference)
        for child_reference in self.__children_references:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_CHILD, child_reference)
        if self.__number_children:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_CHILDREN_COUNT, self.__number_children)
        for submitter_record_reference in self.__submitter_records:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SUBMITTER, submitter_record_reference)
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
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    restriction_notice = property(get_restriction_notice, set_restriction_notice, del_restriction_notice, "restriction_notice's docstring")
    family_event_structures = property(get_family_event_structures, set_family_event_structures, del_family_event_structures, "family_event_structures's docstring")
    husband_reference = property(get_husband_reference, set_husband_reference, del_husband_reference, "husband_reference's docstring")
    wife_reference = property(get_wife_reference, set_wife_reference, del_wife_reference, "wife_reference's docstring")
    children_references = property(get_children_references, set_children_references, del_children_references, "children_references's docstring")
    number_children = property(get_number_children, set_number_children, del_number_children, "number_children's docstring")
    submitter_records = property(get_submitter_records, set_submitter_records, del_submitter_records, "submitter_records's docstring")
    user_reference_numbers = property(get_user_reference_numbers, set_user_reference_numbers, del_user_reference_numbers, "user_reference_numbers's docstring")
    automated_record_id = property(get_automated_record_id, set_automated_record_id, del_automated_record_id, "automated_record_id's docstring")
    change_date = property(get_change_date, set_change_date, del_change_date, "change_date's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    sources = property(get_sources, set_sources, del_sources, "sources's docstring")
    multimedia_links = property(get_multimedia_links, set_multimedia_links, del_multimedia_links, "multimedia_links's docstring")

class Individual(Record):
    def __init__(self):
        self.__reference = ""
        self.__restriction_notice = ""
        self.__personal_name_structures = []
        self.__sex = ""
        self.__event_structures = []
        self.__attribute_structures = []
        self.__child_to_family_links = []
        self.__spouse_to_family_links= []
        self.__submitter_records = []
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

    def get_reference(self):
        return self.__reference


    def get_restriction_notice(self):
        return self.__restriction_notice


    def get_personal_name_structures(self):
        return self.__personal_name_structures


    def get_sex(self):
        return self.__sex


    def get_event_structures(self):
        return self.__event_structures


    def get_attribute_structures(self):
        return self.__attribute_structures


    def get_child_to_family_links(self):
        return self.__child_to_family_links


    def get_spouse_to_family_links(self):
        return self.__spouse_to_family_links


    def get_submitter_records(self):
        return self.__submitter_records


    def get_aliases(self):
        return self.__aliases


    def get_interest_more_research_ancestors(self):
        return self.__interest_more_research_ancestors


    def get_interest_more_research_descendants(self):
        return self.__interest_more_research_descendants


    def get_permanent_record_file_number(self):
        return self.__permanent_record_file_number


    def get_ancestral_file_number(self):
        return self.__ancestral_file_number


    def get_user_reference_numbers(self):
        return self.__user_reference_numbers


    def get_automated_record_id(self):
        return self.__automated_record_id


    def get_change_date(self):
        return self.__change_date


    def get_notes(self):
        return self.__notes


    def get_sources(self):
        return self.__sources


    def get_multimedia_links(self):
        return self.__multimedia_links


    def set_reference(self, value):
        self.__reference = value


    def set_restriction_notice(self, value):
        self.__restriction_notice = value


    def set_personal_name_structures(self, value):
        self.__personal_name_structures = value


    def set_sex(self, value):
        self.__sex = value


    def set_event_structures(self, value):
        self.__event_structures = value


    def set_attribute_structures(self, value):
        self.__attribute_structures = value


    def set_child_to_family_links(self, value):
        self.__child_to_family_links = value


    def set_spouse_to_family_links(self, value):
        self.__spouse_to_family_links = value


    def set_submitter_records(self, value):
        self.__submitter_records = value


    def set_aliases(self, value):
        self.__aliases = value


    def set_interest_more_research_ancestors(self, value):
        self.__interest_more_research_ancestors = value


    def set_interest_more_research_descendants(self, value):
        self.__interest_more_research_descendants = value


    def set_permanent_record_file_number(self, value):
        self.__permanent_record_file_number = value


    def set_ancestral_file_number(self, value):
        self.__ancestral_file_number = value


    def set_user_reference_numbers(self, value):
        self.__user_reference_numbers = value


    def set_automated_record_id(self, value):
        self.__automated_record_id = value


    def set_change_date(self, value):
        self.__change_date = value


    def set_notes(self, value):
        self.__notes = value


    def set_sources(self, value):
        self.__sources = value


    def set_multimedia_links(self, value):
        self.__multimedia_links = value


    def del_reference(self):
        del self.__reference


    def del_restriction_notice(self):
        del self.__restriction_notice


    def del_personal_name_structures(self):
        del self.__personal_name_structures


    def del_sex(self):
        del self.__sex


    def del_event_structures(self):
        del self.__event_structures


    def del_attribute_structures(self):
        del self.__attribute_structures


    def del_child_to_family_links(self):
        del self.__child_to_family_links


    def del_spouse_to_family_links(self):
        del self.__spouse_to_family_links


    def del_submitter_records(self):
        del self.__submitter_records


    def del_aliases(self):
        del self.__aliases


    def del_interest_more_research_ancestors(self):
        del self.__interest_more_research_ancestors


    def del_interest_more_research_descendants(self):
        del self.__interest_more_research_descendants


    def del_permanent_record_file_number(self):
        del self.__permanent_record_file_number


    def del_ancestral_file_number(self):
        del self.__ancestral_file_number


    def del_user_reference_numbers(self):
        del self.__user_reference_numbers


    def del_automated_record_id(self):
        del self.__automated_record_id


    def del_change_date(self):
        del self.__change_date


    def del_notes(self):
        del self.__notes


    def del_sources(self):
        del self.__sources


    def del_multimedia_links(self):
        del self.__multimedia_links

    
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
            elif line.tag in gedcom.tags.INDIVIDUAL_EVENT_STRUCTURE_TAGS and (line.level == 1):
                individual_event_structure = IndividualEventStructure()
                parsed_lines = individual_event_structure.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__event_structures.append(individual_event_structure)
                    index += parsed_lines
                    continue
            elif line.tag in gedcom.tags.INDIVIDUAL_ATTRIBUTE_STRUCTURE_TAGS and (line.level == 1):           
                individual_attribute_structure = IndividualAttributeStructure()
                parsed_lines = individual_attribute_structure.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__attribute_structures.append(individual_attribute_structure)
                    index += parsed_lines
                    continue
            elif line.tag in gedcom.tags.GEDCOM_TAG_FAMILY_CHILD and (line.level == 1):               
                child_to_family_link = ChildToFamilyLink()
                parsed_lines = child_to_family_link.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__child_to_family_links.append(child_to_family_link)
                    index += parsed_lines
                    continue
            elif line.tag in gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE and (line.level == 1):
                spouse_to_family_link = SpouseToFamilyLink()
                parsed_lines = spouse_to_family_link.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__spouse_to_family_links.append(spouse_to_family_link)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_SUBMITTER and (line.level == 1):
                self.__submitter_records.append(line.value)
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
            elif line.tag in (gedcom.tags.IGNORED_INDIVIDUAL_RECORD_TAGS) or line.is_user_defined_tag():
                # current implementation ignores the structures identified by tags in IGNORED_INDIVIDUAL_RECORD_TAGS and the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
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
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    restriction_notice = property(get_restriction_notice, set_restriction_notice, del_restriction_notice, "restriction_notice's docstring")
    personal_name_structures = property(get_personal_name_structures, set_personal_name_structures, del_personal_name_structures, "personal_name_structures's docstring")
    sex = property(get_sex, set_sex, del_sex, "sex's docstring")
    event_structures = property(get_event_structures, set_event_structures, del_event_structures, "event_structures's docstring")
    attribute_structures = property(get_attribute_structures, set_attribute_structures, del_attribute_structures, "attribute_structures's docstring")
    child_to_family_links = property(get_child_to_family_links, set_child_to_family_links, del_child_to_family_links, "child_to_family_links's docstring")
    spouse_to_family_links = property(get_spouse_to_family_links, set_spouse_to_family_links, del_spouse_to_family_links, "spouse_to_family_links's docstring")
    submitter_records = property(get_submitter_records, set_submitter_records, del_submitter_records, "submitter_records's docstring")
    aliases = property(get_aliases, set_aliases, del_aliases, "aliases's docstring")
    interest_more_research_ancestors = property(get_interest_more_research_ancestors, set_interest_more_research_ancestors, del_interest_more_research_ancestors, "interest_more_research_ancestors's docstring")
    interest_more_research_descendants = property(get_interest_more_research_descendants, set_interest_more_research_descendants, del_interest_more_research_descendants, "interest_more_research_descendants's docstring")
    permanent_record_file_number = property(get_permanent_record_file_number, set_permanent_record_file_number, del_permanent_record_file_number, "permanent_record_file_number's docstring")
    ancestral_file_number = property(get_ancestral_file_number, set_ancestral_file_number, del_ancestral_file_number, "ancestral_file_number's docstring")
    user_reference_numbers = property(get_user_reference_numbers, set_user_reference_numbers, del_user_reference_numbers, "user_reference_numbers's docstring")
    automated_record_id = property(get_automated_record_id, set_automated_record_id, del_automated_record_id, "automated_record_id's docstring")
    change_date = property(get_change_date, set_change_date, del_change_date, "change_date's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    sources = property(get_sources, set_sources, del_sources, "sources's docstring")
    multimedia_links = property(get_multimedia_links, set_multimedia_links, del_multimedia_links, "multimedia_links's docstring")

class Multimedia(Record):
    def __init__(self):
        self.__reference = ""
        self.__file = ""
        self.__file_format = ""
        self.__file_format_type = ""
        self.__file_title = ""
        self.__user_reference_numbers = []
        self.__automated_record_id = ""
        self.__change_date = None
        self.__notes = []
        self.__sources = []
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_file(self):
        return self.__file


    def get_file_format(self):
        return self.__file_format


    def get_file_format_type(self):
        return self.__file_format_type


    def get_file_title(self):
        return self.__file_title


    def get_user_reference_numbers(self):
        return self.__user_reference_numbers


    def get_automated_record_id(self):
        return self.__automated_record_id


    def get_change_date(self):
        return self.__change_date


    def get_notes(self):
        return self.__notes


    def get_sources(self):
        return self.__sources


    def set_reference(self, value):
        self.__reference = value


    def set_file(self, value):
        self.__file = value


    def set_file_format(self, value):
        self.__file_format = value


    def set_file_format_type(self, value):
        self.__file_format_type = value


    def set_file_title(self, value):
        self.__file_title = value


    def set_user_reference_numbers(self, value):
        self.__user_reference_numbers = value


    def set_automated_record_id(self, value):
        self.__automated_record_id = value


    def set_change_date(self, value):
        self.__change_date = value


    def set_notes(self, value):
        self.__notes = value


    def set_sources(self, value):
        self.__sources = value


    def del_reference(self):
        del self.__reference


    def del_file(self):
        del self.__file


    def del_file_format(self):
        del self.__file_format


    def del_file_format_type(self):
        del self.__file_format_type


    def del_file_title(self):
        del self.__file_title


    def del_user_reference_numbers(self):
        del self.__user_reference_numbers


    def del_automated_record_id(self):
        del self.__automated_record_id


    def del_change_date(self):
        del self.__change_date


    def del_notes(self):
        del self.__notes


    def del_sources(self):
        del self.__sources

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        index = 0
        starting_level = relevant_lines[0].level
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_FILE:
                self.__file = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_FORMAT and line.level==starting_level+2:
                self.__file_format = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_TYPE and line.level==starting_level+3:
                self.__file_format_type = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_TITLE and line.level==starting_level+2:
                self.__file_title = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_REFERENCE:
                if gedcom_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_TYPE:
                    self.__user_reference_numbers.append((gedcom_lines[index].value, gedcom_lines[index+1].value))
                    index += 1
                else:
                    self.__user_reference_numbers.append((gedcom_lines[index].value, ""))
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER:
                self.__automated_record_id = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level+1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_SOURCE and line.level == starting_level+1:
                source = SourceCitation()
                parsed_lines = source.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__sources.append(source)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE:
                change_date = ChangeDate()
                parsed_lines = change_date.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__change_date = change_date
                    index += parsed_lines
                    continue
            elif  line.is_user_defined_tag():
                # current implementation ignores the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
                    continue
            index += 1
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level=0):
        gedcom_repr = "%s %s %s" % (level, self.__reference, gedcom.tags.GEDCOM_TAG_OBJECT)
        if self.__file:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_FILE, self.__file)
        if self.__file_format:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_FORMAT, self.__file_format)
        if self.__file_format_type:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+3, gedcom.tags.GEDCOM_TAG_TYPE, self.__file_format_type)
        if self.__file_title:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_TITLE, self.__file_title)
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
        return gedcom_repr
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    file = property(get_file, set_file, del_file, "file's docstring")
    file_format = property(get_file_format, set_file_format, del_file_format, "file_format's docstring")
    file_format_type = property(get_file_format_type, set_file_format_type, del_file_format_type, "file_format_type's docstring")
    file_title = property(get_file_title, set_file_title, del_file_title, "file_title's docstring")
    user_reference_numbers = property(get_user_reference_numbers, set_user_reference_numbers, del_user_reference_numbers, "user_reference_numbers's docstring")
    automated_record_id = property(get_automated_record_id, set_automated_record_id, del_automated_record_id, "automated_record_id's docstring")
    change_date = property(get_change_date, set_change_date, del_change_date, "change_date's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    sources = property(get_sources, set_sources, del_sources, "sources's docstring")

class Note(Record):
    def __init__(self):
        self.__reference = ""
        self.__text = ""
        self.__user_reference_numbers = []
        self.__automated_record_id = ""
        self.__change_date = None
        self.__sources = []
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_text(self):
        return self.__text


    def get_user_reference_numbers(self):
        return self.__user_reference_numbers


    def get_automated_record_id(self):
        return self.__automated_record_id


    def get_change_date(self):
        return self.__change_date


    def get_sources(self):
        return self.__sources


    def set_reference(self, value):
        self.__reference = value


    def set_text(self, value):
        self.__text = value


    def set_user_reference_numbers(self, value):
        self.__user_reference_numbers = value


    def set_automated_record_id(self, value):
        self.__automated_record_id = value


    def set_change_date(self, value):
        self.__change_date = value


    def set_sources(self, value):
        self.__sources = value


    def del_reference(self):
        del self.__reference


    def del_text(self):
        del self.__text


    def del_user_reference_numbers(self):
        del self.__user_reference_numbers


    def del_automated_record_id(self):
        del self.__automated_record_id


    def del_change_date(self):
        del self.__change_date


    def del_sources(self):
        del self.__sources

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        index = 0
        starting_level = relevant_lines[0].level      
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level:
                self.__text = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and line.level == starting_level+1:
                self.__text += line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_CONTINUED and line.level == starting_level+1:
                self.__text = self.__text + "\n" + line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_REFERENCE:
                if gedcom_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_TYPE:
                    self.__user_reference_numbers.append((gedcom_lines[index].value, gedcom_lines[index+1].value))
                    index += 1
                else:
                    self.__user_reference_numbers.append((gedcom_lines[index].value, ""))
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER:
                self.__automated_record_id = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level+1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_SOURCE and line.level == starting_level+1:
                source = SourceCitation()
                parsed_lines = source.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__sources.append(source)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE:
                change_date = ChangeDate()
                parsed_lines = change_date.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__change_date = change_date
                    index += parsed_lines
                    continue
            elif  line.is_user_defined_tag():
                # current implementation ignores the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
                    continue
            index += 1
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level=0):
        gedcom_repr = gedcom.gedcom_file.split_text_for_gedcom(self.__text, gedcom.tags.GEDCOM_TAG_NOTE, level, gedcom.tags.MAX_TEXT_LENGTH)
        gedcom_repr = gedcom_repr[0:gedcom_repr.find(' ')] + " " + self.__reference + " " + gedcom_repr[gedcom_repr.find(' ')+1:]
        for user_reference_number in self.__user_reference_numbers:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REFERENCE, user_reference_number[0])
            if user_reference_number[1]:
                gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_TYPE, user_reference_number[1])
        if self.__automated_record_id:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER, self.__automated_record_id)
        if self.__change_date:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__change_date.get_gedcom_repr(level+1))
        for source_citation in self.__sources:
            gedcom_repr = "%s\n%s" % (gedcom_repr, source_citation.get_gedcom_repr(level+1))
        return gedcom_repr
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    text = property(get_text, set_text, del_text, "text's docstring")
    user_reference_numbers = property(get_user_reference_numbers, set_user_reference_numbers, del_user_reference_numbers, "user_reference_numbers's docstring")
    automated_record_id = property(get_automated_record_id, set_automated_record_id, del_automated_record_id, "automated_record_id's docstring")
    change_date = property(get_change_date, set_change_date, del_change_date, "change_date's docstring")
    sources = property(get_sources, set_sources, del_sources, "sources's docstring")

class Repository(Record):
    def __init__(self):
        self.__reference = ""
        self.__repository_name = ""
        self.__address = None
        self.__notes = []
        self.__user_reference_numbers = []
        self.__automated_record_id = ""
        self.__change_date = None
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_repository_name(self):
        return self.__repository_name


    def get_address(self):
        return self.__address


    def get_notes(self):
        return self.__notes


    def get_user_reference_numbers(self):
        return self.__user_reference_numbers


    def get_automated_record_id(self):
        return self.__automated_record_id


    def get_change_date(self):
        return self.__change_date


    def set_reference(self, value):
        self.__reference = value


    def set_repository_name(self, value):
        self.__repository_name = value


    def set_address(self, value):
        self.__address = value


    def set_notes(self, value):
        self.__notes = value


    def set_user_reference_numbers(self, value):
        self.__user_reference_numbers = value


    def set_automated_record_id(self, value):
        self.__automated_record_id = value


    def set_change_date(self, value):
        self.__change_date = value


    def del_reference(self):
        del self.__reference


    def del_repository_name(self):
        del self.__repository_name


    def del_address(self):
        del self.__address


    def del_notes(self):
        del self.__notes


    def del_user_reference_numbers(self):
        del self.__user_reference_numbers


    def del_automated_record_id(self):
        del self.__automated_record_id


    def del_change_date(self):
        del self.__change_date

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        index = 0
        starting_level = relevant_lines[0].level      
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_NAME and line.level == starting_level+1:
                self.__repository_name = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_ADDRESS and line.level == starting_level+1:
                address = AddressStructure()
                parsed_lines = address.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__address = address
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level+1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue    
            elif line.tag == gedcom.tags.GEDCOM_TAG_REFERENCE:
                if gedcom_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_TYPE:
                    self.__user_reference_numbers.append((gedcom_lines[index].value, gedcom_lines[index+1].value))
                    index += 1
                else:
                    self.__user_reference_numbers.append((gedcom_lines[index].value, ""))
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER:
                self.__automated_record_id = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER and line.level == starting_level+1:
                self.__automated_record_id = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE:
                change_date = ChangeDate()
                parsed_lines = change_date.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__change_date = change_date
                    index += parsed_lines
                    continue
            elif  line.is_user_defined_tag():
                # current implementation ignores the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
                    continue
            index += 1
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level=0):
        gedcom_repr = "%s %s %s" % (level, self.__reference, gedcom.tags.GEDCOM_TAG_REPOSITORY)
        gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_NAME, self.__repository_name)
        if self.__address:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__address.get_gedcom_repr(level+1))
        for note_structure in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note_structure.get_gedcom_repr(level+1))
        for user_reference_number in self.__user_reference_numbers:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REFERENCE, user_reference_number[0])
            if user_reference_number[1]:
                gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_TYPE, user_reference_number[1])
        if self.__automated_record_id:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER, self.__automated_record_id)
        if self.__change_date:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__change_date.get_gedcom_repr(level+1))
        return gedcom_repr
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    repository_name = property(get_repository_name, set_repository_name, del_repository_name, "repository_name's docstring")
    address = property(get_address, set_address, del_address, "address's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    user_reference_numbers = property(get_user_reference_numbers, set_user_reference_numbers, del_user_reference_numbers, "user_reference_numbers's docstring")
    automated_record_id = property(get_automated_record_id, set_automated_record_id, del_automated_record_id, "automated_record_id's docstring")
    change_date = property(get_change_date, set_change_date, del_change_date, "change_date's docstring")

class SourceEvent(Record):
    def __init__(self):
        self.__event_recorded = ""
        self.__event_date = ""
        self.__event_place = ""
        super().__init__()

    def get_event_recorded(self):
        return self.__event_recorded


    def get_event_date(self):
        return self.__event_date


    def get_event_place(self):
        return self.__event_place


    def set_event_recorded(self, value):
        self.__event_recorded = value


    def set_event_date(self, value):
        self.__event_date = value


    def set_event_place(self, value):
        self.__event_place = value


    def del_event_recorded(self):
        del self.__event_recorded


    def del_event_date(self):
        del self.__event_date


    def del_event_place(self):
        del self.__event_place

        
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        index = 0
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_EVENT:
                self.__event_recorded = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_DATE:
                self.__event_date = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_PLACE:
                self.__event_place = line.value
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s %s" % (level, gedcom.tags.GEDCOM_TAG_EVENT, self.__event_recorded)
        if self.__event_date:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_DATE, self.__event_date)     
        if self.__event_place:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_PLACE, self.__event_place)
        return gedcom_repr 
    event_recorded = property(get_event_recorded, set_event_recorded, del_event_recorded, "event_recorded's docstring")
    event_date = property(get_event_date, set_event_date, del_event_date, "event_date's docstring")
    event_place = property(get_event_place, set_event_place, del_event_place, "event_place's docstring")

class Source(Record):
    def __init__(self):
        self.__reference = ""
        self.__data_tag = ""
        self.__data_events = []
        self.__data_responsible_agency = ""
        self.__data_notes = []
        self.__source_originator = ""
        self.__source_title = ""
        self.__source_filled_by = ""
        self.__source_publication_facts = ""
        self.__text_from_source = ""
        self.__source_repository_citations = []
        self.__user_reference_numbers = []
        self.__automated_record_id = ""
        self.__change_date = None
        self.__notes = []
        self.__multimedia_links = []
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_data_tag(self):
        return self.__data_tag


    def get_data_events(self):
        return self.__data_events


    def get_data_responsible_agency(self):
        return self.__data_responsible_agency


    def get_data_notes(self):
        return self.__data_notes


    def get_source_originator(self):
        return self.__source_originator


    def get_source_title(self):
        return self.__source_title


    def get_source_filled_by(self):
        return self.__source_filled_by


    def get_source_publication_facts(self):
        return self.__source_publication_facts


    def get_text_from_source(self):
        return self.__text_from_source


    def get_source_repository_citations(self):
        return self.__source_repository_citations


    def get_user_reference_numbers(self):
        return self.__user_reference_numbers


    def get_automated_record_id(self):
        return self.__automated_record_id


    def get_change_date(self):
        return self.__change_date


    def get_notes(self):
        return self.__notes


    def get_multimedia_links(self):
        return self.__multimedia_links


    def set_reference(self, value):
        self.__reference = value


    def set_data_tag(self, value):
        self.__data_tag = value


    def set_data_events(self, value):
        self.__data_events = value


    def set_data_responsible_agency(self, value):
        self.__data_responsible_agency = value


    def set_data_notes(self, value):
        self.__data_notes = value


    def set_source_originator(self, value):
        self.__source_originator = value


    def set_source_title(self, value):
        self.__source_title = value


    def set_source_filled_by(self, value):
        self.__source_filled_by = value


    def set_source_publication_facts(self, value):
        self.__source_publication_facts = value


    def set_text_from_source(self, value):
        self.__text_from_source = value


    def set_source_repository_citations(self, value):
        self.__source_repository_citations = value


    def set_user_reference_numbers(self, value):
        self.__user_reference_numbers = value


    def set_automated_record_id(self, value):
        self.__automated_record_id = value


    def set_change_date(self, value):
        self.__change_date = value


    def set_notes(self, value):
        self.__notes = value


    def set_multimedia_links(self, value):
        self.__multimedia_links = value


    def del_reference(self):
        del self.__reference


    def del_data_tag(self):
        del self.__data_tag


    def del_data_events(self):
        del self.__data_events


    def del_data_responsible_agency(self):
        del self.__data_responsible_agency


    def del_data_notes(self):
        del self.__data_notes


    def del_source_originator(self):
        del self.__source_originator


    def del_source_title(self):
        del self.__source_title


    def del_source_filled_by(self):
        del self.__source_filled_by


    def del_source_publication_facts(self):
        del self.__source_publication_facts


    def del_text_from_source(self):
        del self.__text_from_source


    def del_source_repository_citations(self):
        del self.__source_repository_citations


    def del_user_reference_numbers(self):
        del self.__user_reference_numbers


    def del_automated_record_id(self):
        del self.__automated_record_id


    def del_change_date(self):
        del self.__change_date


    def del_notes(self):
        del self.__notes


    def del_multimedia_links(self):
        del self.__multimedia_links

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        index = 0
        starting_level = relevant_lines[0].level      
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            tag = line.tag
            level = line.level
            if tag == gedcom.tags.GEDCOM_TAG_DATA and level == starting_level+1:
                scope = gedcom.tags.GEDCOM_TAG_DATA
                self.__data_tag = "Y"
            elif tag == gedcom.tags.GEDCOM_TAG_EVENT and scope == gedcom.tags.GEDCOM_TAG_DATA:
                source_event = SourceEvent()
                parsed_lines = source_event.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__data_events.append(source_event)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_AGENCY and scope == gedcom.tags.GEDCOM_TAG_DATA and level == starting_level+2:
                self.__data_responsible_agency = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_NOTE and scope == gedcom.tags.GEDCOM_TAG_DATA and level == starting_level+2:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__data_notes.append(note)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_AUTHOR and level == starting_level+1:
                scope = gedcom.tags.GEDCOM_TAG_AUTHOR
                self.__source_originator = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and scope == gedcom.tags.GEDCOM_TAG_AUTHOR and level == starting_level+2:
                self.__source_originator += line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and scope == gedcom.tags.GEDCOM_TAG_AUTHOR and level == starting_level+2:
                self.__source_originator = self.__source_originator + "\n" + line.value
            elif tag == gedcom.tags.GEDCOM_TAG_TITLE and level == starting_level+1:
                scope = gedcom.tags.GEDCOM_TAG_TITLE
                self.__source_title = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and scope == gedcom.tags.GEDCOM_TAG_TITLE and level == starting_level+2:
                self.__source_title += line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and scope == gedcom.tags.GEDCOM_TAG_TITLE and level == starting_level+2:
                self.__source_title = self.__source_title + "\n" + line.value
            elif tag == gedcom.tags.GEDCOM_TAG_PUBLICATION and level == starting_level+1:
                scope = gedcom.tags.GEDCOM_TAG_PUBLICATION
                self.__source_publication_facts = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and scope == gedcom.tags.GEDCOM_TAG_PUBLICATION and level == starting_level+2:
                self.__source_publication_facts += line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and scope == gedcom.tags.GEDCOM_TAG_PUBLICATION and level == starting_level+2:
                self.__source_publication_facts = self.__source_publication_facts + "\n" + line.value
            elif tag == gedcom.tags.GEDCOM_TAG_NAME_ABBREVIATION and level == starting_level+1:
                self.__source_filled_by = line.value
                scope = ""
            elif tag == gedcom.tags.GEDCOM_TAG_TEXT and level == starting_level+1:
                scope = gedcom.tags.GEDCOM_TAG_TEXT
                self.__text_from_source = line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONCATENATION and scope == gedcom.tags.GEDCOM_TAG_TEXT and level == starting_level+2:
                self.__text_from_source += line.value
            elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED and scope == gedcom.tags.GEDCOM_TAG_TEXT and level == starting_level+2:
                self.__text_from_source = self.__text_from_source + "\n" + line.value
            elif line.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE and line.value == starting_level+1:
                scope = ""
                source = SourceCitation()
                parsed_lines = source.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__sources.append(source)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_REFERENCE:
                if gedcom_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_TYPE:
                    self.__user_reference_numbers.append((gedcom_lines[index].value, gedcom_lines[index+1].value))
                    index += 1
                else:
                    self.__user_reference_numbers.append((gedcom_lines[index].value, ""))
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER:
                scope = ""
                self.__automated_record_id = line.value    
            elif line.get_tag() == gedcom.tags.GEDCOM_TAG_NOTE and line.get_level() == starting_level+1:
                scope = ""
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            elif tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE:
                scope = ""
                change_date = ChangeDate()
                parsed_lines = change_date.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__change_date = change_date
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_OBJECT and line.level == starting_level+1:
                scope = ""
                multimedia = MultimediaLink()
                parsed_lines = multimedia.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__multimedia_links.append(multimedia)
                    index += parsed_lines
                    continue 
            elif  line.is_user_defined_tag():
                # current implementation ignores the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
                    continue
            index += 1
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level=0):
        gedcom_repr = "%s %s %s" % (level, self.__reference, gedcom.tags.GEDCOM_TAG_SOURCE)
        if self.__data_tag:
            gedcom_repr = "%s\n%s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_DATA)
        for source_event in self.__data_events:
            gedcom_repr = "%s\n%s" % (gedcom_repr, source_event.get_gedcom_repr(level+2))
        if self.__data_responsible_agency:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+2, gedcom.tags.GEDCOM_TAG_AGENCY, self.__data_responsible_agency)
        for note in self.__data_notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note.get_gedcom_repr(level+2))
        if self.__source_originator:
            gedcom_repr = "%s\n%s" % (gedcom_repr, gedcom.gedcom_file.split_text_for_gedcom(self.__source_originator, gedcom.tags.GEDCOM_TAG_AUTHOR, level+1, gedcom.tags.MAX_TEXT_LENGTH))
        if self.__source_title:
            gedcom_repr = "%s\n%s" % (gedcom_repr, gedcom.gedcom_file.split_text_for_gedcom(self.__source_title, gedcom.tags.GEDCOM_TAG_TITLE, level+1, gedcom.tags.MAX_TEXT_LENGTH))
        if self.__source_filled_by:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_NAME_ABBREVIATION, self.__source_filled_by)
        if self.__source_publication_facts:
            gedcom_repr = "%s\n%s" % (gedcom_repr, gedcom.gedcom_file.split_text_for_gedcom(self.__source_publication_facts, gedcom.tags.GEDCOM_TAG_PUBLICATION, level+1, gedcom.tags.MAX_TEXT_LENGTH))
        if self.__text_from_source:
            gedcom_repr = "%s\n%s" % (gedcom_repr, gedcom.gedcom_file.split_text_for_gedcom(self.__text_from_source, gedcom.tags.GEDCOM_TAG_TEXT, level+1, gedcom.tags.MAX_TEXT_LENGTH))
        for source in self.__source_repository_citations:
            gedcom_repr = "%s\n%s" % (gedcom_repr, source.get_gedcom_repr(level+1))
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
        for multimedia_link in self.__multimedia_links:
            gedcom_repr = "%s\n%s" % (gedcom_repr, multimedia_link.get_gedcom_repr(level+1))
        return gedcom_repr
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    data_tag = property(get_data_tag, set_data_tag, del_data_tag, "data_tag's docstring")
    data_events = property(get_data_events, set_data_events, del_data_events, "data_events's docstring")
    data_responsible_agency = property(get_data_responsible_agency, set_data_responsible_agency, del_data_responsible_agency, "data_responsible_agency's docstring")
    data_notes = property(get_data_notes, set_data_notes, del_data_notes, "data_notes's docstring")
    source_originator = property(get_source_originator, set_source_originator, del_source_originator, "source_originator's docstring")
    source_title = property(get_source_title, set_source_title, del_source_title, "source_title's docstring")
    source_filled_by = property(get_source_filled_by, set_source_filled_by, del_source_filled_by, "source_filled_by's docstring")
    source_publication_facts = property(get_source_publication_facts, set_source_publication_facts, del_source_publication_facts, "source_publication_facts's docstring")
    text_from_source = property(get_text_from_source, set_text_from_source, del_text_from_source, "text_from_source's docstring")
    source_repository_citations = property(get_source_repository_citations, set_source_repository_citations, del_source_repository_citations, "source_repository_citations's docstring")
    user_reference_numbers = property(get_user_reference_numbers, set_user_reference_numbers, del_user_reference_numbers, "user_reference_numbers's docstring")
    automated_record_id = property(get_automated_record_id, set_automated_record_id, del_automated_record_id, "automated_record_id's docstring")
    change_date = property(get_change_date, set_change_date, del_change_date, "change_date's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    multimedia_links = property(get_multimedia_links, set_multimedia_links, del_multimedia_links, "multimedia_links's docstring")

class Submission(Record):
    def __init__(self):
        self.__reference = ""
        self.__submitter_reference = ""
        self.__family_file = ""
        self.__temple_code = ""
        self.__ancestors_generations = ""
        self.__descendands_generations = ""
        self.__ordinance_process_flag = ""
        self.__automaed_record_id = ""
        self.__notes = []
        self.__change_date = None
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_submitter_reference(self):
        return self.__submitter_reference


    def get_family_file(self):
        return self.__family_file


    def get_temple_code(self):
        return self.__temple_code


    def get_ancestors_generations(self):
        return self.__ancestors_generations


    def get_descendands_generations(self):
        return self.__descendands_generations


    def get_ordinance_process_flag(self):
        return self.__ordinance_process_flag


    def get_automaed_record_id(self):
        return self.__automaed_record_id


    def get_notes(self):
        return self.__notes


    def get_change_date(self):
        return self.__change_date


    def set_reference(self, value):
        self.__reference = value


    def set_submitter_reference(self, value):
        self.__submitter_reference = value


    def set_family_file(self, value):
        self.__family_file = value


    def set_temple_code(self, value):
        self.__temple_code = value


    def set_ancestors_generations(self, value):
        self.__ancestors_generations = value


    def set_descendands_generations(self, value):
        self.__descendands_generations = value


    def set_ordinance_process_flag(self, value):
        self.__ordinance_process_flag = value


    def set_automaed_record_id(self, value):
        self.__automaed_record_id = value


    def set_notes(self, value):
        self.__notes = value


    def set_change_date(self, value):
        self.__change_date = value


    def del_reference(self):
        del self.__reference


    def del_submitter_reference(self):
        del self.__submitter_reference


    def del_family_file(self):
        del self.__family_file


    def del_temple_code(self):
        del self.__temple_code


    def del_ancestors_generations(self):
        del self.__ancestors_generations


    def del_descendands_generations(self):
        del self.__descendands_generations


    def del_ordinance_process_flag(self):
        del self.__ordinance_process_flag


    def del_automaed_record_id(self):
        del self.__automaed_record_id


    def del_notes(self):
        del self.__notes


    def del_change_date(self):
        del self.__change_date

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        index = 0
        starting_level = relevant_lines[0].level
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_SUBMITTER:
                self.__submitter_reference = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_FAMILY_FILE:
                self.__family_file = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_LSD_TEMPLE:
                self.__temple_code = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_ANCESTORS:
                self.__ancestors_generations = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_DESCENDANTS:
                self.__descendands_generations = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_ORDINANCE:
                self.__ordinance_process_flag = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER:
                self.__automaed_record_id = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level+1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE and line.level == starting_level+1:
                change_date = ChangeDate()
                parsed_lines = change_date.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__change_date = change_date
                    index += parsed_lines
                    continue
            elif  line.is_user_defined_tag():
                # current implementation ignores the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
                    continue
            index += 1
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level=0):
        gedcom_repr = "%s %s %s" % (level, self.__reference, gedcom.tags.GEDCOM_TAG_SUBMISSION)
        if self.__submitter_reference:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_SUBMITTER, self.__submitter_reference)
        if self.__family_file:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_FAMILY_FILE, self.__family_file)
        if self.__temple_code:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_LSD_TEMPLE, self.__temple_code)
        if self.__ancestors_generations:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_ANCESTORS, self.__ancestors_generations)
        if self.__descendands_generations:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_DESCENDANTS, self.__descendands_generations)
        if self.__ordinance_process_flag:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_ORDINANCE, self.__ordinance_process_flag)
        if self.__automaed_record_id:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER, self.__automaed_record_id)
        for note in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note.get_gedcom_repr(level+1))
        if self.__change_date:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__change_date.get_gedcom_repr(level+1))
        return gedcom_repr.strip()
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    submitter_reference = property(get_submitter_reference, set_submitter_reference, del_submitter_reference, "submitter_reference's docstring")
    family_file = property(get_family_file, set_family_file, del_family_file, "family_file's docstring")
    temple_code = property(get_temple_code, set_temple_code, del_temple_code, "temple_code's docstring")
    ancestors_generations = property(get_ancestors_generations, set_ancestors_generations, del_ancestors_generations, "ancestors_generations's docstring")
    descendands_generations = property(get_descendands_generations, set_descendands_generations, del_descendands_generations, "descendands_generations's docstring")
    ordinance_process_flag = property(get_ordinance_process_flag, set_ordinance_process_flag, del_ordinance_process_flag, "ordinance_process_flag's docstring")
    automaed_record_id = property(get_automaed_record_id, set_automaed_record_id, del_automaed_record_id, "automaed_record_id's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    change_date = property(get_change_date, set_change_date, del_change_date, "change_date's docstring")

class Submitter(Record):
    def __init__(self):
        self.__reference = ""
        self.__submitter_name = ""
        self.__address = None
        self.__multimedia_links = []
        self.__language_preferences = []
        self.__submitter_registered_rfn = ""
        self.__automated_record_id = ""
        self.__notes = []
        self.__change_date = None
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_submitter_name(self):
        return self.__submitter_name


    def get_address(self):
        return self.__address


    def get_multimedia_links(self):
        return self.__multimedia_links


    def get_language_preferences(self):
        return self.__language_preferences


    def get_submitter_registered_rfn(self):
        return self.__submitter_registered_rfn


    def get_automated_record_id(self):
        return self.__automated_record_id


    def get_notes(self):
        return self.__notes


    def get_change_date(self):
        return self.__change_date


    def set_reference(self, value):
        self.__reference = value


    def set_submitter_name(self, value):
        self.__submitter_name = value


    def set_address(self, value):
        self.__address = value


    def set_multimedia_links(self, value):
        self.__multimedia_links = value


    def set_language_preferences(self, value):
        self.__language_preferences = value


    def set_submitter_registered_rfn(self, value):
        self.__submitter_registered_rfn = value


    def set_automated_record_id(self, value):
        self.__automated_record_id = value


    def set_notes(self, value):
        self.__notes = value


    def set_change_date(self, value):
        self.__change_date = value


    def del_reference(self):
        del self.__reference


    def del_submitter_name(self):
        del self.__submitter_name


    def del_address(self):
        del self.__address


    def del_multimedia_links(self):
        del self.__multimedia_links


    def del_language_preferences(self):
        del self.__language_preferences


    def del_submitter_registered_rfn(self):
        del self.__submitter_registered_rfn


    def del_automated_record_id(self):
        del self.__automated_record_id


    def del_notes(self):
        del self.__notes


    def del_change_date(self):
        del self.__change_date

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__reference = relevant_lines[0].pointer
        index = 0
        starting_level = relevant_lines[0].level
        while index < len(relevant_lines):
            line = gedcom_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_NAME and line.level == starting_level+1:
                self.__submitter_name = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_ADDRESS and line.level == starting_level+1:
                address = AddressStructure()
                parsed_lines = address.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__address = address
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_OBJECT and line.level == starting_level+1:
                multimedia = MultimediaLink()
                parsed_lines = multimedia.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__multimedia_links.append(multimedia)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_LANGUAGE and line.level == starting_level+1:
                self.__language_preferences.append(line.value)
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_FILE_NUMBER and line.level == starting_level+1:
                self.__submitter_registered_rfn = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER and line.level == starting_level+1:
                self.__automated_record_id = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level+1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            elif line.tag == gedcom.tags.GEDCOM_TAG_DATE_CHANGE:
                change_date = ChangeDate()
                parsed_lines = change_date.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__change_date = change_date
                    index += parsed_lines
                    continue
            elif  line.is_user_defined_tag():
                # current implementation ignores the user defined tags
                record = Record()
                parsed_lines = record.get_relevant_lines(relevant_lines[index:])
                if parsed_lines:
                    index += len(parsed_lines)
                    continue
            index += 1
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level=0):
        gedcom_repr = "%s %s %s" % (level, self.__reference, gedcom.tags.GEDCOM_TAG_SUBMITTER)
        gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_NAME, self.__submitter_name)
        if self.__address:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__address.get_gedcom_repr(level+1))
        for multimedia_link in self.__multimedia_links:
            gedcom_repr = "%s\n%s" % (gedcom_repr, multimedia_link.get_gedcom_repr(level+1))
        for language in self.__language_preferences:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_LANGUAGE, language)
        if self.__submitter_registered_rfn:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REC_FILE_NUMBER, self.__submitter_registered_rfn)
        if self.__automated_record_id:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_REC_ID_NUMBER, self.__automated_record_id)
        for note_structure in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note_structure.get_gedcom_repr(level+1))
        if self.__change_date:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__change_date.get_gedcom_repr(level+1))
        return gedcom_repr
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    submitter_name = property(get_submitter_name, set_submitter_name, del_submitter_name, "submitter_name's docstring")
    address = property(get_address, set_address, del_address, "address's docstring")
    multimedia_links = property(get_multimedia_links, set_multimedia_links, del_multimedia_links, "multimedia_links's docstring")
    language_preferences = property(get_language_preferences, set_language_preferences, del_language_preferences, "language_preferences's docstring")
    submitter_registered_rfn = property(get_submitter_registered_rfn, set_submitter_registered_rfn, del_submitter_registered_rfn, "submitter_registered_rfn's docstring")
    automated_record_id = property(get_automated_record_id, set_automated_record_id, del_automated_record_id, "automated_record_id's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    change_date = property(get_change_date, set_change_date, del_change_date, "change_date's docstring")

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

    def get_address_line(self):
        return self.__address_line


    def get_address_line_1(self):
        return self.__address_line1


    def get_address_line_2(self):
        return self.__address_line2


    def get_address_line_3(self):
        return self.__address_line3


    def get_address_city(self):
        return self.__address_city


    def get_address_state(self):
        return self.__address_state


    def get_address_postal_code(self):
        return self.__address_postal_code


    def get_address_country(self):
        return self.__address_country


    def get_phone_number(self):
        return self.__phone_number


    def get_address_email(self):
        return self.__address_email


    def get_address_fax(self):
        return self.__address_fax


    def get_address_web_page(self):
        return self.__address_web_page


    def set_address_line(self, value):
        self.__address_line = value


    def set_address_line_1(self, value):
        self.__address_line1 = value


    def set_address_line_2(self, value):
        self.__address_line2 = value


    def set_address_line_3(self, value):
        self.__address_line3 = value


    def set_address_city(self, value):
        self.__address_city = value


    def set_address_state(self, value):
        self.__address_state = value


    def set_address_postal_code(self, value):
        self.__address_postal_code = value


    def set_address_country(self, value):
        self.__address_country = value


    def set_phone_number(self, value):
        self.__phone_number = value


    def set_address_email(self, value):
        self.__address_email = value


    def set_address_fax(self, value):
        self.__address_fax = value


    def set_address_web_page(self, value):
        self.__address_web_page = value


    def del_address_line(self):
        del self.__address_line


    def del_address_line_1(self):
        del self.__address_line1


    def del_address_line_2(self):
        del self.__address_line2


    def del_address_line_3(self):
        del self.__address_line3


    def del_address_city(self):
        del self.__address_city


    def del_address_state(self):
        del self.__address_state


    def del_address_postal_code(self):
        del self.__address_postal_code


    def del_address_country(self):
        del self.__address_country


    def del_phone_number(self):
        del self.__phone_number


    def del_address_email(self):
        del self.__address_email


    def del_address_fax(self):
        del self.__address_fax


    def del_address_web_page(self):
        del self.__address_web_page

    
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
        gedcom_repr = gedcom.gedcom_file.split_text_for_gedcom(self.__address_line, gedcom.tags.GEDCOM_TAG_ADDRESS, level, gedcom.tags.MAX_TEXT_LENGTH)
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
    address_line = property(get_address_line, set_address_line, del_address_line, "address_line's docstring")
    address_line1 = property(get_address_line_1, set_address_line_1, del_address_line_1, "address_line1's docstring")
    address_line2 = property(get_address_line_2, set_address_line_2, del_address_line_2, "address_line2's docstring")
    address_line3 = property(get_address_line_3, set_address_line_3, del_address_line_3, "address_line3's docstring")
    address_city = property(get_address_city, set_address_city, del_address_city, "address_city's docstring")
    address_state = property(get_address_state, set_address_state, del_address_state, "address_state's docstring")
    address_postal_code = property(get_address_postal_code, set_address_postal_code, del_address_postal_code, "address_postal_code's docstring")
    address_country = property(get_address_country, set_address_country, del_address_country, "address_country's docstring")
    phone_number = property(get_phone_number, set_phone_number, del_phone_number, "phone_number's docstring")
    address_email = property(get_address_email, set_address_email, del_address_email, "address_email's docstring")
    address_fax = property(get_address_fax, set_address_fax, del_address_fax, "address_fax's docstring")
    address_web_page = property(get_address_web_page, set_address_web_page, del_address_web_page, "address_web_page's docstring")

class ChangeDate(Record):
    def __init__(self):
        self.__date = ""
        self.__time = ""
        self.__notes = []
        super().__init__()

    def get_date(self):
        return self.__date


    def get_time(self):
        return self.__time


    def get_notes(self):
        return self.__notes


    def set_date(self, value):
        self.__date = value


    def set_time(self, value):
        self.__time = value


    def set_notes(self, value):
        self.__notes = value


    def del_date(self):
        del self.__date


    def del_time(self):
        del self.__time


    def del_notes(self):
        del self.__notes


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
    date = property(get_date, set_date, del_date, "date's docstring")
    time = property(get_time, set_time, del_time, "time's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")

class ChildToFamilyLink(Record):
    def __init__(self):
        self.__family_reference = ""
        self.__pedigree = ""
        self.__status = ""
        self.__notes = []
        super().__init__()

    def get_family_reference(self):
        return self.__family_reference


    def get_pedigree(self):
        return self.__pedigree


    def get_status(self):
        return self.__status


    def get_notes(self):
        return self.__notes


    def set_family_reference(self, value):
        self.__family_reference = value


    def set_pedigree(self, value):
        self.__pedigree = value


    def set_status(self, value):
        self.__status = value


    def set_notes(self, value):
        self.__notes = value


    def del_family_reference(self):
        del self.__family_reference


    def del_pedigree(self):
        del self.__pedigree


    def del_status(self):
        del self.__status


    def del_notes(self):
        del self.__notes


    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__family_reference = relevant_lines[0].value
        index = 0
        starting_level = relevant_lines[0].level
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_PEDIGREE and line.level == starting_level+1:
                self.__pedigree = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_STATUS and line.level == starting_level+1:
                self.__status = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level+1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s %s" % (level, gedcom.tags.GEDCOM_TAG_FAMILY_CHILD, self.__family_reference)
        if self.__pedigree:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_PEDIGREE, self.__pedigree)
        if self.__status:
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_STATUS, self.__status)
        for note_structure in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note_structure.get_gedcom_repr(level+1))
        return gedcom_repr
    family_reference = property(get_family_reference, set_family_reference, del_family_reference, "family_reference's docstring")
    pedigree = property(get_pedigree, set_pedigree, del_pedigree, "pedigree's docstring")
    status = property(get_status, set_status, del_status, "status's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")

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

    def get_type(self):
        return self.__type


    def get_date(self):
        return self.__date


    def get_place_name(self):
        return self.__place_name


    def get_place_hierarchy(self):
        return self.__place_hierarchy


    def get_place_latitude(self):
        return self.__place_latitude


    def get_place_longitude(self):
        return self.__place_longitude


    def get_place_notes(self):
        return self.__place_notes


    def get_address(self):
        return self.__address


    def get_responsible_agency(self):
        return self.__responsible_agency


    def get_religious_affiliation(self):
        return self.__religious_affiliation


    def get_cause(self):
        return self.__cause


    def get_restriction_notice(self):
        return self.__restriction_notice


    def get_notes(self):
        return self.__notes


    def get_sources(self):
        return self.__sources


    def get_multimedia_links(self):
        return self.__multimedia_links


    def set_type(self, value):
        self.__type = value


    def set_date(self, value):
        self.__date = value


    def set_place_name(self, value):
        self.__place_name = value


    def set_place_hierarchy(self, value):
        self.__place_hierarchy = value


    def set_place_latitude(self, value):
        self.__place_latitude = value


    def set_place_longitude(self, value):
        self.__place_longitude = value


    def set_place_notes(self, value):
        self.__place_notes = value


    def set_address(self, value):
        self.__address = value


    def set_responsible_agency(self, value):
        self.__responsible_agency = value


    def set_religious_affiliation(self, value):
        self.__religious_affiliation = value


    def set_cause(self, value):
        self.__cause = value


    def set_restriction_notice(self, value):
        self.__restriction_notice = value


    def set_notes(self, value):
        self.__notes = value


    def set_sources(self, value):
        self.__sources = value


    def set_multimedia_links(self, value):
        self.__multimedia_links = value


    def del_type(self):
        del self.__type


    def del_date(self):
        del self.__date


    def del_place_name(self):
        del self.__place_name


    def del_place_hierarchy(self):
        del self.__place_hierarchy


    def del_place_latitude(self):
        del self.__place_latitude


    def del_place_longitude(self):
        del self.__place_longitude


    def del_place_notes(self):
        del self.__place_notes


    def del_address(self):
        del self.__address


    def del_responsible_agency(self):
        del self.__responsible_agency


    def del_religious_affiliation(self):
        del self.__religious_affiliation


    def del_cause(self):
        del self.__cause


    def del_restriction_notice(self):
        del self.__restriction_notice


    def del_notes(self):
        del self.__notes


    def del_sources(self):
        del self.__sources


    def del_multimedia_links(self):
        del self.__multimedia_links

    
    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines, gedcom.tags.EVENT_DETAIL_TAGS)
        index = 0
        if len(relevant_lines):
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
            elif line.tag == gedcom.tags.GEDCOM_TAG_FORMAT and scope == gedcom.tags.GEDCOM_TAG_PLACE and line.level == starting_level+1:
                self._place_hierarchy = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_LATITUDE and scope == gedcom.tags.GEDCOM_TAG_PLACE and line.level == starting_level+2:
                self._place_latitude = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_LONGITUDE and scope == gedcom.tags.GEDCOM_TAG_PLACE and line.level == starting_level+2:
                self._place_longitude = line.value
            elif line.tag == gedcom.tags.GEDCOM_TAG_NOTE and scope == gedcom.tags.GEDCOM_TAG_PLACE and line.level == starting_level+1:
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
    type = property(get_type, set_type, del_type, "type's docstring")
    date = property(get_date, set_date, del_date, "date's docstring")
    place_name = property(get_place_name, set_place_name, del_place_name, "place_name's docstring")
    place_hierarchy = property(get_place_hierarchy, set_place_hierarchy, del_place_hierarchy, "place_hierarchy's docstring")
    place_latitude = property(get_place_latitude, set_place_latitude, del_place_latitude, "place_latitude's docstring")
    place_longitude = property(get_place_longitude, set_place_longitude, del_place_longitude, "place_longitude's docstring")
    place_notes = property(get_place_notes, set_place_notes, del_place_notes, "place_notes's docstring")
    address = property(get_address, set_address, del_address, "address's docstring")
    responsible_agency = property(get_responsible_agency, set_responsible_agency, del_responsible_agency, "responsible_agency's docstring")
    religious_affiliation = property(get_religious_affiliation, set_religious_affiliation, del_religious_affiliation, "religious_affiliation's docstring")
    cause = property(get_cause, set_cause, del_cause, "cause's docstring")
    restriction_notice = property(get_restriction_notice, set_restriction_notice, del_restriction_notice, "restriction_notice's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    sources = property(get_sources, set_sources, del_sources, "sources's docstring")
    multimedia_links = property(get_multimedia_links, set_multimedia_links, del_multimedia_links, "multimedia_links's docstring")

class FamilyEventDetail(EventDetail):
    def __init__(self):
        self.__husband_age_at_event = ""
        self.__wife_age_at_event = ""
        super().__init__()

    def get_husband_age_at_event(self):
        return self.__husband_age_at_event


    def get_wife_age_at_event(self):
        return self.__wife_age_at_event


    def set_husband_age_at_event(self, value):
        self.__husband_age_at_event = value


    def set_wife_age_at_event(self, value):
        self.__wife_age_at_event = value


    def del_husband_age_at_event(self):
        del self.__husband_age_at_event


    def del_wife_age_at_event(self):
        del self.__wife_age_at_event


    def parse_gedcom(self, gedcom_lines):
        valid_top_level_tags = gedcom.tags.EVENT_DETAIL_TAGS + [gedcom.tags.GEDCOM_TAG_HUSBAND, gedcom.tags.GEDCOM_TAG_WIFE]
        relevant_lines = super().get_relevant_lines(gedcom_lines, valid_top_level_tags)
        index = 0
        scope = ""
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_HUSBAND:
                scope = gedcom.tags.GEDCOM_TAG_HUSBAND
            elif line.tag == gedcom.tags.GEDCOM_TAG_WIFE:
                scope = gedcom.tags.GEDCOM_TAG_WIFE
            elif line.tag == gedcom.tags.GEDCOM_TAG_AGE:
                if scope == gedcom.tags.GEDCOM_TAG_HUSBAND:
                    self.__husband_age_at_event = line.value
                elif scope == gedcom.tags.GEDCOM_TAG_WIFE:
                    self.__wife_age_at_event = line.value
            elif line.tag in gedcom.tags.EVENT_DETAIL_TAGS:
                parsed_lines = super().parse_gedcom(gedcom_lines[index:])
                index += parsed_lines
                continue
            index += 1
        return len(relevant_lines)
    
    def get_gedcom_repr(self, level):
        gedcom_repr = ""
        if self.__husband_age_at_event:
            gedcom_repr = "%s\n%s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_HUSBAND)
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_AGE, self.__husband_age_at_event)
        if self.__wife_age_at_event:
            gedcom_repr = "%s\n%s %s" % (gedcom_repr, level, gedcom.tags.GEDCOM_TAG_WIFE)
            gedcom_repr = "%s\n%s %s %s" % (gedcom_repr, level+1, gedcom.tags.GEDCOM_TAG_AGE, self.__wife_age_at_event)
        return ("%s\n%s" % (gedcom_repr, super().get_gedcom_repr(level))).strip()
    husband_age_at_event = property(get_husband_age_at_event, set_husband_age_at_event, del_husband_age_at_event, "husband_age_at_event's docstring")
    wife_age_at_event = property(get_wife_age_at_event, set_wife_age_at_event, del_wife_age_at_event, "wife_age_at_event's docstring")

class FamilyEventStructure(FamilyEventDetail):
    def __init__(self):
        self.__tag = ""
        self.__married_yes = ""
        self.__event_descriptor = ""
        super().__init__()

    def get_tag(self):
        return self.__tag


    def get_married_yes(self):
        return self.__married_yes


    def get_event_descriptor(self):
        return self.__event_descriptor


    def set_tag(self, value):
        self.__tag = value


    def set_married_yes(self, value):
        self.__married_yes = value


    def set_event_descriptor(self, value):
        self.__event_descriptor = value


    def del_tag(self):
        del self.__tag


    def del_married_yes(self):
        del self.__married_yes


    def del_event_descriptor(self):
        del self.__event_descriptor


    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__tag = relevant_lines[0].tag
        index = 0
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if self.__tag == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                self.__married_yes = relevant_lines[0].value
                if len(relevant_lines) > index+1 and (relevant_lines[index+1].level == line.level+1):
                    parsed_lines = super().parse_gedcom(relevant_lines[index:])
                    index += parsed_lines
                    continue
            elif self.__tag == gedcom.tags.GEDCOM_TAG_EVENT:
                self.__event_descriptor = line.value
                if len(relevant_lines) >= index+1 and (relevant_lines[index+1].level == line.level+1):
                    parsed_lines = super().parse_gedcom(relevant_lines[index:])
                    index += parsed_lines
                    continue
            else:
                parsed_lines = super().parse_gedcom(relevant_lines[index:])
                index += parsed_lines
                continue
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s" % (level, self.__tag)
        if self.__married_yes:
            gedcom_repr = "%s %s" % (gedcom_repr, self.__married_yes)
        elif self.__event_descriptor:
            gedcom_repr = "%s %s" % (gedcom_repr, self.__event_descriptor)
        return ("%s\n%s" % (gedcom_repr, super().get_gedcom_repr(level+1))).strip()
    tag = property(get_tag, set_tag, del_tag, "tag's docstring")
    married_yes = property(get_married_yes, set_married_yes, del_married_yes, "married_yes's docstring")
    event_descriptor = property(get_event_descriptor, set_event_descriptor, del_event_descriptor, "event_descriptor's docstring")

class IndividualEventDetail(EventDetail):
    def __init__(self):
        self._age_at_event = ""
        super().__init__()

    def get_age_at_event(self):
        return self.__age_at_event


    def set_age_at_event(self, value):
        self.__age_at_event = value


    def del_age_at_event(self):
        del self.__age_at_event


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
    age_at_event = property(get_age_at_event, set_age_at_event, del_age_at_event, "age_at_event's docstring")

class IndividualAttributeStructure(IndividualEventDetail):
    def __init__(self):
        self.__tag = ""
        self.__content = ""
        self.__physical_description = ""
        super().__init__()

    def get_tag(self):
        return self.__tag


    def get_content(self):
        return self.__content


    def get_physical_description(self):
        return self.__physical_description


    def set_tag(self, value):
        self.__tag = value


    def set_content(self, value):
        self.__content = value


    def set_physical_description(self, value):
        self.__physical_description = value


    def del_tag(self):
        del self.__tag


    def del_content(self):
        del self.__content


    def del_physical_description(self):
        del self.__physical_description


    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__tag = relevant_lines[0].tag
        starting_level = gedcom_lines[0].level
        index = 0
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_PHYSICAL_DESCRIPTION:
                self.__tag = line.tag
                self.__physical_description = line.value
                if len(relevant_lines) > index+1 and relevant_lines[index+1].level == starting_level + 1:
                    for line in relevant_lines[index+1:]:
                        if line.tag == gedcom.tags.GEDCOM_TAG_CONTINUED:
                            self.__physical_description = self.__physical_description + '\n' + line.value
                            index += 1
                        elif line.tag == gedcom.tags.GEDCOM_TAG_CONCATENATION:
                            self.__physical_description = self.__physical_description + line.value
                            index += 1
                        else:
                            break
                parsed_lines = super().parse_gedcom(relevant_lines[index+1:])
                index += parsed_lines
            elif line.tag in (gedcom.tags.INDIVIDUAL_ATTRIBUTE_STRUCTURE_TAGS):
                self.__tag = line.tag
                self.__content = line.value
                parsed_lines = super().parse_gedcom(relevant_lines[1:])
                index += parsed_lines
            else:
                return
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s" % (level, self.__tag)
        if self.__content:
            gedcom_repr = "%s %s" % (gedcom_repr, self.__content)
        if self.__physical_description:
            gedcom_repr = gedcom.gedcom_file.split_text_for_gedcom(self.__physical_description, gedcom.tags.GEDCOM_TAG_PHYSICAL_DESCRIPTION, level, gedcom.tags.MAX_TEXT_LENGTH) 
        if super().get_gedcom_repr(level + 1):
            gedcom_repr = "%s\n%s" % (gedcom_repr, super().get_gedcom_repr(level + 1))
        return gedcom_repr
    tag = property(get_tag, set_tag, del_tag, "tag's docstring")
    content = property(get_content, set_content, del_content, "content's docstring")
    physical_description = property(get_physical_description, set_physical_description, del_physical_description, "physical_description's docstring")

class IndividualEventStructure(IndividualEventDetail):
    def __init__(self):
        self.__tag = ""
        self.__birth_christening_yes = ""
        self.__birth_christening_family_reference = ""
        self.__death_yes = ""
        self.__adopting_family_reference = ""
        self.__adopting_parent = ""
        super().__init__()

    def get_tag(self):
        return self.__tag


    def get_birth_christening_yes(self):
        return self.__birth_christening_yes


    def get_birth_christening_family_reference(self):
        return self.__birth_christening_family_reference


    def get_death_yes(self):
        return self.__death_yes


    def get_adopting_family_reference(self):
        return self.__adopting_family_reference


    def get_adopting_parent(self):
        return self.__adopting_parent


    def set_tag(self, value):
        self.__tag = value


    def set_birth_christening_yes(self, value):
        self.__birth_christening_yes = value


    def set_birth_christening_family_reference(self, value):
        self.__birth_christening_family_reference = value


    def set_death_yes(self, value):
        self.__death_yes = value


    def set_adopting_family_reference(self, value):
        self.__adopting_family_reference = value


    def set_adopting_parent(self, value):
        self.__adopting_parent = value


    def del_tag(self):
        del self.__tag


    def del_birth_christening_yes(self):
        del self.__birth_christening_yes


    def del_birth_christening_family_reference(self):
        del self.__birth_christening_family_reference


    def del_death_yes(self):
        del self.__death_yes


    def del_adopting_family_reference(self):
        del self.__adopting_family_reference


    def del_adopting_parent(self):
        del self.__adopting_parent


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
                    if len(relevant_lines) >= index+2 and relevant_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_FAMILY_CHILD:
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
                    if len(relevant_lines) >= index+2 and relevant_lines[index+1].tag == gedcom.tags.GEDCOM_TAG_FAMILY_CHILD:
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
    tag = property(get_tag, set_tag, del_tag, "tag's docstring")
    birth_christening_yes = property(get_birth_christening_yes, set_birth_christening_yes, del_birth_christening_yes, "birth_christening_yes's docstring")
    birth_christening_family_reference = property(get_birth_christening_family_reference, set_birth_christening_family_reference, del_birth_christening_family_reference, "birth_christening_family_reference's docstring")
    death_yes = property(get_death_yes, set_death_yes, del_death_yes, "death_yes's docstring")
    adopting_family_reference = property(get_adopting_family_reference, set_adopting_family_reference, del_adopting_family_reference, "adopting_family_reference's docstring")
    adopting_parent = property(get_adopting_parent, set_adopting_parent, del_adopting_parent, "adopting_parent's docstring")

class MultimediaLink(Record):
    def __init__(self):
        self.__reference = ""
        self.__multimedia_file = ""
        self.__multimedia_format = ""
        self.__multimedia_type = ""
        self.__multimedia_title = ""
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_multimedia_file(self):
        return self.__multimedia_file


    def get_multimedia_format(self):
        return self.__multimedia_format


    def get_multimedia_type(self):
        return self.__multimedia_type


    def get_multimedia_title(self):
        return self.__multimedia_title


    def set_reference(self, value):
        self.__reference = value


    def set_multimedia_file(self, value):
        self.__multimedia_file = value


    def set_multimedia_format(self, value):
        self.__multimedia_format = value


    def set_multimedia_type(self, value):
        self.__multimedia_type = value


    def set_multimedia_title(self, value):
        self.__multimedia_title = value


    def del_reference(self):
        del self.__reference


    def del_multimedia_file(self):
        del self.__multimedia_file


    def del_multimedia_format(self):
        del self.__multimedia_format


    def del_multimedia_type(self):
        del self.__multimedia_type


    def del_multimedia_title(self):
        del self.__multimedia_title


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
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    multimedia_file = property(get_multimedia_file, set_multimedia_file, del_multimedia_file, "multimedia_file's docstring")
    multimedia_format = property(get_multimedia_format, set_multimedia_format, del_multimedia_format, "multimedia_format's docstring")
    multimedia_type = property(get_multimedia_type, set_multimedia_type, del_multimedia_type, "multimedia_type's docstring")
    multimedia_title = property(get_multimedia_title, set_multimedia_title, del_multimedia_title, "multimedia_title's docstring")

class NoteStructure(Record):
    def __init__(self):
        self.__reference = ""
        self.__text = ""
        super().__init__()

    def get_reference(self):
        return self.__reference


    def get_text(self):
        return self.__text


    def set_reference(self, value):
        self.__reference = value


    def set_text(self, value):
        self.__text = value


    def del_reference(self):
        del self.__reference


    def del_text(self):
        del self.__text


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
            return gedcom.gedcom_file.split_text_for_gedcom(self.__text, gedcom.tags.GEDCOM_TAG_NOTE, level, gedcom.tags.MAX_TEXT_LENGTH)
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    text = property(get_text, set_text, del_text, "text's docstring")

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

    def get_name(self):
        return self.__name


    def get_name_type(self):
        return self.__name_type


    def get_variation(self):
        return self.__variation


    def get_name_piece_prefix(self):
        return self.__name_piece_prefix


    def get_name_piece_given(self):
        return self.__name_piece_given


    def get_name_piece_nick(self):
        return self.__name_piece_nick


    def get_name_piece_surname_prefix(self):
        return self.__name_piece_surname_prefix


    def get_name_piece_surname(self):
        return self.__name_piece_surname


    def get_name_piece_suffix(self):
        return self.__name_piece_suffix


    def get_notes(self):
        return self.__notes


    def get_sources(self):
        return self.__sources


    def get_phonetic_variations(self):
        return self.__phonetic_variations


    def get_romanized_variations(self):
        return self.__romanized_variations


    def set_name(self, value):
        self.__name = value


    def set_name_type(self, value):
        self.__name_type = value


    def set_variation(self, value):
        self.__variation = value


    def set_name_piece_prefix(self, value):
        self.__name_piece_prefix = value


    def set_name_piece_given(self, value):
        self.__name_piece_given = value


    def set_name_piece_nick(self, value):
        self.__name_piece_nick = value


    def set_name_piece_surname_prefix(self, value):
        self.__name_piece_surname_prefix = value


    def set_name_piece_surname(self, value):
        self.__name_piece_surname = value


    def set_name_piece_suffix(self, value):
        self.__name_piece_suffix = value


    def set_notes(self, value):
        self.__notes = value


    def set_sources(self, value):
        self.__sources = value


    def set_phonetic_variations(self, value):
        self.__phonetic_variations = value


    def set_romanized_variations(self, value):
        self.__romanized_variations = value


    def del_name(self):
        del self.__name


    def del_name_type(self):
        del self.__name_type


    def del_variation(self):
        del self.__variation


    def del_name_piece_prefix(self):
        del self.__name_piece_prefix


    def del_name_piece_given(self):
        del self.__name_piece_given


    def del_name_piece_nick(self):
        del self.__name_piece_nick


    def del_name_piece_surname_prefix(self):
        del self.__name_piece_surname_prefix


    def del_name_piece_surname(self):
        del self.__name_piece_surname


    def del_name_piece_suffix(self):
        del self.__name_piece_suffix


    def del_notes(self):
        del self.__notes


    def del_sources(self):
        del self.__sources


    def del_phonetic_variations(self):
        del self.__phonetic_variations


    def del_romanized_variations(self):
        del self.__romanized_variations

    
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
    name = property(get_name, set_name, del_name, "name's docstring")
    name_type = property(get_name_type, set_name_type, del_name_type, "name_type's docstring")
    variation = property(get_variation, set_variation, del_variation, "variation's docstring")
    name_piece_prefix = property(get_name_piece_prefix, set_name_piece_prefix, del_name_piece_prefix, "name_piece_prefix's docstring")
    name_piece_given = property(get_name_piece_given, set_name_piece_given, del_name_piece_given, "name_piece_given's docstring")
    name_piece_nick = property(get_name_piece_nick, set_name_piece_nick, del_name_piece_nick, "name_piece_nick's docstring")
    name_piece_surname_prefix = property(get_name_piece_surname_prefix, set_name_piece_surname_prefix, del_name_piece_surname_prefix, "name_piece_surname_prefix's docstring")
    name_piece_surname = property(get_name_piece_surname, set_name_piece_surname, del_name_piece_surname, "name_piece_surname's docstring")
    name_piece_suffix = property(get_name_piece_suffix, set_name_piece_suffix, del_name_piece_suffix, "name_piece_suffix's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    sources = property(get_sources, set_sources, del_sources, "sources's docstring")
    phonetic_variations = property(get_phonetic_variations, set_phonetic_variations, del_phonetic_variations, "phonetic_variations's docstring")
    romanized_variations = property(get_romanized_variations, set_romanized_variations, del_romanized_variations, "romanized_variations's docstring")

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

    def get_pointer_source_record(self):
        return self.__pointer_source_record


    def get_reference(self):
        return self.__reference


    def get_page(self):
        return self.__page


    def get_event(self):
        return self.__event


    def get_event_role(self):
        return self.__event_role


    def get_data(self):
        return self.__data


    def get_data_date(self):
        return self.__data_date


    def get_data_text(self):
        return self.__data_text


    def get_description(self):
        return self.__description


    def get_text(self):
        return self.__text


    def get_multimedia_link(self):
        return self.__multimedia_link


    def get_notes(self):
        return self.__notes


    def get_certainty_assessment(self):
        return self.__certainty_assessment


    def set_pointer_source_record(self, value):
        self.__pointer_source_record = value


    def set_reference(self, value):
        self.__reference = value


    def set_page(self, value):
        self.__page = value


    def set_event(self, value):
        self.__event = value


    def set_event_role(self, value):
        self.__event_role = value


    def set_data(self, value):
        self.__data = value


    def set_data_date(self, value):
        self.__data_date = value


    def set_data_text(self, value):
        self.__data_text = value


    def set_description(self, value):
        self.__description = value


    def set_text(self, value):
        self.__text = value


    def set_multimedia_link(self, value):
        self.__multimedia_link = value


    def set_notes(self, value):
        self.__notes = value


    def set_certainty_assessment(self, value):
        self.__certainty_assessment = value


    def del_pointer_source_record(self):
        del self.__pointer_source_record


    def del_reference(self):
        del self.__reference


    def del_page(self):
        del self.__page


    def del_event(self):
        del self.__event


    def del_event_role(self):
        del self.__event_role


    def del_data(self):
        del self.__data


    def del_data_date(self):
        del self.__data_date


    def del_data_text(self):
        del self.__data_text


    def del_description(self):
        del self.__description


    def del_text(self):
        del self.__text


    def del_multimedia_link(self):
        del self.__multimedia_link


    def del_notes(self):
        del self.__notes


    def del_certainty_assessment(self):
        del self.__certainty_assessment

    
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
                gedcom_repr = "%s\n%s" % (gedcom_repr, gedcom.gedcom_file.split_text_for_gedcom(self.__text, gedcom.tags.GEDCOM_TAG_TEXT, level+2, gedcom.tags.MAX_TEXT_LENGTH))
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
    pointer_source_record = property(get_pointer_source_record, set_pointer_source_record, del_pointer_source_record, "pointer_source_record's docstring")
    reference = property(get_reference, set_reference, del_reference, "reference's docstring")
    page = property(get_page, set_page, del_page, "page's docstring")
    event = property(get_event, set_event, del_event, "event's docstring")
    event_role = property(get_event_role, set_event_role, del_event_role, "event_role's docstring")
    data = property(get_data, set_data, del_data, "data's docstring")
    data_date = property(get_data_date, set_data_date, del_data_date, "data_date's docstring")
    data_text = property(get_data_text, set_data_text, del_data_text, "data_text's docstring")
    description = property(get_description, set_description, del_description, "description's docstring")
    text = property(get_text, set_text, del_text, "text's docstring")
    multimedia_link = property(get_multimedia_link, set_multimedia_link, del_multimedia_link, "multimedia_link's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
    certainty_assessment = property(get_certainty_assessment, set_certainty_assessment, del_certainty_assessment, "certainty_assessment's docstring")

class SpouseToFamilyLink(Record):
    def __init__(self):
        self.__family_reference = ""
        self.__notes = []
        super().__init__()

    def get_family_reference(self):
        return self.__family_reference


    def get_notes(self):
        return self.__notes


    def set_family_reference(self, value):
        self.__family_reference = value


    def set_notes(self, value):
        self.__notes = value


    def del_family_reference(self):
        del self.__family_reference


    def del_notes(self):
        del self.__notes


    def parse_gedcom(self, gedcom_lines):
        relevant_lines = super().get_relevant_lines(gedcom_lines)
        self.__family_reference = relevant_lines[0].value
        index = 0
        starting_level = relevant_lines[0].level
        while index < len(relevant_lines):
            line = relevant_lines[index]
            if line.tag == gedcom.tags.GEDCOM_TAG_NOTE and line.level == starting_level+1:
                note = NoteStructure()
                parsed_lines = note.parse_gedcom(relevant_lines[index:])
                if parsed_lines:
                    self.__notes.append(note)
                    index += parsed_lines
                    continue
            index += 1
        return len(relevant_lines)

    def get_gedcom_repr(self, level):
        gedcom_repr = "%s %s %s" % (level, gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE, self.__family_reference)
        for note in self.__notes:
            gedcom_repr = "%s\n%s" % (gedcom_repr, note.get_gedcom_repr(level+1))
        return gedcom_repr
    family_reference = property(get_family_reference, set_family_reference, del_family_reference, "family_reference's docstring")
    notes = property(get_notes, set_notes, del_notes, "notes's docstring")
