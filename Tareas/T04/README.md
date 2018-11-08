##Readme Tarea 04 Jacques Hasard

- Mi programa funciona principalmente desde la base de la estructura semanal que se aplica para el ramo. Esto consiste en que hay una lista inicial de eventos y todos se van ejecutando y agregando con un +7 en dias, a excepcion de las reuniones y entregas de tareas.

- En la clase simulación hice una función para cada día (en el cual pueden ocurrir distitnos eventos) para faciliarme el llamado de acciones por parte de los alumnos ayudantes y profesores.

- Las horas dedicadas a las tareas son un promedio de las horas que utilizaron durante las dos semanas ya que sino las notas eran todas cercanas al 7, asi son mas realistas 

- Por tiempo no alcance a implementar bien la lectura de escenarios, esta tiene algun problema cuando se terminan las evaluaciones por eso la meti dentro de un try para que no se caiga el programa, pero igual la dejo ahi porque en gran parte si funciona

- Los alumnos adquieren conocimientos para la semana los domingos, pero utilizan las respectivas partes para cada evaluacion (ej una actividad un jueves utilizan 4/7 de las horas de esa semana y 3/7 de la semana anterior)

- La simulación comienza un lunes

- El promedio se calcula como todas las notas divididas en la cantidad de estas, para facilitarlo.

- Para medir mes de mayor aprobacion se contabilizo el examen solo el tercer mes cambiando las ponderaciones a 40 y 60 para actividades y tareas respectivamente los primeros dos meses ya que sino siempre el 50% era un 1.0

- No implemente los eventos no programados
- Las confianzas si pueden pasar a ser negativas, y por lo general lo son D:
- Las funciones que no tenian return, no les puse nada en la documentación, osea no sale ni return.
- Cuando en consola aparece U.u es porque el Malvado Dr. Mavrakis bajo las notas, es mas que nada para que se sepa que se implemento y poder observarlo de alguna forma discreta
- Si los alumnos botaban el ramo no era posible ver sus estadisticas tras terminar el ramo ya que estas no formaban parte del ramo a esa altura