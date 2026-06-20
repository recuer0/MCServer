import json
import os
import re
import requests
import shutil
import signal
import subprocess
import sys

from status import init_status,delete_all
from tqdm import tqdm

NEGRO = "\033[30m"
ROJO = "\033[31m"
VERDE = "\033[32m"
AMARILLO = "\033[33m"
AZUL = "\033[34m"
MAGENTA = "\033[35m"
CIAN = "\033[36m"
BLANCO = "\033[37m"
RESET = "\033[0m"

class Downloader:
    def __init__(self):
        self.URL = "https://gist.githubusercontent.com/cliffano/77a982a7503669c3e1acb0a0cf6127e9/raw/02aa2eae277c98ab3aeb715ffa279fd4ce66ce60/minecraft-server-jar-downloads.md"
        self.version: str
        self.server_link: str
        self.links: dict
        self.json_links: str
        self.downloading = False
        self.file = None
        self.status = init_status()
        self.versions: list


    # --------------------------------------------------------
    # -----------------------DESCARGA-------------------------
    # --------------------------------------------------------
    def obtain_links(self):
        try:
            response = requests.get(self.URL, timeout=10)
        except requests.exceptions.Timeout:
            print(f"\n{ROJO}[!] El servidor de descarga no responde :({RESET}")
            return None,None
        
        all_links = response.text

        parsed_lines = [] 
        util_links = {}

        for line in all_links.splitlines():
            line = line.split("|")
            parsed_line = [line.strip() for line in line][1:][:-1]
            if parsed_line[1] != "Not found":
                parsed_lines.append(parsed_line)

        for line in parsed_lines:
            if re.match(r'\d+\.\d+(\.\d+)?$',line[0]):
                util_links[line[0]] = {
                    "version": line[0],
                    "server-link": line[1],
                    "client-link": line[2]
                }

        self.versions = [version for version in util_links.keys()]

        self.links,self.json_links = util_links,json.dumps(util_links,indent=4)


    def validate_version(self,version):
        server_data = self.links.get(version)

        if server_data:
            self.version = version
            self.server_link = server_data.get('server-link')
            return True
        return False


    def download_server(self,chunk_size=8192):
        descarga_completa = False
        barra = None
        destino = 'server/server.jar'

        def manejador_sigint(signum, frame):
            if barra is not None:
                barra.close()  # cierre limpio ANTES de que se propague la excepción
            print(f"\n{ROJO}[!] Saliendo...{RESET}")
            raise KeyboardInterrupt()

        handler_previo = signal.signal(signal.SIGINT, manejador_sigint)

        try:
            with requests.get(self.server_link, stream=True, timeout=10) as respuesta:
                self.downloading = True
                respuesta.raise_for_status()
                total = int(respuesta.headers.get("content-length", 0))

                with open(destino, "wb") as f:
                    barra = tqdm(
                        total=total if total else None,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=f'{MAGENTA}{destino}{RESET}',
                    )
                    for bloque in respuesta.iter_content(chunk_size=chunk_size):
                        if bloque:
                            f.write(bloque)
                            barra.update(len(bloque))
                    barra.close()

            descarga_completa = True
            self.downloading = False
            return True

        except KeyboardInterrupt:
            print(f"{ROJO}[!] Descarga interrumpida por el usuario{RESET}")

        except requests.exceptions.RequestException as e:
            print(f"\n{ROJO}[!] Error durante la descarga: {e}{RESET}")
            return False

        finally:
            signal.signal(signal.SIGINT, handler_previo)
            if not descarga_completa and os.path.exists(destino):
                os.remove(destino)
                print(f"{ROJO}[!] Archivo '{destino.split('/')[1]}' eliminado.{RESET}")
                return False
            
           
# --------------------------------------------------------        
# ---------------------INSTALADOR-------------------------
# --------------------------------------------------------
class Installer:
    def __init__(self, version=None):
        self.versions:list
        self.version: str
        self.java_version: str = ""
        self.npm_version: str = ""
        self.installing: bool = False
        
    def get_version(self):
        try:
            downloader = Downloader()
            downloader.obtain_links()
            self.versions = downloader.versions
            with open("server/server.jar", "rb") as f:
                contenido = f.read().decode("utf-8", errors="ignore")
                matches = re.findall(r'\d+\.\d+(?:\.\d+)?', contenido)
                
                parsed_matches = [match for match in matches if match in self.versions]
                
                self.version = parsed_matches[-1]
                return self.version
        except:
            self.version = None
            
    def verify_java(self):
        try:
            r = subprocess.run(["java.exe","--version"],text=True,capture_output=True)
            return r.stdout.strip().splitlines()[0]
        except FileNotFoundError:
            return False

    def verify_npm(self):
        try:
            r = subprocess.run(["npm.cmd","-v"],text=True,capture_output=True)
            return r.stdout.strip()
        except FileNotFoundError:
            return "Not installed"
        
    def install_server(self):
        try:
            self.installing = True 
            proceso = subprocess.Popen(
                ["java", "-Xmx4G", "-Xms4G", "-jar", "server.jar", "nogui"],
                cwd='server',
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # combina stderr con stdout en el mismo stream
                text=True,
                bufsize=1                 # line-buffered: entrega línea a línea
            )

            for linea in proceso.stdout:
                linea = linea.rstrip()
                #print(f"[SERVER] {linea}")

                # Aquí puedes evaluar cada línea según lo que necesites
                if "Done" in linea:
                    print(f"{AMARILLO}[+]{RESET} El servidor terminó de cargar")
                    proceso.stdin.write("stop\n")
                    proceso.stdin.flush()
                    break

            proceso.wait()  # espera a que el proceso termine del todo
            self.installing = False
             
        except KeyboardInterrupt:
            print(f"{ROJO}[!] Descarga interrumpida por el usuario{RESET}")
            delete_all()
            sys.exit(1)
        
    def install_gui(self):
        if not os.path.exists("dashboard/node_modules"):
            try:
                self.installing = True 
                print(f"\n{AMARILLO}[+]{RESET} Instalando interfaz gráfica...")
                proceso = subprocess.Popen(
                    ["npm.cmd","install"],
                    cwd='dashboard',
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,  # combina stderr con stdout en el mismo stream
                    text=True,
                    bufsize=1                 # line-buffered: entrega línea a línea
                )
                
                for linea in proceso.stdout:
                    pass
                print(f"{AMARILLO}[+]{RESET} {VERDE}Interfaz gráfica instalada!{RESET}")
                self.installing = False 
            except KeyboardInterrupt:
                print(f"{ROJO}[!] Descarga interrumpida por el usuario{RESET}")
                shutil.rmtree('dashboard/node_modules')
                sys.exit(1)
                
    
    def open_gui(self):
        subprocess.Popen(
            ["npm.cmd", "start"],
            cwd="dashboard",
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
    def accept_eula(self):
        with open("server/eula.txt","r") as f:
            lines = f.readlines()
            lines[2] = 'eula=true\n'
            
        with open("server/eula.txt","w") as f:
            f.writelines(lines)