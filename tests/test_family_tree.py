import unittest
from family_tree.family_member import FamilyMember
from family_tree.individual_profile import IndividualProfile

class TestFamilyTree(unittest.TestCase):
    def setUp(self):
        """Set up test family members"""
        self.luffy = FamilyMember(IndividualProfile(first_name="Monkey", middle_name="D", last_name="Luffy", birth_year=1980))
        self.dragon = FamilyMember(IndividualProfile(first_name="Monkey", middle_name="D", last_name="Dragon", birth_year=1980))
        self.garp = FamilyMember(IndividualProfile(first_name="Monkey", middle_name="D", last_name="Garp", birth_year=1980))

        self.john = FamilyMember(IndividualProfile(first_name="John", last_name="Doe", birth_year=1980))
        self.jane = FamilyMember(IndividualProfile(first_name="Jane", last_name="Doe", birth_year=1982))
        self.junior = FamilyMember(IndividualProfile(first_name="Junior", last_name="Doe", birth_year=2010))

    def test_add_child(self):
        """Test that a child is correctly added to a parent."""
        self.john.add_child(self.junior)
        self.assertIn(self.junior, self.john.children)
        self.assertIn(self.john, self.junior.parents)

    def test_add_parent(self):
        """Test that adding a parent works as expected."""
        self.junior.add_parent(self.john)
        self.assertIn(self.junior, self.john.children)
        self.assertIn(self.john, self.junior.parents)

    def test_add_partner(self):
        """Test that partners are correctly added and reciprocated."""
        self.john.add_partner(self.jane)
        self.assertIn(self.jane, self.john.partners)
        self.assertIn(self.john, self.jane.partners)

    def test_serialize_family(self):
        """Test that family members can be serialized to a dictionary."""
        self.john.add_child(self.junior)
        serialized = self.john.to_dict()
        self.assertEqual(serialized['profile']['first_name'], "John")
        self.assertIn(str(self.junior.member_id), serialized['children'])

    def test_deserialize_family(self):
        """Test that a family member can be deserialized from a dictionary."""
        self.john.add_child(self.junior)
        serialized = self.john.to_dict()
        members = {}
        deserialized_member = FamilyMember.from_dict(serialized, members)
        self.assertEqual(deserialized_member.profile.first_name, "John")

    def test_get_descendants(self):
        """Test that all descendants of a member are correctly retrieved."""
        self.john.add_child(self.junior)
        descendants = self.john.get_descendants()
        self.assertIn(self.junior, descendants)

    def test_get_ancestors(self):
        """Test that all ancestors of a member are correctly retrieved."""
        self.junior.add_parent(self.john)
        ancestors = self.junior.get_ancestors()
        self.assertIn(self.john, ancestors)

if __name__ == '__main__':
    unittest.main()
