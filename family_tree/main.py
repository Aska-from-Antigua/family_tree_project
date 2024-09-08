"""test.py"""
import logging
from .logging_config import setup_logging
from .family_member import FamilyMember
from .individual_profile import IndividualProfile
from .serializers import serialize_family, deserialize_family

setup_logging(logging.WARN)



jerry = FamilyMember(IndividualProfile('Jerry', last_name='Aska', suffix='Jr', death_year=2023))
petra = FamilyMember(IndividualProfile('Petra', 'Williams'))
clarence = FamilyMember(IndividualProfile('Clarence', 'Williams'))
junie = FamilyMember(IndividualProfile('Jerry', 'Aska', suffix='Sr'))
petra.add_child(jerry, junie)
petra.add_parent(clarence)
# print()
# print(f'Ancestors for {jerry}')
# for person in jerry.get_ancestors():
#     print(repr(person))

# print()
# print(f'Descendents for {clarence}')
# for person in clarence.get_descendants():
#     print(repr(person))
# print()


json_data = serialize_family({jerry, petra, clarence, junie})

family = deserialize_family(json_data)

# for member in family:
#     print(repr(member))

print(json_data)