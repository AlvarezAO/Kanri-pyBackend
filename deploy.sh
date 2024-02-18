#!/bin/bash

ALIAS_NAME=$1

if [ -z "$ALIAS_NAME" ]; then
  echo "Ambiente no especificado."
  exit 1
fi

echo "Iniciando despliegue a Lambda con alias: $ALIAS_NAME"
#export AWS_PROFILE=alvaro
# Aquí podrías agregar comandos para empaquetar tu código, si es necesario

# Ejecutar el comando de AWS CodeBuild, pasando el alias como una variable de entorno
#aws codebuild list-projects

aws codebuild start-build --project-name kanri_fastapi_build --environment-variables-override name=ALIAS_NAME,value=$ALIAS_NAME,type=PLAINTEXT
#aws codebuild start-build --project-name kanri_fastapi_build --environment-variables-override name=ALIAS_NAME,value=$ALIAS_NAME,type=PLAINTEXT