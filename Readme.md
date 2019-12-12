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

Ejecuta el comando de la siguiente forma:

```bash
recode carpeta
```

Donde `carpeta` es la ruta donde se localizan los vídeos a convertir.

Ejemplo:

```bash
recode .
```

Para buscar en la carpeta actual.

#### Modificadores:

* `-m, --move`: Mueve los vídeos antiguos a una carpeta de copia de seguridad o recuperación. Por defecto los vídeos nuevos y antiguos se almacenan en la misma carpeta.
* `-b BACKUP, --backup BACKUP`:  Indica el nombre de la carpeta de recuperación, por defecto "`backup`".
* `-s avi, --search avi`: formato de vídeo a buscar, por defecto: "`avi`"
* `-f mkv, --format mkv`: formato a convertir, por defecto: "`mkv`"