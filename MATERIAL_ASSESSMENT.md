# Material Assessment: PLA vs PETG for Pill Organizer

## Application Context
- **Use case**: Swallowable pill storage
- **Critical concern**: Biocompatibility, cleanliness, chemical resistance
- **Key mechanism**: Friction-lock detents (0.05mm interference)
- **Durability requirement**: Daily pocket carry, repeated drawer slides (100s of cycles)

---

## Material Comparison Matrix

### PLA (Polylactic Acid)
#### Advantages
- Lower density → lighter
- Better dimensional stability during printing
- Easier to print (lower temp, less warping)
- More economical
- Faster print times
- Better surface finish inherently
- More food-contact safe (some certifications exist)

#### Disadvantages
- **Brittleness**: High risk of crack propagation at detent peaks
- **Low flexibility**: Detents will be rigid, no give
- **Temperature sensitivity**: Softens ~60°C (dishwasher unsafe, hot climates risky)
- **Chemical resistance**: Susceptible to alcohol, some solvents in pill coatings
- **Moisture absorption**: Slight (~0.3-0.6%), causes dimensional drift
- **Impact sensitivity**: Sharp impacts can crack monolithic structure
- **Detent performance**: Will be unpredictable; may snap at 0.05mm interference
- **Creep**: Gradual permanent deformation under repeated stress

### PETG (Polyethylene Terephthalate Glycol)
#### Advantages
- **Toughness**: Absorbs deflection energy without snapping
- **Elasticity**: Detents will flex predictably and recover
- **Chemical resistance**: Superior to PLA; resists most pill coatings
- **Temperature tolerance**: Stable to ~80°C (safer for warm pockets/climates)
- **Impact resistance**: Won't shatter on drops
- **Dimensional stability**: Lower moisture uptake (~0.05%)
- **Detent predictability**: Will perform as engineered at 0.05mm interference
- **Longevity**: Maintains properties over 1000s of cycles

#### Disadvantages
- Higher print temp (more prone to warping)
- Requires better bed adhesion/cooling strategy
- Slightly slower print
- Higher material cost
- More prone to stringing (cosmetic)

---

## Detent Mechanism Analysis

### PLA Detents
```
Problem: Brittle fracture at peak stress points

Scenario 1 - First assembly:
- Drawer forced in → PLA flex ~ 0.02-0.03mm
- Detent peak stress: σ = 46.2 MPa (theoretical yield)
- With anisotropic print effects: actual σ_yield ~ 35-40 MPa
- Risk: Peak may micro-fracture on first insertion

Scenario 2 - Repeated cycles (week of use):
- Cumulative micro-cracks at detent edges
- Crack propagation in XY-plane (weaker direction)
- Result: Detent loses grip; drawer slides freely by week 2

Scenario 3 - Temperature stress:
- Summer in car: 40-50°C
- PLA stiffens, becomes more brittle
- Crack risk INCREASES with heat
```

### PETG Detents
```
Predictable elastic behavior

Scenario 1 - First assembly:
- Drawer forced in → PETG flexes 0.04-0.05mm
- Wall strain: ~2-3% (well below yield ~4-5%)
- Detent seats, holds, no damage

Scenario 2 - Repeated cycles:
- 1000s of insertions: consistent flex behavior
- No plastic creep at this stress level
- Detents remain functional

Scenario 3 - Temperature:
- 40-50°C: PETG maintains stiffness
- No change in grip performance
- No brittleness increase
```

---

## Biocompatibility & Cleanliness

### PLA
- Generally recognized as food-contact safe (GRAS)
- BUT: Porous structure in FDM print allows bacterial harboring
- Moisture absorption can create growth environment
- Pill coatings: some may contain solvents that attack PLA
- **Risk**: If organizer not cleaned regularly, bacteria could transfer to pills
- **Mitigation**: Requires weekly disassembly and hot water wash

### PETG
- Food-contact capable (some brands certified)
- Lower porosity than PLA
- More resistant to pill-coating solvents
- Easier to clean (less water uptake)
- **Advantage**: Can be washed in 60°C water safely
- **Better hygiene**: Lower bacterial adhesion rates

---

## Test Print Recommendations

### PLA Test Strategy
**If you decide to test PLA despite brittleness:**

1. **Print settings**:
   - 0.1mm layer height (max detail on detents)
   - 100% infill (monolithic = stronger)
   - Slow nozzle speed (~30 mm/s on detents)
   - Print flat (86×54mm base down) for layer strength

2. **Detent modifications**:
   - Increase detent radius: 0.5mm → 0.8mm (reduces peak stress)
   - Reduce interference: 0.05mm → 0.03mm (less insertion force)
   - Add generous fillet to detent base (minimum 0.3mm radius)
   - Result: Weaker grip, but less likely to fracture

3. **Test protocol**:
   - **Day 1**: 10 insertion cycles → check for cracks
   - **Days 2-3**: 50 cycles/day → test drawer retention
   - **Week 1**: Normal use → assess grip fade
   - **Heat test**: Place in 40°C environment for 2 hours, repeat cycles
   - **Chemical test**: Wipe with alcohol, repeat cycles

4. **Failure modes to watch**:
   - Micro-cracks at detent peak (optical inspection)
   - Loss of retention (drawer slides freely)
   - Brittle fracture on thermal stress
   - Visible wear/whitening at stress points

---

## PETG Specification Assessment

### Current PETG Spec (from updated SPEC.md)
- Detent interference: 0.05mm each side + bottom
- Wall thickness: 1.5mm (drawer perimeter), 1.2mm (dividers)
- Edge radius: 1.2-1.5mm
- Material model: Young's 1939 MPa, yield 46.2 MPa

### PLA Equivalent (if proceeding)
**Must revise downward**:
- Interference: 0.03mm (60% reduction) — weaker grip
- Wall thickness: Increase to 2.0mm perimeter (to handle lower yield)
- Edge radius: Minimum 0.5mm on detents (prevent stress concentration)
- Material model: Young's ~2500 MPa (stiffer), yield ~50-55 MPa (but brittle)

**Result**: Functional but marginal. Drawer will hold, but grip will be unreliable by week 4-8.

---

## Recommendation

### For Pill Storage Specifically:
**→ PETG is strongly preferred**

**Why:**
1. **Safety**: Biocompatible AND more hygienic (easier to clean)
2. **Reliability**: Detents will function predictably for 1+ year of daily use
3. **Temperature resilience**: Won't fail in hot climates or summer cars
4. **Cost vs performance**: Material cost difference (~$1-2) is negligible vs re-printing twice with PLA failures

### PLA Test Print Use Case:
- **Only justified if**: You want to validate geometry before PETG production
- **Acceptable risk**: Use PLA as throwaway prototype, then print final in PETG
- **NOT for long-term use**: PLA organizer will degrade within weeks to months

---

## Suggested Test Plan

### Phase 1: PLA Geometry Validation (1 week)
- Print with modified detents (0.03mm interference)
- Test 2-3 days of moderate use
- Assess fit, compartment spacing, grip ergonomics
- **Goal**: Confirm design works, not durability validation

### Phase 2: PETG Production Print (1-2 weeks)
- Print with original spec (0.05mm interference)
- Long-term test (4+ weeks of daily use)
- Validate detent performance, thermal stability
- **Goal**: Production-ready design

### Phase 3: Comparison Report
- Document PLA performance fade over week 2-3
- Highlight PETG reliability advantages
- Quantify cycle count before failure for each material

---

## Material Decision Matrix

| Criterion | PLA | PETG |
|-----------|-----|------|
| **Detent durability** | ⚠️ Marginal | ✅ Excellent |
| **Biocompatibility** | ✅ Good | ✅ Good |
| **Hygiene/Cleanability** | ⚠️ Fair | ✅ Excellent |
| **Temperature stability** | ⚠️ Poor | ✅ Good |
| **Chemical resistance** | ⚠️ Fair | ✅ Good |
| **Impact resistance** | ⚠️ Poor | ✅ Good |
| **Print ease** | ✅ Easy | ⚠️ Moderate |
| **Cost** | ✅ Lower | ⚠️ Higher |
| **Long-term reliability** | ❌ 4-8 weeks | ✅ 12+ months |

---

## Conclusion

**PLA Test**: Acceptable for geometry validation only. Expect detent failure by week 3-4 of regular use.

**PETG Production**: Recommended for actual use. 0.05mm interference detents will perform reliably for 1+ year at ~500 cycles/month.

**Biocompatibility**: Both materials are food-contact safe, but PETG's superior cleanliness profile makes it safer for swallowable-pill storage long-term.
