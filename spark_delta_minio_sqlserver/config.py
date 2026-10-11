import os

LANDING = 'landing-zone'
BRONZE = 'bronze'


def _env(nome: str, padrao: str) -> str:
    return os.environ.get(nome, padrao)


def jdbc_url() -> str:
    host = _env('SQLSERVER_HOST', 'localhost')
    porta = _env('SQLSERVER_PORT', '1433')
    banco = _env('SQLSERVER_DB', 'seguradora')
    return (
        f'jdbc:sqlserver://{host}:{porta};databaseName={banco};'
        'encrypt=true;trustServerCertificate=true'
    )


def jdbc_properties() -> dict[str, str]:
    return {
        'user': _env('SQLSERVER_USER', 'sa'),
        'password': _env('SQLSERVER_PASSWORD', 'SqlServer@2025!'),
        'driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
    }


def minio_endpoint() -> str:
    return _env('MINIO_ENDPOINT', 'http://localhost:9000')


def minio_credentials() -> tuple[str, str]:
    return (
        _env('MINIO_ROOT_USER', 'minioadmin'),
        _env('MINIO_ROOT_PASSWORD', 'minioadmin'),
    )


def s3_path(bucket: str, tabela: str = '') -> str:
    return f's3a://{bucket}/{tabela}'.rstrip('/')
