# Pillbox Project - File Index

**Location**: `/Users/mf/code/pillbox/`
**Project Status**: Production-ready (PETG)
**Last Updated**: 2026-07-20

---

## Quick Links (Start Here)

| What | File |
|------|------|
| **Overview** | `README.md` |
| **Full Specification** | `SPEC.md` |
| **For Handoff** | `HANDOFF.md` ← READ THIS FIRST |
| **Material Decision** | `MATERIAL_ASSESSMENT.md` |
| **Design Issues** | `REVISED_DESIGN_NOTES.md` |

---

## Production Files (Ready to Print)

### CAD Model
- **`pillbox_model.blend`** (393 KB)
  - Source of truth for design
  - Editable Blender file
  - Includes drawer motion animation keyframes
  - All modifiers applied and baked

### STL for 3D Printing
- **`pillbox_sleeve.stl`** (40 KB)
  - Sleeve/container component
  - Import directly into slicer
  - Material: PETG recommended
  - Print orientation: flat (86×54mm base down)

- **`pillbox_drawer.stl`** (41 KB)
  - Drawer component with dividers and pull grip
  - Import directly into slicer
  - Material: PETG recommended
  - Print orientation: flat (84×50.2mm base down)

---

## Documentation (Read in Order)

### 1. Project Context
- **`README.md`** (2.1 KB)
  - Quick project summary
  - Dimensions and features overview
  - Assembly notes

### 2. Full Specification
- **`SPEC.md`** (4.9 KB)
  - Complete design requirements
  - Tolerance stack
  - Material specifications
  - All features documented
  - **Status**: Final (2026-07-20)

### 3. Material Selection
- **`MATERIAL_ASSESSMENT.md`** (7.9 KB)
  - PLA vs PETG comparison
  - Detent mechanism analysis (critical read)
  - Biocompatibility for pill storage
  - Test protocols documented
  - **Decision**: PETG mandatory

- **`REVISED_DESIGN_NOTES.md`** (6.5 KB)
  - Why updated spec broke PLA viability
  - Analysis of tight tolerances (0.2mm)
  - Three-point locking complexity
  - Testing alternatives
  - **Conclusion**: Direct PETG production recommended

### 4. Validation & Verification
- **`COMPARISON.md`** (1.5 KB)
  - Initial spec vs model verification
  - List of implemented features
  - Refinements made

- **`EXPORT_SUMMARY.md`** (2.7 KB)
  - Export process details
  - File sizes and formats
  - Print recommendations
  - Tolerance verification summary

- **`ANIMATION_GUIDE.md`** (2.7 KB)
  - 3-frame drawer motion demonstration
  - Compartment geometry verified (flat dividers)
  - Assembly instructions
  - Use scenarios documented

### 5. Handoff & Next Steps
- **`HANDOFF.md`** (7.8 KB)
  - Comprehensive project summary
  - Status and decisions
  - Production phases (3 phases documented)
  - Technical details for next person
  - Critical tolerances listed
  - **START HERE** for continuing work

---

## Directory Structure

```
~/code/pillbox/
├── pillbox_model.blend          ← CAD source
├── pillbox_sleeve.stl            ← Print component 1
├── pillbox_drawer.stl            ← Print component 2
├── SPEC.md                        ← Design specification
├── README.md                      ← Quick reference
├── HANDOFF.md                     ← Continuation guide
├── MATERIAL_ASSESSMENT.md         ← Material decision
├── REVISED_DESIGN_NOTES.md        ← Design implications
├── EXPORT_SUMMARY.md              ← Export details
├── ANIMATION_GUIDE.md             ← Motion demo
├── COMPARISON.md                  ← Verification
├── INDEX.md                       ← This file
├── engineering/                   ← (Legacy, can ignore)
└── print/                         ← (Legacy, can ignore)
```

---

## Key Files by Use Case

### "I need to understand this project"
1. Read: `README.md`
2. Read: `SPEC.md`
3. Skim: `HANDOFF.md`

### "I need to print this"
1. Read: `HANDOFF.md` → Phase 2
2. Open: `pillbox_sleeve.stl` in slicer
3. Open: `pillbox_drawer.stl` in slicer
4. Use: Material: PETG, Settings from `EXPORT_SUMMARY.md`

### "I need to understand material choice"
1. Read: `MATERIAL_ASSESSMENT.md` (complete analysis)
2. Read: `REVISED_DESIGN_NOTES.md` (why PLA won't work)
3. Check: `HANDOFF.md` → Decision Record section

### "I need to modify the design"
1. Open: `pillbox_model.blend` in Blender
2. Make changes
3. Export: STL files
4. Update: `SPEC.md` with new dimensions
5. Document: Changes in new section of `HANDOFF.md`

### "I need to continue this project later"
1. Read: `HANDOFF.md` completely
2. Check: Production phases (Phase 1, 2, or 3)
3. Refer to: `REVISED_DESIGN_NOTES.md` for testing strategy
4. Follow: Printer requirements in `HANDOFF.md`

---

## Version Control Summary

| File | Date | Status |
|------|------|--------|
| SPEC.md | 2026-07-20 | FINAL (updated with stiffening beads, texture, 3-point locking) |
| pillbox_model.blend | 2026-07-15 | Production-ready |
| pillbox_*.stl | 2026-07-15 | Production-ready (validated for PETG) |
| HANDOFF.md | 2026-07-20 | NEW (comprehensive handoff guide) |
| MATERIAL_ASSESSMENT.md | 2026-07-20 | NEW (PLA vs PETG analysis) |
| REVISED_DESIGN_NOTES.md | 2026-07-20 | NEW (updated spec implications) |

---

## Quick Reference

### Dimensions
- **Sleeve**: 86 × 54 × 19 mm (credit card + 0.75" height)
- **Drawer**: 84 × 50.2 × 15 mm (slides from 54mm edge)
- **Compartments**: 3 equal spaces (~28mm each)
- **Pull grip**: 50mm wide (full drawer front)

### Material
- **Recommended**: PETG
- **Why not PLA**: Detents fracture, tight tolerances uncontrollable, texture bumps collapse
- **Expected lifespan**: 1+ years (PETG), 2-4 weeks (PLA)

### Tolerances (Critical)
- Drawer/sleeve clearance: 0.20mm sides
- Detent interference: 0.05mm (3 points)
- Print accuracy needed: ±0.1mm on 0.2mm features

### Print Settings
- Material: PETG
- Nozzle: 240-250°C
- Bed: 60-80°C
- Orientation: Flat (86×54mm base down)
- Layer: 0.1mm
- Infill: 100%

---

## Contact/Context

**Project**: Pillbox (credit-card pill organizer)
**Team**: Claude Code / Blender / Python
**Session**: pillbox (2026-07-15 to 2026-07-20)
**Status**: Ready for PETG production print

All files are self-contained. No external dependencies.

---

## Next Action

**Recommended next step**: Read `HANDOFF.md` and follow Phase 2 (PETG Production Print).

Expected timeline: 2-3 weeks to validated production model.
