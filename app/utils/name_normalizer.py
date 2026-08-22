import re


def normalize_name(name: str) -> str:
    """
    Normalizes faculty names.

    Examples
    --------
    Dr.Saranya K G  -> Saranya K G
    Saranya KG      -> Saranya K G
    saranya kg      -> Saranya K G
    K.G.            -> K G
    """

    name = name.strip()

    # Remove titles
    name = re.sub(
        r"^(Dr|Mr|Mrs|Ms|Prof)\.?\s*",
        "",
        name,
        flags=re.IGNORECASE,
    )

    # Replace dots with spaces
    name = name.replace(".", " ")

    # Remove duplicate spaces
    name = " ".join(name.split())

    words = name.split()

    normalized = []

    for i, word in enumerate(words):

        # Title case normal words
        word = word.capitalize()

        # Only split the LAST word if it is exactly 2 letters
        if (
            i == len(words) - 1
            and len(word) == 2
            and word.isalpha()
        ):
            normalized.extend([word[0].upper(), word[1].upper()])

        else:
            normalized.append(word)

    return " ".join(normalized)