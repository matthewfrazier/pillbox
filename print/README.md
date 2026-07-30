# Pillbox printable artifacts

- `pillbox_prusaslicer_project.3mf`: combined two-object PrusaSlicer project
- `pillbox_sleeve_print.stl`: centered, bed-placed sleeve
- `pillbox_drawer_print.stl`: centered, bed-placed drawer
- `pillbox_combined_plate.stl`: both objects arranged on one virtual plate

Both manufactured objects are closed, manifold, single-component meshes. The optimized export resolution is approximately 0.1 mm, finer than a typical 0.4 mm FDM nozzle.

The 3MF intentionally does not embed a printer-specific machine or filament profile. Select the actual printer, PETG preset, nozzle, and layer height before slicing.

The open-face-up geometry has shallow underside features: sleeve stiffening beads and the drawer's rear-bottom detent. Inspect the first-layer preview and enable build-plate supports or a suitable support/raft strategy beneath those features. Do not allow the slicer to remove the functional detents as small artifacts.

## Supportless vertical print

`prepare_supportless_plate.py` creates separate print exports and a combined plate with the sleeve
stood on its closed end and the drawer placed bottom-down. `slice_for_material_p2s.sh` slices that
plate for a requested material/profile while preserving the prepared orientation and disabling
supports. `print_from_ams_slot.py --list-materials` queries loaded AMS materials; for a print it
refuses to start unless the requested slot reports the requested material, then explicitly maps the
single sliced filament to that slot.
