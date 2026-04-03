# Init Protocol — First-Time Setup Questionnaire

Collect preferences in four short rounds. Present options as a numbered list wherever possible — do not ask the user to type option names. Wait for answers before moving to the next round.

---

## Round 1 — Your Instrument

Ask:
> "Before I build your first preset, I need to know about your setup. Let's start with your instrument.
>
> 1. Guitar
> 2. Bass
> 3. Both guitar and bass
> 4. Other (describe)
>
> What do you play, and what's the make and model?"

Follow up:
> "What type of pickups?
>
> 1. Single coils
> 2. Humbuckers
> 3. P-bass (split-coil)
> 4. J-bass (single coil)
> 5. PJ (split + single)
> 6. Active electronics
> 7. Mixed or other (describe)"

---

## Round 2 — Your Rig Connection

Ask:
> "How is your HX Stomp connected in your rig?
>
> 1. Direct to FRFR speaker or PA (full-range output — cab sim on)
> 2. Direct to audio interface or recording setup (cab sim on)
> 3. Headphones only (cab sim on)
> 4. Into the front input of a guitar/bass amp (no effects loop integration)
> 5. 4-Cable Method — integrated into my amp's effects loop
> 6. In the amp's effects loop only (amp's own preamp feeds into it)
> 7. Into my amp's effects return, bypassing the amp's preamp
> 8. External preamp or amp sim in the HX Stomp's Send/Return loop, DI or line out to PA/interface
> 9. Something else (describe)"

Based on the answer, ask follow-ups:
- If **4, 5, 6, or 7**: "What amp are you using? Make and model?"
- If **5 or 6**: "Is your amp's effects loop series or parallel? (Series = one path, Parallel = wet/dry blend — write 'Unknown' if unsure)"
- If **8**: "What device is in your Send/Return loop?" (then proceed to the Send/Return deep-dive questions below)

Then ask everyone:
> "Do you have anything connected between the HX Stomp's Send and Return jacks?
>
> 1. No — the loop is empty
> 2. Yes — there's a device in the loop (describe it)"

If yes, follow up with:
> "Tell me more about that device:
> - What is it? (make and model)
> - What does it do? (e.g. amp sim, preamp, compressor, reverb)
> - Does it have multiple channels or modes? If so, list them and what each one sounds like.
> - Does it have its own DI or output that goes somewhere, or does it feed back into the HX Stomp Return?"

Then ask:
> "Do you have any pedals or devices in your signal chain that are outside the HX Stomp — either before the input or after the output?
>
> 1. No — the HX Stomp is the only device
> 2. Yes — before the HX Stomp input (describe each one and what it does)
> 3. Yes — after the HX Stomp output (describe each one and what it does)
> 4. Yes — both before and after (describe all of them)"

---

## Round 3 — Output & Control

Ask:
> "What does your HX Stomp's output connect to? (Describe both outputs if you use both.)"

Then:
> "Mono or stereo?
>
> 1. Mono — I use one output
> 2. Stereo — I use both outputs"

Then:
> "How do you prefer to control the HX Stomp?
>
> 1. Stomp mode — footswitches toggle individual blocks on/off
> 2. Snapshot mode — footswitches recall complete preset states
> 3. Hybrid — mix of both"

Then:
> "Do you use an expression pedal?
>
> 1. No
> 2. Yes — typically for wah
> 3. Yes — typically for volume
> 4. Yes — assigned to something else (describe)"

Then:
> "How do you typically use presets?
>
> 1. One preset per song — each preset is dedicated to a single sound
> 2. Multiple sounds within one preset — I switch between tones mid-song"

---

## Round 4 — Tone Profile

Ask:
> "What genres or styles do you mostly play? (List as many as apply — e.g. rock, blues, metal, jazz, funk, country, ambient)"

Then:
> "How would you describe your typical tone character? Pick all that apply:
>
> 1. Clean
> 2. Crunch / edge of breakup
> 3. High gain
> 4. Warm
> 5. Bright
> 6. Scooped mids
> 7. Mid-focused
> 8. Vintage character
> 9. Modern / hi-fi"

Then:
> "Are there any effects or blocks you always want in every preset?
>
> 1. No standing requirements
> 2. Yes — always include a tuner block
> 3. Yes — always include a noise gate
> 4. Yes — always start with a compressor
> 5. Yes — something else (describe)"

Then:
> "Are there any effects or block types you want to avoid entirely?
>
> 1. No restrictions
> 2. No pitch shifting or octave effects
> 3. No heavy modulation
> 4. Something specific (describe)"

---

## After Round 4

Before proceeding, run through the checklist in Step 0 of SKILL.md. If anything is missing, ask the user before continuing.

Once all items are checked off:

**1.** Display the complete filled-in `references/user_preferences.md` content as a code block so the user can review it. Use the exact field names and option values defined in that file.

**2.** Ask the user to confirm the content is correct, then say:

> "To save your preferences, please invoke the `/skill-creator` command now. Once it confirms the file has been updated, let me know and we'll get straight to building your preset."

**3.** Once confirmed, say:
> "Your setup is saved. What preset would you like to build?"
