
@pytest.mark.asyncio
async def test_unit_of_work_commits_patient_and_outbox_atomically(
    session_factory,
):
    patient = make_patient()

    async with SQLAlchemyUnitOfWork(
        session_factory
    ) as uow:

        await uow.patient_repository.add(patient)

        uow.register(patient)

        await uow.commit()

    async with session_factory() as session:

        from patient.infrastructure.persistence.models.patient_model import (
            PatientModel,
        )

        patient_stmt = select(PatientModel).where(
            PatientModel.id == patient.id
        )

        patient_result = await session.execute(
            patient_stmt
        )

        stored_patient = (
            patient_result.scalar_one_or_none()
        )

        assert stored_patient is not None

        outbox_stmt = select(
            OutboxEventModel
        ).where(
            OutboxEventModel.aggregate_id
            == str(patient.id)
        )

        outbox_result = await session.execute(
            outbox_stmt
        )

        outbox_record = outbox_result.scalar_one()

        assert outbox_record.event_name == (
            "PatientRegistered"
        )

        assert outbox_record.status == "pending"
