# OneSport - priebežné poznámky z rozhovoru

## Úvodná požiadavka používateľa

Používateľ požiadal asistenta, aby:

- prečítal požiadavky projektu OneSport v priečinku `data`,
- počas celého ďalšieho rozhovoru priebežne zapisoval poznámky,
- zapisoval iba zhrnutie dôležitých častí, nie doslovný prepis.

## Prečítané zdroje

- `Week_05_Designing/Tasks/data/OneSport.txt`
- `Week_05_Designing/Tasks/Task_1.md`

## Zhrnutie požiadaviek OneSport

OneSport má byť platforma poskytujúca aktuálne športové správy, informácie o
športových udalostiach a dostupné vstupenky na športové podujatia.

Identifikované oblasti funkcionality:

1. registrácia, prihlasovanie, odhlasovanie a správa používateľského profilu;
2. zmena e-mailu a hesla a vymazanie používateľského účtu;
3. zobrazovanie najnovších športových správ;
4. filtrovanie správ podľa krajiny;
5. pridávanie a odstraňovanie obľúbených správ;
6. zobrazovanie a filtrovanie dostupných vstupeniek podľa krajiny;
7. pridávanie a odstraňovanie vstupeniek v osobnej kolekcii;
8. vymazanie všetkých uložených správ a vstupeniek;
9. vyhľadanie iného používateľa podľa e-mailu;
10. odosielanie, prijímanie, prijímanie/odmietanie a mazanie žiadostí o priateľstvo;
11. zobrazovanie, správa a odstránenie priateľov;
12. zobrazovanie kolekcie uložených správ a vstupeniek.

## Rozhovor:

### Požiadavka používateľa

Používateľ požiadal o návrh jednej možnej architektúry pre OneSport.

### Návrh: modulárny monolit s REST API

OneSport môže byť implementovaný ako **modulárny monolit**. Backend by bol
jedna nasadzovaná aplikácia, ale zdrojový kód by bol rozdelený na samostatné
moduly. Webová aplikácia by s backendom komunikovala cez HTTPS REST API.

```text
Webové používateľské rozhranie
            |
         REST API
            |
     OneSport backend
  +---------+----------+---------+
  | Auth    | Content  | Social  |
  | Profile | News and | Friends |
  |         | Tickets  |         |
  +---------+----------+---------+
            |
        PostgreSQL
```

#### Moduly

- **Auth/Profile**: registrácia, prihlasovanie, odhlasovanie, relácie, zmena
  e-mailu a hesla, nastavenia profilu a vymazanie účtu;
- **News**: ukladanie a zobrazovanie správ, filtrovanie podľa krajiny;
- **Tickets/Events**: športové udalosti, dostupné vstupenky a filtrovanie;
- **Collections**: obľúbené správy a uložené vstupenky používateľa;
- **Social**: vyhľadávanie používateľov podľa e-mailu, žiadosti o priateľstvo
  a správa zoznamu priateľov.

#### Dáta a komunikácia

Ako databáza by sa použil PostgreSQL s tabuľkami napríklad `users`, `sessions`,
`news`, `tickets`, `saved_news`, `saved_tickets`, `friend_requests` a
`friendships`. Vzťahy medzi používateľmi a ich uloženými položkami by boli
reprezentované relačnými tabuľkami.

API by poskytovalo endpointy pre autentifikáciu, profil, správy, vstupenky,
kolekcie a sociálne funkcie. Každý endpoint pracujúci s osobnými údajmi by
overoval prihlásenie a vlastníctvo dát. Heslá by sa ukladali iba ako bezpečné
hash hodnoty. Databáza by pomocou unikátnych obmedzení bránila napríklad
duplicitným e-mailom alebo opakovanému uloženiu rovnakej správy.

### Požiadavka používateľa

Používateľ požiadal o trade-offs.

### Trade-offs navrhnutej architektúry

#### Výhody, ktoré získame

- **Jednoduchší vývoj a nasadenie:** všetky moduly sa nasadzujú ako jedna
  aplikácia, takže tím nemusí spravovať viacero služieb a deploymentov.
- **Konzistentnosť dát:** PostgreSQL a transakcie umožnia bezpečne meniť
  súvisiace dáta naraz, napríklad pri prijatí žiadosti o priateľstvo.
- **Jednoduchšie dotazy:** kolekcie, správy, vstupenky a priateľstvá môžu
  používať relačné väzby a JOIN operácie.
- **Jednoduchšie testovanie:** požiadavka prechádza jednou aplikáciou a logy
  sú sústredené na jednom mieste.
- **Nižšia počiatočná cena:** na začiatku stačí jeden backend a databáza.

#### Nevýhody, ktoré akceptujeme

- **Obmedzené nezávislé škálovanie:** ak je zaťažený iba News modul, zvyčajne
  sa škáluje celý backend, nie iba tento modul.
- **Riziko prepojeného kódu:** ak moduly začnú priamo používať cudzie tabuľky
  alebo interné triedy, systém sa bude ťažšie udržiavať.
- **Spoločný deployment:** chyba v jednom module môže zablokovať nasadenie
  celej aplikácie.
- **Spoločná databáza ako úzke miesto:** veľké množstvo správ alebo akcií
  používateľov môže zvýšiť záťaž na jednu databázu.
- **Ťažšia budúca migrácia:** nedodržané hranice modulov by skomplikovali
  vyčlenenie napríklad Social alebo Content modulu do samostatnej služby.

#### Konkrétny kompromis pre OneSport

Uprednostňujeme jednoduchšiu implementáciu a silnú konzistentnosť dát pred
maximálnou nezávislou škálovateľnosťou. Je to primerané, pretože požiadavky
obsahujú veľa prepojených operácií nad používateľmi, kolekciami a priateľstvami,
ale neuvádzajú extrémnu návštevnosť ani potrebu viacerých vývojových tímov.

Nevýhody sa budú obmedzovať jasnými hranicami modulov, používaním verejných
rozhraní namiesto priameho prístupu do cudzích častí a samostatným workerom na
import externých správ a vstupeniek. Ak neskôr vznikne potreba samostatného
škálovania, modulárne rozdelenie poskytne základ na postupné vyčlenenie modulu.


### Požiadavka používateľa

Používateľ požiadal o náročné časti implementácie.

### Náročné časti implementácie

1. **Bezpečná autentifikácia a správa relácií**

   Registrácia musí kontrolovať duplicitu e-mailu a heslá sa musia ukladať iba
   ako bezpečné hash hodnoty. Prihlásenie, odhlásenie a zmena hesla musia
   správne vytvárať alebo rušiť relácie. Po zmene hesla alebo vymazaní účtu
   nesmú zostať použiteľné staré relácie.

2. **Autorizácia a ochrana osobných dát**

   Nestačí overiť, že používateľ je prihlásený. Každý endpoint musí overiť,
   či používateľ vlastní konkrétnu kolekciu, žiadosť alebo nastavenie profilu.
   Inak by útočník mohol zmeniť ID v URL a pristupovať k dátam iného používateľa.

3. **Vymazanie účtu**

   Treba rozhodnúť, či sa vymažú alebo anonymizujú používateľove kolekcie,
   priateľstvá, žiadosti a profilové údaje. Operácia musí byť konzistentná,
   nesmie omylom odstrániť verejné správy alebo vstupenky a mala by byť
   auditovateľná.

4. **Stavy a súbežné operácie pri priateľstvách**

   Systém musí zabrániť žiadosti na seba samého, duplicitným žiadostiam a
   konfliktu, keď dvaja používatelia naraz prijmú alebo odmietnu rovnakú
   žiadosť. Prijatie žiadosti a vytvorenie priateľstva má prebehnúť v jednej
   databázovej transakcii.

5. **Konzistentnosť uložených správ a vstupeniek**

   Uloženie rovnakej položky dvakrát musí byť idempotentné alebo odmietnuté.
   Vstupenka môže byť neskôr vypredaná či odstránená externým poskytovateľom,
   preto treba zachovať referenciu a používateľovi zobraziť jej aktuálny stav.

6. **Import externých správ a lístkov**

   Externý zdroj môže byť pomalý, nedostupný alebo meniť formát dát. Import
   preto patrí do workera s retry mechanizmom, limitmi, logovaním a ochranou
   pred duplicitami. Chyba importu nesmie zablokovať prihlasovanie alebo
   zobrazovanie už uložených dát.

7. **Filtrovanie, stránkovanie a výkon**

   Správy a vstupenky sa musia filtrovať na serveri a databáza potrebuje vhodné
   indexy, napríklad na krajine a dátume. Bez stránkovania by systém pri väčšom
   počte položiek posielal príliš veľké odpovede a spomaľoval klienta.

8. **Testovanie okrajových prípadov**

   Okrem bežných testov treba testovať neplatné heslá, expirované relácie,
   opakované požiadavky, súbežné zmeny, prístup k cudzím ID, vymazanie účtu a
   nedostupné vstupenky. Práve tieto prípady najčastejšie odhalia chyby v
   autorizácii a konzistentnosti.

### Druhá implementácia: architektúra založená na mikroslužbách

#### Požiadavka používateľa

Používateľ požiadal o ďalšiu možnú implementáciu OneSport, aby ju bolo možné
porovnať s modulárnym monolitom.

#### Návrh

OneSport by bol rozdelený na viac samostatných mikroslužieb. Každá služba by
mala vlastnú zodpovednosť, vlastné API a ideálne aj vlastnú databázu.

```text
Webová alebo mobilná aplikácia
            |
       API Gateway
   +--------+---------+----------+---------+
   |                  |          |         |
Identity service  Content    Collection  Social
                  service    service     service
   |                  |          |         |
 Identity DB      Content DB  Collection DB Social DB
            \       |          |        /
                 Message broker
```

#### Rozdelenie služieb

- **Identity service**: registrácia, prihlasovanie, relácie, zmena údajov
  profilu a vymazanie účtu;
- **Content service**: športové správy, udalosti, vstupenky, filtrovanie podľa
  krajiny a import dát od externých poskytovateľov;
- **Collection service**: obľúbené správy a uložené vstupenky;
- **Social service**: vyhľadávanie používateľov, žiadosti o priateľstvo,
  prijatie alebo odmietnutie žiadosti a zoznam priateľov;
- **API Gateway**: jednotný vstupný bod, overenie tokenu, rate limiting,
  smerovanie požiadaviek a korelačné ID pre logy.

Služby by komunikovali synchronne cez HTTP alebo gRPC, ak používateľ očakáva
okamžitú odpoveď. Zmeny ako `UserDeleted`, `TicketUpdated` alebo
`FriendshipAccepted` by sa posielali asynchrónne cez message broker. Každá
služba by vlastnila svoje tabuľky a iné služby by do nich nemali pristupovať
priamo.

#### Dáta a komunikácia

Collection service by pri zobrazení uloženej vstupenky potrebovala informácie
z Content service. Môže ich načítať cez API, alebo si udržiavať vlastnú
read-model kópiu aktualizovanú udalosťami. Pri vymazaní účtu by Identity
service zverejnila udalosť `UserDeleted` a ostatné služby by asynchrónne
odstránili alebo anonymizovali svoje používateľské dáta.

#### Trade-offs

**Výhody:**

- jednotlivé služby sa dajú škálovať samostatne, napríklad Content service
  pri veľkom počte návštev správ;
- porucha externého importu nemusí priamo ovplyvniť Identity service;
- služby sa môžu nasadzovať nezávisle;
- hranice zodpovedností a vlastníctva dát sú veľmi jasné;
- neskôr sa dá pridať napríklad samostatná platobná alebo odporúčacia služba.

**Nevýhody:**

- systém je podstatne náročnejší na vývoj, deployment a prevádzku;
- jedna používateľská operácia môže vyžadovať komunikáciu viacerých služieb;
- medzi databázami nie je jednoduchá spoločná transakcia;
- dáta môžu byť dočasne nekonzistentné, pretože udalosti sa spracúvajú
  asynchrónne;
- potrebné sú centralizované logy, monitoring, tracing, retry mechanizmus a
  dead-letter queue;
- lokálne spustenie vyžaduje viac procesov, databáz a message broker;
- sieťové volania pridávajú latenciu a môžu zlyhať.

Pri OneSport by táto architektúra vymenila jednoduchosť a okamžitú
konzistentnosť modulárneho monolitu za nezávislé škálovanie a izoláciu služieb.
Pre malý tím a súčasný rozsah by mohla byť zbytočne komplikovaná, ale bola by
vhodná pri veľkej návštevnosti alebo viacerých tímoch.

#### Náročné časti implementácie

1. **Distribuované transakcie:** prijatie žiadosti o priateľstvo a vytvorenie
   priateľstva už nie sú jedna databázová transakcia. Treba použiť workflow,
   saga pattern alebo kompenzačnú operáciu.
2. **Doručovanie udalostí:** broker môže doručiť udalosť viackrát, neskoro alebo
   v inom poradí. Consumer musí byť idempotentný a musí vedieť opakovať
   neúspešné spracovanie.
3. **Vymazanie účtu:** `UserDeleted` musí byť spracované vo všetkých službách.
   Systém musí evidovať neúspešné spracovania a umožniť ich opakovanie.
4. **Konzistentnosť kolekcií:** Collection service môže krátkodobo zobrazovať
   zastaraný názov alebo dostupnosť vstupenky.
5. **Autorizácia:** každá služba musí okrem overenia tokenu kontrolovať aj
   oprávnenie používateľa nad konkrétnym zdrojom.
6. **Observability:** bez korelačných ID, distribuovaného tracingu a
   centralizovaných logov by sa ťažko hľadalo, kde zlyhala jedna požiadavka.

### Otázka používateľa: Čo je Saga pattern?

Používateľ sa opýtal, čo znamená Saga pattern, ktorý bol spomenutý pri
distribuovaných transakciách.

Saga pattern je spôsob koordinovania jednej väčšej operácie, ktorá pozostáva z
viacerých lokálnych transakcií v rôznych mikroslužbách. Namiesto jednej
globálnej databázovej transakcie každá služba vykoná vlastnú zmenu a pošle
udalosť ďalšej službe.

Napríklad pri prijatí žiadosti o priateľstvo:

1. Social service zmení stav žiadosti na `accepted`;
2. vytvorí alebo pošle požiadavku na vytvorenie priateľstva;
3. ďalšia operácia potvrdí vytvorenie záznamu priateľstva;
4. pri zlyhaní sa vykoná kompenzačná operácia, napríklad návrat žiadosti do
   pôvodného stavu alebo označenie operácie na opakovanie.

Saga teda neposkytuje klasický okamžitý rollback ako jedna SQL transakcia.
Namiesto toho udržiava systém konzistentný pomocou postupných krokov,
kompenzačných akcií, retry mechanizmu a evidencie zlyhaných operácií. Existujú
event choreography, kde služby reagujú na udalosti samostatne, a orchestration,
kde centrálny orchestrátor určuje poradie krokov.

Pri OneSport by Saga pattern bol potrebný iba pri mikroslužbách, pretože
modulárny monolit môže prijatie žiadosti a vytvorenie priateľstva vykonať v
jednej databázovej transakcii. Saga prináša flexibilitu a oddelenie služieb, ale
za cenu zložitejšieho návrhu, dočasnej nekonzistentnosti a náročnejšieho
debuggingu.

### Tretia implementácia: serverless a event-driven architektúra

#### Požiadavka používateľa

Používateľ požiadal ešte o tretiu alternatívu, ktorá by využívala cloudové
funkcie a udalosti namiesto stále bežiaceho backendového servera.

#### Návrh

Klient by komunikoval s API Gateway. Jednotlivé endpointy by spúšťali krátko
žijúce cloudové funkcie. Autentifikáciu, databázu, fronty a plánované úlohy by
poskytovali managed cloud services.

```text
Webová alebo mobilná aplikácia
            |
       API Gateway
            |
  +---------+----------+----------+---------+
  |                    |                    |
Auth functions   Content functions     Social functions
  |                    |                    |
Managed Identity   NoSQL database      NoSQL database
                         |
                 Event bus / queues
                         |
             Scheduled import functions
                         |
              Externé news/ticket API
```

#### Funkcie a služby

- managed identity service by riešila registráciu, login a tokeny;
- funkcie by obsluhovali profil, správy, vstupenky, kolekcie a priateľstvá;
- NoSQL databáza by ukladala používateľské kolekcie a sociálne záznamy;
- event bus a queue by spracovávali zmeny a opakovanie neúspešných úloh;
- scheduled function by pravidelne importovala správy a dostupnosť vstupeniek;
- managed search service by mohla podporovať filtrovanie a stránkovanie.

Pri uložení správy by funkcia vykonala autorizáciu a zapísala záznam do
kolekcie. Pri importe by plánovaná funkcia vložila úlohu do fronty a worker
funkcia by ju spracovala neskôr. Používateľská požiadavka by tak nečakala na
externý športový zdroj.

#### Otázka používateľa: Čo je NoSQL databáza?

Používateľ sa opýtal, čo znamená NoSQL databáza, aký typ databázy to je a
aký je rozdiel oproti SQL databáze.

NoSQL je širšia skupina databáz, ktoré sa nespoliehajú primárne na klasický
relačný model tabuliek a SQL dotazov. Často ukladajú dokumenty vo formáte
podobnom JSON, key-value záznamy, grafy alebo široké stĺpce. Schéma býva
flexibilnejšia a databáza sa často ľahšie horizontálne škáluje medzi viaceré
servery.

SQL databázy, napríklad PostgreSQL, ukladajú dáta do tabuliek s pevnejšie
definovanými vzťahmi, podporujú JOIN operácie, cudzie kľúče a silné
transakcie. Sú vhodné tam, kde je dôležitá konzistentnosť prepojených dát,
napríklad pri používateľoch, priateľstvách a uložených položkách.

NoSQL databáza je flexibilnejšia pri veľkom množstve jednoduchých a rýchlych
čítaní, ale vývojár musí dátový model často prispôsobiť konkrétnym spôsobom
vyhľadávania. Namiesto JOIN operácie môže byť potrebné ukladať rovnaké údaje
na viacerých miestach, teda ich denormalizovať. To môže zjednodušiť škálovanie,
ale zároveň vytvárať problém so synchronizáciou a dočasne zastaranými údajmi.

Pre serverless OneSport by NoSQL mohla byť vhodná na kolekcie a sociálne
záznamy, ak sú dotazy vopred dobre známe a aplikácia potrebuje cloudové
škálovanie. PostgreSQL z modulárneho monolitu by bol prirodzenejší pre
vzájomne prepojené operácie, ako je prijatie friend requestu a vytvorenie
priateľstva v jednej transakcii.

#### Trade-offs

**Výhody:**

- cloud automaticky škáluje funkcie podľa počtu požiadaviek;
- netreba spravovať stále bežiace aplikačné servery;
- nepravidelná návštevnosť počas športových udalostí sa dá dobre obslúžiť;
- fronty poskytujú retry a ochranu pred dočasnou nedostupnosťou externého API;
- plánované importy sa dajú spúšťať bez vlastného scheduler servera;
- jednotlivé funkcie sa dajú nasadzovať relatívne nezávisle.

**Nevýhody:**

- NoSQL modelovanie je náročnejšie pri priateľstvách a vzťahoch medzi dátami;
- údaje môžu byť po asynchrónnej udalosti určitý čas zastarané;
- cold starts, timeouty a limity funkcií môžu ovplyvniť odozvu;
- cloudové služby môžu vytvoriť vendor lock-in;
- cena môže byť nepredvídateľná pri veľkom počte invokácií a databázových čítaní;
- lokálne testovanie je ťažšie bez cloudových emulátorov;
- debugging vyžaduje sledovanie gateway, funkcií, front a databázových logov.

Pri OneSport by serverless riešenie zjednodušilo prevádzku a dobre by zvládlo
nepravidelné špičky, ale prinieslo by väčšiu závislosť od konkrétneho cloudu.
Relačné operácie medzi používateľmi, kolekciami a priateľstvami by boli
zložitejšie než pri PostgreSQL.

#### Náročné časti implementácie

1. **Návrh NoSQL dát:** dáta treba modelovať podľa konkrétnych query patternov.
   Priatelia a uložené položky môžu vyžadovať denormalizované kópie.
2. **Súbežné zmeny:** prijatie žiadosti musí používať conditional writes alebo
   transakcie podporované konkrétnou databázou.
3. **Eventual consistency:** používateľ môže krátko vidieť starý stav priateľstva
   alebo dostupnosti vstupenky, preto treba loading a retry stav v rozhraní.
4. **Idempotencia:** opakovaná invokácia funkcie nesmie vytvoriť duplicitnú
   kolekciu, priateľstvo ani importovanú správu.
5. **Limity a zdroje:** funkcie majú limity času, pamäte a veľkosti odpovede.
   Nesprávne vytváranie databázových spojení môže spôsobiť pomalosť a vyššie
   náklady.
6. **Monitoring a bezpečnosť:** treba správne nastaviť IAM oprávnenia, secrets,
   audit logy, alarmy a ochranu API pred zneužitím.

### Zhrnutie porovnania troch implementácií

- **Modulárny monolit** ponúka najjednoduchší vývoj a najlepšiu transakčnú
  konzistentnosť, ale škáluje celý backend naraz.
- **Mikroslužby** ponúkajú nezávislé škálovanie a izoláciu, ale vyžadujú
  distribuované transakcie, observability a náročnejšiu prevádzku.
- **Serverless/event-driven** znižuje správu infraštruktúry a dobre zvláda
  nepravidelné špičky, ale prináša eventual consistency, vendor lock-in a
  zložitejšie NoSQL modelovanie.

Pre aktuálne požiadavky by bol pravdepodobne najvhodnejší modulárny monolit.
Mikroslužby alebo serverless by sa oplatilo zvoliť až pri preukázanej potrebe
nezávislého škálovania, veľkom tíme alebo výraznej cloudovej orientácii.
