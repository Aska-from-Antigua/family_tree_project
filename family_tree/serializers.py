"""
serializers.py

Handles serialization and deserialization of
family tree data to and from JSON format.
"""
import json
import uuid
from .family_member import FamilyMember

def serialize_family(members: set[FamilyMember]) -> str:
    """Converts a set of FamilyMember instances into a JSON string."""
    return json.dumps([member.to_dict() for member in members], indent=4)


def deserialize_family(data: str) -> set[FamilyMember]:
    """Reconstructs a set of FamilyMember instances from a JSON string."""
    data_list = json.loads(data)
    members: set[FamilyMember] = {}
    # First pass: create all members
    for member_data in data_list:
        FamilyMember.from_dict(member_data, members)
    # Second pass: link relationships
    for member_data in data_list:
        member: FamilyMember = members[uuid.UUID(member_data['id'])]
        member.parents = {members[uuid.UUID(pid)]
                          for pid in member_data['parents']}
        member.children = {members[uuid.UUID(cid)]
                           for cid in member_data['children']}
        member.partners = {members[uuid.UUID(pid)]
                           for pid in member_data['partners']}
    return set(members.values())
