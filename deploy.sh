#!/bin/bash
HORA=$(date '+%Y-%m-%d %H:%M:%S')
ALIAS_NAME=$1
RUTA_DEPENDENCIAS_REMOTAS="/mnt/c/Users/alvar/AppData/Local/JetBrains/PyCharm2023.2/remote_sources/-1312678265/1428128763"
RAIZ_PROYECTO="/home/alvaro/proyectos/Kanri-pyBackend"

if [ -z "$ALIAS_NAME" ]; then
  echo "Ambiente no especificado."
  exit 1
fi

echo "Iniciando despliegue a Lambda con alias: $ALIAS_NAME a las: $HORA"

CURRENT_HASH=$(aws s3 cp s3://kanri-project-files/hash_layer/current-hash.txt - 2>/dev/null) || echo "Archivo de hash no encontrado."
echo "Hash Actual: $CURRENT_HASH"
#Revisa todas las dependencias del proyecto y genera un hash basadas en ellas.
NEW_HASH=$(find $RUTA_DEPENDENCIAS_REMOTAS -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}')
echo "Nuevo Hash: $NEW_HASH"

if [ -z "$CURRENT_HASH" ] || [ "$CURRENT_HASH" != "$NEW_HASH" ]; then
  echo "El layer de dependencias ha cambiado o es la primera vez que se sube."
  echo $NEW_HASH | aws s3 cp - s3://kanri-project-files/hash_layer/current-hash.txt #Sube el nuevo hash a S3
  echo "Empaquetando dependencias para el layer..."
  zip -r $RAIZ_PROYECTO/kanri_layer.zip $RUTA_DEPENDENCIAS_REMOTAS
  echo "Subiendo el nuevo layer a S3..."
  aws s3 cp $RAIZ_PROYECTO/kanri_layer.zip s3://kanri-project-files/layer_zip/kanri_layer.zip
  echo "Layer cargado correctamente a S3 | Eliminando zip del local"
  rm kanri_layer.zip
  LAYER_UPDATE="true"
  else
  echo "El layer de dependencias no ha cambiado."
  LAYER_UPDATE="false"
  fi

aws codebuild start-build --project-name kanri_fastapi_build --environment-variables-override name=ALIAS_NAME,value=$ALIAS_NAME,type=PLAINTEXT name=LAYER_UPDATE,value=$LAYER_UPDATE,type=PLAINTEXT