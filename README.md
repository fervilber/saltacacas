# SALTACACAS
Saltacacas es un proyecto familiar y nuestro primer juego de ordenador hecho en python.

La idea se nos ocurió en el camino habitual al cole, ya que nos pasamos el paseo de casa al colegio saltando cacas de perrito, que sus queridos dueños no quieren recoger de las aceras.

Este juego trata, como su nombre indica, de llegar al cole sano y salvo, sin pisar ninguna caca de perro.
Hay 3 personajes a elegir, en la pantalla de inicio. El personaje puede avanzar, retroceder y saltar, incluso puede subirse a algunos monopatines que aparecen por las calles.

Los puntos se consiguen recogiendo fruta que vale 1 punto, o un bocata que vale 3. Hay que llegar con energía al cole y es necesria para saltar las cacas.

![Portada y seleccion de personajes](assets/imagen_portada.png)

![imagen del juego](assets/imagen_juego1.png)

Autores:
 * Fernando Villalba
 * Sofía Villalba
 * Eva Villalba

# Versión descargable para PC

En la carpeta *dist*, se encuentra la versión descargable para PC. Hay que descargar el ejecutable y la carpeta de imagenes tal cual.

## Notas de programacion

Para compartir el juego hay que instalar la librería *pyinstaller*: 

> pip install pyinstaller 

Después, una vez hemos terminado el juego y desde el directorio del proyecto hacemos esto:

 > pyinstaller --windowed --onefile saltakks.py

 Siendo *saltakks.py* el fichero principal del juego, que contiene el código.

 Parece que habitualmente el windows defender da un aviso de troyano al generar esto.