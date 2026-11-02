---
titel: Denken wie Angreifende
kurz: Schutzziele, Bedrohungsmodell und Risiko, bevor eine einzige Massnahme kommt
dauer: 40 Minuten
projekt: PräsenzTool
---
Sicherheit beginnt nicht mit Werkzeugen, sondern mit drei Fragen: Was ist wertvoll? Wer will es? Was kann schiefgehen? Ohne diese Fragen wird Sicherheit eine Liste einzelner Massnahmen, von denen niemand weiss, ob sie das Wichtige schützen.

## Schutzziele

Die klassische Einteilung heisst CIA, nach den englischen Begriffen:

- **Vertraulichkeit** (confidentiality): Nur Berechtigte sehen die Daten. Beispiel: Die Notizen in MIus Notes sieht nur ihre Besitzerin.
- **Integrität** (integrity): Daten werden nicht unbemerkt verändert. Beispiel: Niemand kann im PräsenzTool die Präsenz einer anderen Person eintragen.
- **Verfügbarkeit** (availability): Das System funktioniert, wenn es gebraucht wird. Beispiel: Der Check-in muss am Anlass klappen, auch wenn 30 Handys gleichzeitig kommen.

Oft kommen **Authentizität** (wer etwas getan hat, ist eindeutig) und **Nachvollziehbarkeit** dazu.

## Ein Bedrohungsmodell

Ein Bedrohungsmodell ist eine strukturierte Antwort auf «Was kann schiefgehen?». Adam Shostack fasst den Ablauf in vier Fragen: Woran arbeiten wir? Was kann schiefgehen? Was tun wir dagegen? Haben wir es gut gemacht?

Für die zweite Frage hilft **STRIDE**, eine Liste von sechs Bedrohungsarten, die Microsoft Ende der 1990er-Jahre eingeführt hat:

| Bedrohung | Verletzt | Beispiel |
|---|---|---|
| Spoofing, Identität vortäuschen | Authentizität | Mit fremder QR-Karte einchecken |
| Tampering, Daten verändern | Integrität | Eine Antwort im Faden nachträglich ändern |
| Repudiation, Abstreiten | Nachvollziehbarkeit | «Ich habe das nie gelöscht» |
| Information disclosure, Preisgabe | Vertraulichkeit | Klarnamen gelangen auf den Server |
| Denial of service, Lahmlegen | Verfügbarkeit | Formular mit Anfragen fluten |
| Elevation of privilege, Rechte erschleichen | alle | Studierende erhalten Adminrechte |

## Risiko

Nicht jede Bedrohung ist gleich ernst. Eine einfache, verbreitete Bewertung multipliziert **Wahrscheinlichkeit** und **Schaden**, je auf einer Skala von 1 bis 5. Das Ergebnis ist grob, aber es zwingt zum Priorisieren. Wichtig: Die Zahlen sind Einschätzungen, keine Messungen. Ihr Wert liegt im Gespräch darüber.

## Projektbezug

Das PräsenzTool hat ein Bedrohungsmodell, ohne dass es so heisst. Im README steht: «Ein weitergereichter QR nützt nichts ohne den Anlasscode, und ein weitergereichter Anlasscode nützt nichts ohne eine Karte.» Das ist eine Antwort auf Spoofing: Präsenz erschleicht nur, wer beides hat. Und: «Was der Server nie kennt: Klarnamen.» Das ist eine Antwort auf Information Disclosure. Was der Server nicht hat, kann nicht gestohlen werden.

Eine Lücke steht ebenfalls im README: Die Sperre nach falschen Codes zählt pro IP-Adresse, und in einem Schulhaus teilen sich alle eine Adresse. Das ist ein Zielkonflikt zwischen Verfügbarkeit und Schutz gegen Raten. Genau solche Abwägungen macht ein Bedrohungsmodell sichtbar.

## Karten

F: Welche drei Schutzziele fasst CIA zusammen?
A: Vertraulichkeit, Integrität, Verfügbarkeit.

F: Wofür steht STRIDE?
A: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.

F: Welche vier Fragen stellt Shostack für ein Bedrohungsmodell?
A: Woran arbeiten wir? Was kann schiefgehen? Was tun wir dagegen? Haben wir es gut gemacht?

F: Warum schützt «Der Server kennt keine Klarnamen» im PräsenzTool so gut?
A: Daten, die nicht gespeichert sind, können bei einem Einbruch nicht preisgegeben werden. Datensparsamkeit ist die stärkste Massnahme gegen Information Disclosure.

F: Warum ist Risiko = Wahrscheinlichkeit × Schaden nur ein grobes Mass?
A: Beide Werte sind Einschätzungen auf einer groben Skala. Das Produkt hilft beim Priorisieren und Diskutieren, ist aber keine Messung.

## Prompt

Lass Claude ein Bedrohungsmodell machen, bevor es Massnahmen vorschlägt:

```
Mach für diese Anwendung ein Bedrohungsmodell nach STRIDE, bevor du
Massnahmen vorschlägst. Liste zuerst die schützenswerten Daten und die
Eingänge (Formulare, Schnittstellen, Dateien). Bewerte jede Bedrohung mit
Wahrscheinlichkeit und Schaden von 1 bis 5 und sortiere nach Risiko.
Sag bei jeder Einschätzung, worauf sie beruht.
```

## Literatur

- Shostack, A. (2014). *Threat Modeling: Designing for Security*. Wiley.
- Anderson, R. (2020). *Security Engineering* (3. Aufl.), Kapitel 1 und 2. Wiley.
- OWASP: Threat Modeling Cheat Sheet. cheatsheetseries.owasp.org
- Bundesamt für Sicherheit in der Informationstechnik (BSI): IT-Grundschutz-Kompendium, Kapitel «Risikoanalyse» (BSI-Standard 200-3).
