import re
import gedcom


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
