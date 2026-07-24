This directory contains the local generator for the profile README and SVG asset system.

- `generate_profile.py` reads `../profile.config.json`
- It regenerates `README.md`
- It regenerates SVG assets in `../assets/svg`
- It regenerates the icon set in `../assets/icons`

The goal is to keep profile content and design tokens centralized in one config file so updates stay surgical and diff-friendly.
