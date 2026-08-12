from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from appointment.application.use_case.schedule_appointment import (
    ScheduleAppointmentUseCase,
)
from appointment.infrastructure.persistence.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)


def build_schedule_appointment_use_case(
    database_url: str,
) -> ScheduleAppointmentUseCase:
    engine = create_async_engine(
        database_url,
        echo=False,
    )

    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    unit_of_work = SQLAlchemyUnitOfWork(
        session_factory=session_factory,
    )

    return ScheduleAppointmentUseCase(
        unit_of_work=unit_of_work,
    )