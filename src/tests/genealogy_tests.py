import unittest
import genealogy
from gedcom.structures import Individual, Family, Note, NoteStructure, Source,\
    SourceCitation, Multimedia, MultimediaLink
from genealogy import Genealogy
import os.path
from tests.gedcom_tests import file_to_string


class GenealogyTests(unittest.TestCase):
    empty_gen_gedcom = ("0 HEAD\n"
                            "2 VERS 0.0.1\n"
                            "2 NAME pigen\n"
                            "1 GEDC\n"
                            "2 VERS 5.5\n"
                            "0 TRLR")

    def load_sample_family(self):
        input_path = os.path.join(os.path.abspath(__file__), "../gedcom_files/sample_family.ged")  
        return Genealogy(input_path)


    def test_empty(self):
        g = genealogy.Genealogy()
        gedcom_f = g.get_gedcom()
        self.assertEqual(len(g.get_individuals_list()), 0)
        self.assertEqual(len(g.get_families_list()), 0)
        self.assertEqual(self.empty_gen_gedcom, gedcom_f)


    def test_one_individual(self):
        g = genealogy.Genealogy()
        # testing adding a new individual
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        indi_ref = g.add_new_individual(pinco_pallino)
        indi_gedcom = "0 %s INDI\n" % (indi_ref)
        indi_gedcom = indi_gedcom + ("1 NAME Pinco /Pallino/\n"
                                    "2 GIVN Pinco\n"
                                    "2 SURN Pallino\n"
                                    "1 SEX M\n"
                                    "1 BIRT\n"
                                    "2 DATE 15-feb-1900\n"
                                    "1 DEAT Y\n"
                                    "2 DATE 16-mar-1950\n")
        gedcom = self.empty_gen_gedcom.replace("0 TRLR", indi_gedcom) + "0 TRLR"
        self.assertEqual(len(g.get_individuals_list()), 1)
        self.assertEqual(pinco_pallino, g.get_individual_by_ref(indi_ref))
        self.assertEqual(gedcom, g.get_gedcom())
        # testing removing the individual
        g.remove_individual(pinco_pallino)
        self.assertEqual(len(g.get_individuals_list()), 0)
        self.assertEqual(self.empty_gen_gedcom, g.get_gedcom())


    def test_add_individual(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        pp_ref = g.add_new_individual(pinco_pallino)
        pp_retrieved = g.get_individual_by_ref(pp_ref)
        self.assertEqual(pinco_pallino, pp_retrieved)
        self.assertEqual(len(g.get_individuals_list()), 1)


    def test_remove_individual(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        g.add_new_individual(pinco_pallino)
        g.remove_individual(pinco_pallino)
        self.assertEqual(len(g.get_individuals_list()), 0)


    def test_add_family(self):
        g = genealogy.Genealogy()
        new_family = Family()
        new_family_ref = g.add_new_family(new_family)
        ff_retrieved = g.get_family_by_ref(new_family_ref)
        self.assertEqual(new_family, ff_retrieved)
        self.assertEqual(len(g.get_families_list()), 1)    


    def test_remove_family(self):
        g = genealogy.Genealogy()
        new_family = Family()
        g.add_new_family(new_family)
        g.remove_family(new_family)
        self.assertEqual(len(g.get_families_list()), 0)   


    def test_create_new_family_with_partners(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        pinca_caia = Individual("Pinca", "Caia", "F", "11-mar-1901", "26-nov-1960")
        husb_ref = g.add_new_individual(pinco_pallino)
        wife_ref = g.add_new_individual(pinca_caia)
        fam_ref = g.create_new_family_with_partners(pinco_pallino, pinca_caia)
        fam = g.get_family_by_ref(fam_ref)
        self.assertEqual(fam.husband_reference, husb_ref)
        self.assertEqual(fam.wife_reference, wife_ref)
        self.assertEqual(len(fam.get_children_references()), 0)


    def test_create_new_family_with_parent_child(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        tizio_pallino = Individual("Tizio", "Pallino", "M", "11-mar-1920", "26-nov-1970")
        father_ref = g.add_new_individual(pinco_pallino)
        son_ref = g.add_new_individual(tizio_pallino)
        fam_ref = g.create_new_family_with_parent_child(pinco_pallino, tizio_pallino)
        fam = g.get_family_by_ref(fam_ref)
        self.assertEqual(fam.husband_reference, father_ref)
        self.assertEqual(fam.wife_reference, "")
        self.assertEqual(len(fam.get_children_references()), 1)
        self.assertEqual(fam.get_children_references()[0], son_ref)


    def test_father_son(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        tizio_pallino = Individual("Tizio", "Pallino", "M", "11-mar-1920", "26-nov-1970")
        father_ref = g.add_new_individual(pinco_pallino)
        son_ref = g.add_new_individual(tizio_pallino)
        g.link_individual(pinco_pallino, tizio_pallino, genealogy.Relationship.PARENT)
        family_ref = pinco_pallino.spouse_to_family_links[0].family_reference
        family = g.get_family_by_ref(family_ref)
        self.assertEqual(len(g.get_individuals_list()), 2)
        self.assertEqual(len(g.get_families_list()), 1)
        self.assertEqual(g.get_father_of(tizio_pallino), pinco_pallino)
        self.assertEqual(list(g.get_children_of(pinco_pallino))[0], tizio_pallino)
        self.assertEqual(family.husband_reference, father_ref)
        self.assertEqual(family.children_references[0], son_ref)
        g.remove_individual(pinco_pallino)
        g.remove_individual(tizio_pallino)
        self.assertEqual(len(g.get_individuals_list()), 0)
        self.assertEqual(len(g.get_families_list()), 0)

 
    def test_mother_son(self):
        g = genealogy.Genealogy()
        pinca_caia = Individual("Pinca", "Caia", "F", "11-mar-1901", "26-nov-1960")
        tizio_pallino = Individual("Tizio", "Pallino", "M", "11-mar-1920", "26-nov-1970")
        mother_ref = g.add_new_individual(pinca_caia)
        son_ref = g.add_new_individual(tizio_pallino)
        g.link_individual(pinca_caia, tizio_pallino, genealogy.Relationship.PARENT)
        family_ref = pinca_caia.spouse_to_family_links[0].family_reference
        family = g.get_family_by_ref(family_ref)
        self.assertEqual(g.get_mother_of(tizio_pallino), pinca_caia)
        self.assertEqual(list(g.get_children_of(pinca_caia))[0], tizio_pallino)
        self.assertEqual(family.wife_reference, mother_ref)
        self.assertEqual(family.children_references[0], son_ref)
 
 
    def test_get_partner_of(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        pinca_caia = Individual("Pinca", "Caia", "F", "11-mar-1901", "26-nov-1960")
        husb_ref = g.add_new_individual(pinco_pallino)
        wife_ref = g.add_new_individual(pinca_caia)
        g.link_individual(pinco_pallino, pinca_caia, genealogy.Relationship.PARTNER)
        family_ref = pinco_pallino.spouse_to_family_links[0].family_reference
        family = g.get_family_by_ref(family_ref)
        self.assertEqual(len(g.get_individuals_list()), 2)
        self.assertEqual(len(g.get_families_list()), 1)
        self.assertEqual(g.get_partner_of(pinco_pallino), pinca_caia)
        self.assertEqual(g.get_partner_of(pinca_caia), pinco_pallino)
        self.assertEqual(family.husband_reference, husb_ref)
        self.assertEqual(family.wife_reference, wife_ref)


    def test_create_simple_family(self):
        '''
            pinco_pallino x pinca_caia
                          |
                    tizio_pallino
        '''
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        pinca_caia = Individual("Pinca", "Caia", "F", "11-mar-1901", "26-nov-1960")
        tizio_pallino = Individual("Tizio", "Pallino", "M", "11-mar-1920", "26-nov-1970")
        husb_ref = g.add_new_individual(pinco_pallino)
        wife_ref = g.add_new_individual(pinca_caia)
        son_ref = g.add_new_individual(tizio_pallino)
        g.link_individual(pinco_pallino, pinca_caia, genealogy.Relationship.PARTNER)
        g.link_individual(pinca_caia, tizio_pallino, genealogy.Relationship.PARENT)
        g.link_individual(pinco_pallino, tizio_pallino, genealogy.Relationship.PARENT)
        family_ref = pinco_pallino.spouse_to_family_links[0].family_reference
        family = g.get_family_by_ref(family_ref)
        self.assertEqual(len(g.get_individuals_list()), 3)
        self.assertEqual(len(g.get_families_list()), 1)
        self.assertEqual(g.get_partner_of(pinco_pallino), pinca_caia)
        self.assertEqual(family.husband_reference, husb_ref)
        self.assertEqual(family.wife_reference, wife_ref)
        self.assertEqual(family.children_references[0], son_ref)
        self.assertEqual((g.get_parents_of(tizio_pallino))[0], pinca_caia)
        self.assertEqual((g.get_parents_of(tizio_pallino))[1], pinco_pallino)
        return g
 
 
    def test_siblings(self):
        g = self.test_create_simple_family()
        tizio_pallino = g.get_individual_by_ref("@I3@")
        caia_pallino = Individual("Caia", "Pallino", "F", "11-mar-1921", "26-nov-1971")
        g.add_new_individual(caia_pallino)
        g.link_individual(caia_pallino, tizio_pallino, genealogy.Relationship.SIBLING)
        self.assertEqual(list(g.get_siblings_of(tizio_pallino))[0], caia_pallino)
        self.assertEqual(list(g.get_siblings_of(caia_pallino))[0], tizio_pallino)
        g.un_link_individual(tizio_pallino, caia_pallino, genealogy.Relationship.SIBLING)
        self.assertEqual(len(g.get_siblings_of(tizio_pallino)), 0)
        self.assertEqual(len(g.get_siblings_of(caia_pallino)), 0)
         
   
    def test_unlink_father(self):
        g = self.test_create_simple_family()
        father = g.get_individual_by_ref("@I1@")
        son = g.get_individual_by_ref("@I3@")
        g.un_link_individual(father, son, genealogy.Relationship.PARENT)
        self.assertNotIn(son, list(g.get_children_of(father)))
        self.assertIsNone(g.get_father_of(son))
 
 
    def test_unlink_child(self):
        g = self.load_sample_family()
        mother = g.get_individual_by_ref("@I2@")
        son = g.get_individual_by_ref("@I3@")
        g.un_link_individual(son, mother, genealogy.Relationship.CHILD)
        self.assertNotIn(son, list(g.get_children_of(mother)))
        self.assertIsNone(g.get_mother_of(son))
 
 
    def test_unlink_partner(self):
        g = self.load_sample_family()
        father = g.get_individual_by_ref("@I1@")
        mother = g.get_individual_by_ref("@I2@")
        g.un_link_individual(father, mother, genealogy.Relationship.PARTNER)
        self.assertIsNone(g.get_partner_of(father))
        self.assertIsNone(g.get_partner_of(mother))
     
         
    def test_get_ancestors(self):
        g = self.load_sample_family()
        leaf = g.get_individual_by_ref("@I3@")
        ancestors = [g.get_individual_by_ref("@I1@"), g.get_individual_by_ref("@I2@"), g.get_individual_by_ref("@I5@"), g.get_individual_by_ref("@I6@")]
        self.assertEqual(len(g.get_ancestors_of(leaf)), 4)
        for ancestor in ancestors:
            self.assertIn(ancestor, g.get_ancestors_of(leaf))
     
         
    def test_get_descendants(self):
        g = self.load_sample_family()
        root = g.get_individual_by_ref("@I6@")
        descendants = [g.get_individual_by_ref("@I1@"), g.get_individual_by_ref("@I5@"), g.get_individual_by_ref("@I3@"), g.get_individual_by_ref("@I4@")]
        self.assertEqual(len(g.get_descendants_of(root)), 4)
        for descendant in descendants:
            self.assertIn(descendant, g.get_descendants_of(root))


    def test_rename_individual(self):
        g = self.load_sample_family()
        indi = g.get_individual_by_ref("@I1@")
        indi_wife = g.get_individual_by_ref("@I2@")
        new_ref = "@I999@"
        g.rename_individual_reference(indi.reference, new_ref)
        indi_2 = g.get_individual_by_ref(new_ref)
        self.assertEqual(indi, indi_2)
        self.assertEqual(g.get_partner_of(indi_wife).reference, new_ref)
        self.assertEqual(g.get_partner_of(indi_2), indi_wife)


    def test_rename_family(self):
        g = self.load_sample_family()
        fam = g.get_family_by_ref("@F3@")
        wife = g.get_individual_by_ref("@I2@")
        husb = g.get_individual_by_ref("@I1@")
        new_ref = "@F999@"
        g.rename_family_reference(fam.reference, new_ref)
        fam_new = g.get_family_by_ref(new_ref)
        self.assertEqual(fam, fam_new)
        self.assertEqual(fam_new.husband_reference, husb.reference)
        self.assertEqual(fam_new.wife_reference, wife.reference)
        self.assertEqual(husb.spouse_to_family_links[0].family_reference, new_ref)
        self.assertEqual(wife.spouse_to_family_links[0].family_reference, new_ref)
        for child in [g.get_individual_by_ref("@I3@"), g.get_individual_by_ref("@I4@")]:
            self.assertEqual(child.child_to_family_links[0].family_reference, new_ref)


    def test_gedcom_import_export(self):
        input_filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/allged.ged")
        compare_filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/allged_compare.ged")
        g = Genealogy(input_filepath)
        compare_file = file_to_string(compare_filepath)
        self.assertEqual(compare_file, g.get_gedcom())


    def test_add_disconnected_genealogy(self):
        # 1. load sample family GEDCOM file as a Genealogy named sample_genealogy
        # 2. load again sample family GEDCOM file as another Genealogy named sample_genealogy_2
        # 3. add sample_genealogy_2 to sample_genealogy
        # 4. check GEDCOM representation of sample_genealogy is the same of pre-defined double_sample_family.ged GEDCOM file
        sample_genealogy = self.load_sample_family()
        sample_genealogy_2 = self.load_sample_family()
        sample_genealogy.add_disconnected_genealogy(sample_genealogy_2)
        compare_genealogy_file = file_to_string(os.path.join(os.path.abspath(__file__), "../gedcom_files/sample_family_doubled.ged"))
        self.assertEqual(compare_genealogy_file, sample_genealogy.get_gedcom())

    
    def test_create_and_delete_note(self):
        sample_genealogy = self.load_sample_family()
        sample_genealogy_gedcom = sample_genealogy.get_gedcom()
        new_note = Note()
        new_note.text = "Pigen Test Note"
        new_note_ref = sample_genealogy.add_new_note(new_note)
        new_note_structure = NoteStructure()
        new_note_structure.reference = new_note_ref
        indi = sample_genealogy.get_individual_by_ref("@I1@")
        indi.notes.append(new_note_structure)
        sample_genealogy.remove_note(new_note)
        self.assertEqual(sample_genealogy_gedcom, sample_genealogy.get_gedcom())
        

    def test_create_and_delete_source(self):
        sample_genealogy = self.load_sample_family()
        sample_genealogy_gedcom = sample_genealogy.get_gedcom()
        new_source = Source()
        new_source.source_title = "Pigen Test Source"
        new_source_ref = sample_genealogy.add_new_source(new_source)
        new_source_citation = SourceCitation()
        new_source_citation.reference = new_source_ref
        indi = sample_genealogy.get_individual_by_ref("@I1@")
        indi.sources.append(new_source_citation)
        sample_genealogy.remove_source(new_source)      
        self.assertEqual(sample_genealogy_gedcom, sample_genealogy.get_gedcom())
        

    def test_create_and_delete_multimedia(self):
        sample_genealogy = self.load_sample_family()
        sample_genealogy_gedcom = sample_genealogy.get_gedcom()
        new_multimedia = Multimedia()
        new_multimedia.file_title = "Pigen Test Multimedia"
        new_mult_ref = sample_genealogy.add_new_multimedia(new_multimedia)
        new_multimedia_link = MultimediaLink()
        new_multimedia_link.reference = new_mult_ref
        indi = sample_genealogy.get_individual_by_ref("@I1@")
        indi.multimedia_links.append(new_multimedia_link)
        sample_genealogy.remove_multimedia(new_multimedia)      
        self.assertEqual(sample_genealogy_gedcom, sample_genealogy.get_gedcom())


if __name__ == "__main__":
    unittest.main()