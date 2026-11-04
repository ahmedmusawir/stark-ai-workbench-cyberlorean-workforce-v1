# Image-ready comparison captures

## Trigger
A local HTML comparison includes several full-page preview images, often lazy-loaded, and must be captured or preflighted after fonts and assets load.

## Validated diagnosis and correction
A multi-direction render completed its individual concept captures but timed out at the comparison index. `document.readyState` was `complete` and fonts were `loaded`; offscreen images remained incomplete, some with zero natural width. Awaiting every image's `decode()` without initiating lazy-image loading stalled. Changing animation-frame waits did not resolve that cause.

Log the current file/viewport and readiness details before retrying. In the capture context, use:

```javascript
(async () => {
  await document.fonts.ready;
  document.querySelectorAll('img[loading="lazy"]')
    .forEach(image => { image.loading = 'eager'; });
  await Promise.all([...document.images].map(image =>
    image.decode().catch(() => {})
  ));
  return {
    height: Math.max(document.documentElement.scrollHeight,
                     document.body.scrollHeight),
    imagesReady: [...document.images].every(image =>
      image.complete && image.naturalWidth > 0
    )
  };
})()
```

Require `imagesReady` before claiming success. A production harness should impose a bounded readiness deadline and report unresolved sources; the promise rejection handler is not permission to accept broken images. This eager-loading change belongs to screenshot preparation, not necessarily the delivered site's loading strategy.

## Preserve viewport geometry
After setting the intended viewport and awaiting readiness, capture document coordinates without expanding the emulated viewport height:

```python
shot = cdp.call(
    'Page.captureScreenshot',
    format='png',
    captureBeyondViewport=True,
    clip={'x': 0, 'y': 0, 'width': width,
          'height': ready['height'], 'scale': 1},
)
```

Use the chosen device scale factor in `Emulation.setDeviceMetricsOverride`. Distinguish CSS width from PNG pixel width in reports. Changing viewport height can affect `vh` layouts or media queries, so a screenshot obtained that way need not represent the intended initial viewport.

## Budgeted visual review
For a four-direction assignment with desktop/mobile previews and a maximum of four rechecks:
1. Inspect eight initial previews individually; input-reference inspection is a separate inventory.
2. Record concrete defects before editing.
3. Preserve affected initial renders within the permitted output root.
4. Fix the generator and regenerate canonical previews.
5. Spend targeted rechecks on changed mobile text/art, corresponding desktop changes, and the comparison entry. Use readable crops, not thumbnail grids.
6. Disclose crop boundaries and do not describe a cropped comparison capture as full-page evidence.

Numbers follow the active assignment, not a universal quota. Do not invent a permanent eight-plus-four limit for other work.

## Responsive illustration labels
A wide service diagram looked clear on desktop but scaled its embedded labels to illegible mobile text. The successful repair used a `<picture>` mobile source with the small labels removed and adjacent HTML service labels at a readable size. This preserves the explanatory artwork rather than cropping meaningful content. Verify `img.currentSrc`, alt text, image proportions and responsive labels. DOM text-contrast probes do not inspect text embedded in external SVG images.

## Confinement and rerun safety
- Browser profile/cache directory and temporary negative-test fixtures belong under the approved output root when the assignment confines all writes.
- Set `sys.dont_write_bytecode = True` before importing read-only helper modules from skills.
- Use `finally` to terminate the renderer process created by the harness and remove its private profile; do not kill unrelated browser processes.
- Generate in-progress report stubs only if absent. Completed review/handoff documents should not be overwritten by an ordinary design regeneration.
- Batch mechanical patches, but print only success/error summaries; large unified diffs for minified HTML/CSS can flood context and hide relevant results.
