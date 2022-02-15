## Idea Chatbota Newsie 
Zpravodajské články jen těžko obstojí v konkurenci zábavných obsahů sociálních sítí, her a interaktivních formátů. Zaujměte své čtenáře Chatbotem Newsie, který bude představovat zprávy postupně, bude se uživatele ptát a motivovat ho, aby se ke zprávám vracel.

## Inovace zpravodajského storytellingu 
Projekt vznikl ve spoluprácí Nadačního fondu nezávislé žurnalistiky a Česko.Digital. Cílem bylo navrhnout prototyp, který by dostal zpravodajství k lidem, kteří zprávy nečtou ([dle výzkumu](https://www.nfnz.cz/studie-a-analyzy/cesi-a-zpravodajstvi/) se jedná o více než 30 % populace). Zapojili jsme 150 expertních dobrovolníků a novináře z 10 redakcí. Ověřovali jsme si hypotézy, ptali se novinářů i mediálních domů. Idea chatbota zvítězila v konkurenci téměř stovky nápadů.

## Koncept v kostce
Chatbot funguje na platformě [Messenger](https://cs.wikipedia.org/wiki/Facebook_Messenger) a přináší informace o dění kolem lidem, kteří o ně sice mají zájem, ale zpravodajské servery pro ně nejsou vhodnou formou, nebo nemají čas, chuť či disciplínu zprávy sledovat. Chatbot funguje pro konkrétní redakci, která dodává obsah prostřednictvím RSS. Redakce získávají nové, především mladé čtenáře. Po přečtení zpráv si uživatel může udělat kvíz a získat body. Čtenář je motivován každý den číst alespoň 3 zprávy. 

<img width="1434" alt="obrazek" src="https://user-images.githubusercontent.com/69157075/150365703-8d299281-f401-4767-91a8-3adfbe927177.png">


# Jak to funguje
Koncept projektu, jeho přidanou hodnotu uživateli, cíl a benefity najdete v prezentaci [Chatbot Newsie](https://docs.google.com/presentation/d/1hS9tdPj9EITdcgzo-2qJ_53amQ4pWriF9H6l-a5WkCk/). 

## Licence
Projekt je open source, kdokoliv má právo kdykoliv využít dokumentaci pro své účely. Na projekt platí MIT licence. Více o MIT licenci naleznete na [popisu na GitHub](https://github.com/nfnz/newschatbot/blob/master/LICENSE).

## Návod pro spuštění v nové redakci
Redakce bude potřebovat provést 3 hlavní kroky:
  1) Vytvořit si profil v online platformě [Chatfuel](Chatfuel.com), která zprostředkovává chování chatbota v Messengeru.
  2) Druhým krokem bude spusti backend chatbota v jazyce Python.
  3) Následně je třeba propojit Chatfuel, backend a RSS redakce.

## Chatfuel
Online nástroj Chatfuel nabízí několik verzí, my používali verzi 15$ / měsíc. Zde si definujte workflow a bloky, které volají prostřednictvím API backend. V tomto nástroji nastavíte, jak bude chatbot na uživatele reagovat, jak mu bude zprávy zobrazovat a jaké otázky mu bude klást.
1. Nastavte si chatbota v Chatfuel podle následujícího [zadání](https://docs.google.com/document/d/18zOGlWSjJWydNlYczLIvLEuoPa8K857VnnpsQ0-8Bxo/edit?usp=sharing)
3. Upravte v jednotlivých blocích URL na API podle toho, kde je nasazený backend.

## Newschatbot backend

Python Flask REST API poskytující data pro Chatfuels Chatbot. Nasazení probíhá pomocí [Serverless Frameworku](https://www.serverless.com/) na prostředí [AWS Lambda](https://aws.amazon.com/lambda/). Aplikace je připojena k Postgres databázi.

### Infrastruktura
Infrastruktura pro databázi je spravována pomocí [Terraformu](https://www.terraform.io/) (IaaC - Infrastructure-as-a-code). Nasazení probíhá automaticky pomocí [Github Actions](https://github.com/nfnz/newschatbot/actions). (Na Githubu je potřeba nastavit [proměnné](https://docs.github.com/en/actions/security-guides/encrypted-secrets) AWS_ACCESS_KEY_ID a AWS_SECRET_ACCESS_KEY.)
  
Základy Terraformu, Github Action and detailní popis celého workflow nasazování infrastruktury naleznete v [DevTalku](https://cesko.digital/cedu/devtalk-1-infrastruktura).

AWS PostgreSQL databáze není přístupná přímo, protože přístup do produkční databáze (připojení se přes `psql`) není běžně třeba. V případě řešení jakýchkoli neočekávaných problémů (například chybná migrace), doporučuji obnovit databázi ze zálohy (přes konzoli AWS) nebo si vytvořit dočasnou VPN a připojit se do interní sítě přes ní. Jako návod pro rychlé nastavení VPN na AWS doporučuju [článek od Vladimíra Smitky na Zdrojáku](https://zdrojak.cz/clanky/l2tp-vpn-v-aws-snadno-a-rychle/)
  
### Nasazení

Nasazení probíhá pomocí [Serverless Frameworku](https://www.serverless.com/) na prostředí [AWS Lambda](https://aws.amazon.com/lambda/). Definice funkcí je v souboru `serverless.yml`.

### Lokální vývoj
**Spouštění pomocí Docker Compose:**

```
docker-compose up
```
Spustí Flask aplikaci, PostgreSQL server a databázové migrace.

Ověřit, že spuštění proběhlo v pořádku, můžete příkazem:
```
curl http://127.0.0.1:5000/v1/articles/
```

Ten byl měl vrátit JSON se seznamem výchozích článků.

### Vývoj
**Nastavení Pythonu**

Projekt využívá Python verze 3.6

Vytvoření virtuálního prostředí a instalace závislostí: Při instalaci můžete narazit na problém s balíčkem `greenlet`. (Na Mac zařízení změňte v `requirements.txt` greenlet==0.4.10 na greenlet==0.4.16) 
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

**Nastavení databáze**

Spuštění PostgreSQL pomocí Docker Compose: (Případně si můžete PostgreSQL stáhnout a nainstalovat z https://www.postgresql.org/download/)
```
cd dockers/postgres/
docker-compose up
```
**Databázové migrace** 

Nastavte v terminálu proměnnou prostředí FLASK_APP (na Linux prostředí místo _set_ použijte _export_)
```
set FLASK_APP=app/main:app;
```
Nastavte v terminálu proměnnou prostředíDB_CONNSTR (na Linux prostředí místo _set_ použijte _export_)
```
set DB_CONNSTR="postgresql://postgres:postgres@localhost:5432/feed_parser"
```
Spuštění migrací
```
flask db upgrade
```
**Spuštění aplikace**
```
flask run
```
Flask aplikace se spouští ze souboru app/main.py

### Databázové migrace

Vytvoření nové migrace založené na změnách v aplikačním modelu (app/model.py).
```
flask db migrate
```
Spuštění migrací.
```
flask db update
```

### Přispívání
#### Před odesláním změn
Než odešlete vaše změny, zformátujte kód pomocí nástroje [Black](https://github.com/psf/black), následujícím příkazem:
```
black {source_file_or_directory} 
```
Pokud skript nefunguje, spusťe Black přímo jako balíček: 
```
python3 -m black {source_file_or_directory}
```
