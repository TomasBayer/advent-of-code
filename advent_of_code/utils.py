import requests


def get_advent_of_code_test_data(year: int, day: int, session_cookie: str) -> str:
    response = requests.get(
        url=f'https://adventofcode.com/{year}/day/{day}/input',
        headers={
            'cookie': f'session={session_cookie}',
        },
        timeout=5,
    )

    if response.status_code == 200:
        return response.text.strip()
    elif response.status_code == 404:
        raise ValueError(f"Test data not found for Advent of Code {year}, Day {day}.")
    elif response.status_code == 400:
        raise ValueError("Invalid session cookie.")
    else:
        raise ValueError(f"Unknown error. Status code: {response.status_code}")
