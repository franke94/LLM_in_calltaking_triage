- 1-30 transcripte von aufgenommenen Notrufen, ausgedacht und aufgenommen von erfahrenen Einsatzkröften mit unterschiedlicher medizinishcer Qualifikation (paramedics, EMT)
- 31-60 generated with Ai support (see emergency_call_simulator)
- cases for calls 31-60
- calls are originally in german, but translated to english using openAi GPT5.2, die Übersetzungen sind nicht im Detail überprüft und können entsprechend leicht abweichen. Die Untersuchungen wurden auf den Deutschen Fällen gemacht 
- Abfrage ohne technische Hilfsmitte, ohne besondere Vorgabe zu den Fragen, Fokus bestand auf technischer Umsetzung, nicht auf medizinischer Qualität der Abfrage
- zukünftig ist der Test auf echten Calls geplant, Fokus derzeit ist die Vorbereitung und das Sammeln von Erfahrungen mit LLMs und Notrufen

- bewertung der cases: Bewertungen der cases durch erfahrende paramedics. 
- Gezeigt hat sich: Die Bewertung ist gar nicht so eindeutig, insbesondere da keien Möglichkeiten mehr bestehen nachfragen zu stellen und die Notrufe unvollständig abgefragt sind
- Vorgehen: Calls wurden unabhängig von 2 paramedics bewertet, die Beschreibungen die den paramedics vorgelegen haben sind anbei 
- Bei unklarheiten wurden die Fälle einer Dritten Bewertet vorgelegt. 
- Ausgewertet wurde die Mehrheit der Bewertungen 
- Bei einigen Fällen (8 calls, je 1 Kategorie) konnte keien Mehrheit festgestellt werden, da keine Bewertun überwog. Diese Fälle wurden in einer Fallbesprechung nachbesprochen und ein gemeinsamer Konsens konnte hergestellt werden 
- Die Confidence ist in der confidence-Table angegeben. (1 = Volle confidence, also alle Bewertungen haben übereingestimmt, 0.5 = 2 von 3 Bewertungen haben übereingestimmt, 0 = Bewertungen haben nicht übereingestimmt)

- Interessant ist: Die Auswertung ist gar nicht so eindeutig, das Verfahren langwierig hier gute Daten aufzubauen trotz der fgeringen Fallzahl 
- Werden reale Cases verwendet, liegt zumindest eine bewertung bereits vor, die Problematik bleibt aber die gleiche: Nur eien BEwertung, keien Möglichkeit mehr nachzufragen, nur sehr eingeschränkte Möglichkeiten die Bewertung zu veriizieren (etwa durch RD-Protokolle, die aber nicht die Situation während des anrufes wiederspiegeln) 

- Wieso also eine so kleinteilige Auswertung: Ziel ist das Human-AI-Teaming zu erreichen, Calltaker muss nachvollziehen können wieso die AI gewisse maßnahmen vorschlägt. ABCDE Schema ist da sehr gebräuchlich, kann in allen Fällen standartisiert angewendet werden, macht keine Diagnose etc. reine Zustandsbeschreibung 

- Anpassung der Beschreibungen notwendig und möglich, z.B. ist im Pretest aufgefallen, dass explizit Schlussfolgerungen erlaubt sein müssen (keine Angabe, kann aber normal sprechen: keine Einschränkungne zu erwarten -> Das macht der Menschliche Calltaker auch)

- Erfahrung mit der Callgenerierung: Muss wenn man das im größeren Stil machen muss noch feinjustieren, manche Fälle wiederholen sich etwas, Ortsangaben sollten mit übergeben werden.
- Aber: Calltaking klappt gut, muss aber noch getestet werden ob konsistent

- Vorteil davon, dass es reine synthetische Calls sind: Es sind keine Datenschutzvorgabne zu behandlen, z. B. können kommerzielle Modelle verwendet werden, die hohen Anforderungen sind nicht notwendig (z. B. Selbst Hosten des Modells, etc.)
