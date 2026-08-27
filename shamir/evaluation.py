"""Deterministic evaluation helpers for source-citation integrity.

These checks do not claim semantic truth or full groundedness. They verify a
smaller, auditable property: generated sections may cite only source labels that
were actually retrieved for the request, and source-use statistics are exposed
for downstream benchmarking.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Set

CITATION_RE = re.compile(r"\[(S\d+)\]")


def _generated_sections(result: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for layer in result.get("analysis_layers") or []:
        if layer.get("status") == "generated":
            yield {"name": str(layer.get("name") or "layer"), "content": str(layer.get("content") or "")}

    synthesis = result.get("synthesis") or {}
    if synthesis.get("status") == "generated":
        yield {"name": "synthesis", "content": str(synthesis.get("content") or "")}


def evaluate_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate citation-label integrity for one SHAMIR result.

    The returned metrics intentionally avoid claiming that a citation proves a
    sentence. They only establish whether labels are valid and whether generated
    sections cite retrieved sources at all.
    """
    valid_labels: Set[str] = {
        str(source.get("label"))
        for source in (result.get("sources") or [])
        if source.get("label")
    }

    all_citations: List[str] = []
    invalid_citations: Set[str] = set()
    cited_valid_labels: Set[str] = set()
    generated_without_citations: List[str] = []
    sections: List[Dict[str, Any]] = []

    for section in _generated_sections(result):
        citations = CITATION_RE.findall(section["content"])
        all_citations.extend(citations)
        section_invalid = sorted({label for label in citations if label not in valid_labels})
        invalid_citations.update(section_invalid)
        section_valid = sorted({label for label in citations if label in valid_labels})
        cited_valid_labels.update(section_valid)
        if valid_labels and not citations:
            generated_without_citations.append(section["name"])
        sections.append(
            {
                "name": section["name"],
                "citations": citations,
                "valid_citations": section_valid,
                "invalid_citations": section_invalid,
            }
        )

    total_citations = len(all_citations)
    valid_citation_occurrences = sum(1 for label in all_citations if label in valid_labels)
    citation_validity = (
        valid_citation_occurrences / total_citations if total_citations else None
    )
    source_coverage = (
        len(cited_valid_labels) / len(valid_labels) if valid_labels else None
    )

    return {
        "scope": "citation_label_integrity",
        "valid_source_labels": sorted(valid_labels),
        "citation_count": total_citations,
        "invalid_citations": sorted(invalid_citations),
        "generated_sections_without_citations": generated_without_citations,
        "citation_validity": citation_validity,
        "source_coverage": source_coverage,
        "sections": sections,
        "passed": not invalid_citations and not generated_without_citations,
        "note": (
            "This evaluator validates citation-label integrity only; it does not prove "
            "that cited text semantically supports each generated claim."
        ),
    }
