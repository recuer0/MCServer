import os
import shutil

pre_server_files = ["eula.txt","server.properties","logs","libraries","versions","server.jar"]
server_files = pre_server_files + ["world","whitelist.json","usercache.json","ops.json","banned-players.json","banned-ips.json"]

if not os.path.exists("server"):
    os.mkdir('server')

def delete_all(save_jar=False):
    for file in os.listdir('server'):
        if os.path.isfile(f'server/{file}'):
            if save_jar:
                os.remove('server/' + file) if file != "server.jar" else True
        else:
            shutil.rmtree(f'server/{file}')

def init_status():
    global pre_server_files
    global server_files
    
    content = os.listdir('server')
    
    if len(content) == 1 and content[0] == 'server.jar':
        return "downloaded"
    
    if all(os.path.exists(os.path.join('server', nombre)) for nombre in server_files):
        return "created"
    
    elif all(os.path.exists(os.path.join('server', nombre)) for nombre in pre_server_files):
        return "installed"
    
    elif len(content) == 0:
        return "not-downloaded"
    
    else:
        for file in os.listdir('server'):
            if os.path.isfile:
                os.remove('server/' + file)
            else:
                shutil.rmtree(f'server/{file}')
        return "corrupt"