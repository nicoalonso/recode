# Resumen

Es un simple script en python3 para escanear un directorio en busca de vídeos en formato `".avi"` y los convierte con la utilidad `ffmpeg` a `".mkv"`.



## Dependencias

- ffmpeg
- python3

Para instalar `ffmpeg` en distribuciones derivadas de debian:

```bash
sudo apt install ffmpeg
```



## Instalación

Copia el script a la siguiente ruta

```bash
copy recode.py /usr/local/bin/recode
```

Darle permisos de ejecución

```bash
chmod +x /usr/local/bin/recode
```

## Ejecución

Simplemente muevete a la carpeta donde se localizan los videos y ejecuta

```bash
recode
```

Y a disfrutar.