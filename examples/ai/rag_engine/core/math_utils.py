import math


def vector_norm(v: list[float]) -> float:
    """Computes the L2 norm (magnitude) of a continuous vector."""
    return math.sqrt(sum(x * x for x in v))


def cosine_similarity(u: list[float], v: list[float]) -> float:
    """Computes Cosine Similarity between two continuous vectors u and v."""
    if len(u) != len(v):
        raise ValueError("Vector dimensionality mismatch.")

    dot_product = sum(a * b for a, b in zip(u, v))
    norm_u = vector_norm(u)
    norm_v = vector_norm(v)

    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0

    return dot_product / (norm_u * norm_v)