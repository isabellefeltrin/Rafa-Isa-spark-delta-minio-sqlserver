from pyspark.sql import SparkSession

from spark_delta_minio_sqlserver import config

EXTRA_PACKAGES = [
    'org.apache.hadoop:hadoop-aws:3.3.4',
    'com.amazonaws:aws-java-sdk-bundle:1.12.262',
    'com.microsoft.sqlserver:mssql-jdbc:12.8.1.jre11',
]


def spark_configs() -> dict[str, str]:
    usuario, senha = config.minio_credentials()
    return {
        'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
        'spark.sql.catalog.spark_catalog': (
            'org.apache.spark.sql.delta.catalog.DeltaCatalog'
        ),
        'spark.hadoop.fs.s3a.endpoint': config.minio_endpoint(),
        'spark.hadoop.fs.s3a.access.key': usuario,
        'spark.hadoop.fs.s3a.secret.key': senha,
        'spark.hadoop.fs.s3a.path.style.access': 'true',
        'spark.hadoop.fs.s3a.connection.ssl.enabled': 'false',
        'spark.hadoop.fs.s3a.impl': 'org.apache.hadoop.fs.s3a.S3AFileSystem',
    }


def create_session(app_name: str = 'sqlserver-minio-delta') -> SparkSession:
    from delta import configure_spark_with_delta_pip

    builder = SparkSession.builder.appName(app_name).master('local[*]')
    for chave, valor in spark_configs().items():
        builder = builder.config(chave, valor)
    return configure_spark_with_delta_pip(
        builder, extra_packages=EXTRA_PACKAGES
    ).getOrCreate()
