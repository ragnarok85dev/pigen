import gedcom.structures as gd
import re
from builtins import staticmethod
import gedcom

class GedcomFormatViolationError(Exception):
    pass

class GedcomLine(object):
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

    gedcom_line_format = re.compile("^(?P<level>[0-9]+) ((?P<id>@[-a-zA-Z0-9_]+@) )?(?P<tag>[_A-Z0-9]+)( (?P<value>.*))?$")

    def __init__(self, line_content, index=0):
        self.__content = line_content
        self.__gedcom_index = index
        self.__level = None
        self.__pointer = ""
        self.__value = ""
        match = re.match(GedcomLine.gedcom_line_format, line_content)
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

class GedcomFile(object):
    '''
    GedcomFile class is the basic class to parse and output GEDCOM files 
    '''
    def __init__(self, filepath=None):
        self.__header = None
        self.__submission_record = None
        self.__records = {}
        if filepath:
            self.parse_gedcom(filepath)

    def get_header(self):
        return self.__header


    def get_submission_record(self):
        return self.__submission_record


    def get_records(self):
        return self.__records


    def set_header(self, value):
        self.__header = value


    def set_submission_record(self, value):
        self.__submission_record = value


    def set_records(self, value):
        self.__records = value


    def del_header(self):
        del self.__header


    def del_submission_record(self):
        del self.__submission_record


    def del_records(self):
        del self.__records

    
    def parse_gedcom(self, file_path: str) -> int:
        '''
        It parses a GEDCOM file in file_path and populate GedcomFile header, records and submission record 
        GEDCOM version accepted is 5.5
        :param file_path: input file path of GEDCOM file (e.g. "C:\\users\\public\\mytree.ged")
        '''
        gedcom_lines_list = []
        with open(file_path, mode='r', encoding='utf-8-sig') as content_file:
            content = content_file.readlines()
        for index, line in enumerate(content):
            if GedcomFile.is_valid_gedcom_line(line):
                gedcom_lines_list.append(GedcomLine(line, index))
            else:
                error_message = "Invalid GEDCOM line: " + line
                raise GedcomFormatViolationError(error_message)
        # HEADER record is mandatory and must be the first one
        self.__header = gd.Header()
        parsed_lines = self.__header.parse_gedcom(gedcom_lines_list)
        for line_zero_index in [line for line in gedcom_lines_list[parsed_lines:] if line.level==0]:
            # Submission record is optional
            if line_zero_index.tag == gedcom.tags.GEDCOM_TAG_SUBMISSION:
                record = gd.Submission()
                record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
                self.__submission_record = record
                continue
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_INDIVIDUAL:
                record = gd.Individual()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_FAMILY:
                record = gd.Family()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_OBJECT:
                record = gd.Multimedia()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_NOTE:
                record = gd.Note()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_REPOSITORY:
                record = gd.Repository()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_SOURCE:
                record = gd.Source()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_SUBMITTER:
                record = gd.Submitter()
            elif line_zero_index.is_user_defined_tag():
                continue
            elif line_zero_index.is_last_gedcom_line():
                return
            else:
                return
            record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
            self.__records[record.reference] = record

    def get_gedcom_repr(self) -> str:
        '''
        It returns a GEDCOM representation of the GedcomFile class
        '''
        gedcom_repr = ""
        if self.__header:
            gedcom_repr = self.__header.get_gedcom_repr(0)
        if self.__submission_record:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__submission_record.get_gedcom_repr(0))
        for key, record in self.__records.items():
            gedcom_repr = "%s\n%s" % (gedcom_repr, record.get_gedcom_repr(0))
        gedcom_repr = "%s\n0 %s" % (gedcom_repr, gedcom.tags.GEDCOM_TAG_TRAILER)
        return gedcom_repr
    
    @staticmethod
    def get_gedcom_relevant_lines(gedcom_lines, valid_top_level_tags = None):
        '''
        Return a subset of GEDCOM lines belonging to the structure starting in gedcom_lines[0]
        :param gedcom_lines: list of GEDCOM lines containing the record
        :param valid_top_level_tags: if the GEDCOM structure does not have a hierarchical structure of levels (e.g. ADDRESS_STRUCTURE)
                                     then this is a list of valid top level tags (e.g.['ADDR', 'PHON', 'EMAIL', 'FAX', 'WWW'] ) 
        '''
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

    @staticmethod
    def is_valid_gedcom_line(line):
        '''
        Each line should have the following (bracketed items optional):
        level + ' ' + [pointer + ' ' +] tag + [' ' + line_value]
        '''
        # Level must start with non-negative int, no leading zeros.
        level_regex = '^(0|[1-9]+[0-9]*) '
        # Pointer optional, if it exists it must be flanked by `@`
        pointer_regex = '(@[^@]+@ |)'
        # Tag must be an alphanumeric string
        tag_regex = '([A-Za-z0-9_]+)'
        # Value optional, consists of anything after a space to end of line
        value_regex = '( [^\n\r]*|)'
        # End of line defined by `\n` or `\r`
        end_of_line_regex = '([\r\n]{1,2})'
        # Complete regex
        gedcom_line_regex = level_regex + pointer_regex + tag_regex + value_regex + end_of_line_regex
        return (re.match(gedcom_line_regex, line) is not None) or (line == '0 '+ gedcom.tags.GEDCOM_TAG_TRAILER) and (len(line) <=255)
    
    @staticmethod
    def split_text_for_gedcom(full_text, initial_tag, level, max_length):
        '''
        Splits long text in GEDCOM format using CONC and CONT tags
        :param full_text: variable containing the full text to be split
        :param initial_tag: tag identifying the text
        :param level: initial GEDCOM level associated to initial_tag 
        :param max_length: maximum length of the text chunks
        '''
        gedcom_repr = "%s %s " % (level, initial_tag)
        split_text = list(full_text[0+i:max_length+i] for i in range(0, len(full_text), max_length))
        if len(split_text) == 0:
            return gedcom_repr.strip()
        split_notes = [note.replace("\n", "\n" + str(level+1) +  " " + gedcom.tags.GEDCOM_TAG_CONTINUED + " ") for note in split_text]
        for i, note_list in enumerate(split_notes):
            if i > 0 and not (gedcom.tags.GEDCOM_TAG_CONTINUED in note_list):
                gedcom_repr = gedcom_repr + "\n" + str(level+1) + " "  + gedcom.tags.GEDCOM_TAG_CONCATENATION + " " + "".join(note_list)
            else:
                gedcom_repr += "".join(note_list)
        return gedcom_repr 
    
    def __str__(self):
        return self.get_gedcom_repr()
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__str__() == other.__str__()
        else:
            return False
    
    @property
    def individuals(self):
        return {k:v for k,v in self.__records.items() if isinstance(v, gd.Individual)}

    @property
    def families(self):
        return {k:v for k,v in self.__records.items() if isinstance(v, gd.Family)}

    @property
    def notes(self):
        return {k:v for k,v in self.__records.items() if isinstance(v, gd.Note)}

    @property
    def sources(self):
        return {k:v for k,v in self.__records.items() if isinstance(v, gd.Source)}

    @property
    def objects(self):
        return {k:v for k,v in self.__records.items() if isinstance(v, gd.Multimedia)}

    @property
    def repositories(self):
        return {k:v for k,v in self.__records.items() if isinstance(v, gd.Repository)}
    
    header = property(get_header, set_header, del_header, "header's docstring")
    submission_record = property(get_submission_record, set_submission_record, del_submission_record, "submission_record's docstring")
    records = property(get_records, set_records, del_records, "records's docstring")
