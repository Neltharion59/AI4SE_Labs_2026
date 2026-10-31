# Task 3 - porovnávacia správa

## Vytvorený skill

Skill je uložený v:

`.github/skills/architecture-decision-record/SKILL.md`

Je určený na opakovateľný workflow pre návrh architektúry a tvorbu ADR.
Obsahuje postup od analýzy požiadaviek cez porovnanie troch alternatív až po
výber riešenia, Mermaid diagramy, mapovanie požiadaviek, predpoklady, riziká a
validáciu výsledku. Súčasťou je aj pravidlo zapisovať používateľove pripomienky
a následné opravy do konverzačných poznámok.

## Porovnanie pred skillom a po jeho vytvorení

### Pred skillom

Pri Task 1 a Task 2 vznikol kvalitný ADR, ale jeho tvorba prebiehala
iteratívne. Po prvom návrhu bolo postupne potrebné doplniť:

- stav `Accepted`;
- porovnávaciu tabuľku alternatív;
- explicitné rozhodovacie kritériá;
- zosúladenie kritérií s riadkami tabuľky;
- vizuálnu architektúru v Mermaide namiesto ASCII diagramu;
- mapovanie user stories a nefunkčných požiadaviek;
- sekciu nefunkčných predpokladov.

Záznam v `Task_2 - convo.md` ukazuje, že tieto nedostatky boli odhalené až
po kontrole vytvoreného ADR. Práca bola preto rozdelená do viacerých opráv.

### Po vytvorení skillu

Skill zhromažďuje tieto požiadavky do jedného checklistu a určuje ich poradie:

1. načítať požiadavky a existujúce poznámky;
2. navrhnúť najmenej tri architektúry a ich trade-offs;
3. explicitne definovať a prioritizovať kritériá;
4. vytvoriť tabuľku s presnou zhodou kritérií a riadkov;
5. pridať Mermaid komponentový a procesný diagram;
6. namapovať funkčné aj nefunkčné požiadavky;
7. oddeliť predpoklady od požiadaviek;
8. overiť výsledný dokument a zaznamenať každú používateľovu pripomienku.

Po vytvorení skillu bol Task 1 a Task 2 skutočne zopakovaný od nuly ako
samostatný druhý beh na kratšom systéme RecipeCove. Výsledkom je nový
`ADR-002-recipecove.md` a záznam
`Task_3 - convo.md`. Druhý beh mal 0 používateľských pripomienok v prvej
spätnej väzbe. Následná úplná kontrola však našla 4 nedostatky v novom ADR,
ktoré boli opravené: chýbajúci druhý Mermaid diagram, samostatné mapovanie
nefunkčných požiadaviek, podrobnosti alternatív a explicitné riziká a overenie.

## Výsledok porovnania

| Oblasť | Bez skillu | So skillom |
|---|---|---|
| Začiatok práce | Manuálne hľadanie relevantných súborov a formátu ADR | RecipeCove: požiadavky a skill načítané pred návrhom |
| Alternatívy | Boli doplnené počas diskusie | RecipeCove: tri alternatívy v prvom návrhu |
| Kritériá | Najprv chýbali, potom sa dopĺňali | RecipeCove: kritériá definované pred tabuľkou |
| Vizualizácia | ASCII diagram bol neskôr nahradený | RecipeCove: Mermaid diagram bol súčasťou prvého ADR |
| Traceability | Mapovanie požiadaviek vzniklo až po pripomienke | RecipeCove: všetkých 14 user stories namapovaných v prvom návrhu |
| Predpoklady | Dopĺňané neskôr | RecipeCove: samostatná sekcia v prvom návrhu |
| Opravy po prvej spätnej väzbe | 7 zaznamenaných pripomienok/oprav v Task 2 | 0 pripomienok |
| Opravy po úplnej kontrole | Dopĺňané postupne počas diskusie | 4 nedostatky nájdené a opravené |

## Záver

Skutočný druhý beh na RecipeCove dosiahol hlavný cieľ skillu: návrh alternatív
a ADR vznikli v jednom pracovnom behu bez bezprostredných používateľských
pripomienok. Úplná následná kontrola však našla 4 nedostatky, takže poctivé
porovnanie je 7 opráv v prvom behu oproti 4 opravám v druhom behu. To ukazuje
menej iterácií, hoci presné časové zrýchlenie nebolo merané a systémy mali
rozdielnu veľkosť a spôsob revízie, preto sú tieto počty iba orientačné.

RecipeCove ADR má stav `Proposed`, pretože druhý návrh ešte nebol používateľom
schválený. Stav `Accepted` zostáva iba pri pôvodnom OneSport ADR, kde ho
používateľ výslovne požadoval.

Následná revízia zároveň odhalila tri nedostatky v pôvodnom OneSport ADR:
diagramu chýbali worker a externé API, kritériá neboli zoradené podľa priority
a jeden dôvod odkazoval iba na Task 1. To ukazuje, že checklist skillu nebol
pri pôvodnej kontrole dodržaný dôsledne, hoci tieto pravidlá v skille existujú.
