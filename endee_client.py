"""
Endee Vector Database Client
Handles: index creation, vector upsert, semantic search
"""

import os
import math
import hashlib
from typing import Optional

# Simple text embedding using TF-IDF-like approach (no external ML deps needed)
# For production: replace with sentence-transformers or OpenAI embeddings
VOCAB = [
    "hospital", "clinic", "doctor", "medical", "emergency", "health", "surgery", "icu",
    "police", "station", "crime", "law", "security", "officer", "patrol", "safety",
    "fire", "brigade", "rescue", "firefighter", "hazmat", "burning", "smoke",
    "blood", "bank", "donation", "transfusion", "plasma", "donor", "type",
    "ambulance", "paramedic", "transport", "urgent", "critical", "injury", "trauma",
    "shelter", "disaster", "flood", "relief", "refugee", "temporary", "housing",
    "nearest", "closest", "near", "help", "find", "locate", "need", "where",
    "open", "available", "24", "hour", "night", "day", "service", "contact"
]
DIMENSION = len(VOCAB)  # 48-dimensional embeddings


def text_to_vector(text: str) -> list[float]:
    """Convert text to a simple keyword-frequency vector (48-dim)."""
    text_lower = text.lower()
    vec = []
    for word in VOCAB:
        # Term frequency with partial match
        count = text_lower.count(word)
        vec.append(float(count))

    # L2 normalize
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


class EndeeClient:
    def __init__(self):
        self.base_url = os.getenv("ENDEE_URL", "http://localhost:8080/api/v1")
        self.auth_token = os.getenv("ENDEE_AUTH_TOKEN", "")
        self.index_name = "emergency_resources"
        self._initialized = False

        # Try to import official Endee Python SDK
        try:
            from endee import Endee, Precision
            token = self.auth_token if self.auth_token else None
            self._client = Endee(token)
            if self.base_url != "http://localhost:8080/api/v1":
                self._client.set_base_url(self.base_url)
            self._use_sdk = True
            print("✅ Using official Endee Python SDK")
        except ImportError:
            self._client = None
            self._use_sdk = False
            print("⚠️  Endee SDK not found — using HTTP fallback mode")
        except Exception as e:
            self._client = None
            self._use_sdk = False
            print(f"⚠️  Endee connection failed ({e}) — using in-memory fallback")

        # In-memory fallback store
        self._store: list[dict] = []

    async def initialize(self):
        """Create the Endee index if it doesn't exist."""
        if self._use_sdk:
            try:
                from endee import Precision
                # Check if index already exists
                indexes = self._client.list_indexes()
                names = [idx.get("name", "") for idx in (indexes or [])]
                if self.index_name not in names:
                    self._client.create_index(
                        name=self.index_name,
                        dimension=DIMENSION,
                        space_type="cosine",
                        precision=Precision.INT8
                    )
                    print(f"✅ Created Endee index: '{self.index_name}' (dim={DIMENSION})")
                else:
                    print(f"✅ Endee index '{self.index_name}' already exists")
                self._index = self._client.get_index(name=self.index_name)
            except Exception as e:
                print(f"⚠️  Could not create Endee index: {e} — falling back to in-memory")
                self._use_sdk = False
        else:
            print("📦 Using in-memory vector store (Endee fallback)")
        self._initialized = True

    async def seed_resources(self, resources: list[dict]):
        """Embed and upsert all emergency resources into Endee."""
        if not resources:
            return

        vectors = []
        for r in resources:
            # Create rich text description for embedding
            text = f"{r['name']} {r['type']} {r['address']} {r.get('description', '')}"
            vec = text_to_vector(text)
            vectors.append({
                "id": r["id"],
                "vector": vec,
                "meta": {
                    "name": r["name"],
                    "type": r["type"],
                    "address": r["address"],
                    "phone": r["phone"],
                    "distance_km": r["distance_km"],
                    "is_open": r["is_open"],
                    "icon": r["icon"],
                    "description": r.get("description", ""),
                }
            })

        if self._use_sdk and hasattr(self, '_index'):
            try:
                self._index.upsert(vectors)
                print(f"✅ Seeded {len(vectors)} resources into Endee")
                return
            except Exception as e:
                print(f"⚠️  Endee upsert failed: {e}")

        # Fallback: store in memory
        self._store = vectors
        print(f"📦 Stored {len(vectors)} resources in-memory")

    async def search(
        self,
        query: str,
        top_k: int = 5,
        resource_type: Optional[str] = None
    ) -> list[dict]:
        """Semantic search using Endee vector similarity."""
        query_vec = text_to_vector(query)

        if self._use_sdk and hasattr(self, '_index'):
            try:
                results = self._index.query(vector=query_vec, top_k=top_k * 2)
                return self._format_results(results, resource_type, top_k)
            except Exception as e:
                print(f"⚠️  Endee query failed: {e} — using fallback")

        # Fallback: cosine similarity in memory
        return self._fallback_search(query_vec, top_k, resource_type)

    def _format_results(self, raw_results, resource_type, top_k):
        """Format Endee SDK results into our response model."""
        out = []
        for r in raw_results:
            meta = r.get("meta", {})
            if resource_type and meta.get("type") != resource_type:
                continue
            out.append({
                "id": r.get("id"),
                "name": meta.get("name", ""),
                "type": meta.get("type", ""),
                "address": meta.get("address", ""),
                "phone": meta.get("phone", ""),
                "distance_km": meta.get("distance_km", 0),
                "is_open": meta.get("is_open", True),
                "similarity_score": round(r.get("similarity", 0), 4),
                "icon": meta.get("icon", "🏥"),
            })
            if len(out) >= top_k:
                break
        return out

    def _fallback_search(self, query_vec, top_k, resource_type):
        """In-memory cosine similarity search."""
        scored = []
        for item in self._store:
            meta = item["meta"]
            if resource_type and meta.get("type") != resource_type:
                continue
            score = self._cosine(query_vec, item["vector"])
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        out = []
        for score, item in scored[:top_k]:
            meta = item["meta"]
            out.append({
                "id": item["id"],
                "name": meta["name"],
                "type": meta["type"],
                "address": meta["address"],
                "phone": meta["phone"],
                "distance_km": meta["distance_km"],
                "is_open": meta["is_open"],
                "similarity_score": round(score, 4),
                "icon": meta["icon"],
            })
        return out

    def _cosine(self, a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)) or 1.0
        nb = math.sqrt(sum(x * x for x in b)) or 1.0
        return dot / (na * nb)

    async def get_stats(self):
        return {
            "index": self.index_name,
            "dimension": DIMENSION,
            "total_vectors": len(self._store) if not self._use_sdk else "see_endee_dashboard",
            "endee_url": self.base_url,
            "sdk_connected": self._use_sdk,
            "space_type": "cosine",
        }