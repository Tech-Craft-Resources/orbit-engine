#!/usr/bin/env python3
"""
Add captions to every Pandoc-generated longtable so they appear in \\listoftables.

Pandoc wraps captionless tables in:
    {\\def\\LTcaptype{none} % do not increment counter
    \\begin{longtable}[]{...col specs (1 or more lines, ending with @{}})...
    \\toprule\\noalign{}
    ...
    \\end{longtable}
    }

For tables WITHOUT that wrapper, we still want a caption.

Strategy (rewritten with simpler line-based state machine):
  Pass 1 — identify longtable blocks and their wrappers; collect (start, end,
           wrapper_open_idx_or_None, wrapper_close_idx_or_None) and
           col_spec_end_idx.
  Pass 2 — for each block, derive a caption from:
             (a) preceding "\\textbf{Tabla X.Y.Z.} ...." (and remove that line)
             (b) nearest preceding heading
           then mutate the lines list: remove wrapper lines, remove tabla-label
           line, insert \\caption right after col_spec_end_idx.

We apply mutations in REVERSE order so indices don't shift.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

FILES = [
    "Orbit_Engine/MainMatter/Cap2/C2-MarcoReferencia.tex",
    "Orbit_Engine/MainMatter/Cap3/C3-AnalisisDiseno.tex",
    "Orbit_Engine/MainMatter/Cap4/C4-Desarrollo.tex",
    "Orbit_Engine/MainMatter/Cap5/C5-ResultadosTecnicos.tex",
    "Orbit_Engine/MainMatter/Cap6/C6-ResultadosUsuarios.tex",
    "Orbit_Engine/MainMatter/Cap7/C7-Conclusiones.tex",
    "Orbit_Engine/BackMatter/AnexoA-ManualUsuario.tex",
    "Orbit_Engine/BackMatter/AnexoB-Despliegue.tex",
    "Orbit_Engine/BackMatter/AnexoC-DocTecnica.tex",
]

HEADING_START_RE = re.compile(
    r"^\\(section|subsection|subsubsection|paragraph)\*?\{"
)


def extract_balanced(text: str, start: int) -> tuple[str, int]:
    """Given text and position of `{`, return (inner, idx_after_close)."""
    assert text[start] == "{"
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
        i += 1
    raise ValueError("unbalanced braces")


def parse_heading(line: str) -> str | None:
    m = HEADING_START_RE.match(line)
    if not m:
        return None
    inner, _ = extract_balanced(line, m.end() - 1)
    return inner


TEXORPDF_RE = re.compile(r"\\texorpdfstring")


def unwrap_texorpdfstring(text: str) -> str:
    """Replace `\\texorpdfstring{display}{pdf}` with just `pdf` (no markup)."""
    out = []
    i = 0
    while i < len(text):
        if text.startswith("\\texorpdfstring{", i):
            j = i + len("\\texorpdfstring")
            _disp, j = extract_balanced(text, j)
            pdf_form, j = extract_balanced(text, j)
            out.append(pdf_form)
            i = j
        else:
            out.append(text[i])
            i += 1
    return "".join(out)
TABLA_LABEL_RE = re.compile(r"^\\textbf\{Tabla\s+[\dA-Za-z.]+\.?\}\s*(.*?)\s*$")
WRAPPER_OPEN = "{\\def\\LTcaptype{none}"


def strip_latex_for_short(text: str) -> str:
    s = text
    for cmd in ("textbf", "emph", "texttt", "textit", "textsc"):
        s = re.sub(r"\\" + cmd + r"\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    m = re.match(r"^(.{1,120}?[.!?])(\s|$)", s)
    if m:
        s = m.group(1)
    elif len(s) > 120:
        s = s[:117].rstrip() + "..."
    return s.rstrip(".")


def derive_heading_caption(heading_text: str) -> str:
    s = heading_text
    s = unwrap_texorpdfstring(s)
    s = re.sub(r"\\label\{[^}]*\}", "", s).strip()
    s = re.sub(r"^[A-Z]{2,5}-[A-Z]{2,5}\.\s*", "", s)
    return s.strip()


def find_blocks(lines: list[str]) -> list[dict]:
    """Return list of blocks: {start, end, wrap_open, wrap_close, colspec_end}."""
    blocks: list[dict] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.lstrip().startswith("\\begin{longtable}"):
            start = i
            wrap_open = None
            # Check previous non-empty line for wrapper-open
            k = i - 1
            while k >= 0 and lines[k].strip() == "":
                k -= 1
            if k >= 0 and lines[k].startswith(WRAPPER_OPEN):
                wrap_open = k
            # Find column spec end (line ending with `@{}}`)
            # The begin line itself may already end with `@{}}`.
            colspec_end = i
            if not lines[i].rstrip().endswith("@{}}"):
                j = i + 1
                while j < n:
                    if lines[j].rstrip().endswith("@{}}"):
                        colspec_end = j
                        break
                    j += 1
                else:
                    raise RuntimeError(f"longtable at {i} has no column spec end")
            # Find \end{longtable}
            j = colspec_end + 1
            end = None
            while j < n:
                if lines[j].strip() == "\\end{longtable}":
                    end = j
                    break
                j += 1
            if end is None:
                raise RuntimeError(f"longtable at {i} has no \\end{{longtable}}")
            # Check next non-empty line for wrapper-close `}`
            wrap_close = None
            if wrap_open is not None:
                k = end + 1
                while k < n and lines[k].strip() == "":
                    k += 1
                if k < n and lines[k].strip() == "}":
                    wrap_close = k
            blocks.append(
                {
                    "start": start,
                    "end": end,
                    "wrap_open": wrap_open,
                    "wrap_close": wrap_close,
                    "colspec_end": colspec_end,
                }
            )
            i = end + 1
        else:
            i += 1
    return blocks


def find_tabla_label(lines: list[str], anchor: int) -> tuple[int | None, str | None]:
    """Look back from `anchor` for a `\\textbf{Tabla X.Y.Z.} ...` paragraph.
    Returns (line_index, title) or (None, None)."""
    k = anchor - 1
    skipped_blank = 0
    while k >= 0 and skipped_blank < 3:
        s = lines[k].strip()
        if s == "":
            skipped_blank += 1
            k -= 1
            continue
        m = TABLA_LABEL_RE.match(s)
        if m:
            return k, m.group(1)
        return None, None
    return None, None


def has_existing_caption(lines: list[str], start: int, end: int) -> bool:
    for j in range(start, end + 1):
        if lines[j].lstrip().startswith("\\caption"):
            return True
    return False


def process(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    blocks = find_blocks(lines)

    # Build heading map: for each line index, what's the most recent heading text.
    headings: list[tuple[int, str]] = []  # (line_idx, heading_text)
    for idx, line in enumerate(lines):
        inner = parse_heading(line)
        if inner is not None:
            headings.append((idx, derive_heading_caption(inner)))

    def heading_at(idx: int) -> str:
        cur = ""
        for h_idx, h_text in headings:
            if h_idx < idx:
                cur = h_text
            else:
                break
        return cur or "Tabla"

    # First pass: derive captions per block (with dedupe counter per heading).
    captions: list[tuple[dict, str, int | None]] = []  # (block, caption, tabla_label_line)
    heading_count: dict[str, int] = {}
    for b in blocks:
        if has_existing_caption(lines, b["start"], b["end"]):
            captions.append((b, "", None))
            continue
        anchor = b["wrap_open"] if b["wrap_open"] is not None else b["start"]
        label_idx, label_text = find_tabla_label(lines, anchor)
        if label_text:
            caption = label_text.rstrip(".")
        else:
            base = heading_at(b["start"])
            heading_count[base] = heading_count.get(base, 0) + 1
            caption = base if heading_count[base] == 1 else f"{base} (parte {heading_count[base]})"
        captions.append((b, caption, label_idx))

    # Apply mutations in REVERSE so indices stay valid.
    # For each block: insert caption after colspec_end, remove wrap_open,
    # wrap_close, and tabla_label line.
    n_captioned = 0
    # Iterate blocks in reverse
    for b, caption, label_idx in reversed(captions):
        if not caption:
            continue  # already had caption
        short = strip_latex_for_short(caption)
        cap_line = f"\\caption[{short}]{{{caption}}}\\tabularnewline"

        # Collect indices to delete in descending order, AFTER insert position.
        # Insert AFTER colspec_end.
        insert_at = b["colspec_end"] + 1
        # Insertion comes before deletions in the working order.
        lines.insert(insert_at, cap_line)
        # All subsequent indices shift by +1 if they are >= insert_at.

        def shift(idx: int | None) -> int | None:
            if idx is None:
                return None
            return idx + 1 if idx >= insert_at else idx

        del_indices = sorted(
            [d for d in (shift(b["wrap_close"]), shift(b["wrap_open"]), shift(label_idx)) if d is not None],
            reverse=True,
        )
        for di in del_indices:
            del lines[di]
        n_captioned += 1

    new_text = "\n".join(lines)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return n_captioned


def main():
    root = Path(__file__).parent
    total = 0
    for rel in FILES:
        p = root / rel
        if not p.exists():
            print(f"skip {rel} (missing)")
            continue
        n = process(p)
        print(f"{rel}: {n} tablas captionadas")
        total += n
    print(f"Total: {total}")


if __name__ == "__main__":
    main()
