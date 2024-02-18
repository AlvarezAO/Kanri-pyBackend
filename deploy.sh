#!/bin/bash
HORA=$(date '+%Y-%m-%d %H:%M:%S')
ALIAS_NAME=$1

if [ -z "$ALIAS_NAME" ]; then
  echo "Ambiente no especificado."
  exit 1
fi

echo "Iniciando despliegue a Lambda con alias: $ALIAS_NAME a las: $HORA"


echo "Instalando dependencias de Python..."
pip install -r requirements.txt -t ./dependencies/
echo "Empaquetando dependencias para el layer..."
zip -r kanri_layer.zip ./dependencies/
echo "Cargando layer en S3..."
aws s3 cp kanri_layer.zip s3://kanri-project-files/layer_zip/kanri_layer.zip
echo "Layer termino de cargar en S3..."
echo "Eliminando carpeta dependencies del local a las: $(date '+%Y-%m-%d %H:%M:%S')"
rm -rf ./dependencies/
rm kanri_layer.zip

#export AWS_PROFILE=alvaro
# Aquí podrías agregar comandos para empaquetar tu código, si es necesario

# Ejecutar el comando de AWS CodeBuild, pasando el alias como una variable de entorno
#aws codebuild list-projects

aws codebuild start-build --project-name kanri_fastapi_build --environment-variables-override name=ALIAS_NAME,value=$ALIAS_NAME,type=PLAINTEXT
#aws codebuild start-build --project-name kanri_fastapi_build --environment-variables-override name=ALIAS_NAME,value=$ALIAS_NAME,type=PLAINTEXT