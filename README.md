
# Product Pipeline

Detta projekt automatiserar hämtning, bearbetning och lagring av produktdata från ett öppet API (Tradedoubler). 
Flödet schemaläggs så att det körs automatiskt dagligen via Windows Schemaläggaren.

## Projektstruktur

Pipeline består av följande steg:

1. **Hämtning av produktdata från API**
2. **Bearbetning av data (säkerställer korrekt prisformat)**
3. **Lagring av data i SQLite-databasen `products.db` i tabellen `products`**
4. **Loggning av status och eventuella fel i `product_pipeline_log.txt`**

## Användning

1. Kontrollera att du har Python installerat.
2. Installera beroenden:

```bash
pip install requests pandas
```

3. Kör programmet manuellt:

```bash
python product_pipeline.py
```

4. För att köra automatiskt varje natt:
   - Öppna **Windows Schemaläggaren**
   - Skapa en ny uppgift som kör `python path\to\product_pipeline.py` kl 01:00 varje dag.

## Loggning

Alla fel och statusmeddelanden loggas i `product_pipeline_log.txt`. Denna fil uppdateras varje gång skriptet körs.

## Författare

- Magdalena Wallner
