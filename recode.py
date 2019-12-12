#!/usr/bin/python3

import os
import sys
import subprocess
from argparse import ArgumentParser

# Clase
class Recode:

    # Constructor
    def __init__(self, args):
        # Inicializar
        self.total = 0
        self.omitidos = 0
        self.posicion = 0
        self.videos = []
        self.success = []
        self.current_folder = os.getcwd()
        # parse arguments
        self.arguments()
        self.header()

    # Mostrar mensaje en pantalla
    def mensaje(self, tipo, *args):
        tipo = '[%s]' % tipo
        print('')
        if len(args) == 1 and (isinstance(args[0], list) or isinstance(args[0], tuple)):
            for item in args[0]:
                print(tipo, item)
        else:
            print(tipo, *args)
        print('')

    # Mostrar encabezado en pantalla
    def header(self):
        msgs = ['', 'Recode :: Recodificar videos', '', '          (ffmpeg)', '']
        self.mensaje(' ', msgs)

    # Definir los argumentos por linea de comandos
    def arguments(self):
        parser = ArgumentParser()
        parser.add_argument('carpeta', default=".", help="Carpeta donde escanear videos")
        parser.add_argument('-m', '--move', action="store_true", help="Mover los antiguos videos a una carpeta de historización")
        parser.add_argument('-b', '--backup', default='backup', help="Nombre de la carpeta Backup")
        parser.add_argument('-s', '--search', default='avi', help="Formato de video a buscar (defecto: AVI)")
        parser.add_argument('-f', '--format', default='mkv', help="Formato a convertir el video (defecto: MKV)")
        self.args = parser.parse_args()
        self.get_folder()

    # Obtener la carpeta de busqueda
    def get_folder(self):
        folder = self.args.carpeta
        if not folder.startswith('/'):  # Ruta relativa
            if self.args.carpeta == '.':
                folder = self.current_folder
            else:
                if self.args.carpeta.startswith('.'):
                    parts = self.args.carpeta.split('/')
                    parts.remove('.')
                    folder = os.path.join(self.current_folder, *parts)
                else:
                    folder = os.path.join(self.current_folder, self.args.carpeta)
        self.args.carpeta = folder
        return folder

    # Recuperar el listado de ficheros
    def get_files(self):
        msgs = [
            'Buscar vídeos con formato: ' + self.args.search,
            'En la carpeta: ' + self.args.carpeta
        ]
        self.mensaje('+', msgs)

        for r, d, f in os.walk('.'):
            if r == '.':  # Deshabilitar modo recursivo
                for file in f:
                    if file.endswith('.avi'):
                        self.videos.append( file )
                        print(' > ', file)

        self.total = len(self.videos)
        self.mensaje('+', 'Total videos encontrados: ', self.total)

    # Create folder backup
    def create_folder_backup(self):
        self.backup_folder = os.path.join(self.args.carpeta, self.args.backup)
        if not os.path.isdir(self.backup_folder):
            self.mensaje('+', ['Create backup folder:', self.backup_folder])
            os.mkdir( self.backup_folder )

    # Transformar
    def convert(self, video):
        self.mensaje('+', 'Codificar vídeo:', video)
        parts = video.split('.')
        parts.pop()
        parts.append(self.args.format)
        new_video = '.'.join(parts)

        # Verificar si el video en mkv ya existe en el directorio
        if os.path.isfile(new_video):
            self.omitidos += 1
            self.mensaje('!', 'El vídeo ya existe, omitir')
        else:
            # Convertir video
            self.success.append( new_video )
            p = subprocess.Popen(('ffmpeg', '-i', video, new_video))
            p.wait()

            # check ffmpeg return code
            if p.returncode != 0:
                self.mensaje('!', 'Error en ffmpeg')
                sys.exit(1)
            # Mover el video a la carpeta de backup
            elif self.args.move:
                old_path = os.path.join(self.args.carpeta, video)
                new_path = os.path.join(self.backup_folder, video)
                self.mensaje('+', ['Mover vídeo a la carpeta backup', new_path])

                if not os.path.isfile(new_path):
                    os.rename(old_path, new_path)
                else:
                    self.mensaje('!', ['Error en backup el fichero ya existe', new_path, 'Se omite'])

    # Ejecutar
    def run(self):
        # Cambiar de carpeta
        os.chdir(self.args.carpeta)
        self.get_files()

        if self.total == 0:
            self.mensaje('!', 'Sin videos que codificar')
            os.chdir(self.current_folder)
            sys.exit(1)
        else:
            # Crear carpeta backup
            if self.args.move:
                self.create_folder_backup()
            for movie in self.videos:
                self.posicion += 1
                self.mensaje('-', 'Video %d de %d' % (self.posicion, self.total))
                self.convert( movie )
            self.resumen()

        # Volver a la carpeta inicial
        os.chdir(self.current_folder)

    # Mostrar un resumen al finalizar
    def resumen(self):
        # Mostrar resumen
        msgs = [
            'Total videos:      %d' % self.total,
            'Total omitidos:    %d' % self.omitidos,
            'Total convertidos: %d' % len(self.success)
        ]
        self.mensaje('+', msgs)

        print('[-] Listado de videos convertidos:')
        for v in self.success:
            print(' >> ', v)

        self.mensaje('+', 'Finalizado')


if __name__ == '__main__':
    code = Recode(sys.argv)
    code.run()
