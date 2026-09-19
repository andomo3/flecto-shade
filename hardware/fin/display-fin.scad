// K1: modelled display adaptation of ITKE's Flectofin, EP2320015.
// All dimensions are millimetres and ASSUMED; see README.md.
// Edit these dimensions, press F6 in OpenSCAD, then export STL.
// Geometry only: no deformation or structural simulation is performed.
rib_length_mm = 150;
rib_thickness_mm = 1.5;
rib_height_mm = 5;
sheet_clear_width_mm = 40;
sheet_thickness_mm = 0.4;

assert(rib_length_mm > 0 && rib_thickness_mm > 0);
assert(sheet_clear_width_mm > 0 && sheet_thickness_mm > 0);
assert(rib_height_mm > sheet_thickness_mm);
union() {
    cube([rib_length_mm, rib_thickness_mm, rib_height_mm]);
    // The sheet extends under the rib, making a continuous solid union.
    cube([rib_length_mm, rib_thickness_mm + sheet_clear_width_mm,
          sheet_thickness_mm]);
}
