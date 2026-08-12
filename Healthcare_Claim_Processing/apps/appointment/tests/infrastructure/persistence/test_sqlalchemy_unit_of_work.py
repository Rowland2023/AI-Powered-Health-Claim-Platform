from unittest.mock import AsyncMock, MagicMock

import pytest

from appointment.infrastructure.persistence.repositories.sqlalchemy_appointment_repository import (
    SQLAlchemyAppointmentRepository,
)
from appointment.infrastructure.persistence.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)


@pytest.fixture
def session():
    return AsyncMock()


@pytest.fixture
def session_factory(session):
    factory = MagicMock(return_value=session)
    return factory


@pytest.mark.asyncio
async def test_enter_creates_session_and_appointment_repository(
    session,
    session_factory,
):
    uow = SQLAlchemyUnitOfWork(session_factory)

    async with uow:
        assert uow.session is session

        assert isinstance(
            uow.appointment_repository,
            SQLAlchemyAppointmentRepository,
        )

        assert uow.appointment_repository.session is session


@pytest.mark.asyncio
async def test_commit_commits_session(
    session,
    session_factory,
):
    uow = SQLAlchemyUnitOfWork(session_factory)

    async with uow:
        await uow.commit()

    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_rollback_rolls_back_session(
    session,
    session_factory,
):
    uow = SQLAlchemyUnitOfWork(session_factory)

    async with uow:
        await uow.rollback()

    session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_exception_triggers_rollback(
    session,
    session_factory,
):
    uow = SQLAlchemyUnitOfWork(session_factory)

    with pytest.raises(ValueError):
        async with uow:
            raise ValueError("something went wrong")

    session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_session_is_closed_when_context_exits(
    session,
    session_factory,
):
    uow = SQLAlchemyUnitOfWork(session_factory)

    async with uow:
        pass

    session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_session_is_closed_after_exception(
    session,
    session_factory,
):
    uow = SQLAlchemyUnitOfWork(session_factory)

    with pytest.raises(RuntimeError):
        async with uow:
            raise RuntimeError("database failure")

    session.rollback.assert_awaited_once()
    session.close.assert_awaited_once()
    
@pytest.mark.asyncio
async def test_register_tracks_aggregate():
    session_factory = MagicMock()
    session = MagicMock()

    session_factory.return_value = session

    uow = SQLAlchemyUnitOfWork(session_factory)

    aggregate = MagicMock()

    uow.register(aggregate)

    assert aggregate in uow._registered_aggregates