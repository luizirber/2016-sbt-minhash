import pytest

from sbt import SBT, DictSBT


#@pytest.fixture(params=[SBT])
@pytest.fixture(params=[SBT, DictSBT])
def SBTImplementation(request):
    return request.param
