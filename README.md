# tetris_pygame

Este proyecto esta hecho en Python con la libreria PyGame, es un juego bastante conocido y verdaderamente sencillo. es la base para crear un proyecto mucho más grande.

## Ejecutar con Docker

El juego necesita acceso a un servidor grafico X11. En Linux o WSL con X11/WSLg:

```bash
cd tetris_pygame
xhost +local:
docker compose up --build
```

Para detenerlo, pulsa `Ctrl+C`. Si se ejecuto `xhost +local:`, se puede restaurar el control de acceso con:

```bash
xhost -local:
```

Tambien se puede ejecutar directamente con Docker:

```bash
docker build -t tetris-pygame .
docker run --rm -it \
  -e DISPLAY="${DISPLAY:-:0}" \
  -e SDL_VIDEODRIVER=x11 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  tetris-pygame
```
