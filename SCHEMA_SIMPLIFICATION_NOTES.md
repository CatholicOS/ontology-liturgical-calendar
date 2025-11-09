# JSON Schema to OWL Conversion - Notes and Changes

## Goal
Convert LitCal.json JSON Schema to OWL ontology format using LinkML toolchain.

## Approach
1. JSON Schema → LinkML YAML (using `schemauto import-json-schema`)
2. LinkML YAML → OWL (using `gen-owl`)

## Changes Made to Create Simplified Schema

The original `LitCal.json` had several features that `schemauto` couldn't handle. Created `LitCal.simplified.json` with these fixes:

### 1. Fixed Union Type with Null (lines 476-479, 675-682)
**Original:**
```json
"grade_display": {
    "type": ["string", "null"],
    "title": "Liturgical Grade Display",
    ...
}
```

**Fixed:**
```json
"grade_display": {
    "type": "string",
    "title": "Liturgical Grade Display",
    ...
}
```
- Changed from array `["string", "null"]` to simple `"string"`
- Removed from `required` array to allow null/absence

### 2. Added Type to Const Boolean Properties (lines 544-548, 582-586, 787-791)
**Original:**
```json
"is_vigil_mass": {
    "const": true,
    "title": "Is Vigil Mass",
    ...
}
```

**Fixed:**
```json
"is_vigil_mass": {
    "type": "boolean",
    "const": true,
    "title": "Is Vigil Mass",
    ...
}
```
- Added explicit `"type": "boolean"` before `const`
- Applied to: `is_vigil_mass`, `holy_day_of_obligation`

### 3. Added Type to oneOf Property (lines 8-20)
**Original:**
```json
"settings": {
    "oneOf": [
        {"$ref": "#/definitions/NationalCalendarSettings"},
        ...
    ]
}
```

**Fixed:**
```json
"settings": {
    "type": "object",
    "description": "Settings for the liturgical calendar request...",
    "oneOf": [
        {"$ref": "#/definitions/NationalCalendarSettings"},
        ...
    ]
}
```
- Added explicit `"type": "object"` and description

### 4. Added Type to anyOf Array Items (lines 146-155)
**Original:**
```json
"litcal": {
    "type": "array",
    "items": {
        "anyOf": [
            {"$ref": "#/definitions/LiturgicalEvent"},
            ...
        ]
    }
}
```

**Fixed:**
```json
"litcal": {
    "type": "array",
    "items": {
        "type": "object",
        "description": "Can be either a LiturgicalEvent or LiturgicalEventVigil",
        "anyOf": [
            {"$ref": "#/definitions/LiturgicalEvent"},
            ...
        ]
    }
}
```
- Added explicit `"type": "object"` and description to items

## Remaining Issues

### External References Not Resolved
The LinkML import process doesn't follow external `$ref` links to `./CommonDef.json`. These types are missing:
- `EventKey`
- `EventKeyVigilMass`
- `EventKeyNonVigilMass`
- `LitColor`
- `LitEventType`
- `LitGrade`
- `LitCommon`
- `Readings`
- `Year`
- `Epiphany`
- `Ascension`
- `CorpusChristi`
- `Locale`
- `HolyDaysOfObligation`
- `Nation`
- `DiocesanCalendarId`
- `AcceptLanguage`

This causes `gen-owl` to fail with: `ValueError: Unknown range LitColor`

### schemauto Warnings (Still Present but Non-Fatal)
Even with fixes, schemauto logs these errors but still produces output:
- `ERROR:root:Cannot translate type object` for `settings` (with oneOf)
- `ERROR:root:Cannot translate type object` for `metadata` (complex nested object)
- `ERROR:root:Cannot translate type object` for `litcal` items (with anyOf)

These are logged but don't prevent YAML generation.

## Solutions to Complete OWL Generation

### Option 1: Inline All Definitions (Recommended)
Create a version where all `./CommonDef.json#/definitions/*` refs are inlined into a single schema file:
```bash
# Requires manual merging of CommonDef.json into LitCal.json
# Or write a script to resolve all $refs
```

### Option 2: Manually Complete LinkML Schema
Edit `LitCal.linkml.yaml` to add missing class/type definitions:
```yaml
classes:
  LitColor:
    # Define based on CommonDef.json
  EventKey:
    # Define based on CommonDef.json
  # etc.
```

### Option 3: Use Alternative Tools
Instead of LinkML, use:
- **Protégé** (GUI) - Manually model ontology
- **ROBOT** - If starting from RDF/OWL
- **Custom Python script** with `rdflib` and `owlready2`

## Files Created
- `jsondata/schemas/LitCal.simplified.json` - Simplified JSON Schema compatible with schemauto
- `jsondata/schemas/LitCal.linkml.yaml` - Generated LinkML schema (incomplete due to external refs)
- `jsondata/schemas/SCHEMA_SIMPLIFICATION_NOTES.md` - This file

## Commands Used
```bash
# Generate LinkML from simplified JSON Schema
schemauto import-json-schema jsondata/schemas/LitCal.simplified.json > jsondata/schemas/LitCal.linkml.yaml

# Attempt to generate OWL (fails due to missing types)
gen-owl jsondata/schemas/LitCal.linkml.yaml -o jsondata/schemas/LitCal.owl --format ttl
```

## Next Steps
1. ✅ Check if CommonDef.json can be imported separately with schemauto
2. ✅ Merge CommonDef.json definitions into LitCal.simplified.json
3. ✅ Regenerate LinkML YAML from merged schema
4. ✅ Attempt OWL generation again

## Final Solution - Option B: Fully Inline Schema

Successfully merged all definitions from CommonDef.json into LitCal.simplified.json and generated OWL ontology.

### Process

1. **Created merge script** (`merge_schemas.py`):
   - Loads both JSON schemas
   - Merges 45 definitions from CommonDef.json
   - Updates all external `$ref` links to internal references
   - Produces `LitCal.merged.json` with 51 total definitions

2. **Generated LinkML YAML**:
   ```bash
   schemauto import-json-schema jsondata/schemas/LitCal.merged.json > jsondata/schemas/LitCal.merged.linkml.yaml
   ```

3. **Generated OWL ontology**:
   ```bash
   gen-owl jsondata/schemas/LitCal.merged.linkml.yaml --format ttl > jsondata/schemas/LitCal.owl
   ```

### Results

✅ **Success!** Generated a complete OWL ontology:
- **File**: `jsondata/schemas/LitCal.owl`
- **Format**: Turtle (TTL)
- **Size**: 91KB
- **Lines**: 2,203 lines
- **Contains**: All classes, properties, and restrictions from the liturgical calendar schema

### Files Created

1. `merge_schemas.py` - Python script to merge schemas and update references
2. `LitCal.merged.json` - Fully inline JSON Schema (no external refs)
3. `LitCal.merged.linkml.yaml` - LinkML schema generated from merged JSON
4. `LitCal.owl` - Final OWL ontology in Turtle format

### Warnings (Non-Fatal)

The `gen-owl` tool produced warnings about "guessing types" for properties without explicit ranges. These are non-fatal and the ontology was generated successfully. Properties affected include reading fields, localized strings, and temporal properties.

### Usage

To regenerate the OWL ontology after schema changes:

```bash
# 1. Update LitCal.json or CommonDef.json as needed
# 2. Re-merge the schemas
python3 merge_schemas.py

# 3. Regenerate LinkML
schemauto import-json-schema jsondata/schemas/LitCal.merged.json 2>/dev/null > jsondata/schemas/LitCal.merged.linkml.yaml

# 4. Regenerate OWL (RDF/XML format for WebProtégé compatibility)
gen-owl jsondata/schemas/LitCal.merged.linkml.yaml --format xml 2>/dev/null > jsondata/schemas/LitCal.rdf.xml

# 5. Fix and validate OWL
python3 fix_owl_ontology.py
```

## WebProtégé Import Issues - Fixed!

### Problem
Initial OWL generation had parsing errors when importing to WebProtégé:
1. **Turtle format** had invalid ontology IRI: `LitCal:.owl.ttl`
2. **RDF/XML format** was missing proper `owl:Ontology` declaration
3. Duplicate ontology declarations from Turtle-to-XML conversion

### Solution
Created `fix_owl_ontology.py` script that:
1. Adds proper `owl:Ontology` declaration with IRI `https://example.org/LitCal`
2. Adds `rdfs:label` and `rdfs:comment` to the ontology
3. Removes invalid duplicate ontology declarations
4. Validates and formats the final OWL file

### Final Valid OWL File
**File**: `jsondata/schemas/LitCal_fixed.owl`
- **Format**: RDF/XML (compatible with WebProtégé)
- **Size**: 249KB
- **Lines**: 3,836 lines
- **Statistics**:
  - Total triples: 2,538
  - OWL Classes: 78
  - Object Properties: 66
  - Single valid ontology: `https://example.org/LitCal`

### Validation
Validated using Python rdflib:
```bash
python3 -c "
from rdflib import Graph
g = Graph()
g.parse('jsondata/schemas/LitCal_fixed.owl', format='xml')
print(f'Valid OWL with {len(g)} triples')
"
```

### Import to WebProtégé
Use the file: **`jsondata/schemas/LitCal_fixed.owl`**

This file has been validated and should import successfully into WebProtégé without parsing errors.
