# Changelog 

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-Board class with initialize_checkers() method to place checkers in their initial positions.
-show_board() method with Backgammon-style column display, including top and bottom areas.
-Player class with name, color, points, and checkers_out attributes.
-Methods in Player: add_points(), remove_checker(), has_won(), and __str__().
-Dice class where double dice are detected to give double plays
-Move_checker() method in Board with move validations by color and occupation.
-Logging moves with the log_move(player, source, destination, capture=False) function.
-Basic turn system with printing of the active player.
-Unit tests for:
    -Board initialization (total_pieces_test, white_positions_test, black_positions_test)
    -Piece movement (valid_piece_move_test, color errors, empty origin, occupied destination)
    -Player class (player_creation_test, add_points_test, remove_piece_test, has_won_test)
    -Dice tests
    -Checker tests(Valid moves)
### Fixed 

- Syntax error due to unclosed parentheses in coreBoard.py.
-Incorrect reference to self.points instead of self._points_ within Board.
-Misaligned board display in console (now in columns with arrows and separators).

### Changed 
-

## [0.1.0] - [19/9/2025]

### Added
- Se ha implementado el nucleo (`core`) del juego de Backgammon.
- Funcionalidad para tirar los dados.
- Logica inicial para el movimiento de las fichas.
- Creacion de la funcion `move_piece` para gestionar los movimientos.
- Creacion de tests para `core`:
  - Test de inicializacion del tablero (`test_initialize_board`).
  - Test de creacion de jugadores (`test_player_creation`).
  - Test de movimiento de fichas (`test_move_piece`).

### Changed
- Mejora en la documentacion interna del codigo del `core`.

---

## [0.2.0] - [1/10/2025]

### Added
- Se ha anadido una interfaz de linea de comandos (`cli`) para interactuar con el juego.
- Sistema de turnos para dos jugadores.
- Creacion de tests para `cli`:
  - Test para la entrada de comandos (`test_cli_input`).
  - Test para el sistema de turnos (`test_turn_system`).

### Fixed
- Corregido un error que impedia que los dados dobles se contaran correctamente.
- Solucionado un problema que causaba que las fichas se superpusieran en el tablero.
- Arreglado un bug que no permitia que las fichas eliminadas volvieran a entrar al juego.
- El juego ya no se bloquea al intentar un movimiento invalido.
- Solucionados problemas de rendimiento en la logica del juego.
- Mejorada la validacion de movimientos para evitar trampas.

### Removed
- Se ha eliminado la funcion `move_piece`, ya que su logica ha sido refactorizada y reemplazada por un sistema mas eficiente.
- Se ha eliminado la funcion `calculate_score` por ser obsoleta.

---

## [0.3.0] - [25/10/2025]

### Added
- ¡Se ha anadido una interfaz grafica (`pygame_ui`)! Ahora se puede jugar en una ventana con elementos visuales.
- Representacion grafica del tablero, las fichas y los dados.
- Interaccion con el raton para mover las fichas.

### Changed
- El juego ahora se inicia por defecto con la interfaz de `pygame`.
