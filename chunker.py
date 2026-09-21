"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


# A sentence that opens a new topic. Two patterns cover how these posts are
# written: a short all-lowercase label and a colon ("The good:", "On noise:",
# "Assessment:", "Wait times:"), and the dining posts' "The thing worth going
# for is..." / "The thing to know is...". Proper nouns are left out of the label
# on purpose, or "Fenwick Court to central campus: 18 minutes" would count as one.
_TOPIC_LABEL = re.compile(
    r"^(?:[A-Z][a-z]*(?: [a-z]+){0,4}:\s|The thing (?:worth going for|to know) is\b)"
)
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9$])")


def _split_title(text: str) -> tuple[str, str]:
    """A post's first line is its title if it is short and not a sentence."""
    first, _, rest = text.partition("\n")
    if len(first) < 80 and not re.search(r"[.!?]$", first) and rest.strip():
        return first.strip(), rest.strip()
    return "", text


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks, one topic per chunk.

    Chunking strategy for campus_life (details in README.md):
      - A post of WHOLE_POST_LIMIT characters or fewer stays whole: it is
        already one thought, and cutting it would only lose context.
      - A longer post is cut into sentences and a new chunk starts where a new
        topic starts: at a paragraph break, or at a sentence that opens with a
        label such as "The bad:" or "On noise:".
      - A chunk that runs past MAX_CHUNK_CHARS is cut at a sentence end, and one
        shorter than MIN_CHUNK_CHARS is joined to the next so no chunk is a stub.
      - The post's title is put back at the top of every chunk, so a chunk that
        says "Laundry costs $1.75" still says which building it is about.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        if len(doc.text) <= config.WHOLE_POST_LIMIT:
            pieces = [doc.text]
        else:
            title, body = _split_title(doc.text)
            pieces = []
            current = ""
            for paragraph in re.split(r"\n\s*\n", body):
                sentences = [
                    s.strip()
                    for s in _SENTENCE_END.split(paragraph.replace("\n", " "))
                    if s.strip()
                ]
                for i, sentence in enumerate(sentences):
                    starts_topic = i == 0 or _TOPIC_LABEL.match(sentence)
                    too_long = len(current) + 1 + len(sentence) > config.MAX_CHUNK_CHARS
                    # A short opening line ("I'm a junior and I've done this
                    # twice now.") is preamble, so it waits for the first topic.
                    floor = config.PREAMBLE_CHARS if not pieces else config.MIN_CHUNK_CHARS
                    if current and (starts_topic or too_long) and len(current) >= floor:
                        pieces.append(current)
                        current = ""
                    current = f"{current} {sentence}".strip()
            if current:
                pieces.append(current)
            pieces = [f"{title}\n\n{p}".strip() for p in pieces]

        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
