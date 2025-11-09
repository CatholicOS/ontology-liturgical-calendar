# ontology-liturgical-calendar
A semantic description of the elements that comprise a digital representation of the Roman Catholic liturgical calendar for any given year.

As a first attempt to generate the ontology in OWL format,
I have attempted to convert the JSON schema for the Liturgical Calendar as produced by the Liturgical Calendar API.
I have used Claude Code to assist in the process, and Claude Code summed up the process in this manner:

-----

  ✅ Success - OWL Ontology Generated!

  *Final Output*

  Your OWL ontology has been successfully created:
  - File: `jsondata/schemas/LitCal.owl`
  - Format: Turtle (TTL)
  - Size: 91KB, 2,203 lines
  - Classes: 45+ OWL classes including:
    - `LiturgicalEvent`, `LiturgicalEventVigil`
    - `CalendarSettings`, `NationalCalendarSettings`, `DiocesanCalendarSettings`
    - `ReadingsChristmas`, `ReadingsEaster`, `ReadingsFeast`
    - `LitColor`, `LitGrade`, `LitEventType`
    - And many more...

  *What Was Done*

  1. Created merge script (`merge_schemas.py`):
    - Merged 45 definitions from `CommonDef.json` into `LitCal.simplified.json`
    - Updated all external `$ref` links (`./CommonDef.json#/definitions/X`) to internal refs (`#/definitions/X`)
    - Result: `LitCal.merged.json` with 51 total definitions
  2. Generated LinkML YAML:
  `schemauto import-json-schema jsondata/schemas/LitCal.merged.json`
  2. Created: `LitCal.merged.linkml.yaml`
  3. Generated OWL ontology:
  `gen-owl jsondata/schemas/LitCal.merged.linkml.yaml --format ttl`
  3. Created: `LitCal.owl`

  *Files Created*

  1. `merge_schemas.py` - Reusable Python script for future updates
  2. `LitCal.simplified.json` - Initial simplified schema
  3. `LitCal.merged.json` - Fully inline JSON Schema (no external refs)
  4. `LitCal.merged.linkml.yaml` - Intermediate LinkML format
  5. `LitCal.owl` - Your final OWL ontology! 🎉
  6. `SCHEMA_SIMPLIFICATION_NOTES.md` - Complete documentation

  *To Regenerate After Schema Updates*

  ```bash
  python3 merge_schemas.py
  schemauto import-json-schema jsondata/schemas/LitCal.merged.json 2>/dev/null > jsondata/schemas/LitCal.merged.linkml.yaml
  gen-owl jsondata/schemas/LitCal.merged.linkml.yaml --format ttl 2>/dev/null > jsondata/schemas/LitCal.owl
  ```

  The OWL ontology is ready to use with Protégé, SPARQL queries, or any other semantic web tools!

-----

I was not immediately able to import the resulting OWL file into WebProtege.
I fed the error messages back into Claude Code, which provided a series of steps to attempt a fix:

-----

  ✅ Fixed OWL File Ready for WebProtégé!

  *Problems Found*

  1. Invalid Turtle syntax: The ontology **IRI** was `LitCal:.owl.ttl` instead of a proper **URI**
  2. Missing ontology declaration: **RDF/XML** was missing the `owl:Ontology` element
  3. Duplicate ontologies: Bad **IRI** from Turtle conversion carried over

  *Solution Applied*

  Created and ran `fix_owl_ontology.py` which:
  - Added proper `<owl:Ontology rdf:about="https://example.org/LitCal">` declaration
  - Removed invalid duplicate ontology declarations
  - Validated and formatted the final file

  *Final Validated OWL File*

  Use this file: `jsondata/schemas/LitCal_fixed.owl`

  *Statistics:*
  - ✅ Format: RDF/XML (WebProtégé compatible)
  - ✅ Size: 249KB, 3,836 lines
  - ✅ Total triples: 2,538
  - ✅ OWL Classes: 78
  - ✅ Object Properties: 66
  - ✅ Valid ontology IRI: https://example.org/LitCal
  - ✅ Validated with rdflib parser

  *Files Created/Updated*

  1. `merge_schemas.py` - Merges CommonDef.json into LitCal schema
  2. `fix_owl_ontology.py` - Fixes and validates OWL ontology
  3. `LitCal.merged.json` - Inline JSON Schema
  4. `LitCal.merged.linkml.yaml` - LinkML intermediate format
  5. `LitCal_fixed.owl` - Your validated OWL ontology! 🎉
  6. `SCHEMA_SIMPLIFICATION_NOTES.md` - Complete documentation

  The `LitCal_fixed.owl` file has been validated and should now import successfully into WebProtégé without any parsing errors. Try uploading it again!

-----
