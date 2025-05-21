---
title: Installation
---

# Installation
Maya er primært tænkt som et kommandline værktøj, men hvis man vil, kan man også clone github-repo'et, for ydermere at se, hvordan det er bygget og eventuelt bidrage til udviklingen af værktøjet.

Det er muligt at installere *Maya* på alle platforme, der har `pipx` eller `uv` installeret.

### Brug pipx
[`pipx`](https://pipx.pypa.io/stable/) er et program til at installere python-baseret software inklusiv alle dets afhængigheder i isolerede miljøer, hvorved man undgår at installere programmer direkte i ens styresystem. Hvis du har `pipx` på dit system, installerer du `maya` således:

`$ pipx install git+https://github.com/aarhusstadsarkiv/maya.git`

### Brug uv
[`uv`](https://docs.astral.sh/uv/) er et package- og projektmanagement program til håndtering af python applikationer, men det indholder også et `pipx`-ækvivalent værktøj, hvormed du kan installere `maya`:

`$ uv tool install git+https://github.com/aarhusstadsarkiv/maya.git`

## Windows-installation

- hent latest release
- gem lokalt
- powershell (fuld sti eller i PATH-var)

## Test intallationen
Når du har installeret `maya` med enten `pipx`, `uv` eller som .exe-fil på Windows