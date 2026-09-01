# FAISS Scaling Experiments

## Why this experiment?

The AI DevOps Study Buddy currently contains only around 125 vectors.

At this scale, FAISS `IndexFlatIP` is more than sufficient. However, I wanted
to understand what happens when a vector collection grows to tens or hundreds
of thousands of vectors.

The goal was therefore educational:

- Understand exact nearest-neighbor search
- Understand approximate nearest-neighbor search
- Experiment with FAISS HNSW
- Observe the relationship between latency and recall
- Understand HNSW tuning parameters

---

## IndexFlatIP

`IndexFlatIP` performs exact nearest-neighbor search.

Because the embeddings are L2-normalized, inner-product ranking can be used
for cosine-similarity ranking.

Advantages:

- Exact results
- Simple implementation
- No index training
- Excellent baseline for small datasets

Disadvantage:

- Search cost increases as the number of vectors grows

For the current Study Buddy knowledge base (~125 vectors), this remains a
perfectly reasonable choice.

---

## HNSW

HNSW (Hierarchical Navigable Small World) is an approximate nearest-neighbor
search algorithm.

Instead of exhaustively comparing the query against every vector, HNSW builds
a graph connecting nearby vectors and navigates that graph during search.

Important parameters explored:

### M

Controls graph connectivity.

Higher values generally improve graph quality but require additional memory
and index construction work.

### efConstruction

Controls how thoroughly HNSW searches while constructing the graph.

Higher values can create a better-quality index but increase build time.

### efSearch

Controls how thoroughly the graph is explored during query time.

Higher values generally improve recall but increase search latency.

---

## Scaling Experiment

Synthetic 1024-dimensional normalized vectors were generated to approximate
the dimensionality used by the project's Titan embeddings.

Initial results:

| Vector Count | Flat Search | HNSW Search | HNSW Recall@5 |
|---:|---:|---:|---:|
| 10,000 | 0.126159s | 0.026713s | 76.60% |
| 50,000 | 0.331363s | 0.045616s | 46.20% |
| 100,000 | 0.731429s | 0.042849s | 40.80% |

The experiment demonstrated that HNSW search scaled much better than
exhaustive Flat search, but retrieval recall decreased as the dataset grew
with the same search configuration.

---

## efSearch Experiment

The dataset was fixed at:

- 100,000 vectors
- 1024 dimensions
- 100 queries
- Top K = 5

`IndexFlatIP` was used as the exact-search ground truth.

Results:

| efSearch | Search Time | Recall@5 |
|---:|---:|---:|
| 16 | 0.023344s | 16.00% |
| 32 | 0.041099s | 24.20% |
| 64 | 0.084868s | 38.60% |
| 128 | 0.090585s | 56.80% |
| 256 | 0.156029s | 73.40% |
| 512 | 0.235228s | 83.00% |

Exact Flat search for the same benchmark took:

0.933997 seconds

---

## Key Learning

Increasing `efSearch` caused HNSW to explore more of the graph.

This generally resulted in:

    efSearch increases
            |
            v
    More graph exploration
            |
            +----> Better recall
            |
            +----> Higher search latency

At `efSearch=512`, the experiment achieved 83% Recall@5 while still being
significantly faster than exact Flat search in this synthetic benchmark.

This demonstrates an important vector-search engineering principle:

> Approximate nearest-neighbor search is not simply about making retrieval
> faster. It introduces a tunable trade-off between latency, recall, index
> construction cost, and memory usage.

---

## Important Limitation

These benchmarks use randomly generated synthetic vectors.

Therefore, Recall@5 measures whether HNSW retrieves the same nearest vectors
as exact Flat search.

It does NOT measure whether retrieved chunks are semantically useful for
answering real DevOps questions.

RAG retrieval quality must be evaluated separately using real questions,
knowledge-base chunks, and expected relevant documents.

---

## Current Decision

The Study Buddy's real knowledge base is currently very small.

Therefore:

- `IndexFlatIP` remains an appropriate exact-search baseline.
- HNSW has been implemented as a scaling experiment.
- HNSW should not replace Flat search simply because it performed faster in
  the synthetic benchmark.

The experiment exists primarily to understand how vector retrieval
infrastructure changes as datasets grow.