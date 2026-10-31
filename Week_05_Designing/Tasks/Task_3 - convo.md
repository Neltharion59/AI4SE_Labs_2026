# OneSport - opakovanie Task 1 a Task 2 so skillom

## Nová požiadavka

Používateľ požiadal asistenta, aby po vytvorení skillu zopakoval postup z Task 1
a Task 2 a porovnal ho s pôvodným postupom.

## Použitý skill

Asistent použil skill
`.github/skills/architecture-decision-record/SKILL.md`.
Skill vyžadoval načítanie požiadaviek OneSport, poznámok z Task 1 a Task 2,
porovnanie troch architektúr, rozhodovacie kritériá, Mermaid diagramy,
mapovanie požiadaviek, predpoklady a validačný checklist.

## Skutočné opakovanie Task 1 na RecipeCove

Po vytvorení skillu bol na požiadavkách z `data/RecipeCove.txt` vytvorený nový
návrh od nuly. Zvolené boli tri alternatívy:

1. modulárny monolit;
2. mikroslužby;
3. serverless/event-driven architektúra.

Pri každej alternatíve boli v novom zázname popísané hranice komponentov,
vlastníctvo dát, komunikácia, nasadenie, konzistentnosť, zlyhania a náročné
implementačné časti.

## Skutočné opakovanie Task 2 na RecipeCove

Bol vytvorený nový `ADR-002-recipecove.md`, nie iba skontrolovaný existujúci
ADR. Obsahuje:

- stav `Proposed` a rozhodnutie;
- tri porovnané alternatívy a prioritizované kritériá;
- porovnávaciu tabuľku so zhodnými názvami kritérií;
- dva Mermaid diagramy;
- mapovanie všetkých 14 user stories;
- samostatné mapovanie nefunkčných požiadaviek;
- bezpečnosť OAuth, transakcie, retry, riziká a overenie.

Počet používateľských pripomienok v pôvodnom druhom behu: **0**. Následná
úplná kontrola však našla štyri nedostatky: chýbajúci druhý Mermaid diagram,
chýbajúce samostatné mapovanie nefunkčných požiadaviek, nedostatočne podrobné
alternatívy a chýbajúce explicitné riziká a overenie. Všetky štyri boli
opravené.

## Spätná väzba a oprava záznamu

Pôvodná verzia tohto záznamu opisovala iba kontrolu existujúceho ADR.
Neskôr bol vykonaný skutočný beh Task 1 a Task 2 od nuly na systéme
RecipeCove. Následne boli report a tento záznam zosúladené s týmto skutočným
priebehom.

## Následná kontrola pôvodného OneSport ADR

Pri následnej revízii boli nájdené tri nedostatky v pôvodnom
`ADR-001-onesport.md`: hlavný Mermaid diagram neobsahoval import worker ani
externé API, poradie kritérií nebolo zoradené podľa priority a odkaz na Task 1
neuvádzal konkrétny dôvod. Všetky tri nedostatky boli opravené.

## Úplná kontrola po ďalšej spätnej väzbe

Používateľ požiadal o faktické overenie všetkých výstupov. Kontrola odhalila
štyri nedostatky v novom RecipeCove ADR uvedené vyššie. ADR, report a tento
záznam boli následne zosúladené s výsledkom kontroly.
