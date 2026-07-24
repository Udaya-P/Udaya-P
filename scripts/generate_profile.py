#!/usr/bin/env python3
"""Generate the profile README and SVG assets from a single config file."""

from __future__ import annotations

import base64
import html
import mimetypes
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "profile.config.json"
ASSETS_SVG = ROOT / "assets" / "svg"
ASSETS_ICONS = ROOT / "assets" / "icons"
README_PATH = ROOT / "README.md"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def initials(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", value)
    if not words:
        return "?"
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[1][0]).upper()


def css_tokens(config: dict) -> str:
    light = config["design"]["tokens"]["light"]
    dark = config["design"]["tokens"]["dark"]
    heading = config["design"]["fonts"]["heading"]
    body = config["design"]["fonts"]["body"]
    return f"""
      :root {{
        --bg: {light["bg"]};
        --surface: {light["surface"]};
        --text: {light["text"]};
        --muted: {light["muted"]};
        --accent: {light["accent"]};
        --accent-2: {light["accent_secondary"]};
        --line: {light["line"]};
        --heading: {heading};
        --body: {body};
      }}
      @media (prefers-color-scheme: dark) {{
        :root {{
          --bg: {dark["bg"]};
          --surface: {dark["surface"]};
          --text: {dark["text"]};
          --muted: {dark["muted"]};
          --accent: {dark["accent"]};
          --accent-2: {dark["accent_secondary"]};
          --line: {dark["line"]};
        }}
      }}
      .bg {{ fill: var(--bg); }}
      .surface {{ fill: var(--surface); }}
      .text {{ fill: var(--text); }}
      .muted {{ fill: var(--muted); }}
      .line {{ stroke: var(--line); }}
      .accent {{ fill: var(--accent); }}
      .accent-stroke {{ stroke: var(--accent); }}
      .accent-2 {{ fill: var(--accent-2); }}
      .heading {{ font-family: var(--heading); }}
      .body {{ font-family: var(--body); }}
    """.strip()


def svg_shell(title: str, desc: str, view_box: str, body: str, extra_defs: str = "") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" role="img" aria-labelledby="title desc">
  <title>{html.escape(title)}</title>
  <desc>{html.escape(desc)}</desc>
  <defs>
    {extra_defs}
  </defs>
  <style>
    {GLOBAL_CSS}
  </style>
  {body}
</svg>
"""


def generate_banner(config: dict) -> str:
    name = config["profile"]["name"]
    tagline = config["profile"]["tagline"]
    desc = "A technical banner with the profile holder's name, role, and restrained geometric accents."
    body = f"""
  <rect class="bg" width="1600" height="420" rx="36"/>
  <rect x="40" y="40" width="1520" height="340" rx="28" fill="none" stroke="var(--line)" stroke-width="2"/>
  <path d="M1120 110 C1260 40, 1420 60, 1500 180" fill="none" stroke="var(--line)" stroke-width="2"/>
  <path d="M1050 300 C1200 220, 1360 240, 1490 340" fill="none" stroke="var(--line)" stroke-width="2"/>
  <circle cx="1280" cy="145" r="12" class="accent"/>
  <circle cx="1450" cy="295" r="8" class="accent-2"/>
  <g stroke="var(--line)" stroke-width="1.4" opacity="0.8">
    <path d="M1210 110 h150"/>
    <path d="M1210 150 h220"/>
    <path d="M1210 190 h190"/>
    <path d="M1210 230 h250"/>
    <path d="M1210 270 h160"/>
  </g>
  <g opacity="0.9">
    <text x="92" y="154" class="text heading" font-size="62" letter-spacing="0.5">{html.escape(name)}</text>
    <text x="96" y="208" class="muted body" font-size="26">{html.escape(tagline)}</text>
    <text x="96" y="282" class="text body" font-size="22">Building intelligent systems with a software engineering mindset.</text>
    <text x="96" y="317" class="muted body" font-size="20">Research-driven, practical, and focused on long-term technical growth.</text>
  </g>
  <g transform="translate(1180 108)">
    <rect width="276" height="180" rx="24" class="surface" stroke="var(--line)" stroke-width="1.5"/>
    <text x="28" y="48" class="muted body" font-size="14">CURRENT LENS</text>
    <text x="28" y="86" class="text heading" font-size="32">AI + SWE</text>
    <text x="28" y="120" class="muted body" font-size="17">Explainable NLP</text>
    <text x="28" y="146" class="muted body" font-size="17">Backend foundations</text>
    <text x="28" y="172" class="muted body" font-size="17">Systems thinking</text>
  </g>
"""
    return svg_shell("Profile Banner", desc, "0 0 1600 420", body)


def generate_portrait(config: dict) -> str:
    image_path = ROOT / config["design"]["portrait_image"]
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/jpeg"
    defs = f"""
    <clipPath id="portrait-clip">
      <circle cx="320" cy="320" r="220"/>
    </clipPath>
    <radialGradient id="halo" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="var(--surface)"/>
      <stop offset="100%" stop-color="var(--bg)"/>
    </radialGradient>
    <filter id="soft-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="18" stdDeviation="24" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
  """
    body = f"""
  <rect class="bg" width="640" height="640" rx="40"/>
  <circle cx="320" cy="320" r="255" fill="url(#halo)"/>
  <circle cx="320" cy="320" r="258" fill="none" stroke="var(--line)" stroke-width="2"/>
  <circle cx="320" cy="320" r="220" class="surface" filter="url(#soft-shadow)"/>
  <g stroke="var(--line)" stroke-width="1.4" fill="none" opacity="0.65">
    <path d="M98 182 h80 v56"/>
    <circle cx="146" cy="408" r="16"/>
    <path d="M458 126 h34"/>
    <path d="M503 120 v40"/>
    <path d="M502 455 h72"/>
    <path d="M538 420 v70"/>
  </g>
  <g opacity="0.85">
    <circle cx="144" cy="140" r="10" class="accent"/>
    <circle cx="510" cy="104" r="8" class="accent-2"/>
    <circle cx="520" cy="514" r="8" class="accent"/>
  </g>
  <image href="data:{mime_type};base64,{encoded}" x="84" y="84" width="472" height="472" clip-path="url(#portrait-clip)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="320" cy="320" r="220" fill="none" stroke="var(--line)" stroke-width="2"/>
"""
    desc = "A minimal portrait frame with a professional vector-style rendering of the profile owner."
    return svg_shell("Portrait", desc, "0 0 640 640", body, defs)


def generate_terminal_card(config: dict) -> str:
    focus = config["profile"]["current_focus"]
    learning = config["profile"]["currently_learning"][:4]
    lines = [
        '$ whoami',
        f'> {config["profile"]["tagline"]}',
        '$ current-focus',
        f'> {focus[0]}',
        f'> {focus[1]}',
        '$ learning',
        f'> {learning[0]}',
        f'> {learning[1]}',
        f'> {learning[2]}',
        f'> {learning[3]}'
    ]
    text_lines = "\n".join(
        f'<text x="34" y="{82 + i * 34}" class="{"muted" if line.startswith("$") else "text"} body" font-size="18">{html.escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    body = f"""
  <rect class="bg" width="760" height="420" rx="28"/>
  <rect x="18" y="18" width="724" height="384" rx="22" class="surface" stroke="var(--line)" stroke-width="1.5"/>
  <circle cx="54" cy="48" r="7" class="accent"/>
  <circle cx="78" cy="48" r="7" fill="var(--line)"/>
  <circle cx="102" cy="48" r="7" class="accent-2"/>
  <text x="134" y="54" class="muted body" font-size="14">focus-terminal</text>
  <path d="M34 68 h692" class="line" stroke-width="1"/>
  {text_lines}
"""
    desc = "A calm technical card summarizing the profile owner's focus and current learning areas."
    return svg_shell("Terminal Card", desc, "0 0 760 420", body)


def generate_timeline(config: dict) -> str:
    items = config["timeline"]
    y_positions = [106, 214, 322, 430, 538]
    groups = []
    for index, item in enumerate(items):
      y = y_positions[index]
      accent_class = "accent" if item["year"] == "2026" else "surface"
      year_fill = "var(--bg)" if item["year"] == "2026" else "var(--text)"
      groups.append(f"""
  <g transform="translate(0 {y})">
    <circle cx="96" cy="0" r="14" class="{accent_class}" stroke="var(--line)" stroke-width="2"/>
    <text x="146" y="-12" class="text heading" font-size="24">{html.escape(item["year"])}</text>
    <text x="146" y="22" class="muted body" font-size="18">{html.escape(item["event"])}</text>
  </g>
""")
    body = f"""
  <rect class="bg" width="1400" height="620" rx="36"/>
  <rect x="34" y="34" width="1332" height="552" rx="28" class="surface" stroke="var(--line)" stroke-width="1.5"/>
  <text x="74" y="88" class="muted body" font-size="16">TIMELINE</text>
  <path d="M96 106 V538" fill="none" stroke="var(--line)" stroke-width="2"/>
  <rect x="1068" y="76" width="226" height="90" rx="20" fill="none" stroke="var(--line)" stroke-width="1.5"/>
  <text x="1100" y="114" class="muted body" font-size="14">CURRENT ARC</text>
  <text x="1100" y="146" class="text heading" font-size="28">Research -> Product</text>
  {''.join(groups)}
"""
    desc = "A concise timeline showing the profile owner's academic and technical journey from 2023 to 2027."
    return svg_shell("Timeline", desc, "0 0 1400 620", body)


def generate_footer(config: dict) -> str:
    initials_text = "".join(word[0] for word in config["profile"]["name"].split()[:3]).upper()
    body = f"""
  <rect class="bg" width="1400" height="180" rx="28"/>
  <path d="M60 90 h360" class="line" stroke-width="1.5" fill="none"/>
  <path d="M980 90 h360" class="line" stroke-width="1.5" fill="none"/>
  <circle cx="700" cy="90" r="46" class="surface" stroke="var(--line)" stroke-width="1.5"/>
  <text x="700" y="101" text-anchor="middle" class="text heading" font-size="28">{initials_text}</text>
  <text x="700" y="150" text-anchor="middle" class="muted body" font-size="16">Engineering thoughtful AI systems with clarity, rigor, and restraint.</text>
"""
    desc = "A restrained footer mark with a monogram and closing line."
    return svg_shell("Footer", desc, "0 0 1400 180", body)


def generate_analytics_card(config: dict) -> str:
    breakdown = config["github"]["public_language_breakdown"][:4]
    bars = []
    max_count = max(item["count"] for item in breakdown)
    for index, item in enumerate(breakdown):
        y = 160 + index * 54
        width = 320 * item["count"] / max_count
        bars.append(f"""
  <text x="62" y="{y}" class="muted body" font-size="16">{html.escape(item["language"])}</text>
  <rect x="236" y="{y - 16}" width="320" height="16" rx="8" fill="var(--bg)"/>
  <rect x="236" y="{y - 16}" width="{width:.1f}" height="16" rx="8" class="accent"/>
  <text x="574" y="{y}" class="text body" font-size="16">{item["count"]}</text>
""")
    body = f"""
  <rect class="bg" width="1200" height="420" rx="32"/>
  <rect x="28" y="28" width="1144" height="364" rx="24" class="surface" stroke="var(--line)" stroke-width="1.5"/>
  <text x="62" y="82" class="muted body" font-size="15">VERIFIED PUBLIC SNAPSHOT</text>
  <text x="62" y="132" class="text heading" font-size="34">{config["github"]["public_repos"]} public repositories</text>
  <text x="62" y="358" class="muted body" font-size="16">Account created on {config["github"]["account_created"]} | Dominant public repo language: {config["github"]["dominant_public_language"]}</text>
  <g transform="translate(700 72)">
    <rect width="394" height="118" rx="22" fill="none" stroke="var(--line)" stroke-width="1.5"/>
    <text x="30" y="38" class="muted body" font-size="14">PROFILE METADATA</text>
    <text x="30" y="76" class="text heading" font-size="26">{config["github"]["followers"]} followers · {config["github"]["following"]} following</text>
    <text x="30" y="100" class="muted body" font-size="15">Kept secondary to projects and research by design.</text>
  </g>
  {''.join(bars)}
"""
    desc = "A compact analytics summary based on verified public GitHub metadata."
    return svg_shell("GitHub Analytics", desc, "0 0 1200 420", body)


def generate_icon(name: str) -> str:
    label = html.escape(name)
    mark = html.escape(initials(name))
    body = f"""
  <rect class="bg" width="160" height="64" rx="18"/>
  <rect x="1" y="1" width="158" height="62" rx="17" class="surface" stroke="var(--line)" stroke-width="1.5"/>
  <circle cx="32" cy="32" r="16" class="accent"/>
  <text x="32" y="37" text-anchor="middle" fill="var(--bg)" class="body" font-size="14">{mark}</text>
  <text x="58" y="37" class="text body" font-size="14">{label}</text>
"""
    desc = f"A compact icon chip for {name}."
    return svg_shell(f"{name} Icon", desc, "0 0 160 64", body)


def write_svg(path: Path, content: str) -> None:
    path.write_text(content)


def build_readme(config: dict) -> str:
    profile = config["profile"]
    facts = [
        f"Computer Science (AI & ML) student at {profile['university']}",
        f"Based in {profile['location']}",
        f"Graduating in {profile['graduation_year']}",
        "Interested in Software Engineering, Machine Learning, and Explainable AI"
    ]

    project_sections = []
    for project in config["featured_projects"]:
        stack = " · ".join(project["stack"])
        if project["public_link_verified"]:
            repo_line = f'[{project["repo_url"].replace("https://github.com/", "")}]({project["repo_url"]})'
            verification_line = "Verified as a public repository on July 23, 2026."
        else:
            repo_line = project["repo_url"]
            verification_line = "Public link could not be verified on July 23, 2026, so it is shown as provided."
        project_sections.append(
            f"""### {project["name"]}
{project["summary"]}

- Status: `{project["status"]}`
- Stack: `{stack}`
- Collaboration: {project["collaboration"]}
- Repository: {repo_line}
- Link status: {verification_line}
"""
        )

    icon_names = [
        "Python", "Java", "SQL", "PyTorch", "TensorFlow", "Transformers",
        "Flask", "Spring Boot", "MySQL", "GitHub Actions", "Linux", "System Design"
    ]
    icon_html = "\n".join(
        f'<img src="./assets/icons/{slugify(name)}.svg" alt="{html.escape(name)} icon" width="160" />'
        for name in icon_names
    )

    tech_sections = []
    for category, values in config["tech_stack"].items():
        tech_sections.append(f"- **{category}:** " + ", ".join(values))

    timeline_lines = "\n".join(f"- **{item['year']}** — {item['event']}" for item in config["timeline"])
    links_line = " · ".join([
        f"[GitHub]({profile['github']})",
        f"[LinkedIn]({profile['linkedin']})",
        f"[Portfolio]({profile['portfolio']})",
        f"[Email](mailto:{profile['email']})"
    ])
    learning = ", ".join(profile["currently_learning"])

    return f"""![Profile banner](./assets/svg/banner.svg)

# {profile["name"]}

{profile["tagline"]}

{links_line}

## Hero

Building intelligent systems with a software engineering mindset, with current emphasis on explainable NLP, research-to-product thinking, and strong backend fundamentals.

## About

<table>
  <tr>
    <td width="34%" valign="top">
      <img src="./assets/svg/portrait.svg" alt="Vector-style portrait of {html.escape(profile['name'])}" width="280" />
    </td>
    <td width="66%" valign="top">
      <p>{profile["about"]}</p>
      <ul>
        {''.join(f"<li>{html.escape(fact)}</li>" for fact in facts)}
      </ul>
      <p><strong>Current focus:</strong> {", ".join(profile["current_focus"])}</p>
      <p><strong>Currently learning:</strong> {learning}</p>
      <img src="./assets/svg/terminal-card.svg" alt="Technical focus card" width="100%" />
    </td>
  </tr>
</table>

## Featured Projects

{chr(10).join(project_sections)}

## Tech Stack

<p>{icon_html}</p>

{chr(10).join(tech_sections)}

## GitHub Analytics

<img src="./assets/svg/analytics-card.svg" alt="Verified GitHub analytics summary" width="100%" />

## Timeline

<img src="./assets/svg/timeline.svg" alt="Career and academic timeline" width="100%" />

{timeline_lines}

## Contact

I'm always happy to connect around AI engineering, explainable ML, backend systems, and thoughtful software development.

- Email: [{profile["email"]}](mailto:{profile["email"]})
- LinkedIn: [{profile["linkedin"].replace("https://", "")}]({profile["linkedin"]})
- Portfolio: [{profile["portfolio"]}]({profile["portfolio"]})
- GitHub: [{profile["github"].replace("https://github.com/", "")}]({profile["github"]})

## Footer

<img src="./assets/svg/footer.svg" alt="Profile footer mark" width="100%" />
"""


def main() -> None:
    config = load_config()
    ASSETS_SVG.mkdir(parents=True, exist_ok=True)
    ASSETS_ICONS.mkdir(parents=True, exist_ok=True)

    write_svg(ASSETS_SVG / "banner.svg", generate_banner(config))
    write_svg(ASSETS_SVG / "portrait.svg", generate_portrait(config))
    write_svg(ASSETS_SVG / "terminal-card.svg", generate_terminal_card(config))
    write_svg(ASSETS_SVG / "timeline.svg", generate_timeline(config))
    write_svg(ASSETS_SVG / "footer.svg", generate_footer(config))
    write_svg(ASSETS_SVG / "analytics-card.svg", generate_analytics_card(config))

    icon_names = sorted({item for values in config["tech_stack"].values() for item in values})
    icon_names.extend(["System Design"])
    for name in sorted(set(icon_names)):
        write_svg(ASSETS_ICONS / f"{slugify(name)}.svg", generate_icon(name))

    README_PATH.write_text(build_readme(config))


GLOBAL_CSS = css_tokens(load_config())


if __name__ == "__main__":
    main()
