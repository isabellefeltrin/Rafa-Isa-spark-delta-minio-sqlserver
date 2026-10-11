from spark_delta_minio_sqlserver import config
from spark_delta_minio_sqlserver.spark_session import spark_configs


def test_jdbc_url_usa_valores_do_ambiente(monkeypatch):
    monkeypatch.setenv('SQLSERVER_HOST', 'db')
    monkeypatch.setenv('SQLSERVER_PORT', '1500')
    monkeypatch.setenv('SQLSERVER_DB', 'x')

    assert config.jdbc_url().startswith('jdbc:sqlserver://db:1500;')
    assert 'databaseName=x' in config.jdbc_url()


def test_s3_path():
    assert config.s3_path('bronze', 'carro') == 's3a://bronze/carro'
    assert config.s3_path('bronze') == 's3a://bronze'


def test_spark_configs_tem_delta_e_minio():
    configs = spark_configs()

    assert 'DeltaSparkSessionExtension' in configs['spark.sql.extensions']
    assert configs['spark.hadoop.fs.s3a.path.style.access'] == 'true'
