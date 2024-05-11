# SALTACACAS
Saltacacas es nuestro primero juego hecho en familia.

La idea es crear un juego relacionado con nuestra rutina mañanera de ir al cole.
y es que cada día en el camino encontramos obstáculos que nos impiden hacer la ruta normal, como cacas de perrito, y otras lindezas.

Así que este juego trata de que un personaje principal sale de casa y tiene que llegar al cole sin pisar las cacas que encuentra por el camino. Además para conseguir puntos tiene que ir comiendo frutas sanas, algunas como el tomate da 5 puntos y las otras 1 punto.

![imagen del juego](assets/fondo.png)

Autores: Fernando Villalba y familia


## Notas de programacion
Para compartir el juego hay que instalar la librería *pyinstaller*: 

> pip install pyinstaller 

Después, una vez hemos terminado el juego y desde el directorio del proyecto hacemos esto:

 > pyinstaller --windowed --onefile saltakks.py

 Siendo *saltakks.py* el fichero principal del juego, que contiene el código.

 Parece que habitualmente el windows defender da un aviso de troyano al generar esto.