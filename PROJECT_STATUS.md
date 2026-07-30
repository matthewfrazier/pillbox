# Pillbox Project - Complete Status & Reproduction Guide

**Last Updated**: 2026-07-30  
**Project Status**: Multiple design iterations complete; ready for evaluation and printing

---

## Overview

3D-printable credit-card-sized pill organizer with two-part design (sleeve + drawer). Project includes:
- **Original spec** (v1): Friction-lock detent mechanism
- **Evolved designs** (v2-v6): Advanced locking mechanisms (squeeze-lock, bayonet, rotary cam, edge-roller)
- **Complete documentation**: Specifications, material analysis, design rationale
- **Production files**: STL exports and Blender CAD models

---

## File Organization

### Core Design Files (Production-Ready)

| File | Size | Purpose |
|------|------|---------|
| `pillbox_model.blend` | 393 KB | **Original final design** (v1: friction-lock detents) |
| `pillbox_sleeve.stl` | 40 KB | v1 sleeve for 3D printing |
| `pillbox_drawer.stl` | 40 KB | v1 drawer for 3D printing |

### Advanced Iterations (Post-Original Spec)

**v2: Squeeze-Lock Mechanism** (Jul 21)
- `pillbox_model_v2_squeeze_lock.blend` (45 MB)
- `pillbox_sleeve_v2_squeeze_lock.stl` (55 MB)
- `pillbox_drawer_v2_squeeze_lock.stl` (42 MB)
- `revise_squeeze_lock.py` — design modification script

**v3: Thumbbolt Lock** (Jul 22)
- `pillbox_model_v3_thumbbolt.blend` (89 MB)

**v4: Four Lock Alternatives** (Jul 22)
- `pillbox_v4_lock_alternatives.blend` (89 MB)
- `pillbox_v4_bayonet_lock_animation.mp4`
- `pillbox_v4_dual_cam_lock_animation.mp4`
- `pillbox_v4_four_lock_alternatives.png` — comparison visualization

**v5: Rotary Cam** (Jul 22)
- `pillbox_v5_rotary_cam_preview.blend` (89 MB)
- Screenshots: overview, cutaway

**v6: Edge Roller Cam** (Jul 23)
- `pillbox_v6_edge_roller_cam_preview.blend` (89 MB)
- `pillbox_v6_print_layout_plan.blend` (89 MB) — optimized print layout
- `design_edge_roller_cam_preview.py`
- `design_edge_roller_print_layout.py`
- Screenshots: mechanism, overview, inventory

### Documentation

**Original Specification & Analysis**
- `README.md` — Project overview
- `SPEC.md` — v1 final design specification
- `MATERIAL_ASSESSMENT.md` — PLA vs PETG analysis, detent mechanism stress testing
- `REVISED_DESIGN_NOTES.md` — Why updated specs broke PLA viability

**Handoff & Navigation**
- `INDEX.md` — File index and navigation guide
- `HANDOFF.md` — Comprehensive continuation guide with 3 production phases
- `COMPARISON.md` — v1 spec verification
- `EXPORT_SUMMARY.md` — Export details and tolerances
- `ANIMATION_GUIDE.md` — Drawer motion demonstration

**Iteration Scripts & Artifacts**
- `design_edge_roller_cam_preview.py` — v6 mechanism design script
- `design_edge_roller_print_layout.py` — v6 print layout optimization
- `revise_squeeze_lock.py` — v2 mechanism refinement
- `v4_animation_frames/` — 200+ animation frame PNGs for lock mechanisms
- `engineering/` — Legacy analysis files
- `print/` — Legacy print planning files

---

## Quick Start: What to Print

### Option A: Original Spec (v1) — Friction-Lock Detents
```
Use these files:
- pillbox_sleeve.stl (40 KB)
- pillbox_drawer.stl (40 KB)

Material: PETG (mandatory; PLA will fail in 2-4 weeks)
Print settings: 240-250°C nozzle, 60-80°C bed, 0.1mm layers, 100% infill
Expected: ~500+ drawer cycles, reliable detent locking
Read: MATERIAL_ASSESSMENT.md for full analysis
```

### Option B: Advanced Mechanisms (v2-v6) — For Evaluation
All mechanisms documented in Blender CAD files. Open in Blender 4.0+ to:
- Preview geometry
- Review lock mechanism designs
- Export custom STLs
- View animation keyframes (where present)

---

## Project Evolution Summary

### v1: Original Specification (Jul 15-20)
- Credit-card dimensions: 86 × 54 × 19 mm
- Three-point friction-lock (two sides + rear-bottom)
- Stiffening beads on roof/floor
- Microtexture bumps (0.3mm) on compartment floors
- Tight tolerances: 0.2mm clearances, 0.05mm detent interference
- **Material decision**: PETG mandatory (PLA detents fracture by week 2-4)
- **Status**: Design complete, production-ready

### v2-v6: Lock Mechanism Exploration (Jul 21-23)
Post-specification exploration of alternative locking mechanisms:
- **v2**: Squeeze-lock (mechanical compression)
- **v3**: Thumbbolt (screw-down retention)
- **v4**: Bayonet/dual-cam (rotational engagement)
- **v5**: Rotary cam (continuous rotation)
- **v6**: Edge roller cam (rolling contact mechanism)

Each iteration explores tradeoffs between:
- Ease of use (one-handed vs two-handed)
- Mechanical complexity
- Print tolerance sensitivity
- Detent force feedback

**Status**: Documented in CAD, not yet printed/validated

---

## Material Assessment (v1)

### PETG (Recommended)
- Young's modulus: 1939 MPa
- Yield stress: 46.2 MPa
- Expected lifespan: 1+ year (1000+ drawer cycles)
- Handles tight 0.2mm tolerances reliably
- Biocompatible for pill storage; easy to clean

### PLA (Not Recommended)
- Detent mechanism fails by week 2-4 of daily use
- Tight tolerances uncontrollable (shrinkage variability)
- Microtexture bumps collapse/degrade
- Temperature sensitive (softens ~60°C)
- See `MATERIAL_ASSESSMENT.md` for detailed stress analysis

---

## Tolerances (v1)

Critical dimensions for printing:
- Drawer/sleeve clearance: **0.20 mm** each side
- Detent interference: **0.05 mm** (per point)
- Print accuracy required: **±0.1 mm** on 0.2mm features

---

## Reproduction: From Source to Print

### Phase 1: CAD Verification
1. Open `pillbox_model.blend` in Blender 4.0+
2. Inspect geometry:
   - Sleeve outer: 86 × 54 × 19 mm
   - Drawer outer: 84 × 50.2 × 15 mm
   - 3 equal compartments (~28mm each)
   - Stiffening beads on roof/floor
   - Three-point detent locking visible
3. Verify in SPEC.md

### Phase 2: Export STL
```bash
# Using Blender CLI or GUI:
# Select sleeve → Export → STL (binary format, 86×54mm base down)
# Select drawer → Export → STL (binary format, 84×50.2mm base down)
```

### Phase 3: Print Preparation
1. Import into slicer (Cura, PrusaSlicer, etc.)
2. Configure:
   - Material: PETG
   - Nozzle: 240-250°C
   - Bed: 60-80°C
   - Layer height: 0.1mm (critical for tolerance)
   - Infill: 100% (monolithic)
   - Speed: 30-40 mm/s (quality over speed)
   - Orientation: Flat (86×54mm base down)

### Phase 4: Post-Print Testing
1. Assembly: Insert drawer into sleeve
2. Test cycle: 10 insertions to verify detent engagement
3. Durability: 500+ cycles over 1-2 weeks
4. Environmental: Test in 40-50°C conditions (summer car/pocket)
5. Cleanliness: Wash in warm water, verify no degradation

See `HANDOFF.md` for complete Phase 1-3 production roadmap.

---

## Design Decision Record

### Why Three-Point Locking (v1)?
- Prevents tipping (rear-bottom lock critical)
- Provides symmetry and tactile feedback
- Engages smoothly with PETG flex recovery
- Minimal insertion force (~5N predicted)

### Why Tight Tolerances (v1)?
- 0.2mm clearances: tight but achievable on calibrated FDM
- Reduces drawer rattle/noise
- Allows use of thin divider walls (1.2mm) with flex
- Requires PETG (PLA shrinks unpredictably at this scale)

### Why Friction-Lock Over Slide-Lock (v1)?
- Simpler mechanism (no additional parts)
- No jamming risk
- Reduces component count (2 parts total: sleeve + drawer)
- Noted as future enhancement in spec

### Why Post-Spec Iterations (v2-v6)?
User exploration of alternative locking mechanisms:
- **Trade study**: Compare mechanical complexity vs usability
- **Research**: Evaluate cam profiles, engagement forces, manufacturing feasibility
- **Documentation**: CAD models serve as reference for future lock design

---

## Files Needed to Continue Work

### Minimum for Reproduction
- `pillbox_model.blend` (CAD source of truth)
- `pillbox_sleeve.stl` & `pillbox_drawer.stl` (print files)
- `SPEC.md` (specification)
- `MATERIAL_ASSESSMENT.md` (material choice justification)

### Full Context
- `HANDOFF.md` (continuation guide with phases)
- `INDEX.md` (navigation guide)
- All documentation files (Md files)

### For Design Modification
- Any `*.blend` file matching your target mechanism
- Python scripts (`design_*.py`, `revise_*.py`) for automated refinement
- `v4_animation_frames/` for animation reference

---

## Next Steps

**Pick One:**

1. **Print v1 in PETG** (Recommended)
   - Follow Phase 2-3 in HANDOFF.md
   - Test detent mechanism
   - Validate 0.2mm tolerances
   - Run durability test (500+ cycles)

2. **Evaluate Lock Mechanisms** (v2-v6)
   - Open each Blender file
   - Review mechanism geometry
   - Compare force diagrams
   - Select preferred variant
   - Export STL and print

3. **Refine Design**
   - Modify CAD in Blender
   - Run Python design scripts for parametric studies
   - Export new STLs
   - Update SPEC.md with changes
   - Document rationale in HANDOFF.md

---

## Contacts & Context

**Project**: Pillbox (credit-card pill organizer)  
**Team**: Claude Code (Haiku 4.5) + Blender  
**Sessions**: pillobx (initial design + handoff), additional iterations  
**Infrastructure**: MCP Python API for Blender automation

All work is self-contained in this directory. No external dependencies or cloud services required.
