---
titel: Bremsen gegen Raten
kurz: Rate Limiting, und warum ein Login ohne Bremse eine offene Tür ist
dauer: 40 Minuten
projekt: mius.ch, MIus Notes, PräsenzTool
---
Ein gutes Passwort nützt wenig, wenn jemand beliebig oft raten darf. Ein sechsstelliger Code hat eine Million Möglichkeiten. Bei hundert Versuchen pro Sekunde ist er in drei Stunden durchprobiert. Mit einer Bremse von fünf Versuchen pro Viertelstunde dauert dasselbe im Schnitt über fünf Jahre.

## Was eine Bremse zählt

Eine Bremse (englisch **rate limiting**) zählt Ereignisse pro **Kennung** in einem **Zeitfenster** und lehnt ab, sobald eine Grenze erreicht ist. Die Wahl der Kennung ist die eigentliche Designfrage:

- **Pro IP-Adresse**: einfach, aber alle hinter demselben Schulnetz teilen sich eine Adresse. Und wer viele Adressen hat, umgeht sie.
- **Pro Konto oder E-Mail**: schützt ein bestimmtes Konto, erlaubt aber Angreifenden, ein fremdes Konto absichtlich zu sperren.
- **Beides kombiniert**: die übliche Lösung.

## Festes oder gleitendes Fenster

Das einfachste Verfahren zählt pro fester Viertelstunde (14:00 bis 14:15). An der Grenze lassen sich so doppelt so viele Versuche unterbringen: fünf um 14:14, fünf um 14:15. Ein **gleitendes Fenster** schaut immer auf die letzten fünfzehn Minuten ab jetzt und hat dieses Problem nicht. Dafür muss es die Zeitpunkte der einzelnen Versuche kennen.

## Den Mut, ehrlich zu antworten

Zwei Feinheiten aus deinen Projekten: Bots, die an einem Formular scheitern, sollen nicht merken, dass sie gescheitert sind, sonst probieren sie anders weiter. Das Kontaktformular auf mius.ch gibt einem erkannten Bot deshalb eine Erfolgsmeldung. Und ein Login soll gleich lang antworten, ob es die Adresse gibt oder nicht, sonst verrät die Antwortzeit, welche Konten existieren. MIus Notes macht das so.

## Projektbezug

**mius.ch**: `Mius\gedrosselt()` im gemeinsamen Kern zählt pro Bereich und Anschluss. Das Kontaktformular erlaubt fünf Anfragen pro Stunde, die Faden-Umfrage vierzig, damit ein ganzes Kollegium im selben Schulnetz mitmachen kann. Das ist eine bewusste Abwägung. **MIus Notes**: fünf Fehlversuche pro Adresse und zwanzig pro IP in fünfzehn Minuten, E-Mail-Adressen dafür nur als Hash gespeichert. **PräsenzTool**: Die Sperre zählt pro IP, das README nennt die Schwäche im Schulhaus selbst.

## Karten

F: Warum braucht ein Login eine Bremse, auch bei guten Passwörtern?
A: Ohne Bremse lässt sich beliebig oft raten. Kurze Codes und schwache Passwörter fallen dann in Stunden.

F: Was ist der Nachteil einer Bremse pro IP-Adresse an Schulen?
A: Alle hinter demselben Schulnetz teilen sich eine Adresse und sperren sich gegenseitig.

F: Was ist der Vorteil eines gleitenden gegenüber einem festen Zeitfenster?
A: Es lässt sich an der Fenstergrenze nicht überlisten. Es betrachtet immer die letzten n Sekunden ab jetzt.

F: Warum bekommt ein erkannter Bot auf mius.ch eine Erfolgsmeldung?
A: Damit er nicht merkt, dass er erkannt wurde, und nicht mit anderen Mitteln weiterprobiert.

F: Warum soll ein Login gleich lang dauern, ob es das Konto gibt oder nicht?
A: Sonst verrät die Antwortzeit, welche Konten existieren (Benutzer-Aufzählung).

## Prompt

```
Prüfe alle Stellen, an denen jemand etwas erraten oder massenhaft auslösen
kann: Login, Passwort vergessen, Codes, Einladungen, Formulare, teure
Schnittstellen. Gibt es eine Bremse? Was ist die Kennung, was das Zeitfenster,
was passiert an der Grenze? Kann jemand damit ein fremdes Konto sperren?
```

## Literatur

- OWASP: Authentication Cheat Sheet, Abschnitt «Protect Against Automated Attacks»; Blocking Brute Force Attacks. owasp.org
- OWASP (2023). *API Security Top 10*, API4:2023 Unrestricted Resource Consumption.
- NIST (2017, revidiert 2024). *SP 800-63B*, Abschnitt 5.2.2 Rate Limiting (Throttling).
