---
title: Changelog
---

## v6.2.8

### Changes
* `edit original puid` and `edit master puid` can now change the file signature with the `--signature` option
* `edit` commands can change multiple properties at the same time
* `extract` has an improved commit logic 

...

## v6.2.4

### New Features
* `QUERY` arguments now support the `@not` token for negative matches

### Changes
* `extract` command is faster and keeps its speed regardless of database size

### Fixes
* Fix `extract` saving files from Web Archives with their query parameters in the file name
* Fix `edit original rename` raising exceptions without logging which file caused it
* Fix `identify statutory` command missing its help text
