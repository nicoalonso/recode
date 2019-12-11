#!/usr/bin/python3

import os
import sys
import subprocess
from argparse import ArgumentParser

# Clase
class Recode:

    # Constructor
    def __init__(self, args):
        print('[ ] Convertir videos a MKV')
        # TODO: Parsear parametros de entrada
        # Establecer folder y parametros para ffmpeg

    # Definir los argumentos por linea de comandos
    def arguments(self):
        self.parser = ArgumentParser()


    # Recuperar el listado de ficheros
    def get_files(self):
        print('[+] Buscar videos en formato AVI')
        print('')
        self.videos = []
        for r, d, f in os.walk('.'):
            for file in f:
                if '.avi' in file:
                    self.videos.append( file )
                    print(' > ', file)

        self.total = len(self.videos)
        print('')
        print('[+] Total videos', self.total)

    # Transformar
    def convert(self, video):
        print(' ')
        print('[+] Codificar video: ', video)
        video_mkv = video.split('.')[0] + '.mkv'

        # Verificar si el video en mkv ya existe en el directorio
        if os.path.isfile(video_mkv):
            self.omitidos += 1
            print('[!] El video ya existe, omitir')
        else:
            # Convertir video
            self.success.append( video_mkv )
            p = subprocess.Popen(('ffmpeg', '-i', video, video_mkv))
            p.wait()

    # Ejecutar
    def run(self):
        self.get_files()
        self.omitidos = 0
        self.posicion = 0
        self.success = []
        bar = Bar('Progreso', max=self.total)

        for movie in self.videos:
            self.posicion += 1
            print('[i] Video %d de %d' % (self.posicion, self.total))
            self.convert( movie )

        # Mostrar resumen
        print('')
        print('[+] Total videos: ', self.total)
        print('[+] Total omitidos', self.omitidos)
        print('[+] Total convertidos', len(self.success))
        print('')
        print('[-] Listado de videos convertidos:')
        for v in self.success:
            print(' >> ', v)
        print('')
        print('[+] Finalizado')


if __name__ == '__main__':
    code = Recode(sys.argv)
    code.run()
