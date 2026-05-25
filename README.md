🎯 Semantic Recommender

A semantic recommendation engine built with vector embeddings + pgvector + feedback loop. Designed as a reusable backend for content platforms, e-commerce, and any product that has outgrown rule-based filters.

Instead of relying on keyword matching or hand-crafted rules, the system represents items as high-dimensional vectors and serves recommendations based on semantic similarity. A feedback signal (clicks, ratings, dwell time) feeds back into the ranking, so results improve as users interact with the system.



✨ Features





Vector-based retrieval — items and queries embedded into the same semantic space



PostgreSQL + pgvector — production-ready, scalable storage for embeddings



Feedback loop — user signals re-weight future recommendations



Reusable backend — content-agnostic, can be plugged into any catalog (products, articles, jobs, etc.)



Fast inference — top-k similarity search returns in milliseconds, even with hundreds of thousands of items



🛠 Tech Stack







Layer



Technology





Language



Python





Embeddings



Sentence-transformers / OpenAI





Vector DB



PostgreSQL + pgvector





Retrieval



Cosine similarity, top-k





Feedback storage



PostgreSQL



🚀 Quick Start

Local Development

# 1. Clone the repo
git clone https://github.com/pcbeingused333/semantic-recommender.git
cd semantic-recommender

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your database URL and embedding API key

# 5. Start PostgreSQL with pgvector
# (Docker is the easiest way — see docker-compose.yml)

# 6. Ingest your catalog
python ingest.py

# 7. Run the API
python app.py



🏗 Architecture

┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Catalog   │────▶│  Embeddings  │────▶│ pgvector storage │
└─────────────┘     └──────────────┘     └────────┬─────────┘
                                                  │
┌─────────────┐     ┌──────────────┐              │
│ User query  │────▶│  Embeddings  │──────────────┤
└─────────────┘     └──────────────┘              │
                                                  ▼
                                        ┌──────────────────┐
                                        │  Top-K retrieval │
                                        │   + reranking    │
                                        └────────┬─────────┘
                                                 │
                                                 ▼
                                       ┌────────────────────┐
                                       │ Feedback collector │
                                       │ (clicks, ratings)  │
                                       └────────────────────┘





Ingestion: catalog items are embedded once and stored as vectors



Retrieval: incoming queries are embedded on-the-fly, then nearest neighbors are returned



Feedback loop: user interactions are logged and used to re-weight item scores over time



📦 Use Cases

This backend was built to be domain-agnostic. Examples of where it fits:





Content platforms — "show me articles similar to this one"



E-commerce — "you might also like" beyond category filtering



Job boards — match candidates to listings beyond keyword overlap



Internal tools — semantic search across an internal knowledge base



🔮 Future Improvements





Hybrid retrieval (vector + BM25 keyword search)



Reranking with a cross-encoder for higher precision



A/B testing harness for ranking strategies



Cold-start handling for brand-new items



REST + GraphQL endpoints



📄 License

MIT License — free to use, modify and adapt.
