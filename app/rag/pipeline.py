from __future__ import annotations

import json
from typing import Dict, List

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config import RETRIEVAL_K
from app.rag.prompts import (
    SUMMARY_MAP_PROMPT,
    SUMMARY_REDUCE_PROMPT,
    EXTRACTION_PROMPT,
    IDEAS_PROMPT,
    FINAL_ASSEMBLY_PROMPT,
)
from app.rag.utils import (
    load_pdf_documents,
    split_documents,
    build_local_index_from_docs,
    get_llm,
    join_context_with_citations,
)


class RagAnalyzer:
    def ingest(self, pdf_path: str) -> Dict[str, str]:
        # Kept for API parity; returns a pseudo ID without persistence
        return {"paper_id": "in-memory", "store_path": "in-memory"}

    def _map_summaries(self, chunks: List, llm) -> List[str]:
        prompt = ChatPromptTemplate.from_template(SUMMARY_MAP_PROMPT)
        chain = prompt | llm | StrOutputParser()
        summaries: List[str] = []
        for ch in chunks:
            text = ch.page_content
            page = ch.metadata.get("page")
            segment = f"{text}\n\n[page {page}]" if page is not None else text
            s = chain.invoke({"segment": segment})
            summaries.append(s)
        return summaries

    def _reduce_summary(self, summaries: List[str], llm) -> str:
        prompt = ChatPromptTemplate.from_template(SUMMARY_REDUCE_PROMPT)
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"summaries": "\n\n".join(summaries)})

    def _extract(self, retriever, llm, task: str) -> List[str]:
        docs = retriever.get_relevant_documents(task)
        context = join_context_with_citations(docs)
        prompt = ChatPromptTemplate.from_template(EXTRACTION_PROMPT)
        chain = prompt | llm | StrOutputParser()
        raw = chain.invoke({"task": task, "context": context})
        lines = [ln.strip(" -\t") for ln in raw.strip().splitlines() if ln.strip()]
        return [ln for ln in lines if ln]

    def _ideas(self, llm, summary: str, gaps: List[str]) -> List[dict]:
        prompt = ChatPromptTemplate.from_template(IDEAS_PROMPT)
        chain = prompt | llm | StrOutputParser()
        raw = chain.invoke({"summary": summary, "gaps": "\n".join(gaps)})
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return data
        except Exception:
            pass
        return []

    def analyze(self, pdf_path: str) -> Dict:
        docs = load_pdf_documents(pdf_path)
        chunks = split_documents(docs)
        index = build_local_index_from_docs(chunks)
        retriever = index.as_retriever(k=RETRIEVAL_K)
        llm = get_llm(temperature=0.2)

        summaries = self._map_summaries(chunks, llm)
        final_summary = self._reduce_summary(summaries, llm)

        empirical = self._extract(
            retriever,
            llm,
            task=(
                "Identify empirical evidence: experiments, datasets, sample sizes, variables, evaluation metrics, and data collection methods."
            ),
        )
        novel = self._extract(
            retriever,
            llm,
            task=(
                "Identify novel findings: unexpected results, new patterns, relationships, or performance improvements, and where they appear in the paper."
            ),
        )
        theoretical = self._extract(
            retriever,
            llm,
            task=(
                "Identify theoretical contributions: new theories, models, or refinements to existing ones, including assumptions and scope."
            ),
        )
        contextualization = self._extract(
            retriever,
            llm,
            task=(
                "Explain how the paper situates itself within prior literature (Related Work, Introduction, Discussion), including agreements or challenges to prior work."
            ),
        )
        critical = self._extract(
            retriever,
            llm,
            task=(
                "Critically evaluate the study's methodology and analysis as discussed by the authors; note potential sources of bias or threats to validity."
            ),
        )
        implications = self._extract(
            retriever,
            llm,
            task=(
                "List practical or theoretical implications of the findings as stated by the authors, including recommended applications."
            ),
        )
        gaps = self._extract(
            retriever,
            llm,
            task=(
                "Identify knowledge gaps highlighted by the paper where understanding remains limited or unclear."
            ),
        )
        prev_limits = self._extract(
            retriever,
            llm,
            task=(
                "Identify limitations of previous studies as described by the authors, including methodological flaws or constraints."
            ),
        )
        future_dirs = self._extract(
            retriever,
            llm,
            task=(
                "List future research directions proposed by the authors to address limitations or extend findings."
            ),
        )
        real_apps = self._extract(
            retriever,
            llm,
            task=(
                "Identify real-world applications suggested by the paper, including target domains and stakeholders."
            ),
        )
        decision = self._extract(
            retriever,
            llm,
            task=(
                "Explain how findings can inform decision-making in relevant fields (e.g., policy, healthcare, education, business)."
            ),
        )
        tech = self._extract(
            retriever,
            llm,
            task=(
                "Identify potential new technologies or innovations enabled by the paper's insights."
            ),
        )

        ideas = self._ideas(llm, final_summary, gaps)

        assembly_prompt = ChatPromptTemplate.from_template(FINAL_ASSEMBLY_PROMPT)
        assembly_chain = assembly_prompt | llm | StrOutputParser()
        assembled = assembly_chain.invoke(
            {
                "summary": final_summary,
                "empirical": "\n".join(empirical),
                "novel": "\n".join(novel),
                "theoretical": "\n".join(theoretical),
                "contextualization": "\n".join(contextualization),
                "critical": "\n".join(critical),
                "implications": "\n".join(implications),
                "gaps": "\n".join(gaps),
                "prev_limits": "\n".join(prev_limits),
                "future_dirs": "\n".join(future_dirs),
                "real_apps": "\n".join(real_apps),
                "decision": "\n".join(decision),
                "tech": "\n".join(tech),
                "ideas": json.dumps(ideas, ensure_ascii=False),
            }
        )

        try:
            result = json.loads(assembled)
        except Exception:
            result = {
                "summary": final_summary,
                "new_knowledge_and_findings": {
                    "empirical_evidence": {"items": empirical},
                    "novel_findings": {"items": novel},
                    "theoretical_contributions": {"items": theoretical},
                },
                "deeper_understanding_and_interpretation": {
                    "contextualization": {"items": contextualization},
                    "critical_analysis": {"items": critical},
                    "implications": {"items": implications},
                },
                "identification_of_gaps_and_limitations": {
                    "knowledge_gaps": {"items": gaps},
                    "limitations_of_previous_studies": {"items": prev_limits},
                    "future_research_directions": {"items": future_dirs},
                },
                "practical_applications_and_recommendations": {
                    "real_world_applications": {"items": real_apps},
                    "informing_decision_making": {"items": decision},
                    "developing_new_technologies": {"items": tech},
                },
                "research_ideas": ideas,
                "citations_note": "Inline citations reference [page N] from the PDF where applicable.",
            }

        return result