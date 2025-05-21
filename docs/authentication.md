---
title: Authentication
---

# Authentication
For at teste, udvikle og efterfølgende sætte en Maya-baseret web-klient i produktion, skal man bruge en API-nøgle.

API-nøglen er ikke offentlig, så pas på med at pushe den til Github eller hvilket versionsstyringsprogram man end måtte bruge. For at få udleveret en API-nøgle skal sende en mail til Aarhus Stadsarkiv (stadsarkiv@aarhus.dk) med emnet: "API-nøgle til Maya".

# .env vs. ENVIRONMENT
Den nemmeste måde at håndtere API-nøglen på, er at gemme den i en `.env`-fil i roden af projektets BASE_DIR med navnet "API_KEY". Eksempelvis:

```shell
me@LAPTOP:~/min-maya-klient$ cat .env
API_KEY=your_api_key
```

!!! Bemærk
    > .env-filer er blot simple key-value filer, der bruges til at gemme variabler, ofte af privat karakter:
    ```
    SUPER_SECRET_API_KEY = "a;ljskdshhhDONTTELLkljasdfhio"
    DATABASE_URL=secrets://username:password@localhost:11/secrets
    OTHER_SECRET = "awefWhatevERjlk;a"
    ```

Alternativt kan man benytte API-nøglen direkte som en miljøvariabel.

Links til linux, mac og pc

## Demo uden API-nøgle
Hvis man vil se, hvordan en ukonfigureret Maya-klient se ud og fungerer, kan man som nævnt kigge på demo-siden: https://demo.openaws.dk
