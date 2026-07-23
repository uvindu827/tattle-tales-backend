import logging
import numpy as np

from .ollama_client import get_embedding

logger = logging.getLogger(__name__)

SIMILLIARITY_THRESHOLD = 0.85

def cosine_similliarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Calculating the cosine similliarity of 2 vectores 
    used for calculating the similliarity of 2 aricles
    """
    a = np.array(vec_a)
    b = np.array(vec_b)

    dot_product = a.b

    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)

def _embed_article(article: dict) -> list[float]:
    """
    Get the embedding of a single article
    """
    text_to_embed = f"{article["title"]}. {article["summary"]}"

    return get_embedding(text_to_embed)

def cluster_article(
        articles: list[dict], 
        similliarity_threshold: float = SIMILLIARITY_THRESHOLD
    ) -> list[list[dict]]:

    """
    Group the articles in to same cluster that are about same event
    """

    clusters = list[dict] = []

    for article in articles:
        embedding = _embed_article(article)

        best_cluster_index = None
        best_similliarity = -1.0

        for i, cluster in enumerate(clusters):
            similliarity = cosine_similliarity(embedding, cluster["centroid"])

            if similliarity > best_similliarity:
                best_similliarity = similliarity
                best_cluster_index = i

        if best_cluster_index is not None and best_similliarity >= similliarity_threshold:
            cluster = clusters[best_cluster_index]
            cluster["articles"].append(article)

            cluster["embeddings"].append(embedding)
            cluster["centroid"] = np.mean(cluster["embeddings"], axis=0).tolist()

            logger.info(
                "Article '%s' joined an existing cluster (similliarity: %.3f)",
                article["title"][:50],
                best_similliarity
            )

        else:
            clusters.append({
                "articles": [article],
                "embeddings": [embedding],
                "centroid": embedding
            })

            logger.info(
                "Article '%s' started a new cluster (best similliarity: %.3f)",
                article["title"][:50],
                best_similliarity if best_similliarity is not None else 0.0
            )

    return [cluster["articles"] for cluster in clusters]








