#!/usr/bin/env python3
"""Non-mutating Markdown/metadata format check for Academy content.

Not a technical/pedagogical review, a web renderer, a publication gate, or
an exhaustive Mermaid parser. Lesson/assessment structure remains checked by
scripts/validate_content.py.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
PARSER = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
FRONT = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
MATH_BLOCK = re.compile(r"(?m)^\s{0,3}\$\$\s*$")
UNSAFE_LINK = re.compile(r"\]\(\s*[<]?(?:javascript|vbscript|data):", re.I)
MERMAID_START = re.compile(r"^(?:flowchart|graph|sequenceDiagram|classDiagram|stateDiagram(?:-v2)?|erDiagram|gantt|pie|gitGraph|journey|mindmap|timeline|quadrantChart|requirementDiagram|C4Context|C4Container|C4Component|C4Dynamic|C4Deployment|sankey-beta|xychart-beta|block-beta)\b")


class UniqueKeyLoader(yaml.SafeLoader):
    """Prevent silent YAML overwrites without imposing new fields."""


def _unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode) -> dict:
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in result:
            raise yaml.constructor.ConstructorError(None, None, f"duplicate YAML key {key!r}", key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def split_front_matter(text: str) -> tuple[dict, str, int]:
    """Return metadata, Markdown body and 1-based body start line."""
    found = FRONT.match(text)
    if not found:
        raise ValueError("missing or malformed YAML front matter")
    try:
        metadata = yaml.load(found.group(1), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"malformed YAML front matter: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError("YAML front matter must be a mapping")
    return metadata, text[found.end():], text.count("\n", 0, found.end()) + 1


def _kind(path: Path) -> str:
    parts = path.parts
    if "lessons" in parts:
        return "lesson"
    if "assessments" in parts:
        return "assessment"
    if "integrated" in parts:
        return "integrated"
    raise ValueError(f"cannot infer artifact kind from {path}")


def _fence_closed(token, lines: list[str]) -> bool:
    """Compare parser token span with normalized content line count.

    Lists and blockquotes can indent a valid closing fence more than three
    physical spaces. The parser already removes container indentation from
    token.content, and excludes a valid closing line from that content.
    """
    if not token.map:
        return False
    expected = token.content.count("\n") + 2
    return token.map[1] - token.map[0] == expected


def _link_errors(target: str, source: Path, root: Path, check_files: bool, image: bool) -> list[str]:
    errors = []
    if not target or target.startswith("//"):
        return ["empty or scheme-relative URL"]
    try:
        u = urlsplit(target)
    except ValueError:
        return [f"invalid URL: {target}"]
    if u.scheme:
        if u.scheme not in {"https", "http", "mailto"} or (u.scheme in {"http", "https"} and not u.netloc):
            errors.append(f"unsafe or unsupported URL scheme: {target}")
        if image and u.scheme == "mailto":
            errors.append(f"image must not use mailto URL: {target}")
        return errors
    if u.netloc or u.path.startswith("/"):
        return [f"absolute or scheme-relative repository path: {target}"]
    decoded = unquote(u.path)
    if not decoded:
        if image:
            errors.append("image requires a source path")
        return errors
    if "\\" in decoded or "\x00" in decoded:
        return [f"invalid repository path: {target}"]
    root = root.resolve()
    resolved = (source.parent / decoded).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return [f"relative path escapes repository: {target}"]
    if check_files and not resolved.is_file():
        errors.append(f"missing local {'asset' if image else 'link'}: {target}")
    return errors


def validate_document(
    text: str,
    source: Path,
    *,
    root: Path = ROOT,
    kind: str | None = None,
    check_local_links: bool = True,
) -> list[str]:
    """Validate representation without rewriting or truncating Markdown."""
    errors: list[str] = []
    try:
        metadata, body, body_start = split_front_matter(text)
    except ValueError as exc:
        return [f"{source}: {exc}"]
    kind = kind or _kind(source)
    required = {
        "lesson": ("id", "title", "status", "level", "prerequisites", "outcomes", "assessment", "source_review_date"),
        "assessment": ("id", "status", "lesson", "outcome_map"),
        "integrated": ("id", "status"),
    }[kind]
    for field in required:
        if field not in metadata or metadata[field] is None or metadata[field] == "":
            errors.append(f"{source}: missing metadata field {field!r}")
    if metadata.get("status") != "draft":
        errors.append(f"{source}: canonical artifact must retain status: draft")
    if kind == "lesson":
        if not isinstance(metadata.get("prerequisites"), list) or not all(isinstance(x, str) for x in metadata["prerequisites"]):
            errors.append(f"{source}: prerequisites must be an array of strings")
        if not isinstance(metadata.get("outcomes"), list) or not metadata["outcomes"] or not all(isinstance(x, str) and x for x in metadata["outcomes"]):
            errors.append(f"{source}: outcomes must be a nonempty array of IDs")
        for field in ("id", "title", "assessment"):
            if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                errors.append(f"{source}: {field} must be a nonempty string")
    elif kind == "assessment":
        if not isinstance(metadata.get("outcome_map"), dict) or not metadata["outcome_map"]:
            errors.append(f"{source}: outcome_map must be a nonempty mapping")
        if not isinstance(metadata.get("lesson"), str):
            errors.append(f"{source}: lesson must be a repository-relative path")

    if UNSAFE_LINK.search(body):
        errors.append(f"{source}: unsafe link target in Markdown")

    try:
        tokens = PARSER.parse(body)
    except Exception as exc:
        return errors + [f"{source}: Markdown parse error: {exc}"]
    lines = body.splitlines()
    # Do not mistake literal math syntax inside fenced code for an unsupported
    # math feature. Math-capability checking is deliberately conservative.
    content_lines = list(lines)
    for token in tokens:
        if token.type in ("fence", "code_block") and token.map:
            for pos in range(token.map[0], token.map[1]):
                content_lines[pos] = ""
    if MATH_BLOCK.search("\n".join(content_lines)):
        errors.append(f"{source}: display math syntax is not enabled in v1; request renderer extension without deleting content")
    for token in tokens:
        line = body_start + (token.map[0] if token.map else 0)
        if token.type in {"html_block", "html_inline"}:
            errors.append(f"{source}:{line}: raw HTML/MDX is not supported")
        if token.type == "fence":
            if not _fence_closed(token, lines):
                errors.append(f"{source}:{line}: unclosed fenced code block")
            language = token.info.strip().split(maxsplit=1)[0].lower() if token.info.strip() else ""
            if language == "mermaid":
                diagram = token.content.strip()
                if not diagram:
                    errors.append(f"{source}:{line}: empty Mermaid diagram")
                elif not MERMAID_START.match(diagram):
                    errors.append(f"{source}:{line}: unrecognized Mermaid diagram declaration; full syntax/render validation is deferred")
                if "%%{" in diagram:
                    errors.append(f"{source}:{line}: Mermaid runtime directives are not allowed")
        if token.type != "inline":
            continue
        for child in token.children or []:
            if child.type == "html_inline":
                errors.append(f"{source}:{line}: raw HTML/MDX is not supported")
            elif child.type in {"link_open", "image"}:
                target = child.attrGet("href" if child.type == "link_open" else "src") or ""
                if child.type == "image" and not child.content.strip():
                    errors.append(f"{source}:{line}: image requires meaningful alt text")
                for problem in _link_errors(target, source, root, check_local_links, child.type == "image"):
                    errors.append(f"{source}:{line}: {problem}")
    return errors


def discover(root: Path) -> list[Path]:
    """Cover authored content, not historical review/evidence Markdown."""
    result = []
    for module in (root / "modules").glob("*"):
        if not module.is_dir():
            continue
        if (module / "content-manifest.json").exists():
            raise ValueError(f"{module}: content-manifest.json is obsolete; keep one canonical artifact")
        for folder in ("lessons", "assessments"):
            directory = module / folder
            nested = [p for p in directory.glob("**/*.md") if p.parent != directory]
            if nested:
                raise ValueError(f"{nested[0]}: nested lesson/assessment revisions are unsupported")
            result.extend(directory.glob("*.md"))
        integrated = module / "integrated"
        for pattern in ("brief.md", "solution-rubric*.md", "decision-summary*.md"):
            result.extend(integrated.glob(pattern))
    return sorted(set(result))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", action="append", help="Repository-relative artifact path; may be repeated")
    parser.add_argument("--kind", choices=["lesson", "assessment", "integrated"], help="Explicit kind for --path")
    args = parser.parse_args(argv)
    try:
        paths = [ROOT / p for p in args.path] if args.path else discover(ROOT)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    errors = []
    checked = 0
    for path in paths:
        try:
            path.resolve().relative_to(ROOT.resolve())
            content = path.read_text(encoding="utf-8")
            errors.extend(validate_document(content, path, kind=args.kind))
            checked += 1
        except (ValueError, OSError, UnicodeError) as exc:
            errors.append(f"{path}: {exc}")
    print(f"Academy authoring format: checked {checked} artifacts; found {len(errors)} error(s)")
    for problem in errors:
        print(f"ERROR: {problem}")
    if errors:
        return 1
    print("PASSED (format only, not teaching quality, review, publication, or complete Mermaid syntax)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
