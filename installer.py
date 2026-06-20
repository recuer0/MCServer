import os
import signal
import sys
import time

from python_modules.downloader import Downloader,Installer

java_url = "https://www.oracle.com/java/technologies/javase/jdk25-archive-downloads.html"
node_url = "https://nodejs.org/es/download/current"

ROJO = "\033[31m"
VERDE = "\033[32m"
AMARILLO = "\033[33m"
AMARILLO_BRILLANTE = "\033[93m"
AZUL = "\033[34m"
CIAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"

def def_handler(_sig, _frame):
    global downloader
    global installer
    print(f"\n\n{ROJO}[!] Saliendo...{RESET}\n")
    
    if downloader.downloading or installer.installing:
        time.sleep(0.3)
        raise KeyboardInterrupt
    else:
        sys.exit(0)

signal.signal(signal.SIGINT, def_handler)

def download(downloader):
    print(f"\n{AMARILLO}{AMARILLO}[+]{RESET}{RESET} Bienvenido a la instalación de {AZUL}MCServer{RESET}!")
    print(f"\n{AMARILLO}[+]{RESET} Para la instalación, asegurése de tener instalado {AZUL}Java{RESET} y {AZUL}NodeJS{RESET}")
    time.sleep(0.3)
    print(f"\t{AZUL}[Java]{RESET} --> {CIAN}{java_url}{RESET}")
    print(f"\t{AZUL}[NodeJS]{RESET} --> {CIAN}{node_url}{RESET}")
    
    opt1 = input(f"\n¿Desea continuar con la descarga? {MAGENTA}(Y/n){RESET}: ").strip()
    
    if opt1.lower() != "y" and opt1 != "":
        print(f"\n{ROJO}[!] Cancelando instalación...{RESET}")
        sys.exit(1)
    
    
    print(f"\n{AMARILLO}[+]{RESET} Obteniendo información necesaria...")
    version = ""
    opt2 = ""

    time.sleep(0.75)
    downloader.obtain_links()
    time.sleep(0.25)
    
    #print(json_links)
    #sys.exit(0)

    while not version:
        version = input("\nIntroduzca su versión: ").strip()
        
        if not downloader.validate_version(version):
            print(f"{ROJO}[!] Versión NO válida!{RESET}")
            version = ""

    time.sleep(0.25)
    print(f"\n{AMARILLO}[+]{RESET} Link de descarga: " + downloader.server_link)

    while not opt2:
        opt2 = input(f"{AMARILLO}[+]{RESET} ¿Está seguro de realizar la descarga --> versión {AZUL}{downloader.version}{RESET}? {MAGENTA}(Y/n){RESET}: ").strip()

        if not opt2 or opt2.lower() == 'y':
            time.sleep(0.25)
            break
        elif opt2.lower() == 'n':
            def_handler(None,None)
        else:
            opt2 = ""

    print(f"\n{AMARILLO}[+]{RESET} Comenzando descarga...\n")
    
    if downloader.download_server():
        print(f"\n{AMARILLO}[+]{RESET} {VERDE}Descargado correctamente!{RESET}")
    else:
        sys.exit(1)

def install(installer):
    print(f"\n{AMARILLO}[+]{RESET} Comenzando instalación...")
    installer.java_version = installer.verify_java()
    installer.npm_version = installer.verify_npm()
    
    if not installer.java_version:
        print(f"\n{ROJO}[!] Java no instalado!{RESET}")
        print(f"{ROJO}[!] Instálelo para continuar:{RESET} {CIAN}{java_url}{RESET}\n")
        sys.exit(1)

    if installer.npm_version == "Not installed":
        print(f"\n{ROJO}[!] npm no instalado!{RESET}")
        print(f"{ROJO}[!] Instálelo para utilizar la interfaz gráfica tras la instalación:{RESET} {CIAN}{node_url}{RESET}")
        
        
    print(f"\n{AMARILLO}[+]{RESET} Versión de Java: {VERDE}{installer.java_version}{RESET}")
    print(f"{AMARILLO}[+]{RESET} Versión de npm: {VERDE}{installer.npm_version}{RESET}")
    
    print(f"\n{AMARILLO}[+]{RESET} Instalando servidor...")
    installer.install_server()
    print(f"\n{AMARILLO}[+]{RESET} {VERDE}Servidor instalado con éxito!{RESET}\n")

def create(installer):
    eula = ""
    while not eula:
        eula = input(f"{AMARILLO_BRILLANTE}[i]{RESET} Para continuar, debe aceptar el {AMARILLO_BRILLANTE}EULA{RESET} --> {AZUL}https://aka.ms/MinecraftEULA{RESET} {MAGENTA}(y/n){RESET}: ").strip()
        
        if eula.lower() == "y":
            installer.accept_eula()
        elif eula.lower() == "n":
            print(f"\n{ROJO}[!] Cancelando...{RESET}")
            sys.exit(1)
        else:
            eula = ""
            continue
        
    print(f"{AMARILLO}[+]{RESET} EULA aceptado")
    print(f"\n{AMARILLO}[+]{RESET} Creando mundo...")
    installer.install_server()
    print(f"\n{AMARILLO}[+]{RESET} {VERDE}Mundo creado exitosamente!{RESET}")
    gui(installer)
    
def gui(installer):
    if not installer.npm_version:
        installer.npm_version = installer.verify_npm()
    
    if installer.npm_version != "Not installed":
        installer.install_gui()
        print(f"{AMARILLO}[+]{RESET} Abriendo interfaz gráfica...\n")
        installer.open_gui()
        time.sleep(.5)
    else:
        print(f"\n{ROJO}[!] No se ha podido instalar la interfaz gráfica. No está NodeJS instalado!{RESET}")
        print(f"{AMARILLO}[+]{RESET} Instale NodeJS para continuar: {CIAN}{node_url}{RESET}")

if __name__ == '__main__':
    repeat = True
    while repeat:
        repeat = False
        downloader = Downloader()
        installer = Installer()
        match downloader.status:
            case "not-downloaded":
                print(f"\n{AMARILLO}[+]{RESET} Estado actual: {ROJO}no descargado{RESET}")
                download(downloader)
                installer = Installer(version=downloader.version)
                
                install_opt = ""
                
                while not install_opt:
                    install_opt = input(f"\n{RESET}[+] ¿Desea continuar al proceso de {AZUL}instalación{RESET}? {MAGENTA}(Y/n){RESET}: ").strip()
                    
                    if not install_opt or install_opt.lower() == "y":
                        install(installer)
                        create(installer)
                    elif install_opt.lower() == "n":
                        def_handler(None,None)
                    else:
                        install_opt = ""
                
            case "downloaded":
                print(f"\n{AMARILLO}[+]{RESET} Estado actual: {AZUL}descargado pero no instalado{RESET}")
                installer.get_version()
                print(f"\n{AMARILLO}[+]{RESET} Se ha detectado un servidor descargado --> versión: {AZUL}{installer.version}{RESET}")
                
                opt = input(f"{AMARILLO}[+]{RESET} ¿Desea mantener esta versión? {MAGENTA}(Y/n){RESET}: ").strip()
                if opt.lower() == "y" or not opt:
                    install(installer)
                    create(installer)
                elif opt.lower() == "n":
                    os.remove("server/server.jar")
                    repeat = True
                else:
                    break
                    
            case "installed":
                print(f"\n{AMARILLO}[+]{RESET} Estado actual: {AZUL}instalado pero mundo no creado{RESET}")
                create(installer)
                
            case "created":
                print(f"\n{AMARILLO}[+]{RESET} {VERDE}Todo en orden{RESET}")
                gui(installer)
            case _:
                print(f"\n{ROJO}[!] Información corrupta{RESET}\n")