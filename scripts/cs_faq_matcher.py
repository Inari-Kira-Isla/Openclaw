#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw CS — FAQ 三層匹配器
1. 關鍵字完全匹配  → score 1.0
2. TF-IDF cosine  → score 0.6-0.95
3. 字符 n-gram    → score 0.5-0.8
v1.0 — 2026-03-03
"""

import os
import re
import math
from collections import Counter

# Load .env
_env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(_env_file):
    for _l in open(_env_file):
        _l = _l.strip()
        if _l and not _l.startswith("#") and "=" in _l:
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())


def _tokenize(text):
    """中英文混合分詞：中文字切單字，英文按空格分"""
    text = text.lower().strip()
    tokens = []
    current_en = []
    for ch in text:
        if ch.isascii():
            if ch.isalnum():
                current_en.append(ch)
            else:
                if current_en:
                    tokens.append("".join(current_en))
                    current_en = []
        else:
            if current_en:
                tokens.append("".join(current_en))
                current_en = []
            tokens.append(ch)
    if current_en:
        tokens.append("".join(current_en))
    return tokens


def _ngrams(text, n=2):
    """字符 n-gram set"""
    t = text.lower()
    return set(t[i:i+n] for i in range(len(t)-n+1))


def _cosine(v1, v2):
    """兩個 Counter 的 cosine 相似度"""
    keys = set(v1) | set(v2)
    dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in keys)
    norm1 = math.sqrt(sum(x*x for x in v1.values()))
    norm2 = math.sqrt(sum(x*x for x in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def _keyword_score(query_raw, query_tokens, faq_keywords):
    """關鍵字匹配：在原始 query 中搜尋關鍵字（支援多字片語）"""
    if not faq_keywords:
        return 0.0
    q_lower = query_raw.lower()
    q_set = set(query_tokens)
    hits = sum(1 for kw in faq_keywords
               if kw.lower() in q_lower or kw.lower() in q_set)
    if hits == 0:
        return 0.0
    # Any hit ≥ 0.80; more hits → higher (up to 1.0)
    total = max(1, len(faq_keywords))
    return min(1.0, 0.80 + 0.20 * (hits / total))


def _tfidf_score(query_tokens, question_tokens):
    """簡化 TF-IDF cosine：把 token list 當 bag-of-words"""
    qv = Counter(query_tokens)
    fv = Counter(question_tokens)
    return _cosine(qv, fv)


def _ngram_score(query, question, n=2):
    """bigram Jaccard similarity"""
    q_ng = _ngrams(query, n)
    f_ng = _ngrams(question, n)
    if not q_ng or not f_ng:
        return 0.0
    inter = len(q_ng & f_ng)
    union = len(q_ng | f_ng)
    return inter / union if union > 0 else 0.0


class FAQMatcher:
    """
    使用方式:
        matcher = FAQMatcher()
        result = matcher.match("有優惠嗎", "demo")
        if result:
            answer, score, faq_id = result
    """

    def __init__(self):
        from cs_customer_db import get_faqs, record_faq_hit
        self._get_faqs = get_faqs
        self._record_hit = record_faq_hit
        self._cache = {}   # brand_id → faq list (in-memory cache)

    def _load_faqs(self, brand_id):
        """從 SQLite 載入 FAQ（快取至 session，避免每次查 DB）"""
        if brand_id not in self._cache:
            self._cache[brand_id] = self._get_faqs(brand_id)
        return self._cache[brand_id]

    def invalidate_cache(self, brand_id=None):
        if brand_id:
            self._cache.pop(brand_id, None)
        else:
            self._cache.clear()

    def match(self, query, brand_id, threshold=0.70):
        """
        Returns: (answer, score, faq_id) or None if no match above threshold
        """
        faqs = self._load_faqs(brand_id)
        if not faqs:
            return None

        query_tokens = _tokenize(query)
        best_score = 0.0
        best_faq = None

        for faq in faqs:
            question = faq["question"]
            keywords = faq.get("keywords", [])
            q_tokens = _tokenize(question)

            # Layer 1: keyword match (use original query for multi-char keywords)
            kw_score = _keyword_score(query, query_tokens, keywords)

            # Layer 2: TF-IDF cosine
            tfidf = _tfidf_score(query_tokens, q_tokens)

            # Layer 3: bigram similarity
            ng = _ngram_score(query, question, n=2)

            # Weighted composite score
            score = max(
                kw_score * 1.0,           # keyword hit is high confidence
                tfidf * 0.95,
                ng * 0.80,
            )

            # Bonus if keyword AND tfidf both fire
            if kw_score > 0 and tfidf > 0.3:
                score = min(1.0, score * 1.15)

            if score > best_score:
                best_score = score
                best_faq = faq

        if best_score >= threshold and best_faq:
            self._record_hit(best_faq["id"])
            self.invalidate_cache(brand_id)   # refresh match_count cache
            return best_faq["answer"], round(best_score, 3), best_faq["id"]

        return None


# ─── CLI test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    brand = sys.argv[1] if len(sys.argv) > 1 else "demo"
    matcher = FAQMatcher()

    test_queries = [
        "你們有優惠嗎",
        "怎麼買",
        "運費要多少錢",
        "可以退貨嗎",
        "大概幾天到",
        "你們賣什麼",     # should not match well
    ]

    print(f"\n=== FAQ Matcher Test (brand: {brand}) ===")
    for q in test_queries:
        result = matcher.match(q, brand)
        if result:
            answer, score, fid = result
            print(f"  [{score:.2f}] Q: {q}")
            print(f"         A: {answer[:60]}...")
        else:
            print(f"  [----] Q: {q}  → no match")
