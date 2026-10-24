import pytest

from somx_core.ai import AccessDenied, ModelRouter
from somx_core.security import Gatekeeper
from somx_core.sovereignty import SovereigntyPolicy


def make_router():
    gk = Gatekeeper(b"test-secret")
    policy = SovereigntyPolicy(allowed_models=frozenset({"echo"}))
    router = ModelRouter(gk, policy)
    router.register("echo", lambda p: p.upper())
    return gk, router


def test_valid_request_passes():
    gk, router = make_router()
    assert router.route(gk.issue("user1"), "SO", "echo", "salaam") == "SALAAM"


def test_bad_token_denied():
    _, router = make_router()
    with pytest.raises(AccessDenied):
        router.route("fake.token.here", "SO", "echo", "x")


def test_expired_token_denied():
    gk = Gatekeeper(b"s", ttl=1)
    token = gk.issue("u", now=0)
    assert gk.verify(token, now=100) is False


def test_region_denied():
    gk, router = make_router()
    with pytest.raises(AccessDenied):
        router.route(gk.issue("u"), "US", "echo", "x")


def test_default_policy_denies_all_models():
    assert SovereigntyPolicy().check("SO", "echo") is False
