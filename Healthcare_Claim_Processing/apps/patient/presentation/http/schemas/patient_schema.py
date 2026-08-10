
from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterPatientRequest(BaseModel):
    """
    HTTP request schema for registering a patient.
    """

    medical_record_number: str = Field(
        min_length=1,
        max_length=100,
    )

    first_name: str = Field(
        min_length=1,
        max_length=100,
    )

    last_name: str = Field(
        min_length=1,
        max_length=100,
    )

    email: EmailStr

    phone_number: str = Field(
        min_length=1,
        max_length=50,
    )

    gender: str = Field(
        min_length=1,
        max_length=50,
    )

    date_of_birth: date

    street: str = Field(
        min_length=1,
        max_length=255,
    )

    city: str = Field(
        min_length=1,
        max_length=100,
    )

    state: str = Field(
        min_length=1,
        max_length=100,
    )

    postal_code: str = Field(
        min_length=1,
        max_length=20,
    )

    country: str = Field(
        min_length=1,
        max_length=100,
    )


class UpdatePatientContactInformationRequest(BaseModel):
    """
    HTTP request schema for updating patient contact information.
    """

    email: EmailStr

    phone_number: str = Field(
        min_length=1,
        max_length=50,
    )

    street: str = Field(
        min_length=1,
        max_length=255,
    )

    city: str = Field(
        min_length=1,
        max_length=100,
    )

    state: str = Field(
        min_length=1,
        max_length=100,
    )

    postal_code: str = Field(
        min_length=1,
        max_length=20,
    )

    country: str = Field(
        min_length=1,
        max_length=100,
    )


class PatientResponse(BaseModel):
    """
    HTTP representation of a Patient.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    medical_record_number: str
    name: str
    email: str
    phone_number: str
    gender: str
    date_of_birth: date
    address: str
    active: bool
