# Pipeline

## 1. SQL Server → `landing-zone` (CSV)

O Spark descobre as tabelas em `INFORMATION_SCHEMA.TABLES`, lê cada uma por JDBC e grava `s3a://landing-zone/<tabela>/` com cabeçalho.

```python
def extrair_para_landing(spark):
    for tabela in listar_tabelas(spark):
        df = ler_tabela(spark, tabela)
        df.coalesce(1).write.mode("overwrite").option("header", True) \
            .csv(f"s3a://landing-zone/{tabela}")
```

Como todas as tabelas são listadas, uma tabela nova no banco entra na extração sem mudar o código. Notebook: `00_sqlserver_para_landing.ipynb`.

## 2. `landing-zone` → `bronze` (Delta Lake)

```python
df = spark.read.option("header", True).option("inferSchema", True) \
    .csv(f"s3a://landing-zone/{tabela}")
df.write.format("delta").mode("overwrite").save(f"s3a://bronze/{tabela}")
```

CSV não guarda tipos, então o `inferSchema` recupera `INT`, `DOUBLE` e `DATE`. Efeito colateral: `apolice.valor` (`DECIMAL` na origem) vira `DOUBLE` no bronze. Para manter a precisão, o schema deveria ser declarado explicitamente. Notebook: `01_landing_para_bronze.ipynb`.

Estrutura de cada tabela no bucket `bronze`:

```
bronze/carro/
├── part-00000-....snappy.parquet
└── _delta_log/
    └── 00000000000000000000.json
```

## Acesso ao MinIO

O Spark acessa o MinIO pelo protocolo S3 (`s3a://`), com endpoint e _path style_ configurados em `spark_session.py`:

```python
"spark.hadoop.fs.s3a.endpoint": "http://localhost:9000",
"spark.hadoop.fs.s3a.path.style.access": "true",
```
