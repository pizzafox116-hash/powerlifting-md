# powerlifting-md

Converts powerlifting notes from `.txt` to Markdown for an Obsidian vault.

## Usage

```
python txt_to_md.py <txt-folder> <vault-folder> [--overwrite]
```

- Recurses through `<txt-folder>` and mirrors its subfolders in the vault.
- Originals are left untouched; existing `.md` files are skipped unless `--overwrite` is passed.
- `•` bullets become `-`, Windows line endings are normalized, non-UTF-8 files are decoded.
