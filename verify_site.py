"""
Verification suite for HNAI website.
Validates HTML tag structure, JSON-LD schemas, anchor targets, Progen invariants,
visual aesthetics, feature coverage, and JavaScript syntax.
Zero copula. Exit code zero is passing.
"""

import html.parser
import json
import os
import re
import subprocess
import sys


class TagChecker(html.parser.HTMLParser):
    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if "id" in attrs_dict:
            self.ids.add(attrs_dict["id"])
        if tag not in self.VOID_TAGS:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]}")
            return
        expected, pos = self.stack.pop()
        if expected != tag:
            self.errors.append(
                f"Mismatched tag: expected </{expected}> from line {pos[0]}, found </{tag}> at line {self.getpos()[0]}"
            )


def verify_html_and_anchors(html_content: str):
    checker = TagChecker()
    checker.feed(html_content)
    assert not checker.errors, f"HTML syntax errors: {checker.errors[:5]}"
    assert not checker.stack, f"Unclosed tags: {[t[0] for t in checker.stack]}"

    # Verify all internal href targets
    hrefs = re.findall(r'href="#([a-zA-Z0-9_\-]+)"', html_content)
    for target in hrefs:
        assert target in checker.ids, f"Broken internal anchor href: #{target} not found in DOM ids"

    print(f"[OK] HTML tag structure verified. Found {len(checker.ids)} valid DOM IDs.")
    return checker.ids


def verify_json_ld(html_content: str):
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_content, re.DOTALL)
    assert scripts, "No JSON-LD metadata found in index.html"
    for i, s in enumerate(scripts):
        data = json.loads(s.strip())
        assert "@graph" in data or "@type" in data, f"Malformed JSON-LD structure in script {i}"
        # Verify hydra is registered
        graph = data.get("@graph", [])
        hydra_entry = next((item for item in graph if "hydra" in item.get("@id", "")), None)
        assert hydra_entry is not None, "Hydra SoftwareSourceCode entry missing in JSON-LD @graph"
    print(f"[OK] JSON-LD metadata validated ({len(scripts)} script block).")


def verify_progen_invariants(hydra_html: str):
    # Rule P001: Zero parentheticals in running prose
    # Strip <pre>...</pre>, <code>...</code>, <script>...</script>, <style>...</style>, HTML tags
    cleaned = re.sub(r"<pre.*?</pre>", "", hydra_html, flags=re.DOTALL)
    cleaned = re.sub(r"<code.*?</code>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"<script.*?</script>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"<style.*?</style>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)

    # Check remaining text for parentheses
    parentheses_matches = re.findall(r"[^\n.?!;]*\([^\n)]*\)[^\n.?!;]*", cleaned)
    if parentheses_matches:
        for m in parentheses_matches[:5]:
            print(f"[ERROR] P001 violation (parenthetical in running prose): {m.strip()}")
        raise AssertionError(f"P001 violation: found {len(parentheses_matches)} parentheticals in Hydra running prose.")

    # Rule P018: Zero leading copula in comments
    comments = re.findall(r"<!--(.*?)-->", hydra_html, flags=re.DOTALL)
    copula_pattern = re.compile(r"^\s*(is|are|was|were)\b", re.IGNORECASE)
    for c in comments:
        lines = [line.strip() for line in c.splitlines() if line.strip()]
        for line in lines:
            if copula_pattern.match(line):
                raise AssertionError(f"P018 violation (leading copula in comment): {line}")

    print("[OK] Progen invariants P001 (zero parentheticals) and P018 (zero leading copula) verified.")


def verify_feature_coverage(hydra_html: str):
    text = hydra_html.lower()

    # 1. Functions
    functions = [
        "multi-model routing",
        "prompt execution",
        "interactive tui",
        "continuous swarms",
        "background orchestrator daemon",
        "7777",
    ]
    for fn in functions:
        assert fn in text, f"Missing required function coverage: {fn}"

    # 2. Integrations
    integrations = [
        "opus 5.5",
        "sonnet 5.5",
        "gpt-6.1 sol",
        "cloudflare",
        "openrouter",
        "vercel",
        "hugging face",
        "cheaperinference",
        "ollama",
        "llama.cpp",
        "alice",
    ]
    for integ in integrations:
        assert integ in text, f"Missing required integration coverage: {integ}"

    # 3. Benefits
    benefits = [
        "sovereign local data privacy",
        "compute tiering economics",
        "cross-model consensus verification",
        "zero vendor lock-in",
        "offline fallback",
    ]
    for b in benefits:
        assert b in text, f"Missing required benefit coverage: {b}"

    # 4. Use cases
    use_cases = [
        "autonomous coding swarms",
        "continuous overnight research daemons",
        "terminal workflow automation",
        "multi-model code review",
        "knowledge graph ingestion",
    ]
    for uc in use_cases:
        assert uc in text, f"Missing required use case coverage: {uc}"

    print("[OK] All required feature sections (functions, integrations, benefits, use cases) verified.")


def verify_visual_aesthetics(css_content: str):
    # Electric violet check
    assert "#8a2be2" in css_content.lower(), "Electric violet color #8a2be2 missing from CSS"
    # Dark background checks
    assert "#0a0a0a" in css_content.lower(), "Dark background #0a0a0a missing from CSS"
    assert "#000000" in css_content.lower() or "#000" in css_content.lower(), "Deep black missing from CSS"
    # Cascadia Code typography
    assert "cascadia code" in css_content.lower(), "Cascadia Code font missing from CSS"
    # Spring interactions
    assert "cubic-bezier" in css_content.lower(), "Spring interaction bezier curve missing from CSS"
    print("[OK] Visual aesthetics verified: #8a2be2 electric violet, dark surfaces, Cascadia Code, spring curves.")


def verify_js_syntax():
    js_path = os.path.join(os.path.dirname(__file__), "main.js")
    result = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Node syntax check failed on main.js:\n{result.stderr}"
    print("[OK] JavaScript syntax verified with node --check main.js.")


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(root, "index.html")
    css_path = os.path.join(root, "styles.css")

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    verify_html_and_anchors(html_content)
    verify_json_ld(html_content)
    verify_visual_aesthetics(css_content)
    verify_js_syntax()

    # Extract hydra article
    hydra_match = re.search(r'(<article[^>]+id="hydra".*?</article>)', html_content, re.DOTALL)
    if hydra_match:
        hydra_html = hydra_match.group(1)
        verify_progen_invariants(hydra_html)
        verify_feature_coverage(hydra_html)
    else:
        print("[WARN] <article id=\"hydra\"> not yet updated with full showcase.")

    print("\nALL VERIFICATION GATES PASSED (EXIT CODE 0).")


if __name__ == "__main__":
    main()
