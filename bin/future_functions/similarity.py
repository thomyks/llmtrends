from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity_matrix(abstract_embeddings, topic_embeddings):
    """Computes cosine similarity matrix between abstracts and topics."""
    return cosine_similarity(abstract_embeddings, topic_embeddings)
