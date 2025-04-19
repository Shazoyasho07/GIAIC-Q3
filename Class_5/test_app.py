import cal

def test_main() -> int:
    response1: cal.add = cal.add(2, 5)
    assert response1 == 7, "Expected 2 + 5 to equal 7"

    response2: cal.add = cal.add(0, 0)
    assert response2 == 0, "Expected 0 + 0 to equal 0"

    response3: cal.add = cal.add(-2, -2)
    assert response3 == -4, "Expected -2 + -2 to equal -4"
