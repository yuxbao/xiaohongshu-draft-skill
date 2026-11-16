# Creator Platform Workflow Notes

Use these notes to handle the creator UI. The platform can change its labels and layout, so act on the current visible state rather than assuming a fixed page structure.

## Before editing

- Use the official Creator Service Platform and confirm the displayed account.
- Make sure the user has supplied or clearly selected the exact copy and source images.
- Preserve the image order the user specified. If only a numbered filename sequence is available, use its natural numeric order and make that assumption clear when it matters.
- Check file types, upload progress, and any current limits displayed by the platform.

## Text entry

- Prefer a browser-native paste or fill operation that preserves Unicode and newlines.
- Avoid character-by-character simulated typing for long multilingual copy when it may drop or corrupt characters.
- After entry, read the title and body back from the editor or inspect them visually. Check the first and last lines, punctuation, hashtags, and the character counter.
- If entry is corrupted, replace the affected field in full, then verify again. Do not save until the editor contains the intended text.

## Saving and verification

- Use the platform's visible save-draft or save-and-leave control. The exact label can change.
- If the platform auto-saves, wait for a visible saved state and confirm the note appears in Drafts.
- Do not infer a successful save from clicking a button, closing the editor, or seeing a local export.
- Verify the saved item by its title and image count. Do not open the publish/post action during a draft-only task.

## Blockers

- For an expired session, ask the user to complete normal sign-in in the browser; resume only once the expected account is visible.
- For CAPTCHA, platform risk warnings, or network/security blocks, stop and explain the message. Do not try alternate identities, network routes, fingerprints, private endpoints, or automation designed to defeat the block.
- If browser input, uploads, or saving fails, inspect the current page, then make at most one focused retry. Avoid repeating a failing action blindly.
- If the platform does not expose draft saving, leave content unpublished and offer a local Markdown/image bundle as a separate fallback.
