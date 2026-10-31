# OneSport - priebežné poznámky z rozhovoru

## Úvodná požiadavka používateľa

Používateľ požiadal asistenta, aby na základe súboru `Task_1 - convo.md`
vytvoril Architecture Decision Record (ADR) pre projekt OneSport.

Používateľ zároveň požiadal, aby sa počas ďalšej diskusie zapisovali stručné
poznámky o dôležitých bodoch rozhovoru, nie jeho doslovný prepis.

## Pripomienka a oprava

Používateľ vytkol, že stav ADR má byť `Accepted` namiesto `Navrhnuté`.
Asistent stav v súbore `ADR-001-onesport.md` opravil na `Accepted`.

## Ďalšia pripomienka a oprava

Používateľ vytkol, že ADR neobsahuje porovnávaciu tabuľku alternatív podľa
kritérií. Asistent doplnil tabuľku porovnávajúcu modulárny monolit,
mikroslužby a serverless/event-driven architektúru z hľadiska zložitosti,
konzistentnosti, škálovania, izolácie porúch, nákladov, testovania,
nasadzovania a budúceho rastu.

## Ďalšia pripomienka a oprava

Používateľ vytkol, že v ADR stále chýbajú explicitne definované rozhodovacie
kritériá. Asistent doplnil samostatnú sekciu s kritériami, ich prioritou a
vysvetlením. Do porovnávacej tabuľky pridal aj bezpečnosť osobných údajov a
odolnosť voči výpadku externého zdroja.

## Ďalšia pripomienka a oprava

Používateľ vytkol, že porovnávacia tabuľka nie je úplne zosúladená so zoznamom
rozhodovacích kritérií. Asistent upravil zoznam na samostatné kritériá pre
každý riadok tabuľky a zjednotil ich názvy v oboch častiach ADR.

## Ďalšia pripomienka a oprava

Používateľ požiadal o doplnenie vizuálnej architektúry. Asistent nahradil
ASCII diagram Mermaid diagramom komponentovej architektúry a pridal druhý
Mermaid diagram toku externého importu s validáciou, deduplikáciou a retry
mechanizmom.

## Ďalšia pripomienka a oprava

Používateľ požiadal o namapovanie požiadaviek na architektúru. Asistent
doplnil tabuľku, ktorá prepája user stories 1-24 s modulmi Auth/Profile,
Content, Collections a Social a uvádza konkrétne databázové alebo aplikačné
mechanizmy. Pridal aj mapovanie nefunkčných požiadaviek na bezpečnostné,
transakčné, výkonnostné, importné a testovacie rozhodnutia.

## Ďalšia pripomienka a oprava

Používateľ požiadal o doplnenie sekcie s nefunkčnými predpokladmi. Asistent
pridal tabuľku predpokladov o záťaži, veľkosti tímu, konzistentnosti,
externých zdrojoch, databáze, rozsahu ticketov a dostupnosti. Ku každému
predpokladu doplnil dôsledok pre návrh a signál na budúce prehodnotenie ADR.
