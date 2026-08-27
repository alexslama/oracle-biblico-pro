# Corpus guide

SHAMIR is source-aware only when the corpus is trustworthy, traceable, and legally usable. Corpus quality is therefore part of the system design, not an afterthought.

## JSONL schema

Each line should be one JSON object:

```json
{
  "text": "Passage or reference note to index.",
  "metadata": {
    "title": "Human-readable source title",
    "author": "Author or institution",
    "source": "Canonical URL, DOI, catalog identifier, or local provenance note",
    "license": "License or public-domain status",
    "language": "en",
    "date": "2026-01-01",
    "topic": "example"
  }
}
```

Only `text` is required by the loader, but production-quality corpora should include enough metadata to audit provenance.

## Recommended provenance fields

Where available, record:

- `title`
- `author`
- `publisher` or `institution`
- `source` (URL, DOI, ISBN, archive identifier, etc.)
- `license`
- `date`
- `language`
- `edition`
- `page`, `chapter`, or other locator
- `topic`
- `notes`

## Licensing rule

Do not commit a corpus merely because it is accessible online. Before redistribution, confirm that the material is:

- public domain; or
- under a license that permits redistribution in this repository; or
- authored specifically for SHAMIR; or
- excluded from the repository and loaded locally by the user under their own lawful access.

When rights are unclear, keep only metadata/instructions and require users to provide the source locally.

## Source quality

A corpus can be legally distributable and still be poor evidence. Document whether a source is:

- primary text;
- scholarly edition;
- peer-reviewed research;
- academic reference work;
- historical source;
- commentary or confessional interpretation;
- community-authored note;
- synthetic/demo material.

SHAMIR's included `data/demo_corpus.jsonl` is intentionally marked as demo material and must not be represented as a scholarly corpus.

## Reproducibility

For published benchmarks, record:

- corpus file hash or release tag;
- number of indexed documents;
- chunking rules if used;
- embedding model and version;
- collection name;
- vector-store configuration.

These details make retrieval experiments comparable instead of anecdotal.
