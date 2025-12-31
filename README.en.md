# Khipro Mappings

[বাংলায় পড়ুন](README.md)

Converts [Khipro M17N](https://github.com/rank-coder/khipro-m17n) keyboard mappings from M17N format to JSON.

## What's Inside

| File | Description |
|------|-------------|
| `scripts/full.py` | Converts all mappings from M17N `.mim` file to JSON |
| `scripts/touchscreen.py` | Applies Khipro touchscreen adoption guide with some exclusions and changes |
| `output/full.json` | All mappings from `.mim` file converted to JSON |
| `output/touchscreen.json` | Khipro touchscreen adoption - with some exclusions and changes applied |

## Usage

Using GitHub Actions:
**Actions** → **Convert MIM to JSON** → **Run workflow**

- For custom `.mim` file: paste URL in `mim_url` field
- For custom commit message: type in `commit_message` field
- Leave blank for defaults, then click **Run**
