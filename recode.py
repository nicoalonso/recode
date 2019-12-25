#!/usr/bin/python3

import os
import sys
import subprocess
from argparse import ArgumentParser

from msgterm import MsgTerm


class Recode:
    '''Recode
    
    Recode movies

    Attributes:
        total {number}: number of converted movies
        omitidos {number}: number of skip movies
        posicion {number}: number of current movie
        videos {list}: list of movies to convert
        success {list}: list of successfully converted movies
        current_folder {string}: current folder
    '''

    def __init__(self):
        # Inicializar
        self.total = 0
        self.omitidos = 0
        self.posicion = 0
        self.videos = []
        self.success = []
        self.current_folder = os.getcwd()
        # actions
        self.arguments()
        self.header()


    def header(self):
        '''Show header'''
        msgs = ['', 'Recode :: Recodificar videos', '', '          (ffmpeg)', '']
        MsgTerm.success(msgs, par=True, label='#', bold=True)


    def arguments(self):
        '''Parse input arguments'''
        parser = ArgumentParser()
        parser.add_argument('carpeta', default=".", help="Carpeta donde escanear videos")
        parser.add_argument('-m', '--move', action="store_true", help="Mover los antiguos videos a una carpeta de historización")
        parser.add_argument('-b', '--backup', default='backup', help="Nombre de la carpeta Backup")
        parser.add_argument('-s', '--search', default='avi', help="Formato de video a buscar (defecto: AVI)")
        parser.add_argument('-f', '--format', default='mkv', help="Formato a convertir el video (defecto: MKV)")
        self.args = parser.parse_args()
        self.get_folder()


    def get_folder(self):
        '''Get search folder'''
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


    def get_files(self):
        '''Search and store movies'''
        msgs = [
            'Buscar vídeos con formato: ' + self.args.search,
            'En la carpeta: ' + self.args.carpeta
        ]
        MsgTerm.info(msgs, par=True)
        extension = '.%s' % self.args.search

        for r, d, f in os.walk('.'):
            if r == '.':  # Deshabilitar modo recursivo
                for file in f:
                    if file.endswith(extension):
                        self.videos.append( file )
                        MsgTerm.message(file, label='>', type=MsgTerm.HELP)

        self.total = len(self.videos)
        MsgTerm.info('Total videos encontrados: %d' % self.total, hr=True)


    def create_folder_backup(self):
        '''Create folder backup'''
        self.backup_folder = os.path.join(self.args.carpeta, self.args.backup)
        if not os.path.isdir(self.backup_folder):
            MsgTerm.info('Crear carpeta de respaldo: %s' % self.backup_folder, nl=True)
            os.mkdir( self.backup_folder )


    def convert(self, video):
        '''Convert movie
        
        Arguments:
            video {string}: movie filename
        '''
        MsgTerm.info('Codificar vídeo %s' % video, nl=True)
        parts = video.split('.')
        parts.pop()
        parts.append(self.args.format)
        new_video = '.'.join(parts)

        # Verificar si el video en mkv ya existe en el directorio
        if os.path.isfile(new_video):
            self.omitidos += 1
            MsgTerm.alert('El vídeo ya existe, omitir')
        else:
            # Convertir video
            self.success.append( new_video )
            p = subprocess.Popen(('ffmpeg', '-i', video, new_video))
            p.wait()

            # check ffmpeg return code
            if p.returncode != 0:
                MsgTerm.fatal('ffmpeg devolvio un error de error')
                sys.exit(1)
            # Mover el video a la carpeta de backup
            elif self.args.move:
                old_path = os.path.join(self.args.carpeta, video)
                new_path = os.path.join(self.backup_folder, video)
                MsgTerm.info('Mover vídeo a la carpeta backup %s' % new_path)

                if not os.path.isfile(new_path):
                    os.rename(old_path, new_path)
                else:
                    MsgTerm.error(['Error al realizar el backup el fichero ya existe', new_path, 'Se omite'])


    def run(self):
        '''Ejecutar'''

        # Cambiar de carpeta
        os.chdir(self.args.carpeta)
        self.get_files()

        if self.total == 0:
            MsgTerm.alert('Sin videos que codificar', par=True)
            os.chdir(self.current_folder)
            sys.exit(1)
        else:
            # Crear carpeta backup
            if self.args.move:
                self.create_folder_backup()
            for movie in self.videos:
                self.posicion += 1
                MsgTerm.success('Video %d de %d' % (self.posicion, self.total), par=True)
                self.convert( movie )
            self.resumen()

        # Volver a la carpeta inicial
        os.chdir(self.current_folder)


    def resumen(self):
        '''Mostrar un resumen al finalizar'''
        msgs = [
            'Total videos:      %d' % self.total,
            'Total omitidos:    %d' % self.omitidos,
            'Total convertidos: %d' % len(self.success)
        ]
        MsgTerm.success(msgs)

        MsgTerm.text('Listado de videos convertidos:', label='-')
        for v in self.success:
            MsgTerm.text(v, label='>>')

        MsgTerm.info('Finalizado')


if __name__ == '__main__':
    code = Recode()
    code.run()
