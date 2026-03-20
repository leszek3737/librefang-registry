# Scripts

Utility scripts for maintaining the LibreFang registry.

## validate.py

Validates all TOML content files across the registry.

```bash
python scripts/validate.py
```

### What It Checks

**Per content type:**
- **Providers** -- required fields, valid tiers, non-negative costs, no duplicate model IDs
- **Agents** -- required fields (name, description, module), name matches directory
- **Hands** -- required fields (id, name, description), valid category, [agent] section, id matches directory
- **Integrations** -- required fields (id, name), [transport] section, id matches filename
- **Skills** -- [skill] section with name, [runtime] with valid type
- **Plugins** -- name matches directory, [hooks] section, hook files exist

**Cross-type checks:**
- Routing alias collisions between agents and hands (reported as warnings)
- Cross-file duplicate model IDs within the same provider

### Requirements

- Python 3.11+ (uses `tomllib`)
- Or Python 3.8+ with `pip install tomli`

### Exit Codes

- `0` -- all checks passed
- `1` -- one or more validation errors
