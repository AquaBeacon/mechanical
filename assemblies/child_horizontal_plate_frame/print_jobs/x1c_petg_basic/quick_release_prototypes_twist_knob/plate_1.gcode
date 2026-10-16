; HEADER_BLOCK_START
; BambuStudio 02.08.02.61
; model printing time: 12m 49s; total estimated time: 13m 8s
; total layer number: 50
; total filament length [mm] : 612.87
; total filament volume [cm^3] : 1474.13
; total filament weight [g] : 1.84
; filament_density: 1.25
; filament_diameter: 1.75
; max_z_height: 10.00
; filament: 1
; support_material_on_wipe_tower: 0
; HEADER_BLOCK_END

; CONFIG_BLOCK_START
; accel_to_decel_enable = 0
; accel_to_decel_factor = 50%
; activate_air_filtration = 0
; additional_cooling_fan_speed = 0
; additional_fan_full_speed_layer = 0
; alternate_extra_wall = 0
; ams_filament_load_time_ams = 0
; ams_filament_load_time_ams_lite = 0
; ams_filament_load_time_n3f_s = 0
; ams_filament_unload_time_ams = 0
; ams_filament_unload_time_ams_lite = 0
; ams_filament_unload_time_n3f_s = 0
; apply_scarf_seam_on_circles = 1
; auxiliary_fan = 1
; avoid_crossing_wall_includes_support = 0
; bed_custom_model = 
; bed_custom_texture = 
; bed_exclude_area = 0x0,18x0,18x28,0x28
; bed_heat_soak_area = 
; bed_temperature_formula = by_first_filament
; before_layer_change_gcode = 
; best_object_pos = 0.5,0.5
; bottom_color_penetration_layers = 3
; bottom_shell_layers = 3
; bottom_shell_thickness = 0
; bottom_surface_density = 100%
; bottom_surface_pattern = monotonic
; bridge_angle = 0
; bridge_flow = 1
; bridge_no_support = 0
; bridge_speed = 50
; brim_object_gap = 0.1
; brim_type = outer_only
; brim_width = 5
; chamber_temperatures = 0
; change_filament_gcode = M620 S[next_extruder]A\nM204 S9000\nG1 Z{max_layer_z + 3.0} F1200\n\nG1 X70 F21000\nG1 Y245\nG1 Y265 F3000\nM400\nM106 P1 S0\nM106 P2 S0\n{if old_filament_temp > 142 && next_extruder < 255}\nM104 S[old_filament_temp]\n{endif}\nG1 X90 F3000\nG1 Y255 F4000\nG1 X100 F5000\nG1 X120 F15000\n\nG1 X20 Y50 F21000\nG1 Y-3\n{if toolchange_count == 2}\n; get travel path for change filament\nM620.1 X[travel_point_1_x] Y[travel_point_1_y] F21000 P0\nM620.1 X[travel_point_2_x] Y[travel_point_2_y] F21000 P1\nM620.1 X[travel_point_3_x] Y[travel_point_3_y] F21000 P2\n{endif}\nM620.1 E F[old_filament_e_feedrate] T{nozzle_temperature_range_high[previous_extruder]}\nT[next_extruder]\nM620.1 E F[new_filament_e_feedrate] T{nozzle_temperature_range_high[next_extruder]}\n\n{if next_extruder < 255}\nM400\n\nG92 E0\n{if flush_length_1 > 1}\n; FLUSH_START\n; always use highest temperature to flush\nM400\nM109 S[nozzle_temperature_range_high]\n{if flush_length_1 > 23.7}\nG1 E23.7 F{old_filament_e_feedrate} ; do not need pulsatile flushing for start part\nG1 E{(flush_length_1 - 23.7) * 0.02} F50\nG1 E{(flush_length_1 - 23.7) * 0.23} F{old_filament_e_feedrate}\nG1 E{(flush_length_1 - 23.7) * 0.02} F50\nG1 E{(flush_length_1 - 23.7) * 0.23} F{new_filament_e_feedrate}\nG1 E{(flush_length_1 - 23.7) * 0.02} F50\nG1 E{(flush_length_1 - 23.7) * 0.23} F{new_filament_e_feedrate}\nG1 E{(flush_length_1 - 23.7) * 0.02} F50\nG1 E{(flush_length_1 - 23.7) * 0.23} F{new_filament_e_feedrate}\n{else}\nG1 E{flush_length_1} F{old_filament_e_feedrate}\n{endif}\n; FLUSH_END\nG1 E-[old_retract_length_toolchange] F1800\nG1 E[old_retract_length_toolchange] F300\n{endif}\n\n{if flush_length_2 > 1}\n; FLUSH_START\nG1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_2 * 0.02} F50\nG1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_2 * 0.02} F50\nG1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_2 * 0.02} F50\nG1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_2 * 0.02} F50\nG1 E{flush_length_2 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_2 * 0.02} F50\n; FLUSH_END\nG1 E-[new_retract_length_toolchange] F1800\nG1 E[new_retract_length_toolchange] F300\n{endif}\n\n{if flush_length_3 > 1}\n; FLUSH_START\nG1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_3 * 0.02} F50\nG1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_3 * 0.02} F50\nG1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_3 * 0.02} F50\nG1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_3 * 0.02} F50\nG1 E{flush_length_3 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_3 * 0.02} F50\n; FLUSH_END\nG1 E-[new_retract_length_toolchange] F1800\nG1 E[new_retract_length_toolchange] F300\n{endif}\n\n{if flush_length_4 > 1}\n; FLUSH_START\nG1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_4 * 0.02} F50\nG1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_4 * 0.02} F50\nG1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_4 * 0.02} F50\nG1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_4 * 0.02} F50\nG1 E{flush_length_4 * 0.18} F{new_filament_e_feedrate}\nG1 E{flush_length_4 * 0.02} F50\n; FLUSH_END\n{endif}\n; FLUSH_START\nM400\nM109 S[new_filament_temp]\nG1 E2 F{new_filament_e_feedrate} ;Compensate for filament spillage during waiting temperature\n; FLUSH_END\nM400\nG92 E0\nG1 E-[new_retract_length_toolchange] F1800\nM106 P1 S255\nM400 S3\nG1 X80 F15000\nG1 X60 F15000\nG1 X80 F15000\nG1 X60 F15000; shake to put down garbage\n\nG1 X70 F5000\nG1 X90 F3000\nG1 Y255 F4000\nG1 X100 F5000\nG1 Y265 F5000\nG1 X70 F10000\nG1 X100 F5000\nG1 X70 F10000\nG1 X100 F5000\nG1 X165 F15000; wipe and shake\nG1 Y256 ; move Y to aside, prevent collision\nM400\nG1 Z{max_layer_z + 3.0} F3000\n{if layer_z <= (initial_layer_print_height + 0.001)}\nM204 S[initial_layer_acceleration]\n{else}\nM204 S[default_acceleration]\n{endif}\n{else}\nG1 X[x_after_toolchange] Y[y_after_toolchange] Z[z_after_toolchange] F12000\n{endif}\nM621 S[next_extruder]A
; circle_compensation_manual_offset = 0
; circle_compensation_speed = 200
; close_additional_fan_first_x_layers = 3
; close_fan_the_first_x_layers = 3
; compatible_printers_condition = 
; complete_print_exhaust_fan_speed = 70
; cool_plate_temp = 0
; cool_plate_temp_initial_layer = 0
; cooling_filter_enabled = 0
; cooling_perimeter_transition_distance = 10
; cooling_slowdown_logic = uniform_cooling
; counter_coef_1 = 0
; counter_coef_2 = 0.008
; counter_coef_3 = -0.041
; counter_limit_max = 0.033
; counter_limit_min = -0.035
; counterbore_hole_bridging = none
; curr_bed_type = Textured PEI Plate
; default_acceleration = 10000
; default_ams_type = -1
; default_filament_colour = ""
; default_filament_profile = "Bambu PLA Basic @BBL X1C"
; default_jerk = 0
; default_nozzle_volume_type = Standard
; default_print_profile = 0.20mm Standard @BBL X1C
; deretraction_speed = 30
; detect_floating_vertical_shell = 1
; detect_narrow_internal_solid_infill = 1
; detect_overhang_wall = 1
; detect_thin_wall = 0
; diameter_limit = 50
; different_settings_to_system = ;;
; draft_shield = disabled
; during_print_exhaust_fan_speed = 70
; elefant_foot_compensation = 0.15
; embedding_wall_into_infill = 0
; enable_arc_fitting = 1
; enable_circle_compensation = 0
; enable_filament_dynamic_map = 0
; enable_height_slowdown = 0
; enable_long_retraction_when_cut = 2
; enable_mixed_color_sublayer = 0
; enable_order_independent_overlap_carving = 0
; enable_overhang_bridge_fan = 1
; enable_overhang_speed = 1
; enable_pre_heating = 0
; enable_pressure_advance = 0
; enable_prime_tower = 1
; enable_support = 0
; enable_support_ironing = 0
; enable_tower_interface_features = 0
; enable_wrapping_detection = 0
; enforce_support_layers = 0
; eng_plate_temp = 70
; eng_plate_temp_initial_layer = 70
; ensure_vertical_shell_thickness = enabled
; exclude_object = 1
; extruder_ams_count = 
; extruder_clearance_dist_to_rod = 33
; extruder_clearance_height_to_lid = 90
; extruder_clearance_height_to_rod = 34
; extruder_clearance_max_radius = 68
; extruder_colour = #018001
; extruder_max_nozzle_count = 1
; extruder_nozzle_stats = 
; extruder_offset = 0x2
; extruder_printable_area = 
; extruder_type = Direct Drive
; extruder_variant_list = "Direct Drive Standard,Direct Drive High Flow"
; fan_cooling_layer_time = 30
; fan_direction = left
; fan_max_speed = 40
; fan_min_speed = 20
; farthest_point_timelapse = 1
; filament_adaptive_volumetric_speed = 0
; filament_adhesiveness_category = 300
; filament_bridge_speed = 25
; filament_change_length = 10
; filament_change_length_nc = 10
; filament_colour = #00AE42
; filament_cooling_before_tower = 0
; filament_cost = 17.99
; filament_density = 1.25
; filament_dev_ams_drying_ams_limitations = 1
; filament_dev_ams_drying_heat_distortion_temperature = 75
; filament_dev_ams_drying_temperature = 65
; filament_dev_ams_drying_time = 12
; filament_dev_chamber_drying_bed_temperature = 80
; filament_dev_chamber_drying_time = 12
; filament_dev_drying_cooling_temperature = 55
; filament_dev_drying_softening_temperature = 60
; filament_diameter = 1.75
; filament_enable_overhang_speed = 1
; filament_end_gcode = "; filament end gcode \n\n"
; filament_extruder_compatibility = 0
; filament_extruder_variant = "Direct Drive Standard"
; filament_flow_ratio = 0.95
; filament_flush_temp = 0
; filament_flush_temp_fast = 0
; filament_flush_volumetric_speed = 0
; filament_ids = GFG00
; filament_is_mixed = 0
; filament_is_support = 0
; filament_long_retractions_when_cut = 1
; filament_map = 1
; filament_map_2 = 0
; filament_map_mode = Auto For Flush
; filament_max_volumetric_speed = 15
; filament_metal_stickiness = High
; filament_minimal_purge_on_wipe_tower = 15
; filament_mixed_components = ""
; filament_mixed_gradient = 0
; filament_mixed_gradient_curve = ""
; filament_mixed_gradient_per_part = 0
; filament_mixed_gradient_range = ""
; filament_mixed_sublayer_ratios = ""
; filament_notes = 
; filament_nozzle_map = 0
; filament_overhang_1_4_speed = 0
; filament_overhang_2_4_speed = 50
; filament_overhang_3_4_speed = 30
; filament_overhang_4_4_speed = 10
; filament_overhang_totally_speed = 10
; filament_pre_cooling_temperature = 0
; filament_pre_cooling_temperature_nc = 0
; filament_preheat_temperature_delta = 0
; filament_prime_volume = 45
; filament_prime_volume_nc = 60
; filament_printable = 3
; filament_ramming_travel_time = 0
; filament_ramming_travel_time_nc = 0
; filament_ramming_volumetric_speed = -1
; filament_ramming_volumetric_speed_nc = -1
; filament_retract_length_nc = 14
; filament_retraction_distances_when_cut = 18
; filament_retraction_length = 0.4
; filament_scarf_gap = 0%
; filament_scarf_height = 10%
; filament_scarf_length = 10
; filament_scarf_seam_type = none
; filament_self_index = 1
; filament_settings_id = "Bambu PETG Basic @BBL X1C"
; filament_shrink = 100%
; filament_soluble = 0
; filament_start_gcode = "; filament start gcode\n{if (bed_temperature[current_extruder] >80)||(bed_temperature_initial_layer[current_extruder] >80)}M106 P3 S255\n{elsif (bed_temperature[current_extruder] >60)||(bed_temperature_initial_layer[current_extruder] >60)}M106 P3 S180\n{endif}\n\n{if activate_air_filtration[current_extruder] && support_air_filtration}\nM106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} \n{endif}"
; filament_tower_interface_pre_extrusion_dist = 10
; filament_tower_interface_pre_extrusion_length = 0
; filament_tower_interface_print_temp = -1
; filament_tower_interface_purge_volume = 20
; filament_tower_ironing_area = 4
; filament_type = PETG
; filament_velocity_adaptation_factor = 1
; filament_vendor = "Bambu Lab"
; filament_volume_map = 0
; filament_wipe = 1
; filament_wipe_distance = 1
; filament_z_hop_types = Spiral Lift
; filename_format = {input_filename_base}_{filament_type[0]}_{print_time}.gcode
; fill_multiline = 1
; filter_out_gap_fill = 0
; first_layer_print_sequence = 0
; first_x_layer_fan_speed = 0
; first_x_layer_part_fan_speed = 0
; flush_into_infill = 0
; flush_into_objects = 0
; flush_into_support = 1
; flush_multiplier = 1
; flush_multiplier_fast = 1.2
; flush_volumes_matrix = 0,280,280,280,280,0,280,280,280,280,0,280,280,280,280,0
; flush_volumes_vector = 140,140,140,140,140,140,140,140
; full_fan_speed_layer = 0
; fuzzy_skin = none
; fuzzy_skin_first_layer = 0
; fuzzy_skin_mode = displacement
; fuzzy_skin_noise_type = classic
; fuzzy_skin_octaves = 4
; fuzzy_skin_persistence = 0.5
; fuzzy_skin_point_distance = 0.8
; fuzzy_skin_scale = 1
; fuzzy_skin_thickness = 0.3
; gap_infill_speed = 250
; gcode_add_line_number = 0
; gcode_flavor = marlin
; grab_length = 0
; group_algo_with_time = 0
; has_filament_switcher = 0
; has_scarf_joint_seam = 0
; head_wrap_detect_zone = 
; hole_coef_1 = 0
; hole_coef_2 = -0.008
; hole_coef_3 = 0.23415
; hole_limit_max = 0.22
; hole_limit_min = 0.088
; hot_plate_temp = 70
; hot_plate_temp_initial_layer = 70
; hotend_cooling_rate = 2
; hotend_heating_rate = 2
; impact_strength_z = 13.6
; independent_support_layer_height = 1
; infill_combination = 0
; infill_direction = 0
; infill_instead_top_bottom_surfaces = 0
; infill_jerk = 9
; infill_lock_depth = 1
; infill_rotate_step = 0
; infill_shift_step = 0.4
; infill_wall_overlap = 15%
; inherits_group = ;;
; initial_layer_acceleration = 500
; initial_layer_flow_ratio = 1
; initial_layer_infill_speed = 105
; initial_layer_jerk = 9
; initial_layer_line_width = 0.5
; initial_layer_print_height = 0.2
; initial_layer_speed = 50
; initial_layer_travel_acceleration = 6000
; inner_wall_acceleration = 0
; inner_wall_jerk = 9
; inner_wall_line_width = 0.45
; inner_wall_speed = 300
; interface_shells = 0
; interlocking_beam = 0
; interlocking_beam_layer_count = 2
; interlocking_beam_width = 0.8
; interlocking_boundary_avoidance = 2
; interlocking_depth = 2
; interlocking_orientation = 22.5
; internal_bridge_support_thickness = 0.8
; internal_solid_infill_line_width = 0.42
; internal_solid_infill_pattern = zig-zag
; internal_solid_infill_speed = 250
; ironing_direction = 45
; ironing_fan_speed = -1
; ironing_flow = 10%
; ironing_inset = 0.21
; ironing_pattern = zig-zag
; ironing_spacing = 0.15
; ironing_speed = 30
; ironing_type = no ironing
; is_infill_first = 0
; layer_change_gcode = ; layer num/total_layer_count: {layer_num+1}/[total_layer_count]\n; update layer progress\nM73 L{layer_num+1}\nM991 S0 P{layer_num} ;notify layer change
; layer_height = 0.2
; line_width = 0.42
; locked_skeleton_infill_pattern = zigzag
; locked_skin_infill_pattern = crosszag
; long_retractions_when_cut = 0
; long_retractions_when_ec = 0
; machine_bed_mass_Y = 0
; machine_end_gcode = ;===== date: 20230428 =====================\nM400 ; wait for buffer to clear\nG92 E0 ; zero the extruder\nG1 E-0.8 F1800 ; retract\nG1 Z{max_layer_z + 0.5} F900 ; lower z a little\nG1 X65 Y245 F12000 ; move to safe pos \nG1 Y265 F3000\n\nG1 X65 Y245 F12000\nG1 Y265 F3000\nM140 S0 ; turn off bed\nM106 S0 ; turn off fan\nM106 P2 S0 ; turn off remote part cooling fan\nM106 P3 S0 ; turn off chamber cooling fan\n\nG1 X100 F12000 ; wipe\n; pull back filament to AMS\nM620 S255\nG1 X20 Y50 F12000\nG1 Y-3\nT255\nG1 X65 F12000\nG1 Y265\nG1 X100 F12000 ; wipe\nM621 S255\nM104 S0 ; turn off hotend\n\nM622.1 S1 ; for prev firmware, default turned on\nM1002 judge_flag timelapse_record_flag\nM622 J1\n    M400 ; wait all motion done\n    M991 S0 P-1 ;end smooth timelapse at safe pos\n    M400 S3 ;wait for last picture to be taken\nM623; end of \"timelapse_record_flag\"\n\nM400 ; wait all motion done\nM17 S\nM17 Z0.4 ; lower z motor current to reduce impact if there is something in the bottom\n{if (max_layer_z + 100.0) < 250}\n    G1 Z{max_layer_z + 100.0} F600\n    G1 Z{max_layer_z +98.0}\n{else}\n    G1 Z250 F600\n    G1 Z248\n{endif}\nM400 P100\nM17 R ; restore z current\n\nG90\nG1 X128 Y250 F3600\n\nM220 S100  ; Reset feedrate magnitude\nM201.2 K1.0 ; Reset acc magnitude\nM73.2   R1.0 ;Reset left time magnitude\nM1002 set_gcode_claim_speed_level : 0\n\nM17 X0.8 Y0.8 Z0.5 ; lower motor current to 45% power\n
; machine_hotend_change_time = 0
; machine_load_filament_time = 29
; machine_max_acceleration_e = 5000,5000
; machine_max_acceleration_extruding = 20000,20000
; machine_max_acceleration_retracting = 5000,5000
; machine_max_acceleration_travel = 9000,9000
; machine_max_acceleration_x = 20000,20000
; machine_max_acceleration_y = 20000,20000
; machine_max_acceleration_z = 500,500
; machine_max_force_Y = 0
; machine_max_jerk_e = 2.5,2.5
; machine_max_jerk_x = 9,9
; machine_max_jerk_y = 9,9
; machine_max_jerk_z = 3,3
; machine_max_printed_mass = 0
; machine_max_speed_e = 30,30
; machine_max_speed_x = 500,500
; machine_max_speed_y = 500,500
; machine_max_speed_z = 20,20
; machine_min_extruding_rate = 0
; machine_min_travel_rate = 0
; machine_pause_gcode = M400 U1
; machine_prepare_compensation_time = 260
; machine_start_gcode = G0 Z20 F9000\nG92 E0; G1 E-10 F1200\nG28\nM970 Q1 A10 B10 C130 K0\nM970 Q1 A10 B131 C250 K1\nM974 Q1 S1 P0\nM970 Q0 A10 B10 C130 H20 K0\nM970 Q0 A10 B131 C250 K1\nM974 Q0 S1 P0\nM220 S100 ;Reset Feedrate\nM221 S100 ;Reset Flowrate\nG29 ;Home\nG90;\nG92 E0 ;Reset Extruder \nG1 Z2.0 F3000 ;Move Z Axis up \nG1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position\nM109 S205;\nG1 X10.1 Y200.0 Z0.28 F1500.0 E15 ;Draw the first line\nG1 X10.4 Y200.0 Z0.28 F5000.0 ;Move to side a little\nG1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line\nG92 E0 ;Reset Extruder \nG1 X110 Y110 Z2.0 F3000 ;Move Z Axis up
; machine_switch_extruder_time = 0
; machine_unload_filament_time = 28
; master_extruder_id = 1
; max_bridge_length = 0
; max_layer_height = 0.28
; max_travel_detour_distance = 0
; min_bead_width = 85%
; min_feature_size = 25%
; min_layer_height = 0.08
; minimum_sparse_infill_area = 15
; mmu_segmented_region_interlocking_depth = 0
; mmu_segmented_region_max_width = 0
; monotonic_travel_into_wall = 0%
; no_slow_down_for_cooling_on_outwalls = 0
; nozzle_diameter = 0.4
; nozzle_flush_dataset = 0
; nozzle_height = 4.2
; nozzle_temperature = 255
; nozzle_temperature_initial_layer = 245
; nozzle_temperature_range_high = 270
; nozzle_temperature_range_low = 230
; nozzle_type = hardened_steel
; nozzle_volume = 107
; nozzle_volume_type = Standard
; only_one_wall_first_layer = 0
; ooze_prevention = 0
; other_layers_print_sequence = 0
; other_layers_print_sequence_nums = 0
; outer_wall_acceleration = 5000
; outer_wall_jerk = 9
; outer_wall_line_width = 0.42
; outer_wall_speed = 200
; overhang_1_4_speed = 0
; overhang_2_4_speed = 50
; overhang_3_4_speed = 30
; overhang_4_4_speed = 10
; overhang_fan_speed = 50
; overhang_fan_threshold = 10%
; overhang_threshold_participating_cooling = 95%
; overhang_totally_speed = 10
; override_filament_scarf_seam_setting = 0
; override_process_overhang_speed = 0
; physical_extruder_map = 0
; post_process = 
; pre_start_fan_time = 2
; precise_outer_wall = 0
; precise_z_height = 0
; pressure_advance = 0.02
; prime_tower_brim_width = 3
; prime_tower_enable_framework = 0
; prime_tower_extra_rib_length = 0
; prime_tower_fillet_wall = 1
; prime_tower_flat_ironing = 0
; prime_tower_infill_gap = 150%
; prime_tower_lift_height = -1
; prime_tower_lift_speed = 90
; prime_tower_max_speed = 90
; prime_tower_rib_wall = 1
; prime_tower_rib_width = 8
; prime_tower_skip_points = 1
; prime_tower_width = 35
; prime_volume_mode = Default
; print_compatible_printers = "Bambu Lab X1 Carbon 0.4 nozzle";"Bambu Lab X1 0.4 nozzle";"Bambu Lab P1S 0.4 nozzle";"Bambu Lab X1E 0.4 nozzle"
; print_extruder_id = 1
; print_extruder_variant = "Direct Drive Standard"
; print_flow_ratio = 1
; print_in_clockwise = 0
; print_sequence = by layer
; print_settings_id = 0.20mm Standard @BBL X1C
; printable_area = 0x0,256x0,256x256,0x256
; printable_height = 250
; printer_extruder_id = 1
; printer_extruder_variant = "Direct Drive Standard"
; printer_model = Bambu Lab X1 Carbon
; printer_notes = 
; printer_settings_id = Bambu Lab X1 Carbon 0.4 nozzle
; printer_structure = corexy
; printer_technology = FFF
; printer_variant = 0.4
; printing_by_object_gcode = 
; process_notes = 
; raft_contact_distance = 0.1
; raft_expansion = 1.5
; raft_first_layer_density = 90%
; raft_first_layer_expansion = -1
; raft_layers = 0
; reduce_crossing_wall = 0
; reduce_fan_stop_start_freq = 1
; reduce_infill_retraction_mode = Auto
; required_nozzle_HRC = 3
; resolution = 0.012
; retract_before_wipe = 0%
; retract_length_toolchange = 2
; retract_lift_above = 0
; retract_lift_below = 249
; retract_restart_extra = 0
; retract_restart_extra_toolchange = 0
; retract_when_changing_layer = 1
; retraction_distances_when_cut = 18
; retraction_distances_when_ec = 0
; retraction_length = 0.8
; retraction_minimum_travel = 1
; retraction_speed = 30
; role_base_wipe_speed = 1
; scan_first_layer = 1
; scarf_angle_threshold = 155
; seam_gap = 15%
; seam_placement_away_from_overhangs = 0
; seam_position = aligned
; seam_slope_conditional = 1
; seam_slope_entire_loop = 0
; seam_slope_gap = 0
; seam_slope_inner_walls = 1
; seam_slope_min_length = 10
; seam_slope_start_height = 10%
; seam_slope_steps = 10
; seam_slope_type = none
; silent_mode = 0
; single_extruder_multi_material = 1
; skeleton_infill_density = 15%
; skeleton_infill_line_width = 0.45
; skin_infill_density = 15%
; skin_infill_depth = 2
; skin_infill_line_width = 0.45
; skirt_distance = 2
; skirt_height = 1
; skirt_loops = 0
; skirt_per_object = 1
; slice_closing_radius = 0.049
; slicing_mode = regular
; slow_down_for_layer_cooling = 1
; slow_down_layer_time = 12
; slow_down_min_speed = 10
; slowdown_end_acc = 100000
; slowdown_end_height = 400
; slowdown_end_speed = 1000
; slowdown_start_acc = 100000
; slowdown_start_height = 0
; slowdown_start_speed = 1000
; small_perimeter_speed = 50%
; small_perimeter_threshold = 0
; smooth_coefficient = 150
; smooth_speed_discontinuity_area = 1
; solid_infill_filament = 0
; sparse_infill_acceleration = 100%
; sparse_infill_anchor = 400%
; sparse_infill_anchor_max = 20
; sparse_infill_density = 100%
; sparse_infill_filament = 0
; sparse_infill_lattice_angle_1 = -45
; sparse_infill_lattice_angle_2 = 45
; sparse_infill_line_width = 0.45
; sparse_infill_pattern = alignedrectilinear
; sparse_infill_speed = 270
; spiral_mode = 0
; spiral_mode_max_xy_smoothing = 200%
; spiral_mode_smooth = 0
; standby_temperature_delta = -5
; start_end_points = 30x-3,54x245
; supertack_plate_temp = 70
; supertack_plate_temp_initial_layer = 70
; support_air_filtration = 0
; support_angle = 0
; support_base_pattern = default
; support_base_pattern_spacing = 2.5
; support_bottom_interface_spacing = 0.5
; support_bottom_z_distance = 0.2
; support_chamber_temp_control = 0
; support_cooling_filter = 0
; support_critical_regions_only = 0
; support_expansion = 0
; support_fast_purge_mode = 0
; support_filament = 0
; support_interface_bottom_layers = 2
; support_interface_filament = 0
; support_interface_loop_pattern = 0
; support_interface_not_for_body = 1
; support_interface_pattern = auto
; support_interface_spacing = 0.5
; support_interface_speed = 80
; support_interface_top_layers = 2
; support_ironing_direction = 0
; support_ironing_flow = 10%
; support_ironing_inset = 0
; support_ironing_pattern = zig-zag
; support_ironing_spacing = 0.15
; support_ironing_speed = 30
; support_line_width = 0.42
; support_object_first_layer_gap = 0.2
; support_object_skip_flush = 0
; support_object_xy_distance = 0.35
; support_on_build_plate_only = 1
; support_remove_small_overhang = 1
; support_speed = 150
; support_style = default
; support_threshold_angle = 45
; support_top_z_distance = 0.2
; support_type = tree(auto)
; symmetric_infill_y_axis = 0
; temperature_vitrification = 60
; template_custom_gcode = 
; textured_plate_temp = 70
; textured_plate_temp_initial_layer = 70
; thick_bridges = 0
; thumbnail_size = 50x50
; time_lapse_gcode = ;========Date 20250206========\nM622.1 S1 ; for prev firmware, default turned on\nM1002 judge_flag timelapse_record_flag\nM622 J1\n{if timelapse_type == 0} ; timelapse without wipe tower\nM971 S11 C10 O0\n{elsif timelapse_type == 1} ; timelapse with wipe tower\nG92 E0\nG1 X65 Y245 F20000 ; move to safe pos\nG17\nG2 Z{layer_z} I0.86 J0.86 P1 F20000\nG1 Y265 F3000\nM400 P300\nM971 S11 C10 O0\nG92 E0\nG1 X100 F5000\nG1 Y255 F20000\n{endif}\nM623\n
; timelapse_type = 0
; top_area_threshold = 200%
; top_color_penetration_layers = 5
; top_one_wall_type = all top
; top_shell_layers = 5
; top_shell_thickness = 1
; top_solid_infill_flow_ratio = 1
; top_surface_acceleration = 2000
; top_surface_density = 100%
; top_surface_jerk = 9
; top_surface_line_width = 0.42
; top_surface_pattern = monotonicline
; top_surface_speed = 200
; top_z_overrides_xy_distance = 0
; travel_acceleration = 10000
; travel_jerk = 9
; travel_short_distance_acceleration = 250
; travel_speed = 500
; travel_speed_z = 0
; tree_support_branch_angle = 45
; tree_support_branch_diameter = 2
; tree_support_branch_diameter_angle = 5
; tree_support_branch_distance = 5
; tree_support_wall_count = -1
; upward_compatible_machine = "Bambu Lab P1S 0.4 nozzle";"Bambu Lab P1P 0.4 nozzle";"Bambu Lab X1 0.4 nozzle";"Bambu Lab X1E 0.4 nozzle";"Bambu Lab A1 0.4 nozzle";"Bambu Lab H2D 0.4 nozzle";"Bambu Lab H2D Pro 0.4 nozzle";"Bambu Lab H2S 0.4 nozzle";"Bambu Lab P2S 0.4 nozzle";"Bambu Lab H2C 0.4 nozzle";"Bambu Lab X2D 0.4 nozzle";"Bambu Lab A2L 0.4 nozzle"
; use_firmware_retraction = 0
; use_relative_e_distances = 1
; vertical_shell_speed = 80%
; volumetric_speed_coefficients = "0 0 0 0 0 0"
; wall_distribution_count = 1
; wall_filament = 0
; wall_generator = classic
; wall_loops = 8
; wall_sequence = inner wall/outer wall
; wall_transition_angle = 10
; wall_transition_filter_deviation = 25%
; wall_transition_length = 100%
; wipe = 1
; wipe_distance = 2
; wipe_speed = 80%
; wipe_tower_no_sparse_layers = 0
; wipe_tower_rotation_angle = 0
; wipe_tower_x = 15
; wipe_tower_y = 220
; wrapping_detection_gcode = 
; wrapping_detection_layers = 20
; wrapping_exclude_area = 
; xy_contour_compensation = 0
; xy_hole_compensation = 0
; z_direction_outwall_speed_continuous = 0
; z_hop = 0.4
; z_hop_types = Auto Lift
; CONFIG_BLOCK_END

; EXECUTABLE_BLOCK_START
M73 P0 R13
M201 X20000 Y20000 Z500 E5000
M203 X500 Y500 Z20 E30
M204 P20000 R5000 T20000
M205 X9.00 Y9.00 Z3.00 E2.50
M106 S0
M106 P2 S0
M190 S70 ; set bed temperature and wait for it to be reached
; FEATURE: Custom
G0 Z20 F9000
G92 E0; G1 E-10 F1200
G28
M970 Q1 A10 B10 C130 K0
M970 Q1 A10 B131 C250 K1
M974 Q1 S1 P0
M970 Q0 A10 B10 C130 H20 K0
M970 Q0 A10 B131 C250 K1
M974 Q0 S1 P0
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate
G29 ;Home
G90;
G92 E0 ;Reset Extruder 
G1 Z2.0 F3000 ;Move Z Axis up 
G1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position
M109 S205;
G1 X10.1 Y200.0 Z0.28 F1500.0 E15 ;Draw the first line
G1 X10.4 Y200.0 Z0.28 F5000.0 ;Move to side a little
G1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line
G92 E0 ;Reset Extruder 
M73 P1 R12
G1 X110 Y110 Z2.0 F3000 ;Move Z Axis up
; MACHINE_START_GCODE_END
; filament start gcode
M106 P3 S180


;VT0 H-1
G90
G21
M83 ; use relative distances for extrusion
M981 S1 P20000 ;open spaghetti detector
; CHANGE_LAYER
; Z_HEIGHT: 0.2
; LAYER_HEIGHT: 0.2
G1 E-.4 F1800
; layer num/total_layer_count: 1/50
; update layer progress
M73 L1
M991 S0 P0 ;notify layer change
M106 S0
M106 P2 S0
; OBJECT_ID: 15
M73 P2 R12
G1 X120.327 Y116.346 F30000
M204 S6000
G1 Z.4
G1 Z.2
G1 E.4 F1800
; FEATURE: Brim
; LINE_WIDTH: 0.5
G1 F3000
M204 S500
G1 X120.828 Y115.888 E.0245
G1 X121.581 Y115.347 E.03348
G1 X122.178 Y115.014 E.02467
G1 X122.803 Y114.743 E.0246
G1 X123.453 Y114.534 E.02466
G1 X123.871 Y114.435 E.01553
G1 X124.547 Y114.333 E.02466
G1 X125.225 Y114.297 E.02452
G1 X126.152 Y114.356 E.03355
G1 X126.579 Y114.425 E.01561
G1 X127.242 Y114.589 E.02467
G1 X127.923 Y114.832 E.02608
G1 X128.077 Y114.832 E.00556
G1 X128.733 Y114.597 E.02516
G1 X129.393 Y114.431 E.02458
G1 X130.069 Y114.331 E.02467
G1 X130.498 Y114.302 E.01553
G1 X131.181 Y114.31 E.02466
G1 X131.861 Y114.386 E.02473
G1 X132.763 Y114.595 E.03343
G1 X133.171 Y114.733 E.01554
G1 X133.799 Y115.003 E.02465
G1 X134.397 Y115.333 E.02468
G1 X135.152 Y115.872 E.03348
G1 X135.655 Y116.328 E.02453
G1 X136.114 Y116.833 E.02465
G1 X136.376 Y117.174 E.01553
G1 X136.748 Y117.747 E.02466
G1 X137.062 Y118.352 E.02461
G1 X137.314 Y118.984 E.02457
G1 X137.503 Y119.638 E.02459
G1 X137.633 Y120.349 E.02608
G1 X137.713 Y120.485 E.0057
G1 X138.057 Y120.766 E.01603
G1 X138.549 Y121.239 E.02465
G1 X139.137 Y121.952 E.03337
G1 X139.508 Y122.527 E.02472
G1 X139.821 Y123.135 E.02465
G1 X139.986 Y123.532 E.01554
G1 X140.197 Y124.182 E.02466
G1 X140.344 Y124.85 E.02472
G1 X140.424 Y125.526 E.02455
G1 X140.437 Y126.207 E.02459
G1 X140.383 Y126.883 E.02449
G1 X140.205 Y127.79 E.03337
G1 X139.996 Y128.442 E.02472
G1 X139.725 Y129.068 E.02466
G1 X139.523 Y129.448 E.01554
G1 X139.153 Y130.026 E.02478
G1 X138.734 Y130.557 E.02439
G1 X138.261 Y131.049 E.02465
G1 X137.71 Y131.517 E.0261
G1 X137.633 Y131.65 E.00556
G1 X137.509 Y132.338 E.02524
G1 X137.398 Y132.754 E.01553
G1 X137.17 Y133.397 E.02465
G1 X136.881 Y134.014 E.0246
G1 X136.531 Y134.603 E.02472
G1 X136.13 Y135.146 E.02439
G1 X135.674 Y135.654 E.02465
G1 X135.17 Y136.113 E.02459
G1 X134.625 Y136.521 E.0246
G1 X133.824 Y136.985 E.03343
G1 X133.429 Y137.165 E.01566
G1 X132.787 Y137.397 E.02466
G1 X132.126 Y137.565 E.02459
G1 X131.453 Y137.667 E.02459
G1 X130.773 Y137.703 E.02458
G1 X130.092 Y137.672 E.02461
G1 X129.415 Y137.573 E.02473
G1 X128.755 Y137.41 E.02454
G1 X128.077 Y137.168 E.02598
G1 X127.919 Y137.169 E.0057
G1 X127.504 Y137.327 E.01603
G1 X126.848 Y137.516 E.02466
G1 X126.178 Y137.641 E.0246
G1 X125.5 Y137.698 E.02457
G1 X124.819 Y137.69 E.0246
G1 X124.142 Y137.614 E.02459
G1 X123.476 Y137.472 E.02459
G1 X122.6 Y137.177 E.03338
G1 X121.979 Y136.884 E.02479
G1 X121.603 Y136.667 E.01569
G1 X121.043 Y136.282 E.02453
G1 X120.344 Y135.671 E.03353
G1 X119.883 Y135.162 E.02479
G1 X119.48 Y134.62 E.0244
G1 X119.253 Y134.255 E.01553
G1 X118.841 Y133.425 E.03346
G1 X118.609 Y132.779 E.02477
G1 X118.497 Y132.364 E.01554
G1 X118.367 Y131.651 E.02616
G1 X118.29 Y131.518 E.00556
G1 X117.758 Y131.067 E.02517
G1 X117.285 Y130.578 E.02457
G1 X116.857 Y130.039 E.02487
G1 X116.49 Y129.471 E.0244
G1 X116.287 Y129.092 E.01552
G1 X116.013 Y128.466 E.02466
G1 X115.803 Y127.818 E.02459
G1 X115.657 Y127.154 E.02457
G1 X115.577 Y126.477 E.02461
G1 X115.563 Y125.792 E.02471
G1 X115.652 Y124.873 E.03337
G1 X115.796 Y124.207 E.02459
G1 X116.004 Y123.558 E.02459
G1 X116.275 Y122.932 E.02466
G1 X116.479 Y122.549 E.01566
G1 X116.992 Y121.778 E.03343
G1 X117.434 Y121.257 E.02467
G1 X117.737 Y120.952 E.01553
G1 X118.29 Y120.483 E.02616
G1 X118.367 Y120.35 E.00556
G1 X118.491 Y119.664 E.02516
G1 X118.678 Y119.009 E.02459
G1 X118.928 Y118.374 E.02465
G1 X119.118 Y117.988 E.01554
G1 X119.467 Y117.401 E.02465
G1 X119.871 Y116.852 E.0246
G1 X120.287 Y116.39 E.02243
M204 S6000
G1 X120.626 Y116.697 F30000
G1 F3000
M204 S500
G1 X120.656 Y116.664 E.00161
G1 X121.111 Y116.249 E.0222
G1 X121.82 Y115.738 E.03157
G1 X122.374 Y115.428 E.02294
G1 X122.97 Y115.169 E.02346
G1 X123.581 Y114.973 E.02314
G1 X123.964 Y114.884 E.01421
G1 X124.586 Y114.789 E.02274
G1 X125.23 Y114.756 E.02328
G1 X126.094 Y114.81 E.03126
G1 X126.482 Y114.873 E.01417
G1 X127.104 Y115.026 E.02312
G1 X127.758 Y115.259 E.02507
G1 X127.935 Y115.289 E.00649
G1 X128.065 Y115.289 E.00471
G1 X128.242 Y115.258 E.00649
G1 X128.872 Y115.033 E.02416
G1 X129.489 Y114.879 E.02296
G1 X130.112 Y114.786 E.02275
G1 X130.505 Y114.759 E.01421
G1 X131.159 Y114.768 E.02362
G1 X131.792 Y114.84 E.023
G1 X132.645 Y115.038 E.03162
G1 X133.013 Y115.162 E.01403
G1 X133.591 Y115.411 E.02273
G1 X134.146 Y115.716 E.02287
G1 X134.858 Y116.224 E.03157
G1 X135.327 Y116.647 E.0228
G1 X135.759 Y117.123 E.02322
G1 X136.006 Y117.443 E.0146
G1 X136.356 Y117.983 E.02323
G1 X136.648 Y118.549 E.02299
G1 X136.879 Y119.126 E.02246
G1 X137.056 Y119.737 E.02294
G1 X137.181 Y120.419 E.02506
G1 X137.245 Y120.592 E.00665
G1 X137.313 Y120.707 E.00482
G1 X137.433 Y120.847 E.00665
G1 X137.758 Y121.112 E.01513
G1 X138.208 Y121.545 E.02254
G1 X138.763 Y122.216 E.03145
G1 X139.115 Y122.762 E.02348
G1 X139.403 Y123.322 E.02273
G1 X139.559 Y123.696 E.01462
G1 X139.757 Y124.308 E.02323
G1 X139.894 Y124.933 E.0231
G1 X139.967 Y125.564 E.02293
G1 X139.979 Y126.2 E.02297
G1 X139.928 Y126.829 E.02278
G1 X139.763 Y127.668 E.03087
G1 X139.57 Y128.274 E.02299
G1 X139.31 Y128.875 E.02362
G1 X139.125 Y129.222 E.01421
G1 X138.783 Y129.755 E.02286
G1 X138.393 Y130.251 E.02277
G1 X137.952 Y130.711 E.023
G1 X137.423 Y131.161 E.02509
G1 X137.308 Y131.299 E.00649
G1 X137.243 Y131.412 E.00471
G1 X137.181 Y131.581 E.00649
G1 X137.061 Y132.244 E.02435
G1 X136.959 Y132.624 E.01419
G1 X136.744 Y133.23 E.02322
G1 X136.473 Y133.806 E.02297
G1 X136.153 Y134.344 E.02261
G1 X135.771 Y134.862 E.02325
G1 X135.344 Y135.336 E.02304
G1 X134.884 Y135.756 E.02248
G1 X134.379 Y136.134 E.02279
G1 X133.608 Y136.581 E.03219
G1 X133.251 Y136.743 E.01414
G1 X132.659 Y136.958 E.02274
G1 X132.042 Y137.115 E.02297
G1 X131.413 Y137.211 E.02297
G1 X130.778 Y137.245 E.02296
G1 X130.143 Y137.216 E.02298
G1 X129.496 Y137.122 E.02359
G1 X128.88 Y136.969 E.02291
G1 X128.243 Y136.741 E.02445
G1 X128.061 Y136.711 E.00666
G1 X127.927 Y136.712 E.00482
G1 X127.746 Y136.746 E.00666
G1 X127.354 Y136.894 E.01512
G1 X126.749 Y137.069 E.02273
G1 X126.124 Y137.186 E.02297
G1 X125.491 Y137.24 E.02295
G1 X124.854 Y137.233 E.02297
G1 X124.209 Y137.161 E.02345
G1 X123.59 Y137.028 E.02287
G1 X122.779 Y136.755 E.03088
G1 X122.187 Y136.476 E.02365
G1 X121.842 Y136.277 E.01436
G1 X121.33 Y135.925 E.02243
G1 X120.671 Y135.35 E.0316
G1 X120.241 Y134.877 E.02306
G1 X119.862 Y134.367 E.02297
G1 X119.649 Y134.026 E.0145
G1 X119.259 Y133.238 E.03173
G1 X119.044 Y132.637 E.02306
G1 X118.942 Y132.257 E.01419
G1 X118.819 Y131.581 E.02484
G1 X118.757 Y131.412 E.00649
G1 X118.692 Y131.299 E.00471
G1 X118.576 Y131.161 E.00649
G1 X118.076 Y130.737 E.02368
G1 X117.633 Y130.281 E.02294
G1 X117.233 Y129.777 E.02324
G1 X116.887 Y129.243 E.02298
G1 X116.701 Y128.897 E.0142
G1 X116.439 Y128.297 E.02363
G1 X116.246 Y127.705 E.02249
G1 X116.109 Y127.084 E.02295
G1 X116.033 Y126.439 E.02347
G1 X116.021 Y125.802 E.02299
G1 X116.104 Y124.951 E.03087
G1 X116.24 Y124.319 E.02335
G1 X116.435 Y123.713 E.02297
G1 X116.69 Y123.125 E.02314
G1 X116.876 Y122.778 E.01423
G1 X117.354 Y122.06 E.03113
G1 X117.767 Y121.571 E.02313
G1 X118.044 Y121.292 E.01417
G1 X118.577 Y120.839 E.02526
G1 X118.692 Y120.701 E.00648
G1 X118.757 Y120.588 E.00471
G1 X118.819 Y120.42 E.00649
G1 X118.938 Y119.761 E.02416
G1 X119.113 Y119.15 E.02296
G1 X119.349 Y118.554 E.02313
G1 X119.523 Y118.201 E.01421
G1 X119.845 Y117.66 E.02273
G1 X120.23 Y117.136 E.02347
G1 X120.586 Y116.741 E.01919
M204 S6000
G1 X120.926 Y117.048 F30000
G1 F3000
M204 S500
G1 X120.976 Y116.991 E.00274
G1 X121.394 Y116.61 E.02041
G1 X122.059 Y116.129 E.02966
G1 X122.571 Y115.841 E.0212
G1 X123.126 Y115.6 E.02182
G1 X123.708 Y115.413 E.0221
G1 X124.055 Y115.332 E.01287
G1 X124.626 Y115.245 E.02084
G1 X125.236 Y115.214 E.02204
G1 X126.037 Y115.265 E.02898
G1 X126.385 Y115.32 E.01273
G1 X126.977 Y115.466 E.02201
G1 X127.691 Y115.711 E.02724
G1 X128.056 Y115.746 E.01326
G1 X128.407 Y115.685 E.01286
G1 X128.999 Y115.473 E.02268
G1 X129.585 Y115.327 E.02183
G1 X130.156 Y115.242 E.02085
G1 X130.512 Y115.217 E.01287
G1 X131.137 Y115.225 E.02257
G1 X131.722 Y115.293 E.02126
G1 X132.526 Y115.48 E.02981
G1 X132.854 Y115.592 E.01251
G1 X133.384 Y115.819 E.02084
G1 X133.895 Y116.1 E.02106
G1 X134.565 Y116.576 E.02966
G1 X134.999 Y116.967 E.02107
G1 X135.405 Y117.412 E.02177
G1 X135.636 Y117.712 E.01366
G1 X135.963 Y118.219 E.02179
G1 X136.229 Y118.733 E.02088
G1 X136.443 Y119.269 E.02086
G1 X136.612 Y119.849 E.02179
G1 X136.729 Y120.49 E.02354
G1 X136.857 Y120.832 E.01319
G1 X136.973 Y121.012 E.00772
G1 X137.08 Y121.136 E.00592
G1 X137.458 Y121.458 E.01793
G1 X137.866 Y121.851 E.02045
G1 X138.388 Y122.481 E.02953
G1 X138.722 Y122.997 E.02223
G1 X138.986 Y123.51 E.02081
G1 X139.131 Y123.86 E.01368
G1 X139.317 Y124.434 E.02179
G1 X139.443 Y125.015 E.02147
M73 P3 R12
G1 X139.511 Y125.601 E.0213
G1 X139.521 Y126.192 E.02135
G1 X139.473 Y126.774 E.02107
G1 X139.321 Y127.546 E.02841
G1 X139.139 Y128.12 E.02175
G1 X138.895 Y128.681 E.02208
G1 X138.727 Y128.996 E.01288
G1 X138.414 Y129.485 E.02097
G1 X138.052 Y129.945 E.02115
G1 X137.633 Y130.382 E.02185
G1 X137.136 Y130.805 E.02357
G1 X136.908 Y131.079 E.01286
G1 X136.756 Y131.413 E.01326
G1 X136.613 Y132.149 E.02708
G1 X136.521 Y132.493 E.01286
G1 X136.318 Y133.062 E.0218
G1 X136.072 Y133.585 E.02087
G1 X135.775 Y134.085 E.02099
G1 X135.421 Y134.567 E.02162
G1 X135.015 Y135.018 E.02189
G1 X134.587 Y135.407 E.02088
G1 X134.133 Y135.747 E.02049
G1 X133.392 Y136.178 E.03094
G1 X133.073 Y136.322 E.01261
G1 X132.531 Y136.518 E.02084
G1 X131.958 Y136.665 E.02136
G1 X131.373 Y136.755 E.02135
G1 X130.783 Y136.787 E.02134
G1 X130.193 Y136.761 E.02134
G1 X129.591 Y136.674 E.02195
G1 X129.019 Y136.533 E.02126
G1 X128.307 Y136.289 E.02718
G1 X128.146 Y136.262 E.00591
G1 X127.932 Y136.255 E.00772
G1 X127.573 Y136.323 E.01319
G1 X127.205 Y136.462 E.01423
G1 X126.65 Y136.622 E.02083
G1 X126.069 Y136.731 E.02136
G1 X125.48 Y136.783 E.02133
G1 X124.889 Y136.776 E.02134
G1 X124.289 Y136.71 E.0218
G1 X123.703 Y136.584 E.02164
G1 X122.958 Y136.333 E.02841
G1 X122.394 Y136.068 E.0225
G1 X122.082 Y135.887 E.01301
G1 X121.618 Y135.568 E.02035
G1 X120.997 Y135.028 E.02969
G1 X120.599 Y134.591 E.02133
G1 X120.243 Y134.113 E.02153
G1 X120.046 Y133.797 E.01346
G1 X119.678 Y133.052 E.03
G1 X119.48 Y132.495 E.02134
G1 X119.388 Y132.151 E.01285
G1 X119.271 Y131.51 E.02353
G1 X119.148 Y131.175 E.01288
G1 X118.934 Y130.876 E.01326
G1 X118.384 Y130.398 E.02633
G1 X117.973 Y129.974 E.02132
G1 X117.609 Y129.516 E.02112
G1 X117.284 Y129.015 E.02156
G1 X117.115 Y128.701 E.01286
G1 X116.865 Y128.128 E.02259
G1 X116.686 Y127.578 E.02087
G1 X116.56 Y127.001 E.02133
G1 X116.49 Y126.414 E.02134
G1 X116.479 Y125.828 E.02117
G1 X116.558 Y125.014 E.02954
G1 X116.681 Y124.444 E.02105
G1 X116.861 Y123.881 E.02134
G1 X117.1 Y123.329 E.0217
G1 X117.265 Y123.018 E.01272
G1 X117.725 Y122.329 E.02991
G1 X118.108 Y121.876 E.02144
G1 X118.359 Y121.624 E.01282
G1 X118.864 Y121.195 E.02393
G1 X119.092 Y120.921 E.01286
G1 X119.244 Y120.587 E.01326
G1 X119.383 Y119.87 E.02636
G1 X119.549 Y119.291 E.02176
G1 X119.77 Y118.734 E.02162
G1 X119.928 Y118.414 E.01289
G1 X120.223 Y117.918 E.02083
G1 X120.589 Y117.42 E.02232
G1 X120.885 Y117.092 E.01596
M204 S6000
G1 X121.225 Y117.398 F30000
G1 F3000
M204 S500
G1 X121.297 Y117.319 E.00387
G1 X121.677 Y116.97 E.01863
G1 X122.299 Y116.519 E.02776
G1 X122.769 Y116.255 E.01945
G1 X123.294 Y116.026 E.02066
G1 X123.836 Y115.852 E.02055
G1 X124.147 Y115.78 E.01154
G1 X124.665 Y115.702 E.01893
G1 X125.241 Y115.672 E.0208
G1 X125.98 Y115.719 E.02673
G1 X126.289 Y115.768 E.01129
G1 X126.854 Y115.907 E.02101
G1 X127.529 Y116.139 E.02578
G1 X128.006 Y116.2 E.01736
G1 X128.144 Y116.195 E.00498
G1 X128.475 Y116.137 E.01214
G1 X129.126 Y115.913 E.02488
G1 X129.681 Y115.775 E.02063
G1 X130.201 Y115.697 E.01897
G1 X130.519 Y115.675 E.01152
G1 X131.115 Y115.683 E.02151
G1 X131.651 Y115.745 E.01951
G1 X132.406 Y115.922 E.028
G1 X132.695 Y116.021 E.011
G1 X133.177 Y116.228 E.01897
G1 X133.645 Y116.484 E.01926
G1 X134.272 Y116.929 E.02775
G1 X134.671 Y117.287 E.01934
G1 X135.05 Y117.702 E.02031
G1 X135.265 Y117.981 E.01271
G1 X135.57 Y118.454 E.02034
G1 X135.81 Y118.917 E.01881
G1 X136.008 Y119.412 E.01925
G1 X136.167 Y119.959 E.02057
G1 X136.305 Y120.658 E.02573
G1 X136.48 Y121.09 E.01683
G1 X136.728 Y121.428 E.01512
G1 X137.149 Y121.796 E.0202
G1 X137.525 Y122.157 E.01882
G1 X138.014 Y122.745 E.02761
G1 X138.329 Y123.233 E.02097
G1 X138.568 Y123.698 E.01889
G1 X138.7 Y124.013 E.01232
G1 X138.873 Y124.547 E.02026
G1 X138.99 Y125.083 E.01984
G1 X139.054 Y125.638 E.02016
G1 X139.063 Y126.184 E.01972
G1 X139.018 Y126.718 E.01936
G1 X138.88 Y127.424 E.02597
G1 X138.707 Y127.965 E.0205
G1 X138.481 Y128.487 E.02053
G1 X138.33 Y128.769 E.01154
G1 X138.044 Y129.214 E.0191
G1 X137.711 Y129.64 E.01953
G1 X137.315 Y130.052 E.02063
G1 X136.778 Y130.521 E.02575
G1 X136.563 Y130.779 E.01214
G1 X136.489 Y130.896 E.00498
G1 X136.305 Y131.34 E.01735
G1 X136.166 Y132.051 E.02617
G1 X136.082 Y132.362 E.01164
G1 X135.892 Y132.893 E.02038
G1 X135.671 Y133.365 E.0188
G1 X135.397 Y133.827 E.01938
G1 X135.07 Y134.273 E.01997
G1 X134.685 Y134.699 E.02075
G1 X134.3 Y135.05 E.01879
G1 X133.886 Y135.36 E.01869
G1 X133.188 Y135.767 E.02918
G1 X132.896 Y135.9 E.01157
G1 X132.389 Y136.082 E.01945
G1 X131.859 Y136.217 E.01976
G1 X131.319 Y136.3 E.01972
G1 X130.774 Y136.329 E.01972
G1 X130.229 Y136.305 E.01971
G1 X129.685 Y136.226 E.01981
G1 X129.144 Y136.093 E.02013
G1 X128.374 Y135.837 E.02929
G1 X127.959 Y135.799 E.01508
G1 X127.498 Y135.872 E.01685
G1 X127.055 Y136.029 E.01695
G1 X126.551 Y136.175 E.01896
G1 X126.013 Y136.276 E.01975
G1 X125.469 Y136.325 E.01971
G1 X124.924 Y136.319 E.01971
G1 X124.369 Y136.259 E.02014
G1 X123.817 Y136.14 E.02039
G1 X123.136 Y135.911 E.02595
G1 X122.611 Y135.665 E.02093
G1 X122.322 Y135.498 E.01206
G1 X121.904 Y135.21 E.0183
G1 X121.323 Y134.706 E.02779
G1 X120.957 Y134.305 E.0196
G1 X120.624 Y133.86 E.02006
G1 X120.443 Y133.568 E.01241
G1 X120.097 Y132.866 E.02826
G1 X119.918 Y132.364 E.01922
G1 X119.835 Y132.056 E.01151
G1 X119.696 Y131.342 E.02628
G1 X119.58 Y131.026 E.01215
G1 X119.515 Y130.904 E.00498
G1 X119.223 Y130.522 E.01735
G1 X118.694 Y130.062 E.02533
G1 X118.321 Y129.677 E.01935
G1 X117.984 Y129.254 E.01952
G1 X117.681 Y128.786 E.02014
G1 X117.529 Y128.506 E.0115
G1 X117.29 Y127.959 E.02153
G1 X117.127 Y127.452 E.01925
G1 X117.01 Y126.918 E.01972
G1 X116.948 Y126.389 E.01923
G1 X116.937 Y125.854 E.01935
G1 X117.012 Y125.076 E.02819
G1 X117.125 Y124.555 E.01925
G1 X117.287 Y124.048 E.01923
G1 X117.51 Y123.533 E.02027
G1 X117.655 Y123.259 E.01119
G1 X118.096 Y122.598 E.02868
G1 X118.441 Y122.19 E.01933
G1 X118.665 Y121.964 E.01146
G1 X119.222 Y121.479 E.02666
G1 X119.437 Y121.221 E.01214
G1 X119.51 Y121.104 E.00498
G1 X119.695 Y120.66 E.01736
G1 X119.827 Y119.983 E.02492
G1 X119.985 Y119.432 E.02069
G1 X120.19 Y118.915 E.02009
G1 X120.332 Y118.628 E.01156
G1 X120.601 Y118.177 E.01894
G1 X120.948 Y117.705 E.02118
G1 X121.185 Y117.443 E.01273
M204 S6000
G1 X121.524 Y117.749 F30000
G1 F3000
M204 S500
G1 X121.617 Y117.646 E.00502
G1 X121.961 Y117.33 E.01685
G1 X122.54 Y116.909 E.02586
G1 X122.967 Y116.668 E.01769
G1 X123.462 Y116.452 E.01949
G1 X123.963 Y116.292 E.01899
G1 X124.238 Y116.229 E.01021
G1 X124.705 Y116.158 E.01704
G1 X125.246 Y116.131 E.01957
G1 X125.923 Y116.173 E.02451
G1 X126.193 Y116.215 E.00983
G1 X126.728 Y116.347 E.01992
G1 X127.483 Y116.593 E.02865
G1 X128.032 Y116.656 E.01997
G1 X128.229 Y116.644 E.00713
G1 X128.543 Y116.589 E.01149
G1 X129.252 Y116.353 E.02698
G1 X129.777 Y116.222 E.01953
G1 X130.245 Y116.153 E.0171
G1 X130.526 Y116.132 E.01017
G1 X131.092 Y116.14 E.02043
G1 X131.58 Y116.198 E.01775
G1 X132.287 Y116.364 E.0262
G1 X132.535 Y116.45 E.0095
G1 X132.971 Y116.637 E.01712
G1 X133.395 Y116.869 E.01746
G1 X133.98 Y117.282 E.02585
G1 X134.344 Y117.607 E.0176
G1 X134.696 Y117.992 E.01884
G1 X134.894 Y118.249 E.01174
G1 X135.177 Y118.689 E.01888
G1 X135.396 Y119.114 E.01723
G1 X135.573 Y119.555 E.01717
G1 X135.723 Y120.071 E.01942
G1 X135.886 Y120.841 E.02841
G1 X136.116 Y121.366 E.0207
G1 X136.438 Y121.782 E.019
G1 X137.182 Y122.461 E.03636
G1 X137.639 Y123.01 E.02581
G1 X137.936 Y123.468 E.01971
G1 X138.151 Y123.886 E.01697
G1 X138.269 Y124.166 E.01097
G1 X138.429 Y124.66 E.01873
G1 X138.537 Y125.152 E.0182
G1 X138.597 Y125.661 E.01851
G1 X138.605 Y126.176 E.01858
G1 X138.563 Y126.663 E.01765
G1 X138.438 Y127.303 E.02355
G1 X138.281 Y127.798 E.01875
G1 X138.066 Y128.293 E.01946
G1 X137.932 Y128.541 E.0102
G1 X137.675 Y128.944 E.01726
G1 X137.369 Y129.335 E.0179
G1 X136.996 Y129.724 E.01949
G1 X136.42 Y130.236 E.02782
G1 X136.216 Y130.481 E.01149
G1 X136.107 Y130.646 E.00713
G1 X135.888 Y131.153 E.01996
G1 X135.719 Y131.952 E.02949
G1 X135.644 Y132.231 E.01041
G1 X135.466 Y132.725 E.01896
G1 X135.263 Y133.156 E.01722
G1 X135.019 Y133.569 E.01731
G1 X134.719 Y133.978 E.01832
G1 X134.356 Y134.381 E.01959
G1 X134.013 Y134.693 E.01672
G1 X133.64 Y134.974 E.0169
G1 X132.984 Y135.357 E.02741
G1 X132.719 Y135.478 E.01052
G1 X132.249 Y135.646 E.01803
G1 X131.761 Y135.77 E.01816
G1 X131.266 Y135.845 E.01809
G1 X130.765 Y135.871 E.0181
G1 X130.265 Y135.848 E.01808
G1 X129.78 Y135.778 E.01769
G1 X129.266 Y135.651 E.0191
G1 X128.532 Y135.407 E.02795
G1 X128.007 Y135.345 E.01909
G1 X127.878 Y135.349 E.00464
G1 X127.436 Y135.419 E.01618
G1 X126.454 Y135.727 E.03716
G1 X125.957 Y135.822 E.01825
G1 X125.458 Y135.867 E.0181
G1 X124.958 Y135.863 E.01807
G1 X124.435 Y135.806 E.01897
G1 X123.931 Y135.696 E.01863
G1 X123.314 Y135.489 E.02352
G1 X122.828 Y135.262 E.01935
G1 X122.562 Y135.108 E.01111
G1 X122.191 Y134.853 E.01625
G1 X121.649 Y134.383 E.02591
G1 X121.314 Y134.019 E.01786
G1 X121.005 Y133.607 E.01858
G1 X120.84 Y133.34 E.01134
G1 X120.516 Y132.68 E.02653
G1 X120.357 Y132.233 E.01713
G1 X120.282 Y131.958 E.01031
G1 X120.121 Y131.175 E.02887
G1 X120.011 Y130.875 E.01151
G1 X119.923 Y130.698 E.00714
G1 X119.594 Y130.254 E.01997
G1 X119.005 Y129.725 E.02858
G1 X118.67 Y129.379 E.01739
G1 X118.36 Y128.992 E.01793
G1 X118.077 Y128.557 E.01872
G1 X117.943 Y128.311 E.01013
G1 X117.721 Y127.804 E.01997
G1 X117.571 Y127.339 E.01763
G1 X117.463 Y126.849 E.01812
G1 X117.405 Y126.364 E.01763
G1 X117.394 Y125.879 E.01753
G1 X117.466 Y125.139 E.02684
G1 X117.569 Y124.667 E.01744
G1 X117.714 Y124.215 E.01714
G1 X117.92 Y123.736 E.01884
G1 X118.045 Y123.5 E.00964
G1 X118.466 Y122.868 E.02743
G1 X118.775 Y122.503 E.01725
G1 X118.975 Y122.302 E.01024
G1 X119.58 Y121.764 E.02923
G1 X119.783 Y121.519 E.01149
G1 X119.892 Y121.356 E.00708
G1 X120.147 Y120.734 E.02425
G1 X120.271 Y120.096 E.02349
G1 X120.42 Y119.573 E.01962
G1 X120.611 Y119.096 E.01856
G1 X120.737 Y118.842 E.01024
G1 X120.978 Y118.436 E.01706
G1 X121.308 Y117.989 E.02003
G1 X121.484 Y117.794 E.0095
M204 S6000
G1 X121.849 Y118.07 F30000
G1 F3000
M204 S500
G1 X121.854 Y118.063 E.00031
G1 X122.322 Y117.629 E.02304
G1 X122.844 Y117.258 E.02313
G1 X123.418 Y116.964 E.0233
G1 X123.997 Y116.76 E.02215
G1 X124.709 Y116.618 E.02621
G1 X125.313 Y116.589 E.02183
G1 X125.943 Y116.639 E.02282
G1 X126.462 Y116.745 E.01912
G1 X126.852 Y116.868 E.01479
G1 X127.271 Y117.045 E.01641
G1 X127.782 Y117.337 E.02123
G1 X127.848 Y117.355 E.00249
G1 X128.151 Y117.359 E.01095
G1 X128.228 Y117.336 E.0029
G1 X128.433 Y117.201 E.00887
G1 X128.727 Y117.046 E.01197
G1 X129.214 Y116.846 E.01902
G1 X129.779 Y116.693 E.02115
G1 X130.555 Y116.592 E.02826
G1 X131.227 Y116.61 E.02426
G1 X131.739 Y116.692 E.01873
G1 X132.418 Y116.899 E.02561
G1 X133.003 Y117.171 E.02331
G1 X133.781 Y117.714 E.03423
G1 X134.202 Y118.124 E.02124
G1 X134.684 Y118.759 E.02877
G1 X134.955 Y119.253 E.02036
G1 X135.193 Y119.867 E.02376
G1 X135.325 Y120.398 E.01975
G1 X135.389 Y120.869 E.01716
G1 X135.403 Y121.262 E.01422
G1 X135.391 Y121.464 E.0073
G1 X135.409 Y121.542 E.00287
G1 X135.565 Y121.808 E.01113
G1 X135.614 Y121.857 E.00253
G1 X136.077 Y122.126 E.01933
G1 X136.468 Y122.417 E.01758
G1 X136.806 Y122.725 E.01653
G1 X137.056 Y122.998 E.01336
G1 X137.333 Y123.368 E.01668
G1 X137.857 Y124.367 E.04074
G1 X137.987 Y124.768 E.0152
G1 X138.087 Y125.215 E.01655
G1 X138.137 Y125.609 E.01433
G1 X138.148 Y126.058 E.01623
G1 X138.048 Y126.973 E.03324
G1 X137.948 Y127.369 E.01473
G1 X137.841 Y127.68 E.01187
G1 X137.66 Y128.085 E.01601
G1 X137.43 Y128.492 E.01689
G1 X137.123 Y128.918 E.01897
G1 X136.746 Y129.333 E.02025
G1 X136.441 Y129.606 E.01477
G1 X136.062 Y129.885 E.01699
G1 X135.605 Y130.147 E.01903
G1 X135.554 Y130.199 E.00263
G1 X135.409 Y130.457 E.01069
G1 X135.391 Y130.524 E.00249
G1 X135.39 Y131.08 E.02009
G1 X135.25 Y131.934 E.03122
G1 X135.111 Y132.386 E.01708
G1 X134.928 Y132.81 E.01669
G1 X134.583 Y133.394 E.02448
G1 X134.139 Y133.945 E.02556
G1 X133.608 Y134.428 E.02592
G1 X133.078 Y134.788 E.02313
G1 X132.379 Y135.118 E.02791
G1 X131.802 Y135.294 E.02179
G1 X131.262 Y135.383 E.01975
G1 X130.468 Y135.403 E.02867
G1 X129.817 Y135.317 E.0237
G1 X129.093 Y135.108 E.02721
G1 X128.651 Y134.912 E.01745
G1 X128.241 Y134.664 E.01731
G1 X128.171 Y134.645 E.0026
G1 X127.855 Y134.641 E.01141
G1 X127.785 Y134.66 E.00261
G1 X127.319 Y134.928 E.01944
G1 X126.515 Y135.238 E.03111
G1 X126.085 Y135.34 E.01595
G1 X125.649 Y135.399 E.01587
G1 X124.968 Y135.403 E.0246
G1 X124.259 Y135.304 E.02585
G1 X123.671 Y135.135 E.02208
G1 X123.034 Y134.85 E.0252
G1 X122.486 Y134.5 E.02347
G1 X121.971 Y134.056 E.02457
G1 X121.506 Y133.516 E.02571
G1 X121.131 Y132.914 E.02562
G1 X120.797 Y132.09 E.03211
G1 X120.658 Y131.513 E.0214
G1 X120.604 Y131.032 E.01749
G1 X120.607 Y130.528 E.01822
G1 X120.589 Y130.459 E.00258
G1 X120.438 Y130.194 E.01101
G1 X120.388 Y130.144 E.00254
G1 X119.879 Y129.845 E.02133
G1 X119.544 Y129.593 E.01513
G1 X119.2 Y129.281 E.01675
G1 X118.93 Y128.984 E.01452
G1 X118.685 Y128.663 E.01459
G1 X118.242 Y127.865 E.03293
G1 X118.077 Y127.446 E.01628
G1 X117.955 Y126.999 E.01671
G1 X117.873 Y126.488 E.01871
G1 X117.847 Y126.032 E.01648
G1 X117.861 Y125.638 E.01424
G1 X117.923 Y125.16 E.01743
G1 X118.031 Y124.705 E.01686
G1 X118.179 Y124.275 E.01643
G1 X118.405 Y123.792 E.01924
G1 X118.685 Y123.345 E.01906
G1 X119.164 Y122.762 E.02725
G1 X119.588 Y122.371 E.02084
G1 X119.974 Y122.092 E.01719
G1 X120.394 Y121.853 E.01744
G1 X120.446 Y121.801 E.00265
G1 X120.592 Y121.541 E.01079
G1 X120.61 Y121.466 E.00279
G1 X120.597 Y121.241 E.00813
G1 X120.617 Y120.8 E.01595
G1 X120.673 Y120.404 E.01445
G1 X120.767 Y119.996 E.01511
G1 X120.989 Y119.375 E.02381
G1 X121.259 Y118.848 E.02137
G1 X121.812 Y118.118 E.03309
M204 S6000
G1 X122.156 Y118.406 F30000
G1 F3000
M204 S500
G1 X122.639 Y117.958 E.02379
G1 X123.112 Y117.628 E.02084
G1 X123.629 Y117.37 E.02086
G1 X124.154 Y117.189 E.02003
G1 X124.804 Y117.065 E.0239
G1 X125.272 Y117.044 E.01691
G1 X125.848 Y117.086 E.02086
G1 X126.317 Y117.178 E.01727
G1 X126.721 Y117.306 E.01528
G1 X127.097 Y117.468 E.01479
G1 X127.448 Y117.662 E.01446
G1 X127.625 Y117.786 E.00782
G1 X127.702 Y117.811 E.00291
G1 X128.289 Y117.818 E.02121
G1 X128.368 Y117.794 E.00297
G1 X128.641 Y117.608 E.01192
G1 X128.946 Y117.447 E.01246
G1 X129.331 Y117.288 E.01503
G1 X129.829 Y117.148 E.01869
G1 X130.625 Y117.044 E.02898
G1 X131.217 Y117.067 E.02138
G1 X131.671 Y117.144 E.01663
G1 X132.289 Y117.338 E.0234
G1 X132.817 Y117.589 E.02109
G1 X133.459 Y118.038 E.0283
G1 X133.835 Y118.395 E.01871
G1 X134.281 Y118.975 E.02642
G1 X134.527 Y119.414 E.01816
G1 X134.747 Y119.969 E.02158
G1 X134.884 Y120.516 E.02033
G1 X134.936 Y120.932 E.01513
G1 X134.947 Y121.282 E.01267
G1 X134.924 Y121.579 E.01074
G1 X134.945 Y121.663 E.00313
G1 X135.11 Y121.922 E.0111
G1 X135.226 Y122.148 E.00917
G1 X135.289 Y122.21 E.0032
G1 X135.482 Y122.301 E.00768
G1 X135.846 Y122.52 E.01536
G1 X136.198 Y122.785 E.01591
G1 X136.5 Y123.064 E.01484
G1 X136.721 Y123.309 E.01191
G1 X136.925 Y123.575 E.01208
G1 X137.42 Y124.501 E.03792
G1 X137.54 Y124.864 E.01381
G1 X137.632 Y125.266 E.01491
G1 X137.684 Y125.673 E.01481
G1 X137.691 Y126.074 E.01448
G1 X137.593 Y126.929 E.03108
G1 X137.506 Y127.254 E.01215
G1 X137.408 Y127.533 E.01067
G1 X137.241 Y127.902 E.01463
G1 X137.03 Y128.27 E.0153
G1 X136.791 Y128.605 E.01488
G1 X136.403 Y129.031 E.02079
G1 X136.135 Y129.266 E.01288
G1 X135.831 Y129.49 E.01362
G1 X135.48 Y129.701 E.01479
G1 X135.288 Y129.791 E.00766
G1 X135.227 Y129.848 E.00301
G1 X134.943 Y130.354 E.02095
G1 X134.926 Y130.431 E.00287
G1 X134.945 Y130.694 E.0095
G1 X134.933 Y131.072 E.01367
G1 X134.798 Y131.865 E.02905
G1 X134.674 Y132.252 E.01467
G1 X134.536 Y132.575 E.01269
G1 X134.23 Y133.104 E.02204
G1 X133.835 Y133.603 E.02299
G1 X133.354 Y134.049 E.02368
G1 X132.888 Y134.372 E.02049
G1 X132.251 Y134.68 E.02554
G1 X131.729 Y134.843 E.01974
G1 X131.26 Y134.926 E.01719
G1 X130.446 Y134.946 E.0294
G1 X129.949 Y134.879 E.0181
G1 X129.286 Y134.693 E.02486
G1 X128.828 Y134.491 E.0181
G1 X128.375 Y134.21 E.01926
G1 X128.304 Y134.189 E.00266
G1 X127.715 Y134.183 E.02125
G1 X127.636 Y134.207 E.003
G1 X127.424 Y134.353 E.0093
G1 X127.161 Y134.499 E.01085
G1 X126.414 Y134.792 E.02898
G1 X126.031 Y134.886 E.01423
G1 X125.58 Y134.947 E.01643
G1 X125.041 Y134.952 E.01945
G1 X124.313 Y134.85 E.02656
G1 X123.794 Y134.695 E.01956
G1 X123.283 Y134.466 E.02021
G1 X122.792 Y134.161 E.02088
G1 X122.261 Y133.703 E.02529
G1 X121.85 Y133.215 E.02306
G1 X121.516 Y132.667 E.02315
G1 X121.218 Y131.913 E.02926
G1 X121.113 Y131.468 E.01653
G1 X121.061 Y131.027 E.01603
G1 X121.054 Y130.679 E.01258
G1 X121.075 Y130.42 E.00935
G1 X121.054 Y130.335 E.00319
G1 X120.914 Y130.119 E.00929
G1 X120.774 Y129.851 E.01091
G1 X120.711 Y129.79 E.00316
G1 X120.518 Y129.699 E.00769
G1 X120.156 Y129.482 E.01525
G1 X119.853 Y129.257 E.01363
G1 X119.543 Y128.978 E.01507
G1 X119.263 Y128.672 E.01497
G1 X119.045 Y128.381 E.01312
G1 X118.639 Y127.639 E.03056
G1 X118.503 Y127.279 E.01387
G1 X118.395 Y126.875 E.0151
G1 X118.323 Y126.412 E.01694
G1 X118.303 Y126.004 E.01473
G1 X118.318 Y125.652 E.01273
G1 X118.377 Y125.215 E.0159
G1 X118.476 Y124.807 E.01516
G1 X118.612 Y124.42 E.01483
G1 X118.788 Y124.041 E.01507
G1 X119.077 Y123.579 E.01967
G1 X119.52 Y123.048 E.02497
G1 X119.852 Y122.744 E.01626
G1 X120.203 Y122.487 E.0157
G1 X120.518 Y122.301 E.01322
G1 X120.712 Y122.209 E.00774
G1 X120.773 Y122.152 E.00301
G1 X121.059 Y121.644 E.02104
G1 X121.076 Y121.567 E.00287
G1 X121.053 Y121.265 E.01092
G1 X121.069 Y120.866 E.01442
G1 X121.117 Y120.512 E.01289
G1 X121.214 Y120.091 E.01562
G1 X121.421 Y119.524 E.0218
G1 X121.669 Y119.051 E.01928
G1 X122.12 Y118.454 E.02702
M204 S6000
G1 X122.459 Y118.749 F30000
G1 F3000
M204 S500
G1 X122.957 Y118.286 E.02457
G1 X123.377 Y118 E.01833
G1 X123.836 Y117.777 E.01843
G1 X124.307 Y117.62 E.01793
G1 X124.819 Y117.521 E.01884
G1 X125.23 Y117.5 E.01486
G1 X125.823 Y117.543 E.02144
G1 X126.231 Y117.627 E.01506
G1 X126.585 Y117.742 E.01344
G1 X126.919 Y117.889 E.01317
G1 X127.228 Y118.063 E.01283
G1 X127.488 Y118.251 E.01156
G1 X127.576 Y118.276 E.00333
G1 X127.825 Y118.261 E.00898
G1 X128.425 Y118.279 E.02169
G1 X128.508 Y118.254 E.00311
G1 X128.848 Y118.016 E.015
G1 X129.166 Y117.848 E.01297
G1 X129.454 Y117.728 E.01126
G1 X129.884 Y117.602 E.01621
G1 X130.6 Y117.501 E.0261
G1 X131.14 Y117.518 E.01948
G1 X131.525 Y117.578 E.0141
G1 X132.162 Y117.777 E.02408
G1 X132.545 Y117.956 E.01527
G1 X133.205 Y118.419 E.02909
G1 X133.521 Y118.728 E.01597
G1 X133.922 Y119.258 E.02398
G1 X134.13 Y119.639 E.01569
G1 X134.324 Y120.141 E.01943
G1 X134.441 Y120.629 E.01812
G1 X134.479 Y120.939 E.01126
G1 X134.49 Y121.304 E.01317
G1 X134.454 Y121.693 E.01412
G1 X134.476 Y121.78 E.00325
G1 X134.7 Y122.125 E.01486
G1 X134.892 Y122.5 E.01519
G1 X134.958 Y122.562 E.00328
G1 X135.243 Y122.691 E.01131
G1 X135.569 Y122.884 E.01366
G1 X135.885 Y123.119 E.01424
G1 X136.157 Y123.367 E.01327
G1 X136.386 Y123.62 E.01234
G1 X136.567 Y123.859 E.01082
G1 X136.984 Y124.638 E.0319
G1 X137.094 Y124.963 E.01241
G1 X137.179 Y125.322 E.0133
G1 X137.227 Y125.682 E.01313
G1 X137.238 Y126.017 E.0121
G1 X137.153 Y126.805 E.0286
G1 X137.076 Y127.098 E.01094
G1 X136.975 Y127.387 E.01107
G1 X136.823 Y127.717 E.01313
G1 X136.632 Y128.045 E.01368
G1 X136.416 Y128.343 E.01328
G1 X136.107 Y128.683 E.0166
G1 X135.829 Y128.927 E.01337
G1 X135.559 Y129.123 E.01207
G1 X135.242 Y129.31 E.01326
G1 X134.961 Y129.437 E.01113
G1 X134.897 Y129.497 E.00317
G1 X134.614 Y130.021 E.02151
G1 X134.478 Y130.228 E.00893
G1 X134.456 Y130.316 E.00328
M73 P4 R12
G1 X134.489 Y130.671 E.01288
G1 X134.476 Y131.066 E.01427
G1 X134.364 Y131.721 E.02398
G1 X134.257 Y132.066 E.01305
G1 X134.112 Y132.402 E.01321
G1 X133.878 Y132.813 E.01706
G1 X133.47 Y133.328 E.02373
G1 X133.042 Y133.715 E.02083
G1 X132.623 Y134 E.01831
G1 X132.049 Y134.27 E.02289
G1 X131.591 Y134.408 E.01728
G1 X131.176 Y134.477 E.01518
G1 X130.511 Y134.494 E.02401
G1 X130.082 Y134.441 E.01561
G1 X129.4 Y134.25 E.02556
G1 X129.012 Y134.072 E.01544
G1 X128.496 Y133.745 E.02205
G1 X128.414 Y133.724 E.00304
G1 X128.175 Y133.739 E.00864
G1 X127.578 Y133.721 E.02158
G1 X127.494 Y133.747 E.00314
G1 X127.208 Y133.95 E.0127
G1 X126.931 Y134.104 E.01142
G1 X126.314 Y134.346 E.02395
G1 X125.915 Y134.444 E.01483
G1 X125.516 Y134.494 E.01453
G1 X125.032 Y134.495 E.01746
G1 X124.453 Y134.415 E.02108
G1 X123.916 Y134.254 E.02026
G1 X123.466 Y134.048 E.01787
G1 X123.029 Y133.77 E.01869
G1 X122.556 Y133.354 E.02275
G1 X122.197 Y132.917 E.02041
G1 X121.904 Y132.425 E.02071
G1 X121.642 Y131.742 E.0264
G1 X121.557 Y131.363 E.01402
G1 X121.518 Y131.024 E.0123
G1 X121.511 Y130.662 E.01308
G1 X121.545 Y130.308 E.01284
G1 X121.524 Y130.221 E.00326
G1 X121.294 Y129.865 E.01528
G1 X121.109 Y129.501 E.01474
G1 X121.043 Y129.438 E.00329
G1 X120.757 Y129.31 E.01134
G1 X120.431 Y129.116 E.01369
G1 X120.16 Y128.919 E.01208
G1 X119.882 Y128.672 E.01343
G1 X119.633 Y128.403 E.01325
G1 X119.405 Y128.099 E.01371
G1 X119.07 Y127.486 E.0252
G1 X118.928 Y127.112 E.01446
G1 X118.836 Y126.755 E.01331
G1 X118.78 Y126.392 E.01325
G1 X118.759 Y126.025 E.01328
G1 X118.77 Y125.716 E.01117
G1 X118.821 Y125.325 E.01422
G1 X118.905 Y124.965 E.01338
G1 X119.046 Y124.564 E.01532
G1 X119.204 Y124.231 E.01333
G1 X119.422 Y123.879 E.01493
G1 X119.877 Y123.334 E.02564
G1 X120.161 Y123.081 E.01373
G1 X120.431 Y122.884 E.01208
G1 X120.757 Y122.69 E.01369
G1 X121.039 Y122.563 E.01116
G1 X121.103 Y122.503 E.00317
G1 X121.386 Y121.979 E.02151
G1 X121.523 Y121.771 E.00899
G1 X121.545 Y121.684 E.00327
G1 X121.51 Y121.288 E.01435
G1 X121.522 Y120.929 E.01297
G1 X121.56 Y120.622 E.01116
G1 X121.661 Y120.186 E.01615
G1 X121.852 Y119.676 E.01964
G1 X122.076 Y119.258 E.01714
G1 X122.423 Y118.797 E.02082
M204 S6000
G1 X122.785 Y119.075 F30000
G1 F3000
M204 S500
G1 X122.828 Y119.019 E.00256
G1 X123.27 Y118.62 E.02151
G1 X123.573 Y118.413 E.01326
G1 X123.972 Y118.214 E.0161
G1 X124.46 Y118.051 E.01858
G1 X124.842 Y117.978 E.01404
G1 X125.188 Y117.955 E.01253
G1 X125.798 Y117.999 E.02207
G1 X126.087 Y118.061 E.01065
G1 X126.399 Y118.16 E.01182
G1 X126.695 Y118.287 E.01164
G1 X126.955 Y118.429 E.01069
G1 X127.355 Y118.718 E.01783
G1 X127.445 Y118.744 E.00338
G1 X127.805 Y118.718 E.01304
G1 X128.566 Y118.74 E.02748
G1 X128.65 Y118.714 E.00317
G1 X129.058 Y118.422 E.01811
G1 X129.34 Y118.27 E.01158
G1 X129.583 Y118.167 E.00954
G1 X129.946 Y118.054 E.01371
G1 X130.574 Y117.957 E.02294
G1 X131.134 Y117.975 E.02022
G1 X131.457 Y118.03 E.01185
G1 X132.029 Y118.214 E.0217
G1 X132.356 Y118.372 E.01308
G1 X132.947 Y118.796 E.02627
G1 X133.201 Y119.054 E.01308
G1 X133.56 Y119.538 E.02176
G1 X133.729 Y119.858 E.01306
G1 X133.899 Y120.31 E.01743
G1 X133.986 Y120.677 E.01364
G1 X134.026 Y121.001 E.01177
G1 X134.033 Y121.321 E.01157
G1 X133.983 Y121.805 E.01756
G1 X134.005 Y121.894 E.0033
G1 X134.321 Y122.38 E.02095
G1 X134.557 Y122.852 E.01904
G1 X134.625 Y122.916 E.00338
G1 X135.008 Y123.082 E.01505
G1 X135.294 Y123.249 E.01198
G1 X135.575 Y123.454 E.01256
G1 X135.816 Y123.672 E.01172
G1 X136.018 Y123.891 E.01076
G1 X136.209 Y124.143 E.01142
G1 X136.549 Y124.779 E.02601
G1 X136.649 Y125.066 E.011
G1 X136.725 Y125.38 E.01167
G1 X136.771 Y125.701 E.01169
G1 X136.784 Y125.964 E.00952
G1 X136.713 Y126.679 E.02594
G1 X136.633 Y126.987 E.01151
G1 X136.543 Y127.237 E.00958
G1 X136.406 Y127.53 E.01167
G1 X136.236 Y127.817 E.01203
G1 X136.045 Y128.077 E.01166
G1 X135.807 Y128.337 E.01273
G1 X135.566 Y128.553 E.0117
G1 X135.285 Y128.757 E.01253
G1 X135.007 Y128.918 E.01158
G1 X134.636 Y129.08 E.01465
G1 X134.57 Y129.141 E.00323
G1 X134.209 Y129.809 E.02743
G1 X134.006 Y130.109 E.01306
G1 X133.983 Y130.201 E.00342
G1 X134.032 Y130.647 E.01622
G1 X134.019 Y131.06 E.01492
G1 X133.913 Y131.648 E.02156
G1 X133.821 Y131.928 E.01064
G1 X133.691 Y132.225 E.01172
G1 X133.52 Y132.528 E.01254
G1 X133.172 Y132.981 E.02063
G1 X132.729 Y133.382 E.02159
G1 X132.362 Y133.625 E.01586
G1 X131.852 Y133.857 E.02026
G1 X131.458 Y133.97 E.01478
G1 X131.097 Y134.027 E.01321
G1 X130.494 Y134.037 E.02176
G1 X130.137 Y133.988 E.01303
G1 X129.594 Y133.837 E.02033
G1 X129.257 Y133.687 E.01331
G1 X128.818 Y133.416 E.01864
G1 X128.651 Y133.285 E.00766
G1 X128.557 Y133.256 E.00358
G1 X128.195 Y133.282 E.0131
G1 X127.435 Y133.26 E.02744
G1 X127.35 Y133.286 E.0032
G1 X126.993 Y133.547 E.01597
G1 X126.701 Y133.709 E.01203
G1 X126.143 Y133.922 E.02158
G1 X125.806 Y134 E.01251
G1 X125.455 Y134.041 E.01273
G1 X125.097 Y134.042 E.01293
G1 X124.587 Y133.978 E.01856
G1 X124.115 Y133.843 E.01773
G1 X123.648 Y133.628 E.01856
G1 X123.334 Y133.43 E.01342
G1 X122.911 Y133.066 E.02016
G1 X122.595 Y132.693 E.01764
G1 X122.291 Y132.181 E.02151
G1 X122.068 Y131.576 E.02327
G1 X122.004 Y131.266 E.01143
G1 X121.972 Y130.97 E.01076
G1 X121.968 Y130.649 E.01158
G1 X122.017 Y130.196 E.01644
G1 X121.996 Y130.106 E.00336
G1 X121.705 Y129.664 E.01909
G1 X121.442 Y129.148 E.02093
G1 X121.374 Y129.084 E.00335
G1 X120.993 Y128.918 E.01503
G1 X120.706 Y128.751 E.01199
G1 X120.425 Y128.546 E.01255
G1 X120.184 Y128.329 E.01172
G1 X119.967 Y128.09 E.01164
G1 X119.767 Y127.82 E.01212
G1 X119.499 Y127.33 E.02019
G1 X119.372 Y127 E.01275
G1 X119.288 Y126.687 E.01171
G1 X119.236 Y126.369 E.01163
G1 X119.216 Y126.047 E.01164
G1 X119.227 Y125.725 E.01163
G1 X119.274 Y125.382 E.01252
G1 X119.351 Y125.067 E.01171
G1 X119.457 Y124.763 E.01163
G1 X119.593 Y124.47 E.01164
G1 X119.77 Y124.176 E.01239
G1 X120.178 Y123.679 E.02321
G1 X120.425 Y123.454 E.01206
G1 X120.706 Y123.249 E.01256
G1 X120.993 Y123.082 E.01199
G1 X121.364 Y122.92 E.01465
G1 X121.43 Y122.859 E.00323
G1 X121.791 Y122.191 E.02742
G1 X121.994 Y121.892 E.01305
G1 X122.016 Y121.801 E.00338
G1 X121.966 Y121.307 E.01791
G1 X121.975 Y120.987 E.01158
G1 X122.006 Y120.724 E.00955
G1 X122.086 Y120.354 E.01366
G1 X122.283 Y119.828 E.0203
G1 X122.48 Y119.472 E.0147
G1 X122.748 Y119.123 E.01589
M204 S6000
G1 X123.092 Y119.414 F30000
G1 F3000
M204 S500
G1 X123.182 Y119.308 E.00502
G1 X123.579 Y118.956 E.01915
G1 X123.83 Y118.791 E.01087
G1 X124.108 Y118.65 E.01124
G1 X124.614 Y118.481 E.01926
G1 X124.875 Y118.434 E.00957
G1 X125.152 Y118.41 E.01004
G1 X125.694 Y118.444 E.01961
G1 X125.998 Y118.509 E.01123
G1 X126.262 Y118.596 E.01002
G1 X126.516 Y118.708 E.01002
G1 X126.738 Y118.832 E.00921
G1 X126.967 Y118.99 E.01002
G1 X127.239 Y119.219 E.01285
G1 X127.793 Y119.175 E.02006
G1 X128.43 Y119.185 E.02303
G1 X128.758 Y119.222 E.0119
G1 X129.041 Y118.983 E.01337
G1 X129.271 Y118.827 E.01002
G1 X129.514 Y118.693 E.01002
G1 X129.769 Y118.584 E.01002
G1 X130.012 Y118.507 E.00921
G1 X130.571 Y118.414 E.02045
G1 X130.848 Y118.41 E.01001
G1 X131.103 Y118.431 E.00922
G1 X131.386 Y118.481 E.01039
G1 X131.892 Y118.65 E.01926
G1 X132.159 Y118.785 E.01078
G1 X132.619 Y119.115 E.02047
G1 X132.832 Y119.324 E.01078
G1 X133.155 Y119.749 E.01926
G1 X133.298 Y120.011 E.01078
G1 X133.474 Y120.479 E.01805
G1 X133.541 Y120.782 E.01121
G1 X133.572 Y121.058 E.01002
G1 X133.576 Y121.335 E.01002
G1 X133.553 Y121.612 E.01003
G1 X133.492 Y121.948 E.01232
G1 X133.909 Y122.578 E.02729
G1 X134.255 Y123.269 E.02791
G1 X134.567 Y123.381 E.01196
G1 X134.819 Y123.498 E.01
G1 X135.066 Y123.645 E.01039
G1 X135.307 Y123.824 E.01085
G1 X135.511 Y124.012 E.01002
G1 X135.683 Y124.201 E.00922
G1 X135.848 Y124.424 E.01002
G1 X136.115 Y124.923 E.02045
G1 X136.205 Y125.173 E.00957
G1 X136.273 Y125.443 E.01004
G1 X136.314 Y125.717 E.01003
G1 X136.328 Y125.997 E.01011
G1 X136.273 Y126.558 E.02034
G1 X136.205 Y126.827 E.01002
G1 X136.111 Y127.088 E.01002
G1 X135.991 Y127.339 E.01004
G1 X135.842 Y127.585 E.01039
G1 X135.676 Y127.807 E.01002
G1 X135.504 Y127.996 E.00921
G1 X135.299 Y128.182 E.01002
G1 X135.057 Y128.361 E.01084
G1 X134.819 Y128.502 E.01002
G1 X134.568 Y128.619 E.01
G1 X134.249 Y128.733 E.01221
G1 X134.117 Y129.035 E.01189
G1 X133.807 Y129.592 E.02303
G1 X133.492 Y130.05 E.02006
G1 X133.556 Y130.41 E.01322
G1 X133.577 Y130.687 E.01002
G1 X133.569 Y130.975 E.0104
G1 X133.48 Y131.501 E.01925
G1 X133.403 Y131.744 E.00921
G1 X133.294 Y131.999 E.01002
G1 X133.149 Y132.262 E.01083
G1 X132.99 Y132.49 E.01004
G1 X132.818 Y132.692 E.00957
G1 X132.419 Y133.045 E.01926
G1 X132.159 Y133.215 E.01121
G1 X131.932 Y133.332 E.00921
G1 X131.675 Y133.436 E.01002
G1 X131.386 Y133.519 E.01084
G1 X131.092 Y133.57 E.01079
G1 X130.559 Y133.585 E.01926
G1 X130.262 Y133.548 E.01078
G1 X129.78 Y133.419 E.01805
G1 X129.505 Y133.302 E.01078
G1 X129.051 Y133.023 E.01926
G1 X128.761 Y132.781 E.01361
G1 X128.207 Y132.825 E.02006
G1 X127.57 Y132.815 E.02303
G1 X127.242 Y132.778 E.0119
G1 X126.976 Y133.003 E.01256
G1 X126.729 Y133.174 E.01083
G1 X126.476 Y133.311 E.01041
G1 X125.976 Y133.496 E.01925
G1 X125.705 Y133.554 E.01003
G1 X125.452 Y133.584 E.00921
G1 X125.164 Y133.59 E.0104
G1 X124.635 Y133.523 E.01925
G1 X124.315 Y133.432 E.01199
G1 X123.83 Y133.209 E.01927
G1 X123.579 Y133.044 E.01087
G1 X123.205 Y132.716 E.01795
G1 X122.988 Y132.46 E.01211
G1 X122.722 Y132.029 E.0183
G1 X122.517 Y131.49 E.02083
G1 X122.459 Y131.218 E.01002
G1 X122.429 Y130.965 E.00921
G1 X122.423 Y130.687 E.01002
G1 X122.444 Y130.41 E.01003
G1 X122.508 Y130.052 E.01314
G1 X122.082 Y129.406 E.02792
G1 X121.745 Y128.731 E.02728
G1 X121.433 Y128.619 E.01196
G1 X121.181 Y128.502 E.01001
G1 X120.934 Y128.355 E.0104
G1 X120.693 Y128.176 E.01084
G1 X120.488 Y127.988 E.01003
G1 X120.303 Y127.781 E.01003
G1 X120.133 Y127.546 E.01049
G1 X119.898 Y127.107 E.01794
G1 X119.798 Y126.837 E.01042
G1 X119.729 Y126.568 E.01002
G1 X119.687 Y126.294 E.01002
G1 X119.672 Y126.017 E.01002
G1 X119.684 Y125.739 E.01002
G1 X119.727 Y125.442 E.01083
G1 X119.795 Y125.173 E.01002
G1 X119.889 Y124.912 E.01002
G1 X120.009 Y124.661 E.01004
G1 X120.164 Y124.406 E.01078
G1 X120.481 Y124.02 E.01804
G1 X120.693 Y123.824 E.01041
G1 X120.934 Y123.645 E.01085
G1 X121.181 Y123.498 E.01039
G1 X121.433 Y123.381 E.01
G1 X121.751 Y123.267 E.0122
G1 X121.883 Y122.965 E.01189
G1 X122.193 Y122.408 E.02302
G1 X122.508 Y121.95 E.02006
G1 X122.445 Y121.6 E.01285
G1 X122.423 Y121.323 E.01002
G1 X122.428 Y121.046 E.01002
G1 X122.461 Y120.77 E.01002
G1 X122.52 Y120.499 E.01003
G1 X122.597 Y120.256 E.0092
G1 X122.706 Y120.001 E.01003
G1 X122.851 Y119.738 E.01083
G1 X123.01 Y119.51 E.01004
G1 X123.053 Y119.46 E.00238
; WIPE_START
G1 X123.182 Y119.308 E-.07567
G1 X123.579 Y118.956 E-.20159
G1 X123.805 Y118.808 E-.10273
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I-.834 J.887 P1  F30000
G1 X133.718 Y128.128 Z.6
G1 Z.2
G1 E.4 F1800
; FEATURE: Outer wall
G1 F3000
M204 S500
G1 X133.471 Y128.698 E.02243
G3 X132.683 Y129.897 I-5.426 J-2.704 E.05191
G3 X132.633 Y131.692 I-2.15 J.838 E.0666
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X129.315 Y132.296 I-1.884 J-.935 E.14129
G1 X129.033 Y132.004 E.01464
G3 X126.959 Y132.013 I-1.061 J-5.968 E.07525
G3 X124.773 Y132.808 I-1.734 J-1.364 E.08845
G3 X123.205 Y130.286 I.506 J-2.063 E.11871
G1 X123.316 Y129.898 E.01457
G3 X122.282 Y128.107 I4.22 J-3.631 E.07511
G3 X120.56 Y126.803 I.318 J-2.209 E.08139
G3 X121.891 Y123.991 I1.947 J-.8 E.12642
G1 X122.272 Y123.895 E.01422
G3 X123.317 Y122.103 I5.683 J2.112 E.07525
G3 X123.367 Y120.308 I2.15 J-.838 E.06659
G3 X125.385 Y119.142 I1.914 J.983 E.08893
G3 X126.967 Y119.996 I-.218 J2.296 E.06669
G3 X129.041 Y119.987 I1.061 J5.965 E.07525
G3 X131.227 Y119.192 I1.734 J1.364 E.08846
G3 X132.795 Y121.714 I-.507 J2.063 E.1187
G1 X132.684 Y122.102 E.01457
G3 X133.718 Y123.893 I-4.22 J3.631 E.07511
G3 X135.44 Y125.196 I-.319 J2.209 E.08139
G3 X134.109 Y128.009 I-1.947 J.8 E.12642
G1 X133.762 Y128.096 E.01295
M204 S6000
G1 X133.468 Y127.699 F30000
; FEATURE: Inner wall
G1 F3000
M204 S500
G1 X133.398 Y127.716 E.00261
G1 X133.06 Y128.495 E.03066
G3 X132.177 Y129.787 I-5.504 J-2.815 E.05666
G1 X132.349 Y130.39 E.02265
G3 X129.628 Y131.961 I-1.605 J.363 E.15085
G1 X129.191 Y131.511 E.02265
G3 X127.631 Y131.63 I-1.246 J-6.039 E.05665
G1 X126.787 Y131.533 E.03067
G3 X126.25 Y132.066 I-2.976 J-2.465 E.02738
G3 X123.651 Y130.39 I-.998 J-1.305 E.14538
G1 X123.82 Y129.798 E.02224
G3 X122.621 Y127.721 I4.475 J-3.969 E.08719
G1 X122.023 Y127.571 E.02224
G3 X122.023 Y124.429 I.488 J-1.571 E.15085
G1 X122.602 Y124.284 E.02154
G1 X122.94 Y123.505 E.03066
G3 X123.823 Y122.213 I5.506 J2.817 E.05666
G1 X123.651 Y121.61 E.02264
G3 X125.355 Y119.598 I1.603 J-.37 E.11042
G3 X126.372 Y120.039 I-.118 J1.669 E.04079
G1 X126.809 Y120.489 E.02265
G3 X128.369 Y120.37 I1.246 J6.04 E.05665
G1 X129.213 Y120.467 E.03067
G3 X129.75 Y119.934 I2.976 J2.465 E.02738
G3 X132.349 Y121.61 I.998 J1.305 E.14539
G1 X132.18 Y122.202 E.02224
G3 X133.379 Y124.279 I-4.475 J3.968 E.08719
M73 P5 R12
G3 X134.128 Y124.483 I-.661 J3.906 E.02808
G3 X133.977 Y127.571 I-.631 J1.517 E.14539
G1 X133.526 Y127.684 E.01676
M204 S6000
G1 X133.223 Y127.289 F30000
G1 F3000
M204 S500
G1 X133.068 Y127.328 E.00575
G1 X132.65 Y128.293 E.03799
G3 X131.67 Y129.678 I-5.51 J-2.858 E.06144
G1 X131.903 Y130.494 E.03065
G3 X129.94 Y131.627 I-1.157 J.262 E.10881
G1 X129.35 Y131.017 E.03067
G3 X127.661 Y131.173 I-1.409 J-6.026 E.06142
G1 X126.616 Y131.053 E.038
G1 X126.059 Y131.628 E.02888
G3 X124.097 Y130.494 I-.805 J-.872 E.10879
G1 X124.324 Y129.698 E.02991
G1 X123.786 Y129.02 E.03125
G3 X123.278 Y128.14 I4.208 J-3.016 E.03675
G1 X122.96 Y127.334 E.03126
G1 X122.156 Y127.133 E.02991
G3 X122.156 Y124.867 I.352 J-1.133 E.1088
G1 X122.932 Y124.672 E.02887
G1 X123.35 Y123.707 E.03799
G3 X124.33 Y122.322 I5.512 J2.859 E.06144
G1 X124.097 Y121.506 E.03065
G3 X125.325 Y120.055 I1.156 J-.267 E.07963
G3 X126.06 Y120.372 I-.085 J1.204 E.02943
G1 X126.65 Y120.983 E.03067
G3 X128.339 Y120.827 I1.409 J6.026 E.06142
G1 X129.384 Y120.947 E.038
G1 X129.941 Y120.372 E.02888
G3 X131.903 Y121.506 I.805 J.872 E.10879
G1 X131.676 Y122.302 E.02991
G1 X132.214 Y122.98 E.03125
G3 X132.722 Y123.861 I-4.216 J3.021 E.03676
G1 X133.04 Y124.665 E.03125
G1 X133.844 Y124.867 E.0299
G3 X133.844 Y127.133 I-.352 J1.133 E.10881
G1 X133.281 Y127.274 E.02095
M204 S6000
G1 X132.977 Y126.879 F30000
G1 F3000
M204 S500
G1 X132.738 Y126.939 E.00888
G1 X132.239 Y128.091 E.04532
G3 X131.75 Y128.877 I-4.24 J-2.091 E.03351
G1 X131.164 Y129.568 E.03272
G1 X131.458 Y130.598 E.03867
G3 X130.253 Y131.293 I-.71 J.161 E.06677
G1 X129.508 Y130.524 E.03868
G1 X128.617 Y130.686 E.03272
G3 X127.691 Y130.717 I-.617 J-4.687 E.0335
G1 X126.444 Y130.573 E.04532
G1 X125.747 Y131.294 E.03621
G3 X124.542 Y130.598 I-.494 J-.535 E.06675
G1 X124.828 Y129.597 E.03757
G1 X124.158 Y128.753 E.03892
G3 X123.695 Y127.951 I3.836 J-2.75 E.03351
G1 X123.298 Y126.948 E.03892
G1 X122.289 Y126.695 E.03757
G3 X122.289 Y125.305 I.216 J-.695 E.06676
G1 X123.262 Y125.061 E.0362
G1 X123.761 Y123.91 E.04532
G3 X124.25 Y123.123 I4.235 J2.088 E.03351
G1 X124.836 Y122.431 E.03272
G1 X124.542 Y121.402 E.03866
G3 X125.747 Y120.707 I.71 J-.161 E.06676
G1 X126.492 Y121.476 E.03869
G1 X127.383 Y121.314 E.03272
G3 X128.309 Y121.283 I.617 J4.687 E.03349
G1 X129.556 Y121.427 E.04533
G1 X130.253 Y120.706 E.03621
G3 X130.845 Y120.516 I.499 J.539 E.02315
G3 X131.458 Y121.402 I-.097 J.722 E.04376
G1 X131.172 Y122.403 E.03758
G1 X131.842 Y123.247 E.03892
G3 X132.305 Y124.049 I-3.845 J2.755 E.03351
G1 X132.702 Y125.052 E.03891
G1 X133.711 Y125.305 E.03757
G3 X133.711 Y126.695 I-.216 J.695 E.06677
G1 X133.035 Y126.865 E.02514
; WIPE_START
G1 X132.738 Y126.939 E-.11631
G1 X132.462 Y127.576 E-.26369
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I-.08 J-1.214 P1  F30000
G1 X124.581 Y128.098 Z.6
G1 Z.2
G1 E.4 F1800
G1 F3000
M204 S500
G1 X125.546 Y129.198 E.05284
G1 X126.957 Y129.893 E.05678
G1 X128.417 Y129.989 E.05285
G1 X128.419 Y130.244 E.0092
G3 X127.721 Y130.26 I-.431 J-3.542 E.02526
G1 X126.272 Y130.093 E.05265
G1 X125.414 Y130.977 E.04447
G1 X125.267 Y131.032 E.00565
G1 X125.139 Y131.008 E.00471
G1 X125.073 Y130.965 E.00285
G1 X125.009 Y130.882 E.0038
G1 X124.983 Y130.728 E.00563
G1 X125.332 Y129.497 E.04619
G1 X124.53 Y128.487 E.04658
G1 X124.378 Y128.251 E.01012
G1 X124.533 Y128.134 E.00703
; WIPE_START
G1 X125.223 Y128.858 E-.38
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I.069 J1.215 P1  F30000
G1 X131.116 Y128.526 Z.6
G1 Z.2
G1 E.4 F1800
G1 F3000
M204 S500
G1 X131.297 Y128.704 E.0092
G1 X130.657 Y129.459 E.03572
G1 X131.017 Y130.728 E.04763
G1 X130.991 Y130.882 E.00564
G1 X130.885 Y130.996 E.00564
G1 X130.733 Y131.032 E.00564
G1 X130.586 Y130.977 E.00564
G1 X129.667 Y130.03 E.04765
G1 X128.695 Y130.207 E.03567
G1 X128.631 Y129.961 E.0092
G1 X130.015 Y129.491 E.05279
G1 X131.071 Y128.565 E.05067
; WIPE_START
G1 X131.297 Y128.704 E-.10107
G1 X130.822 Y129.264 E-.27893
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I1.042 J.629 P1  F30000
G1 X132.276 Y126.856 Z.6
G1 Z.2
G1 E.4 F1800
G1 F3000
M204 S500
G1 X131.829 Y127.888 E.04062
G3 X131.465 Y128.485 I-3.216 J-1.548 E.02528
G1 X131.246 Y128.356 E.0092
G1 X131.893 Y127.043 E.05285
G1 X131.996 Y125.474 E.05678
G1 X131.526 Y124.088 E.05284
G1 X131.76 Y123.989 E.0092
G1 X131.889 Y124.238 E.01013
G1 X132.363 Y125.438 E.04658
G1 X133.603 Y125.751 E.04619
G1 X133.724 Y125.851 E.00564
G1 X133.769 Y126.002 E.00569
G1 X133.724 Y126.15 E.00559
G1 X133.603 Y126.249 E.00563
G1 X132.409 Y126.55 E.04448
G1 X132.3 Y126.801 E.00985
; WIPE_START
G1 X131.902 Y127.718 E-.38
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I1.207 J-.153 P1  F30000
G1 X131.419 Y123.902 Z.6
G1 Z.2
G1 E.4 F1800
G1 F3000
M204 S500
G1 X130.454 Y122.802 E.05283
G1 X129.043 Y122.107 E.05678
G1 X127.583 Y122.011 E.05285
G1 X127.581 Y121.756 E.0092
G3 X128.279 Y121.74 I.431 J3.542 E.02526
G1 X129.728 Y121.907 E.05265
G1 X130.566 Y121.04 E.04354
G1 X130.68 Y120.977 E.0047
G1 X130.785 Y120.97 E.00379
G1 X130.861 Y120.992 E.00285
G1 X130.946 Y121.053 E.0038
G1 X131.002 Y121.142 E.00379
G1 X131.019 Y121.246 E.00378
G1 X130.668 Y122.503 E.04713
G1 X131.47 Y123.513 E.04659
G1 X131.622 Y123.749 E.01011
G1 X131.466 Y123.866 E.00703
; WIPE_START
G1 X130.777 Y123.142 E-.38
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I.375 J-1.158 P1  F30000
G1 X127.369 Y122.039 Z.6
G1 Z.2
G1 E.4 F1800
G1 F3000
M204 S500
G1 X125.985 Y122.509 E.05279
G1 X124.884 Y123.474 E.05286
G1 X124.703 Y123.296 E.0092
G1 X125.343 Y122.541 E.03575
G1 X124.981 Y121.246 E.04855
G1 X124.998 Y121.142 E.00379
G1 X125.054 Y121.053 E.00379
M73 P6 R12
G1 X125.139 Y120.992 E.00378
G1 X125.266 Y120.968 E.00467
G1 X125.345 Y120.985 E.00291
G1 X125.434 Y121.041 E.00379
G1 X126.333 Y121.97 E.0467
G1 X127.305 Y121.793 E.03567
G1 X127.354 Y121.981 E.00703
; WIPE_START
G1 X126.421 Y122.341 E-.38
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I-.792 J-.924 P1  F30000
G1 X124.646 Y123.862 Z.6
G1 Z.2
G1 E.4 F1800
G1 F3000
M204 S500
G1 X124.107 Y124.957 E.04406
G1 X124.004 Y126.526 E.05679
G1 X124.474 Y127.912 E.05284
G1 X124.24 Y128.011 E.0092
G1 X124.111 Y127.762 E.01013
G1 X123.637 Y126.562 E.04659
G1 X122.397 Y126.249 E.04619
G1 X122.275 Y126.148 E.00569
G1 X122.231 Y126 E.00559
G1 X122.276 Y125.851 E.00563
G1 X122.397 Y125.751 E.00564
G1 X123.591 Y125.45 E.04448
G1 X124.171 Y124.112 E.05264
G3 X124.535 Y123.515 I3.211 J1.544 E.02529
G1 X124.754 Y123.644 E.0092
G1 X124.673 Y123.808 E.00663
; WIPE_START
G1 X124.231 Y124.705 E-.38
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I.1 J1.213 P1  F30000
G1 X126.462 Y124.522 Z.6
G1 Z.2
G1 E.4 F1800
; FEATURE: Outer wall
G1 F3000
M204 S500
G1 X126.917 Y124.124 E.02182
G1 X127.326 Y123.985 E.01558
G1 X127.717 Y123.852 E.01493
G1 X128.561 Y123.907 E.03052
G1 X129.319 Y124.281 E.03052
G1 X129.876 Y124.917 E.03052
G1 X130.148 Y125.717 E.03052
G1 X130.093 Y126.561 E.03052
G1 X129.719 Y127.319 E.03052
G1 X129.083 Y127.876 E.03052
G1 X128.283 Y128.148 E.03052
G1 X127.439 Y128.093 E.03052
G1 X126.681 Y127.719 E.03052
G1 X126.124 Y127.083 E.03052
G1 X125.852 Y126.283 E.03052
G1 X125.907 Y125.439 E.03052
G1 X126.281 Y124.681 E.03052
G1 X126.417 Y124.562 E.00654
M204 S6000
G1 X126.161 Y124.178 F30000
; FEATURE: Inner wall
G1 F3000
M204 S500
G1 X126.684 Y123.72 E.0251
G1 X127.179 Y123.552 E.01887
G1 X127.656 Y123.39 E.01822
G1 X128.681 Y123.457 E.03709
G1 X129.603 Y123.911 E.03709
G1 X130.28 Y124.684 E.03709
G1 X130.61 Y125.656 E.03709
G1 X130.543 Y126.681 E.03709
G1 X130.089 Y127.603 E.03709
G1 X129.316 Y128.28 E.03709
G1 X128.344 Y128.61 E.03709
G1 X127.319 Y128.543 E.03709
G1 X126.397 Y128.089 E.03709
G1 X125.72 Y127.316 E.03709
G1 X125.39 Y126.344 E.03709
G1 X125.457 Y125.319 E.03709
G1 X125.911 Y124.397 E.03709
G1 X126.116 Y124.218 E.00982
M204 S6000
G1 X125.86 Y123.835 F30000
G1 F3000
M204 S500
G1 X126.451 Y123.316 E.02839
G1 X127.032 Y123.119 E.02215
G1 X127.595 Y122.928 E.02149
G1 X128.802 Y123.007 E.04366
G1 X129.886 Y123.542 E.04365
G1 X130.684 Y124.451 E.04365
G1 X131.072 Y125.596 E.04366
G1 X130.993 Y126.802 E.04365
G1 X130.458 Y127.886 E.04366
G1 X129.549 Y128.684 E.04365
G1 X128.405 Y129.072 E.04365
G1 X127.198 Y128.993 E.04366
G1 X126.114 Y128.458 E.04365
G1 X125.316 Y127.549 E.04366
G1 X124.928 Y126.405 E.04365
G1 X125.007 Y125.198 E.04366
G1 X125.542 Y124.114 E.04366
G1 X125.815 Y123.874 E.0131
M204 S6000
G1 X125.558 Y123.491 F30000
G1 F3000
M204 S500
G1 X126.218 Y122.913 E.03167
G1 X126.885 Y122.686 E.02544
G1 X127.535 Y122.466 E.02477
G1 X128.923 Y122.557 E.05022
G1 X130.17 Y123.172 E.05022
G1 X131.087 Y124.218 E.05022
G1 X131.534 Y125.535 E.05022
G1 X131.443 Y126.923 E.05022
G1 X130.828 Y128.17 E.05022
G1 X129.782 Y129.087 E.05022
G1 X128.465 Y129.534 E.05022
G1 X127.077 Y129.443 E.05022
G1 X125.83 Y128.828 E.05022
G1 X124.913 Y127.782 E.05022
G1 X124.466 Y126.465 E.05022
G1 X124.557 Y125.077 E.05022
G1 X125.172 Y123.83 E.05022
G1 X125.513 Y123.531 E.01638
; WIPE_START
G1 X126.218 Y122.913 E-.35611
G1 X126.277 Y122.893 E-.0239
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I-.896 J-.823 P1  F30000
G1 X123.812 Y125.577 Z.6
G1 Z.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.112238
G1 F3000
M204 S500
G1 X123.792 Y125.66 E.00046
; LINE_WIDTH: 0.140692
G1 X123.461 Y126.282 E.00545
; WIPE_START
G1 X123.792 Y125.66 E-.38
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I-1.126 J.462 P1  F30000
G1 X125.486 Y129.79 Z.6
G1 Z.2
G1 E.4 F1800
; LINE_WIDTH: 0.140689
G1 F3000
M204 S500
G1 X126.191 Y129.814 E.00545
; LINE_WIDTH: 0.112237
G1 X126.272 Y129.838 E.00046
; WIPE_START
G1 X126.191 Y129.814 E-.38
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I.599 J1.059 P1  F30000
G1 X132.188 Y126.422 Z.6
G1 Z.2
G1 E.4 F1800
; LINE_WIDTH: 0.112212
G1 F3000
M204 S500
G1 X132.208 Y126.34 E.00046
; LINE_WIDTH: 0.140614
G1 X132.539 Y125.718 E.00544
; WIPE_START
G1 X132.208 Y126.34 E-.38
; WIPE_END
G1 E-.02 F1800
M204 S6000
G17
G3 Z.6 I1.047 J-.621 P1  F30000
G1 X129.728 Y122.162 Z.6
G1 Z.2
G1 E.4 F1800
; LINE_WIDTH: 0.112179
G1 F3000
M204 S500
G1 X129.809 Y122.186 E.00046
; LINE_WIDTH: 0.140546
G1 X130.514 Y122.21 E.00544
M204 S6000
G1 X130.717 Y121.499 F30000
; LINE_WIDTH: 0.119212
G1 F3000
M204 S500
G1 X130.763 Y121.199 E.00182
; CHANGE_LAYER
; Z_HEIGHT: 0.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F3000
G1 X130.717 Y121.499 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 2/50
; update layer progress
M73 L2
M991 S0 P1 ;notify layer change
; open powerlost recovery
M1003 S1
M976 S1 P1 ; scan model before printing 2nd layer
M400 P100
G1 E.4
M104 S255 ; set nozzle temperature
; OBJECT_ID: 15
G1 E-.4
M204 S10000
G17
G3 Z.6 I-.353 J-1.165 P1  F30000
G1 X125.237 Y123.162 Z.6
G1 Z.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1988
G1 X125.984 Y122.507 E.03192
G1 X126.455 Y122.347 E.01601
G1 X127.474 Y122.002 E.03458
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.801 Y123.545 E.0506
G1 X125.192 Y123.201 E.01675
G1 X125.506 Y123.468 F30000
G1 F1988
G1 X126.191 Y122.867 E.02932
G1 X126.586 Y122.733 E.01341
G1 X127.528 Y122.413 E.03198
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X125.13 Y123.798 E.04539
G1 X125.461 Y123.508 E.01415
G1 X125.774 Y123.774 F30000
G1 F1988
G1 X126.399 Y123.226 E.02671
G1 X126.717 Y123.118 E.0108
G1 X127.582 Y122.825 E.02938
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04018
G1 X126.05 Y128.541 E.04019
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04019
G1 X125.459 Y124.05 E.04019
G1 X125.729 Y123.814 E.01154
G1 X126.043 Y124.08 F30000
G1 F1988
G1 X126.606 Y123.586 E.02411
G1 X126.848 Y123.504 E.0082
G1 X127.636 Y123.236 E.02677
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.279 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.278 E.03498
G1 X125.788 Y124.303 E.03498
G1 X125.997 Y124.12 E.00894
G1 X126.311 Y124.386 F30000
G1 F1988
G1 X126.814 Y123.945 E.0215
G1 X126.978 Y123.889 E.00559
G1 X127.69 Y123.648 E.02417
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
M73 P7 R12
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.118 Y124.556 E.02977
G1 X126.266 Y124.426 E.00634
M204 S250
G1 X126.569 Y124.681 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1988
M204 S5000
G1 X127.014 Y124.291 E.01759
G1 X127.104 Y124.261 E.00286
G1 X127.742 Y124.044 E.02007
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.435 Y124.799 E.02293
G1 X126.524 Y124.72 E.00355
; WIPE_START
G1 F11933.819
M204 S10000
G1 X127.014 Y124.291 E-.24726
G1 X127.104 Y124.261 E-.03646
G1 X127.344 Y124.179 E-.09629
; WIPE_END
G1 E-.02 F1800
G17
G3 Z.8 I-.591 J1.064 P1  F30000
G1 X132.252 Y126.906 Z.8
G1 Z.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1988
G1 X131.827 Y127.887 E.03437
G3 X131.37 Y128.615 I-3.375 J-1.61 E.02771
G1 X130.655 Y129.458 E.03555
G1 X131.015 Y130.728 E.04244
G1 X130.989 Y130.881 E.00499
G1 X130.884 Y130.994 E.00497
G1 X130.733 Y131.03 E.00499
G1 X130.588 Y130.975 E.00498
G1 X129.668 Y130.028 E.04244
G1 X128.534 Y130.232 E.03706
G3 X127.721 Y130.258 I-.536 J-4.113 E.02619
G1 X126.271 Y130.091 E.04691
G1 X125.413 Y130.975 E.03963
G1 X125.344 Y131.013 E.00252
G1 X125.241 Y131.03 E.00335
G1 X125.164 Y131.016 E.00252
G1 X125.091 Y130.977 E.00266
G1 X125 Y130.857 E.00484
G1 X124.985 Y130.728 E.00418
G1 X125.334 Y129.497 E.04115
G1 X124.532 Y128.485 E.04152
G1 X124.292 Y128.114 E.0142
G1 X124.113 Y127.761 E.01273
G1 X123.639 Y126.56 E.04152
G1 X122.423 Y126.256 E.04031
G1 X122.331 Y126.206 E.00335
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00336
G1 X122.244 Y125.923 E.00334
G1 X122.294 Y125.831 E.00335
G1 X122.374 Y125.765 E.00335
G1 X123.593 Y125.451 E.04046
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.374 J1.61 E.0277
G1 X125.345 Y122.542 E.03555
G1 X124.985 Y121.272 E.04244
G1 X125.011 Y121.119 E.00499
G1 X125.117 Y121.006 E.00498
G1 X125.263 Y120.97 E.00484
G1 X125.344 Y120.987 E.00266
G1 X125.413 Y121.025 E.00252
G1 X126.333 Y121.972 E.04245
G1 X127.466 Y121.768 E.03703
G3 X128.279 Y121.742 I.536 J4.116 E.02621
G1 X129.729 Y121.909 E.04691
G1 X130.568 Y121.042 E.0388
G1 X130.681 Y120.979 E.00416
G1 X130.785 Y120.972 E.00335
G1 X130.86 Y120.994 E.00252
G1 X130.942 Y121.052 E.00325
G1 X131 Y121.143 E.00345
G1 X131.017 Y121.246 E.00335
G1 X130.666 Y122.503 E.04199
G1 X131.468 Y123.515 E.04152
G1 X131.708 Y123.886 E.01421
G1 X131.887 Y124.239 E.01272
G1 X132.361 Y125.44 E.04152
G1 X133.602 Y125.753 E.04117
G1 X133.706 Y125.831 E.00417
G1 X133.761 Y125.945 E.00406
G1 X133.766 Y126.026 E.00262
G1 X133.735 Y126.126 E.00336
G1 X133.689 Y126.189 E.00251
G1 X133.602 Y126.247 E.00335
G1 X132.407 Y126.549 E.03964
G1 X132.276 Y126.851 E.01061
G1 X132.577 Y127.181 F30000
G1 F1988
G1 X132.193 Y128.067 E.03106
G3 X131.709 Y128.846 I-4.194 J-2.068 E.02952
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03525
G3 X130.289 Y131.255 I-.659 J.149 E.0552
G1 X129.527 Y130.468 E.03524
G1 X128.61 Y130.635 E.02995
G3 X127.694 Y130.665 I-.61 J-4.637 E.02952
G1 X126.424 Y130.518 E.0411
G1 X125.711 Y131.256 E.03298
G3 X124.593 Y130.61 I-.458 J-.497 E.05517
G1 X124.885 Y129.586 E.03425
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.798 J-2.722 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.646 E.03423
G3 X122.304 Y125.354 I.2 J-.646 E.05521
G1 X123.299 Y125.105 E.03297
G1 X123.808 Y123.933 E.04111
G3 X124.292 Y123.154 I4.194 J2.068 E.02952
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.745 I.659 J-.149 E.05519
G1 X126.474 Y121.532 E.03526
G1 X127.39 Y121.365 E.02995
G3 X128.306 Y121.336 I.61 J4.635 E.02951
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.744 E.03298
G3 X130.838 Y120.568 I.464 J.5 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.798 J2.722 E.02951
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.645 I-.2 J.645 E.0552
G1 X132.701 Y126.895 E.03299
G1 X132.601 Y127.126 E.00811
G1 X132.901 Y127.456 F30000
G1 F1988
G1 X132.558 Y128.248 E.02774
G3 X131.557 Y129.653 I-5.532 J-2.88 E.05567
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.057 J.239 E.08855
G1 X129.385 Y130.907 E.02889
G3 X127.668 Y131.071 I-1.446 J-6.071 E.05567
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.518 I-.736 J-.797 E.08851
G1 X124.437 Y129.675 E.02817
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.129 J-2.959 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02815
G3 X122.186 Y124.964 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.03529
G3 X124.443 Y122.347 I5.532 J2.88 E.05567
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.057 J-.239 E.08854
G1 X126.615 Y121.093 E.0289
G3 X128.332 Y120.929 I1.446 J6.06 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.129 J2.959 E.03208
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.035 I-.321 J1.035 E.08855
G1 X132.995 Y127.241 E.02718
G1 X132.925 Y127.401 E.00561
G1 X133.226 Y127.731 F30000
G1 F1988
G1 X132.924 Y128.428 E.02443
G3 X132.008 Y129.751 I-5.484 J-2.816 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.33 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.027 E.05188
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.097 E.12186
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08124
G1 X122.068 Y127.426 E.02207
G3 X122.068 Y124.574 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.484 J2.816 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.456 J-.329 E.12189
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.018 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.945 Y119.76 I1.024 J1.105 E.04229
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.557 J4.079 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.933 Y127.425 I-.442 J1.425 E.1219
G1 X133.288 Y127.587 E.02136
G1 X133.25 Y127.676 E.00311
G1 X133.55 Y128.006 F30000
G1 F1988
G1 X133.289 Y128.608 E.02112
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.073 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.657 J-1.788 E.13136
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.875 E.03393
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07178
G3 X123.357 Y121.113 I2.742 J-1.021 E.03412
G3 X125.367 Y119.344 I1.914 J.148 E.0953
G3 X126.547 Y119.852 I-.131 J1.927 E.04212
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.071 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.788 E.13136
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01555
G1 X133.574 Y127.951 E.00062
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1988
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
M73 P8 R12
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19224
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.392 Y118.952 I2.166 J-.8 E.13595
G3 X127.033 Y119.791 I-.215 J2.444 E.05627
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19225
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.1905
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.227
G1 X133.446 Y129.134 E-.153
; WIPE_END
G1 E-.02 F1800
G17
G3 Z.8 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z.8
G1 Z.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113554
G1 F1988
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146815
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.17811
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207444
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z.8 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z.8
G1 Z.4
G1 E.4 F1800
; LINE_WIDTH: 0.207559
G1 F1988
G1 X130.168 Y122.195 E.00482
; LINE_WIDTH: 0.178206
G1 X129.798 Y122.182 E.00396
; LINE_WIDTH: 0.146879
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113574
G1 X129.585 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z.8 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z.8
G1 Z.4
G1 E.4 F1800
; LINE_WIDTH: 0.113563
G1 F1988
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146842
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.178142
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.207493
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z.8 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z.8
G1 Z.4
G1 E.4 F1800
; LINE_WIDTH: 0.20745
G1 F1988
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178117
G1 X126.202 Y129.818 E.00396
; LINE_WIDTH: 0.146816
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113553
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 0.6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 3/50
; update layer progress
M73 L3
M991 S0 P2 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z.8 I1.201 J-.197 P1  F30000
G1 X125.216 Y123.181 Z.8
G1 Z.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1982
G1 X125.984 Y122.507 E.03285
G1 X126.489 Y122.336 E.01717
G1 X127.474 Y122.002 E.03342
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.801 Y123.545 E.0506
G1 X125.171 Y123.22 E.01583
G1 X125.484 Y123.487 F30000
G1 F1982
G1 X126.191 Y122.867 E.03024
G1 X126.62 Y122.721 E.01457
G1 X127.528 Y122.413 E.03082
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X125.13 Y123.798 E.04539
G1 X125.439 Y123.527 E.01322
G1 X125.753 Y123.793 F30000
G1 F1982
G1 X126.399 Y123.226 E.02764
G1 X126.751 Y123.107 E.01196
G1 X127.582 Y122.825 E.02822
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04018
G1 X126.05 Y128.541 E.04019
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.459 Y124.05 E.04019
G1 X125.707 Y123.833 E.01062
G1 X126.021 Y124.099 F30000
G1 F1982
G1 X126.606 Y123.586 E.02503
G1 X126.882 Y123.492 E.00936
G1 X127.636 Y123.236 E.02561
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.279 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.788 Y124.303 E.03498
G1 X125.976 Y124.139 E.00802
G1 X126.289 Y124.405 F30000
G1 F1982
G1 X126.814 Y123.945 E.02243
G1 X127.013 Y123.878 E.00676
G1 X127.69 Y123.648 E.02301
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.118 Y124.556 E.02977
G1 X126.244 Y124.445 E.00541
M204 S250
G1 X126.548 Y124.7 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1982
M204 S5000
G1 X127.014 Y124.291 E.01845
G1 X127.139 Y124.249 E.00393
G1 X127.742 Y124.044 E.01899
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.435 Y124.799 E.02293
G1 X126.503 Y124.739 E.00269
; WIPE_START
G1 F11933.819
M204 S10000
G1 X127.014 Y124.291 E-.25817
G1 X127.139 Y124.249 E-.05018
G1 X127.317 Y124.188 E-.07165
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1 I-.587 J1.066 P1  F30000
G1 X132.252 Y126.906 Z1
G1 Z.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1982
M73 P8 R11
G1 X131.827 Y127.887 E.0344
G3 X131.37 Y128.616 I-3.347 J-1.593 E.0277
G1 X130.655 Y129.458 E.03555
G1 X131.015 Y130.728 E.04244
G1 X130.989 Y130.881 E.00499
G1 X130.884 Y130.994 E.00498
G1 X130.74 Y131.03 E.00475
G1 X130.656 Y131.013 E.00276
G1 X130.588 Y130.975 E.00252
G1 X129.668 Y130.029 E.04244
G1 X128.533 Y130.232 E.03707
G3 X127.721 Y130.258 I-.535 J-4.113 E.02618
G1 X126.271 Y130.091 E.04691
G1 X125.413 Y130.975 E.03963
G1 X125.319 Y131.021 E.00335
G1 X125.241 Y131.03 E.00252
G1 X125.095 Y130.98 E.00498
G1 X125 Y130.857 E.00499
G1 X124.985 Y130.728 E.00418
G1 X125.334 Y129.497 E.04115
G1 X124.532 Y128.486 E.04152
G1 X124.292 Y128.114 E.01421
G1 X124.113 Y127.761 E.01272
G1 X123.639 Y126.56 E.04153
G1 X122.422 Y126.255 E.04033
G1 X122.331 Y126.206 E.00334
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00335
G1 X122.244 Y125.923 E.00334
G1 X122.289 Y125.837 E.00311
G1 X122.374 Y125.765 E.00359
G1 X123.593 Y125.451 E.04046
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.363 J1.603 E.0277
G1 X125.345 Y122.542 E.03555
G1 X124.985 Y121.272 E.04244
G1 X125.011 Y121.119 E.00499
G1 X125.117 Y121.006 E.00499
G1 X125.26 Y120.97 E.00475
G1 X125.344 Y120.987 E.00276
G1 X125.413 Y121.025 E.00252
G1 X126.332 Y121.972 E.04245
G1 X127.466 Y121.768 E.03705
G3 X128.279 Y121.742 I.536 J4.115 E.02619
G1 X129.728 Y121.909 E.04692
G1 X130.567 Y121.042 E.0388
G1 X130.656 Y120.987 E.00335
G1 X130.777 Y120.972 E.00393
G1 X130.86 Y120.994 E.00276
G1 X130.941 Y121.05 E.00317
G1 X131 Y121.143 E.00353
G1 X131.017 Y121.245 E.00335
G1 X130.666 Y122.503 E.04199
G1 X131.468 Y123.515 E.04152
G1 X131.708 Y123.886 E.0142
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04152
G1 X133.602 Y125.753 E.04116
G1 X133.703 Y125.827 E.004
G1 X133.762 Y125.948 E.00435
G1 X133.762 Y126.052 E.00334
G1 X133.735 Y126.126 E.00252
G1 X133.689 Y126.189 E.00251
G1 X133.602 Y126.247 E.00335
G1 X132.407 Y126.549 E.03963
G1 X132.276 Y126.851 E.0106
G1 X132.577 Y127.181 F30000
G1 F1982
G1 X132.192 Y128.068 E.03108
G3 X131.709 Y128.845 I-4.191 J-2.067 E.0295
G1 X131.106 Y129.556 E.02996
G1 X131.407 Y130.61 E.03525
G3 X130.289 Y131.255 I-.659 J.149 E.0552
G1 X129.527 Y130.468 E.03524
G1 X128.61 Y130.635 E.02995
G3 X127.694 Y130.665 I-.61 J-4.638 E.02953
G1 X126.424 Y130.518 E.0411
G1 X125.711 Y131.256 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.886 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.797 J-2.721 E.02952
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
M73 P9 R11
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.155 I4.194 J2.068 E.0295
G1 X124.894 Y122.444 E.02996
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.744 I.659 J-.149 E.05518
G1 X126.474 Y121.532 E.03526
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.335 I.61 J4.635 E.0295
G1 X129.576 Y121.482 E.04111
G1 X130.289 Y120.745 E.03298
G3 X130.829 Y120.567 I.463 J.499 E.01887
G3 X131.407 Y121.39 I-.081 J.671 E.03645
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.801 J2.723 E.02951
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X132.701 Y126.895 E.03298
G1 X132.601 Y127.126 E.0081
G1 X132.901 Y127.456 F30000
G1 F1982
G1 X132.558 Y128.248 E.02777
G3 X131.557 Y129.653 I-5.531 J-2.88 E.05566
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.057 J.239 E.08854
G1 X129.385 Y130.907 E.02889
G3 X127.668 Y131.071 I-1.446 J-6.077 E.05567
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.127 J-2.958 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.532 J2.881 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.058 J-.239 E.08854
G1 X126.615 Y121.093 E.0289
G3 X128.332 Y120.929 I1.446 J6.064 E.05566
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.882 Y120.163 I.743 J.801 E.0304
G3 X131.804 Y121.483 I-.134 J1.076 E.05834
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.131 J2.96 E.03208
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08855
G1 X132.995 Y127.241 E.02717
G1 X132.925 Y127.401 E.0056
G1 X133.226 Y127.73 F30000
G1 F1982
G1 X132.923 Y128.428 E.02445
G3 X132.008 Y129.751 I-5.483 J-2.816 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.301 J-6.035 E.05188
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.425 E.02208
G3 X122.068 Y124.575 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.483 J2.816 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.456 J-.329 E.12189
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.023 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.934 Y119.759 I1.023 J1.103 E.04194
G3 X132.201 Y121.575 I-.187 J1.481 E.08023
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.425 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.25 Y127.675 E.0031
G1 X133.55 Y128.005 F30000
G1 F1982
G1 X133.289 Y128.608 E.02114
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01618
G3 X126.883 Y131.8 I-1.149 J-6.074 E.07178
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13136
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.362 Y119.344 I1.913 J.148 E.09515
G3 X126.547 Y119.852 I-.125 J1.925 E.04226
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.069 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.788 E.13137
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01554
G1 X133.574 Y127.95 E.0006
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1982
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.579 J2.112 E.05794
G3 X125.387 Y118.952 I2.166 J-.8 E.13579
G3 X127.033 Y119.791 I-.208 J2.443 E.05642
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.92 E.05349
G3 X132.893 Y122.06 I1.77 J1.468 E.19223
G3 X133.859 Y123.732 I-4.113 J3.49 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22704
G1 X133.446 Y129.134 E-.15296
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z1
G1 Z.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113554
G1 F1982
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146815
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178126
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207462
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z1
G1 Z.6
G1 E.4 F1800
; LINE_WIDTH: 0.207274
G1 F1982
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.177977
G1 X129.798 Y122.182 E.00395
; LINE_WIDTH: 0.146725
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113521
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z1
G1 Z.6
G1 E.4 F1800
; LINE_WIDTH: 0.113559
G1 F1982
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146828
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.17812
G1 X123.621 Y125.975 E.00395
; LINE_WIDTH: 0.20746
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z1
G1 Z.6
G1 E.4 F1800
; LINE_WIDTH: 0.20743
G1 F1982
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178097
G1 X126.202 Y129.818 E.00395
; LINE_WIDTH: 0.146814
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113552
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 0.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 4/50
; update layer progress
M73 L4
M991 S0 P3 ;notify layer change
M106 S99.45
; OBJECT_ID: 15
G17
G3 Z1 I1.2 J-.201 P1  F30000
G1 X125.193 Y123.201 Z1
G1 Z.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X125.984 Y122.507 E.03382
G1 X126.523 Y122.324 E.01833
G1 X127.474 Y122.002 E.03227
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
M73 P10 R11
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.801 Y123.545 E.0506
G1 X125.148 Y123.241 E.01485
G1 X125.461 Y123.507 F30000
G1 F1983
G1 X126.191 Y122.867 E.03122
G1 X126.654 Y122.71 E.01573
G1 X127.528 Y122.413 E.02966
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X125.13 Y123.798 E.04539
G1 X125.416 Y123.547 E.01224
G1 X125.73 Y123.813 F30000
G1 F1983
G1 X126.399 Y123.226 E.02861
G1 X126.785 Y123.095 E.01312
G1 X127.582 Y122.825 E.02706
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.459 Y124.05 E.04019
G1 X125.685 Y123.853 E.00964
G1 X125.998 Y124.119 F30000
G1 F1983
G1 X126.606 Y123.586 E.02601
G1 X126.916 Y123.481 E.01052
G1 X127.636 Y123.236 E.02446
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.788 Y124.303 E.03498
G1 X125.953 Y124.159 E.00704
G1 X126.266 Y124.425 F30000
G1 F1983
G1 X126.814 Y123.945 E.02341
G1 X127.047 Y123.866 E.00792
G1 X127.69 Y123.648 E.02185
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.118 Y124.556 E.02977
G1 X126.221 Y124.465 E.00443
M204 S250
G1 X126.525 Y124.72 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X127.014 Y124.291 E.01936
G1 X127.173 Y124.237 E.00501
G1 X127.742 Y124.044 E.01792
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.435 Y124.799 E.02293
G1 X126.48 Y124.759 E.00179
; WIPE_START
G1 F11933.819
M204 S10000
G1 X127.014 Y124.291 E-.26975
G1 X127.173 Y124.237 E-.06391
G1 X127.288 Y124.198 E-.04635
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.2 I-.583 J1.068 P1  F30000
G1 X132.252 Y126.906 Z1.2
G1 Z.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03441
G3 X131.37 Y128.616 I-3.371 J-1.608 E.0277
G1 X130.655 Y129.458 E.03554
G1 X131.015 Y130.728 E.04245
G1 X130.989 Y130.881 E.00498
G1 X130.884 Y130.994 E.00498
G1 X130.733 Y131.03 E.00498
G1 X130.588 Y130.975 E.00499
G1 X129.668 Y130.028 E.04245
G1 X128.534 Y130.232 E.03705
G3 X127.721 Y130.258 I-.536 J-4.115 E.02619
G1 X126.271 Y130.091 E.04692
G1 X125.391 Y130.99 E.04046
G1 X125.294 Y131.027 E.00335
G1 X125.189 Y131.023 E.00335
G1 X125.095 Y130.98 E.00335
G1 X125.023 Y130.904 E.00335
G1 X124.987 Y130.807 E.00335
G1 X124.99 Y130.702 E.00335
G1 X125.334 Y129.497 E.04032
G1 X124.531 Y128.485 E.04153
G1 X124.292 Y128.114 E.0142
G1 X124.113 Y127.761 E.01272
G1 X123.639 Y126.56 E.04153
G1 X122.398 Y126.247 E.04115
G1 X122.278 Y126.148 E.00498
G1 X122.234 Y126.026 E.00418
G1 X122.244 Y125.923 E.00333
G1 X122.278 Y125.852 E.00253
G1 X122.398 Y125.753 E.00498
G1 X123.593 Y125.452 E.03963
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.384 I3.37 J1.607 E.02772
G1 X125.345 Y122.542 E.03554
G1 X124.983 Y121.246 E.04327
G1 X125 Y121.143 E.00336
G1 X125.055 Y121.054 E.00334
G1 X125.14 Y120.994 E.00335
G1 X125.257 Y120.97 E.00383
G1 X125.344 Y120.987 E.00286
G1 X125.433 Y121.042 E.00334
G1 X126.332 Y121.972 E.04161
G1 X127.466 Y121.768 E.03704
G3 X128.279 Y121.742 I.536 J4.116 E.02621
G1 X129.729 Y121.909 E.04691
G1 X130.588 Y121.025 E.03963
G1 X130.681 Y120.979 E.00334
G1 X130.759 Y120.97 E.00253
G1 X130.836 Y120.984 E.00252
G1 X130.914 Y121.027 E.00286
G1 X131 Y121.143 E.00465
G1 X131.015 Y121.272 E.00418
G1 X130.666 Y122.503 E.04116
G1 X131.468 Y123.514 E.04151
G1 X131.708 Y123.886 E.01421
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04153
G1 X133.578 Y125.745 E.04033
G1 X133.669 Y125.794 E.00334
G1 X133.735 Y125.874 E.00335
G1 X133.766 Y125.974 E.00335
G1 X133.756 Y126.077 E.00334
G1 X133.706 Y126.17 E.00337
G1 X133.626 Y126.235 E.00333
G1 X132.407 Y126.549 E.04047
G1 X132.276 Y126.851 E.01059
G1 X133.003 Y126.819 F30000
G1 F1983
G1 X132.701 Y126.895 E.01002
G1 X132.192 Y128.068 E.04111
G3 X131.709 Y128.846 I-4.191 J-2.067 E.02951
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03525
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.526 Y130.468 E.03525
G1 X128.61 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.634 E.02951
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.255 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.799 J-2.722 E.02951
G1 X123.337 Y126.904 E.03545
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.299 Y125.105 E.03298
G1 X123.807 Y123.933 E.04111
G3 X124.291 Y123.154 I4.194 J2.069 E.02951
G1 X124.894 Y122.444 E.02996
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.745 I.659 J-.149 E.05519
G1 X126.474 Y121.532 E.03526
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.336 I.61 J4.635 E.02951
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.745 E.03298
G3 X130.826 Y120.567 I.462 J.498 E.01875
G3 X131.407 Y121.39 I-.077 J.671 E.03656
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03543
G3 X132.258 Y124.071 I-3.798 J2.722 E.02952
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03425
G3 X133.696 Y126.645 I-.202 J.645 E.05514
G1 X133.061 Y126.804 E.02104
G1 X132.902 Y127.455 F30000
G1 F1983
G1 X132.558 Y128.248 E.02778
G3 X131.557 Y129.653 I-5.532 J-2.88 E.05566
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X127.668 Y131.071 I-1.446 J-6.063 E.05566
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.098 I4.13 J-2.96 E.03208
G1 X123.035 Y127.248 E.02937
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G3 X124.443 Y122.347 I5.532 J2.88 E.05567
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.057 J-.239 E.08854
G1 X126.615 Y121.093 E.0289
G3 X128.333 Y120.929 I1.446 J6.06 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.877 Y120.163 I.742 J.8 E.03027
G3 X131.804 Y121.483 I-.13 J1.076 E.05847
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02935
G3 X132.629 Y123.903 I-4.128 J2.959 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.035 I-.323 J1.035 E.08848
G1 X132.995 Y127.241 E.02717
G1 X132.925 Y127.4 E.00559
G1 X133.226 Y127.73 F30000
G1 F1983
G1 X132.923 Y128.428 E.02446
G3 X132.008 Y129.751 I-5.483 J-2.816 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.33 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.022 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.081 E.08124
G1 X122.068 Y127.426 E.02208
M73 P11 R11
G3 X122.068 Y124.574 I.443 J-1.426 E.12189
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.484 J2.816 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.456 J-.329 E.12189
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.019 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.929 Y119.759 I1.022 J1.102 E.0418
G3 X132.201 Y121.575 I-.183 J1.481 E.08037
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08124
G1 X133.933 Y124.575 E.02208
G3 X133.933 Y127.425 I-.444 J1.425 E.12182
G1 X133.288 Y127.587 E.02136
G1 X133.25 Y127.675 E.00309
G1 X133.551 Y128.005 F30000
G1 F1983
G1 X133.289 Y128.608 E.02115
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.332 J-3.78 E.07165
G3 X121.446 Y127.577 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.115 E.07178
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X125.358 Y119.343 I1.913 J.147 E.09499
G3 X126.547 Y119.852 I-.119 J1.924 E.04242
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.15 J6.071 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.788 E.13137
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.873 E.03393
G3 X134.051 Y127.815 I-1.058 J1.577 E.13764
G1 X133.582 Y127.933 E.01555
G1 X133.574 Y127.95 E.00059
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.922 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.114 J-3.49 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.382 Y118.952 I2.166 J-.8 E.13564
G3 X127.033 Y119.791 I-.201 J2.441 E.05657
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.775 J1.459 E.19268
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X133.924 Y128.256 I-.37 J2.268 E.1909
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22696
G1 X133.445 Y129.134 E-.15304
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.2 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z1.2
G1 Z.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113559
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146829
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178124
G1 X132.379 Y126.025 E.00395
; LINE_WIDTH: 0.207461
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.2 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z1.2
G1 Z.8
G1 E.4 F1800
; LINE_WIDTH: 0.207557
G1 F1983
G1 X130.168 Y122.195 E.00482
; LINE_WIDTH: 0.178206
G1 X129.798 Y122.182 E.00396
; LINE_WIDTH: 0.146877
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113574
G1 X129.585 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.2 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z1.2
G1 Z.8
G1 E.4 F1800
; LINE_WIDTH: 0.113564
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146842
G1 X123.795 Y125.649 E.00091
; LINE_WIDTH: 0.178141
G1 X123.621 Y125.975 E.00395
; LINE_WIDTH: 0.207493
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.2 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z1.2
G1 Z.8
G1 E.4 F1800
; LINE_WIDTH: 0.207386
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178056
G1 X126.202 Y129.818 E.00395
; LINE_WIDTH: 0.146779
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113538
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 1
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 5/50
; update layer progress
M73 L5
M991 S0 P4 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z1.2 I1.199 J-.206 P1  F30000
G1 X125.169 Y123.222 Z1.2
G1 Z1
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X125.984 Y122.507 E.03485
G1 X126.558 Y122.313 E.01949
G1 X127.474 Y122.002 E.03111
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.801 Y123.545 E.0506
G1 X125.124 Y123.262 E.01382
G1 X125.437 Y123.528 F30000
G1 F1983
G1 X126.191 Y122.867 E.03225
G1 X126.688 Y122.698 E.01689
G1 X127.528 Y122.413 E.0285
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X125.13 Y123.798 E.04539
G1 X125.392 Y123.568 E.01121
G1 X125.706 Y123.834 F30000
G1 F1983
G1 X126.399 Y123.226 E.02964
G1 X126.819 Y123.084 E.01428
G1 X127.582 Y122.825 E.0259
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.459 Y124.05 E.04019
G1 X125.66 Y123.874 E.00861
G1 X125.974 Y124.14 F30000
G1 F1983
G1 X126.606 Y123.586 E.02704
G1 X126.95 Y123.469 E.01168
G1 X127.636 Y123.236 E.0233
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.788 Y124.303 E.03498
G1 X125.929 Y124.18 E.00601
G1 X126.242 Y124.446 F30000
G1 F1983
G1 X126.814 Y123.945 E.02443
G1 X127.081 Y123.855 E.00908
G1 X127.69 Y123.648 E.02069
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
M73 P12 R11
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.118 Y124.556 E.02977
G1 X126.197 Y124.486 E.0034
M204 S250
G1 X126.501 Y124.741 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X127.014 Y124.291 E.02031
G1 X127.207 Y124.226 E.00609
G1 X127.742 Y124.044 E.01684
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.435 Y124.799 E.02293
G1 X126.456 Y124.781 E.00083
; WIPE_START
G1 F11933.819
M204 S10000
G1 X127.014 Y124.291 E-.28192
G1 X127.207 Y124.226 E-.07763
G1 X127.258 Y124.208 E-.02045
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.4 I-.578 J1.071 P1  F30000
G1 X132.253 Y126.905 Z1.4
G1 Z1
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03442
G3 X131.37 Y128.616 I-3.349 J-1.594 E.02771
G1 X130.655 Y129.458 E.03555
G1 X131.01 Y130.703 E.04161
G1 X131.013 Y130.807 E.00334
G1 X130.989 Y130.881 E.00252
G3 X130.568 Y130.958 I-.24 J-.121 E.01595
G1 X129.667 Y130.028 E.04162
G1 X128.534 Y130.232 E.03703
G3 X127.721 Y130.258 I-.536 J-4.117 E.02621
G1 X126.271 Y130.091 E.04692
G1 X125.412 Y130.975 E.03963
G1 X125.267 Y131.03 E.00498
G1 X125.164 Y131.016 E.00336
G1 X125.094 Y130.98 E.00251
G1 X125 Y130.857 E.00498
G1 X124.985 Y130.728 E.00418
G1 X125.334 Y129.497 E.04115
G1 X124.532 Y128.485 E.04152
G1 X124.315 Y128.154 E.01273
G1 X124.113 Y127.761 E.01421
G1 X123.639 Y126.56 E.04152
G1 X122.422 Y126.255 E.04032
G1 X122.331 Y126.206 E.00335
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00336
G1 X122.245 Y125.923 E.00334
G1 X122.294 Y125.831 E.00336
G1 X122.374 Y125.765 E.00334
G1 X123.593 Y125.451 E.04047
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.351 J1.595 E.0277
G1 X125.345 Y122.542 E.03555
G1 X124.985 Y121.272 E.04245
G1 X124.992 Y121.168 E.00334
G1 X125.038 Y121.074 E.00336
G1 X125.116 Y121.006 E.00334
G1 X125.215 Y120.972 E.00336
G3 X125.303 Y120.976 I.035 J.237 E.00283
G1 X125.433 Y121.042 E.00469
G1 X126.333 Y121.972 E.04162
G1 X127.466 Y121.768 E.03703
G3 X128.279 Y121.742 I.536 J4.118 E.02621
G1 X129.728 Y121.909 E.04691
G1 X130.588 Y121.025 E.03964
G1 X130.656 Y120.987 E.00251
G1 X130.758 Y120.97 E.00334
G1 X130.906 Y121.02 E.005
G1 X131 Y121.143 E.00498
G1 X131.015 Y121.272 E.00417
G1 X130.666 Y122.503 E.04116
G1 X131.468 Y123.515 E.04151
G1 X131.685 Y123.846 E.01274
G1 X131.887 Y124.239 E.0142
G1 X132.361 Y125.44 E.04153
G1 X133.578 Y125.745 E.04032
G1 X133.669 Y125.794 E.00335
G1 X133.735 Y125.874 E.00335
G1 X133.766 Y125.974 E.00335
G1 X133.756 Y126.077 E.00334
G1 X133.706 Y126.169 E.00336
G1 X133.626 Y126.236 E.00335
G1 X132.407 Y126.549 E.04045
G1 X132.276 Y126.85 E.01058
G1 X132.577 Y127.18 F30000
G1 F1983
G1 X132.192 Y128.068 E.0311
G3 X131.709 Y128.846 I-4.191 J-2.067 E.02951
G1 X131.106 Y129.556 E.02996
G1 X131.407 Y130.61 E.03526
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.526 Y130.468 E.03526
G1 X128.61 Y130.635 E.02995
G3 X127.694 Y130.665 I-.61 J-4.633 E.0295
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.255 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.796 J-2.721 E.02952
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.155 I4.192 J2.067 E.0295
G1 X124.894 Y122.444 E.02996
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.745 I.659 J-.149 E.05519
G1 X126.474 Y121.533 E.03526
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.336 I.61 J4.634 E.0295
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.744 E.03299
G3 X130.822 Y120.567 I.462 J.498 E.01864
G3 X131.407 Y121.39 I-.073 J.671 E.03667
G1 X131.115 Y122.414 E.03425
G1 X131.8 Y123.277 E.03543
G3 X132.258 Y124.071 I-3.797 J2.722 E.02952
G1 X132.663 Y125.096 E.03545
G1 X133.696 Y125.355 E.03424
G3 X133.758 Y126.623 I-.197 J.646 E.05319
G1 X132.701 Y126.895 E.0351
G1 X132.601 Y127.125 E.00808
G1 X132.902 Y127.455 F30000
G1 F1983
G1 X132.558 Y128.248 E.02779
G3 X131.557 Y129.653 I-5.528 J-2.878 E.05566
G1 X131.804 Y130.518 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08853
G1 X129.385 Y130.907 E.02891
G3 X127.668 Y131.071 I-1.446 J-6.058 E.05566
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.128 J-2.958 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.531 J2.88 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.057 J-.239 E.08854
G1 X126.615 Y121.093 E.02891
G3 X128.332 Y120.929 I1.445 J6.053 E.05566
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.874 Y120.163 I.742 J.8 E.03015
G3 X131.804 Y121.483 I-.126 J1.076 E.05858
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02935
G3 X132.629 Y123.903 I-4.128 J2.959 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.035 I-.321 J1.035 E.08854
G1 X132.995 Y127.241 E.02717
G1 X132.926 Y127.4 E.00558
G1 X133.226 Y127.73 F30000
G1 F1983
G1 X132.923 Y128.428 E.02448
G3 X132.008 Y129.751 I-5.48 J-2.814 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.851 I-1.456 J.329 E.12188
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.018 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02135
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.443 J-1.426 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.483 J2.816 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.456 J-.33 E.12189
G1 X126.756 Y120.654 E.02255
G3 X128.359 Y120.522 I1.3 J6.014 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.925 Y119.758 I1.022 J1.102 E.04166
G3 X132.201 Y121.575 I-.178 J1.481 E.0805
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.56 J4.081 E.08124
G1 X133.932 Y124.575 E.02207
G3 X133.933 Y127.425 I-.442 J1.426 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.25 Y127.675 E.00308
G1 X133.551 Y128.005 F30000
G1 F1983
G1 X133.289 Y128.608 E.02116
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.0162
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13136
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.332 J-3.78 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.742 J-1.021 E.03412
G3 X125.353 Y119.343 I1.913 J.147 E.09484
G3 X126.547 Y119.852 I-.114 J1.923 E.04257
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.069 E.07177
G3 X130.082 Y119.461 I1.957 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.333 J3.78 E.07165
G3 X134.554 Y124.423 I-.488 J2.874 E.03392
G3 X134.051 Y127.815 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01555
G1 X133.575 Y127.95 E.00058
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
M73 P13 R11
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.113 J-3.49 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19228
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.377 Y118.952 I2.166 J-.8 E.13548
G3 X127.033 Y119.791 I-.195 J2.439 E.05673
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.114 J3.49 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.227
G1 X133.446 Y129.134 E-.153
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.4 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z1.4
G1 Z1
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113559
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146828
G1 X132.205 Y126.351 E.00091
; LINE_WIDTH: 0.178156
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207498
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.4 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z1.4
G1 Z1
G1 E.4 F1800
; LINE_WIDTH: 0.207382
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178068
G1 X129.798 Y122.182 E.00395
; LINE_WIDTH: 0.146779
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.11354
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.4 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z1.4
G1 Z1
G1 E.4 F1800
; LINE_WIDTH: 0.113559
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146829
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.178142
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.20748
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.4 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z1.4
G1 Z1
G1 E.4 F1800
; LINE_WIDTH: 0.207457
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178119
G1 X126.202 Y129.817 E.00395
; LINE_WIDTH: 0.146817
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113552
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 1.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 6/50
; update layer progress
M73 L6
M991 S0 P5 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z1.4 I1.198 J-.211 P1  F30000
G1 X125.144 Y123.244 Z1.4
G1 Z1.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X125.984 Y122.507 E.03592
G1 X126.592 Y122.301 E.02065
G1 X127.474 Y122.002 E.02995
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.801 Y123.545 E.0506
G1 X125.099 Y123.284 E.01274
G1 X125.412 Y123.55 F30000
G1 F1983
G1 X126.191 Y122.867 E.03332
G1 X126.723 Y122.686 E.01805
G1 X127.528 Y122.413 E.02734
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X125.13 Y123.798 E.04539
G1 X125.367 Y123.59 E.01014
G1 X125.68 Y123.856 F30000
G1 F1983
G1 X126.399 Y123.226 E.03072
G1 X126.853 Y123.072 E.01545
G1 X127.582 Y122.825 E.02474
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.459 Y124.05 E.04019
G1 X125.635 Y123.896 E.00754
G1 X125.949 Y124.162 F30000
G1 F1983
G1 X126.606 Y123.586 E.02811
G1 X126.984 Y123.457 E.01284
G1 X127.636 Y123.236 E.02213
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.788 Y124.303 E.03498
G1 X125.904 Y124.202 E.00493
G1 X126.217 Y124.468 F30000
G1 F1983
G1 X126.814 Y123.945 E.02551
G1 X127.115 Y123.843 E.01024
G1 X127.69 Y123.648 E.01953
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.118 Y124.556 E.02977
G1 X126.172 Y124.508 E.00233
M204 S250
G1 X126.476 Y124.763 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X127.014 Y124.291 E.02131
G1 X127.241 Y124.214 E.00716
G1 X127.742 Y124.044 E.01577
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.432 Y124.804 E.02277
; WIPE_START
G1 F11933.819
M204 S10000
G1 X127.014 Y124.291 E-.29445
G1 X127.227 Y124.219 E-.08555
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.6 I-.574 J1.073 P1  F30000
G1 X132.253 Y126.905 Z1.6
G1 Z1.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03441
G3 X131.37 Y128.616 I-3.357 J-1.599 E.02771
G1 X130.655 Y129.459 E.03555
G1 X131.015 Y130.728 E.04243
G1 X130.989 Y130.881 E.00499
G1 X130.884 Y130.994 E.00498
G1 X130.733 Y131.03 E.00498
G1 X130.588 Y130.975 E.00499
G1 X129.668 Y130.028 E.04245
G1 X128.534 Y130.232 E.03704
G3 X127.721 Y130.258 I-.536 J-4.114 E.02619
G1 X126.272 Y130.091 E.04692
G1 X125.412 Y130.975 E.03964
G1 X125.344 Y131.013 E.00252
G1 X125.241 Y131.03 E.00334
G1 X125.094 Y130.98 E.00499
G1 X125 Y130.857 E.00498
G1 X124.985 Y130.728 E.00418
G1 X125.334 Y129.496 E.04117
G1 X124.532 Y128.486 E.0415
G1 X124.315 Y128.154 E.01273
G1 X124.113 Y127.761 E.01421
G1 X123.639 Y126.56 E.04152
G1 X122.423 Y126.256 E.04032
G1 X122.331 Y126.206 E.00335
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00335
G1 X122.244 Y125.923 E.00334
G1 X122.294 Y125.831 E.00335
G1 X122.374 Y125.765 E.00335
G1 X123.593 Y125.451 E.04047
G1 X124.173 Y124.113 E.04691
G3 X124.63 Y123.385 I3.367 J1.605 E.0277
G1 X125.345 Y122.542 E.03555
G1 X124.983 Y121.246 E.04327
G1 X125 Y121.143 E.00335
G1 X125.074 Y121.036 E.00418
G1 X125.164 Y120.984 E.00334
G1 X125.267 Y120.97 E.00334
G1 X125.344 Y120.987 E.00253
G1 X125.433 Y121.042 E.00335
G1 X126.332 Y121.971 E.04158
G1 X127.467 Y121.768 E.03708
G3 X128.279 Y121.742 I.535 J4.111 E.02617
G1 X129.728 Y121.909 E.04692
G1 X130.588 Y121.025 E.03964
G1 X130.733 Y120.97 E.00498
G1 X130.811 Y120.977 E.00252
G1 X130.905 Y121.02 E.00335
G1 X131 Y121.143 E.00498
G1 X131.015 Y121.272 E.00418
G1 X130.665 Y122.503 E.04114
G1 X131.468 Y123.515 E.04154
G1 X131.685 Y123.846 E.01273
G1 X131.887 Y124.239 E.01421
G1 X132.361 Y125.44 E.04152
G1 X133.578 Y125.745 E.04032
G1 X133.669 Y125.794 E.00334
G1 X133.735 Y125.874 E.00335
G1 X133.766 Y125.974 E.00335
G1 X133.755 Y126.077 E.00334
G1 X133.706 Y126.169 E.00335
G1 X133.626 Y126.235 E.00334
G1 X132.407 Y126.549 E.04047
G1 X132.276 Y126.85 E.01056
G1 X132.577 Y127.18 F30000
G1 F1983
G1 X132.192 Y128.068 E.0311
G3 X131.709 Y128.846 I-4.193 J-2.068 E.02951
G1 X131.106 Y129.556 E.02996
G1 X131.407 Y130.61 E.03524
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.526 Y130.468 E.03526
G1 X128.61 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.635 E.02951
G1 X126.424 Y130.518 E.0411
G1 X125.711 Y131.256 E.03299
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03542
G3 X123.742 Y127.929 I3.799 J-2.723 E.02952
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.646 E.03424
G3 X122.304 Y125.354 I.2 J-.645 E.0552
G1 X123.299 Y125.105 E.03298
M73 P14 R11
G1 X123.808 Y123.932 E.0411
G3 X124.291 Y123.154 I4.194 J2.069 E.02951
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.745 I.659 J-.149 E.0552
G1 X126.473 Y121.532 E.03523
G1 X127.39 Y121.366 E.02995
G3 X128.306 Y121.335 I.611 J4.636 E.02952
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.745 E.03298
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03616
G1 X131.114 Y122.413 E.03424
G1 X131.8 Y123.277 E.03546
G3 X132.258 Y124.071 I-3.796 J2.721 E.02952
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.05519
G1 X132.701 Y126.895 E.03299
G1 X132.601 Y127.125 E.00806
G1 X133.22 Y127.184 F30000
G1 F1983
G1 X132.994 Y127.241 E.0075
G1 X132.558 Y128.248 E.03528
G3 X131.557 Y129.654 I-5.535 J-2.882 E.05567
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X127.668 Y131.071 I-1.446 J-6.063 E.05566
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.436 Y129.675 E.02816
G1 X123.869 Y128.96 E.02934
G3 X123.371 Y128.097 I4.129 J-2.959 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.321 J-1.036 E.08855
G1 X123.006 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G3 X124.443 Y122.347 I5.532 J2.881 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.057 J-.239 E.08854
G1 X126.614 Y121.092 E.02888
G3 X128.332 Y120.929 I1.447 J6.087 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.482 I-.144 J1.075 E.05802
G1 X131.563 Y122.324 E.02816
G1 X132.131 Y123.04 E.02938
G3 X132.629 Y123.903 I-4.128 J2.959 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.322 J1.035 E.08854
G1 X133.279 Y127.17 E.01775
G1 X133.439 Y127.549 F30000
G1 F1983
G1 X133.288 Y127.587 E.005
G1 X132.923 Y128.428 E.02947
G3 X132.008 Y129.751 I-5.486 J-2.818 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.022 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.1219
G1 X123.988 Y129.764 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08122
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.484 J2.817 E.05187
G1 X123.799 Y121.575 E.02254
G3 X125.347 Y119.75 I1.454 J-.335 E.08928
G3 X126.268 Y120.15 I-.11 J1.515 E.03289
G1 X126.756 Y120.653 E.02253
G3 X128.359 Y120.522 I1.301 J6.045 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12188
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.081 E.08125
G1 X133.933 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.425 E.12189
G1 X133.497 Y127.535 E.01443
G1 X133.657 Y127.914 F30000
G1 F1983
G1 X133.582 Y127.933 E.0025
G3 X132.459 Y129.848 I-5.807 J-2.117 E.07177
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.742 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13136
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07164
G3 X121.446 Y127.577 I.489 J-2.875 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.805 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X125.374 Y119.344 I1.914 J.148 E.09553
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.556 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07166
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.715 Y127.9 E.01112
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19276
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.922 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19228
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.381 Y118.952 I2.151 J-.811 E.13593
G3 X127.033 Y119.791 I-.15 J2.342 E.05674
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.921 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19271
G3 X133.859 Y123.732 I-4.112 J3.489 E.05783
G3 X133.924 Y128.256 I-.37 J2.268 E.19089
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22693
G1 X133.445 Y129.134 E-.15307
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.6 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z1.6
G1 Z1.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113521
G1 F1983
G1 X132.179 Y126.46 E.00062
; LINE_WIDTH: 0.146714
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.17795
G1 X132.379 Y126.025 E.00395
; LINE_WIDTH: 0.207235
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.6 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z1.6
G1 Z1.2
G1 E.4 F1800
; LINE_WIDTH: 0.207388
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.17807
G1 X129.798 Y122.183 E.00395
; LINE_WIDTH: 0.146778
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113539
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.6 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z1.6
G1 Z1.2
G1 E.4 F1800
; LINE_WIDTH: 0.113516
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.1467
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.177935
G1 X123.621 Y125.975 E.00395
; LINE_WIDTH: 0.207214
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.6 I-1.096 J.529 P1  F30000
G1 X125.461 Y129.792 Z1.6
G1 Z1.2
G1 E.4 F1800
; LINE_WIDTH: 0.207358
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178033
G1 X126.202 Y129.818 E.00396
; LINE_WIDTH: 0.146765
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113534
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 1.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 7/50
; update layer progress
M73 L7
M991 S0 P6 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z1.6 I1.198 J-.217 P1  F30000
G1 X125.118 Y123.267 Z1.6
G1 Z1.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1987
G1 X125.984 Y122.507 E.03704
G1 X126.626 Y122.289 E.02182
G1 X127.474 Y122.002 E.02878
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
M73 P15 R11
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.801 Y123.545 E.0506
G1 X125.073 Y123.306 E.01163
G1 X125.386 Y123.573 F30000
G1 F1987
G1 X126.191 Y122.867 E.03443
G1 X126.757 Y122.675 E.01921
G1 X127.528 Y122.413 E.02618
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X125.13 Y123.798 E.04539
G1 X125.341 Y123.613 E.00903
G1 X125.654 Y123.879 F30000
G1 F1987
G1 X126.399 Y123.226 E.03183
G1 X126.888 Y123.06 E.01661
G1 X127.582 Y122.825 E.02357
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.459 Y124.05 E.04019
G1 X125.609 Y123.919 E.00642
G1 X125.923 Y124.185 F30000
G1 F1987
G1 X126.606 Y123.586 E.02923
G1 X127.019 Y123.446 E.014
G1 X127.636 Y123.236 E.02097
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.788 Y124.303 E.03498
G1 X125.878 Y124.225 E.00382
G1 X126.191 Y124.491 F30000
G1 F1987
G1 X126.814 Y123.945 E.02662
G1 X127.149 Y123.831 E.0114
G1 X127.69 Y123.648 E.01837
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.118 Y124.556 E.02977
G1 X126.146 Y124.531 E.00122
M204 S250
G1 X126.45 Y124.786 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1987
M204 S5000
G1 X127.014 Y124.291 E.02234
G1 X127.275 Y124.203 E.00824
G1 X127.742 Y124.044 E.01469
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.417 Y124.835 E.02174
; WIPE_START
G1 F11933.819
M204 S10000
G1 X127.014 Y124.291 E-.30665
G1 X127.196 Y124.229 E-.07336
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.8 I-.569 J1.076 P1  F30000
G1 X132.253 Y126.905 Z1.8
G1 Z1.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1987
G1 X131.827 Y127.887 E.03444
G3 X131.37 Y128.616 I-3.365 J-1.604 E.0277
G1 X130.655 Y129.458 E.03554
G1 X131.015 Y130.728 E.04245
G1 X130.989 Y130.881 E.00499
G1 X130.884 Y130.994 E.00498
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G1 X129.668 Y130.028 E.04244
G1 X128.534 Y130.232 E.03704
G3 X127.721 Y130.258 I-.536 J-4.116 E.0262
G1 X126.271 Y130.091 E.04692
G1 X125.413 Y130.975 E.03962
G1 X125.267 Y131.03 E.00499
G1 X125.164 Y131.016 E.00335
G1 X125.094 Y130.98 E.00252
G1 X125 Y130.857 E.00499
G1 X124.985 Y130.728 E.00417
G1 X125.334 Y129.497 E.04116
G1 X124.532 Y128.485 E.04152
G1 X124.315 Y128.154 E.01272
G1 X124.113 Y127.761 E.01421
G1 X123.639 Y126.56 E.04152
G1 X122.423 Y126.256 E.04032
G1 X122.331 Y126.206 E.00335
G1 X122.265 Y126.126 E.00334
G1 X122.234 Y126.026 E.00336
G1 X122.244 Y125.923 E.00334
G1 X122.294 Y125.831 E.00335
G1 X122.374 Y125.765 E.00335
G1 X123.593 Y125.451 E.04047
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.384 I3.343 J1.59 E.02771
G1 X125.345 Y122.542 E.03554
G1 X124.983 Y121.246 E.04328
G1 X125 Y121.143 E.00336
G1 X125.055 Y121.054 E.00335
G1 X125.164 Y120.984 E.00416
G1 X125.267 Y120.97 E.00335
G1 X125.344 Y120.987 E.00252
G1 X125.432 Y121.042 E.00334
G1 X126.332 Y121.971 E.0416
G1 X127.466 Y121.768 E.03706
G3 X128.279 Y121.742 I.536 J4.112 E.02619
G1 X129.729 Y121.909 E.04691
G1 X130.587 Y121.025 E.03963
G1 X130.733 Y120.97 E.00499
G1 X130.836 Y120.984 E.00335
G1 X130.905 Y121.02 E.00251
G1 X130.989 Y121.119 E.00417
G1 X131.015 Y121.272 E.00499
G1 X130.666 Y122.503 E.04115
G1 X131.468 Y123.515 E.04152
G1 X131.708 Y123.886 E.0142
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04152
G1 X133.577 Y125.745 E.04032
G1 X133.669 Y125.794 E.00335
G1 X133.735 Y125.874 E.00335
G1 X133.766 Y125.974 E.00335
G1 X133.755 Y126.077 E.00335
G1 X133.706 Y126.17 E.00336
G1 X133.626 Y126.235 E.00334
G1 X132.407 Y126.549 E.04046
G1 X132.277 Y126.85 E.01055
G1 X133.002 Y126.819 F30000
G1 F1987
G1 X132.701 Y126.895 E.00998
G1 X132.192 Y128.068 E.04111
G3 X131.709 Y128.846 I-4.195 J-2.069 E.02951
G1 X131.106 Y129.556 E.02994
G1 X131.407 Y130.61 E.03526
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.526 Y130.468 E.03525
G1 X128.61 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.635 E.02951
G1 X126.424 Y130.518 E.0411
G1 X125.711 Y131.256 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.8 J-2.723 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.354 I.2 J-.645 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.154 I4.192 J2.068 E.0295
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03526
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.687 E.01489
G1 X126.473 Y121.532 E.03524
G1 X127.39 Y121.366 E.02995
G3 X128.306 Y121.336 I.61 J4.635 E.02952
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.744 E.03299
G3 X131.407 Y121.39 I.459 J.496 E.0552
G1 X131.115 Y122.414 E.03423
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.795 J2.72 E.02951
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.06 Y126.805 E.02106
G1 X133.22 Y127.184 F30000
G1 F1987
G1 X132.995 Y127.241 E.00748
G1 X132.558 Y128.248 E.0353
G3 X131.557 Y129.653 I-5.526 J-2.877 E.05566
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X127.668 Y131.071 I-1.446 J-6.064 E.05567
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.131 J-2.96 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G3 X124.443 Y122.347 I5.525 J2.876 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.321 Y120.157 I1.056 J-.244 E.06486
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.02889
G3 X128.332 Y120.929 I1.446 J6.079 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X131.804 Y121.483 I.736 J.796 E.08854
G1 X131.563 Y122.325 E.02815
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.128 J2.958 E.03209
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08855
G1 X133.278 Y127.17 E.01775
G1 X133.438 Y127.549 F30000
G1 F1987
G1 X133.288 Y127.587 E.00498
G1 X132.923 Y128.428 E.02948
G3 X132.008 Y129.751 I-5.478 J-2.813 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.022 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.851 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12188
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.442 J-1.426 E.12189
G1 X122.712 Y124.413 E.02136
M73 P16 R11
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.478 J2.813 E.05187
G1 X123.799 Y121.575 E.02255
G3 X125.347 Y119.75 I1.454 J-.335 E.08928
G3 X126.268 Y120.15 I-.11 J1.516 E.03289
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.036 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08123
G1 X133.932 Y124.574 E.02208
G3 X133.932 Y127.426 I-.442 J1.426 E.1219
G1 X133.497 Y127.535 E.01444
G1 X133.551 Y128.004 F30000
G1 F1987
G1 X133.289 Y128.608 E.02118
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.744 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.072 E.07177
G3 X125.918 Y132.539 I-1.955 J-1.556 E.03947
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.489 J-2.876 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.744 J-1.021 E.03412
G3 X125.374 Y119.344 I1.914 J.148 E.09553
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.074 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13136
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07164
G3 X134.554 Y124.423 I-.489 J2.875 E.03393
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01554
G1 X133.575 Y127.949 E.00056
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1987
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19277
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X120.865 Y127.601 I.415 J-2.35 E.04358
G3 X122.135 Y123.734 I1.646 J-1.602 E.14903
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.375 Y118.952 I2.165 J-.8 E.13545
M73 P16 R10
G3 X127.033 Y119.791 I-.144 J2.34 E.0569
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X133.924 Y128.256 I-.369 J2.268 E.19093
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22696
G1 X133.445 Y129.134 E-.15304
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.8 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z1.8
G1 Z1.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113554
G1 F1987
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146815
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178103
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207428
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.8 I.99 J-.708 P1  F30000
G1 X129.586 Y122.12 Z1.8
G1 Z1.4
G1 E.4 F1800
; LINE_WIDTH: 0.113552
G1 F1987
G1 X129.692 Y122.151 E.00062
; LINE_WIDTH: 0.146813
G1 X129.798 Y122.182 E.00091
; LINE_WIDTH: 0.178116
G1 X130.168 Y122.195 E.00396
; LINE_WIDTH: 0.207447
G1 X130.538 Y122.208 E.00481
G1 X130.691 Y121.674 F30000
; LINE_WIDTH: 0.162834
G1 F1987
G1 X130.75 Y121.233 E.00421
G1 X130.743 Y121.175 E.00055
; WIPE_START
G1 F15000
G1 X130.75 Y121.233 E-.04417
G1 X130.691 Y121.674 E-.33583
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.8 I-.586 J-1.067 P1  F30000
G1 X123.847 Y125.433 Z1.8
G1 Z1.4
G1 E.4 F1800
; LINE_WIDTH: 0.113554
G1 F1987
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146815
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.178103
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.207428
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z1.8 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z1.8
G1 Z1.4
G1 E.4 F1800
; LINE_WIDTH: 0.207488
G1 F1987
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178143
G1 X126.202 Y129.818 E.00396
; LINE_WIDTH: 0.146835
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113559
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 1.6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 8/50
; update layer progress
M73 L8
M991 S0 P7 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z1.8 I1.171 J-.332 P1  F30000
G1 X124.623 Y123.905 Z1.8
G1 Z1.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.01291
G1 X125.984 Y122.507 E.0506
G1 X126.66 Y122.278 E.02298
G1 X127.474 Y122.002 E.02762
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.596 Y123.959 E.03576
G1 X124.988 Y124.085 F30000
G1 F1983
G1 X125.13 Y123.798 E.01031
G1 X126.191 Y122.867 E.04539
G1 X126.791 Y122.663 E.02037
G1 X127.528 Y122.413 E.02502
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.962 Y124.139 E.03316
G1 X125.353 Y124.265 F30000
G1 F1983
G1 X125.459 Y124.05 E.0077
G1 X126.399 Y123.226 E.04018
G1 X126.922 Y123.049 E.01777
G1 X127.582 Y122.825 E.02241
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.327 Y124.319 E.03055
G1 X125.718 Y124.445 F30000
G1 F1983
G1 X125.788 Y124.303 E.0051
G1 X126.606 Y123.586 E.03498
G1 X127.053 Y123.434 E.01517
G1 X127.636 Y123.236 E.01981
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.692 Y124.499 E.02795
G1 X126.083 Y124.625 F30000
G1 F1983
G1 X126.118 Y124.556 E.0025
G1 X126.814 Y123.945 E.02977
G1 X127.184 Y123.82 E.01256
G1 X127.69 Y123.648 E.01721
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
M73 P17 R10
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.057 Y124.679 E.02534
M204 S250
G1 X126.435 Y124.799 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X127.014 Y124.291 E.02293
G1 X127.31 Y124.191 E.00931
G1 X127.742 Y124.044 E.01362
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.408 Y124.853 E.02114
; WIPE_START
G1 F11933.819
M204 S10000
G1 X127.014 Y124.291 E-.31371
G1 X127.179 Y124.235 E-.06629
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2 I-.567 J1.077 P1  F30000
G1 X132.253 Y126.904 Z2
G1 Z1.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03445
G3 X131.37 Y128.616 I-3.346 J-1.592 E.0277
G1 X130.655 Y129.458 E.03554
G1 X131.015 Y130.728 E.04245
G1 X130.989 Y130.881 E.00499
G1 X130.883 Y130.994 E.00498
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G1 X129.668 Y130.028 E.04245
G1 X128.534 Y130.232 E.03704
G3 X127.721 Y130.258 I-.536 J-4.116 E.0262
G1 X126.271 Y130.091 E.04692
G1 X125.412 Y130.975 E.03963
G1 X125.267 Y131.03 E.00499
G1 X125.189 Y131.023 E.00252
G1 X125.095 Y130.98 E.00335
G1 X125 Y130.857 E.00498
G1 X124.985 Y130.728 E.00418
G1 X125.334 Y129.497 E.04116
G1 X124.532 Y128.485 E.04151
G1 X124.315 Y128.154 E.01273
G1 X124.113 Y127.761 E.01421
G1 X123.639 Y126.56 E.04152
G1 X122.422 Y126.255 E.04032
G1 X122.331 Y126.206 E.00335
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00336
G1 X122.244 Y125.923 E.00334
G1 X122.294 Y125.831 E.00335
G1 X122.374 Y125.765 E.00335
G1 X123.593 Y125.451 E.04046
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.384 I3.344 J1.591 E.0277
G1 X125.345 Y122.542 E.03554
G1 X124.983 Y121.246 E.04328
G1 X125.011 Y121.119 E.00417
G1 X125.074 Y121.036 E.00335
G1 X125.164 Y120.984 E.00336
G1 X125.267 Y120.97 E.00334
G1 X125.344 Y120.987 E.00253
G1 X125.433 Y121.042 E.00335
G1 X126.333 Y121.972 E.04162
G1 X127.466 Y121.768 E.03703
G3 X128.279 Y121.742 I.536 J4.117 E.02621
G1 X129.729 Y121.909 E.04691
G1 X130.588 Y121.025 E.03964
G1 X130.656 Y120.987 E.00251
G1 X130.759 Y120.97 E.00335
G1 X130.905 Y121.02 E.00499
G1 X131 Y121.143 E.00498
G1 X131.015 Y121.272 E.00418
G1 X130.666 Y122.503 E.04115
G1 X131.468 Y123.515 E.04152
G1 X131.708 Y123.886 E.0142
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04151
G1 X133.577 Y125.745 E.04032
G1 X133.669 Y125.794 E.00336
G1 X133.736 Y125.874 E.00335
G1 X133.766 Y125.974 E.00335
G1 X133.755 Y126.077 E.00334
G1 X133.706 Y126.169 E.00335
G1 X133.626 Y126.235 E.00334
G1 X132.407 Y126.549 E.04047
G1 X132.277 Y126.849 E.01054
G1 X133.002 Y126.819 F30000
G1 F1983
G1 X132.701 Y126.895 E.00997
G1 X132.192 Y128.068 E.04111
G3 X131.709 Y128.846 I-4.194 J-2.068 E.0295
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03526
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.526 Y130.468 E.03526
G1 X128.61 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.634 E.02951
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.255 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03543
G3 X123.742 Y127.929 I3.793 J-2.719 E.02952
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.154 I4.194 J2.068 E.0295
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03525
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.01489
G1 X126.474 Y121.533 E.03527
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.335 I.61 J4.635 E.0295
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.745 E.03297
G3 X131.407 Y121.39 I.459 J.496 E.0552
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.799 J2.722 E.02952
G1 X132.663 Y125.096 E.03543
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.06 Y126.805 E.02108
G1 X133.22 Y127.184 F30000
G1 F1983
G1 X132.995 Y127.241 E.00747
G1 X132.558 Y128.248 E.0353
G3 X131.557 Y129.653 I-5.526 J-2.877 E.05566
G1 X131.804 Y130.518 E.02891
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X127.668 Y131.071 I-1.446 J-6.059 E.05566
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02935
G3 X123.371 Y128.097 I4.126 J-2.957 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.528 J2.878 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.321 Y120.157 I1.056 J-.244 E.06486
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.02891
G3 X128.332 Y120.929 I1.445 J6.049 E.05566
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02716
G3 X131.804 Y121.483 I.736 J.796 E.08855
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.131 J2.96 E.03209
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08855
G1 X133.278 Y127.17 E.01777
G1 X133.438 Y127.549 F30000
G1 F1983
G1 X133.288 Y127.587 E.00497
G1 X132.923 Y128.428 E.02948
G3 X132.008 Y129.751 I-5.479 J-2.813 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.019 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.443 J-1.426 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.479 J2.814 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.15 I1.456 J-.329 E.12189
G1 X126.756 Y120.654 E.02255
G3 X128.359 Y120.522 I1.3 J6.01 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02135
G3 X130.944 Y119.76 I1.024 J1.105 E.0423
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.425 E.12189
G1 X133.496 Y127.535 E.01445
G1 X133.551 Y128.004 F30000
G1 F1983
G1 X133.289 Y128.608 E.0212
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07164
G3 X121.446 Y127.577 I.489 J-2.875 E.03393
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.364 Y119.344 I1.913 J.148 E.09519
G3 X126.547 Y119.852 I-.178 J2.045 E.04212
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.15 J6.068 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.261 Y120.091 I.665 J1.785 E.07814
G3 X132.598 Y121.668 I-1.532 J1.151 E.05352
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07164
G3 X134.554 Y124.423 I-.489 J2.875 E.03393
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01554
G1 X133.575 Y127.948 E.00054
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
M73 P18 R10
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.37 Y118.952 I2.165 J-.8 E.13529
G3 X127.033 Y119.791 I-.137 J2.339 E.05706
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.46 E.19264
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X133.924 Y128.256 I-.369 J2.268 E.19094
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22696
G1 X133.445 Y129.134 E-.15304
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z2
G1 Z1.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113554
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146815
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178104
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207429
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z2
G1 Z1.6
G1 E.4 F1800
; LINE_WIDTH: 0.20744
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.1781
G1 X129.798 Y122.183 E.00396
; LINE_WIDTH: 0.146812
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113551
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z2
G1 Z1.6
G1 E.4 F1800
; LINE_WIDTH: 0.113559
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146828
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.178121
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.20746
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z2
G1 Z1.6
G1 E.4 F1800
; LINE_WIDTH: 0.207499
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178147
G1 X126.202 Y129.817 E.00396
; LINE_WIDTH: 0.146841
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113561
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 1.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 9/50
; update layer progress
M73 L9
M991 S0 P8 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z2 I1.171 J-.333 P1  F30000
G1 X124.62 Y123.912 Z2
G1 Z1.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.01316
G1 X125.984 Y122.507 E.0506
G1 X126.694 Y122.266 E.02414
G1 X127.474 Y122.002 E.02646
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.593 Y123.966 E.03552
G1 X124.985 Y124.092 F30000
G1 F1983
G1 X125.13 Y123.798 E.01055
G1 X126.191 Y122.867 E.04539
G1 X126.825 Y122.652 E.02153
G1 X127.528 Y122.413 E.02386
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.958 Y124.146 E.03291
G1 X125.35 Y124.272 F30000
G1 F1983
G1 X125.459 Y124.05 E.00795
G1 X126.399 Y123.226 E.04018
G1 X126.956 Y123.037 E.01893
G1 X127.582 Y122.825 E.02125
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.323 Y124.326 E.03031
G1 X125.715 Y124.452 F30000
G1 F1983
G1 X125.788 Y124.303 E.00534
G1 X126.606 Y123.586 E.03498
G1 X127.087 Y123.423 E.01633
G1 X127.636 Y123.236 E.01865
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.721 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.688 Y124.506 E.0277
G1 X126.08 Y124.632 F30000
G1 F1983
G1 X126.118 Y124.556 E.00274
G1 X126.814 Y123.945 E.02977
G1 X127.218 Y123.808 E.01372
G1 X127.69 Y123.648 E.01605
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.053 Y124.686 E.0251
M204 S250
G1 X126.432 Y124.805 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X126.435 Y124.799 E.00021
G1 X127.014 Y124.291 E.02293
G1 X127.344 Y124.179 E.01039
G1 X127.742 Y124.044 E.01254
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.405 Y124.859 E.02093
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.02554
G1 X127.014 Y124.291 E-.29252
G1 X127.168 Y124.239 E-.06194
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.2 I-.565 J1.078 P1  F30000
G1 X132.253 Y126.904 Z2.2
G1 Z1.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03447
G3 X131.37 Y128.615 I-3.384 J-1.616 E.0277
G1 X130.655 Y129.459 E.03555
G1 X131.015 Y130.728 E.04244
G1 X130.989 Y130.881 E.00499
G1 X130.883 Y130.994 E.00498
G1 X130.733 Y131.03 E.00498
G1 X130.588 Y130.975 E.00499
G1 X129.668 Y130.028 E.04245
G1 X128.534 Y130.232 E.03704
G3 X127.721 Y130.258 I-.536 J-4.115 E.0262
G1 X126.271 Y130.091 E.04692
G1 X125.413 Y130.975 E.03962
G1 X125.267 Y131.03 E.00499
G1 X125.164 Y131.016 E.00335
G1 X125.094 Y130.98 E.00252
G1 X125.011 Y130.881 E.00417
G1 X124.985 Y130.728 E.00499
G1 X125.334 Y129.497 E.04116
G1 X124.532 Y128.485 E.04152
G1 X124.292 Y128.114 E.01421
G1 X124.113 Y127.761 E.01272
G1 X123.639 Y126.56 E.04152
G1 X122.423 Y126.256 E.04032
G1 X122.331 Y126.206 E.00335
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00336
G1 X122.244 Y125.923 E.00333
G1 X122.294 Y125.83 E.00336
G1 X122.374 Y125.765 E.00334
G1 X123.593 Y125.451 E.04046
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.356 J1.598 E.0277
G1 X125.345 Y122.542 E.03555
G1 X124.985 Y121.272 E.04245
G1 X125.011 Y121.119 E.00499
G1 X125.116 Y121.006 E.00497
G1 X125.267 Y120.97 E.00499
G1 X125.413 Y121.025 E.00499
G1 X126.332 Y121.972 E.04244
G1 X127.466 Y121.768 E.03705
G3 X128.279 Y121.742 I.536 J4.116 E.0262
G1 X129.728 Y121.909 E.04691
G1 X130.568 Y121.042 E.0388
G1 X130.681 Y120.979 E.00416
G1 X130.785 Y120.972 E.00335
G1 X130.884 Y121.006 E.00336
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.017 Y121.246 E.00252
G1 X130.666 Y122.503 E.04199
G1 X131.468 Y123.515 E.04152
G1 X131.708 Y123.886 E.01421
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04152
G1 X133.602 Y125.753 E.04117
G1 X133.707 Y125.831 E.00418
G1 X133.762 Y125.948 E.00416
G1 X133.766 Y126.026 E.00252
G1 X133.735 Y126.126 E.00336
G1 X133.689 Y126.189 E.00251
G1 X133.602 Y126.247 E.00336
G1 X132.407 Y126.549 E.03963
G1 X132.277 Y126.849 E.01053
G1 X133.001 Y126.819 F30000
G1 F1983
G1 X132.701 Y126.895 E.00996
G1 X132.192 Y128.068 E.04111
G3 X131.709 Y128.846 I-4.193 J-2.068 E.02951
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03525
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.526 Y130.468 E.03526
G1 X128.61 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.635 E.02951
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.256 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.885 Y129.586 E.03423
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.799 J-2.723 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.646 E.03424
G3 X122.304 Y125.355 I.2 J-.646 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
M73 P19 R10
G3 X124.291 Y123.154 I4.194 J2.069 E.0295
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.744 I.659 J-.149 E.05519
G1 X126.473 Y121.532 E.03526
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.336 I.61 J4.634 E.02951
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.745 E.03299
G3 X130.838 Y120.568 I.464 J.501 E.01914
G3 X131.407 Y121.39 I-.09 J.67 E.03618
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.798 J2.722 E.02952
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.059 Y126.805 E.0211
G1 X133.219 Y127.184 F30000
G1 F1983
G1 X132.995 Y127.241 E.00746
G1 X132.558 Y128.248 E.0353
G3 X131.557 Y129.653 I-5.534 J-2.881 E.05566
G1 X131.804 Y130.518 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X127.668 Y131.071 I-1.446 J-6.063 E.05566
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.129 J-2.959 E.03208
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.528 J2.878 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.057 J-.239 E.08854
G1 X126.615 Y121.093 E.0289
G3 X128.332 Y120.929 I1.446 J6.063 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.144 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.131 J2.96 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08854
G1 X133.278 Y127.17 E.01778
G1 X133.438 Y127.549 F30000
G1 F1983
G1 X133.288 Y127.587 E.00496
G1 X132.923 Y128.428 E.02949
G3 X132.008 Y129.751 I-5.485 J-2.817 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12188
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.021 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.442 J-1.426 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.48 J2.814 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.456 J-.33 E.12189
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.022 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.944 Y119.76 I1.024 J1.105 E.04229
G3 X132.201 Y121.575 I-.199 J1.48 E.07989
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.56 J4.081 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.426 E.1219
G1 X133.496 Y127.535 E.01447
G1 X133.551 Y128.003 F30000
G1 F1983
G1 X133.289 Y128.608 E.02121
G3 X132.459 Y129.848 I-5.514 J-2.792 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.742 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07178
G3 X125.918 Y132.539 I-1.955 J-1.555 E.03946
G3 X123.402 Y130.332 I-.657 J-1.788 E.13137
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.332 J-3.78 E.07165
G3 X121.446 Y127.577 I.489 J-2.876 E.03393
G3 X121.949 Y124.185 I1.07 J-1.575 E.13732
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.805 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.358 Y119.343 I1.913 J.147 E.09502
G3 X126.547 Y119.852 I-.171 J2.042 E.04229
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.071 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03947
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.78 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03393
G3 X134.051 Y127.816 I-1.055 J1.577 E.13774
G1 X133.582 Y127.933 E.01554
G1 X133.575 Y127.948 E.00053
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.774 J-1.46 E.19263
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.579 J2.112 E.05794
G3 X125.365 Y118.951 I2.165 J-.8 E.13513
G3 X127.033 Y119.791 I-.131 J2.338 E.05721
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.114 J3.49 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22704
G1 X133.446 Y129.134 E-.15296
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.2 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z2.2
G1 Z1.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113559
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146829
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178142
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.20748
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.2 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z2.2
G1 Z1.8
G1 E.4 F1800
; LINE_WIDTH: 0.207382
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178068
G1 X129.798 Y122.182 E.00395
; LINE_WIDTH: 0.146779
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.11354
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.2 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z2.2
G1 Z1.8
G1 E.4 F1800
; LINE_WIDTH: 0.113554
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146815
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.1781
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.207428
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.2 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z2.2
G1 Z1.8
G1 E.4 F1800
; LINE_WIDTH: 0.207542
G1 F1983
G1 X125.832 Y129.805 E.00482
; LINE_WIDTH: 0.178187
G1 X126.202 Y129.817 E.00396
; LINE_WIDTH: 0.14686
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113567
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 10/50
; update layer progress
M73 L10
M991 S0 P9 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z2.2 I1.17 J-.334 P1  F30000
G1 X124.616 Y123.919 Z2.2
G1 Z2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.0134
G1 X125.984 Y122.507 E.0506
G1 X127.474 Y122.002 E.0506
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
M73 P20 R10
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.59 Y123.973 E.03527
G1 X124.981 Y124.099 F30000
G1 F1983
G1 X125.13 Y123.798 E.0108
G1 X126.191 Y122.867 E.04539
G1 X127.528 Y122.413 E.04539
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.955 Y124.153 E.03266
G1 X125.346 Y124.279 F30000
G1 F1983
G1 X125.459 Y124.05 E.00819
G1 X126.399 Y123.226 E.04018
G1 X127.582 Y122.825 E.04018
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.32 Y124.333 E.03006
G1 X125.711 Y124.459 F30000
G1 F1983
G1 X125.788 Y124.303 E.00559
G1 X126.606 Y123.586 E.03498
G1 X127.636 Y123.236 E.03498
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.685 Y124.513 E.02746
G1 X126.077 Y124.639 F30000
G1 F1983
G1 X126.118 Y124.556 E.00299
G1 X126.814 Y123.945 E.02977
G1 X127.69 Y123.648 E.02977
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.05 Y124.693 E.02485
M204 S250
G1 X126.428 Y124.812 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X126.435 Y124.799 E.00044
G1 X127.014 Y124.291 E.02293
G1 X127.742 Y124.044 E.02293
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.402 Y124.866 E.0207
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.02847
G1 X127.014 Y124.291 E-.29252
G1 X127.161 Y124.242 E-.05901
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.4 I-.564 J1.079 P1  F30000
G1 X132.253 Y126.904 Z2.4
G1 Z2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03447
G3 X131.37 Y128.616 I-3.329 J-1.581 E.02771
G1 X130.655 Y129.458 E.03554
G1 X131.015 Y130.728 E.04245
G1 X130.989 Y130.881 E.00499
G1 X130.884 Y130.994 E.00498
G1 X130.733 Y131.03 E.00499
G1 X130.587 Y130.975 E.00499
G1 X129.667 Y130.028 E.04245
G1 X128.534 Y130.232 E.03703
G3 X127.721 Y130.258 I-.536 J-4.118 E.02621
G1 X126.271 Y130.091 E.04692
G1 X125.391 Y130.99 E.04046
G1 X125.293 Y131.027 E.00335
G1 X125.189 Y131.023 E.00335
G1 X125.094 Y130.98 E.00335
G1 X125.023 Y130.904 E.00335
G1 X124.987 Y130.807 E.00335
G1 X124.99 Y130.702 E.00335
G1 X125.334 Y129.497 E.04032
G1 X124.531 Y128.485 E.04152
G1 X124.292 Y128.114 E.0142
G1 X124.113 Y127.761 E.01273
G1 X123.639 Y126.56 E.04152
G1 X122.398 Y126.247 E.04116
G1 X122.278 Y126.148 E.00499
G1 X122.234 Y126.026 E.00417
G1 X122.244 Y125.923 E.00334
G1 X122.278 Y125.852 E.00253
G1 X122.398 Y125.753 E.00498
G1 X123.593 Y125.452 E.03963
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.384 I3.369 J1.606 E.02771
G1 X125.345 Y122.542 E.03554
G1 X124.985 Y121.272 E.04245
G1 X125.011 Y121.119 E.00499
G1 X125.117 Y121.006 E.00498
G1 X125.267 Y120.97 E.00498
G1 X125.413 Y121.025 E.00499
G1 X126.332 Y121.972 E.04245
G1 X127.466 Y121.768 E.03704
G3 X128.279 Y121.742 I.536 J4.121 E.02621
G1 X129.729 Y121.909 E.04691
G1 X130.568 Y121.042 E.0388
G1 X130.681 Y120.979 E.00417
G1 X130.785 Y120.972 E.00335
G1 X130.883 Y121.006 E.00335
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00334
G1 X131.017 Y121.246 E.00253
G1 X130.666 Y122.503 E.04199
G1 X131.468 Y123.514 E.04151
G1 X131.685 Y123.846 E.01273
G1 X131.887 Y124.239 E.01421
G1 X132.361 Y125.44 E.04152
G1 X133.602 Y125.753 E.04116
G1 X133.706 Y125.831 E.00418
G1 X133.762 Y125.948 E.00417
G1 X133.762 Y126.052 E.00335
G1 X133.735 Y126.126 E.00252
G1 X133.669 Y126.206 E.00335
G1 X133.602 Y126.247 E.00252
G1 X132.407 Y126.549 E.03963
G1 X132.277 Y126.849 E.01051
G1 X132.578 Y127.178 F30000
G1 F1983
G1 X132.192 Y128.067 E.03116
G3 X131.709 Y128.846 I-4.191 J-2.066 E.02951
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03526
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.526 Y130.467 E.03526
G1 X128.61 Y130.635 E.02995
G3 X127.694 Y130.665 I-.61 J-4.634 E.02951
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.256 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.798 J-2.721 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.299 Y125.105 E.03298
G1 X123.807 Y123.933 E.04111
G3 X124.291 Y123.154 I4.194 J2.068 E.02951
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03525
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.01489
G1 X126.474 Y121.533 E.03526
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.336 I.61 J4.634 E.0295
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.745 E.03298
G3 X131.407 Y121.39 I.459 J.496 E.0552
G1 X131.115 Y122.414 E.03423
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.797 J2.721 E.02952
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X132.701 Y126.895 E.03298
G1 X132.602 Y127.123 E.00801
G1 X132.902 Y127.453 F30000
G1 F1983
G1 X132.558 Y128.248 E.02785
G3 X131.557 Y129.653 I-5.523 J-2.875 E.05566
G1 X131.804 Y130.518 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.02891
G3 X127.668 Y131.071 I-1.446 J-6.054 E.05566
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.13 J-2.96 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.964 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G3 X124.443 Y122.347 I5.527 J2.877 E.05567
G1 X124.196 Y121.483 E.0289
G3 X125.321 Y120.157 I1.056 J-.244 E.06486
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.0289
G3 X128.332 Y120.929 I1.446 J6.054 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X131.804 Y121.483 I.736 J.796 E.08855
G1 X131.563 Y122.325 E.02815
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.13 J2.959 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08855
G1 X132.995 Y127.241 E.02716
G1 X132.926 Y127.398 E.00552
G1 X133.227 Y127.728 F30000
G1 F1983
G1 X132.923 Y128.428 E.02454
G3 X132.008 Y129.751 I-5.476 J-2.811 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.346 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.013 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.443 J-1.426 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
M73 P21 R10
G3 X123.992 Y122.249 I5.479 J2.813 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.456 J-.33 E.1219
G1 X126.756 Y120.654 E.02255
G3 X128.359 Y120.522 I1.3 J6.014 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.945 Y119.76 I1.024 J1.105 E.04229
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.425 E.12189
G1 X133.288 Y127.587 E.02135
G1 X133.251 Y127.673 E.00302
G1 X133.552 Y128.003 F30000
G1 F1983
G1 X133.289 Y128.608 E.02122
G3 X132.459 Y129.848 I-5.512 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.068 E.07177
G3 X125.918 Y132.539 I-1.955 J-1.556 E.03947
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.353 Y119.343 I1.913 J.147 E.09485
G3 X126.547 Y119.852 I-.163 J2.038 E.04247
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.069 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13167
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03393
G3 X134.051 Y127.816 I-1.07 J1.575 E.13732
G1 X133.582 Y127.933 E.01554
G1 X133.575 Y127.948 E.00052
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.577 J2.111 E.05794
G3 X125.359 Y118.951 I2.165 J-.8 E.13497
G3 X127.033 Y119.791 I-.125 J2.337 E.05737
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X133.924 Y128.256 I-.369 J2.268 E.19094
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22693
G1 X133.445 Y129.134 E-.15308
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.4 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z2.4
G1 Z2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113559
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146828
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178152
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207484
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.4 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z2.4
G1 Z2
G1 E.4 F1800
; LINE_WIDTH: 0.207442
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178114
G1 X129.798 Y122.182 E.00396
; LINE_WIDTH: 0.146807
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113549
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.4 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z2.4
G1 Z2
G1 E.4 F1800
; LINE_WIDTH: 0.11357
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146862
G1 X123.795 Y125.649 E.00091
; LINE_WIDTH: 0.178203
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.207552
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.4 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z2.4
G1 Z2
G1 E.4 F1800
; LINE_WIDTH: 0.207492
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178144
G1 X126.202 Y129.817 E.00396
; LINE_WIDTH: 0.146834
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113558
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 2.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 11/50
; update layer progress
M73 L11
M991 S0 P10 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z2.4 I1.17 J-.335 P1  F30000
G1 X124.613 Y123.926 Z2.4
G1 Z2.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.01365
G1 X125.984 Y122.507 E.0506
G1 X126.763 Y122.243 E.02646
G1 X127.474 Y122.002 E.02414
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.586 Y123.98 E.03502
G1 X124.978 Y124.106 F30000
G1 F1983
G1 X125.13 Y123.798 E.01105
G1 X126.191 Y122.867 E.04539
G1 X126.894 Y122.628 E.02386
G1 X127.528 Y122.413 E.02153
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.951 Y124.16 E.03241
G1 X125.343 Y124.286 F30000
G1 F1983
G1 X125.459 Y124.05 E.00845
G1 X126.399 Y123.226 E.04018
G1 X127.024 Y123.014 E.02125
G1 X127.582 Y122.825 E.01893
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.316 Y124.34 E.02981
G1 X125.708 Y124.466 F30000
G1 F1983
G1 X125.788 Y124.303 E.00584
G1 X126.606 Y123.586 E.03498
G1 X127.155 Y123.399 E.01865
G1 X127.636 Y123.236 E.01633
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.721 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.682 Y124.52 E.02721
G1 X126.073 Y124.646 F30000
G1 F1983
G1 X126.118 Y124.556 E.00324
G1 X126.814 Y123.945 E.02977
G1 X127.286 Y123.785 E.01605
G1 X127.69 Y123.648 E.01372
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
M73 P22 R10
G1 X125.708 Y125.386 E.02977
G1 X126.047 Y124.7 E.0246
M204 S250
G1 X126.425 Y124.819 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X126.435 Y124.799 E.00068
G1 X127.014 Y124.291 E.02293
G1 X127.412 Y124.156 E.01254
G1 X127.742 Y124.044 E.01039
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.398 Y124.873 E.02047
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.03143
G1 X127.014 Y124.291 E-.29252
G1 X127.153 Y124.244 E-.05605
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.6 I-.563 J1.079 P1  F30000
G1 X132.253 Y126.903 Z2.6
G1 Z2.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03449
G3 X131.37 Y128.615 I-3.406 J-1.629 E.02769
G1 X130.655 Y129.459 E.03556
G1 X131.015 Y130.728 E.04243
G1 X130.989 Y130.881 E.00498
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G1 X129.668 Y130.028 E.04244
G1 X128.534 Y130.232 E.03705
G3 X127.721 Y130.258 I-.536 J-4.114 E.02619
G1 X126.271 Y130.091 E.04692
G1 X125.413 Y130.975 E.03963
G1 X125.344 Y131.013 E.00252
G1 X125.241 Y131.03 E.00334
G1 X125.094 Y130.98 E.00499
G1 X125 Y130.857 E.00498
G1 X124.985 Y130.728 E.00418
G1 X125.334 Y129.497 E.04115
G1 X124.531 Y128.485 E.04153
G1 X124.292 Y128.114 E.0142
G1 X124.113 Y127.761 E.01272
G1 X123.639 Y126.56 E.04152
G1 X122.423 Y126.256 E.04031
G1 X122.331 Y126.206 E.00336
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00335
G1 X122.244 Y125.923 E.00334
G1 X122.294 Y125.831 E.00335
G1 X122.374 Y125.765 E.00335
G1 X123.593 Y125.451 E.04046
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.351 J1.595 E.0277
G1 X125.345 Y122.542 E.03554
G1 X124.985 Y121.272 E.04244
G1 X125.011 Y121.119 E.00499
G1 X125.116 Y121.006 E.00498
G1 X125.267 Y120.97 E.00499
G1 X125.412 Y121.025 E.00498
G1 X126.332 Y121.972 E.04246
G1 X127.466 Y121.768 E.03704
G3 X128.279 Y121.742 I.536 J4.117 E.0262
G1 X129.729 Y121.909 E.04692
G1 X130.567 Y121.042 E.03878
G1 X130.656 Y120.987 E.00337
G1 X130.785 Y120.972 E.00416
G1 X130.86 Y120.994 E.00252
G1 X130.945 Y121.054 E.00335
G1 X131 Y121.143 E.00335
G1 X131.017 Y121.246 E.00335
G1 X130.666 Y122.503 E.04199
G1 X131.468 Y123.515 E.04152
G1 X131.685 Y123.846 E.01274
G1 X131.887 Y124.239 E.0142
G1 X132.361 Y125.44 E.04152
G1 X133.602 Y125.753 E.04116
G1 X133.707 Y125.831 E.00418
G1 X133.762 Y125.948 E.00417
G1 X133.762 Y126.052 E.00334
G1 X133.735 Y126.126 E.00253
G1 X133.689 Y126.189 E.00251
G1 X133.602 Y126.247 E.00335
G1 X132.407 Y126.549 E.03963
G1 X132.277 Y126.848 E.0105
G1 X133 Y126.82 F30000
G1 F1983
G1 X132.701 Y126.895 E.00993
G1 X132.192 Y128.068 E.04111
G3 X131.708 Y128.846 I-4.194 J-2.068 E.02951
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03524
G3 X130.289 Y131.255 I-.659 J.149 E.0552
G1 X129.527 Y130.468 E.03524
G1 X128.61 Y130.635 E.02995
G3 X127.694 Y130.665 I-.61 J-4.637 E.02951
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.256 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03545
G3 X123.742 Y127.929 I3.798 J-2.721 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.646 E.03423
G3 X122.304 Y125.355 I.2 J-.646 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.154 I4.191 J2.067 E.0295
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.745 I.659 J-.149 E.0552
G1 X126.474 Y121.533 E.03526
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.335 I.61 J4.634 E.0295
G1 X129.576 Y121.482 E.04111
G1 X130.289 Y120.745 E.03297
G3 X130.838 Y120.568 I.464 J.5 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03618
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.799 J2.723 E.02951
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.059 Y126.805 E.02112
G1 X133.219 Y127.185 F30000
G1 F1983
G1 X132.995 Y127.241 E.00743
G1 X132.558 Y128.248 E.0353
G3 X131.557 Y129.654 I-5.541 J-2.886 E.05566
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08855
G1 X129.385 Y130.907 E.02889
G3 X127.668 Y131.071 I-1.446 J-6.071 E.05567
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.518 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02937
G3 X123.371 Y128.097 I4.129 J-2.959 E.03208
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02815
G3 X122.186 Y124.965 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.527 J2.877 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.058 J-.239 E.08855
G1 X126.615 Y121.093 E.0289
G3 X128.332 Y120.929 I1.446 J6.054 E.05566
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02716
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.144 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.129 J2.959 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.035 I-.321 J1.035 E.08854
G1 X133.277 Y127.17 E.01781
G1 X133.437 Y127.55 F30000
G1 F1983
G1 X133.288 Y127.587 E.00493
G1 X132.923 Y128.428 E.02948
G3 X132.008 Y129.751 I-5.491 J-2.821 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.029 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08123
G1 X122.068 Y127.426 E.02207
G3 X122.068 Y124.575 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.479 J2.813 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.15 I1.456 J-.329 E.12189
G1 X126.756 Y120.654 E.02255
G3 X128.359 Y120.522 I1.3 J6.014 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02135
G3 X130.939 Y119.76 I1.024 J1.104 E.04212
G1 X130.946 Y119.76 E.00021
G3 X132.201 Y121.575 I-.2 J1.48 E.07984
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.56 J4.081 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.933 Y127.425 I-.442 J1.426 E.12189
G1 X133.495 Y127.535 E.0145
G1 X133.655 Y127.915 F30000
G1 F1983
G1 X133.582 Y127.933 E.00244
G3 X132.459 Y129.848 I-5.808 J-2.117 E.07177
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.073 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.332 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.875 E.03393
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.348 Y119.343 I1.913 J.147 E.09467
G3 X126.547 Y119.852 I-.156 J2.035 E.04264
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.068 E.07177
G3 X130.082 Y119.461 I1.956 J1.556 E.03947
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.78 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03393
G3 X134.051 Y127.816 I-1.058 J1.577 E.13764
G1 X133.713 Y127.9 E.01118
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.58 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19276
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.113 J-3.49 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19228
M73 P23 R10
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.354 Y118.951 I2.165 J-.8 E.13481
G3 X127.033 Y119.791 I-.118 J2.336 E.05753
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22704
G1 X133.446 Y129.134 E-.15296
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.6 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z2.6
G1 Z2.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.11355
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146801
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178101
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207428
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.6 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z2.6
G1 Z2.2
G1 E.4 F1800
; LINE_WIDTH: 0.207421
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178081
G1 X129.798 Y122.183 E.00395
; LINE_WIDTH: 0.146797
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113545
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.6 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z2.6
G1 Z2.2
G1 E.4 F1800
; LINE_WIDTH: 0.113552
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146809
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.17809
G1 X123.621 Y125.975 E.00395
; LINE_WIDTH: 0.207424
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.6 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z2.6
G1 Z2.2
G1 E.4 F1800
; LINE_WIDTH: 0.207477
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178126
G1 X126.202 Y129.817 E.00396
; LINE_WIDTH: 0.146831
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113557
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 2.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 12/50
; update layer progress
M73 L12
M991 S0 P11 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z2.6 I1.17 J-.336 P1  F30000
G1 X124.609 Y123.933 Z2.6
G1 Z2.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1984
G1 X124.801 Y123.545 E.0139
G1 X125.984 Y122.507 E.0506
G1 X126.797 Y122.231 E.02762
G1 X127.474 Y122.002 E.02298
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.583 Y123.987 E.03477
G1 X124.974 Y124.113 F30000
G1 F1984
G1 X125.13 Y123.798 E.0113
G1 X126.191 Y122.867 E.04539
G1 X126.928 Y122.617 E.02502
G1 X127.528 Y122.413 E.02037
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.948 Y124.167 E.03216
G1 X125.339 Y124.293 F30000
G1 F1984
G1 X125.459 Y124.05 E.0087
G1 X126.399 Y123.226 E.04018
G1 X127.059 Y123.002 E.02241
G1 X127.582 Y122.825 E.01777
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.313 Y124.347 E.02956
G1 X125.705 Y124.473 F30000
G1 F1984
G1 X125.788 Y124.303 E.00609
G1 X126.606 Y123.586 E.03498
G1 X127.19 Y123.388 E.01981
G1 X127.636 Y123.236 E.01516
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.678 Y124.527 E.02695
G1 X126.07 Y124.653 F30000
G1 F1984
G1 X126.118 Y124.556 E.00349
G1 X126.814 Y123.945 E.02977
G1 X127.32 Y123.773 E.01721
G1 X127.69 Y123.648 E.01256
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.043 Y124.707 E.02435
M204 S250
G1 X126.421 Y124.826 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1984
M204 S5000
G1 X126.435 Y124.799 E.00091
G1 X127.014 Y124.291 E.02293
G1 X127.446 Y124.144 E.01362
G1 X127.742 Y124.044 E.00931
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.395 Y124.88 E.02023
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.03441
G1 X127.014 Y124.291 E-.29252
G1 X127.146 Y124.247 E-.05307
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.8 I-.562 J1.08 P1  F30000
G1 X132.254 Y126.903 Z2.8
G1 Z2.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1984
G1 X131.827 Y127.887 E.0345
G3 X131.37 Y128.616 I-3.345 J-1.592 E.02771
G1 X130.655 Y129.458 E.03554
G1 X131.015 Y130.728 E.04245
G1 X130.989 Y130.881 E.00498
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.588 Y130.975 E.00498
G1 X129.668 Y130.028 E.04244
G1 X128.534 Y130.232 E.03706
G3 X127.721 Y130.258 I-.536 J-4.114 E.02619
G1 X126.271 Y130.091 E.04691
G1 X125.413 Y130.975 E.03963
G1 X125.267 Y131.03 E.00499
G1 X125.164 Y131.016 E.00335
G1 X125.095 Y130.98 E.00252
G1 X125.011 Y130.881 E.00418
G1 X124.985 Y130.728 E.00499
G1 X125.334 Y129.497 E.04115
G1 X124.532 Y128.485 E.04152
G1 X124.292 Y128.114 E.01421
G1 X124.113 Y127.761 E.01272
G1 X123.639 Y126.56 E.04152
G1 X122.423 Y126.256 E.04031
G1 X122.331 Y126.207 E.00335
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00336
G1 X122.245 Y125.923 E.00334
G1 X122.294 Y125.831 E.00335
G1 X122.374 Y125.765 E.00335
G1 X123.593 Y125.451 E.04047
G1 X124.173 Y124.113 E.04691
G3 X124.63 Y123.385 I3.346 J1.592 E.02771
G1 X125.345 Y122.542 E.03554
G1 X124.985 Y121.272 E.04245
G1 X125.011 Y121.119 E.00499
G1 X125.117 Y121.006 E.00498
G1 X125.267 Y120.97 E.00498
G1 X125.413 Y121.025 E.00498
G1 X126.332 Y121.972 E.04246
G1 X127.466 Y121.768 E.03703
G3 X128.279 Y121.742 I.536 J4.116 E.02621
G1 X129.728 Y121.909 E.04691
G1 X130.568 Y121.042 E.0388
G1 X130.681 Y120.979 E.00416
G1 X130.785 Y120.972 E.00336
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00335
G1 X131 Y121.143 E.00252
G1 X131.017 Y121.246 E.00335
G1 X130.666 Y122.503 E.04198
G1 X131.468 Y123.515 E.04152
G1 X131.685 Y123.846 E.01273
G1 X131.887 Y124.239 E.0142
G1 X132.361 Y125.44 E.04152
G1 X133.602 Y125.753 E.04116
G1 X133.706 Y125.831 E.00417
G1 X133.762 Y125.948 E.00417
G1 X133.762 Y126.052 E.00334
G1 X133.735 Y126.126 E.00253
G1 X133.689 Y126.189 E.00252
G1 X133.602 Y126.247 E.00334
G1 X132.407 Y126.549 E.03963
G1 X132.277 Y126.848 E.01049
G1 X133 Y126.82 F30000
G1 F1984
G1 X132.701 Y126.895 E.00992
G1 X132.192 Y128.068 E.04111
G3 X131.709 Y128.846 I-4.194 J-2.069 E.02951
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03526
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.527 Y130.468 E.03525
G1 X128.61 Y130.635 E.02995
G3 X127.694 Y130.665 I-.61 J-4.636 E.02952
G1 X126.424 Y130.518 E.0411
G1 X125.711 Y131.256 E.03299
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.886 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.795 J-2.72 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.646 E.03423
G3 X122.304 Y125.355 I.2 J-.646 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.0411
G3 X124.291 Y123.154 I4.191 J2.067 E.02951
G1 X124.894 Y122.444 E.02995
M73 P23 R9
G1 X124.593 Y121.39 E.03525
M73 P24 R9
G3 X125.711 Y120.744 I.659 J-.149 E.05519
G1 X126.474 Y121.533 E.03527
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.336 I.61 J4.634 E.02951
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.744 E.03299
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.115 Y122.414 E.03423
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.798 J2.722 E.02951
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.058 Y126.805 E.02113
G1 X133.218 Y127.185 F30000
G1 F1984
G1 X132.995 Y127.241 E.00742
G1 X132.558 Y128.248 E.03529
G3 X131.557 Y129.653 I-5.526 J-2.877 E.05566
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.02889
G3 X127.668 Y131.071 I-1.446 J-6.068 E.05567
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.127 J-2.958 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02815
G3 X122.186 Y124.965 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G3 X124.443 Y122.347 I5.524 J2.876 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.057 J-.239 E.08854
G1 X126.615 Y121.093 E.02891
G3 X128.332 Y120.929 I1.446 J6.055 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02718
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05803
G1 X131.563 Y122.325 E.02815
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.902 I-4.129 J2.959 E.03208
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.036 E.08854
G1 X133.277 Y127.17 E.01782
G1 X133.437 Y127.55 F30000
G1 F1984
G1 X133.288 Y127.587 E.00492
G1 X132.923 Y128.428 E.02948
G3 X132.008 Y129.751 I-5.479 J-2.813 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.452 J.336 E.12218
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.028 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12218
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.442 J-1.426 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.477 J2.812 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.654 E.02255
G3 X128.359 Y120.522 I1.3 J6.015 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.933 Y119.759 I1.023 J1.103 E.0419
G3 X132.201 Y121.575 I-.182 J1.478 E.08032
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.433 J1.425 E.12226
G1 X133.495 Y127.535 E.0145
G1 X133.552 Y128.002 F30000
G1 F1984
G1 X133.289 Y128.608 E.02124
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.072 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.489 J-2.875 E.03392
G3 X121.949 Y124.185 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.805 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.342 Y119.343 I1.912 J.147 E.0945
G3 X126.547 Y119.852 I-.149 J2.032 E.0428
G1 X126.897 Y120.214 E.0162
G3 X129.117 Y120.2 I1.149 J6.069 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.874 E.03393
G3 X134.051 Y127.816 I-1.069 J1.575 E.13736
G1 X133.582 Y127.933 E.01555
G1 X133.576 Y127.947 E.00049
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1984
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19277
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19228
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.349 Y118.951 I2.165 J-.8 E.13465
G3 X127.033 Y119.791 I-.112 J2.335 E.05769
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X133.924 Y128.256 I-.367 J2.268 E.19102
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22694
G1 X133.445 Y129.134 E-.15306
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.8 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z2.8
G1 Z2.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113554
G1 F1984
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146815
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178108
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207443
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.8 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z2.8
G1 Z2.4
G1 E.4 F1800
; LINE_WIDTH: 0.207368
G1 F1984
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.17805
G1 X129.798 Y122.182 E.00395
; LINE_WIDTH: 0.146782
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113541
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.8 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z2.8
G1 Z2.4
G1 E.4 F1800
; LINE_WIDTH: 0.113548
G1 F1984
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146795
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.178075
G1 X123.621 Y125.975 E.00395
; LINE_WIDTH: 0.207406
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z2.8 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z2.8
G1 Z2.4
G1 E.4 F1800
; LINE_WIDTH: 0.20742
G1 F1984
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178094
G1 X126.202 Y129.818 E.00395
; LINE_WIDTH: 0.146801
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113548
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 2.6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 13/50
; update layer progress
M73 L13
M991 S0 P12 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z2.8 I1.169 J-.337 P1  F30000
G1 X124.606 Y123.94 Z2.8
G1 Z2.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.01416
G1 X125.984 Y122.507 E.0506
G1 X126.831 Y122.22 E.02878
G1 X127.474 Y122.002 E.02181
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
M73 P25 R9
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.579 Y123.994 E.03451
G1 X124.971 Y124.12 F30000
G1 F1983
G1 X125.13 Y123.798 E.01155
G1 X126.191 Y122.867 E.04539
G1 X126.962 Y122.605 E.02618
G1 X127.528 Y122.413 E.01921
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.944 Y124.174 E.03191
G1 X125.336 Y124.3 F30000
G1 F1983
G1 X125.459 Y124.05 E.00895
G1 X126.399 Y123.226 E.04018
G1 X127.093 Y122.991 E.02358
G1 X127.582 Y122.825 E.01661
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.309 Y124.354 E.02931
G1 X125.701 Y124.48 F30000
G1 F1983
G1 X125.788 Y124.303 E.00635
G1 X126.606 Y123.586 E.03498
G1 X127.224 Y123.376 E.02097
G1 X127.636 Y123.236 E.014
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.675 Y124.534 E.0267
G1 X126.066 Y124.66 F30000
G1 F1983
G1 X126.118 Y124.556 E.00374
G1 X126.814 Y123.945 E.02977
G1 X127.355 Y123.762 E.01837
G1 X127.69 Y123.648 E.0114
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.04 Y124.714 E.0241
M204 S250
G1 X126.418 Y124.833 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X126.435 Y124.799 E.00114
G1 X127.014 Y124.291 E.02293
G1 X127.481 Y124.133 E.01469
G1 X127.742 Y124.044 E.00824
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.391 Y124.887 E.02
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.03739
G1 X127.014 Y124.291 E-.29252
G1 X127.138 Y124.249 E-.05009
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3 I-.56 J1.08 P1  F30000
G1 X132.254 Y126.903 Z3
G1 Z2.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.888 E.03452
G3 X131.37 Y128.615 I-3.353 J-1.597 E.0277
G1 X130.655 Y129.458 E.03555
G1 X131.015 Y130.728 E.04244
G1 X130.989 Y130.881 E.00499
G1 X130.884 Y130.994 E.00498
G1 X130.733 Y131.03 E.00499
G1 X130.587 Y130.975 E.00499
G1 X129.668 Y130.028 E.04243
G1 X128.533 Y130.232 E.03706
G3 X127.721 Y130.258 I-.536 J-4.113 E.02619
G1 X126.271 Y130.091 E.04691
G1 X125.413 Y130.975 E.03963
G1 X125.267 Y131.03 E.00499
G1 X125.164 Y131.016 E.00336
G1 X125.095 Y130.98 E.00251
G1 X125 Y130.857 E.00498
G1 X124.985 Y130.728 E.00418
G1 X125.334 Y129.497 E.04115
G1 X124.531 Y128.485 E.04152
G1 X124.292 Y128.114 E.0142
G1 X124.113 Y127.761 E.01273
G1 X123.639 Y126.56 E.04152
G1 X122.422 Y126.255 E.04032
G1 X122.331 Y126.206 E.00334
G1 X122.265 Y126.126 E.00334
G1 X122.234 Y126.026 E.00336
G1 X122.245 Y125.923 E.00335
G1 X122.294 Y125.831 E.00336
G1 X122.374 Y125.765 E.00334
G1 X123.593 Y125.451 E.04047
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.384 I3.34 J1.588 E.02771
G1 X125.345 Y122.542 E.03554
G1 X124.983 Y121.246 E.04328
G1 X125 Y121.143 E.00335
G1 X125.055 Y121.054 E.00336
G1 X125.14 Y120.994 E.00335
G1 X125.267 Y120.97 E.00417
G1 X125.344 Y120.987 E.00252
G1 X125.433 Y121.042 E.00335
G1 X126.333 Y121.972 E.04163
G1 X127.466 Y121.768 E.03702
G3 X128.279 Y121.742 I.536 J4.12 E.02622
G1 X129.729 Y121.909 E.04691
G1 X130.587 Y121.025 E.03963
G1 X130.733 Y120.97 E.00499
G1 X130.836 Y120.984 E.00335
G1 X130.905 Y121.02 E.00251
G1 X131 Y121.143 E.00499
G1 X131.015 Y121.272 E.00418
G1 X130.666 Y122.503 E.04116
G1 X131.468 Y123.515 E.04151
G1 X131.685 Y123.846 E.01273
G1 X131.887 Y124.239 E.0142
G1 X132.361 Y125.44 E.04152
G1 X133.577 Y125.745 E.04032
G1 X133.669 Y125.794 E.00335
G1 X133.736 Y125.874 E.00336
G1 X133.766 Y125.974 E.00335
G1 X133.755 Y126.078 E.00335
G1 X133.706 Y126.169 E.00335
G1 X133.626 Y126.235 E.00334
G1 X132.407 Y126.549 E.04047
G1 X132.278 Y126.847 E.01048
G1 X132.578 Y127.177 F30000
G1 F1983
G1 X132.192 Y128.068 E.0312
G3 X131.709 Y128.846 I-4.192 J-2.068 E.0295
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03525
G3 X130.289 Y131.255 I-.659 J.149 E.0552
G1 X129.527 Y130.468 E.03524
G1 X128.61 Y130.635 E.02995
G3 X127.694 Y130.665 I-.61 J-4.637 E.02952
G1 X126.424 Y130.518 E.0411
G1 X125.711 Y131.256 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.797 J-2.721 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.155 I4.193 J2.068 E.0295
G1 X124.894 Y122.444 E.02996
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.745 I.659 J-.149 E.0552
G1 X126.474 Y121.533 E.03527
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.336 I.61 J4.633 E.0295
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.745 E.03298
G3 X130.838 Y120.568 I.464 J.501 E.01914
G3 X131.407 Y121.39 I-.09 J.67 E.03618
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03543
G3 X132.258 Y124.071 I-3.797 J2.721 E.02952
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.354 E.03424
G3 X133.696 Y126.646 I-.2 J.646 E.05521
G1 X132.701 Y126.895 E.03298
G1 X132.602 Y127.122 E.00798
G1 X132.903 Y127.452 F30000
G1 F1983
G1 X132.558 Y128.248 E.02789
G3 X131.557 Y129.653 I-5.528 J-2.878 E.05566
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08855
G1 X129.385 Y130.907 E.02889
G3 X127.668 Y131.071 I-1.446 J-6.073 E.05567
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.518 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.129 J-2.959 E.03209
G1 X123.035 Y127.248 E.02935
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.524 J2.876 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.057 J-.239 E.08855
G1 X126.615 Y121.093 E.02891
G3 X128.332 Y120.929 I1.445 J6.044 E.05566
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03071
G3 X131.804 Y121.483 I-.144 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.128 J2.959 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.964 E.02816
G3 X133.814 Y127.036 I-.321 J1.036 E.08855
G1 X132.995 Y127.241 E.02717
G1 X132.927 Y127.397 E.00548
G1 X133.227 Y127.727 F30000
G1 F1983
G1 X132.923 Y128.428 E.02457
G3 X132.008 Y129.751 I-5.481 J-2.815 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.031 E.05188
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.017 J-1.09 E.12217
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.476 J2.812 E.05187
G1 X123.799 Y121.575 E.02254
M73 P26 R9
G3 X125.33 Y119.75 I1.453 J-.336 E.08873
G3 X126.268 Y120.15 I-.128 J1.6 E.03336
G1 X126.756 Y120.654 E.02255
G3 X128.359 Y120.522 I1.3 J6.005 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.017 J1.089 E.12217
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.079 E.08123
G1 X133.932 Y124.574 E.02208
G3 X133.932 Y127.426 I-.435 J1.426 E.12218
G1 X133.288 Y127.587 E.02135
G1 X133.251 Y127.672 E.00298
G1 X133.552 Y128.002 F30000
G1 F1983
G1 X133.289 Y128.608 E.02126
G3 X132.459 Y129.848 I-5.512 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01618
G3 X126.883 Y131.8 I-1.149 J-6.074 E.07178
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.332 J-3.779 E.07165
G3 X121.446 Y127.577 I.489 J-2.876 E.03392
G3 X121.949 Y124.185 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.805 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.337 Y119.343 I1.912 J.147 E.09433
G3 X126.547 Y119.852 I-.142 J2.03 E.04298
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.15 J6.067 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.666 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07164
G3 X134.554 Y124.422 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.07 J1.575 E.13733
G1 X133.582 Y127.933 E.01554
G1 X133.576 Y127.947 E.00048
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19228
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.343 Y118.951 I2.165 J-.8 E.13449
G3 X127.033 Y119.791 I-.106 J2.334 E.05785
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.369 J2.268 E.19094
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22696
G1 X133.445 Y129.134 E-.15304
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z3
G1 Z2.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113555
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146815
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178127
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207462
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z3
G1 Z2.6
G1 E.4 F1800
; LINE_WIDTH: 0.207446
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178116
G1 X129.798 Y122.182 E.00396
; LINE_WIDTH: 0.146813
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113552
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z3
G1 Z2.6
G1 E.4 F1800
; LINE_WIDTH: 0.113554
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146815
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.178118
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.207446
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z3
G1 Z2.6
G1 E.4 F1800
; LINE_WIDTH: 0.207452
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178118
G1 X126.202 Y129.818 E.00396
; LINE_WIDTH: 0.14681
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.11355
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 2.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 14/50
; update layer progress
M73 L14
M991 S0 P13 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z3 I1.169 J-.338 P1  F30000
G1 X124.602 Y123.947 Z3
G1 Z2.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.01441
G1 X125.984 Y122.507 E.0506
G1 X126.865 Y122.208 E.02995
G1 X127.474 Y122.002 E.02065
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.576 Y124.001 E.03426
G1 X124.967 Y124.127 F30000
G1 F1983
G1 X125.13 Y123.798 E.01181
G1 X126.191 Y122.867 E.04539
G1 X126.996 Y122.594 E.02734
G1 X127.528 Y122.413 E.01805
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.941 Y124.181 E.03166
G1 X125.333 Y124.307 F30000
G1 F1983
G1 X125.459 Y124.05 E.0092
G1 X126.399 Y123.226 E.04018
G1 X127.127 Y122.979 E.02474
G1 X127.582 Y122.825 E.01544
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.306 Y124.361 E.02905
G1 X125.698 Y124.487 F30000
G1 F1983
G1 X125.788 Y124.303 E.0066
G1 X126.606 Y123.586 E.03498
G1 X127.258 Y123.365 E.02213
G1 X127.636 Y123.236 E.01284
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.671 Y124.541 E.02645
G1 X126.063 Y124.667 F30000
G1 F1983
G1 X126.118 Y124.556 E.00399
G1 X126.814 Y123.945 E.02977
G1 X127.389 Y123.75 E.01953
G1 X127.69 Y123.648 E.01024
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.036 Y124.721 E.02385
M204 S250
G1 X126.414 Y124.84 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
M73 P27 R9
G1 F1983
M204 S5000
G1 X126.435 Y124.799 E.00138
G1 X127.014 Y124.291 E.02293
G1 X127.515 Y124.121 E.01577
G1 X127.742 Y124.044 E.00716
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.388 Y124.894 E.01977
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.04036
G1 X127.014 Y124.291 E-.29252
G1 X127.131 Y124.252 E-.04712
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.2 I-.559 J1.081 P1  F30000
G1 X132.254 Y126.902 Z3.2
G1 Z2.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.888 E.03453
G3 X131.37 Y128.616 I-3.42 J-1.638 E.0277
G1 X130.655 Y129.459 E.03556
G1 X131.015 Y130.728 E.04242
G1 X130.989 Y130.881 E.00498
G1 X130.883 Y130.994 E.00498
G1 X130.732 Y131.03 E.00499
G1 X130.587 Y130.975 E.00498
G1 X129.668 Y130.029 E.04243
G1 X128.533 Y130.232 E.03708
G3 X127.721 Y130.258 I-.535 J-4.112 E.02618
G1 X126.271 Y130.091 E.04692
G1 X125.412 Y130.975 E.03964
G1 X125.267 Y131.03 E.00498
G1 X125.164 Y131.016 E.00335
G1 X125.095 Y130.98 E.00251
G1 X125.011 Y130.881 E.00417
G1 X124.985 Y130.728 E.00499
G1 X125.334 Y129.497 E.04116
G1 X124.532 Y128.485 E.04152
G1 X124.292 Y128.114 E.0142
G1 X124.113 Y127.761 E.01273
G1 X123.639 Y126.56 E.04152
G1 X122.422 Y126.255 E.04032
G1 X122.331 Y126.206 E.00335
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00335
G1 X122.245 Y125.923 E.00334
G1 X122.294 Y125.83 E.00336
G1 X122.374 Y125.765 E.00334
G1 X123.593 Y125.451 E.04046
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.35 J1.595 E.0277
G1 X125.345 Y122.542 E.03554
G1 X124.985 Y121.272 E.04245
G1 X125.011 Y121.119 E.00499
G1 X125.117 Y121.006 E.00498
G1 X125.268 Y120.971 E.00498
G1 X125.413 Y121.025 E.00498
G1 X126.332 Y121.971 E.04241
G1 X127.467 Y121.768 E.0371
G3 X128.279 Y121.742 I.535 J4.11 E.02616
G1 X129.729 Y121.909 E.04692
G1 X130.568 Y121.042 E.0388
G1 X130.681 Y120.979 E.00417
G1 X130.785 Y120.972 E.00335
G1 X130.86 Y120.994 E.00252
G1 X130.945 Y121.054 E.00335
G1 X131 Y121.143 E.00335
G1 X131.017 Y121.246 E.00335
G1 X130.666 Y122.503 E.04199
G1 X131.468 Y123.514 E.04151
G1 X131.708 Y123.886 E.01421
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04151
G1 X133.602 Y125.753 E.04116
G1 X133.706 Y125.831 E.00417
G1 X133.762 Y125.948 E.00417
G1 X133.762 Y126.052 E.00335
G1 X133.735 Y126.126 E.00253
G1 X133.669 Y126.206 E.00335
G1 X133.602 Y126.247 E.00252
G1 X132.407 Y126.549 E.03963
G1 X132.278 Y126.847 E.01046
G1 X132.578 Y127.177 F30000
G1 F1983
G1 X132.192 Y128.068 E.03122
G3 X131.708 Y128.846 I-4.195 J-2.069 E.02952
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03523
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.527 Y130.468 E.03524
G1 X128.611 Y130.635 E.02995
G3 X127.694 Y130.665 I-.611 J-4.638 E.02953
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.255 E.03298
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.798 J-2.722 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.154 I4.193 J2.068 E.0295
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03526
G3 X125.711 Y120.744 I.659 J-.149 E.05519
G1 X126.473 Y121.532 E.03523
G1 X127.389 Y121.366 E.02995
G3 X128.306 Y121.335 I.611 J4.637 E.02954
G1 X129.576 Y121.482 E.04111
G1 X130.289 Y120.745 E.03298
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03618
G1 X131.115 Y122.414 E.03423
G1 X131.8 Y123.277 E.03543
G3 X132.258 Y124.071 I-3.801 J2.724 E.02952
G1 X132.663 Y125.096 E.03543
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X132.701 Y126.895 E.03297
G1 X132.602 Y127.122 E.00797
G1 X132.903 Y127.452 F30000
G1 F1983
G1 X132.558 Y128.248 E.0279
G3 X131.557 Y129.654 I-5.549 J-2.891 E.05567
G1 X131.804 Y130.518 E.02888
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.386 Y130.907 E.02889
G3 X127.668 Y131.071 I-1.446 J-6.081 E.05567
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.129 J-2.959 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.527 J2.878 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.057 J-.239 E.08854
G1 X126.614 Y121.092 E.02888
G3 X128.332 Y120.929 I1.447 J6.095 E.05568
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05803
G1 X131.563 Y122.325 E.02815
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.132 J2.961 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.322 J1.035 E.08855
G1 X132.995 Y127.241 E.02716
G1 X132.927 Y127.397 E.00547
G1 X133.228 Y127.727 F30000
G1 F1983
G1 X132.923 Y128.428 E.02458
G3 X132.008 Y129.751 I-5.5 J-2.826 E.05187
G1 X132.201 Y130.425 E.02253
G3 X129.732 Y131.85 I-1.452 J.336 E.12217
G1 X129.244 Y131.347 E.02253
G3 X127.641 Y131.478 I-1.301 J-6.039 E.05188
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12218
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.435 J-1.426 E.12218
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.478 J2.813 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.149 I1.452 J-.336 E.12217
G1 X126.755 Y120.653 E.02253
G3 X128.359 Y120.522 I1.301 J6.051 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.922 Y119.758 I1.022 J1.102 E.04156
G3 X132.201 Y121.575 I-.188 J1.491 E.08041
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X134.979 Y126.168 I-.455 J1.44 E.06636
G3 X133.932 Y127.426 I-1.512 J-.194 E.05554
G1 X133.288 Y127.587 E.02135
G1 X133.251 Y127.672 E.00297
G1 X133.552 Y128.002 F30000
G1 F1983
G1 X133.289 Y128.608 E.02127
G3 X132.459 Y129.848 I-5.518 J-2.793 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.01618
G3 X126.883 Y131.8 I-1.149 J-6.075 E.07178
G3 X125.918 Y132.539 I-1.955 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.489 J-2.876 E.03392
G3 X121.949 Y124.185 I1.07 J-1.575 E.13732
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.805 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.332 Y119.343 I1.912 J.147 E.09415
G3 X126.547 Y119.852 I-.135 J2.027 E.04314
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.077 E.07178
G3 X130.082 Y119.461 I1.955 J1.556 E.03946
G3 X132.598 Y121.668 I.666 J1.779 E.13167
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07164
G3 X134.554 Y124.423 I-.489 J2.875 E.03392
G3 X134.051 Y127.816 I-1.056 J1.577 E.13772
G1 X133.582 Y127.933 E.01554
G1 X133.576 Y127.946 E.00047
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G3 X132.894 Y129.942 I-5.581 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19276
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
M73 P28 R9
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.338 Y118.951 I2.164 J-.8 E.13433
G3 X127.033 Y119.791 I-.101 J2.333 E.058
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22704
G1 X133.446 Y129.134 E-.15296
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.2 I1.087 J-.547 P1  F30000
G1 X132.153 Y126.567 Z3.2
G1 Z2.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113563
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146842
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178143
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207493
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.2 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z3.2
G1 Z2.8
G1 E.4 F1800
; LINE_WIDTH: 0.207423
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178082
G1 X129.798 Y122.183 E.00395
; LINE_WIDTH: 0.146799
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113545
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.2 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z3.2
G1 Z2.8
G1 E.4 F1800
; LINE_WIDTH: 0.113554
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146815
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.17811
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.207444
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.2 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z3.2
G1 Z2.8
G1 E.4 F1800
; LINE_WIDTH: 0.207494
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178145
G1 X126.202 Y129.817 E.00396
; LINE_WIDTH: 0.146835
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113559
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 3
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 15/50
; update layer progress
M73 L15
M991 S0 P14 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z3.2 I1.169 J-.339 P1  F30000
G1 X124.599 Y123.954 Z3.2
G1 Z3
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.01466
G1 X125.984 Y122.507 E.0506
G1 X126.9 Y122.197 E.03111
G1 X127.474 Y122.002 E.01949
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.572 Y124.008 E.03401
G1 X124.964 Y124.134 F30000
G1 F1983
G1 X125.13 Y123.798 E.01206
G1 X126.191 Y122.867 E.04539
G1 X127.03 Y122.582 E.02851
G1 X127.528 Y122.413 E.01689
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.938 Y124.188 E.03141
G1 X125.329 Y124.314 F30000
G1 F1983
G1 X125.459 Y124.05 E.00945
G1 X126.399 Y123.226 E.04018
G1 X127.161 Y122.967 E.0259
G1 X127.582 Y122.825 E.01428
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.303 Y124.368 E.0288
G1 X125.694 Y124.494 F30000
G1 F1983
G1 X125.788 Y124.303 E.00685
G1 X126.606 Y123.586 E.03498
G1 X127.292 Y123.353 E.0233
G1 X127.636 Y123.236 E.01168
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.721 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.668 Y124.548 E.0262
G1 X126.059 Y124.674 F30000
G1 F1983
G1 X126.118 Y124.556 E.00424
G1 X126.814 Y123.945 E.02977
G1 X127.423 Y123.738 E.02069
G1 X127.69 Y123.648 E.00908
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.033 Y124.728 E.0236
M204 S250
G1 X126.411 Y124.847 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X126.435 Y124.799 E.00161
G1 X127.014 Y124.291 E.02293
G1 X127.549 Y124.11 E.01684
G1 X127.742 Y124.044 E.00609
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.384 Y124.901 E.01953
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.04332
G1 X127.014 Y124.291 E-.29252
G1 X127.124 Y124.254 E-.04417
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.4 I-.558 J1.081 P1  F30000
G1 X132.254 Y126.902 Z3.4
G1 Z3
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.888 E.03454
G3 X131.37 Y128.615 I-3.354 J-1.597 E.0277
G1 X130.655 Y129.458 E.03555
G1 X131.015 Y130.728 E.04244
G1 X130.989 Y130.881 E.00499
G1 X130.884 Y130.994 E.00498
G1 X130.733 Y131.03 E.00499
G1 X130.587 Y130.975 E.00499
G1 X129.668 Y130.028 E.04245
G1 X128.534 Y130.232 E.03704
G3 X127.721 Y130.258 I-.536 J-4.116 E.0262
G1 X126.271 Y130.091 E.04691
G1 X125.413 Y130.975 E.03963
G1 X125.267 Y131.03 E.00499
G1 X125.189 Y131.023 E.00252
G1 X125.094 Y130.98 E.00335
G1 X125 Y130.857 E.00498
G1 X124.985 Y130.728 E.00417
G1 X125.334 Y129.497 E.04116
G1 X124.532 Y128.485 E.04151
G1 X124.292 Y128.114 E.01421
G1 X124.113 Y127.761 E.01272
G1 X123.639 Y126.56 E.04153
G1 X122.423 Y126.256 E.04031
G1 X122.331 Y126.206 E.00336
G1 X122.265 Y126.126 E.00334
G1 X122.234 Y126.026 E.00336
G1 X122.244 Y125.923 E.00333
G1 X122.294 Y125.831 E.00336
G1 X122.374 Y125.765 E.00334
G1 X123.593 Y125.451 E.04047
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.363 J1.603 E.0277
G1 X125.345 Y122.542 E.03555
G1 X124.985 Y121.272 E.04245
G1 X125.011 Y121.119 E.00499
G1 X125.116 Y121.006 E.00498
G1 X125.267 Y120.97 E.00499
G1 X125.413 Y121.025 E.00498
G1 X126.332 Y121.971 E.04241
G1 X127.467 Y121.768 E.0371
G3 X128.279 Y121.742 I.535 J4.108 E.02617
G1 X129.729 Y121.909 E.04691
G1 X130.568 Y121.042 E.0388
G1 X130.681 Y120.979 E.00416
G1 X130.785 Y120.972 E.00337
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.075 E.00336
G1 X131.008 Y121.168 E.00335
G1 X131.017 Y121.245 E.00251
G1 X130.666 Y122.503 E.042
G1 X131.468 Y123.515 E.04152
G1 X131.708 Y123.886 E.01421
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04152
G1 X133.602 Y125.753 E.04116
G1 X133.706 Y125.831 E.00417
G1 X133.762 Y125.948 E.00418
G1 X133.762 Y126.052 E.00334
G1 X133.735 Y126.126 E.00253
G1 X133.689 Y126.189 E.0025
G1 X133.602 Y126.247 E.00335
G1 X132.407 Y126.549 E.03964
G1 X132.278 Y126.847 E.01045
G1 X132.579 Y127.177 F30000
G1 F1983
G1 X132.192 Y128.068 E.03123
G3 X131.709 Y128.846 I-4.193 J-2.068 E.0295
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03525
G3 X130.289 Y131.256 I-.659 J.149 E.0552
G1 X129.526 Y130.468 E.03526
G1 X128.61 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.635 E.02951
G1 X126.424 Y130.518 E.0411
G1 X125.711 Y131.256 E.03299
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03543
G3 X123.742 Y127.929 I3.795 J-2.72 E.02952
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.646 E.03423
G3 X122.304 Y125.355 I.2 J-.646 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.154 I4.194 J2.069 E.02951
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03526
G3 X125.711 Y120.745 I.659 J-.149 E.05519
G1 X126.473 Y121.532 E.03523
G1 X127.389 Y121.366 E.02994
M73 P29 R9
G3 X128.306 Y121.336 I.611 J4.638 E.02954
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.744 E.03299
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03616
G1 X131.115 Y122.414 E.03425
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.798 J2.721 E.02952
G1 X132.663 Y125.096 E.03544
G1 X133.696 Y125.355 E.03424
G3 X133.695 Y126.646 I-.2 J.645 E.0552
G1 X132.701 Y126.895 E.03297
G1 X132.602 Y127.122 E.00796
G1 X133.217 Y127.185 F30000
G1 F1983
G1 X132.995 Y127.241 E.00739
G1 X132.558 Y128.248 E.0353
G3 X131.557 Y129.653 I-5.528 J-2.878 E.05566
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.057 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X127.668 Y131.071 I-1.446 J-6.062 E.05567
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.739 J-.791 E.08875
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.128 J-2.958 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.529 J2.879 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.055 J-.244 E.08875
G1 X126.614 Y121.092 E.02888
G3 X128.332 Y120.929 I1.447 J6.09 E.05568
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05802
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.13 J2.959 E.03209
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.316 J1.035 E.08875
G1 X133.276 Y127.17 E.01784
G1 X133.228 Y127.726 F30000
G1 F1983
G1 X132.923 Y128.428 E.02459
G3 X132.008 Y129.751 I-5.481 J-2.815 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.02 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12217
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.481 J2.815 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02253
G3 X128.359 Y120.522 I1.301 J6.047 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.945 Y119.76 I1.024 J1.105 E.04229
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.557 J4.079 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.435 J1.425 E.12218
G1 X133.288 Y127.587 E.02135
G1 X133.252 Y127.671 E.00296
G1 X133.654 Y127.915 F30000
G1 F1983
G1 X133.582 Y127.933 E.00239
G3 X132.459 Y129.848 I-5.805 J-2.116 E.07177
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.873 E.03392
G3 X121.949 Y124.185 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.805 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.326 Y119.343 I1.912 J.147 E.09398
G3 X126.547 Y119.852 I-.128 J2.025 E.04331
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.077 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.778 E.07165
G3 X134.554 Y124.423 I-.488 J2.873 E.03393
G3 X134.051 Y127.816 I-1.07 J1.575 E.13733
G1 X133.712 Y127.9 E.01122
M204 S250
G1 X133.866 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X133.865 Y128.266 E.00004
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.333 Y118.951 I2.164 J-.8 E.13417
G3 X127.033 Y119.791 I-.095 J2.333 E.05816
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.111 J3.488 E.05782
G3 X134.166 Y128.195 I-.369 J2.268 E.18349
G1 X133.924 Y128.252 E.00739
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02336
G1 X133.641 Y128.782 E-.21357
G1 X133.458 Y129.111 E-.14307
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.4 I1.083 J-.555 P1  F30000
G1 X132.153 Y126.567 Z3.4
G1 Z3
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113565
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146848
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178156
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207501
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.4 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z3.4
G1 Z3
G1 E.4 F1800
; LINE_WIDTH: 0.207442
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178114
G1 X129.798 Y122.182 E.00396
; LINE_WIDTH: 0.146807
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113549
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.4 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z3.4
G1 Z3
G1 E.4 F1800
; LINE_WIDTH: 0.113554
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146815
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.17812
G1 X123.621 Y125.975 E.00395
; LINE_WIDTH: 0.207447
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.4 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z3.4
G1 Z3
G1 E.4 F1800
; LINE_WIDTH: 0.207428
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178097
G1 X126.202 Y129.818 E.00395
; LINE_WIDTH: 0.146813
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113551
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 3.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 16/50
; update layer progress
M73 L16
M991 S0 P15 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z3.4 I1.169 J-.34 P1  F30000
G1 X124.596 Y123.961 Z3.4
G1 Z3.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.01491
G1 X125.984 Y122.507 E.0506
G1 X126.934 Y122.185 E.03227
G1 X127.474 Y122.002 E.01833
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
M73 P30 R9
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.569 Y124.015 E.03377
G1 X124.961 Y124.141 F30000
G1 F1983
G1 X125.13 Y123.798 E.0123
G1 X126.191 Y122.867 E.04539
G1 X127.065 Y122.57 E.02967
G1 X127.528 Y122.413 E.01572
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.934 Y124.195 E.03116
G1 X125.326 Y124.321 F30000
G1 F1983
G1 X125.459 Y124.05 E.0097
G1 X126.399 Y123.226 E.04018
G1 X127.196 Y122.956 E.02706
G1 X127.582 Y122.825 E.01312
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.299 Y124.375 E.02856
G1 X125.691 Y124.501 F30000
G1 F1983
G1 X125.788 Y124.303 E.00709
G1 X126.606 Y123.586 E.03498
G1 X127.326 Y123.341 E.02446
G1 X127.636 Y123.236 E.01052
G1 X128.721 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.721 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.664 Y124.555 E.02595
G1 X126.056 Y124.681 F30000
G1 F1983
G1 X126.118 Y124.556 E.00449
G1 X126.814 Y123.945 E.02977
G1 X127.457 Y123.727 E.02185
G1 X127.69 Y123.648 E.00792
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.029 Y124.735 E.02335
M204 S250
G1 X126.408 Y124.854 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X126.435 Y124.799 E.00184
G1 X127.014 Y124.291 E.02293
G1 X127.583 Y124.098 E.01792
G1 X127.742 Y124.044 E.00501
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.381 Y124.908 E.01931
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.04623
G1 X127.014 Y124.291 E-.29252
G1 X127.116 Y124.257 E-.04125
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.6 I-.557 J1.082 P1  F30000
G1 X132.254 Y126.902 Z3.6
G1 Z3.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03455
G3 X131.37 Y128.615 I-3.358 J-1.6 E.0277
G1 X130.655 Y129.458 E.03555
G1 X131.015 Y130.728 E.04245
G1 X130.989 Y130.881 E.00499
G1 X130.884 Y130.994 E.00497
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G1 X129.667 Y130.028 E.04246
G1 X128.535 Y130.232 E.03701
G3 X127.721 Y130.258 I-.536 J-4.119 E.02622
G1 X126.271 Y130.091 E.04692
G1 X125.391 Y130.99 E.04046
G1 X125.293 Y131.027 E.00335
G1 X125.189 Y131.023 E.00335
G1 X125.095 Y130.98 E.00334
G1 X125.023 Y130.904 E.00336
G1 X124.987 Y130.807 E.00335
G1 X124.99 Y130.702 E.00335
G1 X125.334 Y129.497 E.04032
G1 X124.532 Y128.485 E.04152
G1 X124.292 Y128.114 E.01421
G1 X124.113 Y127.761 E.01273
G1 X123.639 Y126.56 E.04152
G1 X122.398 Y126.247 E.04116
G1 X122.278 Y126.149 E.00497
G1 X122.234 Y126.026 E.00419
G1 X122.238 Y125.948 E.00251
G1 X122.278 Y125.852 E.00335
G1 X122.398 Y125.753 E.00499
G1 X123.593 Y125.452 E.03963
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.368 J1.606 E.02771
G1 X125.345 Y122.542 E.03555
G1 X124.983 Y121.246 E.04328
G1 X125.011 Y121.119 E.00417
G1 X125.074 Y121.036 E.00334
G1 X125.164 Y120.984 E.00335
G1 X125.268 Y120.97 E.00335
G1 X125.368 Y120.997 E.00334
G1 X125.433 Y121.042 E.00253
G1 X126.332 Y121.971 E.04158
G1 X127.467 Y121.768 E.03709
G3 X128.279 Y121.742 I.535 J4.112 E.02618
G1 X129.728 Y121.909 E.04691
G1 X130.588 Y121.025 E.03964
G1 X130.733 Y120.97 E.00498
G1 X130.81 Y120.977 E.00251
G1 X130.905 Y121.02 E.00335
G1 X130.989 Y121.119 E.00417
G1 X131.015 Y121.272 E.00499
G1 X130.666 Y122.503 E.04116
G1 X131.468 Y123.515 E.04151
G1 X131.708 Y123.886 E.0142
G1 X131.887 Y124.239 E.01274
G1 X132.361 Y125.44 E.04151
G1 X133.577 Y125.745 E.04032
G1 X133.669 Y125.794 E.00335
G1 X133.736 Y125.875 E.00337
G1 X133.766 Y125.974 E.00333
G1 X133.755 Y126.077 E.00335
G1 X133.706 Y126.169 E.00336
G1 X133.626 Y126.235 E.00335
G1 X132.407 Y126.549 E.04046
G1 X132.278 Y126.847 E.01044
G1 X132.579 Y127.177 F30000
G1 F1983
G1 X132.192 Y128.068 E.03123
G3 X131.709 Y128.846 I-4.192 J-2.068 E.0295
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03525
G3 X130.289 Y131.256 I-.659 J.149 E.0552
G1 X129.526 Y130.467 E.03527
G1 X128.609 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.633 E.02949
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.256 E.03299
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03543
G3 X123.742 Y127.929 I3.796 J-2.721 E.02952
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.299 Y125.105 E.03298
G1 X123.807 Y123.933 E.0411
G3 X124.291 Y123.154 I4.192 J2.068 E.02951
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.745 I.659 J-.149 E.05519
G1 X126.473 Y121.532 E.03523
G1 X127.39 Y121.366 E.02996
G3 X128.306 Y121.336 I.61 J4.638 E.02953
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.745 E.03298
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03543
G3 X132.258 Y124.071 I-3.8 J2.723 E.02952
G1 X132.663 Y125.096 E.03543
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.645 I-.2 J.646 E.0552
G1 X132.701 Y126.895 E.03298
G1 X132.603 Y127.122 E.00795
G1 X132.903 Y127.451 F30000
G1 F1983
G1 X132.558 Y128.248 E.02792
G3 X131.557 Y129.653 I-5.528 J-2.878 E.05566
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.02892
G3 X127.668 Y131.071 I-1.445 J-6.043 E.05566
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.739 J-.791 E.08874
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.128 J-2.958 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.316 J-1.035 E.08875
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G3 X124.443 Y122.347 I5.529 J2.878 E.05567
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.055 J-.244 E.08875
G1 X126.614 Y121.093 E.02888
G3 X128.332 Y120.929 I1.447 J6.084 E.05568
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.878 Y120.163 I.743 J.801 E.0303
G3 X131.804 Y121.483 I-.14 J1.083 E.0583
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.131 J2.96 E.03209
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.316 J1.036 E.08875
G1 X132.995 Y127.241 E.02717
G1 X132.927 Y127.396 E.00545
G1 X133.228 Y127.726 F30000
G1 F1983
G1 X132.923 Y128.428 E.0246
G3 X132.008 Y129.751 I-5.48 J-2.814 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.346 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.004 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X124.049 Y131.643 I-1.016 J-1.107 E.08074
G3 X123.799 Y130.425 I1.213 J-.884 E.04122
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.435 J-1.425 E.12218
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.48 J2.814 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12218
G1 X126.756 Y120.653 E.02253
M73 P31 R9
G3 X128.359 Y120.522 I1.301 J6.041 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.911 Y119.757 I1.021 J1.1 E.04122
G3 X132.201 Y121.575 I-.177 J1.492 E.08074
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.435 J1.426 E.12218
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.671 E.00295
G1 X133.552 Y128.001 F30000
G1 F1983
G1 X133.289 Y128.608 E.02129
G3 X132.459 Y129.848 I-5.512 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.0162
G3 X126.883 Y131.8 I-1.15 J-6.066 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03947
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.321 Y119.343 I1.912 J.147 E.09381
G3 X126.547 Y119.852 I-.122 J2.023 E.04349
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07164
G3 X134.554 Y124.422 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01555
G1 X133.576 Y127.946 E.00045
M204 S250
G1 X133.867 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X133.865 Y128.266 E.00006
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.922 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.577 J2.111 E.05794
G3 X125.327 Y118.951 I2.164 J-.8 E.13401
G3 X127.033 Y119.791 I-.089 J2.332 E.05832
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X134.166 Y128.195 I-.369 J2.268 E.18349
G1 X133.925 Y128.252 E.00738
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02358
G1 X133.641 Y128.782 E-.21357
G1 X133.458 Y129.111 E-.14285
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.6 I1.083 J-.556 P1  F30000
G1 X132.153 Y126.567 Z3.6
G1 Z3.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113554
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146815
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.17812
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207447
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.6 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z3.6
G1 Z3.2
G1 E.4 F1800
; LINE_WIDTH: 0.207416
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178093
G1 X129.798 Y122.182 E.00396
; LINE_WIDTH: 0.146796
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113546
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.6 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z3.6
G1 Z3.2
G1 E.4 F1800
; LINE_WIDTH: 0.113575
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146876
G1 X123.795 Y125.649 E.00091
; LINE_WIDTH: 0.17819
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.207551
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.6 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z3.6
G1 Z3.2
G1 E.4 F1800
; LINE_WIDTH: 0.207492
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178144
G1 X126.202 Y129.817 E.00396
; LINE_WIDTH: 0.146833
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113557
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 3.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 17/50
; update layer progress
M73 L17
M991 S0 P16 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z3.6 I1.168 J-.341 P1  F30000
G1 X124.592 Y123.967 Z3.6
G1 Z3.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X124.801 Y123.545 E.01515
M73 P31 R8
G1 X125.984 Y122.507 E.0506
G1 X126.968 Y122.173 E.03343
G1 X127.474 Y122.002 E.01717
G1 X129.044 Y122.105 E.0506
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.566 Y124.021 E.03352
G1 X124.957 Y124.147 F30000
G1 F1983
G1 X125.13 Y123.798 E.01254
G1 X126.191 Y122.867 E.04539
G1 X127.099 Y122.559 E.03083
G1 X127.528 Y122.413 E.01456
G1 X128.936 Y122.506 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.931 Y124.201 E.03092
G1 X125.322 Y124.328 F30000
G1 F1983
G1 X125.459 Y124.05 E.00994
G1 X126.399 Y123.226 E.04018
G1 X127.23 Y122.944 E.02822
G1 X127.582 Y122.825 E.01196
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.296 Y124.381 E.02832
G1 X125.687 Y124.508 F30000
G1 F1983
G1 X125.788 Y124.303 E.00734
G1 X126.606 Y123.586 E.03498
G1 X127.361 Y123.33 E.02562
G1 X127.636 Y123.236 E.00936
G1 X128.722 Y123.307 E.03498
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.279 E.03498
G1 X125.661 Y124.561 E.02571
G1 X126.053 Y124.688 F30000
G1 F1983
G1 X126.118 Y124.556 E.00473
G1 X126.814 Y123.945 E.02977
G1 X127.491 Y123.715 E.02302
G1 X127.69 Y123.648 E.00675
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.026 Y124.741 E.02311
M204 S250
G1 X126.404 Y124.861 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X126.435 Y124.799 E.00206
G1 X127.014 Y124.291 E.02293
G1 X127.617 Y124.086 E.019
G1 X127.742 Y124.044 E.00393
M73 P32 R8
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.378 Y124.915 E.01908
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.04909
G1 X127.014 Y124.291 E-.29252
G1 X127.109 Y124.259 E-.03839
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.8 I-.556 J1.083 P1  F30000
G1 X132.254 Y126.901 Z3.8
G1 Z3.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1983
G1 X131.827 Y127.887 E.03456
G3 X131.37 Y128.615 I-3.358 J-1.599 E.0277
G1 X130.655 Y129.458 E.03555
G1 X131.015 Y130.728 E.04245
G1 X130.989 Y130.881 E.00499
G1 X130.883 Y130.994 E.00499
G1 X130.732 Y131.03 E.00498
G1 X130.588 Y130.975 E.00498
G1 X129.668 Y130.028 E.04245
G1 X128.534 Y130.232 E.03705
G3 X127.721 Y130.258 I-.536 J-4.115 E.0262
G1 X126.271 Y130.091 E.04692
G1 X125.412 Y130.975 E.03963
G1 X125.267 Y131.03 E.00498
G1 X125.164 Y131.016 E.00335
G1 X125.094 Y130.98 E.00252
G1 X125 Y130.857 E.00499
G1 X124.985 Y130.728 E.00417
G1 X125.334 Y129.497 E.04116
G1 X124.532 Y128.485 E.04152
G1 X124.292 Y128.114 E.01421
G1 X124.113 Y127.761 E.01273
G1 X123.639 Y126.56 E.04152
G1 X122.422 Y126.255 E.04033
G1 X122.331 Y126.206 E.00334
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00335
G1 X122.245 Y125.923 E.00334
G1 X122.294 Y125.831 E.00335
G1 X122.374 Y125.765 E.00334
G1 X123.593 Y125.451 E.04046
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.359 J1.6 E.0277
G1 X125.345 Y122.542 E.03555
G1 X124.985 Y121.272 E.04245
G1 X125.01 Y121.119 E.00497
G1 X125.117 Y121.006 E.005
G1 X125.268 Y120.97 E.00498
G1 X125.413 Y121.025 E.00499
G1 X126.332 Y121.971 E.04242
G1 X127.467 Y121.768 E.03708
G3 X128.279 Y121.742 I.535 J4.111 E.02618
G1 X129.728 Y121.909 E.04691
G1 X130.567 Y121.042 E.03879
G1 X130.656 Y120.987 E.00336
G1 X130.785 Y120.972 E.00415
G1 X130.86 Y120.994 E.00253
G1 X130.945 Y121.054 E.00335
G1 X131 Y121.143 E.00334
G1 X131.017 Y121.246 E.00335
G1 X130.666 Y122.503 E.04199
G1 X131.468 Y123.515 E.04152
G1 X131.708 Y123.886 E.01421
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04151
G1 X133.602 Y125.753 E.04117
G1 X133.706 Y125.831 E.00417
G1 X133.762 Y125.948 E.00417
G1 X133.762 Y126.052 E.00335
G1 X133.735 Y126.126 E.00252
G1 X133.689 Y126.189 E.00251
G1 X133.602 Y126.247 E.00335
G1 X132.407 Y126.549 E.03963
G1 X132.278 Y126.846 E.01043
G1 X132.999 Y126.82 F30000
G1 F1983
G1 X132.701 Y126.895 E.00987
G1 X132.192 Y128.068 E.04111
G3 X131.709 Y128.846 I-4.192 J-2.067 E.0295
G1 X131.106 Y129.556 E.02995
G1 X131.407 Y130.61 E.03526
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.527 Y130.468 E.03525
G1 X128.61 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.636 E.02951
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.255 E.03297
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03543
G3 X123.742 Y127.929 I3.796 J-2.721 E.02952
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.645 E.03424
G3 X122.304 Y125.354 I.2 J-.645 E.0552
G1 X123.299 Y125.105 E.03297
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.155 I4.194 J2.069 E.0295
G1 X124.894 Y122.444 E.02996
G1 X124.593 Y121.39 E.03525
G3 X125.711 Y120.745 I.659 J-.149 E.0552
G1 X126.473 Y121.532 E.03524
G1 X127.39 Y121.366 E.02995
G3 X128.306 Y121.336 I.61 J4.637 E.02952
G1 X129.576 Y121.482 E.0411
G1 X130.289 Y120.745 E.03298
G3 X130.838 Y120.568 I.464 J.5 E.01914
G3 X131.407 Y121.39 I-.09 J.67 E.03618
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.798 J2.722 E.02952
G1 X132.663 Y125.096 E.03543
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.645 I-.2 J.645 E.0552
G1 X133.057 Y126.806 E.02118
G1 X132.903 Y127.451 F30000
G1 F1983
G1 X132.558 Y128.248 E.02792
G3 X131.557 Y129.653 I-5.527 J-2.878 E.05566
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.055 J.244 E.08875
G1 X129.385 Y130.907 E.0289
G3 X127.668 Y131.071 I-1.446 J-6.063 E.05567
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02716
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.128 J-2.958 E.03209
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.964 I.316 J-1.035 E.08875
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.532 J2.881 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.99 Y120.447 I1.055 J-.244 E.08875
G1 X126.614 Y121.093 E.02889
G3 X128.332 Y120.929 I1.446 J6.079 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.872 Y120.162 I.742 J.799 E.03011
G3 X131.804 Y121.483 I-.122 J1.075 E.05866
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.131 J2.96 E.03209
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.316 J1.035 E.08875
G1 X132.995 Y127.241 E.02717
G1 X132.927 Y127.396 E.00544
G1 X133.228 Y127.726 F30000
G1 F1983
G1 X132.923 Y128.428 E.02461
G3 X132.008 Y129.751 I-5.48 J-2.814 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.452 J.336 E.12218
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.022 E.05188
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02135
G3 X123.799 Y130.425 I-1.013 J-1.096 E.1219
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.435 J-1.425 E.12218
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.484 J2.817 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.906 Y119.757 I1.021 J1.099 E.04104
G3 X132.201 Y121.575 I-.156 J1.481 E.08115
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.435 J1.425 E.12217
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.671 E.00294
G1 X133.552 Y128.001 F30000
G1 F1983
G1 X133.289 Y128.608 E.0213
G3 X132.459 Y129.848 I-5.512 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07178
G3 X125.918 Y132.539 I-1.955 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.874 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.742 J-1.021 E.03412
G3 X125.316 Y119.343 I1.912 J.147 E.09364
G3 X126.547 Y119.852 I-.115 J2.021 E.04366
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.07 J1.575 E.13732
G1 X133.582 Y127.933 E.01555
G1 X133.576 Y127.946 E.00045
M204 S250
G1 X133.867 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1983
M204 S5000
G1 X133.865 Y128.266 E.00008
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19276
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
M73 P33 R8
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.322 Y118.951 I2.164 J-.8 E.13385
G3 X127.033 Y119.791 I-.083 J2.332 E.05848
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X134.166 Y128.195 I-.369 J2.268 E.18349
G1 X133.926 Y128.252 E.00736
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02378
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.11 E-.14265
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.8 I1.083 J-.556 P1  F30000
G1 X132.153 Y126.567 Z3.8
G1 Z3.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113554
G1 F1983
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146815
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178105
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.207442
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.8 I1.096 J-.529 P1  F30000
G1 X130.538 Y122.208 Z3.8
G1 Z3.4
G1 E.4 F1800
; LINE_WIDTH: 0.207405
G1 F1983
G1 X130.168 Y122.195 E.00481
; LINE_WIDTH: 0.178075
G1 X129.798 Y122.182 E.00395
; LINE_WIDTH: 0.146799
G1 X129.692 Y122.151 E.00091
; LINE_WIDTH: 0.113546
G1 X129.586 Y122.12 E.00062
; WIPE_START
G1 F15000
G1 X129.692 Y122.151 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.8 I-.596 J-1.061 P1  F30000
G1 X123.847 Y125.433 Z3.8
G1 Z3.4
G1 E.4 F1800
; LINE_WIDTH: 0.113559
G1 F1983
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146828
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.17812
G1 X123.621 Y125.975 E.00395
; LINE_WIDTH: 0.20746
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z3.8 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z3.8
G1 Z3.4
G1 E.4 F1800
; LINE_WIDTH: 0.207515
G1 F1983
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178165
G1 X126.202 Y129.817 E.00396
; LINE_WIDTH: 0.146845
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113562
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 3.6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 18/50
; update layer progress
M73 L18
M991 S0 P17 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z3.8 I1.168 J-.342 P1  F30000
G1 X124.589 Y123.974 Z3.8
G1 Z3.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1987
G1 X124.801 Y123.545 E.01538
G1 X125.984 Y122.507 E.0506
G1 X127.002 Y122.162 E.0346
G1 X127.474 Y122.002 E.01601
G1 X129.044 Y122.105 E.05059
G1 X130.455 Y122.801 E.0506
G1 X131.493 Y123.984 E.0506
G1 X131.998 Y125.474 E.0506
G1 X131.895 Y127.044 E.0506
G1 X131.199 Y128.455 E.0506
G1 X130.016 Y129.493 E.0506
G1 X128.526 Y129.998 E.0506
G1 X126.956 Y129.895 E.0506
G1 X125.545 Y129.199 E.0506
G1 X124.507 Y128.016 E.0506
G1 X124.002 Y126.526 E.0506
G1 X124.105 Y124.956 E.0506
G1 X124.562 Y124.028 E.03329
G1 X124.954 Y124.154 F30000
G1 F1987
G1 X125.13 Y123.798 E.01278
G1 X126.191 Y122.867 E.04539
G1 X127.133 Y122.547 E.03199
G1 X127.528 Y122.413 E.0134
G1 X128.936 Y122.505 E.04539
G1 X130.202 Y123.13 E.04539
G1 X131.133 Y124.191 E.04539
G1 X131.587 Y125.528 E.04539
G1 X131.495 Y126.936 E.04539
G1 X130.87 Y128.202 E.04539
G1 X129.809 Y129.133 E.04539
G1 X128.472 Y129.587 E.04539
G1 X127.064 Y129.495 E.04539
G1 X125.798 Y128.87 E.04539
G1 X124.867 Y127.809 E.04539
G1 X124.413 Y126.472 E.04539
G1 X124.505 Y125.064 E.04539
G1 X124.928 Y124.208 E.03068
G1 X125.319 Y124.334 F30000
G1 F1987
G1 X125.459 Y124.05 E.01018
G1 X126.399 Y123.226 E.04018
G1 X127.264 Y122.933 E.02939
G1 X127.582 Y122.825 E.0108
G1 X128.829 Y122.906 E.04018
G1 X129.95 Y123.459 E.04019
G1 X130.774 Y124.399 E.04018
G1 X131.175 Y125.582 E.04018
G1 X131.094 Y126.829 E.04018
G1 X130.541 Y127.95 E.04019
G1 X129.601 Y128.774 E.04018
G1 X128.418 Y129.175 E.04018
G1 X127.171 Y129.094 E.04019
G1 X126.05 Y128.541 E.04018
G1 X125.226 Y127.601 E.04018
G1 X124.825 Y126.418 E.04018
G1 X124.906 Y125.171 E.04018
G1 X125.293 Y124.388 E.02808
G1 X125.684 Y124.514 F30000
G1 F1987
G1 X125.788 Y124.303 E.00757
G1 X126.606 Y123.586 E.03498
G1 X127.395 Y123.318 E.02678
G1 X127.636 Y123.236 E.0082
G1 X128.722 Y123.307 E.03497
G1 X129.697 Y123.788 E.03498
G1 X130.414 Y124.606 E.03498
G1 X130.764 Y125.636 E.03498
G1 X130.693 Y126.722 E.03498
G1 X130.212 Y127.697 E.03498
G1 X129.394 Y128.414 E.03498
G1 X128.364 Y128.764 E.03498
G1 X127.278 Y128.693 E.03498
G1 X126.303 Y128.212 E.03498
G1 X125.586 Y127.394 E.03498
G1 X125.236 Y126.364 E.03498
G1 X125.307 Y125.278 E.03498
G1 X125.658 Y124.568 E.02547
G1 X126.049 Y124.694 F30000
G1 F1987
G1 X126.118 Y124.556 E.00497
G1 X126.814 Y123.945 E.02977
G1 X127.526 Y123.704 E.02418
G1 X127.69 Y123.648 E.00559
G1 X128.614 Y123.708 E.02977
G1 X129.444 Y124.118 E.02977
G1 X130.055 Y124.814 E.02977
G1 X130.352 Y125.69 E.02977
G1 X130.292 Y126.614 E.02977
G1 X129.882 Y127.444 E.02977
G1 X129.186 Y128.055 E.02977
G1 X128.31 Y128.352 E.02977
G1 X127.386 Y128.292 E.02977
G1 X126.556 Y127.882 E.02977
G1 X125.945 Y127.186 E.02977
G1 X125.648 Y126.31 E.02977
G1 X125.708 Y125.386 E.02977
G1 X126.023 Y124.748 E.02287
M204 S250
G1 X126.401 Y124.868 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1987
M204 S5000
G1 X126.435 Y124.799 E.00228
G1 X127.014 Y124.291 E.02293
G1 X127.652 Y124.075 E.02007
G1 X127.742 Y124.044 E.00286
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.374 Y124.921 E.01886
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.05189
G1 X127.014 Y124.291 E-.29252
G1 X127.102 Y124.261 E-.0356
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4 I-.555 J1.083 P1  F30000
G1 X132.254 Y126.901 Z4
G1 Z3.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1987
G1 X131.827 Y127.887 E.03457
G3 X131.37 Y128.616 I-3.333 J-1.584 E.02771
G1 X130.655 Y129.458 E.03554
G1 X131.015 Y130.728 E.04245
G1 X130.989 Y130.881 E.00498
G1 X130.883 Y130.994 E.00499
G1 X130.732 Y131.03 E.00499
G1 X130.587 Y130.975 E.00499
G1 X129.667 Y130.028 E.04246
G1 X128.534 Y130.232 E.03701
G3 X127.721 Y130.258 I-.536 J-4.12 E.02622
G1 X126.271 Y130.091 E.04692
G1 X125.413 Y130.975 E.03963
G1 X125.267 Y131.03 E.00499
G1 X125.189 Y131.023 E.00252
G1 X125.095 Y130.98 E.00334
G1 X125.011 Y130.881 E.00418
G1 X124.985 Y130.728 E.00499
G1 X125.334 Y129.497 E.04116
G1 X124.532 Y128.485 E.04152
G1 X124.292 Y128.114 E.0142
G1 X124.113 Y127.761 E.01273
G1 X123.639 Y126.56 E.04152
G1 X122.423 Y126.256 E.04031
G1 X122.331 Y126.206 E.00335
G1 X122.265 Y126.126 E.00335
G1 X122.234 Y126.026 E.00336
G1 X122.244 Y125.923 E.00334
G1 X122.294 Y125.831 E.00336
G1 X122.374 Y125.765 E.00335
G1 X123.593 Y125.451 E.04046
G1 X124.173 Y124.113 E.04692
G3 X124.63 Y123.385 I3.352 J1.596 E.0277
G1 X125.345 Y122.542 E.03554
G1 X124.985 Y121.272 E.04245
G1 X125.011 Y121.119 E.00499
G1 X125.116 Y121.006 E.00498
G1 X125.268 Y120.971 E.00499
G1 X125.412 Y121.025 E.00498
G1 X126.332 Y121.972 E.04245
G1 X127.467 Y121.768 E.03707
G3 X128.279 Y121.742 I.535 J4.112 E.02617
G1 X129.729 Y121.909 E.04691
G1 X130.568 Y121.042 E.0388
G1 X130.656 Y120.987 E.00335
G1 X130.785 Y120.972 E.00417
G1 X130.883 Y121.006 E.00335
G1 X130.945 Y121.054 E.00252
G1 X131 Y121.143 E.00335
G1 X131.017 Y121.246 E.00335
G1 X130.666 Y122.503 E.04199
G1 X131.468 Y123.515 E.04151
G1 X131.708 Y123.886 E.01421
G1 X131.887 Y124.239 E.01273
G1 X132.361 Y125.44 E.04151
G1 X133.602 Y125.753 E.04116
G1 X133.706 Y125.831 E.00417
G1 X133.762 Y125.948 E.00417
G1 X133.762 Y126.052 E.00334
G1 X133.735 Y126.126 E.00253
G1 X133.689 Y126.189 E.00252
G1 X133.602 Y126.247 E.00334
G1 X132.407 Y126.549 E.03963
G1 X132.278 Y126.846 E.01042
G1 X132.579 Y127.176 F30000
G1 F1987
G1 X132.192 Y128.068 E.03124
G3 X131.709 Y128.845 I-4.192 J-2.067 E.0295
G1 X131.106 Y129.555 E.02995
G1 X131.407 Y130.61 E.03527
G3 X130.289 Y131.256 I-.659 J.149 E.05518
G1 X129.526 Y130.467 E.03528
G1 X128.61 Y130.635 E.02996
G3 X127.694 Y130.665 I-.61 J-4.633 E.02949
G1 X126.424 Y130.518 E.04111
G1 X125.711 Y131.256 E.03299
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.885 Y129.586 E.03424
G1 X124.2 Y128.723 E.03544
G3 X123.742 Y127.929 I3.798 J-2.721 E.02951
G1 X123.337 Y126.904 E.03544
G1 X122.304 Y126.646 E.03423
G3 X122.304 Y125.354 I.2 J-.646 E.05521
G1 X123.299 Y125.105 E.03298
G1 X123.808 Y123.932 E.04111
G3 X124.291 Y123.154 I4.192 J2.068 E.0295
G1 X124.894 Y122.444 E.02995
G1 X124.593 Y121.39 E.03526
G3 X125.711 Y120.745 I.659 J-.149 E.05519
G1 X126.474 Y121.532 E.03525
G1 X127.39 Y121.365 E.02996
G3 X128.306 Y121.336 I.61 J4.636 E.02951
G1 X129.576 Y121.482 E.0411
M73 P34 R8
G1 X130.289 Y120.745 E.03298
G3 X130.838 Y120.568 I.464 J.5 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.115 Y122.414 E.03424
G1 X131.8 Y123.277 E.03544
G3 X132.258 Y124.071 I-3.799 J2.722 E.02952
G1 X132.663 Y125.096 E.03543
G1 X133.696 Y125.355 E.03424
G3 X133.696 Y126.645 I-.2 J.645 E.05519
G1 X132.701 Y126.895 E.03298
G1 X132.603 Y127.121 E.00793
G1 X132.903 Y127.451 F30000
G1 F1987
G1 X132.558 Y128.248 E.02793
G3 X131.557 Y129.653 I-5.52 J-2.873 E.05566
G1 X131.804 Y130.518 E.02891
G3 X130.01 Y131.553 I-1.058 J.239 E.08853
G1 X129.385 Y130.907 E.02892
G3 X127.668 Y131.071 I-1.445 J-6.043 E.05566
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.739 J-.791 E.08874
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G3 X123.371 Y128.097 I4.13 J-2.96 E.03209
G1 X123.035 Y127.248 E.02935
G1 X122.186 Y127.036 E.02815
G3 X122.186 Y124.964 I.316 J-1.036 E.08876
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G3 X124.443 Y122.347 I5.529 J2.879 E.05566
G1 X124.196 Y121.483 E.0289
G3 X125.297 Y120.157 I1.055 J-.244 E.06409
G3 X125.99 Y120.447 I-.078 J1.156 E.02459
G1 X126.615 Y121.093 E.0289
G3 X128.332 Y120.929 I1.446 J6.062 E.05567
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X131.804 Y121.483 I.739 J.791 E.08875
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G3 X132.629 Y123.903 I-4.132 J2.961 E.0321
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.035 I-.316 J1.035 E.08875
G1 X132.995 Y127.241 E.02717
G1 X132.927 Y127.396 E.00544
G1 X133.228 Y127.726 F30000
G1 F1987
G1 X132.923 Y128.428 E.02462
G3 X132.008 Y129.751 I-5.473 J-2.81 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12188
G1 X129.244 Y131.346 E.02256
G3 X127.641 Y131.478 I-1.3 J-6.004 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12218
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02207
G3 X122.068 Y124.574 I.435 J-1.426 E.12218
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.481 J2.815 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.021 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.901 Y119.756 I1.02 J1.099 E.04088
G3 X132.201 Y121.575 I-.166 J1.492 E.08108
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.56 J4.081 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.435 J1.426 E.12218
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.671 E.00294
G1 X133.553 Y128.001 F30000
G1 F1987
G1 X133.289 Y128.608 E.0213
G3 X132.459 Y129.848 I-5.51 J-2.79 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.0162
G3 X126.883 Y131.8 I-1.15 J-6.067 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03947
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13732
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.31 Y119.343 I1.912 J.147 E.09347
G3 X126.547 Y119.852 I-.109 J2.02 E.04383
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.071 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.78 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03393
G3 X134.051 Y127.816 I-1.07 J1.575 E.13732
G1 X133.582 Y127.933 E.01555
G1 X133.576 Y127.945 E.00044
M204 S250
G1 X133.868 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1987
M204 S5000
G1 X133.865 Y128.266 E.00009
G3 X132.894 Y129.942 I-5.577 J-2.111 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.317 Y118.951 I2.164 J-.8 E.13369
G3 X127.033 Y119.791 I-.077 J2.331 E.05864
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X134.166 Y128.195 I-.369 J2.268 E.18349
G1 X133.926 Y128.252 E.00734
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02396
G1 X133.641 Y128.782 E-.21356
G1 X133.459 Y129.11 E-.14248
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4 I1.083 J-.556 P1  F30000
G1 X132.153 Y126.567 Z4
G1 Z3.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.113559
G1 F1987
G1 X132.179 Y126.459 E.00062
; LINE_WIDTH: 0.146828
G1 X132.205 Y126.352 E.00091
; LINE_WIDTH: 0.178121
G1 X132.379 Y126.025 E.00396
; LINE_WIDTH: 0.20746
G1 X132.553 Y125.698 E.00481
; WIPE_START
G1 F15000
G1 X132.379 Y126.025 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4 I.99 J-.708 P1  F30000
G1 X129.586 Y122.12 Z4
G1 Z3.6
G1 E.4 F1800
; LINE_WIDTH: 0.113548
G1 F1987
G1 X129.692 Y122.151 E.00062
; LINE_WIDTH: 0.146801
G1 X129.798 Y122.182 E.00091
; LINE_WIDTH: 0.178096
G1 X130.168 Y122.195 E.00396
; LINE_WIDTH: 0.207425
G1 X130.538 Y122.208 E.00481
G1 X130.694 Y121.663 F30000
; LINE_WIDTH: 0.163098
G1 F1987
G1 X130.771 Y121.178 E.00466
; WIPE_START
G1 F15000
G1 X130.694 Y121.663 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4 I-.587 J-1.066 P1  F30000
G1 X123.847 Y125.433 Z4
G1 Z3.6
G1 E.4 F1800
; LINE_WIDTH: 0.113559
G1 F1987
G1 X123.821 Y125.541 E.00062
; LINE_WIDTH: 0.146829
G1 X123.795 Y125.648 E.00091
; LINE_WIDTH: 0.178122
G1 X123.621 Y125.975 E.00396
; LINE_WIDTH: 0.207461
G1 X123.447 Y126.302 E.00481
; WIPE_START
G1 F15000
G1 X123.621 Y125.975 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4 I-1.096 J.529 P1  F30000
G1 X125.462 Y129.792 Z4
G1 Z3.6
G1 E.4 F1800
; LINE_WIDTH: 0.207479
G1 F1987
G1 X125.832 Y129.805 E.00481
; LINE_WIDTH: 0.178127
G1 X126.202 Y129.817 E.00395
; LINE_WIDTH: 0.146832
G1 X126.308 Y129.849 E.00091
; LINE_WIDTH: 0.113556
G1 X126.414 Y129.88 E.00062
; CHANGE_LAYER
; Z_HEIGHT: 3.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X126.308 Y129.849 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 19/50
; update layer progress
M73 L19
M991 S0 P18 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z4 I1.217 J.022 P1  F30000
G1 X126.398 Y124.874 Z4
G1 Z3.8
G1 E.4 F1800
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F2428
M204 S5000
G1 X126.435 Y124.799 E.00249
G1 X127.014 Y124.291 E.02293
G1 X127.686 Y124.063 E.02115
G1 X127.743 Y124.044 E.00178
G1 X128.511 Y124.094 E.02293
G1 X129.201 Y124.435 E.02293
G1 X129.709 Y125.014 E.02293
G1 X129.956 Y125.742 E.02293
G1 X129.906 Y126.511 E.02293
G1 X129.565 Y127.201 E.02293
G1 X128.986 Y127.709 E.02293
G1 X128.258 Y127.956 E.02293
G1 X127.489 Y127.906 E.02293
G1 X126.799 Y127.565 E.02293
G1 X126.291 Y126.986 E.02293
G1 X126.044 Y126.258 E.02293
G1 X126.094 Y125.489 E.02293
G1 X126.371 Y124.928 E.01865
; WIPE_START
G1 F11933.819
M204 S10000
G1 X126.435 Y124.799 E-.05459
G1 X127.014 Y124.291 E-.29253
G1 X127.096 Y124.264 E-.03289
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I1.112 J-.495 P1  F30000
G1 X125.346 Y120.336 Z4.2
G1 Z3.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F2428
G1 X124.422 Y120.869 E.0343
G1 X124.29 Y120.726 E.00628
G3 X125.287 Y120.149 I1 J.58 E.03879
G1 X125.328 Y120.279 E.00436
; WIPE_START
M73 P35 R8
G1 F11054.348
G1 X124.49 Y120.825 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I.374 J1.158 P1  F30000
G1 X126.355 Y120.223 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X123.82 Y121.687 E.09414
G3 X125.298 Y119.75 I1.437 J-.437 E.09144
G3 X126.312 Y120.182 I-.096 J1.629 E.03614
G1 X127 Y120.321 F30000
G1 F2428
G1 X123.581 Y122.295 E.12695
G1 X123.402 Y121.668 E.02097
G3 X125.305 Y119.343 I1.849 J-.428 E.11147
G3 X126.547 Y119.852 I-.103 J2.018 E.044
G1 X126.959 Y120.278 E.01904
; WIPE_START
G1 F11054.348
G1 X126.1 Y120.79 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.018 J1.217 P1  F30000
G1 X131.578 Y120.869 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X130.654 Y120.336 E.0343
G1 X130.713 Y120.149 E.00629
G1 X130.862 Y120.162 E.00483
G3 X131.711 Y120.726 I-.124 J1.106 E.03403
G1 X131.619 Y120.825 E.00436
; WIPE_START
G1 F11054.348
G1 X130.727 Y120.373 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.816 J.903 P1  F30000
G1 X132.18 Y121.687 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X129.645 Y120.223 E.09414
G3 X130.895 Y119.756 I1.111 J1.067 E.0444
G3 X132.197 Y121.63 I-.152 J1.494 E.0833
G1 X132.419 Y122.295 F30000
G1 F2428
G1 X129 Y120.321 E.12695
G1 X129.453 Y119.852 E.02097
G3 X130.929 Y119.35 I1.299 J1.398 E.05163
G3 X132.598 Y121.668 I-.179 J1.888 E.10397
G1 X132.435 Y122.237 E.01904
; WIPE_START
G1 F11054.348
G1 X131.562 Y121.75 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-1.063 J.593 P1  F30000
G1 X134.232 Y126.533 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X134.232 Y125.467 E.0343
G1 X134.423 Y125.424 E.00628
G1 X134.5 Y125.586 E.00577
G3 X134.423 Y126.576 I-1.038 J.418 E.03309
G1 X134.291 Y126.546 E.00436
; WIPE_START
G1 F11054.348
G1 X134.237 Y125.548 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-1.19 J-.256 P1  F30000
G1 X133.825 Y127.464 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X133.825 Y124.536 E.09414
G1 X134.07 Y124.624 E.00837
G3 X133.883 Y127.449 I-.58 J1.381 E.11933
G1 X133.653 Y127.915 F30000
G1 F2428
G1 X133.418 Y127.974 E.00778
G1 X133.418 Y124.026 E.12695
G1 X134.051 Y124.184 E.02096
G3 X134.051 Y127.816 I-.553 J1.816 E.15565
G1 X133.711 Y127.901 E.01125
; WIPE_START
G1 F11054.348
G1 X133.418 Y127.974 E-.11478
G1 X133.418 Y127.276 E-.26522
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-1.098 J-.524 P1  F30000
G1 X131.578 Y131.131 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X131.711 Y131.274 E.00629
G3 X130.713 Y131.851 I-1 J-.58 E.03879
G1 X130.654 Y131.664 E.00629
G1 X131.526 Y131.161 E.03237
; WIPE_START
G1 F11054.348
G1 X131.711 Y131.274 E-.08233
G1 X131.54 Y131.503 E-.10837
G1 X131.291 Y131.7 E-.12067
G1 X131.123 Y131.767 E-.06863
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I.984 J.716 P1  F30000
G1 X132.18 Y130.313 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X132.227 Y130.569 E.00836
G3 X129.645 Y131.777 I-1.486 J.188 E.12126
G1 X132.128 Y130.343 E.09221
G1 X132.419 Y129.705 F30000
G1 F2428
G1 X132.598 Y130.332 E.02097
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X129.453 Y132.148 I-1.854 J.42 E.15524
G1 X129 Y131.679 E.02097
G1 X132.367 Y129.735 E.12502
; WIPE_START
G1 F11054.348
G1 X132.598 Y130.332 E-.24327
G1 X132.631 Y130.516 E-.07074
G1 X132.637 Y130.689 E-.06599
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.139 J-1.209 P1  F30000
G1 X125.151 Y131.552 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X125.346 Y131.664 E.00721
G1 X125.287 Y131.851 E.00629
G3 X124.289 Y131.274 I-.012 J-1.132 E.03888
G1 X124.422 Y131.131 E.00629
G1 X125.099 Y131.522 E.02516
G1 X125.847 Y131.483 F30000
G1 F2428
G1 X126.355 Y131.777 E.01888
G3 X123.82 Y130.313 I-1.098 J-1.027 E.12975
G1 X125.795 Y131.453 E.07334
G1 X126.398 Y131.331 F30000
G1 F2428
G1 X127 Y131.679 E.02237
G1 X126.547 Y132.148 E.02097
G3 X123.402 Y130.332 I-1.295 J-1.387 E.1556
G1 X123.581 Y129.705 E.02097
G1 X126.346 Y131.301 E.10264
; WIPE_START
G1 F11054.348
G1 X127 Y131.679 E-.2872
G1 X126.83 Y131.855 E-.0928
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I.954 J-.756 P1  F30000
G1 X121.768 Y125.467 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X121.768 Y126.533 E.0343
G1 X121.577 Y126.576 E.00629
G3 X121.577 Y125.424 I1.002 J-.576 E.03879
G1 X121.709 Y125.454 E.00436
; WIPE_START
G1 F11054.348
G1 X121.763 Y126.452 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I1.19 J.256 P1  F30000
G1 X122.175 Y124.536 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
G1 X122.175 Y127.464 E.09414
G3 X122.117 Y124.551 I.347 J-1.464 E.12752
G1 X122.582 Y124.026 F30000
G1 F2428
G1 X122.582 Y127.974 E.12695
G1 X121.949 Y127.816 E.02097
G3 X121.949 Y124.184 I.564 J-1.816 E.15524
G1 X122.524 Y124.041 E.01904
; WIPE_START
G1 F11054.348
G1 X122.538 Y125.041 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.333 J1.17 P1  F30000
G1 X133.868 Y128.265 Z4.2
G1 Z3.8
G1 E.4 F1800
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F2428
M204 S5000
G1 X133.865 Y128.266 E.0001
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19233
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05348
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.311 Y118.951 I2.164 J-.8 E.13353
G3 X127.033 Y119.791 I-.072 J2.331 E.0588
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.195 I-.368 J2.268 E.18354
G1 X133.926 Y128.252 E.00733
M204 S10000
G1 X133.566 Y128.462 F30000
; FEATURE: Gap infill
; LINE_WIDTH: 0.103897
G1 F2428
G1 X132.969 Y129.514 E.00582
; WIPE_START
G1 F15000
G1 X133.463 Y128.644 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.696 J-.999 P1  F30000
G1 X128.558 Y132.061 Z4.2
G1 Z3.8
G1 E.4 F1800
; LINE_WIDTH: 0.103882
G1 F2428
G1 X127.349 Y132.051 E.00582
; WIPE_START
G1 F15000
G1 X128.348 Y132.059 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I.536 J-1.093 P1  F30000
G1 X123.398 Y129.632 Z4.2
G1 Z3.8
G1 E.4 F1800
; LINE_WIDTH: 0.400228
G1 F2428
G1 X122.727 Y129.052 E.02504
G1 X122.72 Y129.041 F30000
; LINE_WIDTH: 0.400262
G1 F2428
G1 X122.554 Y128.169 E.02504
; WIPE_START
G1 F12592.993
G1 X122.72 Y129.041 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I1.215 J-.063 P1  F30000
G1 X122.434 Y123.537 Z4.2
G1 Z3.8
G1 E.4 F1800
; LINE_WIDTH: 0.103874
G1 F2428
G1 X123.031 Y122.485 E.00582
; WIPE_START
G1 F15000
G1 X122.538 Y123.355 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I.695 J.999 P1  F30000
G1 X127.442 Y119.939 Z4.2
G1 Z3.8
G1 E.4 F1800
; LINE_WIDTH: 0.103906
G1 F2428
G1 X128.018 Y119.945 E.00277
; WIPE_START
G1 F15000
G1 X127.442 Y119.939 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.453 J1.129 P1  F30000
G1 X128.922 Y120.533 Z4.2
G1 Z3.8
G1 E.4 F1800
; FEATURE: Top surface
; LINE_WIDTH: 0.42
G1 F2428
M204 S2000
G1 X127.078 Y120.533 E.0549
G1 X126.425 Y120.91
G1 X129.575 Y120.91 E.09381
G1 X130.228 Y121.287
G1 X125.772 Y121.287 E.13271
G1 X125.119 Y121.664
G1 X130.881 Y121.664 E.17162
G1 X131.534 Y122.041
M73 P36 R8
G1 X124.466 Y122.041 E.21053
G1 X123.813 Y122.418
G1 X132.187 Y122.418 E.24944
G1 X132.84 Y122.795
G1 X123.16 Y122.795 E.28834
G1 X122.804 Y123.172
G1 X133.196 Y123.172 E.30953
G1 X133.196 Y123.549
G1 X122.804 Y123.549 E.30953
G1 X122.804 Y123.926
G1 X127.444 Y123.926 E.13821
G1 X126.686 Y124.303
G1 X122.804 Y124.303 E.11561
G1 X122.804 Y124.68
G1 X126.262 Y124.68 E.103
G1 X126.076 Y125.057
G1 X122.804 Y125.057 E.09746
G1 X122.804 Y125.434
G1 X125.89 Y125.434 E.09192
G1 X125.865 Y125.812
G1 X122.804 Y125.812 E.09118
G1 X122.804 Y126.189
G1 X125.841 Y126.189 E.09044
G1 X125.93 Y126.566
G1 X122.804 Y126.566 E.09309
G1 X122.804 Y126.943
G1 X126.058 Y126.943 E.0969
G1 X126.308 Y127.32
G1 X122.804 Y127.32 E.10436
G1 X122.804 Y127.697
G1 X126.639 Y127.697 E.11421
G1 X127.362 Y128.074
G1 X122.804 Y128.074 E.13575
; WIPE_START
G1 F11933.819
M204 S10000
G1 X123.804 Y128.074 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I.792 J.924 P1  F30000
G1 X128.639 Y123.926 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
M204 S2000
G1 X133.196 Y123.926 E.13574
G1 X133.196 Y124.303
G1 X129.361 Y124.303 E.11421
G1 X129.692 Y124.68
G1 X133.196 Y124.68 E.10436
G1 X133.196 Y125.057
G1 X129.942 Y125.057 E.0969
G1 X130.07 Y125.434
G1 X133.196 Y125.434 E.09309
G1 X133.196 Y125.812
G1 X130.159 Y125.812 E.09044
G1 X130.135 Y126.189
G1 X133.196 Y126.189 E.09118
G1 X133.196 Y126.566
G1 X130.11 Y126.566 E.09192
G1 X129.924 Y126.943
G1 X133.196 Y126.943 E.09746
G1 X133.196 Y127.32
G1 X129.738 Y127.32 E.103
G1 X129.314 Y127.697
G1 X133.196 Y127.697 E.11561
G1 X133.196 Y128.074
G1 X128.555 Y128.074 E.13822
; WIPE_START
G1 F11933.819
M204 S10000
G1 X129.555 Y128.074 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.125 J1.21 P1  F30000
G1 X133.196 Y128.451 Z4.2
G1 Z3.8
G1 E.4 F1800
G1 F2428
M204 S2000
G1 X122.804 Y128.451 E.30953
G1 X122.804 Y128.828
G1 X133.196 Y128.828 E.30953
G1 X132.84 Y129.205
G1 X123.16 Y129.205 E.28833
G1 X123.813 Y129.582
G1 X132.187 Y129.582 E.24943
G1 X131.534 Y129.959
G1 X124.466 Y129.959 E.21052
G1 X125.119 Y130.336
G1 X130.881 Y130.336 E.17161
G1 X130.228 Y130.713
G1 X125.772 Y130.713 E.1327
G1 X126.426 Y131.091
G1 X129.574 Y131.091 E.0938
G1 X128.921 Y131.468
G1 X127.079 Y131.468 E.05489
; WIPE_START
G1 F11933.819
M204 S10000
G1 X128.079 Y131.468 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I1.214 J.09 P1  F30000
G1 X128.639 Y123.93 Z4.2
G1 Z3.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.170413
G1 F2428
G1 X128.565 Y123.835 E.0012
; LINE_WIDTH: 0.186291
G1 X128.553 Y123.823 E.0002
G1 X127.721 Y123.796 E.00943
; LINE_WIDTH: 0.160265
G1 X127.698 Y123.797 E.00021
; LINE_WIDTH: 0.17554
G1 X127.571 Y123.818 E.00135
; LINE_WIDTH: 0.2031
G1 X127.444 Y123.839 E.00163
; WIPE_START
G1 F15000
G1 X127.571 Y123.818 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.326 J1.173 P1  F30000
G1 X129.361 Y124.316 Z4.2
G1 Z3.8
G1 E.4 F1800
; LINE_WIDTH: 0.0978591
G1 F2428
G1 X129.261 Y124.115 E.00097
; WIPE_START
G1 F15000
G1 X129.361 Y124.316 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-.941 J.771 P1  F30000
G1 X129.924 Y125.001 Z4.2
G1 Z3.8
G1 E.4 F1800
; LINE_WIDTH: 0.103299
G1 F2428
G1 X129.907 Y124.904 E.00047
G1 X129.845 Y124.869 E.00034
; WIPE_START
G1 F15000
G1 X129.907 Y124.904 E-.15998
G1 X129.924 Y125.001 E-.22002
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I-1.117 J-.484 P1  F30000
G1 X128.555 Y128.161 Z4.2
G1 Z3.8
G1 E.4 F1800
; LINE_WIDTH: 0.203103
G1 F2428
G1 X128.429 Y128.182 E.00163
; LINE_WIDTH: 0.173275
G3 X128.279 Y128.204 I-.19 J-.755 E.00156
; LINE_WIDTH: 0.172422
G1 X127.863 Y128.191 E.00426
; LINE_WIDTH: 0.199729
G1 X127.447 Y128.177 E.00516
G1 X127.435 Y128.164 E.00022
; LINE_WIDTH: 0.170122
G1 X127.362 Y128.07 E.0012
; WIPE_START
G1 F15000
G1 X127.435 Y128.164 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.2 I.712 J.987 P1  F30000
G1 X133.446 Y123.831 Z4.2
G1 Z3.8
G1 E.4 F1800
; LINE_WIDTH: 0.400262
G1 F2428
G1 X133.28 Y122.959 E.02504
G1 X133.273 Y122.948 F30000
; LINE_WIDTH: 0.400234
G1 F2428
G1 X132.602 Y122.368 E.02504
; CHANGE_LAYER
; Z_HEIGHT: 4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F12593.987
G1 X133.273 Y122.948 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 20/50
; update layer progress
M73 L20
M991 S0 P19 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z4.2 I-.08 J-1.214 P1  F30000
G1 X124.515 Y123.527 Z4.2
G1 Z4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.667 Y123.439 E.00563
G1 X128 Y121.515 E.12377
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
M73 P37 R8
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y123.758 E.14421
G1 X124.463 Y123.557 E.0129
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X124.87 Y123.792 E.00562
G1 X128 Y121.985 E.11621
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.1291
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.066 Y124.132 E.00521
G1 X128 Y122.438 E.1009
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.066 Y124.132 E-.08029
G1 X125.749 Y123.737 E-.29971
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-.672 J-1.015 P1  F30000
G1 X122.895 Y125.626 Z4.4
G1 Z4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.402 J-2.604 E.01653
G1 X122.278 Y126.148 E.00497
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.895 J2.464 E.0146
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03306
G3 X122.305 Y125.354 I.197 J-.645 E.05534
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01064
G1 X123.035 Y127.248 E.02935
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.316 J-1.036 E.08876
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.444 J-.951 E.01652
G1 X125 Y121.143 E.00416
G1 X125.055 Y121.054 E.00336
G1 X125.164 Y120.984 E.00417
G1 X125.268 Y120.971 E.00335
G1 X125.412 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.676 J1.997 E.0146
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.28 Y120.564 I.658 J-.152 E.03997
G1 X125.294 Y120.564 E.00046
G3 X125.711 Y120.745 I-.05 J.686 E.01489
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X123.816 Y123.461 E.15134
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.347 I5.301 J3.365 E.03968
G1 X124.196 Y121.483 E.0289
G3 X125.286 Y120.157 I1.055 J-.244 E.06374
G3 X125.99 Y120.447 I-.064 J1.152 E.02493
G1 X126.618 Y121.096 E.02904
G3 X127.834 Y120.921 I1.459 J5.817 E.03959
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.036 J1.632 E.01652
G1 X130.681 Y120.979 E.00334
G1 X130.785 Y120.972 E.00336
G1 X130.884 Y121.006 E.00335
G1 X130.962 Y121.074 E.00334
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.571 J-.454 E.01459
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.5 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03073
G3 X131.804 Y121.483 I-.145 J1.075 E.05802
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02935
G1 X132.31 Y123.318 E.01064
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02404
G1 X133.578 Y125.745 E.01566
G1 X133.648 Y125.778 E.00252
G1 X133.722 Y125.852 E.00334
G1 X133.767 Y126 E.00499
G1 X133.722 Y126.148 E.00498
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.895 J-2.465 E.0146
G1 X132.998 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00994
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.645 I-.2 J.645 E.05519
G1 X133.056 Y126.806 E.0212
G1 X133.216 Y127.185 F30000
G1 F1914
G1 X132.995 Y127.241 E.00735
G1 X132.558 Y128.248 E.0353
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01064
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.322 J1.035 E.08854
G1 X133.275 Y127.171 E.01789
; WIPE_START
G1 F11054.348
G1 X132.995 Y127.241 E-.10969
G1 X132.712 Y127.893 E-.27031
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-.958 J-.751 P1  F30000
G1 X130.876 Y130.234 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00498
G1 X130.945 Y130.946 E.00335
G1 X130.883 Y130.994 E.00252
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.663 J-1.984 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.301 J-3.365 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.383 Y130.905 E.02899
G3 X128.166 Y131.079 I-1.467 J-5.912 E.03961
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18952
G1 X131.848 Y129.311 E-.10814
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G3 X125.412 Y130.975 I-2.041 J-1.636 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.59 J.459 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.255 E.03306
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
M73 P38 R8
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02716
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I.189 J1.202 P1  F30000
G1 X133.228 Y127.725 Z4.4
G1 Z4
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.02463
G3 X132.008 Y129.751 I-5.483 J-2.816 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.243 Y131.345 E.02261
G3 X127.641 Y131.478 I-1.297 J-5.925 E.05184
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02135
G3 X123.799 Y130.425 I-1.013 J-1.096 E.1219
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02207
G3 X122.068 Y124.574 I.435 J-1.426 E.12219
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.484 J2.817 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.758 Y120.656 E.02265
G3 X128.359 Y120.522 I1.296 J5.872 E.05182
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.945 Y119.76 I1.024 J1.105 E.04229
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.933 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.425 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.67 E.00293
G1 X133.553 Y128 F30000
G1 F1914
G1 X133.289 Y128.608 E.02132
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.102 Y131.785 E.01623
G3 X126.883 Y131.8 I-1.151 J-6.047 E.07175
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.489 J-2.876 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.742 J-1.021 E.03411
G3 X125.3 Y119.343 I1.912 J.147 E.09312
G3 X126.547 Y119.852 I-.096 J2.017 E.04417
G1 X126.898 Y120.215 E.01625
G3 X129.117 Y120.2 I1.152 J6.033 E.07173
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01555
G1 X133.577 Y127.945 E.00043
M204 S250
G1 X133.868 Y128.265 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00011
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19234
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.922 E.05348
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.306 Y118.95 I2.164 J-.8 E.13337
G3 X127.034 Y119.791 I-.066 J2.331 E.05898
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05347
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.194 I-.379 J2.268 E.18305
G1 X133.927 Y128.251 E.00732
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02423
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.109 E-.1422
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I.061 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z4.4
G1 Z4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118619
G1 F1914
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.16202
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205421
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.248823
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-.62 J-1.047 P1  F30000
G1 X129.342 Y130.57 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.247242
G1 F1914
G1 X129.188 Y130.627 E.00265
; LINE_WIDTH: 0.204294
G1 X129.034 Y130.683 E.00209
; LINE_WIDTH: 0.161345
G1 X128.88 Y130.74 E.00154
; LINE_WIDTH: 0.118396
G1 X128.725 Y130.797 E.00098
; WIPE_START
G1 F15000
G1 X128.88 Y130.74 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.166669
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28735
G1 X125.272 Y130.821 E-.09265
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.260651
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213869
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167086
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120304
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167097
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213882
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260668
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.167358
G1 F1914
G1 X122.5 Y126 E.0019
G1 X122.452 Y125.961 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09204
G1 X122.691 Y125.977 E-.28796
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.118628
G1 F1914
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.162024
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.20542
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.248815
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I.62 J1.047 P1  F30000
G1 X126.659 Y121.431 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.24639
G1 F1914
G1 X126.812 Y121.374 E.00264
; LINE_WIDTH: 0.203686
G1 X126.966 Y121.317 E.00208
; LINE_WIDTH: 0.160981
G1 X127.12 Y121.26 E.00153
; LINE_WIDTH: 0.118277
G1 X127.274 Y121.203 E.00098
; WIPE_START
G1 F15000
G1 X127.12 Y121.26 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I.011 J1.217 P1  F30000
G1 X130.811 Y121.227 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.166383
G1 F1914
G1 X130.751 Y121.236 E.0006
G1 X130.631 Y121.389 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28908
G1 X130.811 Y121.227 E-.09092
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.260657
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213873
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167089
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120305
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.4 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z4.4
G1 Z4
G1 E.4 F1800
; LINE_WIDTH: 0.120311
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167097
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213882
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 4.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 21/50
; update layer progress
M73 L21
M991 S0 P20 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z4.4 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z4.4
G1 Z4.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X124.76 Y123.386 E.0239
G1 X128 Y121.515 E.12032
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
M73 P39 R8
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X124.963 Y123.738 E.00906
G1 X128 Y121.985 E.11276
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.159 Y124.078 E.0084
G1 X128 Y122.438 E.09771
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
M73 P39 R7
G1 F11933.819
M204 S10000
G1 X125.159 Y124.078 E-.12015
G1 X125.751 Y123.736 E-.25985
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-.672 J-1.015 P1  F30000
G1 X122.895 Y125.626 Z4.6
G1 Z4.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.394 J-2.576 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00499
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.895 J2.464 E.0146
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03306
G3 X122.304 Y125.355 I.197 J-.645 E.05533
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.316 J-1.036 E.08875
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.44 J-.95 E.01652
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.054 E.00417
G1 X125.164 Y120.984 E.00418
G1 X125.268 Y120.97 E.00335
G1 X125.413 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.686 J2.006 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.275 Y120.563 I.658 J-.152 E.03979
G3 X125.711 Y120.744 I-.042 J.719 E.01548
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.298 J3.363 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.281 Y120.156 I1.055 J-.244 E.06357
G3 X125.99 Y120.447 I-.058 J1.151 E.0251
G1 X126.614 Y121.093 E.02889
G3 X127.834 Y120.921 I1.485 J6.123 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.037 J1.633 E.01652
G1 X130.681 Y120.979 E.00334
G1 X130.785 Y120.972 E.00335
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00336
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.569 J-.453 E.0146
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.818 Y120.567 I.462 J.497 E.01851
G3 X131.407 Y121.39 I-.068 J.671 E.03682
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.852 Y120.161 I.741 J.797 E.02944
G3 X131.804 Y121.483 I-.101 J1.077 E.05932
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.745 E.01565
G1 X133.706 Y125.831 E.00499
G1 X133.766 Y125.974 E.00499
G1 X133.756 Y126.077 E.00334
G1 X133.722 Y126.148 E.00253
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.895 J-2.464 E.01459
G1 X132.998 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00993
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.646 I-.197 J.645 E.05533
G1 X133.056 Y126.806 E.0212
G1 X132.904 Y127.45 F30000
G1 F1914
G1 X132.558 Y128.248 E.02795
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08855
G1 X132.995 Y127.241 E.02716
G1 X132.927 Y127.395 E.00542
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35311
G1 X132.523 Y128.31 E-.02689
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-.925 J-.791 P1  F30000
G1 X130.876 Y130.234 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.702 E.01565
G1 X131.013 Y130.807 E.00335
G1 X130.989 Y130.881 E.00253
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.673 J-1.993 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.657 J.152 E.05533
G1 X129.574 Y130.516 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I1.138 J.432 P1  F30000
G1 X132.183 Y128.54 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.311 J-3.372 E.03966
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.055 J.244 E.08875
G1 X129.385 Y130.907 E.02892
G3 X128.166 Y131.079 I-1.479 J-6.048 E.03965
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18967
G1 X131.848 Y129.311 E-.108
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G3 X125.412 Y130.975 I-2.042 J-1.637 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.117 Y130.994 E.00498
G1 X125.011 Y130.881 E.00499
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.578 J.456 E.01652
G1 X125.719 Y130.578 E.0221
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.46 J-.493 E.05532
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.739 J-.791 E.08874
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I.189 J1.202 P1  F30000
M73 P40 R7
G1 X133.228 Y127.725 Z4.6
G1 Z4.2
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.02464
G3 X132.008 Y129.751 I-5.491 J-2.821 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.452 J.336 E.12217
G1 X129.244 Y131.346 E.02256
G3 X127.641 Y131.478 I-1.299 J-5.997 E.05186
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12218
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.435 J-1.426 E.12218
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.483 J2.816 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.885 Y119.755 I1.02 J1.098 E.04036
G3 X132.201 Y121.575 I-.135 J1.483 E.08181
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.425 E.1219
G1 X133.288 Y127.587 E.02135
G1 X133.252 Y127.67 E.00292
G1 X133.553 Y128 F30000
G1 F1914
G1 X133.289 Y128.608 E.02132
G3 X132.459 Y129.848 I-5.515 J-2.792 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.0162
G3 X126.883 Y131.8 I-1.15 J-6.065 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.489 J-2.876 E.03392
G3 X121.949 Y124.185 I1.07 J-1.575 E.13732
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.294 Y119.342 I1.912 J.147 E.09295
G3 X126.547 Y119.852 I-.09 J2.015 E.04434
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.422 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.057 J1.577 E.13769
G1 X133.582 Y127.933 E.01554
G1 X133.577 Y127.945 E.00042
M204 S250
G1 X133.869 Y128.265 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00012
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19277
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.922 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.301 Y118.95 I2.164 J-.8 E.13321
G3 X127.033 Y119.791 I-.06 J2.33 E.05911
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.194 I-.379 J2.268 E.18305
G1 X133.927 Y128.251 E.00731
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02433
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.109 E-.1421
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I.061 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z4.6
G1 Z4.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118628
G1 F1914
G1 X131.667 Y129.131 E.00099
; LINE_WIDTH: 0.162061
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205493
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248926
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.57 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.248389
G1 F1914
G1 X129.188 Y130.627 E.00267
; LINE_WIDTH: 0.205112
G1 X129.034 Y130.684 E.00211
; LINE_WIDTH: 0.161835
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118558
G1 X128.724 Y130.798 E.00098
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.166588
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.325 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.2874
G1 X125.272 Y130.821 E-.0926
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.260642
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213862
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167083
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.166397
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.0926
G1 X122.691 Y125.977 E-.2874
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.11863
G1 F1914
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162027
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205425
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.248822
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.248997
G1 F1914
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205544
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.16209
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118637
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I.009 J1.217 P1  F30000
G1 X130.812 Y121.23 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.165124
G1 F1914
G1 X130.751 Y121.236 E.00059
G2 X130.635 Y121.391 I.286 J.336 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28867
G1 X130.812 Y121.23 E-.09133
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.260637
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213859
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167081
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120303
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.6 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z4.6
G1 Z4.2
G1 E.4 F1800
; LINE_WIDTH: 0.120309
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.16709
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.21387
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.26065
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 4.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 22/50
; update layer progress
M73 L22
M991 S0 P21 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z4.6 I.177 J-1.204 P1  F30000
G1 X124.515 Y123.527 Z4.6
G1 Z4.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1913
G1 X124.852 Y123.332 E.01251
G1 X128 Y121.515 E.11688
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y123.758 E.14422
G1 X124.463 Y123.557 E.01291
G1 X124.719 Y123.879 F30000
M73 P41 R7
G1 F1913
G1 X125.056 Y123.685 E.01251
G1 X128 Y121.985 E.10932
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1913
M204 S5000
G1 X125.252 Y124.024 E.01159
G1 X128 Y122.438 E.09452
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.252 Y124.024 E-.16043
G1 X125.752 Y123.736 E-.21957
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-.672 J-1.015 P1  F30000
G1 X122.895 Y125.626 Z4.8
G1 Z4.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1913
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.394 J-2.575 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00499
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.893 J2.457 E.0146
G1 X123.302 Y125.105 F30000
G1 F1913
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03306
G3 X122.304 Y125.354 I.197 J-.646 E.05533
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.316 J-1.036 E.08876
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.439 J-.95 E.01652
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.054 E.00417
G1 X125.14 Y120.994 E.00335
G1 X125.268 Y120.97 E.00417
G1 X125.412 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.694 J2.014 E.0146
G1 X126.426 Y121.484 F30000
G1 F1913
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.269 Y120.563 I.657 J-.152 E.03962
G3 X125.711 Y120.745 I-.036 J.717 E.01565
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.347 I5.299 J3.364 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.276 Y120.156 I1.055 J-.244 E.0634
G3 X125.99 Y120.447 I-.052 J1.149 E.02527
G1 X126.614 Y121.093 E.02889
G3 X127.834 Y120.921 I1.485 J6.123 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.039 J1.634 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00336
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00336
G3 X130.897 Y121.71 I-2.568 J-.453 E.01459
G1 X131.125 Y122.379 F30000
G1 F1913
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.745 E.03306
G3 X130.838 Y120.568 I.464 J.5 E.01916
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02716
G3 X130.891 Y120.164 I.744 J.803 E.03073
G3 X131.804 Y121.483 I-.145 J1.075 E.05802
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02935
G1 X132.31 Y123.318 E.01064
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.745 E.01565
G1 X133.648 Y125.778 E.00251
G1 X133.722 Y125.852 E.00335
G1 X133.767 Y126 E.00499
G1 X133.722 Y126.148 E.00498
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.894 J-2.458 E.01459
G1 X132.998 Y126.82 F30000
G1 F1913
G1 X132.698 Y126.895 E.00993
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.645 I-.199 J.645 E.05523
G1 X133.056 Y126.806 E.02121
G1 X133.216 Y127.185 F30000
G1 F1913
G1 X132.995 Y127.241 E.00735
G1 X132.558 Y128.248 E.0353
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.32 J1.035 E.08861
G1 X133.274 Y127.171 E.01789
; WIPE_START
G1 F11054.348
G1 X132.995 Y127.241 E-.1096
G1 X132.711 Y127.894 E-.2704
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-.958 J-.751 P1  F30000
G1 X130.876 Y130.234 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X131.01 Y130.703 E.01565
G1 X131.013 Y130.806 E.00334
G1 X130.989 Y130.881 E.00253
G1 X130.884 Y130.994 E.00498
G1 X130.733 Y131.03 E.00499
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.682 J-2.002 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1913
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.657 J.152 E.05532
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.301 J-3.365 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.055 J.244 E.08875
G1 X129.385 Y130.907 E.02891
G3 X128.166 Y131.079 I-1.48 J-6.061 E.03965
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18952
G1 X131.848 Y129.311 E-.10814
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G3 X125.412 Y130.975 I-2.044 J-1.64 E.01652
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.567 J.453 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1913
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I.189 J1.202 P1  F30000
G1 X133.228 Y127.725 Z4.8
G1 Z4.4
G1 E.4 F1800
G1 F1913
G1 X132.923 Y128.428 E.02464
G3 X132.008 Y129.751 I-5.483 J-2.816 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.452 J.336 E.12217
G1 X129.244 Y131.346 E.02256
G3 X127.641 Y131.478 I-1.3 J-6.005 E.05187
M73 P42 R7
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.435 J-1.426 E.12218
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.484 J2.817 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12218
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02135
G3 X130.945 Y119.76 I1.024 J1.105 E.0423
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.44 J1.426 E.12199
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.67 E.00292
G1 X133.653 Y127.915 F30000
G1 F1913
G1 X133.582 Y127.933 E.00235
G3 X132.459 Y129.848 I-5.806 J-2.116 E.07177
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.0162
G3 X126.883 Y131.8 I-1.15 J-6.067 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.742 J-1.021 E.03412
G3 X125.289 Y119.342 I1.912 J.147 E.09278
G3 X126.547 Y119.852 I-.084 J2.014 E.04451
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.074 E.07178
G3 X130.082 Y119.461 I1.956 J1.556 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.422 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.711 Y127.901 E.01127
M204 S250
G1 X133.869 Y128.265 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1913
M204 S5000
G1 X133.865 Y128.266 E.00013
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19277
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.295 Y118.95 I2.164 J-.8 E.13305
G3 X127.033 Y119.791 I-.055 J2.33 E.05927
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.195 I-.375 J2.268 E.18321
G1 X133.927 Y128.251 E.00731
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02439
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.109 E-.14203
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I.06 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z4.8
G1 Z4.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118619
G1 F1913
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.16202
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205421
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.248823
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.248514
G1 F1913
G1 X129.188 Y130.627 E.00268
; LINE_WIDTH: 0.205201
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161888
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118576
G1 X128.724 Y130.798 E.00098
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.166793
G1 F1913
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28728
G1 X125.272 Y130.821 E-.09272
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.260642
G1 F1913
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213863
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167083
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120304
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1913
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167097
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213883
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260668
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.166682
G1 F1913
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09242
G1 X122.691 Y125.977 E-.28758
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.118629
G1 F1913
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162027
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205424
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.248822
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.248997
G1 F1913
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205543
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.16209
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118636
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I.017 J1.217 P1  F30000
G1 X130.805 Y121.206 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.164799
G1 F1913
G1 X130.751 Y121.236 E.00059
G1 X130.631 Y121.389 E.00187
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28857
G1 X130.805 Y121.206 E-.09143
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-1.144 J.416 P1  F30000
G1 X131.29 Y122.542 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.260645
G1 F1913
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213865
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167084
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120303
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z4.8 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z4.8
G1 Z4.4
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1913
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167097
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213882
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 4.6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 23/50
; update layer progress
M73 L23
M991 S0 P22 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z4.8 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z4.8
G1 Z4.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X124.945 Y123.279 E.03079
G1 X128 Y121.515 E.11343
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.149 Y123.631 E.01595
G1 X128 Y121.985 E.10588
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
M73 P43 R7
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.345 Y123.971 E.01478
G1 X128 Y122.438 E.09133
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.345 Y123.971 E-.20088
G1 X125.753 Y123.735 E-.17912
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-.672 J-1.015 P1  F30000
G1 X122.895 Y125.626 Z5
G1 Z4.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.393 J-2.572 E.01652
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00499
G3 X122.836 Y125.636 I.894 J2.462 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03306
G3 X122.304 Y125.355 I.2 J-.646 E.0552
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.442 J-.95 E.01652
G1 X125 Y121.143 E.00417
G1 X125.055 Y121.054 E.00334
G1 X125.14 Y120.994 E.00335
G1 X125.257 Y120.97 E.00386
G1 X125.344 Y120.987 E.00283
G1 X125.413 Y121.025 E.00253
G3 X125.733 Y121.346 I-1.678 J1.999 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.264 Y120.563 I.657 J-.152 E.03945
G3 X125.711 Y120.745 I-.03 J.716 E.01583
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.299 J3.364 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.27 Y120.156 I1.055 J-.244 E.06322
G3 X125.99 Y120.447 I-.046 J1.148 E.02545
G1 X126.614 Y121.093 E.02889
G3 X127.834 Y120.921 I1.485 J6.123 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.045 J1.64 E.01652
G1 X130.681 Y120.979 E.00334
G1 X130.774 Y120.971 E.00302
G1 X130.884 Y121.006 E.00368
G1 X130.962 Y121.075 E.00336
G1 X131.008 Y121.168 E.00333
G1 X131.015 Y121.272 E.00336
G3 X130.897 Y121.71 I-2.584 J-.457 E.01459
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.808 Y120.566 I.462 J.497 E.01817
G3 X131.407 Y121.39 I-.058 J.672 E.03715
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.841 Y120.16 I.741 J.797 E.02909
G3 X131.804 Y121.483 I-.091 J1.078 E.05965
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.744 E.01564
G1 X133.706 Y125.831 E.005
G1 X133.766 Y125.974 E.00499
G1 X133.735 Y126.126 E.00498
G1 X133.669 Y126.206 E.00334
G1 X133.602 Y126.247 E.00252
G3 X133.164 Y126.364 I-.895 J-2.463 E.0146
G1 X132.998 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00993
G1 X132.698 Y125.105 E.05758
G1 X133.695 Y125.354 E.03306
G3 X133.696 Y126.646 I-.2 J.646 E.05521
G1 X133.056 Y126.806 E.0212
G1 X132.904 Y127.45 F30000
G1 F1914
G1 X132.558 Y128.248 E.02796
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01064
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.964 E.02815
G3 X133.814 Y127.036 I-.321 J1.036 E.08856
G1 X132.995 Y127.241 E.02716
G1 X132.928 Y127.395 E.00541
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35317
G1 X132.524 Y128.31 E-.02683
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-.925 J-.791 P1  F30000
G1 X130.876 Y130.234 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00498
G1 X130.962 Y130.926 E.00253
G1 X130.884 Y130.994 E.00334
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.686 J-2.006 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.0552
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.299 J-3.364 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.02891
G3 X128.166 Y131.079 I-1.48 J-6.061 E.03965
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08233
G1 X132.032 Y129.094 E-.18952
G1 X131.848 Y129.311 E-.10815
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G3 X125.413 Y130.975 I-2.043 J-1.638 E.01651
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.579 J.456 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.46 J-.493 E.05532
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.739 J-.791 E.08875
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I.189 J1.202 P1  F30000
G1 X133.228 Y127.725 Z5
G1 Z4.6
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.02464
G3 X132.008 Y129.751 I-5.483 J-2.816 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.346 E.02256
G3 X127.641 Y131.478 I-1.3 J-6.005 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.017 J-1.09 E.12217
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
M73 P44 R7
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.443 J-1.426 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.484 J2.816 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02135
G3 X130.874 Y119.754 I1.02 J1.097 E.04002
G3 X132.201 Y121.575 I-.124 J1.484 E.08215
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08123
G1 X133.932 Y124.574 E.02207
G3 X133.932 Y127.426 I-.442 J1.426 E.1219
G1 X133.288 Y127.587 E.02135
G1 X133.252 Y127.67 E.00292
G1 X133.553 Y128 F30000
G1 F1914
G1 X133.289 Y128.608 E.02133
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.0162
G3 X126.883 Y131.8 I-1.15 J-6.067 E.07177
G3 X125.918 Y132.539 I-1.955 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.875 E.03392
G3 X121.949 Y124.185 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07178
G3 X123.357 Y121.113 I2.742 J-1.021 E.03412
G3 X125.284 Y119.342 I1.912 J.147 E.09261
G3 X126.547 Y119.852 I-.078 J2.014 E.04468
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07164
G3 X134.554 Y124.422 I-.489 J2.877 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13766
G1 X133.582 Y127.933 E.01554
G1 X133.577 Y127.945 E.00042
M204 S250
G1 X133.869 Y128.265 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00013
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.922 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.579 J2.112 E.05794
G3 X125.29 Y118.95 I2.164 J-.8 E.1329
G3 X127.033 Y119.791 I-.05 J2.33 E.05943
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X134.166 Y128.194 I-.379 J2.268 E.18305
G1 X133.927 Y128.251 E.0073
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02442
G1 X133.641 Y128.782 E-.21357
G1 X133.46 Y129.109 E-.14201
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I.06 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z5
G1 Z4.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.11863
G1 F1914
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162027
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205424
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.248821
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.248514
G1 F1914
G1 X129.188 Y130.627 E.00268
; LINE_WIDTH: 0.205201
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161889
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118576
G1 X128.724 Y130.798 E.00098
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-.022 J-1.217 P1  F30000
G1 X125.206 Y130.807 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.167409
G1 F1914
G1 X125.25 Y130.764 E.0006
G1 X125.325 Y130.586 E.0019
; WIPE_START
G1 F15000
G1 X125.25 Y130.764 E-.28829
G1 X125.206 Y130.807 E-.09171
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I1.142 J-.42 P1  F30000
G1 X124.71 Y129.459 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.260642
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213862
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167083
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.167439
G1 F1914
G1 X122.5 Y126 E.0019
G1 X122.452 Y125.961 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09204
G1 X122.691 Y125.977 E-.28796
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.118629
G1 F1914
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162026
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205423
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.24882
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.24899
G1 F1914
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205538
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162087
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118635
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.166322
G1 F1914
G1 X130.751 Y121.236 E.0006
G1 X130.631 Y121.389 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28902
G1 X130.811 Y121.227 E-.09098
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.260621
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213848
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167074
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.1203
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z5
G1 Z4.6
G1 E.4 F1800
; LINE_WIDTH: 0.120313
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167098
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213883
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 4.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 24/50
; update layer progress
M73 L24
M991 S0 P23 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z5 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z5
G1 Z4.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.038 Y123.225 E.03423
G1 X128 Y121.515 E.10999
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.241 Y123.578 E.01939
G1 X128 Y121.985 E.10243
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
M73 P45 R7
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.437 Y123.917 E.01797
G1 X128 Y122.438 E.08814
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.437 Y123.917 E-.2414
G1 X125.753 Y123.735 E-.1386
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-.672 J-1.015 P1  F30000
G1 X122.895 Y125.626 Z5.2
G1 Z4.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.398 J-2.592 E.01651
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.891 J2.448 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.197 J-.645 E.05533
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.316 J-1.035 E.08875
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.441 J-.95 E.01651
G1 X125 Y121.143 E.00418
G1 X125.055 Y121.054 E.00336
G1 X125.14 Y120.994 E.00335
G1 X125.252 Y120.97 E.00368
G1 X125.344 Y120.987 E.00301
G1 X125.413 Y121.025 E.00253
G3 X125.733 Y121.346 I-1.686 J2.007 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.258 Y120.563 I.657 J-.152 E.03927
G3 X125.711 Y120.745 I-.024 J.715 E.016
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.346 I5.311 J3.373 E.03966
G1 X124.196 Y121.483 E.02889
G3 X125.265 Y120.156 I1.055 J-.244 E.06305
G3 X125.99 Y120.447 I-.04 J1.148 E.02562
G1 X126.614 Y121.093 E.02889
G3 X127.834 Y120.921 I1.485 J6.123 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.054 J1.649 E.01652
G1 X130.681 Y120.979 E.00334
G1 X130.769 Y120.971 E.00284
G1 X130.883 Y121.006 E.00384
G1 X130.962 Y121.074 E.00336
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.571 J-.454 E.0146
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.802 Y120.565 I.462 J.497 E.01799
G3 X131.407 Y121.39 I-.053 J.673 E.03732
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.836 Y120.159 I.741 J.797 E.02892
G3 X131.804 Y121.483 I-.086 J1.079 E.05981
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.745 E.01565
G1 X133.706 Y125.83 E.00498
G1 X133.766 Y125.974 E.00499
G1 X133.756 Y126.077 E.00334
G1 X133.722 Y126.148 E.00252
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.893 J-2.455 E.0146
G1 X132.998 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00993
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03306
G3 X133.696 Y126.645 I-.197 J.646 E.05533
G1 X133.056 Y126.806 E.02121
G1 X133.216 Y127.185 F30000
G1 F1914
G1 X132.995 Y127.241 E.00734
G1 X132.558 Y128.248 E.0353
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.964 E.02816
G3 X133.814 Y127.036 I-.316 J1.036 E.08875
G1 X133.274 Y127.171 E.0179
; WIPE_START
G1 F11054.348
G1 X132.995 Y127.241 E-.10957
G1 X132.711 Y127.894 E-.27043
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-.958 J-.751 P1  F30000
G1 X130.876 Y130.234 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.702 E.01565
G1 X131.016 Y130.781 E.00253
G1 X130.989 Y130.881 E.00334
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.687 J-2.007 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.516 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I1.138 J.432 P1  F30000
G1 X132.183 Y128.54 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.311 J-3.373 E.03966
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.09 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18966
G1 X131.848 Y129.311 E-.108
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G3 X125.413 Y130.975 I-2.04 J-1.635 E.01651
G1 X125.267 Y131.03 E.005
G1 X125.117 Y130.994 E.00497
G1 X125.011 Y130.881 E.00499
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.567 J.453 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.875 Y129.621 E.03306
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02935
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I.189 J1.202 P1  F30000
G1 X133.228 Y127.725 Z5.2
G1 Z4.8
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.02464
G3 X132.008 Y129.751 I-5.491 J-2.821 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.02 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.425 E.02208
G3 X122.068 Y124.574 I.435 J-1.425 E.12218
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.49 J2.82 E.05188
G1 X123.799 Y121.575 E.02254
M73 P46 R7
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.869 Y119.754 I1.02 J1.097 E.03985
G3 X132.201 Y121.575 I-.12 J1.485 E.0823
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.556 J4.079 E.08123
G1 X133.932 Y124.574 E.02208
G3 X133.932 Y127.426 I-.435 J1.426 E.12218
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.67 E.00292
G1 X133.653 Y127.915 F30000
G1 F1914
G1 X133.582 Y127.933 E.00235
G3 X132.459 Y129.848 I-5.807 J-2.116 E.07178
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07178
G3 X125.918 Y132.539 I-1.955 J-1.555 E.03947
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.489 J-2.876 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.807 J2.116 E.07178
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X125.278 Y119.342 I1.912 J.147 E.09244
G3 X126.547 Y119.852 I-.072 J2.013 E.04486
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.329 J3.778 E.07164
G3 X134.554 Y124.423 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.07 J1.575 E.13732
G1 X133.711 Y127.901 E.01127
M204 S250
G1 X133.869 Y128.265 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00013
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.285 Y118.95 I2.164 J-.8 E.13274
G3 X127.033 Y119.791 I-.044 J2.33 E.05959
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.111 J3.488 E.05782
G3 X134.166 Y128.195 I-.369 J2.268 E.18349
G1 X133.927 Y128.252 E.00731
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02441
G1 X133.641 Y128.782 E-.21357
G1 X133.46 Y129.109 E-.14201
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I.06 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z5.2
G1 Z4.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118629
G1 F1914
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162061
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205493
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248925
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.24876
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205377
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.161994
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118611
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.16675
G1 F1914
G1 X125.25 Y130.763 E.0006
G1 X125.325 Y130.586 E.00189
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28784
G1 X125.272 Y130.821 E-.09216
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.260633
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213856
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167079
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120302
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167097
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213882
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260668
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.166312
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.0006
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09246
G1 X122.691 Y125.977 E-.28754
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.118656
G1 F1914
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.162112
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205569
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.249025
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.24899
G1 F1914
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205538
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162087
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118635
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I.009 J1.217 P1  F30000
G1 X130.812 Y121.23 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.165056
G1 F1914
G1 X130.751 Y121.236 E.00059
G2 X130.635 Y121.391 I.281 J.333 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28875
G1 X130.812 Y121.23 E-.09125
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.260621
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213847
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167073
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.1203
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.2 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z5.2
G1 Z4.8
G1 E.4 F1800
; LINE_WIDTH: 0.120304
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.16708
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213856
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260632
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 5
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 25/50
; update layer progress
M73 L25
M991 S0 P24 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z5.2 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z5.2
G1 Z5
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1913
G1 X124.116 Y123.758 E.01484
G1 X125.131 Y123.172 E.03767
G1 X128 Y121.515 E.10655
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
M73 P46 R6
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1913
G1 X125.334 Y123.524 E.02284
G1 X128 Y121.985 E.09899
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1913
M204 S5000
G1 X125.53 Y123.864 E.02116
G1 X128 Y122.438 E.08495
G1 X131.085 Y124.219 E.10611
M73 P47 R6
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.53 Y123.864 E-.28198
G1 X125.753 Y123.735 E-.09802
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-.672 J-1.015 P1  F30000
G1 X122.895 Y125.626 Z5.4
G1 Z5
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1913
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.399 J-2.593 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00499
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.901 J2.486 E.01459
G1 X123.302 Y125.105 F30000
G1 F1913
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.354 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.964 I.321 J-1.035 E.08855
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X125.124 Y121.766 E.02403
G3 X124.985 Y121.272 I2.444 J-.951 E.01652
G1 X125 Y121.143 E.00417
G1 X125.055 Y121.054 E.00335
G1 X125.164 Y120.984 E.00417
G1 X125.268 Y120.97 E.00335
G1 X125.413 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.687 J2.007 E.01459
G1 X126.426 Y121.484 F30000
G1 F1913
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.253 Y120.563 I.657 J-.152 E.0391
G3 X125.711 Y120.744 I-.018 J.715 E.01617
G1 X126.384 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.299 J3.364 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.26 Y120.156 I1.055 J-.244 E.06288
G3 X125.99 Y120.447 I-.034 J1.147 E.02579
G1 X126.614 Y121.093 E.02889
G3 X127.834 Y120.921 I1.485 J6.123 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.039 J1.635 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.884 Y121.006 E.00335
G1 X130.962 Y121.074 E.00334
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.591 J-.459 E.0146
G1 X131.125 Y122.379 F30000
G1 F1913
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.797 Y120.565 I.462 J.497 E.01782
G3 X131.407 Y121.39 I-.048 J.673 E.03749
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.83 Y120.159 I.741 J.797 E.02875
G3 X131.804 Y121.483 I-.081 J1.079 E.05999
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.745 E.01565
G1 X133.706 Y125.83 E.00498
G1 X133.747 Y125.898 E.00252
G1 X133.767 Y126 E.00335
G1 X133.722 Y126.149 E.005
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.892 J-2.452 E.01459
G1 X132.998 Y126.82 F30000
G1 F1913
G1 X132.698 Y126.895 E.00993
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.646 I-.199 J.645 E.05524
G1 X133.056 Y126.806 E.02121
G1 X132.904 Y127.45 F30000
G1 F1913
G1 X132.558 Y128.248 E.02795
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.32 J1.035 E.08861
G1 X132.995 Y127.241 E.02717
G1 X132.928 Y127.395 E.00542
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35314
G1 X132.524 Y128.31 E-.02686
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-.925 J-.791 P1  F30000
G1 X130.876 Y130.234 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X131.01 Y130.703 E.01565
G1 X131.013 Y130.806 E.00334
G1 X130.989 Y130.881 E.00253
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.683 J-2.004 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1913
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.299 J-3.364 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.094 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08233
G1 X132.032 Y129.094 E-.18952
G1 X131.848 Y129.311 E-.10815
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G3 X125.413 Y130.975 I-2.05 J-1.645 E.01651
G1 X125.267 Y131.03 E.00499
G1 X125.117 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.584 J.458 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1913
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05518
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I.189 J1.202 P1  F30000
G1 X133.228 Y127.725 Z5.4
G1 Z5
G1 E.4 F1800
G1 F1913
G1 X132.923 Y128.428 E.02464
G3 X132.008 Y129.751 I-5.483 J-2.816 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.021 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.443 J-1.425 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.484 J2.817 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.864 Y119.753 I1.02 J1.098 E.03968
G3 X132.201 Y121.575 I-.114 J1.485 E.08248
M73 P48 R6
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.574 E.02208
G3 X133.932 Y127.426 I-.44 J1.426 E.122
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.67 E.00292
G1 X133.553 Y128 F30000
G1 F1913
G1 X133.289 Y128.608 E.02133
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.489 J-2.876 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X125.273 Y119.342 I1.912 J.147 E.09227
G3 X126.547 Y119.852 I-.067 J2.012 E.04503
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07164
G3 X134.554 Y124.423 I-.489 J2.875 E.03392
G3 X134.051 Y127.816 I-1.057 J1.577 E.13768
G1 X133.582 Y127.933 E.01554
G1 X133.577 Y127.945 E.00042
M204 S250
G1 X133.869 Y128.265 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1913
M204 S5000
G1 X133.865 Y128.266 E.00012
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19231
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19228
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.279 Y118.95 I2.164 J-.8 E.13258
G3 X127.033 Y119.791 I-.039 J2.33 E.05975
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.195 I-.375 J2.268 E.18322
G1 X133.927 Y128.251 E.00731
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02437
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.109 E-.14206
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I.06 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z5.4
G1 Z5
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.11863
G1 F1913
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162027
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205424
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.248821
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.248792
G1 F1913
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205397
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.162002
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118607
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.166578
G1 F1913
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28744
G1 X125.272 Y130.821 E-.09256
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.260634
G1 F1913
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213857
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.16708
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120302
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.120309
G1 F1913
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167089
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.21387
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.26065
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.167158
G1 F1913
G1 X122.438 Y126.005 E.0025
; WIPE_START
G1 F15000
G1 X122.691 Y125.977 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.11862
G1 F1913
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162023
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205426
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.248829
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.249028
G1 F1913
G1 X126.812 Y121.372 E.00269
; LINE_WIDTH: 0.205566
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162103
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118641
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I.017 J1.217 P1  F30000
G1 X130.805 Y121.207 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.165622
G1 F1913
G1 X130.751 Y121.236 E.00059
G2 X130.634 Y121.391 I.285 J.336 E.0019
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28917
G1 X130.805 Y121.207 E-.09083
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-1.144 J.416 P1  F30000
G1 X131.29 Y122.542 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.260606
G1 F1913
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213837
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167067
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120298
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.4 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z5.4
G1 Z5
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1913
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167097
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213882
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 5.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 26/50
; update layer progress
M73 L26
M991 S0 P25 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z5.4 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z5.4
G1 Z5.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.223 Y123.118 E.04112
G1 X128 Y121.515 E.1031
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.427 Y123.471 E.02628
G1 X128 Y121.985 E.09555
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.623 Y123.81 E.02435
G1 X128 Y122.438 E.08176
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
M73 P49 R6
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.623 Y123.81 E-.32259
G1 X125.754 Y123.735 E-.05741
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-.672 J-1.015 P1  F30000
G1 X122.895 Y125.626 Z5.6
G1 Z5.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.396 J-2.581 E.01651
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.891 J2.447 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03306
G3 X122.304 Y125.354 I.2 J-.646 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02403
G3 X124.985 Y121.272 I2.444 J-.951 E.01651
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.055 E.00417
G1 X125.14 Y120.994 E.00335
G1 X125.268 Y120.97 E.00417
G1 X125.413 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.675 J1.995 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.248 Y120.563 I.658 J-.152 E.03893
G3 X125.711 Y120.745 I-.013 J.715 E.01634
G1 X126.384 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.301 J3.365 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.254 Y120.156 I1.055 J-.244 E.06271
G3 X125.99 Y120.447 I-.029 J1.147 E.02596
G1 X126.614 Y121.093 E.02889
G3 X127.834 Y120.921 I1.485 J6.123 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.041 J1.636 E.01651
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.884 Y121.006 E.00335
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00336
G3 X130.897 Y121.71 I-2.601 J-.462 E.01459
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.744 E.03307
G3 X130.792 Y120.564 I.462 J.498 E.01764
G3 X131.407 Y121.39 I-.048 J.678 E.03758
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.825 Y120.159 I.741 J.798 E.02857
G3 X131.804 Y121.483 I-.085 J1.087 E.06001
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02935
G1 X132.31 Y123.318 E.01064
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.744 E.01564
G1 X133.706 Y125.83 E.00498
G1 X133.766 Y125.974 E.00499
G1 X133.755 Y126.077 E.00335
G1 X133.722 Y126.148 E.00252
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.897 J-2.473 E.01459
G1 X132.998 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00993
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.354 E.03306
G3 X133.696 Y126.646 I-.199 J.646 E.05523
G1 X133.056 Y126.806 E.0212
G1 X132.904 Y127.45 F30000
G1 F1914
G1 X132.558 Y128.248 E.02795
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.964 E.02816
G3 X133.814 Y127.036 I-.32 J1.036 E.08861
G1 X132.995 Y127.241 E.02717
G1 X132.927 Y127.395 E.00542
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35308
G1 X132.524 Y128.31 E-.02692
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-.925 J-.791 P1  F30000
G1 X130.876 Y130.234 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00498
G1 X130.905 Y130.98 E.00499
G1 X130.811 Y131.023 E.00334
G1 X130.733 Y131.03 E.00252
G1 X130.588 Y130.975 E.00498
G3 X130.229 Y130.608 I1.684 J-2.005 E.01652
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.657 J.152 E.05533
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.306 J-3.369 E.03966
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.055 J.244 E.08875
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.094 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18963
G1 X131.848 Y129.311 E-.10803
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G3 X125.413 Y130.975 I-2.034 J-1.629 E.01651
G1 X125.267 Y131.03 E.00499
G1 X125.117 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.585 J.458 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I.208 J1.199 P1  F30000
G1 X133.434 Y127.55 Z5.6
G1 Z5.2
G1 E.4 F1800
G1 F1914
G1 X133.288 Y127.587 E.00485
G1 X132.923 Y128.428 E.02949
G3 X132.008 Y129.751 I-5.486 J-2.818 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.452 J.336 E.12218
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.022 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.484 J2.816 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02253
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.858 Y119.753 I1.02 J1.098 E.0395
G3 X132.201 Y121.575 I-.122 J1.496 E.08245
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.44 J1.426 E.12199
G1 X133.493 Y127.536 E.01458
G1 X133.653 Y127.915 F30000
M73 P50 R6
G1 F1914
G1 X133.582 Y127.933 E.00235
G3 X132.459 Y129.848 I-5.807 J-2.116 E.07177
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07178
G3 X125.918 Y132.539 I-1.955 J-1.555 E.03947
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.489 J-2.876 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X125.268 Y119.342 I1.912 J.147 E.0921
G3 X126.547 Y119.852 I-.061 J2.012 E.0452
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.955 J1.556 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.422 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.057 J1.577 E.13769
G1 X133.711 Y127.901 E.01127
M204 S250
G1 X133.868 Y128.265 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00012
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19231
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19228
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.274 Y118.95 I2.165 J-.8 E.13242
G3 X127.033 Y119.791 I-.033 J2.33 E.05991
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X134.166 Y128.195 I-.375 J2.268 E.18321
G1 X133.927 Y128.251 E.00732
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02428
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.109 E-.14215
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I.061 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z5.6
G1 Z5.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118627
G1 F1914
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162036
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205445
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248854
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.248784
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205391
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.161998
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118605
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.166629
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28736
G1 X125.272 Y130.821 E-.09264
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.260642
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213862
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167083
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.166351
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09259
G1 X122.691 Y125.977 E-.28741
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.11863
G1 F1914
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162027
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205424
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.248821
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.249032
G1 F1914
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205569
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162105
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118642
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.166367
G1 F1914
G1 X130.751 Y121.236 E.0006
G1 X130.63 Y121.389 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28895
G1 X130.811 Y121.227 E-.09105
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.260658
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213873
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167089
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120305
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.6 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z5.6
G1 Z5.2
G1 E.4 F1800
; LINE_WIDTH: 0.120313
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167098
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213883
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 5.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 27/50
; update layer progress
M73 L27
M991 S0 P26 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z5.6 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z5.6
G1 Z5.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.316 Y123.065 E.04456
G1 X128 Y121.515 E.09966
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12745
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.52 Y123.417 E.02973
G1 X128 Y121.985 E.0921
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.716 Y123.757 E.02754
G1 X128 Y122.438 E.07857
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.716 Y123.757 E-.36322
M73 P51 R6
G1 X125.754 Y123.735 E-.01679
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-.671 J-1.015 P1  F30000
G1 X122.895 Y125.626 Z5.8
G1 Z5.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.394 J-2.573 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.893 J2.454 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03307
G3 X122.304 Y125.355 I.197 J-.645 E.05533
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.316 J-1.036 E.08876
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.445 J-.951 E.01652
G1 X125 Y121.143 E.00417
G1 X125.055 Y121.054 E.00336
G1 X125.14 Y120.994 E.00334
G1 X125.267 Y120.97 E.00418
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.685 J2.005 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.242 Y120.563 I.658 J-.152 E.03876
G3 X125.711 Y120.745 I-.008 J.715 E.01652
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.345 I5.369 J3.412 E.03968
G1 X124.196 Y121.483 E.02886
G3 X125.249 Y120.156 I1.055 J-.244 E.06254
G3 X125.99 Y120.447 I-.023 J1.147 E.02614
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.482 J6.089 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.039 J1.634 E.01652
G1 X130.681 Y120.979 E.00334
G1 X130.785 Y120.972 E.00336
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00336
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.572 J-.454 E.0146
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.5 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05802
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.744 E.01564
G1 X133.706 Y125.831 E.005
G1 X133.766 Y125.974 E.00499
G1 X133.756 Y126.077 E.00334
G1 X133.722 Y126.148 E.00253
G1 X133.602 Y126.247 E.00499
G3 X133.164 Y126.364 I-.89 J-2.446 E.01459
G1 X132.998 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00994
G1 X132.698 Y125.105 E.05759
G1 X133.695 Y125.354 E.03306
G3 X133.696 Y126.645 I-.197 J.646 E.05533
G1 X133.056 Y126.806 E.0212
G1 X133.216 Y127.185 F30000
G1 F1914
G1 X132.995 Y127.241 E.00735
G1 X132.558 Y128.248 E.0353
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01064
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.964 E.02815
G3 X133.814 Y127.035 I-.316 J1.036 E.08876
G1 X133.274 Y127.171 E.01789
; WIPE_START
G1 F11054.348
G1 X132.995 Y127.241 E-.10968
G1 X132.712 Y127.893 E-.27032
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-.958 J-.751 P1  F30000
G1 X130.876 Y130.234 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.702 E.01565
G1 X131 Y130.857 E.00499
G1 X130.962 Y130.926 E.00251
G1 X130.883 Y130.994 E.00335
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.684 J-2.004 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03306
G3 X130.289 Y131.255 I-.659 J.149 E.0552
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.655 I-5.378 J-3.418 E.03968
G1 X131.804 Y130.517 E.02885
G3 X130.01 Y131.553 I-1.057 J.24 E.08855
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.091 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.031 Y129.095 E-.18995
G1 X131.848 Y129.311 E-.10772
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G3 X125.412 Y130.975 I-2.022 J-1.617 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.117 Y130.994 E.00498
G1 X125.011 Y130.881 E.00499
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.585 J.458 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.255 E.03306
G3 X124.593 Y130.61 I-.461 J-.493 E.05533
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.739 J-.791 E.08875
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I.208 J1.199 P1  F30000
G1 X133.435 Y127.55 Z5.8
G1 Z5.4
G1 E.4 F1800
G1 F1914
G1 X133.288 Y127.587 E.00485
G1 X132.923 Y128.428 E.02948
G3 X132.009 Y129.752 I-5.525 J-2.841 E.05189
G1 X132.201 Y130.425 E.02251
G3 X129.732 Y131.85 I-1.456 J.33 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.021 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02135
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12218
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.435 J-1.426 E.12218
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.248 I5.521 J2.838 E.05189
G1 X123.799 Y121.575 E.02251
G3 X126.268 Y120.15 I1.452 J-.336 E.12218
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.019 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.945 Y119.76 I1.024 J1.105 E.04229
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.574 E.02207
G3 X133.932 Y127.426 I-.435 J1.426 E.12218
G1 X133.493 Y127.536 E.01458
G1 X133.653 Y127.915 F30000
G1 F1914
G1 X133.582 Y127.933 E.00235
G3 X132.46 Y129.849 I-5.818 J-2.121 E.07179
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.02 E.0341
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
M73 P52 R6
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.875 E.03392
G3 X121.949 Y124.185 I1.07 J-1.575 E.13732
G1 X122.418 Y124.067 E.01555
G3 X123.54 Y122.151 I5.816 J2.12 E.07179
G3 X123.357 Y121.113 I2.742 J-1.02 E.0341
G3 X125.262 Y119.342 I1.912 J.147 E.09193
G3 X126.547 Y119.852 I-.055 J2.011 E.04537
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.779 E.07164
G3 X134.554 Y124.423 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.07 J1.575 E.13732
G1 X133.711 Y127.901 E.01126
M204 S250
G1 X133.868 Y128.265 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00011
G3 X132.894 Y129.942 I-5.585 J-2.115 E.05795
G3 X128.967 Y132.209 I-2.154 J.803 E.19231
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.583 J2.114 E.05795
G3 X125.269 Y118.95 I2.165 J-.8 E.13225
G3 X127.033 Y119.791 I-.028 J2.331 E.06007
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.113 J3.489 E.05782
G3 X134.166 Y128.195 I-.369 J2.268 E.18349
G1 X133.926 Y128.252 E.00733
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02414
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.109 E-.14228
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I.061 J-1.215 P1  F30000
G1 X131.794 Y129.026 Z5.8
G1 Z5.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118737
G1 F1914
G1 X131.667 Y129.131 E.00099
; LINE_WIDTH: 0.162358
G1 X131.54 Y129.237 E.00156
; LINE_WIDTH: 0.205979
G1 X131.414 Y129.343 E.00213
; LINE_WIDTH: 0.2496
G1 X131.287 Y129.449 E.0027
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.248755
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205373
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161992
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.11861
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.166552
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.325 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28736
G1 X125.272 Y130.821 E-.09264
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.260655
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213872
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167089
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120305
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.167205
G1 F1914
G1 X122.438 Y126.007 E.0025
; WIPE_START
G1 F15000
G1 X122.691 Y125.977 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I1.086 J.548 P1  F30000
G1 X124.206 Y122.974 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.118723
G1 F1914
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.162324
G1 X124.46 Y122.763 E.00156
; LINE_WIDTH: 0.205926
G1 X124.586 Y122.657 E.00213
; LINE_WIDTH: 0.249527
G1 X124.713 Y122.551 E.00269
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.248731
G1 F1914
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205357
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161982
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118607
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I.017 J1.217 P1  F30000
G1 X130.805 Y121.207 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.164826
G1 F1914
G1 X130.751 Y121.236 E.00059
G1 X130.631 Y121.389 E.00187
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28852
G1 X130.805 Y121.207 E-.09148
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-1.144 J.416 P1  F30000
G1 X131.29 Y122.542 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.260621
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213848
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167074
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.1203
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z5.8 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z5.8
G1 Z5.4
G1 E.4 F1800
; LINE_WIDTH: 0.120313
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167098
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213883
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 5.6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 28/50
; update layer progress
M73 L28
M991 S0 P27 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z5.8 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z5.8
G1 Z5.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.409 Y123.011 E.04801
G1 X128 Y121.515 E.09622
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.612 Y123.364 E.03317
G1 X128 Y121.985 E.08866
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.808 Y123.703 E.03072
G1 X128 Y122.438 E.07538
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.756 Y123.737 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-.671 J-1.016 P1  F30000
G1 X122.895 Y125.626 Z6
G1 Z5.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.393 J-2.573 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00499
G3 X122.836 Y125.636 I.894 J2.459 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
M73 P53 R6
G1 X122.304 Y126.646 E.03306
G3 X122.304 Y125.354 I.197 J-.646 E.05534
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02815
G3 X122.186 Y124.964 I.316 J-1.036 E.08876
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.447 J-.952 E.01652
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.054 E.00417
G1 X125.14 Y120.994 E.00335
G1 X125.267 Y120.97 E.00417
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.671 J1.992 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03306
G3 X125.237 Y120.563 I.658 J-.152 E.03859
G3 X125.711 Y120.745 I-.002 J.716 E.01669
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.348 I5.244 J3.326 E.03964
G1 X124.196 Y121.483 E.02892
G3 X125.244 Y120.156 I1.055 J-.244 E.06237
G3 X125.99 Y120.447 I-.018 J1.147 E.02631
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.482 J6.087 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.045 J1.64 E.01651
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00334
G1 X130.883 Y121.006 E.00335
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.572 J-.454 E.0146
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.745 E.03306
G3 X130.781 Y120.563 I.464 J.5 E.01731
G3 X131.407 Y121.39 I-.038 J.679 E.03792
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02716
G3 X130.814 Y120.158 I.742 J.799 E.02824
G3 X131.804 Y121.483 I-.075 J1.088 E.06035
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01565
G1 X133.706 Y125.831 E.00498
G1 X133.756 Y125.923 E.00336
G1 X133.767 Y126 E.00251
G1 X133.722 Y126.148 E.00499
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.889 J-2.442 E.01459
G1 X132.998 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00994
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.645 I-.2 J.645 E.05519
G1 X133.056 Y126.806 E.0212
G1 X132.904 Y127.451 F30000
G1 F1914
G1 X132.558 Y128.248 E.02794
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08854
G1 X132.995 Y127.241 E.02717
G1 X132.927 Y127.396 E.00543
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35302
G1 X132.523 Y128.31 E-.02698
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-.925 J-.791 P1  F30000
G1 X130.876 Y130.234 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00498
G1 X130.906 Y130.98 E.00498
G1 X130.759 Y131.03 E.00499
G1 X130.681 Y131.021 E.00252
G1 X130.587 Y130.975 E.00335
G3 X130.229 Y130.608 I1.688 J-2.009 E.01652
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.655 I-5.37 J-3.413 E.03968
G1 X131.804 Y130.517 E.02886
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.094 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.031 Y129.094 E-.18989
G1 X131.848 Y129.311 E-.10777
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G3 X125.413 Y130.975 I-2.049 J-1.644 E.01652
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.558 J.45 E.01651
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.255 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03306
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02935
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I.189 J1.202 P1  F30000
G1 X133.228 Y127.726 Z6
G1 Z5.6
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.02463
G3 X132.008 Y129.752 I-5.523 J-2.84 E.05188
G1 X132.201 Y130.425 E.02251
G3 X129.732 Y131.85 I-1.456 J.33 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.022 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02207
G3 X122.068 Y124.574 I.435 J-1.426 E.12218
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.25 I5.456 J2.8 E.05186
G1 X123.799 Y121.575 E.02256
G3 X125.25 Y119.749 I1.452 J-.336 E.08615
G3 X126.268 Y120.15 I-.034 J1.579 E.03592
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.02 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02135
G3 X132.201 Y121.575 I1.017 J1.089 E.12218
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.426 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.67 E.00293
G1 X133.553 Y128 F30000
G1 F1914
G1 X133.289 Y128.608 E.02131
G3 X132.46 Y129.849 I-5.523 J-2.796 E.0481
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.02 E.0341
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.874 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
M73 P54 R6
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.799 J2.113 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03413
G3 X125.257 Y119.342 I1.912 J.147 E.09175
G3 X126.547 Y119.852 I-.05 J2.011 E.04554
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07177
G3 X130.082 Y119.461 I1.956 J1.556 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.874 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01555
G1 X133.576 Y127.945 E.00043
M204 S250
G1 X133.868 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00009
G3 X132.894 Y129.942 I-5.583 J-2.114 E.05795
G3 X128.967 Y132.209 I-2.154 J.803 E.19231
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.575 J2.111 E.05794
G3 X125.263 Y118.95 I2.165 J-.8 E.13211
G3 X127.033 Y119.791 I-.023 J2.331 E.06023
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.194 I-.379 J2.268 E.18304
G1 X133.926 Y128.252 E.00734
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02398
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.11 E-.14245
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I.061 J-1.215 P1  F30000
G1 X131.794 Y129.026 Z6
G1 Z5.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118723
G1 F1914
G1 X131.667 Y129.131 E.00099
; LINE_WIDTH: 0.162324
G1 X131.54 Y129.237 E.00156
; LINE_WIDTH: 0.205925
G1 X131.414 Y129.343 E.00213
; LINE_WIDTH: 0.249526
G1 X131.287 Y129.449 E.00269
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.248765
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205378
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.16199
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118603
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.166606
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28743
G1 X125.272 Y130.821 E-.09257
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.260644
M73 P54 R5
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213869
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167094
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120318
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.120318
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167113
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213908
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260703
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I1.072 J-.575 P1  F30000
G1 X122.691 Y125.977 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.1666
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09256
G1 X122.691 Y125.977 E-.28744
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.118538
G1 F1914
G1 X124.334 Y122.868 E.00098
; LINE_WIDTH: 0.161788
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205038
G1 X124.587 Y122.658 E.00211
; LINE_WIDTH: 0.248288
G1 X124.713 Y122.552 E.00267
; WIPE_START
G1 F15000
G1 X124.587 Y122.658 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.24873
G1 F1914
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205356
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161981
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118607
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.166353
G1 F1914
G1 X130.751 Y121.236 E.0006
G1 X130.63 Y121.389 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28904
G1 X130.811 Y121.227 E-.09096
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.260614
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213842
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167071
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120299
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z6
G1 Z5.6
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 5.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 29/50
; update layer progress
M73 L29
M991 S0 P28 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z6 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z6
G1 Z5.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.501 Y122.958 E.05145
G1 X128 Y121.515 E.09277
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12745
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.705 Y123.31 E.03661
G1 X128 Y121.985 E.08521
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.901 Y123.65 E.03391
G1 X128 Y122.438 E.07219
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.758 Y123.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-.669 J-1.016 P1  F30000
G1 X122.895 Y125.626 Z6.2
G1 Z5.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.399 J-2.593 E.01651
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00499
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.894 J2.462 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
M73 P55 R5
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.446 J-.951 E.01651
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.054 E.00417
G1 X125.14 Y120.994 E.00334
G1 X125.267 Y120.97 E.00417
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.669 J1.99 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03306
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.384 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.289 J3.357 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.238 Y120.156 I1.055 J-.244 E.0622
G3 X125.99 Y120.447 I-.013 J1.147 E.02648
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.483 J6.095 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.039 J1.635 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.884 Y121.006 E.00335
G1 X130.962 Y121.075 E.00336
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.582 J-.457 E.01459
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.809 Y120.157 I.742 J.8 E.02807
G3 X131.804 Y121.483 I-.061 J1.081 E.06067
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01565
G1 X133.669 Y125.794 E.00334
G1 X133.722 Y125.852 E.00253
G1 X133.767 Y126 E.00498
G1 X133.722 Y126.148 E.00498
G1 X133.602 Y126.247 E.00499
G3 X133.164 Y126.364 I-.889 J-2.443 E.01459
G1 X132.998 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00995
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.057 Y126.806 E.02118
G1 X132.903 Y127.451 F30000
G1 F1914
G1 X132.558 Y128.248 E.02794
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.316 J1.035 E.08876
G1 X132.995 Y127.241 E.02716
G1 X132.927 Y127.396 E.00544
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35293
G1 X132.523 Y128.31 E-.02707
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-.925 J-.791 P1  F30000
G1 X130.876 Y130.234 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01565
G1 X131.016 Y130.781 E.00252
G1 X130.989 Y130.881 E.00334
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.671 J-1.992 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.296 J-3.362 E.03966
G1 X131.804 Y130.518 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.095 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18953
G1 X131.848 Y129.311 E-.10813
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G3 X125.412 Y130.975 I-2.027 J-1.622 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.117 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.582 J.457 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.255 E.03306
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02716
G3 X124.196 Y130.517 I-.739 J-.791 E.08876
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02935
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I.189 J1.202 P1  F30000
G1 X133.228 Y127.726 Z6.2
G1 Z5.8
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.02462
G3 X132.008 Y129.751 I-5.48 J-2.814 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.022 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02135
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12218
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.478 J2.813 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.15 I1.452 J-.336 E.12218
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.021 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.842 Y119.752 I1.021 J1.099 E.03899
G3 X132.201 Y121.575 I-.094 J1.488 E.08316
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.574 E.02208
G3 X133.932 Y127.426 I-.435 J1.426 E.12219
G1 X133.288 Y127.587 E.02135
G1 X133.252 Y127.671 E.00294
G1 X133.553 Y128.001 F30000
G1 F1914
G1 X133.289 Y128.608 E.02131
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07178
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.874 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.252 Y119.342 I1.913 J.147 E.09158
G3 X126.547 Y119.852 I-.044 J2.011 E.04571
M73 P56 R5
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.07 J1.575 E.13733
G1 X133.582 Y127.933 E.01554
G1 X133.576 Y127.945 E.00044
M204 S250
G1 X133.867 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00008
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.258 Y118.95 I2.165 J-.8 E.13195
G3 X127.033 Y119.791 I-.018 J2.331 E.06039
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.195 I-.369 J2.268 E.18349
G1 X133.925 Y128.252 E.00736
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02377
G1 X133.641 Y128.782 E-.21357
G1 X133.459 Y129.11 E-.14266
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I.061 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z6.2
G1 Z5.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118619
G1 F1914
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162002
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205385
G1 X131.413 Y129.343 E.00211
; LINE_WIDTH: 0.248768
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.248785
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205392
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.161999
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118606
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-.027 J-1.217 P1  F30000
G1 X125.273 Y130.821 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.166835
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00189
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28754
G1 X125.273 Y130.821 E-.09246
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.26065
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213868
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167086
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120304
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.120321
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167121
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.21392
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.26072
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.166491
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09262
G1 X122.691 Y125.977 E-.28738
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.118605
G1 F1914
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.161971
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205338
G1 X124.587 Y122.657 E.00211
; LINE_WIDTH: 0.248704
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.248799
G1 F1914
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205405
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162011
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118617
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.166371
G1 F1914
G1 X130.751 Y121.236 E.0006
G1 X130.631 Y121.389 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28905
G1 X130.811 Y121.227 E-.09095
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.260621
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213848
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167074
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.1203
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.2 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z6.2
G1 Z5.8
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 30/50
; update layer progress
M73 L30
M991 S0 P29 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z6.2 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z6.2
G1 Z6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.594 Y122.904 E.05489
G1 X128 Y121.515 E.08933
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.798 Y123.257 E.04006
G1 X128 Y121.985 E.08177
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X125.994 Y123.596 E.0371
G1 X128 Y122.438 E.069
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.76 Y123.744 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-.668 J-1.017 P1  F30000
G1 X122.895 Y125.626 Z6.4
G1 Z6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.399 J-2.593 E.01651
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00499
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00499
G3 X122.836 Y125.636 I.893 J2.456 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
M73 P57 R5
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.446 J-.951 E.01652
G1 X125 Y121.143 E.00417
G1 X125.055 Y121.054 E.00335
G1 X125.14 Y120.994 E.00335
G1 X125.267 Y120.97 E.00417
G1 X125.413 Y121.025 E.005
G3 X125.733 Y121.346 I-1.681 J2.001 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04042
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.442 Y122.345 I5.43 J3.454 E.0397
G1 X124.196 Y121.483 E.02883
G3 X125.233 Y120.156 I1.055 J-.244 E.06202
G3 X125.99 Y120.447 I-.007 J1.147 E.02665
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.482 J6.09 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.028 J1.624 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.883 Y121.006 E.00335
G1 X130.962 Y121.075 E.00336
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.582 J-.457 E.01459
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.804 Y120.157 I.743 J.801 E.02789
G3 X131.804 Y121.483 I-.064 J1.089 E.0607
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01566
G1 X133.669 Y125.794 E.00334
G1 X133.722 Y125.852 E.00251
G1 X133.767 Y126 E.00498
G1 X133.722 Y126.148 E.00499
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.894 J-2.461 E.0146
G1 X132.999 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00996
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03308
G3 X133.696 Y126.646 I-.201 J.645 E.05519
G1 X133.057 Y126.806 E.02118
G1 X133.217 Y127.185 F30000
G1 F1914
G1 X132.995 Y127.241 E.00737
G1 X132.558 Y128.248 E.0353
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02817
G3 X133.814 Y127.036 I-.321 J1.035 E.08857
G1 X133.275 Y127.17 E.01786
; WIPE_START
G1 F11054.348
G1 X132.995 Y127.241 E-.10993
G1 X132.712 Y127.893 E-.27007
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-.958 J-.751 P1  F30000
G1 X130.876 Y130.234 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01566
G1 X131 Y130.857 E.00499
G1 X130.962 Y130.926 E.00251
G1 X130.884 Y130.994 E.00335
G1 X130.733 Y131.03 E.00499
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.669 J-1.99 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05566
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.32 J-3.378 E.03967
G1 X131.804 Y130.518 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.02891
G3 X128.166 Y131.079 I-1.48 J-6.064 E.03965
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08233
G1 X132.032 Y129.094 E-.18965
G1 X131.848 Y129.311 E-.10802
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G3 X125.412 Y130.975 I-2.032 J-1.628 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.117 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.582 J.457 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.255 E.03306
G3 X124.593 Y130.61 I-.459 J-.496 E.05521
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.0353
G1 X125.99 Y131.553 E.02716
G3 X124.196 Y130.517 I-.739 J-.791 E.08876
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I.208 J1.199 P1  F30000
G1 X133.435 Y127.55 Z6.4
G1 Z6
G1 E.4 F1800
G1 F1914
G1 X133.288 Y127.587 E.00487
G1 X132.923 Y128.428 E.02949
G3 X132.008 Y129.751 I-5.495 J-2.823 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.346 E.02256
G3 X127.641 Y131.478 I-1.3 J-6.006 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02135
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12218
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.991 Y122.248 I5.553 J2.858 E.0519
G1 X123.799 Y121.575 E.02249
G3 X126.268 Y120.15 I1.452 J-.336 E.12218
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.02 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.837 Y119.751 I1.021 J1.1 E.03882
G3 X132.201 Y121.575 I-.101 J1.497 E.08313
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.933 Y124.575 E.02208
G3 X133.932 Y127.426 I-.441 J1.425 E.12195
G1 X133.493 Y127.535 E.01455
G1 X133.653 Y127.915 F30000
G1 F1914
G1 X133.582 Y127.933 E.00238
G3 X132.459 Y129.848 I-5.809 J-2.117 E.07178
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.0162
G3 X126.883 Y131.8 I-1.15 J-6.067 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.874 E.03392
G3 X121.949 Y124.185 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.54 Y122.151 I5.824 J2.124 E.07179
G3 X123.357 Y121.113 I2.742 J-1.02 E.03408
G3 X125.246 Y119.342 I1.913 J.147 E.09141
G3 X126.547 Y119.852 I-.039 J2.01 E.04589
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.779 E.07165
M73 P58 R5
G3 X134.554 Y124.423 I-.488 J2.874 E.03392
G3 X134.051 Y127.816 I-1.056 J1.577 E.1377
G1 X133.712 Y127.9 E.01124
M204 S250
G1 X133.866 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00006
G3 X132.894 Y129.942 I-5.58 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.922 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.057 I5.588 J2.116 E.05795
G3 X125.253 Y118.95 I2.165 J-.8 E.13178
G3 X127.033 Y119.791 I-.013 J2.331 E.06055
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.194 I-.376 J2.268 E.18317
G1 X133.925 Y128.252 E.00737
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02353
G1 X133.641 Y128.782 E-.21357
G1 X133.458 Y129.111 E-.1429
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I.062 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z6.4
G1 Z6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118651
G1 F1914
G1 X131.667 Y129.131 E.00099
; LINE_WIDTH: 0.162112
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205573
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.249033
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.248529
G1 F1914
G1 X129.188 Y130.627 E.00268
; LINE_WIDTH: 0.205212
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161895
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118577
G1 X128.724 Y130.798 E.00098
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-.026 J-1.217 P1  F30000
G1 X125.225 Y130.82 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.167203
G1 F1914
G1 X125.326 Y130.586 E.0025
; WIPE_START
G1 F15000
G1 X125.225 Y130.82 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I1.138 J-.43 P1  F30000
G1 X124.71 Y129.459 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.26064
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213861
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167082
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.120321
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167121
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.21392
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.26072
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I1.072 J-.575 P1  F30000
G1 X122.691 Y125.977 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.166543
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09274
G1 X122.691 Y125.977 E-.28726
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I1.087 J.548 P1  F30000
G1 X124.206 Y122.975 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.118793
G1 F1914
G1 X124.332 Y122.869 E.00099
; LINE_WIDTH: 0.162549
G1 X124.459 Y122.763 E.00156
; LINE_WIDTH: 0.206306
G1 X124.586 Y122.657 E.00213
; LINE_WIDTH: 0.250062
G1 X124.713 Y122.551 E.0027
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I.62 J1.047 P1  F30000
G1 X126.657 Y121.429 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.248754
G1 F1914
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205373
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161991
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.11861
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.166889
G1 F1914
G2 X130.749 Y121.238 I-.023 J.055 E.00066
G1 X130.634 Y121.391 E.00187
; WIPE_START
G1 F15000
G1 X130.749 Y121.238 E-.28504
G1 X130.811 Y121.227 E-.09496
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.260614
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213842
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167071
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120299
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.4 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z6.4
G1 Z6
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 6.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 31/50
; update layer progress
M73 L31
M991 S0 P30 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z6.4 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z6.4
G1 Z6.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.687 Y122.85 E.05834
G1 X128 Y121.515 E.08589
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.89 Y123.203 E.0435
G1 X128 Y121.985 E.07833
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X126.087 Y123.543 E.04029
G1 X128 Y122.438 E.06581
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.762 Y123.747 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-.667 J-1.018 P1  F30000
G1 X122.895 Y125.626 Z6.6
G1 Z6.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.396 J-2.584 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.893 J2.456 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.354 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.964 I.316 J-1.035 E.08875
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02403
G3 X124.985 Y121.272 I2.428 J-.946 E.01652
G1 X124.992 Y121.168 E.00335
M73 P59 R5
G1 X125.055 Y121.054 E.00417
G1 X125.14 Y120.994 E.00335
G1 X125.267 Y120.97 E.00417
G1 X125.412 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.677 J1.998 E.0146
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04042
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.384 Y121.44 E.03113
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.346 I5.333 J3.387 E.03967
G1 X124.196 Y121.483 E.02888
G3 X125.228 Y120.156 I1.056 J-.244 E.06186
G3 X125.99 Y120.447 I-.002 J1.148 E.02682
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.483 J6.09 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.031 J1.626 E.01652
G1 X130.681 Y120.979 E.00334
G1 X130.785 Y120.972 E.00336
G1 X130.884 Y121.006 E.00335
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.583 J-.457 E.01459
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.5 E.01916
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02716
G3 X130.798 Y120.156 I.744 J.802 E.02773
G3 X131.804 Y121.483 I-.059 J1.089 E.06087
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01565
G1 X133.706 Y125.831 E.00498
G1 X133.766 Y125.974 E.00499
G1 X133.735 Y126.126 E.00498
G1 X133.689 Y126.189 E.00252
G1 X133.602 Y126.247 E.00335
G3 X133.164 Y126.364 I-.89 J-2.445 E.01459
G1 X132.999 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00997
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.057 Y126.805 E.02117
G1 X132.903 Y127.451 F30000
G1 F1914
G1 X132.558 Y128.248 E.02792
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08856
G1 X132.995 Y127.241 E.02717
G1 X132.927 Y127.396 E.00545
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35271
G1 X132.523 Y128.311 E-.02729
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-.925 J-.791 P1  F30000
G1 X130.876 Y130.234 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01565
G1 X131.016 Y130.781 E.00252
G1 X130.989 Y130.881 E.00335
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.675 J-1.995 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.516 E.03307
G1 X131.073 Y129.651 E.05566
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.324 J-3.381 E.03966
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.094 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18973
G1 X131.848 Y129.311 E-.10793
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G3 X125.413 Y130.975 I-2.042 J-1.637 E.01651
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.559 J.451 E.01651
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03306
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02935
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I.189 J1.202 P1  F30000
G1 X133.228 Y127.726 Z6.6
G1 Z6.2
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.0246
G3 X132.008 Y129.751 I-5.495 J-2.824 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.452 J.336 E.12217
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.021 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.425 E.02208
G3 X122.068 Y124.574 I.435 J-1.425 E.12218
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.501 J2.826 E.05188
G1 X123.799 Y121.575 E.02253
G3 X126.268 Y120.15 I1.452 J-.336 E.12218
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.02 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02135
G3 X130.832 Y119.751 I1.022 J1.101 E.03865
G3 X132.201 Y121.575 I-.096 J1.498 E.08331
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.441 J1.426 E.12194
G1 X133.288 Y127.587 E.02136
G1 X133.252 Y127.671 E.00295
G1 X133.552 Y128.001 F30000
G1 F1914
G1 X133.289 Y128.608 E.02129
G3 X132.459 Y129.848 I-5.516 J-2.793 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03947
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.874 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.54 Y122.152 I5.81 J2.118 E.07178
G3 X123.357 Y121.113 I2.743 J-1.02 E.03411
G3 X125.241 Y119.342 I1.913 J.148 E.09124
G3 X126.547 Y119.852 I-.033 J2.011 E.04606
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07178
G3 X130.082 Y119.461 I1.955 J1.556 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13165
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.056 J1.577 E.13771
G1 X133.582 Y127.933 E.01554
G1 X133.576 Y127.946 E.00046
M204 S250
M73 P60 R5
G1 X133.866 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X133.865 Y128.266 E.00004
G3 X132.894 Y129.942 I-5.58 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19276
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.58 J2.113 E.05794
G3 X125.247 Y118.95 I2.165 J-.8 E.13163
G3 X127.033 Y119.791 I-.008 J2.332 E.06071
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X134.166 Y128.194 I-.377 J2.268 E.18316
G1 X133.924 Y128.252 E.0074
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.865 Y128.266 E-.02326
G1 X133.641 Y128.782 E-.21357
G1 X133.458 Y129.111 E-.14317
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I.062 J-1.215 P1  F30000
G1 X131.793 Y129.026 Z6.6
G1 Z6.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118638
G1 F1914
G1 X131.667 Y129.131 E.00099
; LINE_WIDTH: 0.162095
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205552
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.249009
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.248795
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205399
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.162003
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118607
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.166689
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.2875
G1 X125.272 Y130.821 E-.0925
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.260648
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213867
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167085
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120304
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.120318
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167113
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213908
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260703
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.167197
G1 F1914
G1 X122.438 Y126.008 E.0025
; WIPE_START
G1 F15000
G1 X122.691 Y125.977 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.118663
G1 F1914
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.16215
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205638
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.249126
G1 X124.713 Y122.551 E.00269
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.248797
G1 F1914
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205403
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.16201
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118616
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.167011
G1 F1914
G2 X130.749 Y121.238 I-.023 J.054 E.00066
G1 X130.634 Y121.391 E.00187
; WIPE_START
G1 F15000
G1 X130.749 Y121.238 E-.28533
G1 X130.811 Y121.227 E-.09467
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.260614
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213842
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167071
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120299
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.6 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z6.6
G1 Z6.2
G1 E.4 F1800
; LINE_WIDTH: 0.120318
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167113
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213908
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260703
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 6.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 32/50
; update layer progress
M73 L32
M991 S0 P31 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z6.6 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z6.6
G1 Z6.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.78 Y122.797 E.06178
G1 X128 Y121.515 E.08244
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X125.983 Y123.149 E.04694
G1 X128 Y121.985 E.07488
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X126.179 Y123.489 E.04348
G1 X128 Y122.438 E.06262
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.763 Y123.749 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-.666 J-1.018 P1  F30000
G1 X122.895 Y125.626 Z6.8
G1 Z6.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.396 J-2.584 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00499
G3 X122.836 Y125.636 I.895 J2.466 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03306
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.316 J-1.035 E.08875
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.436 J-.949 E.01651
G1 X125 Y121.143 E.00417
G1 X125.055 Y121.054 E.00336
G1 X125.14 Y120.994 E.00334
G1 X125.267 Y120.97 E.00417
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.689 J2.009 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04042
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.968 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z6.8
G1 Z6.4
M73 P61 R5
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.3 J3.365 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.222 Y120.156 I1.056 J-.244 E.06169
G3 X125.99 Y120.447 I.003 J1.148 E.02699
G1 X126.614 Y121.093 E.02888
G3 X127.834 Y120.921 I1.486 J6.13 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.025 J1.621 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00336
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.589 J-.459 E.01459
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.744 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.793 Y120.156 I.744 J.804 E.02754
G3 X131.804 Y121.483 I-.045 J1.083 E.06119
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02935
G1 X132.31 Y123.318 E.01064
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01566
G1 X133.706 Y125.831 E.00498
G1 X133.747 Y125.898 E.00252
G1 X133.767 Y126 E.00334
G1 X133.722 Y126.148 E.00499
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.895 J-2.462 E.0146
G1 X132.999 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00998
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.058 Y126.805 E.02115
G1 X133.218 Y127.185 F30000
G1 F1914
G1 X132.995 Y127.241 E.00739
G1 X132.558 Y128.248 E.0353
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08856
G1 X133.276 Y127.17 E.01784
; WIPE_START
G1 F11054.348
G1 X132.995 Y127.241 E-.11018
G1 X132.712 Y127.892 E-.26982
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-.958 J-.751 P1  F30000
G1 X130.876 Y130.234 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.702 E.01565
G1 X131 Y130.857 E.00499
G1 X130.962 Y130.926 E.00252
G1 X130.884 Y130.994 E.00334
G1 X130.733 Y131.03 E.00499
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.685 J-2.006 E.01652
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.0552
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05566
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.295 J-3.362 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.055 J.244 E.08875
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.093 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18959
G1 X131.848 Y129.311 E-.10807
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G3 X125.413 Y130.975 I-2.044 J-1.639 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.567 J.453 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.255 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I.208 J1.199 P1  F30000
G1 X133.436 Y127.55 Z6.8
G1 Z6.4
G1 E.4 F1800
G1 F1914
G1 X133.288 Y127.587 E.0049
G1 X132.923 Y128.428 E.02949
G3 X132.008 Y129.751 I-5.482 J-2.815 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.02 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.425 E.02208
G3 X122.068 Y124.575 I.435 J-1.425 E.12217
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.484 J2.816 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02253
G3 X128.359 Y120.522 I1.301 J6.042 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.826 Y119.75 I1.022 J1.102 E.03848
G3 X132.201 Y121.575 I-.079 J1.489 E.08368
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08124
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.441 J1.426 E.12194
G1 X133.494 Y127.535 E.01453
G1 X133.654 Y127.915 F30000
G1 F1914
G1 X133.582 Y127.933 E.0024
G3 X132.459 Y129.848 I-5.806 J-2.116 E.07177
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13136
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.876 E.03392
G3 X121.949 Y124.185 I1.07 J-1.575 E.13732
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.236 Y119.341 I1.914 J.148 E.09107
G3 X126.547 Y119.852 I-.028 J2.011 E.04623
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.955 J1.556 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.056 J1.577 E.13771
G1 X133.712 Y127.9 E.01122
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
M73 P62 R5
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
M73 P62 R4
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.242 Y118.949 I2.166 J-.8 E.13147
G3 X127.033 Y119.791 I-.002 J2.332 E.06086
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.377 J2.268 E.19059
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22702
G1 X133.445 Y129.134 E-.15298
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z6.8
G1 Z6.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118621
G1 F1914
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.16201
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205398
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.248787
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.248747
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205368
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161989
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118609
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.166649
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28734
G1 X125.272 Y130.821 E-.09266
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.260641
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213862
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167082
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.166529
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09268
G1 X122.691 Y125.977 E-.28732
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.118629
G1 F1914
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162026
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205423
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.24882
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.249075
G1 F1914
G1 X126.812 Y121.372 E.00269
; LINE_WIDTH: 0.205604
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162133
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118661
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I.009 J1.217 P1  F30000
G1 X130.812 Y121.23 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.164399
G1 F1914
G1 X130.751 Y121.236 E.00059
G1 X130.631 Y121.389 E.00186
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28829
G1 X130.812 Y121.23 E-.09171
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.260645
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213864
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167084
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120303
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z6.8 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z6.8
G1 Z6.4
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 6.6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 33/50
; update layer progress
M73 L33
M991 S0 P32 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z6.8 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z6.8
G1 Z6.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.872 Y122.743 E.06522
G1 X128 Y121.515 E.079
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X126.076 Y123.096 E.05039
G1 X128 Y121.985 E.07144
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X126.272 Y123.435 E.04667
G1 X128 Y122.438 E.05943
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.764 Y123.751 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-.666 J-1.019 P1  F30000
G1 X122.895 Y125.626 Z7
G1 Z6.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.396 J-2.583 E.01651
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.893 J2.457 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.964 I.322 J-1.035 E.08855
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G2 X125.124 Y121.766 I161.073 J279.583 E.02404
G3 X124.985 Y121.272 I2.43 J-.947 E.01652
G1 X125 Y121.143 E.00418
G1 X125.055 Y121.054 E.00334
G1 X125.14 Y120.994 E.00336
G1 X125.267 Y120.97 E.00416
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.69 J2.011 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04042
G3 X125.711 Y120.744 I-.05 J.686 E.01489
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.346 I5.357 J3.404 E.03968
G1 X124.196 Y121.483 E.02887
G3 X125.321 Y120.157 I1.056 J-.244 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
M73 P63 R4
G1 X126.614 Y121.093 E.02889
G3 X127.834 Y120.921 I1.485 J6.123 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.04 J1.636 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.883 Y121.006 E.00335
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.572 J-.454 E.0146
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.744 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01914
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.144 J1.075 E.05802
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01566
G1 X133.669 Y125.794 E.00335
G1 X133.722 Y125.852 E.00251
G1 X133.767 Y126 E.00499
G1 X133.722 Y126.148 E.00498
G1 X133.602 Y126.247 E.00499
G3 X133.164 Y126.364 I-.894 J-2.459 E.01459
G1 X133 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.00999
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03308
G3 X133.696 Y126.645 I-.201 J.645 E.05518
G1 X133.058 Y126.805 E.02115
G1 X132.903 Y127.452 F30000
G1 F1914
G1 X132.558 Y128.248 E.02789
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02817
G3 X133.914 Y127 I-.316 J1.036 E.08533
G1 X132.995 Y127.241 E.03056
G1 X132.927 Y127.397 E.00548
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35241
G1 X132.523 Y128.311 E-.02759
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-.924 J-.791 P1  F30000
G1 X130.876 Y130.234 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01566
G1 X131.016 Y130.781 E.00252
G1 X130.989 Y130.881 E.00334
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.689 J-2.009 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.365 J-3.41 E.03968
G1 X131.804 Y130.518 E.02886
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.091 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.031 Y129.094 E-.18989
G1 X131.848 Y129.311 E-.10777
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G3 X125.413 Y130.975 I-2.039 J-1.635 E.01651
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00499
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.582 J.457 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02935
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I.189 J1.202 P1  F30000
G1 X133.227 Y127.727 Z7
G1 Z6.6
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.02458
G3 X132.008 Y129.752 I-5.519 J-2.838 E.05188
G1 X132.201 Y130.425 E.02252
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.02 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.435 J-1.425 E.12218
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.515 J2.835 E.05188
G1 X123.799 Y121.575 E.02252
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.821 Y119.75 I1.023 J1.103 E.03831
G3 X132.201 Y121.575 I-.086 J1.499 E.08365
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.933 Y124.575 E.02208
G3 X133.932 Y127.426 I-.437 J1.425 E.12211
G1 X133.288 Y127.587 E.02136
G1 X133.251 Y127.672 E.00298
G1 X133.552 Y128.002 F30000
G1 F1914
G1 X133.289 Y128.608 E.02126
G3 X132.46 Y129.849 I-5.523 J-2.795 E.0481
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.02 E.0341
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.54 Y122.151 I5.815 J2.12 E.07178
G3 X123.357 Y121.113 I2.743 J-1.02 E.0341
G3 X125.23 Y119.341 I1.914 J.148 E.0909
G3 X126.547 Y119.852 I-.023 J2.011 E.0464
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.874 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01555
G1 X133.576 Y127.947 E.00048
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G3 X132.894 Y129.942 I-5.583 J-2.114 E.05795
G3 X128.967 Y132.209 I-2.154 J.803 E.19231
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.583 J2.114 E.05795
M73 P64 R4
G3 X125.237 Y118.949 I2.166 J-.8 E.13131
G3 X127.033 Y119.791 I.003 J2.333 E.06102
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X135.77 Y125.715 I-.404 J2.302 E.0877
G3 X133.923 Y128.255 I-2.31 J.263 E.10271
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22716
G1 X133.446 Y129.134 E-.15284
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I.079 J-1.214 P1  F30000
G1 X131.794 Y129.026 Z7
G1 Z6.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118708
G1 F1914
G1 X131.667 Y129.131 E.00099
; LINE_WIDTH: 0.162292
G1 X131.54 Y129.237 E.00156
; LINE_WIDTH: 0.205875
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.249459
G1 X131.287 Y129.449 E.00269
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.248754
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205373
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161991
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.11861
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.166603
G1 F1914
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28748
G1 X125.272 Y130.821 E-.09252
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.260649
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213868
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167086
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120304
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.1665
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.0006
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09236
G1 X122.691 Y125.977 E-.28764
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I1.086 J.548 P1  F30000
G1 X124.206 Y122.974 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.118721
G1 F1914
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.162284
G1 X124.46 Y122.763 E.00156
; LINE_WIDTH: 0.205846
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.249408
G1 X124.713 Y122.551 E.00269
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.248997
G1 F1914
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205543
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.16209
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118636
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.166931
G1 F1914
G1 X130.751 Y121.236 E.0006
G2 X130.634 Y121.391 I.29 J.341 E.00191
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28927
G1 X130.811 Y121.227 E-.09073
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.260614
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213842
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167071
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120299
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z7
G1 Z6.6
G1 E.4 F1800
; LINE_WIDTH: 0.120318
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167113
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213908
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260703
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 6.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 34/50
; update layer progress
M73 L34
M991 S0 P33 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z7 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z7
G1 Z6.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X124.116 Y123.758 E.01484
G1 X125.965 Y122.69 E.06867
G1 X128 Y121.515 E.07555
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1914
G1 X126.169 Y123.042 E.05383
G1 X128 Y121.985 E.068
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G1 X126.365 Y123.382 E.04986
G1 X128 Y122.438 E.05624
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.765 Y123.753 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-.665 J-1.019 P1  F30000
G1 X122.895 Y125.626 Z7.2
G1 Z6.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1914
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.397 J-2.588 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.851 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.892 J2.454 E.01459
G1 X123.302 Y125.105 F30000
G1 F1914
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.354 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.964 I.321 J-1.035 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.433 J-.948 E.01651
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.054 E.00418
G1 X125.14 Y120.994 E.00335
G1 X125.267 Y120.97 E.00417
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.685 J2.006 E.01459
G1 X126.426 Y121.484 F30000
G1 F1914
G1 X124.875 Y122.379 E.05759
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04042
G3 X125.711 Y120.745 I-.05 J.687 E.0149
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.968 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.346 I5.318 J3.376 E.03966
G1 X124.196 Y121.483 E.02889
G3 X125.321 Y120.157 I1.056 J-.244 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.0239
G1 X126.614 Y121.093 E.02889
G3 X127.834 Y120.921 I1.485 J6.123 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
M73 P65 R4
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.038 J1.634 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00334
G1 X130.883 Y121.006 E.00335
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.585 J-.457 E.0146
G1 X131.125 Y122.379 F30000
G1 F1914
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.144 J1.075 E.05803
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02935
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X133.105 Y125.626 E.02404
G1 X133.578 Y125.745 E.01565
G1 X133.648 Y125.778 E.00251
G1 X133.722 Y125.852 E.00335
G1 X133.767 Y126 E.00499
G1 X133.722 Y126.148 E.00497
G1 X133.602 Y126.247 E.005
G3 X133.164 Y126.364 I-.893 J-2.456 E.01459
G1 X133 Y126.82 F30000
G1 F1914
G1 X132.698 Y126.895 E.01
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.645 I-.2 J.645 E.05519
G1 X133.058 Y126.805 E.02113
G1 X132.903 Y127.453 F30000
G1 F1914
G1 X132.558 Y128.248 E.02787
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.036 E.08854
G1 X132.995 Y127.241 E.02717
G1 X132.927 Y127.398 E.00549
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35219
G1 X132.522 Y128.312 E-.02781
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-.924 J-.791 P1  F30000
G1 X130.876 Y130.234 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00499
G1 X130.945 Y130.946 E.00334
G1 X130.884 Y130.994 E.00252
G1 X130.733 Y131.03 E.00499
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.682 J-2.003 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1914
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05566
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.32 J-3.378 E.03967
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.089 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08233
G1 X132.032 Y129.094 E-.18965
G1 X131.848 Y129.311 E-.10802
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G3 X125.413 Y130.975 I-2.043 J-1.639 E.01652
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.569 J.453 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1914
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I.189 J1.202 P1  F30000
G1 X133.227 Y127.727 Z7.2
G1 Z6.8
G1 E.4 F1800
G1 F1914
G1 X132.923 Y128.428 E.02456
G3 X132.008 Y129.751 I-5.496 J-2.823 E.05188
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.452 J.336 E.12217
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.019 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.017 J-1.089 E.12217
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02207
G3 X122.068 Y124.574 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.497 J2.824 E.05188
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.456 J-.329 E.12189
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.301 J6.037 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.816 Y119.749 I1.024 J1.104 E.03814
G3 X132.201 Y121.575 I-.069 J1.49 E.08402
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.436 J1.426 E.12213
G1 X133.288 Y127.587 E.02136
G1 X133.251 Y127.672 E.003
G1 X133.552 Y128.002 F30000
G1 F1914
G1 X133.289 Y128.608 E.02124
G3 X132.459 Y129.848 I-5.517 J-2.793 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.809 J2.117 E.07178
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X123.892 Y119.914 I2.026 J.186 E.04298
G3 X125.225 Y119.341 I1.362 J1.333 E.04786
G3 X126.547 Y119.852 I-.018 J2.011 E.04657
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01554
G1 X133.576 Y127.947 E.0005
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1914
M204 S5000
G3 X132.894 Y129.942 I-5.58 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19276
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.58 J2.113 E.05794
G3 X125.231 Y118.949 I2.149 J-.811 E.13148
G3 X127.033 Y119.791 I.008 J2.333 E.06118
M73 P66 R4
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X130.881 Y118.953 I1.821 J1.563 E.06428
G3 X132.893 Y122.06 I-.138 J2.294 E.12818
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.372 J2.268 E.19079
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22699
G1 X133.445 Y129.134 E-.15301
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z7.2
G1 Z6.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118651
G1 F1914
G1 X131.667 Y129.131 E.00099
; LINE_WIDTH: 0.162111
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205572
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.249032
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.248739
G1 F1914
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205362
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161985
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118608
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.1666
G1 F1914
G1 X125.25 Y130.763 E.0006
G1 X125.325 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28766
G1 X125.272 Y130.821 E-.09234
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.260641
G1 F1914
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213862
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167082
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1914
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.166551
G1 F1914
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.0006
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09233
G1 X122.691 Y125.977 E-.28767
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.11865
G1 F1914
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.162108
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205566
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.249025
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.248994
G1 F1914
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205549
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162104
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118659
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.166303
G1 F1914
G1 X130.751 Y121.236 E.0006
G1 X130.631 Y121.389 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28885
G1 X130.811 Y121.227 E-.09115
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.260613
G1 F1914
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213842
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.16707
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120299
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.2 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z7.2
G1 Z6.8
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1914
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167097
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213882
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 7
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 35/50
; update layer progress
M73 L35
M991 S0 P34 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z7.2 I.177 J-1.204 P1  F30000
G1 X124.515 Y123.527 Z7.2
G1 Z7
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1913
G1 X128 Y121.515 E.12938
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y123.758 E.14422
G1 X124.463 Y123.557 E.01291
G1 X124.719 Y123.879 F30000
G1 F1913
G1 X128 Y121.985 E.12183
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1913
M204 S5000
G1 X128 Y122.438 E.10611
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.774 Y123.766 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-.66 J-1.022 P1  F30000
G1 X122.895 Y125.626 Z7.4
G1 Z7
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1913
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.393 J-2.57 E.01652
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.892 J2.453 E.01459
G1 X123.302 Y125.105 F30000
G1 F1913
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.354 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.964 I.321 J-1.035 E.08855
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00554
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I1.067 J.584 P1  F30000
G1 X125.771 Y121.392 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.461 J-.956 E.01651
G1 X125 Y121.143 E.00418
G1 X125.055 Y121.054 E.00335
G1 X125.164 Y120.984 E.00417
G1 X125.267 Y120.97 E.00334
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.673 J1.994 E.01459
G1 X126.426 Y121.484 F30000
G1 F1913
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04042
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.3 J3.365 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.321 Y120.157 I1.056 J-.244 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.0239
G1 X126.614 Y121.093 E.02888
G3 X127.834 Y120.921 I1.486 J6.131 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-.064 J1.215 P1  F30000
G1 X130.876 Y121.766 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.046 J1.642 E.01652
G1 X130.681 Y120.979 E.00334
G1 X130.785 Y120.972 E.00335
G1 X130.884 Y121.006 E.00336
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.583 J-.457 E.0146
G1 X131.125 Y122.379 F30000
G1 F1913
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.5 E.01914
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
M73 P67 R4
G1 E-.02 F1800
G17
G3 Z7.4 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03071
G3 X131.804 Y121.483 I-.144 J1.075 E.05803
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02935
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.745 E.01565
G1 X133.706 Y125.831 E.00499
G1 X133.766 Y125.974 E.00499
G1 X133.762 Y126.052 E.00251
G1 X133.722 Y126.148 E.00335
G1 X133.602 Y126.247 E.00499
G3 X133.164 Y126.364 I-.894 J-2.461 E.0146
G1 X133 Y126.82 F30000
G1 F1913
G1 X132.698 Y126.895 E.01002
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.059 Y126.805 E.02111
G1 X133.219 Y127.185 F30000
G1 F1913
G1 X132.995 Y127.241 E.00744
G1 X132.558 Y128.248 E.0353
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.036 E.08855
G1 X133.277 Y127.17 E.01779
; WIPE_START
G1 F11054.348
G1 X132.995 Y127.241 E-.11071
G1 X132.713 Y127.891 E-.26929
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-.958 J-.751 P1  F30000
G1 X130.876 Y130.235 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X131.01 Y130.702 E.01565
G1 X131 Y130.857 E.00499
G1 X130.945 Y130.946 E.00335
G1 X130.883 Y130.994 E.00253
G1 X130.733 Y131.03 E.00497
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.675 J-1.996 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1913
G1 X131.407 Y130.61 E.03306
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I1.138 J.432 P1  F30000
G1 X132.183 Y128.54 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.294 J-3.36 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.057 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.094 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08233
G1 X132.032 Y129.094 E-.18958
G1 X131.848 Y129.311 E-.10809
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G3 X125.412 Y130.975 I-2.039 J-1.635 E.01652
G1 X125.268 Y131.03 E.00498
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.582 J.457 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1913
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02935
G1 X123.69 Y128.682 E.01064
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I.208 J1.199 P1  F30000
G1 X133.437 Y127.55 Z7.4
G1 Z7
G1 E.4 F1800
G1 F1913
G1 X133.288 Y127.587 E.00494
G1 X132.923 Y128.428 E.02948
G3 X132.008 Y129.751 I-5.482 J-2.815 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.33 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.021 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.435 J-1.425 E.12218
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02949
G3 X123.992 Y122.249 I5.485 J2.817 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.15 I1.452 J-.336 E.12217
G1 X126.756 Y120.653 E.02253
G3 X128.359 Y120.522 I1.301 J6.042 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.811 Y119.749 I1.024 J1.106 E.03796
G3 X132.201 Y121.575 I-.076 J1.5 E.084
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.574 E.02208
G3 X133.932 Y127.426 I-.443 J1.426 E.1219
G1 X133.495 Y127.535 E.01448
G1 X133.552 Y128.003 F30000
G1 F1913
G1 X133.289 Y128.608 E.02123
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X125.22 Y119.341 I1.915 J.148 E.09056
G3 X126.547 Y119.852 I-.012 J2.011 E.04674
G1 X126.897 Y120.214 E.01618
G3 X129.117 Y120.2 I1.149 J6.075 E.07178
G3 X130.082 Y119.461 I1.957 J1.558 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.489 J2.876 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01554
G1 X133.575 Y127.948 E.00051
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1913
M204 S5000
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.226 Y118.949 I2.166 J-.8 E.131
G3 X127.033 Y119.791 I.012 J2.334 E.06134
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19048
; WIPE_START
M73 P68 R4
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22704
G1 X133.446 Y129.134 E-.15296
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z7.4
G1 Z7
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118621
G1 F1913
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.16201
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205399
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.248788
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.248794
G1 F1913
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205398
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.162003
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118607
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.16636
G1 F1913
G1 X125.25 Y130.763 E.0006
G1 X125.325 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28754
G1 X125.272 Y130.821 E-.09246
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.260649
G1 F1913
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213868
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167086
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120304
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1913
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.166458
G1 F1913
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.0006
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09242
G1 X122.691 Y125.977 E-.28758
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.118629
G1 F1913
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162026
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205422
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.248819
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.24908
G1 F1913
G1 X126.812 Y121.372 E.00269
; LINE_WIDTH: 0.205608
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162135
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118663
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.166247
G1 F1913
G1 X130.751 Y121.236 E.0006
G1 X130.631 Y121.389 E.00189
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28887
G1 X130.811 Y121.227 E-.09113
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.260614
G1 F1913
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213842
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167071
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120299
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.4 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z7.4
G1 Z7
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1913
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167097
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213883
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 7.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 36/50
; update layer progress
M73 L36
M991 S0 P35 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z7.4 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z7.4
G1 Z7.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X124.116 Y123.758 E.01484
G1 X126.151 Y122.583 E.07555
G1 X128 Y121.515 E.06867
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1915
G1 X126.354 Y122.935 E.06072
G1 X128 Y121.985 E.06111
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G1 X126.55 Y123.275 E.05624
G1 X128 Y122.438 E.04986
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.767 Y123.756 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I1.217 J.002 P1  F30000
G1 X125.771 Y121.392 Z7.6
G1 Z7.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.449 J-.952 E.01652
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.054 E.00417
G1 X125.164 Y120.984 E.00417
G1 X125.267 Y120.97 E.00335
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.681 J2.002 E.01459
G1 X126.426 Y121.484 F30000
G1 F1915
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03306
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.01489
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.968 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.347 I5.305 J3.368 E.03966
G1 X124.196 Y121.483 E.02889
G3 X125.321 Y120.157 I1.056 J-.244 E.06486
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.482 J6.087 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.397 J-2.588 E.01651
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.896 J2.467 E.01459
G1 X123.302 Y125.105 F30000
G1 F1915
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.037 J1.633 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.884 Y121.006 E.00335
G1 X130.962 Y121.074 E.00334
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.582 J-.457 E.01459
G1 X131.125 Y122.379 F30000
G1 F1915
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
M73 P69 R4
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03073
G3 X131.804 Y121.483 I-.145 J1.075 E.05802
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02935
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.745 E.01565
G1 X133.706 Y125.831 E.00499
G1 X133.766 Y125.974 E.00498
G1 X133.755 Y126.077 E.00334
G1 X133.722 Y126.148 E.00252
G1 X133.602 Y126.247 E.00499
G3 X133.164 Y126.364 I-.894 J-2.46 E.01459
G1 X133.001 Y126.82 F30000
G1 F1915
G1 X132.698 Y126.895 E.01003
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03306
G3 X133.696 Y126.646 I-.2 J.646 E.0552
G1 X133.059 Y126.805 E.0211
G1 X132.902 Y127.453 F30000
G1 F1915
G1 X132.558 Y128.248 E.02785
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.964 E.02816
G3 X133.814 Y127.036 I-.321 J1.036 E.08855
G1 X132.995 Y127.241 E.02717
G1 X132.926 Y127.398 E.00553
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35185
G1 X132.522 Y128.313 E-.02815
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.234 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X131.01 Y130.703 E.01566
G1 X131.016 Y130.781 E.00252
G1 X130.989 Y130.881 E.00334
G1 X130.883 Y130.994 E.00499
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.674 J-1.995 E.01652
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1915
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.308 J-3.37 E.03966
G1 X131.804 Y130.518 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.094 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.1896
G1 X131.848 Y129.311 E-.10806
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G3 X125.412 Y130.975 I-2.043 J-1.638 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.117 Y130.994 E.00498
G1 X125.011 Y130.881 E.00499
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.582 J.457 E.01651
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1915
G1 X125.711 Y131.255 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I.189 J1.202 P1  F30000
G1 X133.227 Y127.728 Z7.6
G1 Z7.2
G1 E.4 F1800
G1 F1915
G1 X132.923 Y128.428 E.02453
G3 X132.008 Y129.751 I-5.487 J-2.819 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.021 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08123
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02136
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.487 J2.818 E.05187
G1 X123.799 Y121.575 E.02254
G3 X125.347 Y119.75 I1.454 J-.336 E.08928
G3 X126.268 Y120.15 I-.11 J1.515 E.03289
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.019 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.574 E.02208
G3 X133.932 Y127.426 I-.435 J1.426 E.12218
G1 X133.288 Y127.587 E.02136
G1 X133.251 Y127.673 E.00303
G1 X133.551 Y128.003 F30000
G1 F1915
G1 X133.289 Y128.608 E.02121
G3 X132.459 Y129.848 I-5.514 J-2.792 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
M73 P69 R3
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.489 J-2.876 E.03392
G3 X121.949 Y124.185 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01555
G3 X123.541 Y122.152 I5.807 J2.116 E.07178
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X125.214 Y119.341 I1.915 J.149 E.09039
G3 X126.547 Y119.852 I-.007 J2.012 E.04691
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.666 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.489 J2.875 E.03392
G3 X134.051 Y127.816 I-1.055 J1.577 E.13773
G1 X133.582 Y127.933 E.01554
G1 X133.575 Y127.948 E.00053
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.113 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19228
G3 X123.106 Y122.058 I5.579 J2.112 E.05794
G3 X125.221 Y118.949 I2.166 J-.8 E.13084
G3 X127.033 Y119.791 I.017 J2.335 E.0615
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X130.87 Y118.952 I1.822 J1.565 E.06396
G3 X132.893 Y122.06 I-.128 J2.295 E.1285
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.378 J2.268 E.19056
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22703
M73 P70 R3
G1 X133.445 Y129.134 E-.15297
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z7.6
G1 Z7.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118622
G1 F1915
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162045
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205469
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248893
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.248784
G1 F1915
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205391
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.161998
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118605
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.166677
G1 F1915
G1 X125.25 Y130.763 E.0006
G1 X125.326 Y130.586 E.00189
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.2878
G1 X125.272 Y130.821 E-.0922
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.260642
G1 F1915
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213862
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167083
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1915
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167097
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213882
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260668
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I1.072 J-.575 P1  F30000
G1 X122.691 Y125.977 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.166483
G1 F1915
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09258
G1 X122.691 Y125.977 E-.28742
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.118619
G1 F1915
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.16204
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205462
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.248883
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.248712
G1 F1915
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205343
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161973
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118603
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.165652
G1 F1915
G1 X130.75 Y121.237 E.0006
G1 X130.626 Y121.386 E.00188
; WIPE_START
G1 F15000
G1 X130.75 Y121.237 E-.28786
G1 X130.811 Y121.227 E-.09214
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.260614
G1 F1915
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213842
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167071
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120299
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.6 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z7.6
G1 Z7.2
G1 E.4 F1800
; LINE_WIDTH: 0.120312
G1 F1915
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167097
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213883
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260668
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 7.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 37/50
; update layer progress
M73 L37
M991 S0 P36 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z7.6 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z7.6
G1 Z7.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X124.116 Y123.758 E.01484
G1 X126.243 Y122.529 E.079
G1 X128 Y121.515 E.06522
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1915
G1 X126.447 Y122.882 E.06416
G1 X128 Y121.985 E.05767
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G1 X126.643 Y123.221 E.05943
G1 X128 Y122.438 E.04667
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.768 Y123.757 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I1.217 J.001 P1  F30000
G1 X125.771 Y121.392 Z7.8
G1 Z7.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G3 X125.124 Y121.766 I-157.124 J-271.242 E.02403
G3 X124.985 Y121.272 I2.424 J-.945 E.01651
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.054 E.00417
G1 X125.164 Y120.984 E.00417
G1 X125.267 Y120.97 E.00335
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.345 I-1.687 J2.007 E.01458
G1 X126.426 Y121.484 F30000
G1 F1915
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.744 I-.05 J.686 E.01489
G1 X126.385 Y121.44 E.03115
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.346 I5.311 J3.372 E.03966
G1 X124.196 Y121.483 E.02889
G3 X125.321 Y120.157 I1.056 J-.244 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.02891
G3 X127.834 Y120.921 I1.483 J6.093 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.4 J-2.6 E.01651
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.89 J2.446 E.01459
G1 X123.302 Y125.105 F30000
G1 F1915
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.322 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.044 J1.639 E.01652
G1 X130.681 Y120.979 E.00334
G1 X130.785 Y120.972 E.00335
G1 X130.884 Y121.006 E.00336
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00334
G3 X130.897 Y121.71 I-2.57 J-.453 E.01459
G1 X131.125 Y122.379 F30000
G1 F1915
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.5 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.144 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z7.8
G1 Z7.4
M73 P71 R3
G1 E.4 F1800
G1 F1915
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01565
G1 X133.706 Y125.83 E.00497
G1 X133.766 Y125.974 E.00499
G1 X133.756 Y126.077 E.00334
G1 X133.722 Y126.148 E.00252
G1 X133.602 Y126.247 E.00499
G3 X133.164 Y126.364 I-.89 J-2.443 E.01459
G1 X133.001 Y126.819 F30000
G1 F1915
G1 X132.698 Y126.895 E.01005
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.646 I-.2 J.645 E.0552
G1 X133.06 Y126.805 E.02109
G1 X132.902 Y127.454 F30000
G1 F1915
G1 X132.558 Y128.248 E.02783
G1 X132.474 Y128.399 E.00554
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08855
G1 X132.995 Y127.241 E.02717
G1 X132.926 Y127.399 E.00554
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35164
G1 X132.522 Y128.313 E-.02836
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.234 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00499
G1 X130.905 Y130.98 E.00498
G1 X130.836 Y131.016 E.00252
G1 X130.733 Y131.03 E.00335
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.689 J-2.009 E.01652
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1915
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.307 J-3.369 E.03966
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.088 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08233
G1 X132.032 Y129.094 E-.18959
G1 X131.848 Y129.311 E-.10808
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G3 X125.413 Y130.975 I-2.043 J-1.638 E.01651
G1 X125.268 Y131.03 E.00499
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.729 E.00498
G3 X125.124 Y130.235 I2.564 J.452 E.01652
G1 X125.719 Y130.578 E.0221
G1 X126.426 Y130.516 F30000
G1 F1915
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.876 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I.189 J1.202 P1  F30000
G1 X133.227 Y127.729 Z7.8
G1 Z7.4
G1 E.4 F1800
G1 F1915
G1 X132.923 Y128.428 E.02451
G3 X132.008 Y129.751 I-5.488 J-2.819 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.019 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02135
G1 X123.077 Y123.572 E.02948
G3 X123.992 Y122.249 I5.49 J2.82 E.05187
G1 X123.799 Y121.575 E.02254
G3 X126.268 Y120.149 I1.456 J-.33 E.12188
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.021 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.944 Y119.76 I1.024 J1.105 E.04229
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.426 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.25 Y127.674 E.00304
G1 X133.551 Y128.004 F30000
G1 F1915
G1 X133.289 Y128.608 E.0212
G3 X132.459 Y129.848 I-5.515 J-2.792 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.899 J-.139 E.13732
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.808 J2.117 E.07178
G3 X123.357 Y121.113 I2.743 J-1.021 E.03411
G3 X125.209 Y119.341 I1.916 J.149 E.09023
G3 X126.547 Y119.852 I-.002 J2.013 E.04708
G1 X126.897 Y120.214 E.0162
G3 X129.117 Y120.2 I1.149 J6.071 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.055 J1.577 E.13774
G1 X133.582 Y127.933 E.01554
G1 X133.575 Y127.949 E.00055
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G3 X132.894 Y129.942 I-5.579 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19276
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.579 J2.112 E.05794
G3 X125.215 Y118.949 I2.167 J-.8 E.13069
G3 X127.033 Y119.791 I.022 J2.335 E.06166
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.378 J2.268 E.19055
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22703
G1 X133.445 Y129.134 E-.15297
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z7.8
G1 Z7.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118626
G1 F1915
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162059
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205491
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248923
M73 P72 R3
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.248741
G1 F1915
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205363
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161985
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118608
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.16617
G1 F1915
G1 X125.25 Y130.763 E.0006
G1 X125.325 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28747
G1 X125.272 Y130.821 E-.09253
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.260674
G1 F1915
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213885
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167096
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120308
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1915
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.166518
G1 F1915
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09265
G1 X122.691 Y125.977 E-.28735
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.118632
G1 F1915
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.162069
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205507
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.248945
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.248772
G1 F1915
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205385
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.161999
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118612
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I.011 J1.217 P1  F30000
G1 X130.811 Y121.227 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.167125
G1 F1915
G2 X130.749 Y121.238 I-.023 J.055 E.00065
G1 X130.634 Y121.391 E.00187
; WIPE_START
G1 F15000
G1 X130.749 Y121.238 E-.28539
G1 X130.811 Y121.227 E-.09461
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.260619
G1 F1915
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213846
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167073
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.1203
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z7.8 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z7.8
G1 Z7.4
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1915
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 7.6
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 38/50
; update layer progress
M73 L38
M991 S0 P37 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z7.8 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z7.8
G1 Z7.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X124.116 Y123.758 E.01484
G1 X126.336 Y122.476 E.08244
G1 X128 Y121.515 E.06178
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1915
G1 X126.54 Y122.828 E.06761
G1 X128 Y121.985 E.05422
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G1 X126.736 Y123.168 E.06262
G1 X128 Y122.438 E.04348
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.769 Y123.758 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I1.217 J.001 P1  F30000
G1 X125.771 Y121.392 Z8
G1 Z7.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.43 J-.947 E.01651
G1 X124.992 Y121.168 E.00336
G1 X125.055 Y121.054 E.00417
G1 X125.14 Y120.994 E.00335
G1 X125.267 Y120.97 E.00417
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.682 J2.002 E.01459
G1 X126.426 Y121.484 F30000
G1 F1915
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.384 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.271 J3.344 E.03965
G1 X124.196 Y121.483 E.02891
G3 X125.321 Y120.157 I1.056 J-.244 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.0239
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.482 J6.089 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.397 J-2.585 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.894 J2.458 E.0146
G1 X123.302 Y125.105 F30000
G1 F1915
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.322 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.038 J1.633 E.01651
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00336
G1 X130.884 Y121.006 E.00335
G1 X130.962 Y121.075 E.00336
G1 X131.008 Y121.168 E.00333
G1 X131.015 Y121.272 E.00336
G3 X130.897 Y121.71 I-2.585 J-.458 E.01459
G1 X131.125 Y122.379 F30000
G1 F1915
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.744 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.144 J1.075 E.05802
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02935
G1 X132.31 Y123.318 E.01064
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.744 E.01564
G1 X133.706 Y125.831 E.00499
G1 X133.766 Y125.974 E.00499
G1 X133.755 Y126.078 E.00335
G1 X133.722 Y126.148 E.00252
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.889 J-2.442 E.0146
G1 X133.002 Y126.819 F30000
G1 F1915
G1 X132.698 Y126.895 E.01006
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.354 E.03306
G3 X133.696 Y126.645 I-.2 J.646 E.0552
G1 X133.06 Y126.805 E.02108
M73 P73 R3
G1 X132.902 Y127.454 F30000
G1 F1915
G1 X132.558 Y128.248 E.0278
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.964 E.02815
G3 X133.814 Y127.036 I-.321 J1.036 E.08855
G1 X132.995 Y127.241 E.02717
G1 X132.926 Y127.399 E.00556
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35137
G1 X132.521 Y128.314 E-.02863
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.234 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00498
G1 X130.962 Y130.926 E.00252
G1 X130.883 Y130.994 E.00335
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.005
G3 X130.229 Y130.608 I1.686 J-2.006 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1915
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.0552
G1 X129.574 Y130.516 E.03307
G1 X131.073 Y129.651 E.05566
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.272 J-3.345 E.03965
G1 X131.804 Y130.517 E.02891
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.092 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08233
G1 X132.032 Y129.093 E-.18944
G1 X131.848 Y129.311 E-.10822
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G3 X125.413 Y130.975 I-2.049 J-1.644 E.01651
G1 X125.267 Y131.03 E.00499
G1 X125.117 Y130.994 E.00497
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.235 I2.581 J.457 E.01652
G1 X125.719 Y130.578 E.0221
G1 X126.426 Y130.516 F30000
G1 F1915
G1 X125.711 Y131.255 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.876 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02716
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I.208 J1.199 P1  F30000
G1 X133.439 Y127.549 Z8
G1 Z7.6
G1 E.4 F1800
G1 F1915
G1 X133.288 Y127.587 E.00499
G1 X132.923 Y128.428 E.02948
G3 X132.008 Y129.75 I-5.47 J-2.808 E.05186
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.021 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02135
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.25 I5.47 J2.808 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.15 I1.456 J-.329 E.12189
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.021 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02135
G3 X130.945 Y119.76 I1.024 J1.105 E.0423
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.574 E.02207
G3 X133.932 Y127.426 I-.442 J1.426 E.1219
G1 X133.497 Y127.535 E.01443
G1 X133.551 Y128.004 F30000
G1 F1915
G1 X133.289 Y128.608 E.02118
G3 X132.459 Y129.848 I-5.51 J-2.79 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.744 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.072 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.07 J-1.575 E.13733
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.803 J2.114 E.07177
G3 X123.357 Y121.113 I2.744 J-1.021 E.03412
G3 X125.204 Y119.341 I1.916 J.149 E.09006
G3 X126.547 Y119.852 I.003 J2.013 E.04726
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.071 E.07177
G3 X130.082 Y119.461 I1.956 J1.556 E.03946
G3 X132.598 Y121.668 I.665 J1.779 E.13166
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.422 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.054 J1.577 E.13775
G1 X133.582 Y127.933 E.01554
G1 X133.575 Y127.949 E.00056
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G3 X132.894 Y129.942 I-5.577 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.369 J-2.268 E.19272
G3 X123.106 Y122.058 I5.577 J2.112 E.05794
G3 X125.21 Y118.949 I2.167 J-.8 E.13053
G3 X127.033 Y119.791 I.027 J2.336 E.06182
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X130.86 Y118.951 I1.824 J1.568 E.06365
G3 X132.893 Y122.06 I-.117 J2.296 E.12882
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.378 J2.268 E.19054
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22703
G1 X133.446 Y129.134 E-.15297
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z8
G1 Z7.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118585
G1 F1915
G1 X131.666 Y129.132 E.00098
; LINE_WIDTH: 0.161908
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205232
G1 X131.413 Y129.343 E.00211
; LINE_WIDTH: 0.248555
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.248786
G1 F1915
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205395
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.162005
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118615
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-.015 J-1.217 P1  F30000
G1 X125.192 Y130.785 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.167241
M73 P74 R3
G1 F1915
G1 X125.25 Y130.763 E.0006
G1 X125.326 Y130.586 E.00189
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28801
G1 X125.192 Y130.785 E-.09199
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I1.144 J-.415 P1  F30000
G1 X124.71 Y129.459 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.260684
G1 F1915
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213892
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167101
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120309
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1915
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.167218
G1 F1915
G1 X122.438 Y126.005 E.0025
; WIPE_START
G1 F15000
G1 X122.691 Y125.977 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.118581
G1 F1915
G1 X124.334 Y122.868 E.00098
; LINE_WIDTH: 0.161899
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205216
G1 X124.587 Y122.657 E.00211
; LINE_WIDTH: 0.248534
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.248756
G1 F1915
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205374
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.161992
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.11861
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I.009 J1.217 P1  F30000
G1 X130.812 Y121.23 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.164283
G1 F1915
G1 X130.751 Y121.236 E.00059
G1 X130.63 Y121.389 E.00186
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28823
G1 X130.812 Y121.23 E-.09177
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.26065
G1 F1915
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213868
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167086
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120304
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z8
G1 Z7.6
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1915
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 7.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 39/50
; update layer progress
M73 L39
M991 S0 P38 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z8 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z8
G1 Z7.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1916
G1 X124.116 Y123.758 E.01484
G1 X126.429 Y122.422 E.08589
G1 X128 Y121.515 E.05834
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1916
G1 X126.632 Y122.775 E.07105
G1 X128 Y121.985 E.05078
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1916
M204 S5000
G1 X126.828 Y123.114 E.06581
G1 X128 Y122.438 E.04029
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.769 Y123.759 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I1.217 J.001 P1  F30000
G1 X125.771 Y121.392 Z8.2
G1 Z7.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1916
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.41 J-.941 E.01651
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.055 E.00417
G1 X125.14 Y120.994 E.00335
G1 X125.267 Y120.97 E.00417
G1 X125.413 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.674 J1.995 E.01459
G1 X126.426 Y121.484 F30000
G1 F1916
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03306
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.293 J3.36 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.321 Y120.157 I1.056 J-.244 E.06486
G3 X125.99 Y120.447 I-.08 J1.101 E.0239
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.482 J6.089 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.396 J-2.583 E.01652
G1 X122.278 Y126.148 E.00498
G1 X122.233 Y126 E.00499
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.896 J2.469 E.01459
G1 X123.302 Y125.105 F30000
G1 F1916
G1 X123.302 Y126.895 E.05757
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.098 E.01063
G1 X123.035 Y127.248 E.02937
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.321 J-1.035 E.08855
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.0353
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.04 J1.635 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.883 Y121.006 E.00335
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.585 J-.457 E.0146
G1 X131.125 Y122.379 F30000
G1 F1916
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.744 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01914
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.144 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.745 E.01565
G1 X133.706 Y125.831 E.00499
G1 X133.766 Y125.974 E.00499
G1 X133.755 Y126.077 E.00335
G1 X133.722 Y126.148 E.00252
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.894 J-2.458 E.0146
G1 X133.002 Y126.819 F30000
G1 F1916
G1 X132.698 Y126.895 E.01008
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03306
G3 X133.696 Y126.645 I-.2 J.645 E.0552
G1 X133.06 Y126.805 E.02106
G1 X133.221 Y127.184 F30000
G1 F1916
G1 X132.995 Y127.241 E.00751
G1 X132.558 Y128.248 E.0353
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
M73 P75 R3
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.035 E.08855
G1 X133.279 Y127.169 E.01773
; WIPE_START
G1 F11054.348
G1 X132.995 Y127.241 E-.11152
G1 X132.713 Y127.889 E-.26848
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-.958 J-.75 P1  F30000
G1 X130.876 Y130.235 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X131.01 Y130.703 E.01566
G1 X131.016 Y130.781 E.00251
G1 X130.989 Y130.881 E.00335
G1 X130.883 Y130.994 E.00498
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.689 J-2.01 E.01652
G1 X130.824 Y130.265 E.02211
G1 X131.124 Y129.621 F30000
G1 F1916
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.072 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.318 J-3.377 E.03967
G1 X131.804 Y130.518 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.091 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18964
G1 X131.848 Y129.311 E-.10802
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G3 X125.412 Y130.975 I-2.035 J-1.631 E.01652
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.235 I2.579 J.457 E.01651
G1 X125.719 Y130.578 E.0221
G1 X126.426 Y130.516 F30000
G1 F1916
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05518
G1 X124.876 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.518 I-.736 J-.796 E.08853
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02937
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I.189 J1.202 P1  F30000
G1 X133.226 Y127.73 Z8.2
G1 Z7.8
G1 E.4 F1800
G1 F1916
G1 X132.923 Y128.428 E.02447
G3 X132.008 Y129.751 I-5.493 J-2.822 E.05188
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.02 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12188
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.556 J-4.079 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.443 J-1.425 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.48 J2.814 E.05187
G1 X123.799 Y121.575 E.02255
G3 X126.268 Y120.15 I1.456 J-.329 E.12189
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.019 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X130.944 Y119.76 I1.024 J1.105 E.04229
G3 X132.201 Y121.575 I-.199 J1.48 E.07988
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.442 J1.425 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.25 Y127.675 E.00308
G1 X133.658 Y127.914 F30000
G1 F1916
G1 X133.582 Y127.933 E.00251
G3 X132.459 Y129.848 I-5.808 J-2.117 E.07178
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.741 J1.02 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.665 J-1.779 E.13166
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.329 J-3.778 E.07165
G3 X121.446 Y127.578 I.488 J-2.874 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X126.547 Y119.852 I1.895 J.128 E.13765
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.071 E.07177
G3 X130.082 Y119.461 I1.956 J1.556 E.03946
G3 X130.823 Y119.342 I.685 J1.887 E.02428
G3 X132.598 Y121.668 I-.092 J1.911 E.10712
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.422 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.07 J1.575 E.13733
G1 X133.716 Y127.899 E.01111
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1916
M204 S5000
G3 X132.894 Y129.942 I-5.58 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.775 J-1.458 E.19272
G3 X122.141 Y128.268 I4.111 J-3.488 E.05783
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.577 J2.111 E.05794
G3 X125.205 Y118.949 I2.151 J-.811 E.13069
G3 X127.033 Y119.791 I.032 J2.337 E.06198
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X132.893 Y122.06 I1.775 J1.458 E.19272
G3 X133.859 Y123.732 I-4.111 J3.488 E.05782
G3 X133.924 Y128.256 I-.369 J2.268 E.19093
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22694
G1 X133.445 Y129.134 E-.15306
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z8.2
G1 Z7.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118646
G1 F1916
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162103
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.20556
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.249018
G1 X131.287 Y129.449 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.248742
G1 F1916
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205364
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161986
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118608
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.166693
G1 F1916
G1 X125.25 Y130.763 E.00061
G1 X125.325 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28752
G1 X125.272 Y130.821 E-.09248
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.260665
G1 F1916
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213879
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167093
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120307
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z8.2
G1 Z7.8
M73 P76 R3
G1 E.4 F1800
; LINE_WIDTH: 0.120313
G1 F1916
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167103
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213894
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.166643
G1 F1916
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09258
G1 X122.691 Y125.977 E-.28742
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.118615
G1 F1916
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.161995
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205374
G1 X124.586 Y122.657 E.00211
; LINE_WIDTH: 0.248754
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.248713
G1 F1916
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205343
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161974
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118604
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I.017 J1.217 P1  F30000
G1 X130.805 Y121.206 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.165648
G1 F1916
G1 X130.751 Y121.236 E.00059
G2 X130.634 Y121.391 I.29 J.341 E.0019
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.2891
G1 X130.805 Y121.206 E-.0909
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-1.144 J.416 P1  F30000
G1 X131.29 Y122.542 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.260619
G1 F1916
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213846
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167073
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.1203
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.2 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z8.2
G1 Z7.8
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1916
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 40/50
; update layer progress
M73 L40
M991 S0 P39 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z8.2 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z8.2
G1 Z8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X124.116 Y123.758 E.01484
G1 X126.522 Y122.369 E.08933
G1 X128 Y121.515 E.05489
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1915
G1 X126.725 Y122.721 E.07449
G1 X128 Y121.985 E.04734
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G1 X126.921 Y123.061 E.069
G1 X128 Y122.438 E.0371
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.77 Y123.76 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I1.217 J.001 P1  F30000
G1 X125.771 Y121.392 Z8.4
G1 Z8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X125.124 Y121.766 E.02403
G3 X124.985 Y121.272 I2.444 J-.951 E.01651
G1 X124.992 Y121.168 E.00335
G1 X125.055 Y121.054 E.00418
G1 X125.164 Y120.984 E.00417
G1 X125.267 Y120.97 E.00335
G1 X125.412 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.673 J1.993 E.0146
G1 X126.426 Y121.484 F30000
G1 F1915
G1 X124.875 Y122.379 E.05757
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04042
G3 X125.711 Y120.744 I-.05 J.686 E.01489
G1 X126.384 Y121.441 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.346 I5.311 J3.372 E.03966
G1 X124.196 Y121.483 E.02889
G3 X125.321 Y120.157 I1.056 J-.243 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.614 Y121.093 E.0289
G3 X127.834 Y120.921 I1.483 J6.091 E.03967
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.393 J-2.573 E.01651
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.851 E.00499
G1 X122.398 Y125.753 E.00497
G3 X122.836 Y125.636 I.897 J2.469 E.0146
G1 X123.302 Y125.105 F30000
G1 F1915
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.646 E.03306
G3 X122.304 Y125.355 I.2 J-.646 E.0552
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01064
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02815
G3 X122.186 Y124.965 I.321 J-1.036 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.041 J1.637 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.587 J-.458 E.01459
G1 X131.125 Y122.379 F30000
G1 F1915
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.744 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05802
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.744 E.01564
G1 X133.706 Y125.831 E.00499
G1 X133.766 Y125.974 E.00499
G1 X133.756 Y126.077 E.00334
G1 X133.722 Y126.149 E.00254
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.893 J-2.455 E.01459
G1 X133.003 Y126.819 F30000
G1 F1915
G1 X132.698 Y126.895 E.01009
G1 X132.698 Y125.104 E.05759
G1 X133.696 Y125.354 E.03306
G3 X133.696 Y126.646 I-.2 J.646 E.05521
G1 X133.061 Y126.804 E.02104
G1 X132.901 Y127.456 F30000
G1 F1915
G1 X132.558 Y128.248 E.02777
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01064
G1 X132.965 Y124.752 E.02935
G1 X133.814 Y124.964 E.02815
G3 X133.814 Y127.036 I-.321 J1.036 E.08856
G1 X132.995 Y127.241 E.02716
G1 X132.925 Y127.4 E.0056
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35095
G1 X132.521 Y128.315 E-.02905
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.235 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
M73 P77 R3
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00499
G1 X130.905 Y130.98 E.00498
G1 X130.811 Y131.023 E.00335
G1 X130.733 Y131.03 E.00252
G1 X130.588 Y130.975 E.00498
G3 X130.229 Y130.608 I1.695 J-2.014 E.01652
G1 X130.824 Y130.265 E.0221
G1 X131.125 Y129.621 F30000
G1 F1915
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.516 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.311 J-3.372 E.03966
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.057 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.088 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08233
G1 X132.032 Y129.094 E-.18965
G1 X131.848 Y129.311 E-.10802
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G3 X125.413 Y130.975 I-2.046 J-1.641 E.01651
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.235 I2.577 J.456 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1915
G1 X125.711 Y131.255 E.03306
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02716
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I.208 J1.199 P1  F30000
M73 P77 R2
G1 X133.44 Y127.549 Z8.4
G1 Z8
G1 E.4 F1800
G1 F1915
G1 X133.288 Y127.587 E.00503
G1 X132.923 Y128.428 E.02948
G3 X132.008 Y129.751 I-5.491 J-2.821 E.05188
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.019 E.05188
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02135
G3 X123.799 Y130.425 I-1.013 J-1.096 E.1219
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02207
G3 X122.068 Y124.575 I.442 J-1.426 E.1219
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.49 J2.82 E.05188
G1 X123.799 Y121.575 E.02254
G3 X125.347 Y119.75 I1.454 J-.335 E.08928
G3 X126.268 Y120.15 I-.11 J1.515 E.03289
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.021 E.05188
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.56 J4.081 E.08123
G1 X133.932 Y124.574 E.02207
G3 X133.932 Y127.426 I-.442 J1.426 E.1219
G1 X133.498 Y127.534 E.0144
G1 X133.551 Y128.005 F30000
G1 F1915
G1 X133.289 Y128.608 E.02114
G3 X132.459 Y129.848 I-5.516 J-2.792 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.15 J-6.07 E.07178
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13136
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.874 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.808 J2.117 E.07178
G3 X123.357 Y121.113 I2.742 J-1.021 E.03411
G3 X125.374 Y119.344 I1.914 J.148 E.09553
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.15 J6.071 E.07178
G3 X130.082 Y119.461 I1.956 J1.556 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.333 J3.78 E.07164
G3 X134.554 Y124.423 I-.489 J2.877 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01554
G1 X133.574 Y127.95 E.0006
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G3 X132.894 Y129.942 I-5.58 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.149 J.812 E.19276
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.58 J2.113 E.05794
G3 X125.199 Y118.949 I2.168 J-.8 E.13022
G3 X127.033 Y119.791 I.037 J2.337 E.06214
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.923 E.05349
G3 X130.849 Y118.95 I1.826 J1.571 E.06333
G3 X132.893 Y122.06 I-.124 J2.308 E.12884
G3 X133.859 Y123.732 I-4.114 J3.49 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22704
G1 X133.446 Y129.134 E-.15296
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z8.4
G1 Z8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118635
G1 F1915
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162079
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205523
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248967
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.248787
G1 F1915
G1 X129.188 Y130.627 E.00268
; LINE_WIDTH: 0.205396
G1 X129.034 Y130.684 E.00212
; LINE_WIDTH: 0.162005
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118615
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.166474
G1 F1915
G1 X125.25 Y130.763 E.0006
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28762
G1 X125.272 Y130.821 E-.09238
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.260656
G1 F1915
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213872
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167088
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120305
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.120319
G1 F1915
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.16712
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.21392
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.26072
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.166399
G1 F1915
M73 P78 R2
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.0006
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09234
G1 X122.691 Y125.977 E-.28766
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.118632
G1 F1915
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.162069
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205506
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.248944
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.24882
G1 F1915
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.20542
G1 X126.966 Y121.316 E.00212
; LINE_WIDTH: 0.16202
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118619
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I.017 J1.217 P1  F30000
G1 X130.805 Y121.207 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.164871
G1 F1915
G1 X130.751 Y121.236 E.00059
G1 X130.63 Y121.389 E.00187
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28857
G1 X130.805 Y121.207 E-.09143
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-1.144 J.416 P1  F30000
G1 X131.29 Y122.542 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.260615
G1 F1915
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213843
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167072
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.1203
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.4 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z8.4
G1 Z8
G1 E.4 F1800
; LINE_WIDTH: 0.120325
G1 F1915
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167112
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213899
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260687
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 8.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 41/50
; update layer progress
M73 L41
M991 S0 P40 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z8.4 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z8.4
G1 Z8.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1924
G1 X124.116 Y123.758 E.01484
G1 X126.614 Y122.315 E.09277
G1 X128 Y121.515 E.05145
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1924
G1 X126.818 Y122.668 E.07794
G1 X128 Y121.985 E.04389
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1924
M204 S5000
G1 X127.014 Y123.007 E.07219
G1 X128 Y122.438 E.03391
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.77 Y123.761 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I1.217 J0 P1  F30000
G1 X125.771 Y121.392 Z8.6
G1 Z8.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1924
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.457 J-.955 E.01652
G1 X125 Y121.143 E.00418
G1 X125.055 Y121.054 E.00334
G1 X125.14 Y120.994 E.00335
G1 X125.267 Y120.97 E.00417
G1 X125.412 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.696 J2.017 E.0146
G1 X126.426 Y121.484 F30000
G1 F1924
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.968 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.347 I5.293 J3.36 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.321 Y120.157 I1.056 J-.244 E.06486
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.483 J6.095 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X122.895 Y126.373 E.02403
G3 X122.398 Y126.247 I.388 J-2.558 E.01651
G1 X122.278 Y126.148 E.005
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.851 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.895 J2.464 E.01459
G1 X123.302 Y125.105 F30000
G1 F1924
G1 X123.302 Y126.895 E.05756
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.354 I.201 J-.645 E.05519
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02938
G1 X122.186 Y127.035 E.02815
G3 X122.186 Y124.964 I.322 J-1.035 E.08854
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X130.229 Y121.392 E.02403
G3 X130.587 Y121.025 I2.035 J1.63 E.01651
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.584 J-.458 E.01459
G1 X131.125 Y122.379 F30000
G1 F1924
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.744 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.0353
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05802
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X133.105 Y125.627 E.02403
G1 X133.578 Y125.745 E.01566
G1 X133.669 Y125.794 E.00334
G1 X133.722 Y125.852 E.00252
G1 X133.767 Y126 E.00498
G1 X133.722 Y126.148 E.00498
G1 X133.602 Y126.247 E.00499
G3 X133.164 Y126.364 I-.893 J-2.456 E.01459
G1 X133.003 Y126.819 F30000
G1 F1924
G1 X132.698 Y126.895 E.01011
G1 X132.698 Y125.105 E.05757
G1 X133.696 Y125.355 E.03308
G3 X133.696 Y126.646 I-.201 J.645 E.05519
G1 X133.061 Y126.804 E.02103
G1 X132.901 Y127.456 F30000
G1 F1924
G1 X132.558 Y128.248 E.02774
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.608 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02937
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.322 J1.035 E.08854
G1 X132.995 Y127.241 E.02717
G1 X132.925 Y127.401 E.00562
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35065
G1 X132.521 Y128.315 E-.02935
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.235 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X131.01 Y130.703 E.01565
G1 X131 Y130.857 E.00498
G1 X130.962 Y130.926 E.00253
G1 X130.883 Y130.994 E.00335
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.685 J-2.005 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1924
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.516 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z8.6
G1 Z8.2
M73 P79 R2
G1 E.4 F1800
G1 F1924
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.294 J-3.361 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.09 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18953
G1 X131.848 Y129.311 E-.10814
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G3 X125.412 Y130.975 I-2.043 J-1.638 E.01652
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.234 I2.583 J.457 E.01651
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1924
G1 X125.711 Y131.255 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03306
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I.189 J1.202 P1  F30000
G1 X133.226 Y127.731 Z8.6
G1 Z8.2
G1 E.4 F1800
G1 F1924
G1 X132.924 Y128.428 E.02443
G3 X132.008 Y129.751 I-5.481 J-2.814 E.05188
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.02 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.1219
G1 X123.988 Y129.765 E.02208
G3 X122.733 Y127.592 I4.561 J-4.082 E.08125
G1 X122.067 Y127.425 E.02208
G3 X122.068 Y124.574 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.48 J2.814 E.05188
G1 X123.799 Y121.575 E.02254
G3 X125.347 Y119.75 I1.454 J-.335 E.08928
G3 X126.268 Y120.15 I-.11 J1.515 E.03289
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.022 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.267 Y124.408 I-4.56 J4.081 E.08125
G1 X133.933 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.425 E.12188
G1 X133.288 Y127.587 E.02136
G1 X133.25 Y127.676 E.00312
G1 X133.55 Y128.006 F30000
G1 F1924
G1 X133.289 Y128.608 E.02112
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13136
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.334 J-3.781 E.07166
G3 X121.446 Y127.577 I.486 J-2.87 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.116 E.07177
G3 X123.357 Y121.113 I2.742 J-1.021 E.03412
G3 X125.374 Y119.344 I1.914 J.148 E.09553
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.071 E.07178
G3 X130.082 Y119.461 I1.955 J1.555 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.333 J3.78 E.07165
G3 X134.554 Y124.422 I-.486 J2.871 E.03391
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01554
G1 X133.574 Y127.951 E.00062
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1924
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.116 J-3.491 E.05783
G3 X122.135 Y123.734 I.379 J-2.267 E.19227
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.194 Y118.949 I2.168 J-.8 E.13006
G3 X127.033 Y119.791 I.042 J2.338 E.0623
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.114 J3.49 E.05783
G3 X133.924 Y128.256 I-.378 J2.267 E.19051
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22697
G1 X133.446 Y129.134 E-.15303
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z8.6
G1 Z8.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118622
G1 F1924
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.16201
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205398
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.248786
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.248741
G1 F1924
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205363
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161985
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118608
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.166473
G1 F1924
G1 X125.25 Y130.763 E.0006
G1 X125.325 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28766
G1 X125.272 Y130.821 E-.09234
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.260642
G1 F1924
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213862
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167083
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.12036
G1 F1924
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167218
G1 X123.421 Y127.444 E.00162
; LINE_WIDTH: 0.214075
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260932
G1 X123.36 Y127.119 E.00285
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I1.072 J-.575 P1  F30000
G1 X122.691 Y125.977 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.166425
G1 F1924
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.0006
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09226
G1 X122.691 Y125.977 E-.28774
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.118617
G1 F1924
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.161999
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205382
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.248764
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I1.065 J.59 P1  F30000
G1 X125.252 Y121.457 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.169851
G1 F1924
M73 P80 R2
G1 X125.252 Y121.24 E.00217
G1 X125.219 Y121.183 E.00066
; WIPE_START
G1 F15000
G1 X125.252 Y121.24 E-.08799
G1 X125.252 Y121.457 E-.29201
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I.024 J1.217 P1  F30000
G1 X126.657 Y121.429 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.248766
G1 F1924
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205381
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161996
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118612
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.165831
G1 F1924
G1 X130.75 Y121.237 E.0006
G1 X130.626 Y121.386 E.00189
; WIPE_START
G1 F15000
G1 X130.75 Y121.237 E-.28799
G1 X130.811 Y121.227 E-.09201
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-1.143 J.416 P1  F30000
G1 X131.29 Y122.542 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.26064
G1 F1924
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213861
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167082
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120303
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.6 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z8.6
G1 Z8.2
G1 E.4 F1800
; LINE_WIDTH: 0.120339
G1 F1924
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167174
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.214008
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260843
G1 X132.64 Y124.881 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 8.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 42/50
; update layer progress
M73 L42
M991 S0 P41 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z8.6 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z8.6
G1 Z8.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1906
G1 X124.116 Y123.758 E.01484
G1 X126.707 Y122.261 E.09622
G1 X128 Y121.515 E.04801
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1906
G1 X126.911 Y122.614 E.08138
G1 X128 Y121.985 E.04045
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1906
M204 S5000
G1 X127.107 Y122.954 E.07538
G1 X128 Y122.438 E.03072
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.771 Y123.761 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I1.217 J0 P1  F30000
G1 X125.771 Y121.392 Z8.8
G1 Z8.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1906
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.431 J-.947 E.01652
G1 X125.011 Y121.119 E.00498
G3 X125.294 Y120.973 I.245 J.129 E.0109
G1 X125.413 Y121.025 E.00418
G3 X125.733 Y121.346 I-1.67 J1.991 E.01459
G1 X126.426 Y121.484 F30000
G1 F1906
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.01489
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.289 J3.357 E.03965
G1 X124.196 Y121.483 E.02891
G3 X125.321 Y120.157 I1.056 J-.244 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.483 J6.091 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.395 J-2.58 E.01652
G1 X122.331 Y126.206 E.00252
G3 X122.423 Y125.745 I.17 J-.206 E.01853
G1 X122.836 Y125.641 E.01372
G1 X123.302 Y125.105 F30000
G1 F1906
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.036 E.02816
G3 X122.186 Y124.964 I.321 J-1.035 E.08855
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.042 J1.637 E.01651
G1 X130.707 Y120.973 E.00417
G3 X130.811 Y120.977 I.04 J.371 E.00336
G1 X130.905 Y121.02 E.00335
G1 X130.977 Y121.096 E.00335
G1 X131.013 Y121.194 E.00336
G1 X131.015 Y121.272 E.00251
G3 X130.897 Y121.71 I-2.58 J-.456 E.0146
G1 X131.125 Y122.379 F30000
G1 F1906
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01914
G3 X131.407 Y121.39 I-.09 J.67 E.03618
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.144 J1.075 E.05803
G1 X131.563 Y122.325 E.02817
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01565
G1 X133.648 Y125.778 E.00252
G1 X133.713 Y125.84 E.00289
G1 X133.756 Y125.923 E.00298
G1 X133.767 Y126 E.00252
G1 X133.722 Y126.148 E.00498
G1 X133.602 Y126.247 E.00499
G3 X133.164 Y126.364 I-.893 J-2.456 E.01459
G1 X133.004 Y126.819 F30000
G1 F1906
G1 X132.698 Y126.895 E.01012
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.646 I-.2 J.645 E.05522
G1 X133.062 Y126.804 E.02101
G1 X132.901 Y127.457 F30000
G1 F1906
G1 X132.558 Y128.248 E.02773
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.036 I-.321 J1.036 E.08857
G1 X132.995 Y127.241 E.02717
G1 X132.925 Y127.402 E.00563
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35046
G1 X132.52 Y128.316 E-.02954
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.234 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X131.01 Y130.703 E.01565
G1 X131.008 Y130.832 E.00417
G1 X130.935 Y130.956 E.00461
G1 X130.836 Y131.016 E.00373
G1 X130.706 Y131.027 E.00417
G3 X130.568 Y130.958 I.046 J-.269 E.00505
G1 X130.229 Y130.608 E.01565
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1906
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X132.316 Y128.684 E.00629
M73 P81 R2
G3 X131.557 Y129.653 I-5.302 J-3.366 E.03966
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.02891
G3 X128.166 Y131.079 I-1.482 J-6.087 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.1896
G1 X131.848 Y129.311 E-.10806
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G3 X125.412 Y130.975 I-2.043 J-1.639 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.117 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.58 J.456 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.517 F30000
G1 F1906
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.05519
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I.189 J1.202 P1  F30000
G1 X133.226 Y127.731 Z8.8
G1 Z8.4
G1 E.4 F1800
G1 F1906
G1 X132.924 Y128.428 E.02442
G3 X132.008 Y129.751 I-5.484 J-2.816 E.05188
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.018 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.574 I.443 J-1.425 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.477 J2.812 E.05187
G1 X123.799 Y121.575 E.02255
G3 X125.347 Y119.75 I1.454 J-.335 E.08928
G3 X126.268 Y120.15 I-.11 J1.515 E.03289
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.022 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.574 E.02208
G3 X133.932 Y127.426 I-.442 J1.426 E.12192
G1 X133.288 Y127.587 E.02136
G1 X133.249 Y127.676 E.00313
G1 X133.659 Y127.914 F30000
G1 F1906
G1 X133.582 Y127.933 E.00256
G3 X132.459 Y129.848 I-5.807 J-2.117 E.07177
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.557 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13136
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.874 E.03393
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.804 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.374 Y119.344 I1.914 J.148 E.09553
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07177
G3 X130.082 Y119.461 I1.956 J1.556 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.778 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.06 J1.577 E.1376
G1 X133.717 Y127.899 E.01105
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1906
M204 S5000
G3 X132.894 Y129.942 I-5.58 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.577 J2.111 E.05794
G3 X125.4 Y118.952 I2.167 J-.8 E.13618
G3 X127.033 Y119.791 I-.225 J2.448 E.05605
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.111 J3.488 E.05782
G3 X133.924 Y128.256 I-.378 J2.268 E.19052
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22698
G1 X133.446 Y129.134 E-.15302
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z8.8
G1 Z8.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118626
G1 F1906
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162038
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.20545
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248861
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z8.8
G1 Z8.4
G1 E.4 F1800
; LINE_WIDTH: 0.248698
G1 F1906
G1 X129.188 Y130.627 E.00268
; LINE_WIDTH: 0.205333
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161967
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118602
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z8.8
G1 Z8.4
G1 E.4 F1800
; LINE_WIDTH: 0.166741
G1 F1906
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00188
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.2874
G1 X125.272 Y130.821 E-.0926
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z8.8
G1 Z8.4
G1 E.4 F1800
; LINE_WIDTH: 0.260656
G1 F1906
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213872
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167089
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120305
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z8.8
G1 Z8.4
G1 E.4 F1800
; LINE_WIDTH: 0.120317
G1 F1906
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167112
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213907
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260703
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z8.8
G1 Z8.4
G1 E.4 F1800
; LINE_WIDTH: 0.165883
G1 F1906
G1 X122.438 Y126.007 E.00247
; WIPE_START
G1 F15000
G1 X122.691 Y125.977 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z8.8
G1 Z8.4
G1 E.4 F1800
; LINE_WIDTH: 0.118601
G1 F1906
G1 X124.334 Y122.868 E.00098
; LINE_WIDTH: 0.161958
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205316
G1 X124.587 Y122.657 E.00211
; LINE_WIDTH: 0.248674
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z8.8
G1 Z8.4
G1 E.4 F1800
; LINE_WIDTH: 0.248753
G1 F1906
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205372
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161991
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.11861
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-.358 J1.163 P1  F30000
G1 X131.29 Y122.542 Z8.8
G1 Z8.4
M73 P82 R2
G1 E.4 F1800
; LINE_WIDTH: 0.260614
G1 F1906
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213842
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167071
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120299
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z8.8 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z8.8
G1 Z8.4
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1906
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 8.6
; LAYER_HEIGHT: 0.200001
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 43/50
; update layer progress
M73 L43
M991 S0 P42 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z8.8 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z8.8
G1 Z8.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1906
G1 X124.116 Y123.758 E.01484
G1 X126.8 Y122.208 E.09966
G1 X128 Y121.515 E.04456
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1906
G1 X127.003 Y122.56 E.08482
G1 X128 Y121.985 E.037
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1906
M204 S5000
G1 X127.199 Y122.9 E.07857
G1 X128 Y122.438 E.02753
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.771 Y123.762 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I1.217 J0 P1  F30000
G1 X125.771 Y121.392 Z9
G1 Z8.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1906
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.445 J-.951 E.01652
G1 X125 Y121.143 E.00417
G1 X125.063 Y121.047 E.00369
G1 X125.164 Y120.984 E.00383
G1 X125.267 Y120.97 E.00334
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.67 J1.991 E.01459
G1 X126.426 Y121.484 F30000
G1 F1906
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03306
G3 X125.294 Y120.564 I.66 J-.151 E.0404
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.969 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.347 I5.288 J3.356 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.321 Y120.157 I1.058 J-.242 E.06482
G3 X125.99 Y120.447 I-.08 J1.101 E.0239
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.483 J6.091 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.393 J-2.571 E.01652
G1 X122.331 Y126.206 E.00252
G1 X122.274 Y126.142 E.00276
G1 X122.233 Y126 E.00475
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.892 J2.45 E.0146
G1 X123.302 Y125.105 F30000
G1 F1906
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X130.229 Y121.392 E.02404
G3 X130.588 Y121.025 I2.048 J1.643 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00334
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00336
G1 X131.008 Y121.168 E.00334
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.602 J-.462 E.0146
G1 X131.125 Y122.379 F30000
G1 F1906
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.5 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05802
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X133.105 Y125.626 E.02404
G1 X133.577 Y125.745 E.01565
G1 X133.706 Y125.831 E.00499
G1 X133.756 Y125.923 E.00335
G1 X133.767 Y126 E.00252
G1 X133.722 Y126.148 E.00498
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.893 J-2.455 E.0146
G1 X133.004 Y126.819 F30000
G1 F1906
G1 X132.698 Y126.895 E.01014
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.645 I-.2 J.645 E.0552
G1 X133.062 Y126.804 E.021
G1 X132.901 Y127.457 F30000
G1 F1906
G1 X132.558 Y128.248 E.02771
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15106
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.035 I-.321 J1.035 E.08854
G1 X132.994 Y127.241 E.02717
G1 X132.925 Y127.402 E.00565
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35022
G1 X132.52 Y128.316 E-.02979
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.234 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X131.01 Y130.702 E.01565
G1 X131 Y130.857 E.00498
G1 X130.906 Y130.98 E.00498
G1 X130.811 Y131.023 E.00335
G1 X130.733 Y131.03 E.00252
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.676 J-1.997 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.124 Y129.621 F30000
G1 F1906
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.574 Y130.516 E.03307
G1 X131.072 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.289 J-3.357 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.091 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.1895
G1 X131.848 Y129.311 E-.10816
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z9
G1 Z8.6
M73 P83 R2
G1 E.4 F1800
G1 F1906
G3 X125.412 Y130.975 I-2.05 J-1.645 E.01652
G1 X125.267 Y131.03 E.00499
G1 X125.116 Y130.994 E.00498
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.579 J.456 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.517 F30000
G1 F1906
G1 X125.711 Y131.255 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03306
G1 X126.374 Y130.487 E.05566
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08854
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I.188 J1.202 P1  F30000
G1 X133.225 Y127.732 Z9
G1 Z8.6
G1 E.4 F1800
G1 F1906
G1 X132.924 Y128.428 E.0244
G3 X132.008 Y129.751 I-5.476 J-2.812 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.02 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12189
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.477 J2.812 E.05187
G1 X123.799 Y121.575 E.02254
G3 X125.347 Y119.75 I1.456 J-.334 E.08925
G3 X126.268 Y120.15 I-.11 J1.515 E.03289
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.021 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.442 J1.425 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.249 Y127.677 E.00315
G1 X133.66 Y127.913 F30000
G1 F1906
G1 X133.582 Y127.933 E.00258
G3 X132.459 Y129.848 I-5.803 J-2.115 E.07177
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.742 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
G3 X125.918 Y132.539 I-1.957 J-1.558 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.874 E.03392
G3 X121.949 Y124.185 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.116 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.374 Y119.344 I1.913 J.147 E.09554
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07177
G3 X130.082 Y119.461 I1.956 J1.557 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13134
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.33 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.875 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.718 Y127.899 E.01103
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1906
M204 S5000
G3 X132.894 Y129.942 I-5.577 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19228
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.579 J2.112 E.05794
G3 X125.4 Y118.952 I2.153 J-.81 E.13649
G3 X127.033 Y119.791 I-.225 J2.448 E.05605
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.227
G1 X133.446 Y129.134 E-.153
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z9
G1 Z8.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118609
G1 F1906
G1 X131.666 Y129.132 E.00099
; LINE_WIDTH: 0.161982
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205355
G1 X131.413 Y129.343 E.00211
; LINE_WIDTH: 0.248728
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.248752
G1 F1906
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205371
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.16199
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.11861
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-.021 J-1.217 P1  F30000
G1 X125.204 Y130.805 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.167402
G1 F1906
G1 X125.25 Y130.764 E.0006
G1 X125.326 Y130.586 E.0019
; WIPE_START
G1 F15000
G1 X125.25 Y130.764 E-.28821
G1 X125.204 Y130.805 E-.09179
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I1.142 J-.419 P1  F30000
G1 X124.71 Y129.459 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.260652
G1 F1906
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213869
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167087
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120305
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.120317
G1 F1906
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167112
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213908
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260703
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.166343
G1 F1906
G1 X122.438 Y126.007 E.00248
; WIPE_START
G1 F15000
G1 X122.691 Y125.977 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.118605
G1 F1906
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.161972
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205339
G1 X124.587 Y122.657 E.00211
; LINE_WIDTH: 0.248705
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.248753
G1 F1906
G1 X126.812 Y121.373 E.00268
; LINE_WIDTH: 0.205372
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161991
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.11861
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-.358 J1.163 P1  F30000
G1 X131.29 Y122.542 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.260624
G1 F1906
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213849
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167075
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120301
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z9
G1 Z8.6
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1906
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 8.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 44/50
; update layer progress
M73 L44
M991 S0 P43 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z9 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z9
G1 Z8.8
M73 P84 R2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X124.116 Y123.758 E.01484
G1 X126.893 Y122.154 E.1031
G1 X128 Y121.515 E.04112
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1915
G1 X127.096 Y122.507 E.08827
G1 X128 Y121.985 E.03356
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.008 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G1 X127.292 Y122.846 E.08176
G1 X128 Y122.438 E.02435
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.772 Y123.763 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I1.217 J0 P1  F30000
G1 X125.771 Y121.392 Z9.2
G1 Z8.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.443 J-.951 E.01651
G1 X124.992 Y121.168 E.00336
G1 X125.055 Y121.054 E.00416
G1 X125.147 Y120.991 E.00359
G1 X125.267 Y120.97 E.00393
G1 X125.413 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.68 J2 E.01459
G1 X126.426 Y121.484 F30000
G1 F1915
G1 X124.876 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.687 E.01489
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.968 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.299 J3.364 E.03966
G1 X124.196 Y121.483 E.02889
G3 X125.321 Y120.157 I1.056 J-.244 E.06486
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.02889
G3 X127.834 Y120.921 I1.484 J6.105 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X122.895 Y126.374 E.02404
G3 X122.398 Y126.247 I.398 J-2.592 E.01651
G1 X122.283 Y126.154 E.00475
G1 X122.245 Y126.077 E.00276
G1 X122.233 Y126 E.00252
G1 X122.278 Y125.852 E.00499
G1 X122.398 Y125.753 E.00498
G3 X122.836 Y125.636 I.893 J2.456 E.0146
G1 X123.302 Y125.105 F30000
G1 F1915
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.354 I.2 J-.645 E.0552
G1 X123.244 Y125.119 E.03113
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01064
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.964 I.322 J-1.035 E.08855
G1 X123.005 Y124.759 E.02716
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.043 J1.638 E.01651
G1 X130.681 Y120.979 E.00336
G1 X130.785 Y120.972 E.00334
G1 X130.883 Y121.006 E.00334
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00336
G3 X130.897 Y121.71 I-2.598 J-.462 E.01459
G1 X131.125 Y122.379 F30000
G1 F1915
G1 X129.574 Y121.484 E.05759
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01916
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01565
G1 X133.706 Y125.831 E.00498
G1 X133.747 Y125.898 E.00252
G1 X133.767 Y126 E.00334
G1 X133.722 Y126.148 E.00499
G1 X133.602 Y126.247 E.00498
G3 X133.164 Y126.364 I-.895 J-2.463 E.01459
G1 X133.005 Y126.819 F30000
G1 F1915
G1 X132.698 Y126.895 E.01015
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.645 I-.2 J.645 E.0552
G1 X133.063 Y126.804 E.02098
G1 X132.901 Y127.458 F30000
G1 F1915
G1 X132.558 Y128.248 E.02769
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01064
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.035 I-.321 J1.035 E.08855
G1 X132.995 Y127.241 E.02717
G1 X132.924 Y127.403 E.00567
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.35005
G1 X132.52 Y128.317 E-.02995
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.234 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X131.01 Y130.703 E.01565
G1 X131.016 Y130.781 E.00252
G1 X130.992 Y130.876 E.00316
G1 X130.945 Y130.946 E.0027
G1 X130.883 Y130.994 E.00252
G1 X130.733 Y131.03 E.00498
G1 X130.588 Y130.975 E.00499
G3 X130.229 Y130.608 I1.679 J-2 E.01652
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1915
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.255 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03306
G1 X131.073 Y129.651 E.05565
; WIPE_START
M73 P84 R1
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.654 I-5.309 J-3.371 E.03966
G1 X131.804 Y130.517 E.02889
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.482 J-6.09 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18968
G1 X131.848 Y129.311 E-.10798
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G3 X125.412 Y130.975 I-2.04 J-1.635 E.01652
G1 X125.268 Y131.03 E.00498
G1 X125.189 Y131.023 E.00252
G1 X125.112 Y130.991 E.00269
G1 X125.011 Y130.881 E.00481
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.597 J.461 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1915
G1 X125.711 Y131.255 E.03307
G3 X124.593 Y130.61 I-.458 J-.497 E.05516
G1 X124.875 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z9.2
G1 Z8.8
M73 P85 R1
G1 E.4 F1800
G1 F1915
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.797 E.08851
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I.188 J1.202 P1  F30000
G1 X133.225 Y127.732 Z9.2
G1 Z8.8
G1 E.4 F1800
G1 F1915
G1 X132.924 Y128.428 E.02438
G3 X132.008 Y129.751 I-5.488 J-2.819 E.05188
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.3 J-6.02 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.097 E.12185
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.425 E.02208
G3 X122.068 Y124.574 I.443 J-1.425 E.1219
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.484 J2.816 E.05188
G1 X123.799 Y121.575 E.02254
G3 X125.347 Y119.75 I1.454 J-.335 E.08928
G3 X126.268 Y120.15 I-.11 J1.516 E.0329
G1 X126.756 Y120.653 E.02254
G3 X128.359 Y120.522 I1.3 J6.026 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.558 J4.08 E.08124
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.442 J1.425 E.1219
G1 X133.288 Y127.587 E.02136
G1 X133.249 Y127.677 E.00317
G1 X133.55 Y128.007 F30000
G1 F1915
G1 X133.289 Y128.608 E.02106
G3 X132.459 Y129.848 I-5.515 J-2.792 E.0481
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.742 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13765
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.07 E.07177
G3 X125.918 Y132.539 I-1.955 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.578 I.488 J-2.875 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13766
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.742 J-1.021 E.03412
G3 X125.374 Y119.344 I1.914 J.148 E.09553
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.071 E.07177
G3 X130.082 Y119.461 I1.957 J1.558 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.873 E.03392
G3 X134.051 Y127.816 I-1.059 J1.577 E.13762
G1 X133.582 Y127.933 E.01554
G1 X133.573 Y127.952 E.00067
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G3 X132.894 Y129.942 I-5.58 J-2.113 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.468 E.19222
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.4 Y118.952 I2.166 J-.8 E.13618
G3 X127.033 Y119.791 I-.225 J2.448 E.05605
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05348
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19051
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22695
G1 X133.445 Y129.134 E-.15305
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z9.2
G1 Z8.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118628
G1 F1915
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162062
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205497
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248932
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.248754
G1 F1915
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205373
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161991
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.11861
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-.015 J-1.217 P1  F30000
G1 X125.192 Y130.785 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.167392
G1 F1915
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00189
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28783
G1 X125.192 Y130.785 E-.09217
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I1.144 J-.416 P1  F30000
G1 X124.71 Y129.459 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.26066
G1 F1915
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213876
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167091
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120306
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1915
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.166179
G1 F1915
G1 X122.499 Y126 E.00188
G1 X122.461 Y126.048 E.0006
; WIPE_START
G1 F15000
G1 X122.499 Y126 E-.09224
G1 X122.691 Y125.977 E-.28776
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.11862
G1 F1915
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162024
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205427
G1 X124.587 Y122.657 E.00212
; LINE_WIDTH: 0.248831
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.587 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.248826
G1 F1915
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205421
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.162017
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118612
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I.017 J1.217 P1  F30000
G1 X130.805 Y121.207 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.165465
G1 F1915
G1 X130.752 Y121.236 E.00058
G2 X130.627 Y121.386 I.266 J.348 E.00191
; WIPE_START
G1 F15000
G1 X130.752 Y121.236 E-.29065
G1 X130.805 Y121.207 E-.08935
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-1.144 J.416 P1  F30000
G1 X131.29 Y122.541 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.260659
G1 F1915
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213875
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.16709
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120305
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.2 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z9.2
G1 Z8.8
G1 E.4 F1800
; LINE_WIDTH: 0.120314
G1 F1915
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167104
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 9
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 45/50
; update layer progress
M73 L45
M991 S0 P44 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z9.2 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z9.2
G1 Z9
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X124.116 Y123.758 E.01484
G1 X126.985 Y122.101 E.10655
G1 X128 Y121.515 E.03767
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
M73 P86 R1
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1915
G1 X127.189 Y122.453 E.09171
G1 X128 Y121.985 E.03012
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G1 X127.385 Y122.793 E.08495
G1 X128 Y122.438 E.02116
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.772 Y123.763 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I1.217 J0 P1  F30000
G1 X125.771 Y121.392 Z9.4
G1 Z9
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.426 J-.946 E.01651
G1 X125 Y121.143 E.00418
G1 X125.055 Y121.054 E.00335
G1 X125.164 Y120.984 E.00416
G1 X125.267 Y120.97 E.00335
G1 X125.412 Y121.025 E.00499
G3 X125.733 Y121.346 I-1.68 J2.002 E.0146
G1 X126.426 Y121.483 F30000
G1 F1915
G1 X124.875 Y122.379 E.05758
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.658 J-.152 E.04043
G3 X125.711 Y120.745 I-.05 J.686 E.0149
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.968 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.317 E.00629
G3 X124.443 Y122.347 I5.29 J3.358 E.03966
G1 X124.196 Y121.483 E.0289
G3 X125.321 Y120.157 I1.056 J-.244 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.0239
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.483 J6.094 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.397 J-2.588 E.01651
G1 X122.278 Y126.148 E.00499
G1 X122.233 Y126 E.00498
G1 X122.278 Y125.851 E.00499
G1 X122.398 Y125.753 E.00497
G3 X122.836 Y125.636 I.893 J2.454 E.0146
G1 X123.302 Y125.105 F30000
G1 F1915
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01064
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.032 J1.627 E.01652
G1 X130.681 Y120.979 E.00335
G1 X130.785 Y120.972 E.00335
G1 X130.883 Y121.006 E.00335
G1 X130.962 Y121.074 E.00335
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.58 J-.456 E.01459
G1 X131.125 Y122.379 F30000
G1 F1915
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.745 E.03307
G3 X130.838 Y120.568 I.464 J.501 E.01915
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03114
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.01 Y120.447 E.02717
G3 X130.891 Y120.164 I.744 J.803 E.03072
G3 X131.804 Y121.483 I-.145 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X133.105 Y125.626 E.02403
G1 X133.577 Y125.745 E.01565
G1 X133.706 Y125.831 E.00498
G1 X133.766 Y125.974 E.00499
G1 X133.735 Y126.126 E.00499
G1 X133.689 Y126.189 E.00251
G1 X133.602 Y126.247 E.00334
G3 X133.164 Y126.364 I-.894 J-2.46 E.0146
G1 X133.005 Y126.819 F30000
G1 F1915
G1 X132.698 Y126.895 E.01017
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.696 Y126.645 I-.2 J.645 E.05519
G1 X133.063 Y126.804 E.02097
G1 X132.9 Y127.458 F30000
G1 F1915
G1 X132.558 Y128.248 E.02767
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01063
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.814 Y127.035 I-.321 J1.035 E.08854
G1 X132.994 Y127.241 E.02717
G1 X132.924 Y127.403 E.00569
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.34983
G1 X132.519 Y128.317 E-.03017
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.234 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X131.01 Y130.703 E.01565
G1 X131.016 Y130.781 E.00252
G1 X130.989 Y130.881 E.00334
G1 X130.884 Y130.994 E.00498
G1 X130.733 Y131.03 E.00498
G1 X130.587 Y130.975 E.00499
G3 X130.229 Y130.608 I1.682 J-2.003 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1915
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.517 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.294 J-3.361 E.03966
G1 X131.804 Y130.518 E.0289
G3 X130.01 Y131.553 I-1.058 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.483 J-6.095 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.1896
G1 X131.848 Y129.311 E-.10806
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G3 X125.413 Y130.975 I-2.046 J-1.641 E.01652
G1 X125.267 Y131.03 E.00498
G1 X125.116 Y130.994 E.00499
G1 X125.011 Y130.881 E.00499
G1 X124.985 Y130.728 E.00498
G3 X125.124 Y130.234 I2.57 J.453 E.01652
G1 X125.719 Y130.578 E.02211
G1 X126.426 Y130.516 F30000
G1 F1915
G1 X125.711 Y131.256 E.03307
G3 X124.593 Y130.61 I-.459 J-.496 E.0552
G1 X124.875 Y129.621 E.03306
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.99 Y131.553 E.02717
G3 X124.196 Y130.517 I-.736 J-.796 E.08855
M73 P87 R1
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I.188 J1.202 P1  F30000
G1 X133.225 Y127.733 Z9.4
G1 Z9
G1 E.4 F1800
G1 F1915
G1 X132.924 Y128.428 E.02436
G3 X132.008 Y129.751 I-5.481 J-2.814 E.05187
G1 X132.201 Y130.425 E.02255
G3 X129.732 Y131.85 I-1.456 J.329 E.12189
G1 X129.244 Y131.347 E.02255
G3 X127.641 Y131.478 I-1.3 J-6.021 E.05187
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.85 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.1219
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.558 J-4.08 E.08124
G1 X122.068 Y127.426 E.02208
G3 X122.068 Y124.575 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02136
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.479 J2.813 E.05187
G1 X123.799 Y121.575 E.02255
G3 X125.347 Y119.75 I1.454 J-.335 E.08928
G3 X126.268 Y120.15 I-.11 J1.515 E.03289
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.022 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.15 E.02135
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.081 E.08124
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.425 I-.442 J1.425 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.249 Y127.678 E.00319
G1 X133.549 Y128.008 F30000
G1 F1915
G1 X133.289 Y128.608 E.02105
G3 X132.459 Y129.848 I-5.512 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.743 J1.021 E.03412
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.071 E.07177
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13136
G1 X123.539 Y129.854 E.01599
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.874 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.805 J2.115 E.07177
G3 X123.357 Y121.113 I2.743 J-1.021 E.03412
G3 X125.374 Y119.344 I1.914 J.148 E.09553
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.07 E.07177
G3 X130.082 Y119.461 I1.956 J1.556 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.332 J3.78 E.07165
G3 X134.554 Y124.422 I-.488 J2.874 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01555
G1 X133.573 Y127.953 E.00069
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.923 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.577 J2.111 E.05794
G3 X125.4 Y118.952 I2.167 J-.8 E.13618
G3 X127.033 Y119.791 I-.225 J2.448 E.05605
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19228
G3 X133.859 Y123.732 I-4.114 J3.49 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.22699
G1 X133.446 Y129.134 E-.15301
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z9.4
G1 Z9
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118617
G1 F1915
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.161999
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205382
G1 X131.413 Y129.343 E.00212
; LINE_WIDTH: 0.248764
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.413 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.248761
G1 F1915
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.205374
G1 X129.033 Y130.684 E.00211
; LINE_WIDTH: 0.161988
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118602
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.166833
G1 F1915
G1 X125.25 Y130.763 E.00061
G1 X125.326 Y130.586 E.00189
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28758
G1 X125.272 Y130.821 E-.09242
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.260641
G1 F1915
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213861
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167082
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120303
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1915
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.166534
G1 F1915
G1 X122.5 Y126 E.00188
G1 X122.461 Y126.048 E.00061
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.09253
G1 X122.691 Y125.977 E-.28747
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.118611
G1 F1915
G1 X124.333 Y122.869 E.00099
; LINE_WIDTH: 0.161986
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205361
G1 X124.586 Y122.657 E.00211
; LINE_WIDTH: 0.248736
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.248759
G1 F1915
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.205374
G1 X126.967 Y121.316 E.00211
; LINE_WIDTH: 0.161988
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118602
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I.009 J1.217 P1  F30000
G1 X130.812 Y121.23 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.164356
G1 F1915
G2 X130.749 Y121.238 I-.026 J.054 E.00065
G1 X130.61 Y121.377 E.00188
; WIPE_START
G1 F15000
G1 X130.749 Y121.238 E-.28662
G1 X130.812 Y121.23 E-.09338
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.260605
G1 F1915
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213836
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167066
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120297
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.4 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z9.4
G1 Z9
G1 E.4 F1800
; LINE_WIDTH: 0.120322
G1 F1915
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167121
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213921
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260721
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 9.2
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 46/50
; update layer progress
M73 L46
M991 S0 P45 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z9.4 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z9.4
G1 Z9.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X124.116 Y123.758 E.01484
G1 X127.078 Y122.047 E.10999
G1 X128 Y121.515 E.03423
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
M73 P88 R1
G1 X124.719 Y123.879 F30000
G1 F1915
G1 X127.282 Y122.4 E.09515
G1 X128 Y121.985 E.02667
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.008 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G1 X127.478 Y122.739 E.08814
G1 X128 Y122.438 E.01797
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.772 Y123.764 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I1.217 J-.001 P1  F30000
G1 X125.771 Y121.392 Z9.6
G1 Z9.2
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1915
G1 X125.124 Y121.766 E.02404
G3 X124.985 Y121.272 I2.448 J-.952 E.01651
G1 X125 Y121.143 E.00418
G1 X125.056 Y121.053 E.00339
G1 X125.164 Y120.984 E.00413
G1 X125.267 Y120.97 E.00334
G1 X125.412 Y121.025 E.00498
G3 X125.733 Y121.346 I-1.695 J2.016 E.0146
G1 X126.426 Y121.483 F30000
G1 F1915
G1 X124.875 Y122.379 E.05759
G1 X124.593 Y121.39 E.03307
G3 X125.294 Y120.564 I.659 J-.152 E.04042
G3 X125.711 Y120.744 I-.05 J.686 E.01489
G1 X126.385 Y121.44 E.03114
; WIPE_START
G1 F11054.348
G1 X125.535 Y121.968 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I.418 J1.143 P1  F30000
G1 X127.892 Y121.107 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X123.817 Y123.46 E.15133
G1 X123.684 Y123.316 E.00629
G3 X124.443 Y122.347 I5.304 J3.368 E.03966
G1 X124.196 Y121.483 E.02889
G3 X125.321 Y120.157 I1.057 J-.243 E.06485
G3 X125.99 Y120.447 I-.08 J1.101 E.02389
G1 X126.615 Y121.093 E.0289
G3 X127.834 Y120.921 I1.483 J6.101 E.03966
G1 X127.874 Y121.05 E.00436
; WIPE_START
G1 F11054.348
G1 X127.015 Y121.561 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-.855 J-.866 P1  F30000
G1 X122.895 Y125.626 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X122.895 Y126.374 E.02403
G3 X122.398 Y126.247 I.397 J-2.585 E.01652
G1 X122.278 Y126.148 E.00501
G1 X122.233 Y126 E.00496
G1 X122.278 Y125.852 E.00498
G1 X122.398 Y125.753 E.00499
G3 X122.836 Y125.636 I.894 J2.462 E.01459
G1 X123.302 Y125.105 F30000
G1 F1915
G1 X123.302 Y126.895 E.05758
G1 X122.304 Y126.645 E.03307
G3 X122.304 Y125.355 I.2 J-.645 E.05519
G1 X123.244 Y125.119 E.03114
; WIPE_START
G1 F11054.348
G1 X123.276 Y126.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I1.187 J.27 P1  F30000
G1 X123.709 Y124.219 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X123.709 Y128.346 E.13272
G1 X123.522 Y128.392 E.00618
G1 X123.371 Y128.097 E.01063
G1 X123.035 Y127.248 E.02936
G1 X122.186 Y127.035 E.02816
G3 X122.186 Y124.965 I.321 J-1.035 E.08854
G1 X123.005 Y124.759 E.02717
G1 X123.442 Y123.752 E.03529
G1 X123.526 Y123.601 E.00555
G1 X123.709 Y123.649 E.00608
G1 X123.709 Y124.159 E.0164
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I.521 J1.1 P1  F30000
G1 X130.876 Y121.766 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X130.229 Y121.392 E.02404
G3 X130.587 Y121.025 I2.041 J1.636 E.01651
G1 X130.681 Y120.979 E.00336
G1 X130.785 Y120.972 E.00335
G1 X130.884 Y121.006 E.00335
G1 X130.962 Y121.074 E.00334
G1 X131.008 Y121.168 E.00335
G1 X131.015 Y121.272 E.00335
G3 X130.897 Y121.71 I-2.568 J-.453 E.0146
G1 X131.125 Y122.379 F30000
G1 F1915
G1 X129.574 Y121.484 E.05758
G1 X130.289 Y120.744 E.03308
G3 X130.838 Y120.568 I.464 J.501 E.01914
G3 X131.407 Y121.39 I-.09 J.67 E.03617
G1 X131.141 Y122.321 E.03113
; WIPE_START
G1 F11054.348
G1 X130.259 Y121.85 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-.781 J.933 P1  F30000
G1 X132.178 Y123.457 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X128.109 Y121.108 E.15106
G1 X128.16 Y120.926 E.00608
G1 X128.332 Y120.929 E.00555
G1 X129.423 Y121.054 E.03529
G1 X130.011 Y120.447 E.02718
G3 X130.891 Y120.164 I.744 J.803 E.03071
G3 X131.804 Y121.483 I-.145 J1.075 E.05803
G1 X131.563 Y122.325 E.02816
G1 X132.131 Y123.04 E.02936
G1 X132.31 Y123.318 E.01063
G1 X132.219 Y123.413 E.00425
; WIPE_START
G1 F11054.348
G1 X131.347 Y122.924 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-1.084 J.553 P1  F30000
G1 X133.105 Y126.374 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X133.105 Y125.626 E.02403
G1 X133.578 Y125.745 E.01565
G1 X133.706 Y125.831 E.00498
G1 X133.766 Y125.974 E.00499
G1 X133.735 Y126.126 E.00498
G1 X133.669 Y126.206 E.00334
G1 X133.602 Y126.247 E.00252
G3 X133.164 Y126.364 I-.898 J-2.476 E.01459
G1 X133 Y126.818 F30000
G1 F1915
G1 X132.698 Y126.895 E.01002
G1 X132.698 Y125.105 E.05758
G1 X133.696 Y125.355 E.03307
G3 X133.758 Y126.623 I-.197 J.646 E.0532
G1 X133.058 Y126.803 E.02323
G1 X132.9 Y127.459 F30000
G1 F1915
G1 X132.558 Y128.248 E.02766
G1 X132.474 Y128.399 E.00555
G1 X132.291 Y128.351 E.00608
G1 X132.291 Y123.654 E.15105
G1 X132.478 Y123.609 E.00618
G1 X132.629 Y123.903 E.01064
G1 X132.965 Y124.752 E.02936
G1 X133.814 Y124.965 E.02816
G3 X133.914 Y127 I-.316 J1.036 E.08534
G1 X132.994 Y127.241 E.03056
G1 X132.924 Y127.404 E.0057
; WIPE_START
G1 F11054.348
G1 X132.558 Y128.248 E-.34963
G1 X132.519 Y128.318 E-.03037
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-.924 J-.792 P1  F30000
G1 X130.876 Y130.234 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X131.01 Y130.702 E.01565
G1 X131 Y130.857 E.00499
G1 X130.905 Y130.98 E.00498
G1 X130.759 Y131.03 E.00498
G1 X130.681 Y131.021 E.00252
G1 X130.587 Y130.975 E.00335
G3 X130.229 Y130.608 I1.675 J-1.995 E.01651
G1 X130.824 Y130.264 E.02211
G1 X131.125 Y129.621 F30000
G1 F1915
G1 X131.407 Y130.61 E.03307
G3 X130.289 Y131.256 I-.659 J.149 E.05519
G1 X129.574 Y130.516 E.03307
G1 X131.073 Y129.651 E.05565
; WIPE_START
G1 F11054.348
G1 X131.402 Y130.595 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I1.138 J.433 P1  F30000
G1 X132.183 Y128.54 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X132.316 Y128.684 E.00629
G3 X131.557 Y129.653 I-5.304 J-3.368 E.03966
G1 X131.804 Y130.517 E.0289
G3 X130.01 Y131.553 I-1.057 J.239 E.08854
G1 X129.385 Y130.907 E.0289
G3 X128.166 Y131.079 I-1.484 J-6.112 E.03966
G1 X128.108 Y130.893 E.00629
G1 X132.131 Y128.57 E.1494
; WIPE_START
G1 F11054.348
G1 X132.316 Y128.684 E-.08234
G1 X132.032 Y129.094 E-.18959
G1 X131.848 Y129.311 E-.10807
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-.254 J-1.19 P1  F30000
G1 X125.771 Y130.608 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G3 X125.413 Y130.975 I-2.032 J-1.628 E.01651
G1 X125.267 Y131.03 E.00499
G1 X125.117 Y130.994 E.00497
G1 X125.011 Y130.881 E.00498
G1 X124.985 Y130.728 E.00499
G3 X125.124 Y130.235 I2.59 J.46 E.01651
G1 X125.719 Y130.578 E.0221
G1 X126.426 Y130.516 F30000
G1 F1915
G1 X125.711 Y131.256 E.03308
G3 X124.593 Y130.61 I-.459 J-.497 E.05518
G1 X124.876 Y129.621 E.03307
G1 X126.374 Y130.486 E.05565
; WIPE_START
G1 F11054.348
G1 X125.721 Y131.244 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I.996 J-.7 P1  F30000
G1 X123.822 Y128.543 Z9.6
G1 Z9.2
G1 E.4 F1800
G1 F1915
G1 X127.891 Y130.892 E.15106
G1 X127.84 Y131.074 E.00608
G1 X127.668 Y131.071 E.00555
G1 X126.577 Y130.946 E.03529
G1 X125.989 Y131.553 E.02718
G3 X124.196 Y130.517 I-.736 J-.796 E.08853
G1 X124.437 Y129.675 E.02816
G1 X123.869 Y128.96 E.02936
G1 X123.69 Y128.682 E.01063
G1 X123.781 Y128.587 E.00425
; WIPE_START
G1 F11054.348
G1 X124.653 Y129.076 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I.188 J1.202 P1  F30000
G1 X133.225 Y127.733 Z9.6
G1 Z9.2
G1 E.4 F1800
M73 P89 R1
G1 F1915
G1 X132.923 Y128.428 E.02435
G3 X132.008 Y129.751 I-5.486 J-2.818 E.05187
G1 X132.201 Y130.425 E.02254
G3 X129.732 Y131.85 I-1.456 J.33 E.12189
G1 X129.244 Y131.347 E.02254
G3 X127.641 Y131.478 I-1.301 J-6.031 E.05188
G1 X126.73 Y131.373 E.02948
G1 X126.268 Y131.851 E.02136
G3 X123.799 Y130.425 I-1.013 J-1.096 E.12188
G1 X123.988 Y129.765 E.02208
G3 X122.734 Y127.592 I4.559 J-4.08 E.08124
G1 X122.068 Y127.425 E.02208
G3 X122.068 Y124.574 I.443 J-1.425 E.12189
G1 X122.712 Y124.413 E.02135
G1 X123.076 Y123.572 E.02948
G3 X123.992 Y122.249 I5.486 J2.818 E.05188
G1 X123.799 Y121.575 E.02254
G3 X125.347 Y119.75 I1.454 J-.335 E.08928
G3 X126.268 Y120.15 I-.11 J1.515 E.03289
G1 X126.756 Y120.653 E.02255
G3 X128.359 Y120.522 I1.3 J6.027 E.05187
G1 X129.27 Y120.627 E.02948
G1 X129.732 Y120.149 E.02136
G3 X132.201 Y121.575 I1.013 J1.096 E.12189
G1 X132.012 Y122.235 E.02208
G3 X133.266 Y124.408 I-4.559 J4.08 E.08123
G1 X133.932 Y124.575 E.02208
G3 X133.932 Y127.426 I-.443 J1.426 E.12189
G1 X133.288 Y127.587 E.02136
G1 X133.248 Y127.678 E.0032
G1 X133.549 Y128.008 F30000
G1 F1915
G1 X133.289 Y128.608 E.02103
G3 X132.459 Y129.848 I-5.513 J-2.791 E.04809
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.643 Y130.887 I-2.744 J1.021 E.03411
G3 X129.453 Y132.148 I-1.895 J-.128 E.13764
G1 X129.103 Y131.786 E.01619
G3 X126.883 Y131.8 I-1.149 J-6.072 E.07178
G3 X125.918 Y132.539 I-1.956 J-1.556 E.03946
G3 X123.402 Y130.332 I-.657 J-1.789 E.13135
G1 X123.539 Y129.854 E.016
G3 X122.432 Y127.936 I4.331 J-3.779 E.07165
G3 X121.446 Y127.577 I.488 J-2.874 E.03392
G3 X121.949 Y124.184 I1.058 J-1.577 E.13765
G1 X122.418 Y124.067 E.01554
G3 X123.541 Y122.152 I5.806 J2.116 E.07177
G3 X123.357 Y121.113 I2.742 J-1.021 E.03412
G3 X125.374 Y119.344 I1.914 J.148 E.09553
G3 X126.547 Y119.852 I-.14 J1.93 E.04189
G1 X126.897 Y120.214 E.01619
G3 X129.117 Y120.2 I1.149 J6.071 E.07178
G3 X130.082 Y119.461 I1.955 J1.556 E.03946
G3 X132.598 Y121.668 I.657 J1.789 E.13135
G1 X132.461 Y122.146 E.016
G3 X133.568 Y124.064 I-4.331 J3.779 E.07165
G3 X134.554 Y124.423 I-.488 J2.874 E.03392
G3 X134.051 Y127.816 I-1.058 J1.577 E.13765
G1 X133.582 Y127.933 E.01554
G1 X133.573 Y127.953 E.00071
M204 S250
G1 X133.865 Y128.266 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1915
M204 S5000
G3 X132.894 Y129.942 I-5.578 J-2.112 E.05794
G3 X128.967 Y132.209 I-2.154 J.803 E.19232
G1 X128.821 Y132.236 E.00442
G3 X127.03 Y132.212 I-.803 J-6.922 E.05349
G3 X123.107 Y129.94 I-1.77 J-1.467 E.19227
G3 X122.141 Y128.268 I4.112 J-3.489 E.05782
G3 X122.135 Y123.734 I.379 J-2.268 E.19227
G3 X123.106 Y122.058 I5.578 J2.112 E.05794
G3 X125.4 Y118.952 I2.167 J-.8 E.13617
G3 X127.033 Y119.791 I-.225 J2.448 E.05605
G1 X127.179 Y119.764 E.00442
G3 X128.97 Y119.788 I.803 J6.922 E.05349
G3 X132.893 Y122.06 I1.77 J1.467 E.19227
G3 X133.859 Y123.732 I-4.112 J3.489 E.05782
G3 X133.924 Y128.256 I-.379 J2.268 E.19049
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.641 Y128.782 E-.227
G1 X133.446 Y129.134 E-.153
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I.079 J-1.214 P1  F30000
G1 X131.793 Y129.026 Z9.6
G1 Z9.2
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.118622
G1 F1915
G1 X131.667 Y129.132 E.00099
; LINE_WIDTH: 0.162024
G1 X131.54 Y129.237 E.00155
; LINE_WIDTH: 0.205426
G1 X131.414 Y129.343 E.00212
; LINE_WIDTH: 0.248828
G1 X131.287 Y129.448 E.00268
; WIPE_START
G1 F15000
G1 X131.414 Y129.343 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-.621 J-1.047 P1  F30000
G1 X129.343 Y130.571 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.248908
G1 F1915
G1 X129.188 Y130.628 E.00268
; LINE_WIDTH: 0.20548
G1 X129.033 Y130.684 E.00212
; LINE_WIDTH: 0.162052
G1 X128.879 Y130.741 E.00155
; LINE_WIDTH: 0.118624
G1 X128.724 Y130.798 E.00099
; WIPE_START
G1 F15000
G1 X128.879 Y130.741 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-.027 J-1.217 P1  F30000
G1 X125.272 Y130.821 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.1668
G1 F1915
G1 X125.25 Y130.763 E.00061
G1 X125.325 Y130.586 E.00189
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.28768
G1 X125.272 Y130.821 E-.09232
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I1.125 J-.464 P1  F30000
G1 X124.71 Y129.459 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.260668
G1 F1915
G1 X124.585 Y129.351 E.00284
; LINE_WIDTH: 0.213886
G1 X124.46 Y129.243 E.00223
; LINE_WIDTH: 0.167104
G1 X124.335 Y129.135 E.00162
; LINE_WIDTH: 0.120322
G1 X124.21 Y129.027 E.00101
; WIPE_START
G1 F15000
G1 X124.335 Y129.135 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I1.033 J-.644 P1  F30000
G1 X123.483 Y127.768 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1915
G1 X123.452 Y127.606 E.00101
; LINE_WIDTH: 0.167105
G1 X123.422 Y127.444 E.00162
; LINE_WIDTH: 0.213895
G1 X123.391 Y127.282 E.00223
; LINE_WIDTH: 0.260685
G1 X123.36 Y127.12 E.00284
; WIPE_START
G1 F15000
G1 X123.391 Y127.282 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I1.073 J-.575 P1  F30000
G1 X122.691 Y125.977 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.167144
G1 F1915
G1 X122.438 Y126.006 E.0025
; WIPE_START
G1 F15000
G1 X122.691 Y125.977 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I1.086 J.548 P1  F30000
G1 X124.207 Y122.974 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.118626
G1 F1915
G1 X124.333 Y122.868 E.00099
; LINE_WIDTH: 0.162035
G1 X124.46 Y122.763 E.00155
; LINE_WIDTH: 0.205444
G1 X124.586 Y122.657 E.00212
; LINE_WIDTH: 0.248854
G1 X124.713 Y122.552 E.00268
; WIPE_START
G1 F15000
G1 X124.586 Y122.657 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I.621 J1.047 P1  F30000
G1 X126.657 Y121.429 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.248764
G1 F1915
G1 X126.812 Y121.372 E.00268
; LINE_WIDTH: 0.20538
G1 X126.967 Y121.316 E.00212
; LINE_WIDTH: 0.161996
G1 X127.121 Y121.259 E.00155
; LINE_WIDTH: 0.118612
G1 X127.276 Y121.202 E.00099
; WIPE_START
G1 F15000
G1 X127.121 Y121.259 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I.01 J1.217 P1  F30000
G1 X130.811 Y121.227 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.166474
G1 F1915
G1 X130.751 Y121.236 E.0006
G1 X130.63 Y121.389 E.0019
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.28905
G1 X130.811 Y121.227 E-.09095
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-1.143 J.417 P1  F30000
G1 X131.29 Y122.542 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.260664
G1 F1915
G1 X131.415 Y122.649 E.00284
; LINE_WIDTH: 0.213878
G1 X131.54 Y122.757 E.00223
; LINE_WIDTH: 0.167092
G1 X131.665 Y122.865 E.00162
; LINE_WIDTH: 0.120307
G1 X131.79 Y122.973 E.00101
; WIPE_START
G1 F15000
G1 X131.665 Y122.865 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.6 I-1.033 J.644 P1  F30000
G1 X132.517 Y124.232 Z9.6
G1 Z9.2
G1 E.4 F1800
; LINE_WIDTH: 0.120315
G1 F1915
G1 X132.548 Y124.394 E.00101
; LINE_WIDTH: 0.167105
G1 X132.578 Y124.556 E.00162
; LINE_WIDTH: 0.213895
G1 X132.609 Y124.718 E.00223
; LINE_WIDTH: 0.260685
G1 X132.64 Y124.88 E.00284
; CHANGE_LAYER
; Z_HEIGHT: 9.4
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.609 Y124.718 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 47/50
; update layer progress
M73 L47
M991 S0 P46 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z9.6 I.071 J-1.215 P1  F30000
G1 X124.116 Y124.219 Z9.6
G1 Z9.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1932
G1 X124.116 Y123.758 E.01484
G1 X127.171 Y121.994 E.11343
G1 X128 Y121.515 E.03079
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1932
G1 X127.374 Y122.346 E.0986
M73 P90 R1
G1 X128 Y121.985 E.02323
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.007 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1932
M204 S5000
G1 X127.57 Y122.686 E.09133
G1 X128 Y122.438 E.01478
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.773 Y123.764 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I1.217 J-.007 P1  F30000
G1 X125.759 Y121.399 Z9.8
G1 Z9.4
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1932
G1 X125.135 Y121.759 E.02316
G3 X124.998 Y121.27 I2.401 J-.937 E.01635
G1 X125.012 Y121.148 E.00396
G1 X125.065 Y121.063 E.00319
G1 X125.168 Y120.997 E.00397
G1 X125.267 Y120.984 E.00318
G1 X125.405 Y121.036 E.00474
G3 X125.721 Y121.352 I-1.662 J1.978 E.01442
G1 X126.414 Y121.49 F30000
G1 F1932
G1 X124.887 Y122.372 E.05671
G1 X124.606 Y121.387 E.03295
G3 X125.293 Y120.577 I.649 J-.146 E.03957
G3 X125.702 Y120.754 I-.049 J.673 E.0146
G1 X126.373 Y121.447 E.03101
; WIPE_START
G1 F11054.348
G1 X125.524 Y121.976 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I.417 J1.143 P1  F30000
G1 X127.866 Y121.123 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X123.843 Y123.445 E.14935
G1 X123.711 Y123.301 E.00629
G3 X124.458 Y122.35 I5.196 J3.31 E.03895
G1 X124.209 Y121.479 E.02911
G3 X125.32 Y120.17 I1.048 J-.237 E.06396
G3 X125.981 Y120.457 I-.079 J1.087 E.0236
G1 X126.61 Y121.107 E.02911
G3 X127.807 Y120.936 I1.466 J5.981 E.03895
G1 X127.848 Y121.065 E.00436
; WIPE_START
G1 F11054.348
G1 X126.988 Y121.576 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-.857 J-.864 P1  F30000
G1 X122.895 Y125.64 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X122.895 Y126.36 E.02316
G3 X122.403 Y126.234 I.396 J-2.574 E.01635
G1 X122.289 Y126.141 E.00474
G1 X122.246 Y126 E.00474
G1 X122.289 Y125.859 E.00473
G1 X122.403 Y125.765 E.00475
G3 X122.836 Y125.65 I.884 J2.433 E.01442
G1 X123.302 Y125.118 F30000
G1 F1932
G1 X123.302 Y126.882 E.05671
G1 X122.308 Y126.633 E.03293
G3 X122.308 Y125.367 I.196 J-.633 E.05412
G1 X123.244 Y125.133 E.03102
; WIPE_START
G1 F11054.348
G1 X123.277 Y126.132 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I1.187 J.268 P1  F30000
G1 X123.709 Y124.219 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X123.709 Y128.318 E.1318
G1 X123.522 Y128.363 E.00618
G1 X123.383 Y128.092 E.00979
G1 X123.045 Y127.237 E.02956
G1 X122.19 Y127.023 E.02835
G3 X122.19 Y124.977 I.317 J-1.023 E.08747
G1 X123.015 Y124.77 E.02736
G1 X123.454 Y123.758 E.03548
G1 X123.526 Y123.628 E.00477
G1 X123.709 Y123.676 E.00608
G1 X123.709 Y124.159 E.01553
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I.522 J1.099 P1  F30000
G1 X130.865 Y121.759 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X130.241 Y121.399 E.02317
G3 X130.596 Y121.035 I2.017 J1.616 E.01636
G1 X130.684 Y120.992 E.00316
G1 X130.766 Y120.984 E.00264
G1 X130.877 Y121.017 E.00374
G1 X130.951 Y121.082 E.00318
G1 X130.995 Y121.171 E.00318
G1 X131.002 Y121.27 E.00319
G3 X130.886 Y121.703 I-2.562 J-.454 E.01443
G1 X131.113 Y122.372 F30000
G1 F1932
G1 X129.585 Y121.49 E.05671
G1 X130.298 Y120.754 E.03294
G3 X130.799 Y120.578 I.453 J.487 E.01758
G3 X131.394 Y121.387 I-.055 J.664 E.03657
G1 X131.129 Y122.314 E.03101
; WIPE_START
G1 F11054.348
G1 X130.247 Y121.844 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-.782 J.932 P1  F30000
G1 X132.153 Y123.443 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X128.133 Y121.122 E.14926
G1 X128.183 Y120.94 E.00608
G1 X128.332 Y120.942 E.00477
G1 X129.428 Y121.068 E.03548
G1 X130.019 Y120.457 E.02735
G3 X130.832 Y120.172 I.732 J.787 E.0285
G3 X131.791 Y121.48 I-.092 J1.073 E.05901
G1 X131.549 Y122.327 E.02835
G1 X132.12 Y123.047 E.02955
G1 X132.285 Y123.303 E.00979
G1 X132.194 Y123.399 E.00425
; WIPE_START
G1 F11054.348
G1 X131.322 Y122.91 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-1.081 J.559 P1  F30000
G1 X133.105 Y126.36 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X133.105 Y125.64 E.02316
G1 X133.574 Y125.757 E.01552
G1 X133.696 Y125.839 E.00474
G1 X133.753 Y125.975 E.00475
G1 X133.749 Y126.049 E.00239
G1 X133.711 Y126.141 E.00318
G1 X133.597 Y126.234 E.00474
G3 X133.164 Y126.35 I-.88 J-2.418 E.01443
G1 X132.995 Y126.807 F30000
G1 F1932
G1 X132.698 Y126.882 E.00984
G1 X132.698 Y125.118 E.05671
G1 X133.692 Y125.367 E.03294
G3 X133.692 Y126.633 I-.196 J.633 E.05412
G1 X133.053 Y126.793 E.02117
G1 X132.891 Y127.446 F30000
G1 F1932
G1 X132.546 Y128.242 E.02788
G1 X132.474 Y128.372 E.00477
G1 X132.291 Y128.324 E.00608
G1 X132.291 Y123.682 E.14926
G1 X132.478 Y123.637 E.00618
G1 X132.617 Y123.908 E.00979
G1 X132.955 Y124.763 E.02955
G1 X133.81 Y124.977 E.02836
G3 X133.81 Y127.023 I-.318 J1.023 E.08747
G1 X132.985 Y127.23 E.02735
G1 X132.915 Y127.391 E.00567
; WIPE_START
G1 F11054.348
G1 X132.546 Y128.242 E-.35229
G1 X132.511 Y128.306 E-.02771
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-.927 J-.788 P1  F30000
G1 X130.865 Y130.241 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X130.997 Y130.706 E.01553
G1 X130.988 Y130.852 E.00473
G1 X130.951 Y130.918 E.00239
G1 X130.877 Y130.983 E.00318
G1 X130.733 Y131.016 E.00474
G1 X130.596 Y130.965 E.00474
G3 X130.241 Y130.601 I1.669 J-1.986 E.01635
G1 X130.813 Y130.271 E.02123
G1 X131.113 Y129.628 F30000
G1 F1932
G1 X131.394 Y130.613 E.03294
G3 X130.298 Y131.246 I-.645 J.149 E.05425
G1 X129.585 Y130.51 E.03294
G1 X131.061 Y129.658 E.05478
; WIPE_START
G1 F11054.348
G1 X131.39 Y130.602 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I1.14 J.427 P1  F30000
G1 X132.157 Y128.555 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X132.289 Y128.699 E.00629
G3 X131.542 Y129.65 I-5.195 J-3.309 E.03895
G1 X131.791 Y130.52 E.0291
G3 X130.019 Y131.543 I-1.042 J.241 E.08767
G1 X129.39 Y130.893 E.0291
G3 X128.193 Y131.064 I-1.466 J-5.983 E.03895
G1 X128.134 Y130.877 E.00629
G1 X132.105 Y128.585 E.14742
; WIPE_START
G1 F11054.348
G1 X132.289 Y128.699 E-.08234
G1 X132.021 Y129.086 E-.17881
G1 X131.819 Y129.324 E-.11885
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-.251 J-1.191 P1  F30000
G1 X125.759 Y130.601 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G3 X125.405 Y130.964 I-2.013 J-1.612 E.01635
G1 X125.266 Y131.016 E.00474
G1 X125.123 Y130.983 E.00473
G1 X125.022 Y130.875 E.00474
G1 X124.998 Y130.73 E.00474
G3 X125.135 Y130.241 I2.559 J.454 E.01635
G1 X125.707 Y130.571 E.02124
G1 X126.415 Y130.51 F30000
G1 F1932
G1 X125.702 Y131.246 E.03294
G3 X124.606 Y130.613 I-.45 J-.487 E.05412
G1 X124.887 Y129.628 E.03294
G1 X126.363 Y130.48 E.05479
; WIPE_START
G1 F11054.348
G1 X125.71 Y131.237 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I.999 J-.695 P1  F30000
G1 X123.847 Y128.558 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X127.867 Y130.878 E.14926
G1 X127.817 Y131.06 E.00608
G1 X127.668 Y131.058 E.00477
G1 X126.572 Y130.932 E.03548
G1 X125.981 Y131.543 E.02736
G3 X124.209 Y130.52 I-.727 J-.787 E.08746
G1 X124.451 Y129.672 E.02836
G1 X123.88 Y128.952 E.02956
G1 X123.715 Y128.697 E.00978
G1 X123.806 Y128.601 E.00425
; WIPE_START
G1 F11054.348
G1 X124.678 Y129.09 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I.193 J1.202 P1  F30000
G1 X133.216 Y127.721 Z9.8
G1 Z9.4
G1 E.4 F1800
G1 F1932
G1 X132.912 Y128.422 E.02457
G3 X131.994 Y129.748 I-5.481 J-2.816 E.05199
G1 X132.188 Y130.428 E.02275
G3 X129.741 Y131.841 I-1.439 J.333 E.1211
G1 X129.249 Y131.332 E.02275
G3 X127.642 Y131.465 I-1.305 J-6.02 E.052
G1 X126.725 Y131.359 E.02967
G1 X126.259 Y131.841 E.02155
G3 X123.812 Y130.428 I-1.004 J-1.086 E.12081
G1 X124.002 Y129.762 E.02228
M73 P91 R1
G3 X122.743 Y127.581 I4.568 J-4.091 E.08154
G1 X122.072 Y127.413 E.02227
G3 X122.071 Y124.587 I.438 J-1.413 E.12082
G1 X122.721 Y124.424 E.02155
G1 X123.088 Y123.578 E.02967
G3 X124.006 Y122.252 I5.481 J2.816 E.05199
G1 X123.812 Y121.572 E.02275
G3 X125.347 Y119.764 I1.448 J-.327 E.08836
G3 X126.259 Y120.159 I-.109 J1.502 E.0326
G1 X126.751 Y120.668 E.02275
G3 X128.358 Y120.535 I1.305 J6.02 E.052
G1 X129.275 Y120.641 E.02967
G1 X129.741 Y120.159 E.02154
G3 X132.188 Y121.572 I1.008 J1.08 E.1211
G1 X131.998 Y122.238 E.02227
G3 X133.257 Y124.419 I-4.569 J4.091 E.08154
G1 X133.929 Y124.587 E.02228
G3 X133.928 Y127.413 I-.439 J1.413 E.12081
G1 X133.279 Y127.576 E.02154
G1 X133.239 Y127.666 E.00317
G1 X133.54 Y127.996 F30000
G1 F1932
G1 X133.277 Y128.603 E.02125
G3 X132.445 Y129.845 I-5.519 J-2.797 E.04821
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.63 Y130.886 I-2.74 J1.024 E.0342
G3 X129.462 Y132.138 I-1.886 J-.138 E.13637
G1 X129.108 Y131.772 E.01639
G3 X126.878 Y131.787 I-1.155 J-6.078 E.07208
G3 X125.914 Y132.526 I-1.959 J-1.556 E.03948
G3 X123.415 Y130.335 I-.652 J-1.776 E.13044
G1 X123.553 Y129.851 E.0162
G3 X122.442 Y127.925 I4.341 J-3.79 E.07196
G3 X121.453 Y127.566 I.484 J-2.873 E.034
G3 X121.953 Y124.197 I1.051 J-1.566 E.13669
G1 X122.428 Y124.078 E.01574
G3 X123.555 Y122.155 I5.814 J2.116 E.07208
G3 X123.37 Y121.114 I2.739 J-1.024 E.03419
G3 X126.538 Y119.862 I1.886 J.138 E.13637
G1 X126.892 Y120.228 E.0164
G3 X129.122 Y120.213 I1.155 J6.079 E.07208
G3 X130.086 Y119.474 I1.959 J1.556 E.03948
G3 X130.899 Y119.361 I.665 J1.808 E.02658
G3 X132.585 Y121.665 I-.167 J1.891 E.10389
G1 X132.447 Y122.149 E.01619
G3 X133.558 Y124.075 I-4.342 J3.79 E.07196
G3 X134.547 Y124.434 I-.484 J2.874 E.034
G3 X134.695 Y127.456 I-1.052 J1.567 E.11292
G3 X133.572 Y127.922 I-1.49 J-2.009 E.03948
G1 X133.564 Y127.941 E.00068
M204 S250
G1 X133.855 Y128.255 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1932
M204 S5000
G3 X132.879 Y129.939 I-5.585 J-2.112 E.05823
G3 X128.972 Y132.195 I-2.135 J.814 E.19216
G1 X128.819 Y132.223 E.00461
G3 X127.025 Y132.198 I-.802 J-6.92 E.05358
G3 X123.121 Y129.937 I-1.765 J-1.453 E.19165
G3 X122.151 Y128.257 I4.122 J-3.5 E.05811
G3 X122.145 Y123.745 I.37 J-2.256 E.19165
G3 X123.121 Y122.061 I5.585 J2.112 E.05823
G3 X127.028 Y119.805 I2.135 J-.814 E.19216
G1 X127.181 Y119.777 E.00461
G3 X128.975 Y119.802 I.802 J6.921 E.05358
G3 X130.931 Y118.97 I1.811 J1.543 E.06564
G3 X132.879 Y122.063 I-.187 J2.278 E.12616
G3 X133.849 Y123.743 I-4.123 J3.501 E.05811
G3 X133.914 Y128.245 I-.37 J2.256 E.18987
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.629 Y128.776 E-.22918
G1 X133.436 Y129.123 E-.15082
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I1.216 J.043 P1  F30000
G1 X133.548 Y126.005 Z9.8
G1 Z9.4
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.143794
G1 F1932
G1 X133.309 Y125.973 E.00192
; WIPE_START
G1 F15000
G1 X133.548 Y126.005 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I.941 J-.772 P1  F30000
G1 X132.636 Y124.893 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.25421
G1 F1932
G1 X132.606 Y124.736 E.00265
; LINE_WIDTH: 0.20927
G1 X132.576 Y124.58 E.00209
; LINE_WIDTH: 0.16433
G1 X132.546 Y124.424 E.00153
; LINE_WIDTH: 0.11939
G1 X132.517 Y124.268 E.00096
; WIPE_START
G1 F15000
G1 X132.546 Y124.424 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I1.073 J-.575 P1  F30000
G1 X131.759 Y122.955 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.119393
G1 F1932
G1 X131.638 Y122.851 E.00096
; LINE_WIDTH: 0.164355
G1 X131.518 Y122.747 E.00153
; LINE_WIDTH: 0.209316
G1 X131.397 Y122.643 E.00209
; LINE_WIDTH: 0.254277
G1 X131.277 Y122.539 E.00266
; WIPE_START
G1 F15000
G1 X131.397 Y122.643 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I1.039 J-.633 P1  F30000
G1 X130.634 Y121.391 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.141488
G1 F1932
G3 X130.751 Y121.236 I.399 J.179 E.00152
G1 X130.798 Y121.23 E.00037
; WIPE_START
G1 F15000
G1 X130.751 Y121.236 E-.07554
G1 X130.634 Y121.391 E-.30446
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I.061 J-1.215 P1  F30000
G1 X127.242 Y121.222 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.117638
G1 F1932
G1 X127.094 Y121.276 E.00093
; LINE_WIDTH: 0.159075
G1 X126.945 Y121.331 E.00145
; LINE_WIDTH: 0.200513
G1 X126.797 Y121.385 E.00197
; LINE_WIDTH: 0.24195
G1 X126.649 Y121.44 E.00248
; WIPE_START
G1 F15000
G1 X126.797 Y121.385 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-.005 J-1.217 P1  F30000
G1 X125.366 Y121.391 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.141106
G1 F1932
G1 X125.225 Y121.195 E.00187
; WIPE_START
G1 F15000
G1 X125.366 Y121.391 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-1.065 J-.588 P1  F30000
G1 X124.726 Y122.55 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.241985
G1 F1932
G1 X124.605 Y122.651 E.00249
; LINE_WIDTH: 0.20054
G1 X124.483 Y122.752 E.00197
; LINE_WIDTH: 0.159095
G1 X124.362 Y122.853 E.00145
; LINE_WIDTH: 0.117649
G1 X124.241 Y122.955 E.00093
; WIPE_START
G1 F15000
G1 X124.362 Y122.853 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-1.046 J-.622 P1  F30000
G1 X122.469 Y126.038 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.140974
G1 F1932
G1 X122.5 Y126 E.00038
G1 X122.691 Y125.977 E.00149
; WIPE_START
G1 F15000
G1 X122.5 Y126 E-.30275
G1 X122.469 Y126.038 E-.07725
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-.933 J.781 P1  F30000
G1 X123.364 Y127.107 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.254263
G1 F1932
G1 X123.394 Y127.264 E.00266
; LINE_WIDTH: 0.209309
G1 X123.424 Y127.42 E.00209
; LINE_WIDTH: 0.164355
G1 X123.454 Y127.576 E.00153
; LINE_WIDTH: 0.1194
G1 X123.483 Y127.733 E.00096
; WIPE_START
G1 F15000
G1 X123.454 Y127.576 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-1.073 J.575 P1  F30000
G1 X124.241 Y129.045 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.119387
G1 F1932
G1 X124.362 Y129.149 E.00096
; LINE_WIDTH: 0.164334
G1 X124.482 Y129.253 E.00153
; LINE_WIDTH: 0.209281
G1 X124.603 Y129.357 E.00209
; LINE_WIDTH: 0.254227
G1 X124.723 Y129.461 E.00266
; WIPE_START
G1 F15000
G1 X124.603 Y129.357 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-1.049 J.617 P1  F30000
G1 X125.326 Y130.586 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.140998
G1 F1932
G1 X125.25 Y130.763 E.00149
G1 X125.268 Y130.809 E.00038
; WIPE_START
G1 F15000
G1 X125.25 Y130.763 E-.07714
G1 X125.326 Y130.586 E-.30286
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-.068 J1.215 P1  F30000
G1 X128.758 Y130.778 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.11764
G1 F1932
G1 X128.906 Y130.724 E.00093
; LINE_WIDTH: 0.159082
G1 X129.055 Y130.669 E.00145
; LINE_WIDTH: 0.200524
G1 X129.203 Y130.615 E.00197
; LINE_WIDTH: 0.241966
G1 X129.351 Y130.56 E.00249
; WIPE_START
G1 F15000
G1 X129.203 Y130.615 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I-.148 J1.208 P1  F30000
G1 X130.77 Y130.807 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.143806
G1 F1932
G1 X130.679 Y130.584 E.00192
; WIPE_START
G1 F15000
G1 X130.77 Y130.807 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z9.8 I1.141 J.424 P1  F30000
G1 X131.274 Y129.451 Z9.8
G1 Z9.4
G1 E.4 F1800
; LINE_WIDTH: 0.241986
G1 F1932
G1 X131.395 Y129.349 E.00249
; LINE_WIDTH: 0.200541
G1 X131.517 Y129.248 E.00197
; LINE_WIDTH: 0.159095
G1 X131.638 Y129.147 E.00145
; LINE_WIDTH: 0.117649
G1 X131.759 Y129.045 E.00093
; CHANGE_LAYER
; Z_HEIGHT: 9.6
; LAYER_HEIGHT: 0.200001
; WIPE_START
G1 F15000
G1 X131.638 Y129.147 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 48/50
; update layer progress
M73 L48
M991 S0 P47 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z9.8 I.667 J-1.018 P1  F30000
G1 X124.116 Y124.219 Z9.8
G1 Z9.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1835
G1 X124.116 Y123.758 E.01484
G1 X127.264 Y121.94 E.11688
G1 X128 Y121.515 E.02734
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1835
M73 P92 R1
G1 X127.467 Y122.293 E.10204
G1 X128 Y121.985 E.01979
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.007 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.008 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1835
M204 S5000
G1 X127.663 Y122.632 E.09452
G1 X128 Y122.438 E.01159
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.773 Y123.765 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I1.217 J-.031 P1  F30000
G1 X125.712 Y121.426 Z10
G1 Z9.6
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1835
G1 X125.182 Y121.732 E.01968
G3 X125.051 Y121.263 I2.304 J-.901 E.01567
G1 X125.056 Y121.185 E.00254
G1 X125.103 Y121.099 E.00314
G1 X125.185 Y121.046 E.00315
G1 X125.263 Y121.036 E.00252
G1 X125.373 Y121.077 E.00376
G3 X125.674 Y121.379 I-1.592 J1.894 E.01375
G1 X126.368 Y121.517 F30000
G1 F1835
G1 X124.934 Y122.345 E.05323
G1 X124.657 Y121.375 E.03244
G3 X125.254 Y120.629 I.593 J-.137 E.03532
G3 X125.666 Y120.792 I-.018 J.646 E.01456
G1 X126.326 Y121.474 E.03051
; WIPE_START
G1 F11054.348
G1 X125.478 Y122.005 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I.412 J1.145 P1  F30000
G1 X127.759 Y121.184 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X123.95 Y123.383 E.14145
G1 X123.817 Y123.24 E.00628
G1 X124.02 Y122.946 E.01148
G1 X124.516 Y122.362 E.02462
G1 X124.26 Y121.468 E.02992
G3 X125.26 Y120.222 I.991 J-.229 E.05909
G3 X125.945 Y120.495 I-.033 J1.078 E.02419
G1 X126.592 Y121.164 E.02993
G1 X127.345 Y121.027 E.02463
G1 X127.701 Y120.997 E.01147
G1 X127.741 Y121.127 E.00436
; WIPE_START
G1 F11054.348
G1 X126.882 Y121.638 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-.868 J-.853 P1  F30000
G1 X122.895 Y125.694 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X122.895 Y126.306 E.01968
G3 X122.423 Y126.186 I.371 J-2.441 E.01568
G1 X122.333 Y126.112 E.00375
G1 X122.299 Y126 E.00377
G1 X122.333 Y125.888 E.00375
G1 X122.423 Y125.814 E.00375
G3 X122.836 Y125.704 I.846 J2.334 E.01375
G1 X123.302 Y125.172 F30000
G1 F1835
G1 X123.302 Y126.828 E.05323
G1 X122.323 Y126.583 E.03243
G3 X122.323 Y125.417 I.181 J-.583 E.04982
G1 X123.244 Y125.187 E.0305
; WIPE_START
G1 F11054.348
G1 X123.279 Y126.186 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I1.189 J.26 P1  F30000
G1 X123.709 Y124.219 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X123.709 Y128.203 E.1281
G1 X123.522 Y128.248 E.00618
G1 X123.431 Y128.07 E.00642
G1 X123.084 Y127.193 E.03034
G1 X122.205 Y126.973 E.02914
G3 X122.205 Y125.027 I.302 J-.973 E.08316
G1 X123.053 Y124.815 E.02811
G1 X123.514 Y123.751 E.03729
G1 X123.709 Y123.791 E.00639
G1 X123.709 Y124.159 E.01182
; WIPE_START
M73 P92 R0
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I.528 J1.096 P1  F30000
G1 X130.818 Y121.732 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X130.288 Y121.426 E.01968
G3 X130.628 Y121.077 I1.919 J1.532 E.01568
G1 X130.698 Y121.043 E.00252
G1 X130.776 Y121.037 E.00252
G1 X130.851 Y121.063 E.00253
G1 X130.91 Y121.114 E.00252
G1 X130.944 Y121.185 E.00252
G1 X130.95 Y121.263 E.00253
G3 X130.839 Y121.676 I-2.48 J-.445 E.01376
G1 X131.066 Y122.345 F30000
G1 F1835
G1 X129.632 Y121.517 E.05323
G1 X130.334 Y120.793 E.03244
G3 X130.806 Y120.631 I.417 J.449 E.01652
G3 X131.343 Y121.375 I-.057 J.606 E.03339
G1 X131.082 Y122.287 E.03051
; WIPE_START
G1 F11054.348
G1 X130.199 Y121.818 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-.785 J.93 P1  F30000
G1 X132.053 Y123.385 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X128.233 Y121.179 E.14185
G1 X128.295 Y120.991 E.00639
G1 X129.447 Y121.123 E.0373
G1 X130.055 Y120.495 E.02811
G3 X130.839 Y120.226 I.696 J.749 E.02745
G3 X131.74 Y121.468 I-.09 J1.013 E.05589
G1 X131.491 Y122.339 E.02914
G1 X132.077 Y123.078 E.03034
G1 X132.186 Y123.246 E.00642
G1 X132.094 Y123.342 E.00425
; WIPE_START
G1 F11054.348
G1 X131.222 Y122.853 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-1.068 J.583 P1  F30000
G1 X133.105 Y126.306 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X133.105 Y125.694 E.01968
G1 X133.558 Y125.807 E.01502
G1 X133.656 Y125.872 E.00375
G1 X133.701 Y126 E.00436
G1 X133.667 Y126.112 E.00376
G1 X133.577 Y126.186 E.00375
G3 X133.164 Y126.296 I-.846 J-2.334 E.01375
G1 X132.952 Y126.764 F30000
G1 F1835
G1 X132.698 Y126.828 E.0084
G1 X132.698 Y125.172 E.05323
G1 X133.677 Y125.417 E.03244
G3 X133.677 Y126.583 I-.181 J.583 E.04981
G1 X133.01 Y126.75 E.0221
G1 X133.171 Y127.129 F30000
G1 F1835
G1 X132.947 Y127.185 E.00743
G1 X132.486 Y128.249 E.03729
G1 X132.291 Y128.209 E.00639
G1 X132.291 Y123.797 E.14185
G1 X132.478 Y123.752 E.00618
G1 X132.569 Y123.93 E.00641
G1 X132.916 Y124.807 E.03034
G1 X133.795 Y125.027 E.02914
G3 X133.795 Y126.973 I-.302 J.973 E.08316
G1 X133.229 Y127.114 E.01875
; WIPE_START
G1 F11054.348
G1 X132.947 Y127.185 E-.11056
G1 X132.665 Y127.836 E-.26944
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-.969 J-.736 P1  F30000
G1 X130.818 Y130.268 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X130.946 Y130.718 E.01502
G1 X130.938 Y130.834 E.00375
G1 X130.851 Y130.937 E.00435
G1 X130.737 Y130.964 E.00376
G1 X130.628 Y130.923 E.00376
G3 X130.288 Y130.574 I1.598 J-1.899 E.01568
G1 X130.766 Y130.298 E.01775
G1 X131.066 Y129.655 F30000
G1 F1835
G1 X131.343 Y130.625 E.03244
G3 X130.334 Y131.207 I-.595 J.135 E.04981
G1 X129.632 Y130.483 E.03243
G1 X131.014 Y129.685 E.0513
; WIPE_START
G1 F11054.348
G1 X131.343 Y130.625 E-.37844
G1 X131.343 Y130.629 E-.00156
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I1.148 J.403 P1  F30000
G1 X132.05 Y128.617 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X132.183 Y128.76 E.00629
G1 X131.98 Y129.054 E.01148
G1 X131.484 Y129.638 E.02462
G1 X131.74 Y130.532 E.02991
G3 X130.055 Y131.505 I-.993 J.225 E.08316
G1 X129.408 Y130.836 E.02992
G1 X128.655 Y130.973 E.02463
G1 X128.299 Y131.003 E.01147
G1 X128.241 Y130.816 E.00629
G1 X131.998 Y128.647 E.13952
; WIPE_START
G1 F11054.348
G1 X132.183 Y128.76 E-.08234
G1 X131.98 Y129.054 E-.13566
G1 X131.704 Y129.379 E-.162
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-.238 J-1.193 P1  F30000
G1 X125.712 Y130.574 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G3 X125.372 Y130.923 I-1.937 J-1.549 E.01568
G1 X125.263 Y130.964 E.00376
G1 X125.149 Y130.937 E.00375
G1 X125.07 Y130.852 E.00375
G1 X125.05 Y130.737 E.00376
G3 X125.182 Y130.268 I2.472 J.443 E.01568
G1 X125.66 Y130.544 E.01775
G1 X126.368 Y130.483 F30000
G1 F1835
G1 X125.666 Y131.207 E.03243
G3 X124.657 Y130.625 I-.416 J-.445 E.04993
G1 X124.934 Y129.655 E.03244
G1 X126.316 Y130.453 E.0513
; WIPE_START
G1 F11054.348
G1 X125.666 Y131.207 E-.37838
G1 X125.663 Y131.21 E-.00162
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I1.015 J-.671 P1  F30000
G1 X123.947 Y128.615 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X127.767 Y130.821 E.14185
G1 X127.705 Y131.009 E.00639
G1 X126.553 Y130.877 E.0373
G1 X125.945 Y131.505 E.0281
G3 X124.26 Y130.532 I-.694 J-.743 E.08336
G1 X124.509 Y129.661 E.02914
G1 X123.922 Y128.922 E.03034
G1 X123.814 Y128.754 E.00642
G1 X123.906 Y128.658 E.00425
; WIPE_START
G1 F11054.348
G1 X124.778 Y129.147 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I.229 J1.195 P1  F30000
G1 X133.39 Y127.494 Z10
G1 Z9.6
G1 E.4 F1800
G1 F1835
G1 X133.241 Y127.531 E.00493
G1 X132.865 Y128.399 E.03042
G3 X131.935 Y129.735 I-5.491 J-2.826 E.05249
G1 X132.137 Y130.44 E.02356
G3 X129.777 Y131.802 I-1.392 J.315 E.11651
G1 X129.267 Y131.276 E.02357
G3 X127.645 Y131.412 I-1.323 J-6.018 E.05249
M73 P93 R0
G1 X126.705 Y131.304 E.03042
G1 X126.223 Y131.802 E.02229
G3 X123.863 Y130.44 I-.972 J-1.041 E.11678
G1 X124.06 Y129.75 E.02306
G3 X122.782 Y127.537 I4.595 J-4.129 E.08278
G1 X122.087 Y127.363 E.02306
G3 X122.087 Y124.637 I.423 J-1.363 E.11651
G1 X122.759 Y124.469 E.0223
G1 X123.136 Y123.601 E.03042
G3 X124.065 Y122.265 I5.481 J2.82 E.05248
G1 X123.863 Y121.56 E.02357
G3 X125.267 Y119.815 I1.388 J-.321 E.08287
G3 X126.223 Y120.198 I-.05 J1.51 E.0338
G1 X126.733 Y120.724 E.02357
G3 X128.355 Y120.588 I1.324 J6.019 E.05248
G1 X129.294 Y120.696 E.03042
G1 X129.777 Y120.198 E.0223
G3 X132.137 Y121.56 I.97 J1.045 E.11663
G1 X131.94 Y122.25 E.02306
G3 X133.218 Y124.463 I-4.595 J4.128 E.08278
G1 X133.913 Y124.637 E.02306
G3 X133.913 Y127.363 I-.423 J1.363 E.11651
G1 X133.448 Y127.479 E.01544
G1 X133.504 Y127.947 F30000
G1 F1835
G1 X133.23 Y128.579 E.02217
G3 X132.387 Y129.833 I-5.546 J-2.821 E.0487
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.578 Y130.883 I-2.727 J1.038 E.03452
G3 X129.498 Y132.1 I-1.829 J-.123 E.13288
G1 X129.126 Y131.715 E.01721
G3 X126.858 Y131.732 I-1.178 J-6.108 E.07332
G3 X126.06 Y132.406 I-2.223 J-1.823 E.03379
G3 X123.466 Y130.347 I-.8 J-1.655 E.13257
G1 X123.611 Y129.84 E.01698
G3 X122.481 Y127.881 I4.368 J-3.827 E.07319
G3 X121.483 Y127.523 I.465 J-2.867 E.03429
G3 X121.968 Y124.247 I1.021 J-1.522 E.13287
G1 X122.466 Y124.123 E.01649
G3 X123.613 Y122.167 I5.849 J2.119 E.07332
G3 X123.422 Y121.117 I2.726 J-1.038 E.03452
G3 X125.274 Y119.408 I1.846 J.142 E.08912
G3 X126.502 Y119.9 I-.066 J1.943 E.04342
G1 X126.874 Y120.285 E.01722
G3 X129.142 Y120.268 I1.178 J6.107 E.07332
G3 X129.94 Y119.594 I2.223 J1.822 E.03379
G3 X132.534 Y121.653 I.808 J1.646 E.13288
G1 X132.389 Y122.16 E.01698
G3 X133.519 Y124.119 I-4.368 J3.828 E.07319
G3 X134.517 Y124.477 I-.466 J2.867 E.03429
G3 X134.032 Y127.753 I-1.021 J1.522 E.13287
G1 X133.534 Y127.877 E.01649
G1 X133.528 Y127.892 E.00051
M204 S250
G1 X133.816 Y128.213 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1835
M204 S5000
G1 X133.582 Y128.753 E.01752
G3 X132.821 Y129.926 I-5.379 J-2.654 E.04176
G3 X128.99 Y132.138 I-2.083 J.816 E.18933
G3 X127.006 Y132.143 I-1.006 J-5.912 E.05937
G3 X123.179 Y129.926 I-1.749 J-1.393 E.18959
G3 X122.19 Y128.212 I4.149 J-3.537 E.05925
G3 X122.183 Y123.79 I.334 J-2.212 E.18916
G3 X123.179 Y122.074 I5.613 J2.111 E.05937
G3 X125.28 Y119.016 I2.093 J-.813 E.13006
G3 X127.01 Y119.862 I-.043 J2.28 E.05922
G3 X128.994 Y119.857 I1.006 J5.912 E.05937
G3 X132.821 Y122.075 I1.746 J1.397 E.18935
G3 X133.81 Y123.788 I-4.149 J3.537 E.05925
G3 X133.873 Y128.201 I-.334 J2.212 E.18746
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.582 Y128.753 E-.23712
G1 X133.399 Y129.082 E-.14288
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-.029 J-1.217 P1  F30000
G1 X131.625 Y129.123 Z10
G1 Z9.6
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.119396
G1 F1835
G1 X131.49 Y129.235 E.00106
; LINE_WIDTH: 0.16436
G1 X131.356 Y129.347 E.00168
; LINE_WIDTH: 0.209325
G1 X131.222 Y129.459 E.0023
; WIPE_START
G1 F15000
G1 X131.356 Y129.347 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-.622 J-1.046 P1  F30000
G1 X129.385 Y130.52 Z10
G1 Z9.6
G1 E.4 F1800
; LINE_WIDTH: 0.209121
G1 F1835
G1 X129.221 Y130.58 E.00229
; LINE_WIDTH: 0.16424
G1 X129.057 Y130.64 E.00167
; LINE_WIDTH: 0.11936
G1 X128.893 Y130.7 E.00105
; WIPE_START
G1 F15000
G1 X129.057 Y130.64 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I.321 J-1.174 P1  F30000
G1 X124.775 Y129.47 Z10
G1 Z9.6
G1 E.4 F1800
; LINE_WIDTH: 0.228428
G1 F1835
G1 X124.673 Y129.382 E.00198
; LINE_WIDTH: 0.190852
G1 X124.57 Y129.294 E.00158
; LINE_WIDTH: 0.153276
G1 X124.468 Y129.205 E.00118
; LINE_WIDTH: 0.115701
G1 X124.365 Y129.117 E.00078
; WIPE_START
G1 F15000
G1 X124.468 Y129.205 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I1.039 J-.633 P1  F30000
G1 X123.483 Y127.59 Z10
G1 Z9.6
G1 E.4 F1800
; LINE_WIDTH: 0.115713
G1 F1835
G1 X123.458 Y127.457 E.00078
; LINE_WIDTH: 0.153298
G1 X123.433 Y127.324 E.00118
; LINE_WIDTH: 0.190883
G1 X123.407 Y127.191 E.00158
; LINE_WIDTH: 0.228468
G1 X123.382 Y127.058 E.00198
; WIPE_START
G1 F15000
G1 X123.407 Y127.191 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I1.187 J.267 P1  F30000
G1 X124.376 Y122.877 Z10
G1 Z9.6
G1 E.4 F1800
; LINE_WIDTH: 0.119376
G1 F1835
G1 X124.51 Y122.765 E.00106
; LINE_WIDTH: 0.16427
G1 X124.644 Y122.653 E.00168
; LINE_WIDTH: 0.209163
G1 X124.778 Y122.541 E.00229
; WIPE_START
G1 F15000
G1 X124.644 Y122.653 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I.622 J1.046 P1  F30000
G1 X126.615 Y121.48 Z10
G1 Z9.6
G1 E.4 F1800
; LINE_WIDTH: 0.209115
G1 F1835
G1 X126.779 Y121.42 E.00229
; LINE_WIDTH: 0.164236
G1 X126.943 Y121.36 E.00167
; LINE_WIDTH: 0.119358
G1 X127.107 Y121.3 E.00105
; WIPE_START
G1 F15000
G1 X126.943 Y121.36 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-.321 J1.174 P1  F30000
G1 X131.225 Y122.53 Z10
G1 Z9.6
G1 E.4 F1800
; LINE_WIDTH: 0.228465
G1 F1835
G1 X131.327 Y122.618 E.00198
; LINE_WIDTH: 0.190879
G1 X131.43 Y122.706 E.00158
; LINE_WIDTH: 0.153293
G1 X131.532 Y122.795 E.00118
; LINE_WIDTH: 0.115706
G1 X131.635 Y122.883 E.00078
; WIPE_START
G1 F15000
G1 X131.532 Y122.795 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10 I-1.039 J.633 P1  F30000
G1 X132.517 Y124.41 Z10
G1 Z9.6
G1 E.4 F1800
; LINE_WIDTH: 0.11571
G1 F1835
G1 X132.542 Y124.543 E.00078
; LINE_WIDTH: 0.15329
G1 X132.567 Y124.676 E.00118
; LINE_WIDTH: 0.19087
G1 X132.593 Y124.809 E.00158
; LINE_WIDTH: 0.22845
G1 X132.618 Y124.942 E.00198
; CHANGE_LAYER
; Z_HEIGHT: 9.8
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X132.593 Y124.809 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 49/50
; update layer progress
M73 L49
M991 S0 P48 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z10 I.085 J-1.214 P1  F30000
G1 X124.116 Y124.219 Z10
G1 Z9.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1790
G1 X124.116 Y123.758 E.01484
G1 X127.356 Y121.887 E.12032
G1 X128 Y121.515 E.0239
G1 X131.884 Y123.758 E.14422
G1 X131.884 Y128.243 E.14422
G1 X128 Y130.485 E.14422
G1 X124.116 Y128.243 E.14422
G1 X124.116 Y124.279 E.12746
G1 X124.719 Y123.879 F30000
G1 F1790
G1 X127.56 Y122.239 E.10548
G1 X128 Y121.985 E.01634
G1 X131.477 Y123.993 E.12911
G1 X131.477 Y128.008 E.12911
G1 X128 Y130.015 E.12911
G1 X124.523 Y128.008 E.12911
G1 X124.523 Y123.993 E.12911
G1 X124.667 Y123.909 E.00535
M204 S250
M73 P94 R0
G1 X124.915 Y124.219 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1790
M204 S5000
G1 X127.756 Y122.579 E.09771
G1 X128 Y122.438 E.0084
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.773 Y123.765 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.19 J-.253 P1  F30000
G1 X125.324 Y121.651 Z10.2
G1 Z9.8
G1 E.4 F1800
; FEATURE: Inner wall
; LINE_WIDTH: 0.45
G1 F1790
G1 X125.231 Y121.415 E.00813
G1 X125.414 Y121.31 E.00677
G1 X125.57 Y121.507 E.00809
G1 X125.376 Y121.62 E.00723
G1 X126.183 Y121.624 F30000
G1 F1790
G1 X125.119 Y122.238 E.0395
G1 X124.785 Y121.394 E.02918
G3 X125.282 Y120.747 I.469 J-.154 E.03087
G3 X125.619 Y120.913 I-.047 J.519 E.01234
G1 X126.145 Y121.577 E.02726
; WIPE_START
G1 F11054.348
G1 X125.305 Y122.119 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I.412 J1.145 P1  F30000
G1 X127.524 Y121.32 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X124.185 Y123.248 E.12398
G1 X124.053 Y123.09 E.00661
G1 X124.711 Y122.314 E.0327
G1 X124.399 Y121.525 E.02728
G3 X125.309 Y120.341 I.853 J-.287 E.05666
G3 X125.925 Y120.644 I-.086 J.951 E.0226
G1 X126.452 Y121.309 E.02728
G1 X127.453 Y121.127 E.03271
G1 X127.503 Y121.263 E.00468
; WIPE_START
G1 F11054.348
G1 X126.645 Y121.777 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-.896 J-.823 P1  F30000
G1 X122.895 Y125.858 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X122.895 Y126.142 E.00915
G1 X122.645 Y126.105 E.00812
G1 X122.645 Y125.895 E.00678
G1 X122.835 Y125.867 E.00619
G1 X123.302 Y125.386 F30000
G1 F1790
G1 X123.302 Y126.614 E.0395
G1 X122.404 Y126.481 E.02918
G3 X122.404 Y125.519 I.099 J-.481 E.04323
G1 X123.242 Y125.395 E.02724
; WIPE_START
G1 F11054.348
G1 X123.291 Y126.393 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.195 J.23 P1  F30000
G1 X123.709 Y124.219 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X123.709 Y127.912 E.11877
G1 X123.51 Y127.95 E.0065
G1 X123.135 Y127.001 E.03282
G1 X122.325 Y126.881 E.02635
G3 X122.325 Y125.119 I.177 J-.881 E.07933
G1 X123.099 Y125.004 E.02518
G1 X123.514 Y124.048 E.03353
G1 X123.709 Y124.088 E.00639
G1 X123.709 Y124.159 E.00228
; WIPE_START
G1 F11054.348
G1 X123.709 Y125.159 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-1.162 J.362 P1  F30000
G1 X125.324 Y130.351 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X125.571 Y130.492 E.00915
G1 X125.414 Y130.69 E.00812
G1 X125.231 Y130.585 E.00678
G1 X125.302 Y130.406 E.00617
G1 X125.119 Y129.762 F30000
G1 F1790
G1 X126.183 Y130.376 E.0395
G1 X125.619 Y131.087 E.02918
G3 X124.785 Y130.605 I-.367 J-.326 E.04323
G1 X125.097 Y129.818 E.02724
; WIPE_START
G1 F11054.348
G1 X125.986 Y130.275 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I.787 J-.929 P1  F30000
G1 X124.198 Y128.76 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X127.51 Y130.672 E.12298
G1 X127.448 Y130.861 E.00639
G1 X126.412 Y130.742 E.03353
G1 X125.925 Y131.356 E.02519
G3 X124.399 Y130.474 I-.672 J-.597 E.07914
G1 X124.701 Y129.713 E.02634
G1 X124.066 Y128.913 E.03282
G1 X124.159 Y128.806 E.00457
; WIPE_START
G1 F11054.348
G1 X125.033 Y129.292 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-.224 J1.196 P1  F30000
G1 X130.676 Y130.35 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X130.769 Y130.585 E.00812
G1 X130.586 Y130.69 E.00677
G1 X130.43 Y130.493 E.0081
G1 X130.624 Y130.38 E.00723
G1 X130.881 Y129.762 F30000
G1 F1790
G1 X131.215 Y130.605 E.02917
G3 X130.381 Y131.087 I-.466 J.155 E.04322
G1 X129.817 Y130.376 E.02919
G1 X130.829 Y129.792 E.03757
; WIPE_START
G1 F11054.348
G1 X131.215 Y130.605 E-.34214
G1 X131.232 Y130.703 E-.03786
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.166 J.348 P1  F30000
G1 X131.815 Y128.752 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X131.947 Y128.91 E.00661
G1 X131.289 Y129.686 E.0327
G1 X131.6 Y130.474 E.02728
G3 X130.075 Y131.356 I-.851 J.288 E.07932
G1 X129.548 Y130.691 E.02728
G1 X128.547 Y130.873 E.03271
G1 X128.476 Y130.68 E.00661
G1 X131.763 Y128.782 E.12205
; WIPE_START
G1 F11054.348
G1 X131.947 Y128.91 E-.08502
G1 X131.444 Y129.502 E-.29498
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.091 J.539 P1  F30000
G1 X133.105 Y126.142 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X133.105 Y125.858 E.00915
G1 X133.355 Y125.895 E.00812
G1 X133.355 Y126.106 E.00678
G1 X133.165 Y126.133 E.00618
G1 X132.906 Y126.583 F30000
G1 F1790
G1 X132.698 Y126.614 E.00675
G1 X132.698 Y125.386 E.0395
G1 X133.596 Y125.519 E.02917
G3 X133.596 Y126.481 I-.099 J.481 E.04323
G1 X132.965 Y126.575 E.0205
G1 X132.797 Y127.234 F30000
G1 F1790
G1 X132.486 Y127.952 E.02518
G1 X132.291 Y127.912 E.00639
G1 X132.291 Y124.088 E.12298
G1 X132.49 Y124.05 E.0065
G1 X132.865 Y124.999 E.03282
G1 X133.675 Y125.119 E.02635
G3 X133.675 Y126.881 I-.181 J.881 E.07915
G1 X132.901 Y126.996 E.02518
G1 X132.821 Y127.179 E.00642
; WIPE_START
G1 F11054.348
G1 X132.486 Y127.952 E-.32038
G1 X132.332 Y127.921 E-.05962
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.177 J-.311 P1  F30000
G1 X130.676 Y121.65 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X130.429 Y121.508 E.00915
G1 X130.586 Y121.31 E.00812
G1 X130.769 Y121.415 E.00678
G1 X130.698 Y121.594 E.00618
G1 X130.881 Y122.238 F30000
G1 F1790
G1 X129.817 Y121.624 E.0395
G1 X130.381 Y120.913 E.02918
G3 X130.814 Y120.75 I.376 J.343 E.01543
G3 X131.215 Y121.395 I-.07 J.49 E.0278
G1 X130.903 Y122.183 E.02724
; WIPE_START
G1 F11054.348
G1 X130.014 Y121.725 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-.787 J.929 P1  F30000
G1 X131.802 Y123.24 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X128.49 Y121.328 E.12298
G1 X128.552 Y121.139 E.00639
G1 X129.588 Y121.258 E.03353
G1 X130.075 Y120.645 E.02518
G3 X130.844 Y120.344 I.687 J.626 E.0275
G3 X131.6 Y121.526 I-.095 J.894 E.05175
G1 X131.299 Y122.287 E.02634
G1 X131.934 Y123.087 E.03282
G1 X131.841 Y123.195 E.00457
; WIPE_START
G1 F11054.348
G1 X130.967 Y122.708 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-1.111 J.496 P1  F30000
G1 X133.116 Y127.521 Z10.2
G1 Z9.8
G1 E.4 F1800
G1 F1790
G1 X132.759 Y128.347 E.02892
G3 X131.757 Y129.763 I-5.633 J-2.921 E.05595
G1 X131.986 Y130.343 E.02007
G3 X129.768 Y131.624 I-1.237 J.418 E.11532
G1 X129.38 Y131.135 E.02008
G3 X127.653 Y131.294 I-1.441 J-6.182 E.05596
G1 X126.59 Y131.172 E.0344
G3 X126.143 Y131.716 I-2.984 J-1.999 E.02269
G3 X124.014 Y130.343 I-.892 J-.955 E.11122
G1 X124.236 Y129.782 E.01943
G1 X123.687 Y129.09 E.02837
G3 X123.167 Y128.19 I4.31 J-3.089 E.03349
G1 X122.843 Y127.369 E.02837
G1 X122.245 Y127.281 E.01943
G3 X122.245 Y124.719 I.257 J-1.281 E.11533
G1 X122.816 Y124.635 E.01855
G1 X123.241 Y123.653 E.0344
G3 X124.243 Y122.237 I5.633 J2.921 E.05595
G1 X124.014 Y121.656 E.02008
G3 X126.232 Y120.376 I1.237 J-.418 E.11532
G1 X126.62 Y120.865 E.02008
G3 X128.347 Y120.706 I1.441 J6.183 E.05596
G1 X129.41 Y120.828 E.0344
G3 X129.857 Y120.284 I2.978 J1.994 E.02269
G3 X130.877 Y119.939 I.894 J.963 E.03566
G3 X131.986 Y121.657 I-.129 J1.3 E.07553
G1 X131.764 Y122.218 E.01943
G1 X132.313 Y122.91 E.02837
G3 X132.833 Y123.81 I-4.312 J3.09 E.0335
G1 X133.157 Y124.631 E.02837
G1 X133.755 Y124.719 E.01943
M73 P95 R0
G3 X133.755 Y127.281 I-.263 J1.281 E.11506
G1 X133.184 Y127.365 E.01855
G1 X133.14 Y127.466 E.00354
G1 X133.435 Y127.809 F30000
G1 F1790
G1 X133.124 Y128.527 E.02516
G3 X132.225 Y129.84 I-5.579 J-2.854 E.05131
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X132.44 Y131.042 I-1.848 J.951 E.03985
G3 X129.462 Y131.893 I-1.694 J-.293 E.12401
G1 X129.213 Y131.579 E.01287
G3 X127.626 Y131.701 I-1.269 J-6.14 E.05132
G1 X126.769 Y131.602 E.02777
G3 X125.529 Y132.454 I-1.611 J-1.018 E.0497
G3 X123.628 Y130.212 I-.276 J-1.693 E.1135
G1 X123.771 Y129.85 E.01251
G3 X122.551 Y127.737 I4.541 J-4.03 E.07899
G3 X121.289 Y127.212 I.104 J-2.027 E.04485
G1 X121.218 Y127.134 E.00337
G3 X122.166 Y124.32 I1.296 J-1.13 E.11524
G1 X122.532 Y124.265 E.01192
G1 X122.876 Y123.473 E.02777
G3 X123.775 Y122.16 I5.579 J2.854 E.05131
G3 X123.56 Y120.958 I1.848 J-.951 E.03985
G3 X126.538 Y120.107 I1.694 J.293 E.12401
G1 X126.787 Y120.421 E.01287
G3 X128.374 Y120.299 I1.269 J6.141 E.05132
G1 X129.231 Y120.398 E.02777
G3 X130.471 Y119.546 I1.611 J1.018 E.0497
G3 X130.91 Y119.533 I.275 J1.817 E.01417
G3 X132.372 Y121.788 I-.162 J1.707 E.0993
G1 X132.229 Y122.15 E.01252
G3 X133.449 Y124.263 I-4.545 J4.032 E.07899
G3 X134.711 Y124.789 I-.104 J2.027 E.04485
G1 X134.782 Y124.866 E.00337
G3 X133.834 Y127.68 I-1.283 J1.135 E.11555
G1 X133.468 Y127.735 E.01192
G1 X133.459 Y127.754 E.00067
M204 S250
G1 X133.736 Y128.102 F30000
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1790
M204 S5000
G1 X133.476 Y128.701 E.01943
G3 X132.676 Y129.915 I-5.472 J-2.735 E.04341
G3 X129.052 Y132.007 I-1.927 J.847 E.18325
G3 X126.94 Y132.017 I-1.083 J-6.022 E.06322
G3 X123.323 Y129.917 I-1.685 J-1.262 E.18238
G3 X122.269 Y128.092 I4.264 J-3.678 E.06313
G3 X120.513 Y126.689 I.235 J-2.095 E.07063
G3 X122.259 Y123.909 I2.006 J-.678 E.11189
G3 X123.324 Y122.085 I5.737 J2.125 E.06322
G3 X126.948 Y119.993 I1.927 J-.847 E.18324
G3 X129.06 Y119.983 I1.083 J6.022 E.06322
G3 X130.942 Y119.142 I1.691 J1.258 E.06417
G3 X132.677 Y122.083 I-.204 J2.103 E.11842
G3 X133.731 Y123.908 I-4.267 J3.68 E.06313
G3 X135.487 Y125.311 I-.235 J2.095 E.07063
G3 X135.515 Y126.611 I-2.013 J.694 E.03938
G1 X135.487 Y126.689 E.00246
G3 X133.787 Y128.085 I-1.99 J-.692 E.06892
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.476 Y128.701 E-.26226
G1 X133.326 Y128.971 E-.11774
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.212 J.113 P1  F30000
G1 X133.577 Y126.277 Z10.2
G1 Z9.8
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.183097
G1 F1790
G1 X133.633 Y126.165 E.00139
; LINE_WIDTH: 0.215702
G1 X133.656 Y126.107 E.00085
; LINE_WIDTH: 0.256877
G2 X133.65 Y125.876 I-.357 J-.107 E.00397
; LINE_WIDTH: 0.209733
G1 X133.634 Y125.837 E.00057
; LINE_WIDTH: 0.169166
G1 X133.61 Y125.792 E.00051
; LINE_WIDTH: 0.130912
G1 X133.564 Y125.719 E.0006
; WIPE_START
G1 F15000
G1 X133.61 Y125.792 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I.641 J-1.034 P1  F30000
G1 X132.599 Y125.165 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.197287
G1 F1790
G1 X132.572 Y125.021 E.00179
; LINE_WIDTH: 0.157139
G1 X132.544 Y124.876 E.00133
; LINE_WIDTH: 0.116991
G1 X132.517 Y124.732 E.00086
; WIPE_START
G1 F15000
G1 X132.544 Y124.876 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.066 J-.588 P1  F30000
G1 X131.357 Y122.723 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.117007
G1 F1790
G1 X131.246 Y122.627 E.00086
; LINE_WIDTH: 0.157194
G1 X131.134 Y122.53 E.00133
; LINE_WIDTH: 0.19738
G1 X131.023 Y122.434 E.0018
; WIPE_START
G1 F15000
G1 X131.134 Y122.53 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.212 J-.107 P1  F30000
G1 X131.027 Y121.313 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.170188
G1 F1790
G1 X130.958 Y121.202 E.00131
; LINE_WIDTH: 0.210013
G1 X130.932 Y121.168 E.00057
; LINE_WIDTH: 0.257106
G2 X130.738 Y121.049 I-.272 J.226 E.00393
; LINE_WIDTH: 0.218216
G1 X130.678 Y121.039 E.00084
; LINE_WIDTH: 0.171605
G1 X130.546 Y121.035 E.00134
; WIPE_START
G1 F15000
G1 X130.678 Y121.039 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-.136 J-1.209 P1  F30000
G1 X126.804 Y121.475 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.121566
G1 F1790
G1 X126.618 Y121.543 E.00123
; LINE_WIDTH: 0.170877
G1 X126.432 Y121.611 E.002
; WIPE_START
G1 F15000
G1 X126.618 Y121.543 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I.489 J-1.114 P1  F30000
G1 X125.449 Y121.03 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.19193
G1 F1790
G1 X125.302 Y121.042 E.00173
; LINE_WIDTH: 0.230598
G1 X125.246 Y121.053 E.00084
; LINE_WIDTH: 0.26089
G2 X125.081 Y121.154 I.106 J.36 E.00337
; LINE_WIDTH: 0.218295
G1 X125.043 Y121.201 E.00084
; LINE_WIDTH: 0.171726
G1 X124.973 Y121.313 E.00134
; WIPE_START
G1 F15000
G1 X125.043 Y121.201 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-1.216 J-.059 P1  F30000
G1 X124.983 Y122.448 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.170768
G1 F1790
G1 X124.831 Y122.575 E.002
; LINE_WIDTH: 0.121541
G1 X124.679 Y122.701 E.00123
; WIPE_START
G1 F15000
G1 X124.831 Y122.575 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-.967 J-.739 P1  F30000
G1 X122.423 Y125.723 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.183016
G1 F1790
G1 X122.367 Y125.835 E.00138
; LINE_WIDTH: 0.210031
G1 X122.349 Y125.879 E.00062
; LINE_WIDTH: 0.259147
G2 X122.327 Y126.003 I.557 J.16 E.00216
G1 X122.331 Y126.051 E.00083
; LINE_WIDTH: 0.241236
G2 X122.35 Y126.126 I.389 J-.059 E.00121
G1 X122.356 Y126.141 E.00025
; LINE_WIDTH: 0.192743
G1 X122.42 Y126.276 E.00176
; WIPE_START
G1 F15000
G1 X122.356 Y126.141 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-.673 J1.014 P1  F30000
G1 X123.401 Y126.835 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.197287
G1 F1790
G1 X123.428 Y126.979 E.00179
; LINE_WIDTH: 0.157139
G1 X123.456 Y127.124 E.00133
; LINE_WIDTH: 0.116992
G1 X123.483 Y127.268 E.00086
; WIPE_START
G1 F15000
G1 X123.456 Y127.124 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-1.066 J.588 P1  F30000
G1 X124.643 Y129.277 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.116995
G1 F1790
G1 X124.755 Y129.374 E.00086
; LINE_WIDTH: 0.157161
G1 X124.866 Y129.47 E.00133
; LINE_WIDTH: 0.197327
G1 X124.978 Y129.566 E.0018
; WIPE_START
G1 F15000
G1 X124.866 Y129.47 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-1.213 J.104 P1  F30000
G1 X124.971 Y130.695 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.193062
G1 F1790
G1 X125.056 Y130.817 E.00177
; LINE_WIDTH: 0.219387
G1 X125.066 Y130.83 E.00023
; LINE_WIDTH: 0.258559
G2 X125.229 Y130.942 I.289 J-.246 E.0034
; LINE_WIDTH: 0.236527
G1 X125.3 Y130.958 E.00112
; LINE_WIDTH: 0.192901
G1 X125.449 Y130.97 E.00176
; WIPE_START
G1 F15000
G1 X125.3 Y130.958 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I.134 J1.21 P1  F30000
G1 X129.196 Y130.525 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.121558
G1 F1790
G1 X129.382 Y130.457 E.00123
; LINE_WIDTH: 0.170855
G1 X129.568 Y130.389 E.002
; WIPE_START
G1 F15000
G1 X129.382 Y130.457 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I-.489 J1.114 P1  F30000
G1 X130.551 Y130.97 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.192909
G1 F1790
G1 X130.7 Y130.958 E.00176
; LINE_WIDTH: 0.21934
G1 X130.716 Y130.956 E.00023
; LINE_WIDTH: 0.258691
G2 X130.894 Y130.87 I-.065 J-.365 E.00341
; LINE_WIDTH: 0.236657
G1 X130.944 Y130.817 E.00111
; LINE_WIDTH: 0.193157
G1 X131.029 Y130.695 E.00177
; WIPE_START
G1 F15000
G1 X130.944 Y130.817 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.2 I1.215 J.071 P1  F30000
G1 X131.017 Y129.552 Z10.2
G1 Z9.8
G1 E.4 F1800
; LINE_WIDTH: 0.170775
G1 F1790
G1 X131.169 Y129.425 E.002
; LINE_WIDTH: 0.121543
G1 X131.321 Y129.299 E.00123
; CHANGE_LAYER
; Z_HEIGHT: 10
; LAYER_HEIGHT: 0.2
; WIPE_START
G1 F15000
G1 X131.169 Y129.425 E-.38
; WIPE_END
G1 E-.02 F1800
; layer num/total_layer_count: 50/50
; update layer progress
M73 L50
M991 S0 P49 ;notify layer change
; OBJECT_ID: 15
G17
G3 Z10.2 I.779 J-.935 P1  F30000
G1 X124.915 Y124.219 Z10.2
G1 Z10
G1 E.4 F1800
; FEATURE: Outer wall
; LINE_WIDTH: 0.42
G1 F1898
M204 S5000
G1 X127.849 Y122.525 E.1009
G1 X128 Y122.438 E.00521
G1 X131.085 Y124.219 E.10611
G1 X131.085 Y127.781 E.10611
G1 X128 Y129.562 E.10611
G1 X124.915 Y127.781 E.10611
G1 X124.915 Y124.279 E.10432
; WIPE_START
G1 F11933.819
M204 S10000
G1 X125.773 Y123.766 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I-.593 J1.063 P1  F30000
G1 X133.494 Y128.074 Z10.4
G1 Z10
G1 E.4 F1800
G1 F1898
M204 S5000
G1 X133.261 Y128.594 E.01697
G3 X132.408 Y129.87 I-5.298 J-2.616 E.04585
;========Date 20250206========
M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
 ; timelapse without wipe tower
M971 S11 C10 O0

M623

G3 X129.148 Y131.753 I-1.668 J.875 E.17173
G3 X126.852 Y131.753 I-1.148 J-5.796 E.06882
G3 X123.589 Y129.877 I-1.592 J-1.007 E.1715
G3 X122.437 Y127.881 I4.431 J-3.889 E.0691
G3 X122.444 Y124.118 I.083 J-1.882 E.1715
G3 X123.592 Y122.13 I5.594 J1.904 E.06882
M73 P96 R0
G3 X126.852 Y120.247 I1.668 J-.875 E.17173
G3 X129.148 Y120.247 I1.148 J5.796 E.06882
G3 X131.01 Y119.383 I1.611 J1.034 E.06454
G3 X132.411 Y122.123 I-.271 J1.866 E.10717
G3 X133.563 Y124.119 I-4.432 J3.889 E.0691
G3 X133.556 Y127.882 I-.083 J1.882 E.1715
G3 X133.508 Y128.018 I-5.593 J-1.904 E.00429
; WIPE_START
G1 F11933.819
M204 S10000
G1 X133.261 Y128.594 E-.23819
G1 X133.083 Y128.923 E-.14181
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I.914 J.803 P1  F30000
G1 X134.976 Y126.769 Z10.4
G1 Z10
G1 E.4 F1800
; FEATURE: Top surface
G1 F1898
M204 S2000
G1 X134.976 Y125.235 E.04568
G1 X134.599 Y124.756
G1 X134.599 Y127.243 E.07408
G1 X134.222 Y127.494
G1 X134.222 Y124.508 E.08893
G1 X133.845 Y124.382
G1 X133.845 Y127.618 E.09638
G1 X133.467 Y127.688
G1 X133.467 Y124.312 E.10056
G1 X133.09 Y123.527
G1 X133.09 Y128.483 E.14762
G1 X132.713 Y129.132
G1 X132.713 Y122.869 E.18655
G1 X132.336 Y122.362
G1 X132.336 Y129.635 E.21662
; WIPE_START
G1 F11933.819
M204 S10000
G1 X132.336 Y128.635 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I-1.209 J-.14 P1  F30000
G1 X131.959 Y131.895 Z10.4
G1 Z10
G1 E.4 F1800
G1 F1898
M204 S2000
G1 X131.959 Y120.095 E.3515
G1 X131.582 Y119.805
G1 X131.582 Y132.204 E.36932
G1 X131.205 Y132.358
G1 X131.205 Y127.951 E.13125
G1 X130.828 Y128.169
G1 X130.828 Y132.417 E.12655
G1 X130.451 Y132.397
G1 X130.451 Y128.387 E.11947
G1 X130.074 Y128.604
G1 X130.074 Y132.276 E.10937
G1 X129.697 Y132.042
G1 X129.697 Y128.822 E.09592
G1 X129.32 Y129.04
G1 X129.32 Y131.635 E.07729
G1 X128.943 Y131.579
G1 X128.943 Y129.257 E.06916
G1 X128.566 Y129.475
G1 X128.566 Y131.631 E.0642
G1 X128.188 Y131.661
G1 X128.188 Y129.693 E.05864
G1 X127.811 Y129.693
G1 X127.811 Y131.656 E.05847
G1 X127.434 Y131.63
G1 X127.434 Y129.475 E.06419
G1 X127.057 Y129.257
G1 X127.057 Y131.585 E.06933
G1 X126.68 Y131.636
G1 X126.68 Y129.04 E.07733
G1 X126.303 Y128.822
G1 X126.303 Y132.046 E.09602
G1 X125.926 Y132.278
G1 X125.926 Y128.604 E.10943
G1 X125.549 Y128.387
G1 X125.549 Y132.392 E.11931
G1 X125.172 Y132.423
G1 X125.172 Y128.169 E.12672
G1 X124.795 Y127.951
G1 X124.795 Y132.357 E.13125
; WIPE_START
G1 F11933.819
M204 S10000
G1 X124.795 Y131.357 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I.915 J.802 P1  F30000
G1 X131.205 Y124.049 Z10.4
G1 Z10
G1 E.4 F1800
G1 F1898
M204 S2000
G1 X131.205 Y119.642 E.13125
G1 X130.828 Y119.575
G1 X130.828 Y123.831 E.12677
G1 X130.451 Y123.613
G1 X130.451 Y119.603 E.11947
G1 X130.074 Y119.718
G1 X130.074 Y123.396 E.10955
G1 X129.697 Y123.178
G1 X129.697 Y119.958 E.09592
G1 X129.32 Y120.365
G1 X129.32 Y122.96 E.07729
M73 P97 R0
G1 X128.943 Y122.743
G1 X128.943 Y120.415 E.06932
G1 X128.566 Y120.37
G1 X128.566 Y122.525 E.06419
G1 X128.188 Y122.307
G1 X128.188 Y120.344 E.05846
G1 X127.811 Y120.339
G1 X127.811 Y122.307 E.05864
G1 X127.434 Y122.525
G1 X127.434 Y120.369 E.0642
G1 X127.057 Y120.421
G1 X127.057 Y122.743 E.06916
G1 X126.68 Y122.96
G1 X126.68 Y120.365 E.0773
G1 X126.303 Y119.958
G1 X126.303 Y123.178 E.09592
G1 X125.926 Y123.396
G1 X125.926 Y119.724 E.10937
G1 X125.549 Y119.603
G1 X125.549 Y123.613 E.11947
G1 X125.172 Y123.831
G1 X125.172 Y119.576 E.12674
G1 X124.795 Y119.643
G1 X124.795 Y124.049 E.13125
; WIPE_START
G1 F11933.819
M204 S10000
G1 X124.795 Y123.049 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I1.209 J-.14 P1  F30000
G1 X124.418 Y119.796 Z10.4
G1 Z10
G1 E.4 F1800
G1 F1898
M204 S2000
G1 X124.418 Y132.195 E.36932
G1 X124.041 Y131.905
G1 X124.041 Y120.105 E.35149
; WIPE_START
G1 F11933.819
M204 S10000
G1 X124.041 Y121.105 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I-1.166 J-.349 P1  F30000
G1 X123.664 Y122.366 Z10.4
G1 Z10
G1 E.4 F1800
G1 F1898
M204 S2000
G1 X123.664 Y129.638 E.21661
G1 X123.287 Y129.131
G1 X123.287 Y122.868 E.18654
G1 X122.91 Y123.517
G1 X122.91 Y128.473 E.14761
G1 X122.532 Y127.688
G1 X122.532 Y124.312 E.10056
G1 X122.155 Y124.382
G1 X122.155 Y127.618 E.09638
G1 X121.778 Y127.492
G1 X121.778 Y124.506 E.08893
G1 X121.401 Y124.757
G1 X121.401 Y127.241 E.07398
G1 X121.024 Y126.764
G1 X121.024 Y125.231 E.04566
; WIPE_START
G1 F11933.819
M204 S10000
G1 X121.024 Y126.231 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I-.67 J1.016 P1  F30000
G1 X130.262 Y132.32 Z10.4
G1 Z10
G1 E.4 F1800
; FEATURE: Gap infill
; LINE_WIDTH: 0.107458
G1 F1898
G3 X130.106 Y132.294 I.058 J-.804 E.00081
; WIPE_START
G1 F15000
G1 X130.262 Y132.32 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I-.015 J-1.217 P1  F30000
G1 X124.983 Y132.387 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.0935276
G1 F1898
G1 X124.851 Y132.379 E.00053
; WIPE_START
G1 F15000
G1 X124.983 Y132.387 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I.674 J-1.013 P1  F30000
G1 X123.797 Y131.598 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.24445
G1 F1898
G1 X123.759 Y131.307 E.00467
; LINE_WIDTH: 0.285883
G1 X123.72 Y131.016 E.00564
; LINE_WIDTH: 0.311603
G3 X123.73 Y130.411 I3.076 J-.252 E.01286
; LINE_WIDTH: 0.262892
G1 X123.754 Y130.271 E.00247
; LINE_WIDTH: 0.214877
G1 X123.778 Y130.131 E.00193
; LINE_WIDTH: 0.166863
G1 X123.802 Y129.991 E.00139
; LINE_WIDTH: 0.105818
G2 X123.807 Y129.638 I-.666 J-.186 E.00177
; WIPE_START
G1 F15000
G1 X123.826 Y129.85 E-.22821
G1 X123.802 Y129.991 E-.15179
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I.325 J1.173 P1  F30000
G1 X131.23 Y127.935 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.0983886
G1 F1898
G1 X131.29 Y127.918 E.00027
; LINE_WIDTH: 0.122195
G1 X131.312 Y127.905 E.00016
; LINE_WIDTH: 0.162789
G1 X131.334 Y127.89 E.00025
G1 X131.333 Y124.109 E.0358
; LINE_WIDTH: 0.149322
G1 X131.312 Y124.095 E.00022
; LINE_WIDTH: 0.105345
G2 X131.23 Y124.066 I-.09 J.119 E.00044
; WIPE_START
G1 F15000
G1 X131.312 Y124.095 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I-1.202 J.191 P1  F30000
G1 X132.192 Y129.635 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.0931119
G1 F1898
G1 X132.172 Y129.839 E.00081
; LINE_WIDTH: 0.115211
G1 X132.196 Y129.982 E.00083
; LINE_WIDTH: 0.164288
G1 X132.221 Y130.125 E.00139
; LINE_WIDTH: 0.213365
G1 X132.245 Y130.268 E.00195
; LINE_WIDTH: 0.262442
G1 X132.27 Y130.411 E.00251
; LINE_WIDTH: 0.3117
G3 X132.28 Y131.016 I-3.067 J.353 E.01287
; LINE_WIDTH: 0.285964
G1 X132.241 Y131.307 E.00564
; LINE_WIDTH: 0.244522
G1 X132.203 Y131.598 E.00468
; WIPE_START
G1 F15000
G1 X132.241 Y131.307 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I1.164 J.356 P1  F30000
G1 X133.348 Y127.688 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.143694
G1 F1898
G1 X133.323 Y127.847 E.00128
; LINE_WIDTH: 0.106671
G1 X133.298 Y128.006 E.00081
; WIPE_START
G1 F15000
G1 X133.323 Y127.847 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I.492 J-1.113 P1  F30000
G1 X124.77 Y124.066 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.0983575
G1 F1898
G1 X124.71 Y124.082 E.00027
; LINE_WIDTH: 0.122175
G1 X124.688 Y124.095 E.00016
; LINE_WIDTH: 0.162879
G1 X124.666 Y124.11 E.00025
G1 X124.666 Y127.891 E.03583
; LINE_WIDTH: 0.149379
G1 X124.688 Y127.905 E.00022
; LINE_WIDTH: 0.105338
G2 X124.77 Y127.934 I.089 J-.119 E.00044
; WIPE_START
G1 F15000
G1 X124.688 Y127.905 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I1.059 J-.6 P1  F30000
G1 X122.652 Y124.312 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.143628
G1 F1898
G1 X122.677 Y124.153 E.00128
; LINE_WIDTH: 0.10665
G1 X122.702 Y123.995 E.00081
; WIPE_START
G1 F15000
G1 X122.677 Y124.153 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I1.028 J.651 P1  F30000
G1 X123.808 Y122.366 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.093032
G1 F1898
G1 X123.828 Y122.161 E.00081
; LINE_WIDTH: 0.115126
G1 X123.804 Y122.018 E.00083
; LINE_WIDTH: 0.164199
G1 X123.779 Y121.875 E.00139
; LINE_WIDTH: 0.213272
G1 X123.755 Y121.732 E.00195
; LINE_WIDTH: 0.262344
G1 X123.73 Y121.589 E.00251
; LINE_WIDTH: 0.310875
G3 X123.722 Y120.97 I3.045 J-.351 E.01314
; LINE_WIDTH: 0.283594
G1 X123.76 Y120.686 E.00545
; LINE_WIDTH: 0.243772
G1 X123.797 Y120.401 E.00455
; WIPE_START
M73 P98 R0
G1 F15000
G1 X123.76 Y120.686 E-.38
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I.048 J1.216 P1  F30000
G1 X132.176 Y120.353 Z10.4
G1 Z10
G1 E.4 F1800
; LINE_WIDTH: 0.177878
G1 F1898
G1 X132.206 Y120.515 E.00176
; LINE_WIDTH: 0.217447
G1 X132.235 Y120.677 E.00227
; LINE_WIDTH: 0.257016
G1 X132.265 Y120.839 E.00278
; LINE_WIDTH: 0.30793
G3 X132.27 Y121.589 I-3.757 J.401 E.01574
; LINE_WIDTH: 0.262974
G1 X132.246 Y121.729 E.00247
; LINE_WIDTH: 0.214959
G1 X132.222 Y121.869 E.00193
; LINE_WIDTH: 0.166943
G1 X132.198 Y122.009 E.00139
; LINE_WIDTH: 0.105914
G2 X132.193 Y122.362 I.666 J.186 E.00178
; close powerlost recovery
M1003 S0
; WIPE_START
G1 F15000
G1 X132.174 Y122.15 E-.22818
G1 X132.198 Y122.009 E-.15182
; WIPE_END
G1 E-.02 F1800
G17
G3 Z10.4 I1.217 J0 P1  F30000
M106 S0
M106 P2 S0
M981 S0 P20000 ; close spaghetti detector
; FEATURE: Custom
; MACHINE_END_GCODE_START
; filament end gcode 

;===== date: 20230428 =====================
M400 ; wait for buffer to clear
G92 E0 ; zero the extruder
G1 E-0.8 F1800 ; retract
G1 Z10.5 F900 ; lower z a little
G1 X65 Y245 F12000 ; move to safe pos 
G1 Y265 F3000

G1 X65 Y245 F12000
G1 Y265 F3000
M140 S0 ; turn off bed
M106 S0 ; turn off fan
M106 P2 S0 ; turn off remote part cooling fan
M106 P3 S0 ; turn off chamber cooling fan

G1 X100 F12000 ; wipe
; pull back filament to AMS
M620 S255
G1 X20 Y50 F12000
G1 Y-3
T255
G1 X65 F12000
G1 Y265
G1 X100 F12000 ; wipe
M621 S255
M104 S0 ; turn off hotend

M622.1 S1 ; for prev firmware, default turned on
M1002 judge_flag timelapse_record_flag
M622 J1
    M400 ; wait all motion done
    M991 S0 P-1 ;end smooth timelapse at safe pos
    M400 S3 ;wait for last picture to be taken
M623; end of "timelapse_record_flag"

M400 ; wait all motion done
M17 S
M17 Z0.4 ; lower z motor current to reduce impact if there is something in the bottom

    G1 Z110 F600
    G1 Z108

M400 P100
M17 R ; restore z current

G90
G1 X128 Y250 F3600

M220 S100  ; Reset feedrate magnitude
M201.2 K1.0 ; Reset acc magnitude
M73.2   R1.0 ;Reset left time magnitude
M1002 set_gcode_claim_speed_level : 0

M17 X0.8 Y0.8 Z0.5 ; lower motor current to 45% power
M73 P100 R0
; EXECUTABLE_BLOCK_END

