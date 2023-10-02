import random


def has_duplicate_birthday(people_count):
    birthdays = [random.randint(1, 365) for _ in range(people_count)]
    unique_birthdays = set(birthdays)
    return len(birthdays) != len(unique_birthdays)


def simulate_birthday_paradox(trials, people_count):
    duplicate_count = 0
    for _ in range(trials):
        if has_duplicate_birthday(people_count):
            duplicate_count += 1
    return duplicate_count / trials


if __name__ == "__main__":
    trials = 10000
    people_count = 75
    probability = simulate_birthday_paradox(trials, people_count)
    print(f"Probability of at least two people sharing a birthday in a group of {people_count}: {probability}")
