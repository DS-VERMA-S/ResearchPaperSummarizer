from typing import List

SUMMARY_MAP_PROMPT = (
    "You are an expert scientific writer. Read the following paper segment and write a concise segment summary (5-8 sentences) focusing on: problem, methods, key results, contributions, and limitations. Include inline citations to page numbers using the format [page N] where N is the page number from the provided metadata if the sentence derives from a specific page.\n\n"
    "Segment:\n{segment}\n"
)

SUMMARY_REDUCE_PROMPT = (
    "You are an expert scientific writer. Merge the following segment summaries into a final, cohesive paper summary (180-250 words). Preserve key details on problem, methods, results, contributions, and limitations. Retain inline page citations like [page N] when present.\n\n"
    "Segment Summaries:\n{summaries}\n"
)

EXTRACTION_PROMPT = (
    "You are a research assistant extracting evidence strictly from the provided context."
    " Return a bullet list where each bullet is a single sentence and includes inline page citations like [page N] wherever possible."
    " If information is absent, return an empty list. Do not fabricate.\n\n"
    "Task: {task}\n\n"
    "Context:\n{context}\n\n"
    "Return bullets only."
)

IDEAS_PROMPT = (
    "You are a creative yet rigorous research advisor. Based on the paper summary and gaps/limitations, propose 5-8 new research ideas."
    " Each idea must include: title, rationale, method_outline, novelty_score (1-10), feasibility_score (1-10)."
    " Use JSON array with objects of these fields only. Cite pages in rationale if helpful using [page N].\n\n"
    "Summary:\n{summary}\n\nGaps and Limitations:\n{gaps}\n"
)

FINAL_ASSEMBLY_PROMPT = (
    "You are assembling a final structured report for a research paper."
    " Use the extracted bullets as-is (no fabrication) and the final summary."
    " Produce strict JSON matching the target schema fields.\n\n"
    "Summary:\n{summary}\n\n"
    "New Knowledge and Findings - Empirical Evidence:\n{empirical}\n\n"
    "New Knowledge and Findings - Novel Findings:\n{novel}\n\n"
    "New Knowledge and Findings - Theoretical Contributions:\n{theoretical}\n\n"
    "Deeper Understanding - Contextualization:\n{contextualization}\n\n"
    "Deeper Understanding - Critical Analysis:\n{critical}\n\n"
    "Deeper Understanding - Implications:\n{implications}\n\n"
    "Gaps and Limitations - Knowledge Gaps:\n{gaps}\n\n"
    "Gaps and Limitations - Limitations of Previous Studies:\n{prev_limits}\n\n"
    "Gaps and Limitations - Future Research Directions:\n{future_dirs}\n\n"
    "Practical Applications - Real-world Applications:\n{real_apps}\n\n"
    "Practical Applications - Informing Decision-making:\n{decision}\n\n"
    "Practical Applications - Developing New Technologies:\n{tech}\n\n"
    "Research Ideas (JSON Array):\n{ideas}\n\n"
    "Return strict JSON with the following top-level fields: \n"
    "summary, new_knowledge_and_findings, deeper_understanding_and_interpretation, identification_of_gaps_and_limitations, practical_applications_and_recommendations, research_ideas, citations_note."
)