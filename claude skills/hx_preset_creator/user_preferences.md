# User Preferences

Populated by Claude during init. Each field includes valid options as a reference.
All `*(not set)*` values trigger the init flow in Step 0.

---

## Instrument

**instruments:**
*(not set)*
<!-- List all instruments used with this rig. Format: Type — Make Model (strings/scale if relevant) -->

**pickup_type:**
*(not set)*
<!-- Options: single_coil | humbucker | p_bass | j_bass | pj_bass | active | piezo | mixed -->

**pickup_output:**
*(not set)*
<!-- Options: low | medium | high | active -->

---

## Signal Chain

**signal_chain_type:**
*(not set)*
<!-- Options:
     direct_frfr          — HX Stomp output into a full-range speaker (Powercab, FRFR, PA)
     direct_interface     — HX Stomp output into an audio interface (studio/recording)
     direct_headphones    — HX Stomp into headphones only
     front_of_amp         — HX Stomp output into amp input (no effects loop integration)
     4cm                  — 4-Cable Method: HX Stomp integrated into amp's effects loop
     fx_loop_only         — HX Stomp in amp effects loop only (amp's own preamp before it)
     power_amp_in         — HX Stomp output into amp effects return (bypassing amp preamp)
     ext_preamp_in_loop   — External preamp/amp sim in HX Stomp Send/Return, DI or line out to PA/interface
-->

**cab_simulation:**
*(not set)*
<!-- Options: required | not_required
     required:     output goes to FRFR, PA, interface, or headphones — use Amp+Cab blocks
     not_required: output drives a real speaker cabinet — use Preamp blocks only
-->

**amp_make_model:**
*(not set)*
<!-- The amp in the rig, if any. Write "None" if going direct. -->

**amp_type:**
*(not set)*
<!-- Options: tube | solid_state | hybrid | modelling | none -->

**amp_fx_loop_type:**
*(not set)*
<!-- Options: series | parallel | none | unknown
     series = one signal path through the loop
     parallel = wet/dry blend between loop and dry signal -->

**hx_fx_loop_devices:**
*(not set)*
<!-- Devices connected between HX Stomp Send and Return jacks.
     Format: Device name — type (preamp / effect / amp_sim / compressor / etc.)
     Write "None" if empty. -->

**hx_fx_loop_device_details:**
*(not set)*
<!-- Full details for each device in the loop. For each device include:
     - Channels or modes available and what each one sounds like
     - Whether it has its own DI/output or feeds back into HX Stomp Return
     - Any settings or voicings the user has established
     Write "None" if loop is empty. -->

**external_chain_devices:**
*(not set)*
<!-- Pedals or devices outside the HX Stomp (before input or after output).
     Format: Device name — position (before_hx / after_hx)
     Write "None" if the HX Stomp is the only device. -->

---

## Output

**output_mode:**
*(not set)*
<!-- Options: mono | stereo -->

**output_connections:**
*(not set)*
<!-- What each output jack connects to.
     Format: Output type — destination
     e.g. Left 1/4" — amp input, XLR L+R — PA mixer, Headphones — practice -->

**monitoring_context:**
*(not set)*
<!-- Options: stage | studio | practice | mixed -->

---

## Performance

**control_mode:**
*(not set)*
<!-- Options: stomp | snapshot | hybrid -->

**expression_pedal:**
*(not set)*
<!-- Options: none | wah | volume | pitch | mix | other
     If other or multiple, describe briefly. -->

**preset_style:**
*(not set)*
<!-- Options: one_per_song | multi_sound_per_preset | mixed -->

**snapshot_count_preference:**
*(not set)*
<!-- Options: 1 | 2 | 3 | not_applicable -->

---

## Tone Profile

**primary_genres:**
*(not set)*
<!-- List genres in order of priority. e.g. rock, blues, jazz, metal, funk -->

**tone_character:**
*(not set)*
<!-- Options (pick all that apply): clean | crunch | high_gain | warm | bright | scooped | mid_focused | vintage | modern -->

**always_include:**
*(not set)*
<!-- Block types always wanted in every preset. e.g. tuner, noise_gate, compressor
     Write "None" if no standing requirements. -->

**always_exclude:**
*(not set)*
<!-- Block types or effects to never use. e.g. pitch_shift, octave, modulation
     Write "None" if no restrictions. -->
