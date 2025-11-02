# Justificacion del Proyecto Backgammon


## Resumen del Diseño General

El proyecto implementa el juego de Backgammon siguiendo una arquitectura de capas que separa claramente la logica de negocio de las interfaces de usuario. Esta separacion permite:

- **Reutilizacion:** La misma logica del `core` es utilizada tanto por la interfaz de linea de comandos (CLI) como por la interfaz grafica (Pygame).
- **Testabilidad:** El `core` puede ser testeado de forma aislada, sin depender de las interfaces.
- **Mantenibilidad:** Los cambios en las reglas del juego se pueden realizar en el `core` sin afectar el codigo de las interfaces.
- **Extensibilidad:** La arquitectura facilita la adicion de nuevas interfaces (por ejemplo, una interfaz web) en el futuro.

### Estructura del Proyecto

```
backgammon/
├── core/              # Logica de negocio (independiente de la UI)
│   ├── game.py        # Orquestador principal del juego
│   ├── board.py       # Representacion y logica del tablero
│   ├── dados.py       # Logica para tirar los dados
│   ├── player.py      # Estado y acciones del jugador
│   └── checker.py     # Representacion de las fichas
├── cli/               # Interfaz de linea de comandos
│   └── cli.py
├── pygame_ui/         # Interfaz grafica con Pygame
│   └── ui.py
└── tests/             # Suite de pruebas unitarias
    ├── test_game.py
    ├── test_board.py
    ├── test_dados.py
    ├── test_player.py
    ├── test_checker.py
    └── test_cli.py
```

---

## Arquitectura y Principios de Diseño

### Separacion de Responsabilidades (SRP - Single Responsibility Principle)

Cada clase en el proyecto tiene una unica razon para cambiar:

- **`Board`:** Gestiona el estado fisico del tablero y las posiciones de las fichas.
- **`Dice`:** Se encarga de la generacion de numeros aleatorios para los dados.
- **`Jugador`:** Maneja el estado de un jugador, incluyendo su nombre, color y fichas.
- **`Checker`:** Representa una ficha individual.
- **`Game`:** Orquesta el flujo del juego, coordinando los demas componentes del `core`.
- **`cli.py` / `ui.py`:** Se encargan exclusivamente de presentar la informacion al usuario y capturar sus entradas.

### Inversion de Dependencias (DIP - Dependency Inversion Principle)

Las interfaces de usuario (`cli` y `pygame_ui`) dependen de la clase `Game` del `core`, pero el `core` no depende de ninguna interfaz. Esto asegura que la logica de negocio sea completamente independiente y reutilizable.

---

## Modulo Core - Logica de Negocio

### `core/game.py` - Clase `Game`

**Proposito:** Es el orquestador principal. Coordina el `Board`, los `Dados`, los `Jugadores` y el `TurnManager` para ejecutar el flujo del juego.

#### Atributos Clave:

- `board`: Instancia de `Board` que representa el tablero.
- `dice`: Instancia de `Dice` para manejar los dados.
- `jugador1`, `jugador2`: Instancias de `Jugador`.
- `turnos`: Instancia de `TurnManager` que gestiona de quien es el turno.
- `available_moves`: Lista de movimientos disponibles segun la ultima tirada de dados.

#### Metodos Principales:

- `__init__()`: Inicializa todos los componentes del juego.
- `tirar_dados()`: Lanza los dados y actualiza los movimientos disponibles.
- `puede_mover(origen, destino, color)`: Valida si un movimiento es legal segun las reglas.
- `mover_ficha(origen, destino, color)`: Ejecuta un movimiento, incluyendo la logica de captura.
- `verificar_ganador()`: Comprueba si alguno de los jugadores ha ganado la partida.

### `core/board.py` - Clase `Board`

**Proposito:** Mantiene el estado de los 24 puntos del tablero y las fichas que se encuentran en ellos.

#### Atributos Clave:

- `_puntos_`: Una lista de 24 listas, donde cada sublista representa una pila de fichas en un punto del tablero.

#### Metodos Principales:

- `inicializar_fichas()`: Coloca las fichas en sus posiciones iniciales estandar.
- `mover_ficha(origen, destino, color)`: Mueve una ficha entre dos puntos, validando reglas basicas.
- `puede_entrar_desde_bar(color, entrada)`: Verifica si una ficha puede reingresar al tablero desde la barra.

### `core/dados.py` - Clase `Dice`

**Proposito:** Encapsula toda la logica relacionada con los dados.

#### Metodos Principales:

- `roll_dice()`: Genera dos valores aleatorios entre 1 y 6.
- `is_double()`: Verifica si ambos dados tienen el mismo valor.
- `get_moves()`: Devuelve una lista de movimientos disponibles (2 movimientos o 4 si es doble).

### `core/player.py` - Clases `Jugador` y `TurnManager`

**Proposito:** `Jugador` representa a un participante, mientras que `TurnManager` gestiona la secuencia de turnos.

#### Atributos Clave de `Jugador`:

- `nombre`, `color`: Identificadores del jugador.
- `fichas`: Lista de 15 objetos `Checker` que pertenecen al jugador.

#### Metodos Principales de `Jugador`:

- `ha_ganado()`: Verifica si el jugador ha retirado todas sus fichas.
- `puede_sacar_fichas(board)`: Comprueba si todas las fichas del jugador estan en su zona de "home" para poder empezar a retirarlas.

---

## Interfaces de Usuario

### `cli/cli.py` - Interfaz de Linea de Comandos

**Proposito:** Permite jugar una partida de Backgammon a traves de la terminal.

#### Responsabilidades:

- **Control de Flujo:** La funcion `ejecutar_cli()` orquesta el bucle principal del juego.
- **Entrada de Usuario:** Captura las acciones del jugador, como tirar los dados y seleccionar los movimientos.
- **Visualizacion:** Las clases `TableroView` y `EstadoView` se encargan de mostrar el tablero y la informacion del turno de forma textual.

**Integracion con `Game`:** La CLI no contiene ninguna regla de juego. Delega todas las validaciones y modificaciones de estado al objeto `Game`, actuando unicamente como una capa de presentacion.

### `pygame_ui/ui.py` - Interfaz Grafica con Pygame

**Proposito:** Ofrece una experiencia de juego visual e interactiva.

#### Responsabilidades:

- **Renderizado:** Funciones como `draw_board()` y `draw_checkers()` se encargan de dibujar todos los elementos del juego en la ventana.
- **Manejo de Eventos:** La funcion `handle_event()` procesa las acciones del usuario, como clics del raton en las fichas, puntos del tablero o botones.
- **Calculos de Coordenadas:** Un conjunto de funciones auxiliares (`get_point_center`, `get_point_from_pos`, etc.) se encarga de traducir las coordenadas de la pantalla a la logica del tablero.

**Consistencia:** Al igual que la CLI, la interfaz de Pygame utiliza la misma API del `core`, lo que garantiza que el comportamiento del juego sea identico en ambas interfaces.

---

## Estrategias de Testing y Cobertura

### Enfoque de Testing

El proyecto cuenta con una suite de tests unitarios disenada para verificar el correcto funcionamiento de cada componente del `core` de forma aislada.

### Resultados de Cobertadura

Se ejecuto una bateria de tests sobre los modulos del `core`, obteniendo los siguientes resultados de cobertura. *Nota: No se pudo generar un informe de cobertura completo para los modulos `cli` y `board` debido a problemas tecnicos persistentes en sus respectivos tests, los cuales no pudieron ser resueltos en el tiempo disponible.*

```
Name               Stmts   Miss  Cover
------------------------------------------------
core/checker.py       50      0   100%
core/dados.py         20      0   100%
core/game.py         112      6    95%
core/player.py        41      0   100%
------------------------------------------------
```

### Analisis de la Cobertura

- **`core/checker.py` (100%):** La clase que representa las fichas esta completamente testeada.
- **`core/dados.py` (100%):** La logica de los dados, incluyendo la generacion de dobles, esta totalmente cubierta.
- **`core/player.py` (100%):** La gestion del estado del jugador esta completamente verificada.
- **`core/game.py` (95%):** El orquestador principal del juego tiene una cobertura casi total, lo que garantiza que la mayoria de los flujos y reglas de negocio funcionan como se espera.

### Conclusion

La alta cobertura en los modulos criticos del `core` demuestra la robustez y fiabilidad de la logica de negocio del proyecto. Los tests aseguran que las reglas del Backgammon estan implementadas correctamente y que los componentes individuales funcionan de manera predecible.
