# Independent artifact runs and native keyboard probes

## Input isolation without false preservation claims

Apply only when the current assignment explicitly prohibits inspecting prior designs.

1. Read the permitted brief, content map, work order and original assets.
2. View every requested reference; establish identity from original evidence, not old output.
3. Create a new output directory. Honor an explicitly separate completion handoff; do not overwrite or archive the old handoff by reading it.
4. Use permitted source/system assets and generic skill tooling, not assets copied from prior packages.
5. Confine writes. Do not open prohibited files merely to produce before/after hashes. Report preservation by write scope, not byte identity.
6. State the actual isolation boundary: prior artifacts were not opened during the run. If prior conversation context exists, do not call the experiment scientifically blinded.

This is a conditional exception to the normal advice to snapshot protected files, not a reason to stop snapshotting when inspection is allowed.

## Minimal honest run record

Record:
- First observed start time, completion cutoff, timezone and tool-computed elapsed duration.
- Whether those timestamps cover artifact work or include final delivery; wall-clock is not model inference time.
- Observable session model/provider label, separately from any provider-returned per-request identity.
- Effort setting, actual token usage and cost, each explicitly unavailable if telemetry is absent.
- Tools used, commands/exit statuses, inspected renders, real findings and verification limitations.

Do not estimate tokens/cost from elapsed time, source-file size, output length or model branding. Do not make extra model requests for accounting. Do not inspect secret-bearing configuration just to fill optional metadata. Finish the record after rendering, inspection, verification and handoff so the end time reflects the stated cutoff.

## Tested CDP Enter activation for native details

Observed failure: a native disclosure did not open when a test sent only keyDown/keyUp with key/code and virtual key 13. The page did not need a custom JavaScript replacement. The successful probe included Enter's character payload.

Using the skill's CDP helper `c`, after navigation and font readiness:

```python
c.evaluate("document.querySelectorAll('summary')[1].focus()")
assert c.evaluate("document.activeElement.tagName") == 'SUMMARY'
assert c.evaluate("document.querySelectorAll('details')[1].open") is False

c.call('Input.dispatchKeyEvent',
       type='keyDown', key='Enter', code='Enter',
       windowsVirtualKeyCode=13, nativeVirtualKeyCode=13,
       text='\r', unmodifiedText='\r')
c.call('Input.dispatchKeyEvent',
       type='keyUp', key='Enter', code='Enter',
       windowsVirtualKeyCode=13, nativeVirtualKeyCode=13)

assert c.evaluate("document.querySelectorAll('details')[1].open") is True
```

The successful targeted experiment changed the three disclosure states from `[True, False, False]` to `[True, True, False]`. The completed viewport suite then passed keyboard activation at narrow mobile, standard mobile, tablet and desktop.

Guardrails:
- Select the intended control and assert its initial state; do not assume every page has a second disclosure or that it starts closed.
- If evaluation returns missing/undefined data, inspect the current document, focus and CDP exception details before classifying it as a page failure.
- Programmatic focus plus real Enter tests activation, not sequential Tab reachability. Test Tab separately before claiming traversal coverage.
- Setting every disclosure open is useful for expanded layout/contrast scans, but is not keyboard evidence.
- `.click()` does not prove keyboard behavior.
- Keep artifact defects separate from test-harness defects in the handoff. Correct the actual cause and rerun the affected tests.
