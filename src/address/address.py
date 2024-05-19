from __future__ import annotations

import doctest
from typing import Any, TypedDict


class _MissingSentinel:
    """
    A sentinel class representing a missing value.

    This class is used to indicate a missing value in certain contexts.
    It overrides the equality, boolean, and hash methods to always return False or 0.
    """

    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return "..."


MISSING: Any = _MissingSentinel()


class AddressDict(TypedDict):
    recipient_name: str
    organization_name: str | None
    building_number: str | None
    street_name: str | None
    apartment_number: str | None
    city: str | None
    state: str | None
    postal_code: str | None


class Address:
    def __init__(
        self,
        *,
        recipient_name: str,
        organization_name: str | None = None,
        building_number: str | None = None,
        street_name: str | None = None,
        apartment_number: str | None = None,
        city: str | None = None,
        state: str | None = None,
        postal_code: str | None = None,
        **kwargs,
    ) -> None:
        """Address class to represent a physical address

        >>> address = Address(recipient_name="John Doe", building_number="123", street_name="Main St")
        >>> address
        <Address recipient_name=John Doe>
        >>> address.building_number
        '123'
        """
        self.recipient_name: str = recipient_name
        self.organization_name = organization_name
        self.building_number = building_number
        self.street_name = street_name
        self.apartment_number = apartment_number
        self.city = city
        self.state = state
        self.postal_code = postal_code

    @property
    def id(self) -> str:
        return "0" + str(hash(self))

    def __str__(self) -> str:
        address = ""
        if self.recipient_name:
            address += f"{self.recipient_name}\n"
        if self.organization_name:
            address += f"{self.organization_name}\n"
        if self.building_number:
            address += f"{self.building_number} "
        if self.street_name:
            address += f"{self.street_name}\n"
        if self.apartment_number:
            address += f"{self.apartment_number}\n"
        if self.city:
            address += f"{self.city}, "
        if self.state:
            address += f"{self.state} "
        if self.postal_code:
            address += f"{self.postal_code}\n"
        return address

    def __repr__(self) -> str:
        return "<Address recipient_name=%s>" % self.recipient_name

    def __eq__(self, other: Address) -> bool:
        """
        >>> addr1 = Address(recipient_name="Ritik")
        >>> addr2 = Address(recipient_name="Ritik")
        >>> addr1 == addr2
        True
        """
        return all(
            [
                self.recipient_name == other.recipient_name,
                self.organization_name == other.organization_name,
                self.building_number == other.building_number,
                self.street_name == other.street_name,
                self.apartment_number == other.apartment_number,
                self.city == other.city,
                self.state == other.state,
                self.postal_code == other.postal_code,
            ]
        )

    def edit(
        self,
        *,
        recipient_name: str = MISSING,
        organization_name: str | None = MISSING,
        building_number: str | None = MISSING,
        street_name: str | None = MISSING,
        apartment_number: str | None = MISSING,
        city: str | None = MISSING,
        state: str | None = MISSING,
        postal_code: str | None = MISSING,
    ) -> Address:
        """
        >>> address = Address(recipient_name="John Doe", building_number="123", street_name="Main St")
        >>> address
        <Address recipient_name=John Doe>
        >>> address.building_number
        '123'
        >>> address.edit(building_number="456")
        <Address recipient_name=John Doe>
        >>> address.building_number
        '456'
        """
        if recipient_name is not MISSING:
            self.recipient_name = recipient_name

        if organization_name is not MISSING:
            self.organization_name = organization_name

        if building_number is not MISSING:
            self.building_number = building_number

        if street_name is not MISSING:
            self.street_name = street_name

        if apartment_number is not MISSING:
            self.apartment_number = apartment_number

        if city is not MISSING:
            self.city = city

        if state is not MISSING:
            self.state = state

        if postal_code is not MISSING:
            self.postal_code = postal_code

        return self

    def __delattr__(self, name: str) -> None:
        """
        >>> address = Address(recipient_name="John Doe", building_number="123", street_name="Main St")
        >>> address
        <Address recipient_name=John Doe>
        >>> del address.recipient_name
        Traceback (most recent call last):
            ...
        AttributeError: Cannot delete attributes from an Address
        """
        raise AttributeError("Cannot delete attributes from an Address")

    def json(self) -> AddressDict:
        """Returns the address as a JSON serializable dictionary

        >>> address = Address(recipient_name="John Doe", building_number="123", street_name="Main St")
        >>> address.json()
        {'recipient_name': 'John Doe', 'organization_name': None, 'building_number': '123', 'street_name': 'Main St', 'apartment_number': None, 'city': None, 'state': None, 'postal_code': None}
        """
        return {
            "recipient_name": self.recipient_name,
            "organization_name": self.organization_name or None,
            "building_number": self.building_number or None,
            "street_name": self.street_name or None,
            "apartment_number": self.apartment_number or None,
            "city": self.city or None,
            "state": self.state or None,
            "postal_code": self.postal_code or None,
        }

    @staticmethod
    def from_dict(json: AddressDict) -> Address:
        """Returns an Address object from a JSON serializable dictionary

        >>> address = Address.from_dict({'recipient_name': 'John Doe', 'organization_name': None, 'building_number': '123', 'street_name': 'Main St', 'apartment_number': None, 'city': None, 'state': None, 'postal_code': None})
        >>> address
        <Address recipient_name=John Doe>
        """

        return Address(
            recipient_name=json.get("recipient_name"),
            organization_name=json.get("organization_name"),
            building_number=json.get("building_number"),
            street_name=json.get("street_name"),
            apartment_number=json.get("apartment_number"),
            city=json.get("city"),
            state=json.get("state"),
            postal_code=json.get("postal_code"),
        )

    @classmethod
    def from_address(cls, address: Address) -> Address:
        """Returns a new Address object from an existing Address object

        >>> address = Address(recipient_name="John Doe", building_number="123", street_name="Main St")
        >>> new_address = Address.from_address(address)
        >>> new_address
        <Address recipient_name=John Doe>
        """
        return cls(
            recipient_name=address.recipient_name,
            organization_name=address.organization_name,
            building_number=address.building_number,
            street_name=address.street_name,
            apartment_number=address.apartment_number,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
        )

    def to_dict(self) -> AddressDict:
        """Returns the address as a JSON serializable dictionary

        >>> address = Address(recipient_name="John Doe", building_number="123", street_name="Main St")
        >>> address.to_dict()
        {'recipient_name': 'John Doe', 'organization_name': None, 'building_number': '123', 'street_name': 'Main St', 'apartment_number': None, 'city': None, 'state': None, 'postal_code': None}
        """
        return self.json()

    def __hash__(self) -> int:
        return hash(
            (
                self.recipient_name,
                self.organization_name,
                self.building_number,
                self.street_name,
                self.apartment_number,
                self.city,
                self.state,
                self.postal_code,
            )
        )


if __name__ == "__main__":
    doctest.testmod()
