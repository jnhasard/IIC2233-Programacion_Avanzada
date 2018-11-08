# Tarea 6 Programación Avanzada
## Jacques Hasard
Bienvenidos a PrograPop

Mi programa consta de principalmente 5 modulos:

- server
- equalizador
- sala
- client
- interfaz

Carperta server
-
Los primeros 3 de esta lista se encuentran en la carpeta "server". El modulo server es el que como dice el nombre hace de servidor en el juego, esta constantemente recibiendo actualizaciones de los distintos clientes y reenviandolas al resto, también esta constantemente escuchando a los objetos de clase salas del modulo sala los cuales se tienen guardadas todas sus respectivas canciones y van actualizando los tiempos y cancion actual. 

El equializador no esta implementado en el juego ya que no logre hacerlo del todo bien, funciona bien la parte del sample rate y cambia el como suena la canción, sin embargo cuando hacía el siguiente paso resultaba un sonido muy desagradable. Además se demoraba mucho en iterar en toda la canción lo que hubiese perjudicado el funcionamiento del juego. Sin embargo, decidi adjuntarlo como un modulo independiente donde pueden probar como funciona para ojala rescatar algun puntaje :D. (La prueba esta con uno de los reggaetones que era el que menos pesaba para que demorara poco)

En esta carpeta deben incluir la carpeta "songs" con las salas y canciones tal como sale el enunciado para que todo funcione en orden. (Sin esta el servidor no podrá comenzar)

Para iniciar el server solo deben ejecutar server.py y se creara también un "usuarios.json" que es la base de datos de los jugadores que se vayan inscribiendo.

Carpeta client
-
Aquí encontraran 2 modulos un .ui y una imagen. Los dos modulos son client e interfaz, como los nombres los dicen client será el que se conecte con el servidor e ira actualizando y almacenando todo tipo de datos del jugador y por otro lado interfaz será la encargada de ir mostrando todo esto en la interfaz gráfica con la que interactuará el usuario.

El "interfaz.ui" es el archivo creado con el designer que me ayudo a diseñar la interfaz y la imagen es el fondo que escogí para esta.

Si bien la interfaz no debería tener que hacer mucho pensamiento supuestamente, en este caso me simplificó darle un par de tareas extra para no tener que hacer conexiones innecesarias con el backend el cual en este caso sería el cliente.

De esta carpeta basta con correr el modulo "interfaz.py" para que se abra la interfaz y poder jugar.

No implementado
-
- Ningún bonus
- Equalizador a medias

El resto está todo incluido y (debería estar) funcional.

Disfruten!