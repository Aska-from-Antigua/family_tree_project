"""
family_member.py

This module defines the FamilyMember class, which models family relationships
and allows for managing and traversing family trees. The class includes
serialization and deserialization functionality for storing and retrieving
family trees in JSON format.
"""
from __future__ import annotations
import logging
import uuid
from .utils import validate_input
from .individual_profile import IndividualProfile
logger = logging.getLogger("family_member")

class FamilyMember:
    """
    Models a family member with personal details and relationships such as
    parents, children, and partners. Relationships are bi-directional,
    and the class supports traversing ancestors and descendants.
    """

    def __init__(self, profile: IndividualProfile, member_id: uuid.uuid4 = None) -> None:
        """Initialize a FamilyMember with a unique ID and personal details."""
        self.member_id = member_id if member_id else uuid.uuid4()
        self.profile = profile
        self.parents: set[FamilyMember] = set()
        self.children: set[FamilyMember] = set()
        self.partners: set[FamilyMember] = set()
        logger.info('Family member named %s created', self.profile.full_name)

    def add_partner(self, partner: FamilyMember) -> None:
        """Reciprocally adds a partner to this family member."""
        validate_input(partner, FamilyMember, var_name='Partner')

        if partner in self.partners:
            logger.warning('%s already a partner for %s', partner,  self)
            return
        self.partners.add(partner)
        partner.partners.add(self)
        logger.info('Added %s as a partner to %s', partner, self)

    def add_child(self, child: FamilyMember, partner: FamilyMember = None) -> None:
        """Adds a child and optionally links to a partner as the other parent."""
        validate_input(child, FamilyMember, 'Child')
        validate_input(partner, FamilyMember, 'Partner', True)

        if child in self.children:
            logger.warning('%s already a child for %s', child, self)
            return
        self.children.add(child)
        child.parents.add(self)
        logger.info('Added %s as child to %s', child, self)
        if partner:
            self.add_partner(partner)
            partner.add_child(child)

    def add_parent(self, parent: FamilyMember) -> None:
        """Adds a parent to this family member."""
        parent.add_child(self)

    def add_partners(self, partners: list[FamilyMember]) -> None:
        """Adds multiple partners at once."""
        logger.debug('Bulk assigning partners to %s', self)
        for partner in partners:
            self.add_partner(partner)

    def add_children(self, children: list[FamilyMember], partner: FamilyMember = None) -> None:
        """Adds multiple children at once and optionally links a partner."""
        logger.debug('Bulk assigning children to %s', self)
        for child in children:
            self.add_child(child, partner)

    def add_parents(self, parents: list[FamilyMember]) -> None:
        """Adds multiple parents at once."""
        logger.debug('Bulk assigning parents to %s', self)
        for parent in parents:
            self.add_parent(parent)

    def __str__(self) -> str:
        return self.profile.full_name

    def __repr__(self) -> str:
        return self.profile.details

    def __hash__(self):
        return hash(self.member_id)

    def __eq__(self, other):
        if not isinstance(other, FamilyMember):
            return False
        return (self.member_id) == (other.member_id)

    def to_dict(self) -> dict:
        """Serializes the FamilyMember instance to a dictionary format."""
        return {
            'id': str(self.member_id),
            "profile": self.profile.to_dict(),
            'parents': [str(parent.member_id) for parent in self.parents],
            'children': [str(child.member_id) for child in self.children],
            'partners': [str(partner.member_id) for partner in self.partners],
        }

    @staticmethod
    def from_dict(data: dict, members: dict) -> FamilyMember:
        """Deserializes a FamilyMember from a dictionary."""
        profile = IndividualProfile.from_dict(data["profile"])
        member_id = uuid.UUID(data['id'])
        member = FamilyMember(profile, member_id)
        members[member_id] = member

        return member

    def get_descendants(self) -> list[FamilyMember]:
        """Retrieves a list of all descendants of the current family member."""
        descendants = []
        stack = list(self.children)
        while stack:
            current = stack.pop()
            if current not in descendants:
                descendants.append(current)
                stack.extend(current.children)
        return descendants

    def get_ancestors(self) -> list[FamilyMember]:
        """Retrieves a list of all ancestors of the current family member."""
        ancestors = []
        stack = list(self.parents)
        while stack:
            current = stack.pop()
            if current not in ancestors:
                ancestors.append(current)
                stack.extend(current.parents)
        return ancestors
