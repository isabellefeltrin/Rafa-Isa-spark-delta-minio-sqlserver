# DML no Delta Lake

Mesmas operações do trabalho 1, agora sobre a tabela `carro` do bucket `bronze` (notebook `02_dml_delta.ipynb`). A tabela é acessada direto pelo caminho: `` delta.`s3a://bronze/carro` ``.

## INSERT

```sql
INSERT INTO delta.`s3a://bronze/carro`
VALUES ('KLM2468', 'ONIX', '11223344556', 5, 2023, 'PRATA', 1);
```

Grava um novo arquivo Parquet e adiciona uma versão ao `_delta_log`.

## UPDATE

```sql
UPDATE delta.`s3a://bronze/carro` SET cor = 'VERMELHO' WHERE placa = 'EEE1056';
```

O Parquet é imutável: o Delta reescreve o arquivo que contém a linha e marca o antigo como removido no log.

## DELETE

```sql
DELETE FROM delta.`s3a://bronze/carro` WHERE placa = 'ALD3834';
```

## Histórico e _time travel_

```sql
DESCRIBE HISTORY delta.`s3a://bronze/carro`;
SELECT * FROM delta.`s3a://bronze/carro` VERSION AS OF 0;
```

| versão | operação                  |
| ------ | ------------------------- |
| 0      | `WRITE` (carga do bronze) |
| 1      | `WRITE` (INSERT)          |
| 2      | `UPDATE`                  |
| 3      | `DELETE`                  |

Os arquivos antigos continuam no MinIO até um `VACUUM`, o que permite voltar a qualquer versão.
