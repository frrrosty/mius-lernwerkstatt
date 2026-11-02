---
titel: Die Lieferkette
kurz: Fremder Code in deinen Projekten, festgelegte Versionen und warum ein Tag kein Versprechen ist
dauer: 40 Minuten
projekt: Shutter Call, MIus Notes, Lernwerkstatt
---
Der meiste Code in deinen Anwendungen stammt nicht von dir und nicht von Claude. Er kommt aus Paketen (npm, Composer, PyPI) und, in der Pipeline, aus GitHub Actions. Jedes dieser Teile kann angreifbar sein oder böswillig verändert werden. Das ist die **Lieferkette** (supply chain).

## Was passieren kann

- **Bekannte Lücken** in Paketen: Sie werden in Datenbanken wie der GitHub Advisory Database erfasst. `npm audit` und `composer audit` gleichen deine Abhängigkeiten damit ab.
- **Übernommene Pakete**: Jemand übernimmt das Konto einer Paketbetreuerin und veröffentlicht eine Version mit Schadcode. 2024 wurde in xz-utils eine Hintertür entdeckt, die über zwei Jahre von einer vermeintlich hilfsbereiten Mitarbeiterin eingebaut worden war.
- **Verschobene Tags**: Eine GitHub Action wird oft mit einem Tag eingebunden, etwa `actions/checkout@v4`. Ein Tag ist aber nur ein Name, der auf einen Commit zeigt, und er lässt sich verschieben. Im März 2025 wurden die Tags der verbreiteten Action `tj-actions/changed-files` auf einen Commit umgebogen, der Secrets in die Protokolle schrieb. Betroffen waren alle, die die Action per Tag einbanden.

## Festlegen statt vertrauen

Die Gegenmassnahme heisst **Pinning**: Die Version wird auf einen unveränderlichen Wert festgelegt.

- Für Actions: der volle Commit-Hash mit 40 Zeichen, der Tag als Kommentar dahinter.
  `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2`
- Für Pakete: eine Lock-Datei (`package-lock.json`, `composer.lock`) mit exakten Versionen und Prüfsummen, eingecheckt im Repo, und in der CI `npm ci` statt `npm install`.
- Für Dateien, die man selbst herunterlädt: eine Prüfsumme vergleichen.

Pinning hat einen Preis: Updates kommen nicht mehr von selbst. Dafür gibt es Dependabot, das Pull Requests für neue Versionen öffnet, die man dann bewusst prüft und übernimmt.

## Projektbezug

**Shutter Call** bindet Actions per Tag ein (`actions/checkout@v4`, `r0adkll/upload-google-play@v1.1.3`). Gerade der Upload in den Play Store bekommt das Dienstkonto für Google Play. Ein verschobener Tag dort wäre gefährlich. **MIus Notes** prüft bei jedem Push mit `composer audit` und `npm audit`, und Dependabot meldet neue Versionen. **Die Lernwerkstatt** selbst lädt Python (Pyodide) beim Bauen aus npm und prüft dabei die SHA-512-Prüfsumme, die npm veröffentlicht. Stimmt sie nicht, bricht der Bau ab. Und ihre CI bindet Actions per Commit-Hash ein. Die Übung unten prüft genau das.

## Karten

F: Was ist die Lieferkette einer Software?
A: Alles, was nicht selbst geschrieben ist und mitläuft: Pakete, Bibliotheken, Actions, Container, Werkzeuge im Build.

F: Warum ist `uses: aktion@v4` riskant?
A: Ein Tag ist ein verschiebbarer Name. Wer das Repo der Action kontrolliert, kann ihn auf anderen Code zeigen lassen, der dann mit deinen Secrets läuft.

F: Woran erkennt man eine auf einen Commit festgelegte Action?
A: Hinter dem @ steht ein 40-stelliger Hexadezimal-Hash statt eines Namens.

F: Was macht eine Lock-Datei?
A: Sie hält exakte Versionen und Prüfsummen aller Abhängigkeiten fest, damit jeder Bau dieselben Pakete verwendet.

F: Was ist der Nachteil von Pinning, und wie gleicht man ihn aus?
A: Sicherheits-Updates kommen nicht automatisch. Dependabot oder Renovate öffnen dafür Pull Requests, die man prüft.

## Prompt

```
Prüfe die Lieferkette dieses Projekts: Sind alle GitHub Actions auf einen
Commit-Hash festgelegt? Welche Actions bekommen Secrets? Gibt es Lock-Dateien,
und nutzt die CI npm ci bzw. composer install aus dem Lock? Läuft ein Audit?
Welche Rechte hat der GITHUB_TOKEN (permissions:)? Mach Vorschläge mit dem
genauen Hash, nicht nur mit dem Tag.
```

## Literatur

- GitHub Docs: Security hardening for GitHub Actions, Abschnitt «Using third-party actions». docs.github.com
- CISA (2025). Supply Chain Compromise of Third-Party tj-actions/changed-files (CVE-2025-30066). cisa.gov
- Ohm, M., Plate, H., Sykosch, A., Meier, M. (2020). Backstabber's Knife Collection: A Review of Open Source Software Supply Chain Attacks. *DIMVA 2020*, LNCS 12223, Springer.
- OpenSSF: Supply-chain Levels for Software Artifacts (SLSA). slsa.dev
