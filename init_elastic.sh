#!/bin/bash

echo "Esperando a que Elasticsearch esté disponible en el puerto 9200..."
until curl -s http://localhost:9200/_cat/health?pretty | grep -q "green\|yellow"; do
  sleep 2
done

echo "Creando el índice 'articulos'..."
curl -X PUT "http://localhost:9200/articulos" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  }
}'

echo -e "\nInsertando artículos de prueba..."
curl -X POST "http://localhost:9200/articulos/_doc/1" -H 'Content-Type: application/json' -d'
{
  "nombre": "Teclado Mecánico RGB",
  "descripcion": "Teclado mecánico con switches rojos para gaming",
  "precio": 79.99
}'

curl -X POST "http://localhost:9200/articulos/_doc/2" -H 'Content-Type: application/json' -d'
{
  "nombre": "Ratón Inalámbrico Ergonómico",
  "descripcion": "Ratón vertical de alta precisión",
  "precio": 45.50
}'

echo -e "\n¡Elasticsearch inicializado con éxito!"
