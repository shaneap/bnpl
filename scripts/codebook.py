"""Parse a SHED codebook PDF (Stata codebook layout) into variable blocks.

Each block: name, label (question wording as printed), type, missing count, and the
tabulation of codes -> labels with unweighted frequencies. Used for Phase 1 checks only.
"""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pypdf import PdfReader

HEADER = re.compile(r"^(\[?[A-Za-z][\w\]\[]*)\s+(\S.*)$")
MISSING = re.compile(r"missing\s+\.:\s+([\d,]+)/([\d,]+)", re.I)
TAB_ROW = re.compile(r"^\s*([\d,]+)\s+(-?[\d.]+|\.)\s*(.*)$")


@dataclass
class Var:
    name: str
    label: str
    page: int
    missing: int | None = None
    total: int | None = None
    codes: list = field(default_factory=list)  # (freq, code, label)
    body: str = ""

    @property
    def nonmissing(self):
        return None if self.missing is None else self.total - self.missing


def is_rule(line: str) -> bool:
    """Horizontal rule of dashes, sometimes broken by spaces in the PDF text."""
    return line.count("-") >= 40 and not line.replace("-", "").strip()


def pdf_lines(path: Path):
    for i, page in enumerate(PdfReader(path).pages, 1):
        for line in (page.extract_text(extraction_mode="layout") or "").splitlines():
            yield i, line.expandtabs()


def norm(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip()


def parse(path: Path) -> dict[str, Var]:
    return parse_lines(list(pdf_lines(path)))


def parse_lines(lines: list[tuple[int, str]]) -> dict[str, Var]:
    """Parse (page, line) pairs into variable blocks."""
    out: dict[str, Var] = {}
    i = 0
    while i < len(lines):
        page, line = lines[i]
        # Block header: rule, "NAME   label...", label continuation lines, rule
        if is_rule(line) and i + 1 < len(lines) and (m := HEADER.match(lines[i + 1][1])) and not is_rule(lines[i + 1][1]):
            j = i + 2
            label = [m.group(2)]
            while j < len(lines) and not is_rule(lines[j][1]):
                label.append(lines[j][1])
                j += 1
            if j < len(lines) and "type:" in "".join(l for _, l in lines[j + 1 : j + 4]).lower():
                k = j + 1
                body = []
                while k < len(lines) and not is_rule(lines[k][1]):
                    if not lines[k][1].startswith("====="):
                        body.append(lines[k][1])
                    k += 1
                v = Var(m.group(1), norm(" ".join(label)), page, body="\n".join(body))
                text = " ".join(body)
                if mm := MISSING.search(text):
                    v.missing = int(mm.group(1).replace(",", ""))
                    v.total = int(mm.group(2).replace(",", ""))
                v.codes = parse_tab(body)
                out[v.name] = v
                i = k
                continue
        i += 1
    return out


def parse_tab(body: list[str]):
    rows, in_tab = [], False
    for line in body:
        if "tabulation:" in line.lower():
            in_tab = True
            continue
        if not in_tab or not line.strip():
            continue
        if m := TAB_ROW.match(line):
            rows.append([int(m.group(1).replace(",", "")), m.group(2), norm(m.group(3))])
        elif rows:  # wrapped label continuation
            rows[-1][2] = norm(rows[-1][2] + " " + line)
    return rows


if __name__ == "__main__":
    vars_ = parse(Path(sys.argv[1]))
    pat = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
    for v in vars_.values():
        if pat is None or pat.search(v.name):
            print(f"{v.name} [p{v.page}] n={v.nonmissing}/{v.total}\n  {v.label}")
            for f, c, l in v.codes:
                print(f"    {c:>4} {l}  ({f:,})")
