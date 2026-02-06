from aicorp.scorer import NEVInputs, calculate_nev


def test_calculate_nev():
    inputs = NEVInputs(
        revenue=100.0,
        costs=40.0,
        legal_risk=10.0,
        harm_risk=5.0,
        reputation_decay=5.0,
        uncertainty_penalty=10.0,
    )
    score = calculate_nev(inputs)
    assert score.total == 30.0
