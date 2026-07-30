# Revised Design Notes: Advanced Specifications

## Updated SPEC Summary
The specification has been substantially revised from the initial CAD model to include:

### Sleeve Changes
- **Stiffening beads**: Shallow longitudinal ribs on roof/floor (maintain 19mm height)
- **Interior microtexture**: PETG bumps (~0.3mm) above compartments (prevent rattle)
- **Three-point detent locking**: 
  - Two symmetric side bumps (drawer edge locks)
  - One rear-bottom bump (prevents tipping)
- **Detent receivers**: Shallow recesses (non-through) in inner walls and floor
- **Variable wall thickness**: 
  - Base: 1.1mm nominal (beaded)
  - Beads: ~2.1mm local thickness
  - Side walls: 1.7mm nominal

### Drawer Changes
- **Monolithic construction**: Single solid body (no separate dividers)
- **Tight tolerances**:
  - Side clearance: 0.20mm each side (0.40mm total)
  - Bottom clearance: 0.20mm
  - Top clearance: 0.60mm to plain ceiling, 0.30mm to texture crowns
- **Compartment microtexture**: ~0.3mm bumps with 6mm spacing on each floor
- **Full-width pull grip**: 50mm wide (entire front face), integrated with drawer
- **Pull ridges**: Shallow grip texture on top surface
- **Divider walls**: 1.2mm thick (thin and flexible for PETG properties)

---

## Implications for PLA Test

### Complexity Jump
**Original CAD**: Simple rectangular boxes + bevel
**Revised Spec**: Advanced features requiring precision printing

### PLA Printing Challenges

#### 1. Stiffening Beads
- **PLA**: Ribs will be brittle, prone to chipping
- **Risk**: Ribs crack if drawer slides roughly
- **Test impact**: Adds noise/friction if beads fracture

#### 2. Microtexture Bumps
- **PLA**: 0.3mm bumps hard to print cleanly; may collapse/merge
- **PETG**: Bumps stay crisp and rounded
- **Test finding**: PLA bumps will be mushy; effectiveness unknown

#### 3. Three-Point Detent Locking
- **Critical for PLA**: This is now MORE demanding, not less
- **Original spec**: Simple 2-point (side) locking
- **New spec**: Add 3rd rear-bottom lock (increases complexity)
- **PLA risk**: Rear bump will fracture first under repeated drawer closure

#### 4. Tight Tolerances
- **Original**: Clearances were ~1.0mm (forgiving)
- **New spec**: 0.20mm side clearances (60% tighter)
- **PLA problem**: Shrinkage/warping at 0.2mm tolerance is uncontrollable
  - Drawer may jam (too tight)
  - Or rattle (too loose)
  - Test will be inconclusive due to print variability

#### 5. Monolithic Drawer
- **PLA**: Single solid with 1.2mm dividers and 0.20mm clearances
- **Stress concentration**: Dividers are thin and weak in PLA
- **Risk**: Dividers may flex excessively, allowing compartment walls to catch

---

## PLA Test Viability Assessment

### Verdict: **PLA Test is now HIGH RISK**

**Why the updated spec broke PLA viability:**

| Feature | Original CAD | Revised Spec | PLA Impact |
|---------|--------------|--------------|-----------|
| Tolerance | ±1.0mm | ±0.2mm | Print variability dominates |
| Detents | 2-point | 3-point | Rear lock WILL fracture |
| Texture | None | 0.3mm bumps | Bumps will be mushy |
| Dividers | 1.5mm | 1.2mm | Fragile in PLA, risk jamming |
| Beads | None | 2.1mm local | Ribs will chip/snap |

### Modified PLA Test Approach (if still desired)

**Only viable if simplifying the design:**

```
PLA Test Spec (de-featured):
- Remove stiffening beads (flat walls)
- Remove microtexture bumps (smooth surfaces)
- Reduce to 2-point detent (side locks only, no rear lock)
- Increase clearances to 0.5mm (printable tolerance)
- Use 1.5mm divider thickness

Result: Validates basic geometry only
NOT representative of final product
```

**Recommendation**: Skip PLA test entirely.

---

## Revised Testing Strategy

### Option A: Direct PETG Production (Recommended)
1. Print full spec in PETG
2. Test detent mechanism (most critical feature)
3. Validate tolerance stacking
4. Assess texture effectiveness
5. Run durability test (500+ cycles)

**Timeline**: 2-3 weeks
**Cost**: One full print (~$15-25 material)
**Confidence**: High (full spec tested)

### Option B: Parametric Study (If design uncertainty)
**Don't test materials yet. Test the spec itself:**

1. **Tolerance sensitivity**:
   - Print 3 drawer samples at different scale offsets (±0.05mm)
   - Measure actual clearance vs. design
   - Validate CAD tolerance stack is achievable

2. **Detent force**:
   - 3D print load cell strain gauge setup
   - Measure insertion force for 3-point locking
   - Validate 0.05mm interference is appropriate

3. **Texture effectiveness**:
   - Print compartments with/without microtexture
   - Test pill motion under vibration
   - Confirm texture reduces rattle

4. **Then proceed to PETG** with validated parameters

**Timeline**: 4-5 weeks
**Cost**: Multiple prints (~$40-50)
**Confidence**: Very high (design validated before production)

---

## Material Decision for This Design

### For the Revised Spec:
**PETG is now essential, not optional**

**Specific reasons:**
1. **Rear-bottom detent**: Needs flex recovery; PLA will snap
2. **Tight 0.2mm clearances**: Requires stable material; PLA shrinks unpredictably
3. **Texture bumps**: PLA bumps won't hold shape; PETG stays crisp
4. **Stiffening beads**: PLA ribs will chip; PETG ribs are durable
5. **Biocompatibility + durability**: PETG now dominates all criteria

### PLA Now Unviable For:
- ❌ Detent locking (especially rear lock)
- ❌ Tight tolerance assembly
- ❌ Microtexture durability
- ❌ Long-term storage use

---

## Recommendations

### Immediate Actions
1. **Confirm design intent**: Are stiffening beads and microtexture critical to function?
   - If yes → PETG is mandatory
   - If no → Simplify spec, then PLA test becomes possible

2. **Finalize tolerance budget**:
   - Current 0.2mm clearance is TIGHT for FDM
   - Consider relaxing to 0.3-0.4mm for print reliability
   - Or validate with tolerance study first

3. **Prioritize detent validation**:
   - 3-point locking is complex
   - Test physical model (even cardboard) before printing
   - Confirm rear-bottom lock works as intended

### For PLA vs PETG Decision
**No ambiguity with updated spec:**
- **Test print material**: PETG (represents final product)
- **PLA role**: Design iteration only (if simplifying)

### Cost/Timeline
- **PETG full spec**: 1-2 weeks, single print, ~$20 material
- **PLA simplified spec + PETG final**: 3 weeks, 2 prints, ~$35 material
- **Parametric study + PETG**: 4-5 weeks, multiple prints, ~$50 material

**Recommendation**: Go straight to PETG full spec. Revised design is mature; new features (beads, texture, 3-point lock) don't require PLA validation.
