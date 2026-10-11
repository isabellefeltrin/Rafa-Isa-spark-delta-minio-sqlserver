# Tabelas gerenciadas × não gerenciadas

Comparação entre os dois laboratórios (notebook `03_gerenciada_vs_nao_gerenciada.ipynb`).

|                            | Trabalho 1 (`carros`)      | Trabalho 2, `carro_externa`  | Trabalho 2, `carro_gerenciada` |
| -------------------------- | -------------------------- | ---------------------------- | ------------------------------ |
| Armazenamento              | disco local (`warehouse/`) | MinIO (`s3a://bronze/carro`) | `spark-warehouse/` (local)     |
| Criação                    | com `LOCATION`             | com `LOCATION`               | sem `LOCATION`                 |
| Tipo (`DESCRIBE EXTENDED`) | `EXTERNAL`                 | `EXTERNAL`                   | `MANAGED`                      |
| `DROP TABLE`               | remove só o metadado       | remove só o metadado         | remove metadado **e** dados    |

No trabalho 2 também há o acesso direto por caminho (`` delta.`s3a://bronze/carro` ``), que nem chega a registrar a tabela no catálogo.

## Pontos para discussão

- **Quem é dono dos dados?** Na externa, o dono é quem escreveu no caminho (o pipeline de ingestão); o Spark só enxerga. Na gerenciada, o Spark é dono: `DROP TABLE` apaga tudo.
- **Camadas do data lake** (`landing-zone`, `bronze`) devem ser **não gerenciadas**: o dado é um ativo do lake, e dropar uma tabela do catálogo não deve destruí-lo.
- **Gerenciadas** servem a tabelas intermediárias, fáceis de recriar.
- **O catálogo local é descartável**: com o metastore padrão (Derby em memória), as tabelas registradas somem ao encerrar a sessão. Os dados do `bronze` não, porque estão no MinIO. É o argumento mais forte para usar caminho/`LOCATION` em dados que precisam durar.
- No trabalho 1 tudo ficava em disco local, então a diferença era menos visível. Com object storage separado do Spark, fica claro que o armazenamento é independente do motor.
