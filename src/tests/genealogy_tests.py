import unittest
import genealogy
from gedcom.structures import Individual, Family

class GenealogyTests(unittest.TestCase):
    empty_gen_gedcom = ("0 HEAD\n"
                            "2 VERS 0.0.1\n"
                            "2 NAME pigen\n"
                            "1 GEDC\n"
                            "2 VERS 5.5\n"
                            "0 TRLR")

    def test_empty(self):
        g = genealogy.Genealogy()
        gedcom_f = g.export_gedcom_file()
        self.assertEqual(len(g.get_individuals()), 0)
        self.assertEqual(len(g.get_families()), 0)
        self.assertEqual(self.empty_gen_gedcom, gedcom_f.get_gedcom_repr())


    def test_one_individual(self):
        g = genealogy.Genealogy()
        # testing adding a new individual
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        indi_ref = g.add_individual(pinco_pallino)
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
        self.assertEqual(len(g.get_individuals()), 1)
        self.assertEqual(pinco_pallino, g.get_individual_by_ref(indi_ref))
        self.assertEqual(gedcom, g.export_gedcom_file().get_gedcom_repr())
        # testing removing the individual
        g.remove_individual(pinco_pallino)
        self.assertEqual(len(g.get_individuals()), 0)
        self.assertEqual(self.empty_gen_gedcom, g.export_gedcom_file().get_gedcom_repr())


    def test_add_individual(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        pp_ref = g.add_individual(pinco_pallino)
        pp_retrieved = g.get_individual_by_ref(pp_ref)
        self.assertEqual(pinco_pallino, pp_retrieved)
        self.assertEqual(len(g.get_individuals()), 1)


    def test_remove_individual(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        g.add_individual(pinco_pallino)
        g.remove_individual(pinco_pallino)
        self.assertEqual(len(g.get_individuals()), 0)


    def test_add_family(self):
        g = genealogy.Genealogy()
        new_family = Family()
        new_family_ref = g.add_family(new_family)
        ff_retrieved = g.get_family_by_ref(new_family_ref)
        self.assertEqual(new_family, ff_retrieved)
        self.assertEqual(len(g.get_families()), 1)    


    def test_remove_family(self):
        g = genealogy.Genealogy()
        new_family = Family()
        g.add_family(new_family)
        g.remove_family(new_family)
        self.assertEqual(len(g.get_families()), 0)   


    def test_create_new_family_with_partners(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        pinca_caia = Individual("Pinca", "Caia", "F", "11-mar-1901", "26-nov-1960")
        husb_ref = g.add_individual(pinco_pallino)
        wife_ref = g.add_individual(pinca_caia)
        fam_ref = g.create_new_family_with_partners(pinco_pallino, pinca_caia)
        fam = g.get_family_by_ref(fam_ref)
        self.assertEqual(fam.husband_reference, husb_ref)
        self.assertEqual(fam.wife_reference, wife_ref)
        self.assertEqual(len(fam.get_children_references()), 0)


    def test_create_new_family_with_parent_child(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        tizio_pallino = Individual("Tizio", "Pallino", "M", "11-mar-1920", "26-nov-1970")
        father_ref = g.add_individual(pinco_pallino)
        son_ref = g.add_individual(tizio_pallino)
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
        father_ref = g.add_individual(pinco_pallino)
        son_ref = g.add_individual(tizio_pallino)
        g.link_individual(pinco_pallino, tizio_pallino, genealogy.Genealogy.RELATIONSHIP_FATHER)
        family_ref = pinco_pallino.spouse_to_family_links[0].family_reference
        family = g.get_family_by_ref(family_ref)
        self.assertEqual(len(g.get_individuals()), 2)
        self.assertEqual(len(g.get_families()), 1)
        self.assertEqual(g.get_father_of(tizio_pallino), pinco_pallino)
        self.assertEqual(list(g.get_children_of(pinco_pallino))[0], tizio_pallino)
        self.assertEqual(family.husband_reference, father_ref)
        self.assertEqual(family.children_references[0], son_ref)
        g.remove_individual(pinco_pallino)
        g.remove_individual(tizio_pallino)
        self.assertEqual(len(g.get_individuals()), 0)
        self.assertEqual(len(g.get_families()), 0)


    def test_mother_son(self):
        g = genealogy.Genealogy()
        pinca_caia = Individual("Pinca", "Caia", "F", "11-mar-1901", "26-nov-1960")
        tizio_pallino = Individual("Tizio", "Pallino", "M", "11-mar-1920", "26-nov-1970")
        mother_ref = g.add_individual(pinca_caia)
        son_ref = g.add_individual(tizio_pallino)
        g.link_individual(pinca_caia, tizio_pallino, genealogy.Genealogy.RELATIONSHIP_MOTHER)
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
        husb_ref = g.add_individual(pinco_pallino)
        wife_ref = g.add_individual(pinca_caia)
        g.link_individual(pinco_pallino, pinca_caia, genealogy.Genealogy.RELATIONSHIP_PARTNER)
        family_ref = pinco_pallino.spouse_to_family_links[0].family_reference
        family = g.get_family_by_ref(family_ref)
        self.assertEqual(len(g.get_individuals()), 2)
        self.assertEqual(len(g.get_families()), 1)
        self.assertEqual(g.get_partner_of(pinco_pallino), pinca_caia)
        self.assertEqual(g.get_partner_of(pinca_caia), pinco_pallino)
        self.assertEqual(family.husband_reference, husb_ref)
        self.assertEqual(family.wife_reference, wife_ref)
    
    
    def test_create_simple_family(self):
        g = genealogy.Genealogy()
        pinco_pallino = Individual("Pinco", "Pallino", "M", "15-feb-1900", "16-mar-1950")
        pinca_caia = Individual("Pinca", "Caia", "F", "11-mar-1901", "26-nov-1960")
        tizio_pallino = Individual("Tizio", "Pallino", "M", "11-mar-1920", "26-nov-1970")
        husb_ref = g.add_individual(pinco_pallino)
        wife_ref = g.add_individual(pinca_caia)
        son_ref = g.add_individual(tizio_pallino)
        g.link_individual(pinco_pallino, pinca_caia, genealogy.Genealogy.RELATIONSHIP_PARTNER)
        g.link_individual(pinca_caia, tizio_pallino, genealogy.Genealogy.RELATIONSHIP_MOTHER)
        g.link_individual(pinco_pallino, tizio_pallino, genealogy.Genealogy.RELATIONSHIP_FATHER)
        family_ref = pinco_pallino.spouse_to_family_links[0].family_reference
        family = g.get_family_by_ref(family_ref)
        
        self.assertEqual(len(g.get_individuals()), 3)
        self.assertEqual(len(g.get_families()), 1)
        self.assertEqual(g.get_partner_of(pinco_pallino), pinca_caia)
        self.assertEqual(family.husband_reference, husb_ref)
        self.assertEqual(family.wife_reference, wife_ref)
        self.assertEqual(family.children_references[0], son_ref)
        self.assertEqual(list(g.get_parents_of(tizio_pallino))[0], pinca_caia)
        self.assertEqual(list(g.get_parents_of(tizio_pallino))[1], pinco_pallino)
        return g


    def test_siblings(self):
        g = self.test_create_simple_family()
        tizio_pallino = g.get_individual_by_ref("@I3@")
        caia_pallino = Individual("Caia", "Pallino", "F", "11-mar-1921", "26-nov-1971")
        g.add_individual(caia_pallino)
        g.link_individual(caia_pallino, tizio_pallino, genealogy.Genealogy.RELATIONSHIP_SIBLING)
        self.assertEqual(list(g.get_siblings_of(tizio_pallino))[0], caia_pallino)
        self.assertEqual(list(g.get_siblings_of(caia_pallino))[0], tizio_pallino)
        g.un_link_individual(tizio_pallino, caia_pallino, genealogy.Genealogy.RELATIONSHIP_SIBLING)
        self.assertEqual(len(g.get_siblings_of(tizio_pallino)), 0)
        self.assertEqual(len(g.get_siblings_of(caia_pallino)), 0)
        

    def test_unlink_father(self):
        g = self.test_create_simple_family()
        father = g.get_individual_by_ref("@I1@")
        son = g.get_individual_by_ref("@I3@")
        g.un_link_individual(father, son, genealogy.Genealogy.RELATIONSHIP_FATHER)
        self.assertEqual(len(list(g.get_children_of(father))), 0)
        self.assertIsNone(g.get_father_of(son))


    def test_unlink_child(self):
        g = self.test_create_simple_family()
        mother = g.get_individual_by_ref("@I2@")
        son = g.get_individual_by_ref("@I3@")
        g.un_link_individual(son, mother, genealogy.Genealogy.RELATIONSHIP_CHILD)
        self.assertEqual(len(list(g.get_children_of(mother))), 0)
        self.assertIsNone(g.get_mother_of(son))


    def test_unlink_partner(self):
        g = self.test_create_simple_family()
        father = g.get_individual_by_ref("@I1@")
        mother = g.get_individual_by_ref("@I2@")
        g.un_link_individual(father, mother, genealogy.Genealogy.RELATIONSHIP_PARTNER)
        self.assertIsNone(g.get_partner_of(father))
        self.assertIsNone(g.get_partner_of(mother))


if __name__ == "__main__":
    unittest.main()