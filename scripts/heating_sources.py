"""Read maintained heating chapters, excluding generated evidence/statistics inputs."""
from pathlib import Path
import re

GENERATED = {'evidence_index', 'batch_stats'}

def report_source(path: Path, seen=None):
    seen = set() if seen is None else seen
    path = path.resolve()
    if path in seen:
        return ''
    seen.add(path)
    source = path.read_text(encoding='utf-8')
    def expand(match):
        name = match[1]
        if name in GENERATED or name.startswith('../'):
            return ''
        return report_source(path.parent / (name + '.tex'), seen)
    # Expand in place so the evidence index follows first citation order.
    return re.sub(r'\\input\{([^}]+)\}', expand, source)
