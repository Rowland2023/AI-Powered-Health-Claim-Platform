registry = ToolRegistry()

registry.register_many([
    RegisterPatientTool(register_patient_use_case),
    CreateClaimTool(create_claim_use_case),
    SubmitClaimTool(submit_claim_use_case),
    ApproveClaimTool(approve_claim_use_case),
    RejectClaimTool(reject_claim_use_case),
    CreateMedicalRecordTool(create_medical_record_use_case),
])

tool_execution_service = ToolExecutionService(registry)

execute_ai_request_use_case = ExecuteAIRequestUseCase(
    llm_service=llm_service,
    tool_execution_service=tool_execution_service,
)