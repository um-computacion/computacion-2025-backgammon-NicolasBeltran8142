# Proyecto Backgammon

-**Autor:** Nicolás Marcos Beltran Lazo 
-**Interfaz:** Consola y Gráfica (Pygame)
-**Carrera:** Ingenieria Informatica
Este proyecto es una implementacion completa del juego de mesa Backgammon, desarrollado en Python. Ofrece dos modos de juego para una experiencia versatil:

- **Interfaz de Linea de Comandos (CLI):** Para una experiencia de juego clasica y rapida.
- **Interfaz Grafica (Pygame):** Para una experiencia visual e interactiva.

---

## Estructura del Proyecto

El codigo esta organizado en modulos con responsabilidades bien definidas, separando la logica del juego de su presentacion.

```
backgammon/
├── core/
│   ├── game.py
│   ├── board.py
│   ├── dados.py
│   ├── player.py
│   └── checker.py
├── cli/
│   └── cli.py
├── pygame_ui/
│   └── ui.py
├── tests/
│   ├── test_game.py
│   ├── test_board.py
│   ├── test_dados.py
│   ├── test_player.py
│   ├── test_checker.py
│   └── test_cli.py
├── Justificacion.md
├── Changelog.md
└── requirements.txt
```

---

## Instalacion

Para ejecutar el proyecto, necesitaras Python 3.10 o una version superior.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu_usuario/backgammon.git
    cd backgammon
    ```

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate     # En Windows
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Como Jugar

Puedes iniciar el juego en cualquiera de los dos modos disponibles.

### Interfaz de Linea de Comandos (CLI)

Ejecuta el siguiente comando desde la raiz del proyecto para iniciar el juego en tu terminal:

```bash
python -m cli.cli
```

### Interfaz Grafica (Pygame)

Para una experiencia mas visual, ejecuta este comando para lanzar la interfaz grafica:

```bash
python -m pygame_ui.ui
```

---

## Testing

El proyecto incluye una suite de tests unitarios para asegurar el correcto funcionamiento de la logica del juego.

Para ejecutar todos los tests, utiliza el siguiente comando:

```bash
python -m unittest discover -s tests
```

---

## Documentacion

- **[Justificacion.md](./Justificacion.md):** Contiene un analisis detallado de la arquitectura, las decisiones de diseno y la aplicacion de principios SOLID en el proyecto.

- **[Changelog.md](./Changelog.md):** Documenta el historial de cambios y la evolucion del proyecto a lo largo del tiempo.

---


