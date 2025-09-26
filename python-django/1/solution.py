def queranumeric(order: list[str], words: list[str]) -> list[str]:
    ordered_map = {char: i for i, char in enumerate(order)}
    return sorted(words, key=lambda word: [ordered_map[char] for char in word])

