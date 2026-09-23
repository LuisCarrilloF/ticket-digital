# ticket-digital
El negocio va creciendo, se  me ocurrio un generador de tickets para poder enviar al cliente sobre el precio final.



# Entorno de desarrollo
## Entorno virtual
comando para poder crear el entorno virtual:
```
py -3.13 -m venv venv
```
Activas el entorno con:
`ctrl`+`shft`+`p`
seleccionas el entorno recomendado y descargas las dependencias del archivo `requirements.txt`
 
esto con 
```
pip instal requirements.txt
```

para correr el programa de forma local se usa el siguiente comando:
```
flet run
```

Para poder creear el apk para tu celular ejecuta:
```
.\venv\Scripts\flet.exe build apk
```