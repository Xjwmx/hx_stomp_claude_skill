# Block Selection Reference

## Rig Filter

Evaluate the user's rig output type and eliminate entire block categories before any other scoring:

| Rig output type | Use Amp+Cab? | Use Preamp? | Use Cab separately? |
|---|---|---|---|
| FRFR / PA / headphones / studio DI | ✅ Yes | ❌ No | Only with Preamp |
| Real amp power section + real cab | ❌ No | ✅ Yes | ❌ No |
| 4-Cable Method (4CM) | ❌ No | ✅ Yes (before FX send) | ❌ No |
| Into clean amp, FX return | ❌ No | ✅ Yes | ❌ No |

---

## Block Scoring Model

After the rig filter, score remaining candidates. Select the highest scorer; break ties by lower DSP cost.

```
Score = 0

+ 100  if block.based_on exactly matches the identified real-world gear
+  60  if block.based_on partially matches (same brand/era/type)
+  20  if block.subcategory matches the gear type

+  15  if hx_subcategory is "Mono" or "Stereo"   (HX generation — prefer these)
-  10  if hx_subcategory is "Legacy"              (older models)

+  10  if user rig is stereo AND block supports stereo routing
-   5  if user rig is mono   AND block is stereo-only

-  (block.dsp.mono  * 0.1)  for mono routing    (DSP efficiency tiebreaker)
-  (block.dsp.stereo * 0.1) for stereo routing

+   5  if estimated target params fall between 20%–80% of their range
```

**Legacy exception:** prefer Legacy if the target tone is pre-2016, the user asks for vintage character, the Legacy block is the only model of that hardware, or the HX version has a notably different character.

---

## Stereo vs. Mono

Use a Stereo block only if **all three** are true:
1. User rig has stereo outputs.
2. The effect is inherently stereo (e.g. ping-pong delay, wide chorus, spread reverb).
3. DSP budget allows after all other blocks are accounted for.

Otherwise default to Mono. Never use a Stereo block for a mono rig.

---

## Amp + Cab Pairing

When using `Preamp` + `Cab` (rather than the combined `Amp+Cab`), match the cab to the amp era:

| Amp type | Typical cab match |
|---|---|
| British (Marshall, Vox) | 4×12 Greenback or Vintage 30 |
| American (Fender, Dumble) | 1×12 or 2×12 Alnico/Jensen |
| High gain (Mesa, EVH, Peavey) | 4×12 Vintage 30 or V30/G12T-75 mix |
| Bass amp | 8×10, 4×10, or 1×15 bass-specific |

---

## Block Order Rules

1. Wah or fuzz → always first in chain (input impedance).
2. Compression → before drive if enhancing dynamics; after drive if controlling output.
3. Drive blocks → before amp.
4. Amp+Cab or Preamp+Cab → after all pre-amp effects.
5. Modulation, delay, reverb → after amp, in that order.
6. If using 4CM: pre-amp effects → Send block (`@path: 0`) → [amp effects loop] → Return block (`@path: 0`) → post-amp effects.

---

## Stacking Logic

- High-gain amp + overdrive: prefer a low-gain boost (low drive, high level) over a heavy distortion.
- Clean or slightly breaking up amp: a heavier drive block is appropriate.
