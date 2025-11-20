from pyscript import when, document
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction

status_el = document.querySelector("#status")
output_el = document.querySelector("#output")
btn = document.querySelector("#run")

# At this point PyScript has already applied pyscript.toml,
# so Biopython is available.
status_el.textContent = "Python + Biopython ready."
btn.disabled = False


def parse_fasta_or_raw(text: str) -> str:
    """Strip FASTA headers and whitespace, return raw sequence."""
    lines = [ln.strip() for ln in text.strip().splitlines()]
    seq_lines = [ln for ln in lines if not ln.startswith(">")]
    seq = "".join(seq_lines).replace(" ", "").upper()
    return seq


def clean_acgt(seq: str) -> str:
    """Keep only A, C, G, T."""
    return "".join(b for b in seq if b in "ACGT")


def analyze_sequence(text: str) -> str:
    raw = parse_fasta_or_raw(text)
    cleaned = clean_acgt(raw)

    seq = Seq(cleaned)

    # GC content using Biopython helper
    gc_pct = gc_fraction(seq) * 100 if len(seq) else 0.0

    rev_comp = str(seq.reverse_complement())
    protein = str(seq.translate(to_stop=True)) if len(seq) >= 3 else ""

    out_lines = []
    out_lines.append(f"Original length (post-header, pre-cleaning): {len(raw)}")
    out_lines.append(f"Cleaned length (ACGT only): {len(cleaned)}")
    out_lines.append(f"GC content (gc_fraction): {gc_pct:.2f} percent")
    out_lines.append("")

    out_lines.append("Reverse complement (first 120 bp):")
    if rev_comp:
        snippet = rev_comp[:120]
        if len(rev_comp) > 120:
            snippet += "..."
        out_lines.append(snippet)
    else:
        out_lines.append("(empty)")

    out_lines.append("")
    out_lines.append("Protein translation (frame 1, stop at first stop codon):")
    out_lines.append(protein if protein else "(no complete ORF / empty)")

    return "\n".join(out_lines)


@when("click", "#run")
def on_run(event) -> None:
    btn.disabled = True
    status_el.textContent = "Running…"

    try:
        seq_text = document.querySelector("#seq").value
        result = analyze_sequence(seq_text)
        output_el.textContent = result
        status_el.textContent = "Done."
    except Exception as e:
        output_el.textContent = "Error during analysis:\n" + repr(e)
        status_el.textContent = "Error."
    finally:
        btn.disabled = False
