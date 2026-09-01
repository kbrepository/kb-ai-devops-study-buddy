import time

import faiss
import numpy as np


DIMENSION = 1024
VECTOR_COUNT = 100_000
QUERY_COUNT = 100
TOP_K = 5

EF_SEARCH_VALUES = [16, 32, 64, 128, 256, 512]


def generate_vectors(count):
    vectors = np.random.random(
        (count, DIMENSION)
    ).astype("float32")

    faiss.normalize_L2(vectors)
    return vectors


def generate_queries():
    queries = np.random.random(
        (QUERY_COUNT, DIMENSION)
    ).astype("float32")

    faiss.normalize_L2(queries)
    return queries


def calculate_recall(flat_indices, hnsw_indices):
    total_matches = 0
    total_expected = flat_indices.size

    for flat_result, hnsw_result in zip(
        flat_indices,
        hnsw_indices,
    ):
        total_matches += len(
            set(flat_result) & set(hnsw_result)
        )

    return total_matches / total_expected


def main():
    print(f"Generating {VECTOR_COUNT:,} vectors...")

    vectors = generate_vectors(VECTOR_COUNT)
    queries = generate_queries()

    # Exact ground truth
    flat_index = faiss.IndexFlatIP(DIMENSION)
    flat_index.add(vectors)

    start = time.perf_counter()
    _, flat_indices = flat_index.search(
        queries,
        TOP_K,
    )
    flat_search_time = time.perf_counter() - start

    print(
        f"Flat search time: {flat_search_time:.6f}s"
    )

    # Build HNSW once
    print("\nBuilding HNSW index...")

    hnsw_index = faiss.IndexHNSWFlat(
        DIMENSION,
        32,
        faiss.METRIC_INNER_PRODUCT,
    )

    hnsw_index.hnsw.efConstruction = 200

    start = time.perf_counter()
    hnsw_index.add(vectors)
    build_time = time.perf_counter() - start

    print(f"HNSW build time: {build_time:.4f}s")

    print("\n" + "=" * 60)
    print("efSearch tuning")
    print("=" * 60)

    for ef_search in EF_SEARCH_VALUES:
        hnsw_index.hnsw.efSearch = ef_search

        start = time.perf_counter()

        _, hnsw_indices = hnsw_index.search(
            queries,
            TOP_K,
        )

        search_time = time.perf_counter() - start

        recall = calculate_recall(
            flat_indices,
            hnsw_indices,
        )

        print(
            f"efSearch={ef_search:<3} "
            f"| Search={search_time:.6f}s "
            f"| Recall@{TOP_K}={recall:.2%}"
        )


if __name__ == "__main__":
    main()