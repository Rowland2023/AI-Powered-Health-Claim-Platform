import pytest
from apps.claim.domain.value_objects.denial_reason import DenialReason

def test_valid_denial_reason():
    r = DenialReason(code="CO-50", description="Non-covered service")
    assert r.is_coding_error is True

def test_prior_auth_detection():
    r = DenialReason(code="PRIOR_AUTH_REQUIRED", description="Requires prior auth")
    assert r.is_prior_auth_required is True

def test_empty_code_raises():
    with pytest.raises(ValueError):
        DenialReason(code="", description="test")
