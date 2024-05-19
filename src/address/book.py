from __future__ import annotations

import doctest
import json
import logging
import os
import pathlib
from typing import Any, TypedDict

from .address import MISSING, Address, AddressDict, _MissingSentinel

log = logging.getLogger(__name__)


class JsonEncoder(json.JSONEncoder):
    def default(self, other: _MissingSentinel | Any) -> Any:
        if isinstance(other, _MissingSentinel):
            return None
        return super().default(other)


class AddressBookDict(TypedDict):
    id: int
    name: str
    addresses: list[AddressDict]


class AddressBook:
    def __init__(self) -> None:
        """
        >>> address_book = AddressBook()
        >>> address_book
        <AddressBook name=... total_addresses=0>
        >>> address_book.book_holder_name = "John Doe"
        >>> address_book
        <AddressBook name=John Doe total_addresses=0>
        """
        self.__book_holder_name: str = MISSING
        self.__book_holder_id: int = MISSING
        self.__addresses: set[Address] = set()

    @property
    def book_holder_name(self) -> str:
        return self.__book_holder_name

    @book_holder_name.setter
    def book_holder_name(self, name: str) -> None:
        log.debug("setting book holder name to %s", name)
        self.__book_holder_name = name

    @property
    def book_holder_id(self) -> int:
        return self.__book_holder_id

    @book_holder_id.setter
    def book_holder_id(self, id: int) -> None:
        log.debug("setting book holder id to %s", id)
        self.__book_holder_id = id

    def add_address(self, address: Address) -> None:
        log.info("adding address %s to address book", address)
        self.__addresses.add(address)

    def remove_address(self, address: Address) -> None:
        log.info("removing address %s from address book", address)
        self.__addresses.remove(address)

    def __repr__(self) -> str:
        return f"<AddressBook name={self.__book_holder_name} total_addresses={len(self.__addresses)}>"

    def __str__(self) -> str:
        return self.__book_holder_name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AddressBook):
            return False
        return self.__book_holder_id == other.__book_holder_id

    def __len__(self) -> int:
        return len(self.__addresses)

    def __iter__(self):
        return iter(self.__addresses)

    def __contains__(self, address: Address) -> bool:
        return address in self.__addresses

    def __getitem__(self, index: int) -> Address:
        return sorted(list(self.__addresses), key=lambda x: x.recipient_name)[index]

    def __setitem__(self, index: int, address: Address) -> None:
        self.__addresses.add(address)

    def to_dict(self) -> AddressBookDict:
        """
        >>> address_book = AddressBook()
        >>> address_book.book_holder_name = "John Doe"
        >>> address_book.book_holder_id = 1
        >>> address_book.add_address(Address(recipient_name="Ritik"))
        >>> address_book.to_dict()
        {'name': 'John Doe', 'id': 1, 'addresses': [{'recipient_name': 'Ritik', 'organization_name': None, 'building_number': None, 'street_name': None, 'apartment_number': None, 'city': None, 'state': None, 'postal_code': None}]}
        """
        return {
            "name": self.__book_holder_name,
            "id": self.__book_holder_id,
            "addresses": [address.to_dict() for address in self.__addresses],
        }

    def to_file(self, file_path: str | None = None) -> None:
        """
        >>> address_book = AddressBook()
        >>> address_book.book_holder_name = "John Doe"
        >>> address_book.book_holder_id = 1
        >>> address_book.add_address(Address(recipient_name="Ritik"))
        >>> address_book.to_file()
        """
        if file_path is None:
            path = pathlib.Path(__file__).parent / "address_book.json"
        else:
            path = pathlib.Path(file_path)

        with open(path, "w+") as file:
            json.dump(self.to_dict(), file, indent=4, cls=JsonEncoder)

    @classmethod
    def from_file(cls, file_path: str | None = None) -> AddressBook:
        """
        >>> AddressBook.from_file(None)
        """
        if file_path is None:
            path = pathlib.Path(__file__).parent / "address_book.json"
        else:
            path = pathlib.Path(file_path)

        if not os.path.exists(path):
            log.warning("file %s does not exist", path)
            return cls()

        log.debug("loading address book from %s", path)
        with open(path, "r") as file:
            data = json.load(file)

        address_book = cls()
        address_book.book_holder_name = data["name"]
        address_book.book_holder_id = data["id"]

        for address in data["addresses"]:
            address_book.add_address(Address(**address))

        return address_book


if __name__ == "__main__":
    doctest.testmod()
