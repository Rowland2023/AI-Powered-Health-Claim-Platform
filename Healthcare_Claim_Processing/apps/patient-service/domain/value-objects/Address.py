### `patient/domain/value_objects/Address.py`

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    """
    Value Object representing a patient's residential address.

    The address is immutable and guarantees that the required
    address components contain meaningful values.
    """

    street: str
    city: str
    state: str
    postal_code: str
    country: str = "NG"

    def __post_init__(self) -> None:
        street = self.street.strip()
        city = self.city.strip()
        state = self.state.strip()
        postal_code = self.postal_code.strip()
        country = self.country.strip().upper()

        if not street:
            raise ValueError(
                "Street address cannot be empty."
            )

        if not city:
            raise ValueError(
                "City cannot be empty."
            )

        if not state:
            raise ValueError(
                "State cannot be empty."
            )

        if not postal_code:
            raise ValueError(
                "Postal code cannot be empty."
            )

        if not country:
            raise ValueError(
                "Country cannot be empty."
            )

        if len(country) != 2:
            raise ValueError(
                "Country must be a two-letter ISO country code."
            )

        object.__setattr__(
            self,
            "street",
            street,
        )

        object.__setattr__(
            self,
            "city",
            city,
        )

        object.__setattr__(
            self,
            "state",
            state,
        )

        object.__setattr__(
            self,
            "postal_code",
            postal_code,
        )

        object.__setattr__(
            self,
            "country",
            country,
        )
