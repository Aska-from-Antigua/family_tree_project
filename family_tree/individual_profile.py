"""
individual_profile.py

Represents the personal and demographic details of an individual.
"""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class IndividualProfile:
    """Stores personal details such as names, gender, and birth/death years."""
    first_name: str
    last_name: str
    middle_name: str = None
    suffix: str = None
    gender: str = None
    birth_year: int = 1900
    death_year: int = None

    @property
    def full_name(self) -> str:
        """Returns the individual's full name."""
        parts = [self.first_name, self.middle_name, self.last_name, self.suffix]
        return ' '.join(str(x) for x in filter(None, parts))

    @property
    def age(self) -> int:
        pass

    @property
    def details(self) -> str:
        """Returns personal details, including age or lifespan."""
        if self.death_year:
            lifespan = f"({self.birth_year} - {self.death_year})"
            age = self.death_year - self.birth_year
        else:
            lifespan = f"({self.birth_year} - present)"
            age = datetime.now().year - self.birth_year

        parts = [self.full_name, self.gender, age, lifespan]
        return ' '.join(str(x) for x in filter(None, parts))

    def to_dict(self) -> dict:
        """Converts the personal information to a dictionary."""
        return {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "suffix": self.suffix,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "death_year": self.death_year,
        }

    @staticmethod
    def from_dict(data: dict) -> 'IndividualProfile':
        """Converts a dictionary to an IndividualProfile instance."""
        return IndividualProfile(
            first_name=data["first_name"],
            middle_name=data.get("middle_name"),
            last_name=data["last_name"],
            suffix=data.get("suffix"),
            gender=data.get("gender"),
            birth_year=data.get("birth_year"),
            death_year=data.get("death_year"),
        )
