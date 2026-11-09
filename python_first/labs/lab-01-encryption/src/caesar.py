import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""  # Строка для зашифровки
    for symbol in plaintext:  # Проходим каждый символ из строки для зашифровки
        if symbol.isalpha():  # Проверяем является ли символ буквой
            first_symbol = (
                ord("a") if symbol.islower() else ord("A")
            )  # Проверяем является ли первый символ строчным или заглавным, чтобы получить его код
            shifted_symbol = chr(
                (ord(symbol) - first_symbol + shift) % 26 + first_symbol
            )  # Сдвигаем каждый символ на шифт позиций, используя остаток от деления, чтобы зациклить сдвиги.(получаем зашифрованный символ)
        else:
            shifted_symbol = symbol  # Если символ - не буква, просто записываем его
        ciphertext += shifted_symbol  # Добавляем к тексту сдвинутый символ
    return ciphertext  # Возвращаем зашифрованную строку


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""  # Строка для расшифровки
    for symbol in ciphertext:  # Проходим каждый символ из зашифрованной строки
        if symbol.isalpha():  # Проверяем является ли символ буквой
            start = (
                ord("a") if symbol.islower() else ord("A")
            )  # Проверяем является ли первый символ строчным или заглавным, чтобы получить его код
            shifted_symbol = chr(
                (ord(symbol) - start - shift) % 26 + start
            )  # Получаем сдвинутый символ обратно
        else:
            shifted_symbol = symbol  # Если символ - не буква, просто записываем его
        plaintext += shifted_symbol  # Добавляем к тексту сдвинутый символ
    return plaintext  # Возвращаем расшифрованную строку


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
