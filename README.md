# SQL Server → MinIO → Delta Lake com Apache Spark

## Descrição

Pipeline com **PySpark** que extrai todas as tabelas de um banco **SQL Server** (`seguradora`), grava-as em CSV no bucket **`landing-zone`** do **MinIO**, converte para **Delta Lake** no bucket **`bronze`** e reproduz `INSERT`, `UPDATE` e `DELETE` nas tabelas Delta.

Trabalho 2 de Engenharia de Dados (UNISATC), Prof. Jorge Luiz da Silva. Complementa o [trabalho 1](https://github.com/raffaelarcego/trabalho-apachespark-eng_dados) (Delta Lake e Apache Iceberg).

**Integrantes:** Raffael Michels Arcego · Isabelle Luiz Feltrin

📖 **Documentação completa:** https://isabellefeltrin.github.io/Rafa-Isa-spark-delta-minio-sqlserver/

```mermaid
flowchart LR
    A[(SQL Server<br/>seguradora)] -->|JDBC + CSV| B[(MinIO<br/>landing-zone)]
    B -->|Delta Lake| C[(MinIO<br/>bronze)]
    C --> D[INSERT / UPDATE / DELETE]
```

## Disclaimer

- O Spark 3.5 exige **Java 17**. Versões 21 ou superiores não funcionam.
- Na primeira execução, o Spark baixa os JARs (Delta, hadoop-aws, driver JDBC do SQL Server) pela internet.
- O SQL Server em contêiner precisa de **pelo menos 2 GB de RAM** livres para o Docker.
- Os comandos são executados no **terminal do Ubuntu (WSL)**, e não no PowerShell.

## Pré-requisitos

- Windows 11 com **WSL 2 (Ubuntu)**
- **Java 17**
- **Docker** com Compose v2
- **[uv](https://docs.astral.sh/uv/)** (gerenciador de pacotes; ele também instala o Python 3.11)

| Componente         | Versão                         |
| ------------------ | ------------------------------ |
| pyspark            | 3.5.x                          |
| delta-spark        | 3.3.2                          |
| hadoop-aws         | 3.3.4                          |
| mssql-jdbc         | 12.8.1                         |
| SQL Server         | 2022 (contêiner)               |
| MinIO              | RELEASE.2025-02-03 (contêiner) |
| jupyterlab, mkdocs | 4.x, 1.6 + material            |

## Instalação

```bash
# 1. Java 17
sudo apt update && sudo apt install -y openjdk-17-jdk-headless

# 2. uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# 3. Projeto
cd ~
git clone https://github.com/isabellefeltrin/Rafa-Isa-spark-delta-minio-sqlserver.git
cd Rafa-Isa-spark-delta-minio-sqlserver
uv sync
cp .env.example .env
```

## Howto

```bash
docker compose up -d
uv run jupyter lab
```

Rode os notebooks em ordem, cada um com **Run All**:

| Notebook                                | O que faz                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------- |
| `00_sqlserver_para_landing.ipynb`       | Extrai todas as tabelas do SQL Server para CSV no bucket `landing-zone`   |
| `01_landing_para_bronze.ipynb`          | Lê os CSVs e grava em Delta Lake no bucket `bronze`                       |
| `02_dml_delta.ipynb`                    | `INSERT`, `UPDATE`, `DELETE`, histórico e _time travel_ na tabela `carro` |
| `03_gerenciada_vs_nao_gerenciada.ipynb` | Compara tabelas gerenciadas e não gerenciadas                             |

Console do MinIO: http://127.0.0.1:9001 (`minioadmin` / `minioadmin`). No Windows com WSL, `localhost` pode não responder.

Para encerrar: `docker compose down` (acrescente `-v` para apagar os dados).

## Testes

```bash
uv run task test    # pytest com cobertura
uv run task lint    # ruff, blue e isort
uv run task format  # corrige a formatação
```

## Documentação

```bash
uv run mkdocs serve       # visualizar localmente em http://127.0.0.1:8000
uv run mkdocs gh-deploy   # publicar no GitHub Pages
```

## Estrutura

```
├── spark_delta_minio_sqlserver/   # pacote Python (sessão Spark, extração e conversão)
├── notebooks/                     # 00 a 03, em ordem de execução
├── sql/01_seguradora.sql          # cria e popula o banco (4 tabelas)
├── docker-compose.yml             # SQL Server e MinIO
├── tests/                         # testes com pytest
├── docs/                          # páginas do MkDocs
├── mkdocs.yml
└── pyproject.toml                 # dependências e tarefas (uv + taskipy)
```

## Problemas comuns

<details>
<summary><b>Sem internet no Ubuntu (WSL)</b>: <code>apt</code> ou <code>uv sync</code> falham com <i>Network is unreachable</i></summary>

Crie o arquivo `C:\Users\<seu-usuario>\.wslconfig` no Windows com:

```ini
[wsl2]
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
```

Depois, no PowerShell, rode `wsl --shutdown`, abra o Ubuntu de novo e teste com `curl -I https://pypi.org`.

</details>

<details>
<summary><b><code>JAVA_GATEWAY_EXITED</code></b> ou <b><code>JAVA_HOME is not set</code></b></summary>

```bash
java -version                              # deve mostrar 17
sudo update-alternatives --config java     # se houver mais de uma versão, escolha a 17
```

</details>

<details>
<summary><b>Notebook 00 falha ao conectar no SQL Server</b></summary>

O contêiner `sqlserver-init` cria o banco depois que o SQL Server fica saudável. Confira com `docker compose ps -a` e `docker compose logs sqlserver-init`. Se a porta 1433 ou 9000 já estiver em uso, pare o outro serviço.

</details>

## Erros encontrados durante o desenvolvimento

| Erro                                                                                                     | Causa                                                                                                                         | Como contornamos                                                                                                                                     |
| -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `git clone` e link da documentação davam 404                                                             | O repositório foi renomeado para `Rafa-Isa-spark-delta-minio-sqlserver`, mas o README e o `mkdocs.yml` usavam o nome antigo | Atualizamos os links para o nome atual                                                                                                               |
| Site do MkDocs dava 404 no GitHub Pages                                                                  | A documentação ainda não tinha sido publicada                                                                                 | `mkdocs gh-deploy` (cria a branch `gh-pages`) e, em **Settings → Pages**, escolhemos a branch `gh-pages` como fonte                                  |
| `cd: No such file or directory` e `no configuration file provided` no Ubuntu                             | O projeto estava clonado só no Windows, não dentro do WSL                                                                     | Clonamos o repositório dentro do Ubuntu (`cd ~ && git clone ...`) antes de rodar `docker compose` e `uv`                                             |
| Primeira execução do notebook 00 parecia travada em `downloading ... aws-java-sdk-bundle-1.12.262.jar` | O Spark baixa os JARs na primeira vez, e esse tem quase 300 MB                                                                | Esperar o download terminar. Os JARs ficam em cache em `~/.ivy2`, e as próximas execuções sobem rápido                                               |
| Uma tabela nova no SQL Server iria para a `landing-zone`, mas não para o `bronze`                       | O notebook 01 tinha a lista de tabelas fixa no código                                                                         | Criamos `pipeline.listar_landing()`, que lista as pastas do bucket `landing-zone`, e o notebook 01 passou a usá-la                                   |
| `apolice.valor` virou `DOUBLE` e `cpf`/`chassi` viraram `BIGINT` no `bronze`                            | CSV não guarda tipos; o `inferSchema` deduz o tipo pelo conteúdo                                                              | Documentado em [Pipeline](https://isabellefeltrin.github.io/Rafa-Isa-spark-delta-minio-sqlserver/pipeline/). A solução completa é declarar o schema |
| `pull access denied for minio/minio` no `docker compose up`, e o console em `localhost:9001` não abria   | O MinIO deixou de publicar a imagem oficial no Docker Hub e no quay.io                                                        | Trocamos para `pgsty/minio`, um fork comunitário que mantém o console web e aceita os mesmos comandos                                               |
| WSL caiu com `Falha catastrófica` (`Wsl/Service/E_UNEXPECTED`) e depois dava `Input/output error`        | O disco C: encheu durante o `docker compose up`; o disco virtual do Ubuntu (`ext4.vhdx`) fica no C: e não tinha como crescer | Liberamos espaço no C:, rodamos `wsl --shutdown` e limpamos imagens antigas do Docker (`docker image prune -a`)                                      |
| Console do MinIO em `http://localhost:9001` ficava carregando até dar timeout no navegador do Windows   | O Windows resolve `localhost` primeiro como IPv6 (`::1`), e o encaminhamento de portas do WSL só respondia em IPv4             | Acessar por `http://127.0.0.1:9001`                                                                                                                  |
| `bad object HEAD` e `empty compose file` depois do travamento                                            | O WSL caiu no meio de um `git pull`, e os arquivos que estavam sendo gravados ficaram vazios                                  | Renomeamos o clone quebrado, clonamos de novo e trouxemos de volta só o que não estava no git (notebook alterado, `.venv`, `.env`)                    |
| `INSERT` duplicado ao rodar o notebook 02 duas vezes                                                     | Cada execução grava uma nova versão na mesma tabela Delta                                                                     | Rodar o notebook 01 de novo antes do 02 (ele sobrescreve a tabela do `bronze`)                                                                       |

## Referências

- [jlsilva01/spark-delta-minio-sqlserver](https://github.com/jlsilva01/spark-delta-minio-sqlserver) (repositório modelo do professor)
- [Delta Lake](https://docs.delta.io/) · [Apache Spark](https://spark.apache.org/docs/3.5.3/) · [MinIO](https://min.io/docs/minio/container/index.html) · [Hadoop S3A](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html)

## Uso de IA

O Claude (Anthropic) foi usado como apoio para estruturar o projeto, revisar código e documentação. O grupo executou, conferiu e revisou tudo.
