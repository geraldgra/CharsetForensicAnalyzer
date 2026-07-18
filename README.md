# Charset Forensic Analyzer v1.0

## Analizar un archivo

```bash
python analyzer.py archivo.txt
```
Realiza el análisis completo y muestra el diagnóstico en consola.

-----------------------------------------------------------------

## Mostrar los primeros bytes en hexadecimal
```bash
python analyzer.py archivo.txt --hex
```
Además del análisis, muestra los primeros 32 bytes del archivo en hexadecimal.

-----------------------------------------------------------------

## Comparar la visualización con distintos encodings
```bash
python analyzer.py archivo.txt --preview
```
Muestra las primeras líneas del archivo interpretadas como:
Windows-1252
ISO-8859-1
UTF-8
UTF-8 (replace)

-----------------------------------------------------------------

## Generar un reporte JSON
```bash
python analyzer.py archivo.txt --json
```

Genera un archivo:
archivo.json
con toda la información del análisis.

-----------------------------------------------------------------

## muestra la respuesta en la CLI en formato JSON
```bash
python analyzer.py archivo.txt --output json
```

Genera un archivo:
archivo.json
con toda la información del análisis.

-----------------------------------------------------------------

## Convertir automáticamente a UTF-8
Modo seguro.
```bash
python analyzer.py archivo.txt --convert utf8
```
Si encuentra bytes incompatibles la conversión se cancela.

-----------------------------------------------------------------

## Convertir reemplazando caracteres inválidos
```bash
python analyzer.py archivo.txt --convert utf8 --errors replace
```
Los caracteres incompatibles serán reemplazados por �.

-----------------------------------------------------------------

## Convertir ignorando caracteres inválidos
```bash
python analyzer.py archivo.txt --convert utf8 --errors ignore
```
Los caracteres incompatibles serán eliminados.

-----------------------------------------------------------------

## Combinar opciones

Es posible combinar los parámetros.

### Ejemplo:

```bash
python analyzer.py archivo.txt --hex --preview
python analyzer.py archivo.txt --json --preview
python analyzer.py archivo.txt --json --convert utf8
python analyzer.py archivo.txt --hex --json --preview --convert utf8 --errors replace --output json
```

## Resumen de parámetros
Parámetro	        Descripción
--hex	            Muestra los primeros 32 bytes del archivo en hexadecimal.
--preview	        Compara visualmente el archivo usando distintos encodings.
--json	            Genera un reporte JSON del análisis.
--convert utf8	    Convierte el archivo a UTF-8.
--errors strict	    Cancela la conversión si hay bytes incompatibles (valor por defecto).
--errors replace	Sustituye caracteres incompatibles por �.
--errors ignore	    Elimina los caracteres incompatibles durante la conversión.