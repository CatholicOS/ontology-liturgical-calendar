#!/usr/bin/env python3
"""
Merge CommonDef.json definitions into LitCal.simplified.json
and update all external references to internal references.
"""

import json
import re
from pathlib import Path

def merge_schemas(litcal_path, commondef_path, output_path):
    """
    Merge CommonDef.json definitions into LitCal schema and update references.

    Args:
        litcal_path: Path to LitCal.simplified.json
        commondef_path: Path to CommonDef.json
        output_path: Path for merged output schema
    """
    # Load both schemas
    with open(litcal_path, 'r', encoding='utf-8') as f:
        litcal = json.load(f)

    with open(commondef_path, 'r', encoding='utf-8') as f:
        commondef = json.load(f)

    # Get definitions from CommonDef
    commondef_definitions = commondef.get('definitions', {})

    # Get existing definitions from LitCal (if any)
    litcal_definitions = litcal.get('definitions', {})

    # Merge definitions - CommonDef definitions come first, then LitCal's own definitions
    # This way LitCal's definitions can override if needed
    merged_definitions = {**commondef_definitions, **litcal_definitions}

    # Update the definitions in litcal
    litcal['definitions'] = merged_definitions

    # Convert the schema to string for regex replacement
    schema_str = json.dumps(litcal, indent=4)

    # Replace all external references to CommonDef with internal references
    # Pattern: "./CommonDef.json#/definitions/SomeName" -> "#/definitions/SomeName"
    schema_str = re.sub(
        r'"\.\/CommonDef\.json#\/definitions\/([^"]+)"',
        r'"#/definitions/\1"',
        schema_str
    )

    # Parse back to ensure valid JSON
    litcal_merged = json.loads(schema_str)

    # Write merged schema
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(litcal_merged, f, indent=4, ensure_ascii=False)

    print(f"✓ Merged {len(commondef_definitions)} definitions from CommonDef.json")
    print(f"✓ Total definitions in merged schema: {len(merged_definitions)}")
    print(f"✓ Saved to: {output_path}")

    return litcal_merged

if __name__ == "__main__":
    base_dir = Path(__file__).parent / "jsondata" / "schemas"

    litcal_path = base_dir / "LitCal.simplified.json"
    commondef_path = base_dir / "CommonDef.json"
    output_path = base_dir / "LitCal.merged.json"

    merge_schemas(litcal_path, commondef_path, output_path)
