## Desafío teórico

### Procesos

Utilizaría procesos para realizar tareas paralelas potencialmente largas, extensas o significativas. Un par de ejemplos sería aprovechar el multicore de un procesador para paralelizar por rows el cálculo de una multiplicación de matrices extensas, o por otro lado dado un programa que orqueste compilación/construcción y deploy de otros programas utilizaría multiprocesos para realizar dichas tareas. Esto porque de estos tres los procesos son los que consumen más recursos del sistema operativo, son más caros de crear/matar y además proveen buenos mecanismos de comunicación y jerarquización para organizar la ejecución de sus tareas.

### Threads

El caso de uso en este desafío técnico es un excelente ejemplo para aprovechar las ventajas de los threads. Realizar múltiples operaciones I/O, como por ejemplo requests a servicios externos, es un problema fácil de resolver con threads ya que puedes reducir el tiempo de consultar múltiples servicios a lo que tarda uno solo en responder. Los threads son ligeros y rápidos de crear/destruir por lo que se puede tener una generosa cantidad de esto cohabitando en un mismo proceso sin problemas. Otro caso de uso sería implementar un sistema de actores parecido al de Akka, donde todo actor iniciado viva en su propio thread independientemente de la ejecución de los demás y puedan realizar tareas asincrónicamente con sus propios recursos del sistema operativo.

### Corrutinas

Las corrutinas son capaces de resolver muchos casos que normalmente necesitarías threads como el caso de uso anterior. Sin embargo, como estas se pueden reducir a fragmentos de código que se bloquean para ceder la ejecución a otro un buen caso de uso en Python es el uso de generadores, donde puedo tener funciones que simultáneamente están realizando cálculos. Más específico, imaginemos un programa que recibe inputs secuenciales de enteros y para cada uno calcula su número de fibonacci y lo envía a otro servicio. Esto se podría resolver con dos corrutinas, una que reciba el número, haga el cálculo y ceda el control a la otra corrutina quien envía dicho resultado al otro servicio y mientras espera respuesta cede el control a la otra corrutina que repite el proceso.

### 1.000.000 de HTTP requests

Para este problema crearía un pool de procesos para dividir equitativamente la carga entre ellos. Cada proceso recibiría su parte del millón de inputs y crearía un pool de threads para comenzar el trabajo de ejecutar los requests y obtener los resultados.

Además, analizaría los inputs para averiguar si existe una cantidad significante de solicitudes repetidas que valga la pena cachear para ahorrar llamadas al sistema operativo.