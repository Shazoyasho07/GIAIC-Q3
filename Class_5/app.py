import cal

def main() -> int:
    response: cal.add = cal.add(2, 5)
    assert response == 7, "Expected 2 + 5 to equal 7"
    return response

if __name__ == "__main__":
    result = main()
    print(f"Result: {result}")
