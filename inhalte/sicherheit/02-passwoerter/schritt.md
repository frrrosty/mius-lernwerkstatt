---
titel: Passwörter richtig speichern
kurz: Hash statt Verschlüsselung, Salz, absichtlich langsam, Vergleich in konstanter Zeit
dauer: 45 Minuten
projekt: MIus Notes, PräsenzTool
---
Jede Anwendung mit Anmeldung muss Passwörter prüfen, ohne sie zu kennen. Das klingt widersprüchlich und ist der Kern dieses Schritts.

## Hash statt Verschlüsselung

Eine **Verschlüsselung** lässt sich mit dem Schlüssel rückgängig machen. Wer in den Server einbricht, findet oft auch den Schlüssel, und dann alle Passwörter. Eine **kryptografische Hashfunktion** dagegen ist eine Einbahnstrasse: Aus dem Passwort entsteht ein Fingerabdruck fester Länge, aus dem Fingerabdruck lässt sich das Passwort nicht zurückrechnen. Beim Anmelden wird das eingegebene Passwort erneut gehasht und mit dem gespeicherten Fingerabdruck verglichen.

## Salz

Gleiche Passwörter ergeben gleiche Hashes. Angreifende nutzen das mit vorberechneten Tabellen («Rainbow Tables»): Einmal die Hashes von Millionen häufiger Passwörter berechnen, dann nur noch nachschlagen. Dagegen hilft ein **Salz**: ein zufälliger Wert pro Person, der vor dem Hashen an das Passwort gehängt und offen neben dem Hash gespeichert wird. Gleiche Passwörter ergeben nun verschiedene Hashes, und jede Tabelle müsste pro Person neu berechnet werden.

## Absichtlich langsam

SHA-256 ist schnell. Eine Grafikkarte berechnet Milliarden davon pro Sekunde. Für Passwörter ist das schlecht: Ein gestohlener Hash eines achtstelligen Passworts ist so in Stunden geknackt. Passwort-Hashfunktionen sind deshalb **absichtlich teuer**: PBKDF2 wiederholt den Hash hunderttausendfach, bcrypt und Argon2 brauchen zusätzlich viel Speicher, was Grafikkarten bremst. Argon2id gewann 2015 die Password Hashing Competition und ist heute die Empfehlung von OWASP.

## Vergleich in konstanter Zeit

Ein normaler Vergleich `a == b` bricht beim ersten unterschiedlichen Zeichen ab. Aus der Antwortzeit lässt sich so im Prinzip ablesen, wie viele Zeichen stimmen (**Timing-Angriff**). Für Geheimnisse gibt es deshalb Vergleiche, die immer gleich lang dauern: in Python `hmac.compare_digest`, in PHP `hash_equals`.

## Projektbezug

**MIus Notes** nutzt Argon2id mit mindestens zwölf Zeichen und dazu einen zweiten Faktor. **Die MIUS-Plattform** (konto.mius.ch, mius-website) nutzt bcrypt mit mindestens zehn Zeichen und ohne zweiten Faktor. Beides ist vertretbar. Der Unterschied ist eine Abwägung, die du begründen können solltest: Was schützt MIus Notes, was die Einkaufsliste?

**Das PräsenzTool** speichert Kartentokens als `sha256(token + pepper)`, also schnell und ohne Salz. Ist das ein Fehler? Nein, und hier steckt ein wichtiger Unterschied: Die Tokens sind keine von Menschen gewählten Passwörter, sondern lange Zufallswerte. Bei einem 128-Bit-Zufallswert hilft auch die schnellste Grafikkarte nichts, langsames Hashen ist überflüssig. Der **Pepper** ist ein geheimer Wert, der nur in der Konfiguration auf dem Server liegt, nicht in der Datenbank. Wer nur die Datenbank stiehlt, kann damit gar nichts prüfen.

## Karten

F: Warum werden Passwörter gehasht und nicht verschlüsselt?
A: Eine Verschlüsselung lässt sich mit dem Schlüssel umkehren, und der liegt oft auf demselben Server. Ein Hash lässt sich nicht umkehren, nur nachrechnen.

F: Wogegen schützt ein Salz?
A: Gegen vorberechnete Tabellen und dagegen, dass gleiche Passwörter gleiche Hashes ergeben. Es muss nicht geheim sein.

F: Was ist der Unterschied zwischen Salz und Pepper?
A: Das Salz ist pro Person verschieden und liegt neben dem Hash in der Datenbank. Der Pepper ist für alle gleich, geheim und liegt ausserhalb der Datenbank.

F: Warum darf SHA-256 für Kartentokens im PräsenzTool schnell sein?
A: Die Tokens sind lange Zufallswerte, kein menschliches Passwort. Ihr Suchraum ist zu gross zum Durchprobieren, egal wie schnell.

F: Wozu dient `hmac.compare_digest`?
A: Es vergleicht zwei Werte in konstanter Zeit, damit die Antwortzeit nicht verrät, wie viele Zeichen übereinstimmen.

## Prompt

Prüf Anmeldecode gezielt, statt «ist das sicher?» zu fragen:

```
Prüfe, wie dieser Code Passwörter speichert und vergleicht. Beantworte einzeln:
Welche Hashfunktion, mit welchen Parametern? Gibt es ein Salz pro Person?
Wird in konstanter Zeit verglichen? Was passiert bei einem Datenbank-Leck?
Vergleiche mit der Empfehlung im OWASP Password Storage Cheat Sheet und nenne
Abweichungen mit Fundstelle im Code.
```

## Literatur

- OWASP: Password Storage Cheat Sheet. cheatsheetseries.owasp.org
- NIST (2017, revidiert 2024). *SP 800-63B: Digital Identity Guidelines, Authentication and Lifecycle Management*, Abschnitt 5.1.1.
- Biryukov, A., Dinu, D., Khovratovich, D. (2016). Argon2: New Generation of Memory-Hard Functions for Password Hashing and Other Applications. *IEEE European Symposium on Security and Privacy*.
- Python-Dokumentation: Modul `hashlib`, Abschnitt «Key derivation», und Modul `hmac`.
