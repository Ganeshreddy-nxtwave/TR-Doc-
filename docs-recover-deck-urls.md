# Recovering deck URLs from the tracker

**Resolved for the current tracker.** Removing the smart chips from the sheet and
re-exporting produced real URLs in every `PPT Link` cell: 93 of 93, zero lost.
Keep this note for the next export.

## The problem

Google Sheets stores a smart chip / hyperlinked cell as rich text. CSV export
keeps only the **display text**, so a cell showing `Intro to LangChain` exports as
that sentence rather than the URL behind it. The first export lost 48 of 93 links
this way -- only the Generative AI block, where cells held raw URLs, survived.

## Fix

Remove the smart chips so the cells hold plain URL text, then re-export as CSV.
That is what was done here.

If you would rather keep the chips, this Apps Script writes the underlying URLs
into a new column instead. Extensions -> Apps Script, paste, Run, re-export.

```javascript
function expandPptLinks() {
  const sh = SpreadsheetApp.getActiveSheet();
  const rows = sh.getLastRow();
  const header = sh.getDataRange().getValues()[1];      // real header is row 2
  const col = header.indexOf('PPT Link') + 1;
  if (!col) throw new Error('No "PPT Link" column found in row 2');

  const rich = sh.getRange(1, col, rows, 1).getRichTextValues();
  const out = rich.map(([rt]) => {
    if (!rt) return [''];
    let url = rt.getLinkUrl();
    if (!url) {
      for (const run of rt.getRuns()) {
        if (run.getLinkUrl()) { url = run.getLinkUrl(); break; }
      }
    }
    return [url || ''];
  });

  const target = sh.getLastColumn() + 1;
  sh.getRange(1, target, rows, 1).setValues(out);
  sh.getRange(2, target).setValue('PPT URL');
}
```

The importer reads a `PPT URL` column first and falls back to `PPT Link`, so
either fix works with no code change.

## How to tell it worked

`python -m tr curriculum --tracker "<csv>"` prints a per-course table with a
`lost links` column. Zero everywhere means every deck is fetchable.

## Sharing still matters

A real URL only works if the deck has link-sharing on. A restricted deck returns
Google's sign-in page; the fetcher checks the file signature and reports that
rather than caching HTML as a deck. All 93 current decks are readable.
