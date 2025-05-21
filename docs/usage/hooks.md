---
title: Hooks
---

Maya udstiller en række `hooks` i sin kildekode, der kan bruges til an ændre måden Maya eksekverer sin kode på.

Ved at implementere en eller flere af disse `hooks` kan man med andre ord skrive en slags *letvægtsplugin*. Man skal blot bruge `@hookimpl` decoratoren på en funktion, der er navngivet efter en af Mayas hooks, og som accepterer en eller flere af de dokumenterede parametre, der bliver sendt til det hook.

Alle hook-implementeringer, der er implementeret i et python-modul (`.py`-fil) i roden af "hooks"-mappen i projektets BASE_DIR, bliver automatisk integereret i Mayas kodeeksekvering. Hvis samme hook er implementeret i flere python-moduler, eksekveres de i alfabetisk rækkefølge.

## Eksempel

For example, you can implement the render_cell plugin hook like this even though the full documented hook signature is render_cell(row, value, column, table, database, datasette):

## Liste af hooks

###
