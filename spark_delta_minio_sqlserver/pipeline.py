from pyspark.sql import DataFrame, SparkSession

from spark_delta_minio_sqlserver import config


def listar_tabelas(spark: SparkSession) -> list[str]:
    consulta = (
        '(SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES '
        "WHERE TABLE_TYPE = 'BASE TABLE') t"
    )
    df = spark.read.jdbc(
        config.jdbc_url(), consulta, properties=config.jdbc_properties()
    )
    return sorted(linha.TABLE_NAME for linha in df.collect())


def ler_tabela(spark: SparkSession, tabela: str) -> DataFrame:
    return spark.read.jdbc(
        config.jdbc_url(), tabela, properties=config.jdbc_properties()
    )


def extrair_para_landing(spark: SparkSession) -> dict[str, int]:
    contagem = {}
    for tabela in listar_tabelas(spark):
        df = ler_tabela(spark, tabela)
        (
            df.coalesce(1)
            .write.mode('overwrite')
            .option('header', True)
            .csv(config.s3_path(config.LANDING, tabela))
        )
        contagem[tabela] = df.count()
    return contagem


def landing_para_bronze(
    spark: SparkSession, tabelas: list[str]
) -> dict[str, int]:
    contagem = {}
    for tabela in tabelas:
        df = (
            spark.read.option('header', True)
            .option('inferSchema', True)
            .csv(config.s3_path(config.LANDING, tabela))
        )
        (
            df.write.format('delta')
            .mode('overwrite')
            .save(config.s3_path(config.BRONZE, tabela))
        )
        contagem[tabela] = df.count()
    return contagem


def _cliente_s3():
    import boto3

    usuario, senha = config.minio_credentials()
    return boto3.client(
        's3',
        endpoint_url=config.minio_endpoint(),
        aws_access_key_id=usuario,
        aws_secret_access_key=senha,
    )


def criar_buckets() -> None:
    s3 = _cliente_s3()
    existentes = {b['Name'] for b in s3.list_buckets()['Buckets']}
    for bucket in (config.LANDING, config.BRONZE):
        if bucket not in existentes:
            s3.create_bucket(Bucket=bucket)


def listar_landing() -> list[str]:
    resposta = _cliente_s3().list_objects_v2(
        Bucket=config.LANDING, Delimiter='/'
    )
    return sorted(
        pasta['Prefix'].rstrip('/')
        for pasta in resposta.get('CommonPrefixes', [])
    )
