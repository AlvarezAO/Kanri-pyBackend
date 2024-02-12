import boto3
from botocore.exceptions import ClientError
from sqlalchemy import create_engine
import json


#TODO Usar AWS SECRET mas adelante, por ahora en desarrollo no es necesario
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


'''SECRET = get_secret()
HOST_RDS = "kanri-database.cxmiiiegiwuu.us-east-1.rds.amazonaws.com"
USER_RDS = SECRET['username']
PASS_RDS = SECRET['password']
DB_NAME_RDS = "kanri_desarrollo"'''

HOST_RDS = "kanri-database.cxmiiiegiwuu.us-east-1.rds.amazonaws.com"
USER_RDS = "kanri_admin"
PASS_RDS = "k4nr1_2024"
DB_NAME_RDS = "kanri_desarrollo"

DATABASE_URL = f"mysql+pymysql://{USER_RDS}:{PASS_RDS}@{HOST_RDS}/{DB_NAME_RDS}?charset=utf8mb4"


# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

