def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""  # Пустая строка для шифрованного текста
    keyword = keyword.upper()  # Преобразуем ключ в верхний регистр
    keyword_length = len(keyword)  # Длина ключа
    for i in range(len(plaintext)):  # Цикл по каждому символу открытого текста
        char = plaintext[i]  # Текущий символ открытого текста
        if char.isalpha():  # Если символ - буква:
            shift = ord(keyword[i % keyword_length]) - ord("A")  # Вычисляем сдвиг по ключу
            if char.isupper():  # Если символ в верхнем регистре:
                shifted_char = chr(
                    (ord(char) - ord("A") + shift) % 26 + ord("A")
                )  # Вычисляем сдвинутый символ
            else:  # Если символ в нижнем регистре:
                shifted_char = chr(
                    (ord(char) - ord("a") + shift) % 26 + ord("a")
                )  # Вычисляем сдвинутый символ
            ciphertext += shifted_char  # Добавляем сдвинутый символ к шифрованному тексту
        else:  # Если символ не буква:
            ciphertext += char  # Добавляем символ к шифрованному тексту без изменений
    return ciphertext  # Возвращаем шифрованный текст


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""  # Пустая строка для дешифрованного текста
    keyword = keyword.upper()  # Преобразуем ключ в верхний регистр
    for i in range(len(ciphertext)):  # Цикл по каждому символу шифрованного текста
        char = ciphertext[i]  # Текущий символ шифрованного текста
        if char.isalpha():  # Если символ - буква:
            shift = ord(keyword[i % len(keyword)]) - ord("A")  # Вычисляем сдвиг по ключу
            if char.isupper():  # Если символ в верхнем регистре:
                shifted_char = chr(
                    (ord(char) - ord("A") - shift) % 26 + ord("A")
                )  # Вычисляем сдвинутый символ
            else:  # Если символ в нижнем регистре:
                shifted_char = chr(
                    (ord(char) - ord("a") - shift) % 26 + ord("a")
                )  # Вычисляем сдвинутый символ
            plaintext += shifted_char  # Добавляем сдвинутый символ к дешифрованному тексту
        else:  # Если символ не буква:
            plaintext += char  # Добавляем символ к дешифрованному тексту без изменений
    return plaintext  # Возвращаем дешифрованный текст
