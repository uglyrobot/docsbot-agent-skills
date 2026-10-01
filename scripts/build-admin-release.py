#!/usr/bin/env python3
"""Build and validate the complete DocsBot plugin ZIP."""
import argparse
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1] / "plugins" / "docsbot-administration"
REPO_ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PARTS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
FORBIDDEN_NAMES = {".env", ".env.local", "id_rsa", "id_ed25519", "credentials.json", "secrets.json"}
FORBIDDEN_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
EXPECTED_REVIEW_TOOLS = {"list_teams", "list_bots", "get_bot", "list_sources", "get_source", "get_bot_stats", "list_questions", "update_bot"}


def die(message):
    raise SystemExit(message)


def check_https(value, label):
    if not isinstance(value, str) or len(value) > 1024:
        die(f"Invalid {label} URL")
    url = urlsplit(value)
    if url.scheme != "https" or not url.hostname or url.username or url.password:
        die(f"{label} must be a public HTTPS URL without embedded credentials")


def check_asset_path(path, rels, label):
    if not isinstance(path, str) or not path.startswith("./") or path[2:] not in rels:
        die(f"Missing or unsafe {label}: {path}")


def check_path(root, file):
    rel = file.relative_to(root)
    if file.is_symlink() or any(parent.is_symlink() for parent in file.parents if parent.is_relative_to(root)):
        die(f"Symlink forbidden: {rel}")
    if any(p in FORBIDDEN_PARTS for p in rel.parts) or file.name in FORBIDDEN_NAMES or file.suffix in FORBIDDEN_SUFFIXES:
        die(f"Forbidden package content: {rel}")
    if not file.resolve().is_relative_to(root.resolve()):
        die(f"Path escapes package root: {rel}")
    return rel


def check_bundled_references():
    """Entrypoints differ by install surface; shared workflow references must match."""
    canonical = REPO_ROOT / "skills" / "docsbot-administration" / "references"
    bundled = ROOT / "skills" / "docsbot-administration" / "references"
    canonical_files = {p.relative_to(canonical).as_posix(): p for p in canonical.rglob("*") if p.is_file()}
    bundled_files = {p.relative_to(bundled).as_posix(): p for p in bundled.rglob("*") if p.is_file()}
    # This short plugin-only note records the bundled package's source context.
    allowed_extras = {"source-context.md"}
    if set(bundled_files) - set(canonical_files) - allowed_extras:
        die("Unexpected bundled reference: update the canonical skill first")
    for name, source in canonical_files.items():
        if name not in bundled_files or source.read_bytes() != bundled_files[name].read_bytes():
            die(f"Bundled skill reference is stale: {name}. Mirror the canonical reference before packaging")


def main():
    global ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, help="Complete staging package to validate instead of the repository package")
    parser.add_argument("--output", type=Path, help="ZIP output path; omit for validation only")
    args = parser.parse_args()
    if args.package_root:
        ROOT = args.package_root.absolute()
    if ROOT.is_symlink():
        die("Package root must not be a symlink")
    files = sorted((p for p in ROOT.rglob("*") if p.is_file() or p.is_symlink()), key=lambda p: p.relative_to(ROOT).as_posix())
    rels = {check_path(ROOT, p).as_posix(): p for p in files}
    required = {"plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json", ".cursor-plugin/mcp.json", "mcp.json", ".mcp.json", "skills/docsbot-administration/SKILL.md"}
    if missing := required - rels.keys():
        die(f"Missing package files: {sorted(missing)}")
    portable = json.loads(rels["plugin.json"].read_text())
    compat = json.loads(rels[".codex-plugin/plugin.json"].read_text())
    if portable["name"] != compat["name"] or portable["version"] != compat["version"]:
        die("Portable and Codex manifest name or version differs")
    for filename in (".claude-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        client = json.loads(rels[filename].read_text())
        if client.get("name") != portable["name"] or client.get("version") != portable["version"]:
            die(f"{filename} name or version differs from the portable manifest")
    claude = json.loads(rels[".claude-plugin/plugin.json"].read_text())
    if claude.get("displayName") != "DocsBot":
        die("Claude directory displayName must preserve DocsBot capitalization")
    for key in ("privacyPolicyUrl", "supportUrl", "documentationUrl", "termsOfServiceUrl"):
        check_https(claude.get(key), f"Claude {key}")
    check_asset_path(claude.get("icon"), rels, "Claude directory icon")
    if "README.md" not in rels or len(re.sub(r"```.*?```", "", rels["README.md"].read_text(), flags=re.S).split()) < 40:
        die("Claude directory requires a package-local README of at least 40 words")
    if "LICENSE" not in rels and not claude.get("license"):
        die("Claude directory requires a license")
    extension = portable["extensions"]["com.openai"]
    compat_extension = compat["extensions"]["com.openai"]
    if extension["interface"] != compat["interface"]:
        die("Portable and Codex listing interfaces differ")
    if extension["review"] != compat_extension["review"]:
        die("Portable and Codex review cases differ")
    if extension["publication"] != compat_extension["publication"]:
        die("Portable and Codex release notes differ")
    if extension["onboardingSkill"] != compat_extension["onboardingSkill"]:
        die("Portable and Codex onboarding skills differ")
    if any(key in compat for key in ("onboardingSkill", "review", "publication")):
        die("Review, publication, and onboarding belong under extensions.com.openai")
    interface = extension["interface"]
    for key, limit in (("displayName", 30), ("shortDescription", 30), ("developerName", 80), ("longDescription", 4000)):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            die(f"Invalid {key}: must be nonempty and at most {limit} characters")
    if not isinstance(interface.get("category"), str) or not interface["category"].strip():
        die("Missing listing category")
    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or len(capabilities) > 20 or any(not isinstance(c, str) or len(c) > 120 for c in capabilities):
        die("Invalid listing capabilities")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        check_https(interface.get(key), key)
    for key in ("homepage",):
        check_https(portable.get(key), key)
    check_https(portable.get("author", {}).get("url"), "author.url")
    cases = extension["review"]["test_cases"]
    if len(cases["positive"]) != 5 or len(cases["negative"]) != 3:
        die("Review cases must contain exactly five positive and three negative cases")
    for case in cases["positive"]:
        if not all(case.get(k) for k in ("description", "prompt", "tools_triggered", "expected_behavior")):
            die("Incomplete positive review case")
        names = {name.strip() for name in case["tools_triggered"].split(",")}
        if not names or not names <= EXPECTED_REVIEW_TOOLS:
            die("Positive review case has an unknown expected tool")
    for case in cases["negative"]:
        if not all(case.get(k) for k in ("description", "prompt", "expected_behavior")):
            die("Incomplete negative review case")
    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, list) or len(prompts) > 3 or len(set(prompts)) != len(prompts) or any(not isinstance(p, str) or len(p) > 128 for p in prompts):
        die("Starter prompts exceed listing limits")
    if "test_credentials" in extension["review"] or "reviewer_instructions" in extension["review"]:
        die("Review secrets or unsupported fields must not be packaged")
    if "demo_recording_url" in extension["review"]:
        check_https(extension["review"]["demo_recording_url"], "demo_recording_url")
    check_asset_path(extension["onboardingSkill"], rels, "onboarding skill")
    if not extension["onboardingSkill"].endswith("/SKILL.md"):
        die("Onboarding path must point to SKILL.md")
    servers = json.loads(rels["mcp.json"].read_text())["mcpServers"]
    if len(servers) != 1 or next(iter(servers.values()))["url"] != "https://mcp.docsbot.ai":
        die("Expected one DocsBot HTTPS MCP server")
    compat_servers = json.loads(rels[".mcp.json"].read_text())["mcpServers"]
    if set(compat_servers) != set(servers) or any(compat_servers[name]["url"] != servers[name]["url"] for name in servers):
        die("Portable and Codex MCP configurations differ")
    if compat.get("mcpServers") != "./.mcp.json" or compat.get("skills") != "./skills/":
        die("Codex manifest MCP or skills path differs")
    cursor = json.loads(rels[".cursor-plugin/plugin.json"].read_text())
    if cursor.get("skills") != "./skills/" or cursor.get("mcpServers") != "./.cursor-plugin/mcp.json":
        die("Cursor manifest MCP or skills path differs")
    cursor_servers = json.loads(rels[".cursor-plugin/mcp.json"].read_text())["mcpServers"]
    if set(cursor_servers) != set(servers) or any(cursor_servers[name].get("url") != servers[name]["url"] for name in servers):
        die("Cursor and Codex MCP endpoints differ")
    cursor_logo = cursor.get("logo", "")
    check_asset_path(cursor_logo if cursor_logo.startswith("./") else f"./{cursor_logo}", rels, "Cursor logo")
    if not args.package_root:
        check_bundled_references()
    for key in ("composerIcon", "logo", "logoDark"):
        check_asset_path(interface.get(key), rels, key)
    for key in ("composerIconDark",):
        if key in interface:
            check_asset_path(interface[key], rels, key)
    for path in interface.get("screenshots", []):
        check_asset_path(path, rels, "screenshot")
    for name, p in rels.items():
        if not name.endswith("/SKILL.md"):
            continue
        body = p.read_text()
        if not body.startswith("---\n") or "\n---\n" not in body[4:]:
            die(f"Missing skill YAML frontmatter: {name}")
        frontmatter = body.split("\n---\n", 1)[0][4:]
        if not re.search(r"(?m)^name:\s*\S+", frontmatter) or not re.search(r"(?m)^description:\s*\S+", frontmatter):
            die(f"Missing skill name or description: {name}")
    for name, p in rels.items():
        if not name.endswith(".md"):
            continue
        text = p.read_text()
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            ref = (p.parent / target.split("#", 1)[0]).resolve()
            if not ref.is_relative_to(ROOT.resolve()) or not ref.is_file() or ref.is_symlink():
                die(f"Missing or unsafe reference from {name}: {target}")
            if ref.relative_to(ROOT).as_posix() not in rels:
                die(f"Unbundled reference from {name}: {target}")
    for name, p in rels.items():
        if p.suffix not in {".md", ".json", ".yaml", ".txt"}:
            continue
        body = p.read_text(errors="replace")
        if "-----BEGIN PRIVATE KEY-----" in body or re.search(
            r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[=:]\s*['\"](?:sk-|ghp_|pat_|eyJ)[A-Za-z0-9._-]{12,}",
            body,
        ):
            die(f"Possible packaged credential: {name}")
    if args.output:
        output = args.output.resolve()
        if output.is_relative_to(ROOT.resolve()):
            die("Output ZIP must be outside the package root")
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, p in rels.items():
                info = zipfile.ZipInfo(name, FIXED_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        with zipfile.ZipFile(output) as archive:
            if archive.namelist() != sorted(rels):
                die("ZIP entries differ from validated source")
        print(f"Built {output} ({len(rels)} files, version {portable['version']})")
    else:
        print(f"Validated {len(rels)} package files (version {portable['version']})")


if __name__ == "__main__":
    main()
