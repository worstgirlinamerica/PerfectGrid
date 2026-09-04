# Localization in Perfect Grid

## What's supported

The UI is fully translated into:

| Language | Code | Script | Works in UI | Works in filenames |
|---|---|---|---|---|
| English | `en` | Latin | Yes | Yes |
| Chinese (Simplified) | `zh` | CJK | Yes | Yes |
| Portuguese | `pt` | Latin | Yes | Yes |
| Spanish | `es` | Latin | Yes | Yes |
| Japanese | `ja` | CJK + Kana | Yes | Yes |
| French | `fr` | Latin | Yes | Yes |
| German | `de` | Latin | Yes | Yes |
| Korean | `ko` | Hangul | Yes | Yes |

"Works in filenames" means: if you drag in a video whose filename is written in that language, the contact sheet will display the filename correctly.

## What's not fully supported as of v0.1.2

Some scripts need extra rendering work beyond what's currently implemented:

**Hebrew** — Right-to-left, same direction as Arabic. The bidi reorder already applies to Hebrew ranges (U+0590–U+05FF), so direction should be mostly correct. Hebrew letters don't reshape like Arabic does, so no reshaper is needed. Not explicitly tested — may work on macOS via Arial Unicode MS, likely boxes on Linux.

**Thai** — No reshaping needed, but Thai has no spaces between words and uses stacking diacritics. macOS has Thonburi in the font fallback list. Linux will box out.

**Devanagari (Hindi, Sanskrit, Nepali, Marathi)** — Needs glyph combination similar to Arabic reshaping but handled by a different library (`uharfbuzz`). Not currently handled — will show boxes on all platforms.

**Farsi/Persian** — Uses Arabic script, so it does go through `arabic_reshaper`. Farsi-specific ligatures may not form correctly with the current reshaper config. Probably mostly readable.

**Linux non-Latin filenames** — The font priority list falls back to the PIL bitmap default if no system font matches. Non-ASCII filenames will likely box out. Fix planned: bundling Noto Sans with the app.

## How the UI translation works

Every string in the UI has a key in `src/perfect_grid/pg_i18n.py`. The `LANGUAGES` dictionary maps each language code to a full set of translated strings. A function called `get_tr()` returns a translator for a given language code — `tr("export_png")` returns `"Export PNG"` in English, `"导出 PNG"` in Chinese, and so on.

When you change the language in Settings and hit OK, `retranslate_ui()` runs and updates all visible widget text in place. No restart required.

If a key is missing in a language, it falls back to English rather than crashing or showing a blank.

## How Sheet Rendering works

This is separate from UI translation. When you drag in a video, the app draws the filename onto the contact sheet image as pixels using PIL. Latin scripts draw fine with no extra handling. Non-Latin scripts need additional steps:

**CJK (Chinese, Japanese, Korean)** — Draw correctly as-is. On macOS, PingFang covers the full CJK range. On Linux, a Noto CJK font is needed.

**Arabic** — Arabic letters change shape depending on their position in a word. The app uses `arabic_reshaper` to convert logical codepoints into correct visual forms, then `python-bidi` to reverse the render order for right-to-left display. GeezaPro is prioritized for Arabic text on macOS.

**Other RTL scripts** — The bidi reorder applies to Hebrew ranges too, so direction should be handled. Reshaping is Arabic-specific and not needed for Hebrew.

## Adding a new UI language

1. Open `src/perfect_grid/pg_i18n.py`.
2. Copy the `"en"` block and change the key to your language code (e.g. `"ru"` for Russian).
3. Translate all the values. Keys never change.
4. Done — the language picker in Settings includes it automatically.

No code changes needed beyond the dictionary entry.
