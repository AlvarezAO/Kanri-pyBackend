import boto3
from botocore.exceptions import ClientError
from sqlalchemy import create_engine
import json


def get_secret():
    secret_name = "rds!db-09ba5175-7829-4458-896b-d4b2926463aa"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    return secret


SECRET = get_secret()
HOST_RDS = "kanri-database.clrflhflhrpj.us-east-1.rds.amazonaws.com"
USER_RDS = SECRET['username']
PASS_RDS = SECRET['password']
DB_NAME_RDS = "kanri_desarrollo"

DATABASE_URL = f"mysql+pymysql://{USER_RDS}:{PASS_RDS}@{HOST_RDS}/{DB_NAME_RDS}?charset=utf8mb4"


# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)


if __name__ == "__main__":
    print(get_secret())