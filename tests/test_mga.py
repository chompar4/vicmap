import pytest
from mga import geographic_to_mga
from datums import GDA20

def test_geographic_to_mga():

    z, E, N, m, γ = geographic_to_mga(-23.67012389, 133.8855133, datum=GDA20)

    assert z == 53
    assert round(E, 2) == round(386352.397753, 2)
    assert round(N, 2) == round(7381850.768886, 2)
    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481414