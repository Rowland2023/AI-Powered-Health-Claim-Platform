
from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ============================================================
# REQUEST SCHEMAS
# ============================================================


class RegisterPatientRequest(BaseModel):
    """
    HTTP request body for registering a patient.
    """

    medical_record_number: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    email: EmailStr

    phone_number: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    gender: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    date_of_birth: date

    address: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )


class UpdatePatientContactInformationRequest(BaseModel):
    """
    HTTP request body for updating patient contact information.
    """

    email: EmailStr

    phone_number: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    address: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )


# ============================================================
# RESPONSE SCHEMAS
# ============================================================


class PatientResponse(BaseModel):
    """
    HTTP representation of a Patient aggregate.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    medical_record_number: str
    name: str
    email: str
    phone_number: str
    gender: str
    date_of_birth: date
    address: str

    active: bool

    created_at: str
    updated_at: str
