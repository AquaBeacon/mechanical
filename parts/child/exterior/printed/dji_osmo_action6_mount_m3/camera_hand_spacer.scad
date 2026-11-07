// Removable U spacer plus fingertip tab; uses canonical mating spacer.
use <../../../../../scad/lib/camera_rotary_joint.scad>
use <../../../../../scad/lib/edge_finished_profiles.scad>
module camera_hand_spacer() {
 union() {
  camera_qr_spacer();
  translate([-10.5,0,2.25]) ef_box(10,10,6,1.3,.4);
 }
}
camera_hand_spacer();
