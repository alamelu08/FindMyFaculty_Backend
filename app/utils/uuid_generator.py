import uuid
from app.utils.name_normalizer import normalize_name


def generate_faculty_uuid(name: str) -> str:
    """
    Generate a deterministic UUID v5 for a faculty.
    The same normalized faculty name will always produce the same UUID.
    """

    normalized_name = normalize_name(name)

    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            normalized_name
        )
    )