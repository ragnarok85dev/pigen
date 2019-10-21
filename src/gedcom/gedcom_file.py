import gedcom

def split_text_for_gedcom(full_text, initial_tag, level, max_length):
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

class GedcomFile(object):
    def __init__(self, params):
        '''
        Constructor
        '''
        