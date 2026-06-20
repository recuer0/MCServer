# MCServer

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Minecraft](https://img.shields.io/badge/minecraft-server-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A simple and efficient way to automate the installation of a Minecraft Java Edition server, combined with a graphical user interface (GUI) that allows monitoring and management of the server. It streamlines the entire process, making server administration more intuitive, accessible, and user-friendly, even for users with little prior experience.

---
## ⚒️ Installation:

On CMD / PowerShell, use **git** to clone this project to a directory on your computer:
``` bash
git clone https://github.com/recuer0/MCServer.git
cd MCServer
installer.exe
```
Or, download the project's ZIP file, open it in your file explorer, and run installer.exe.

- Java must be installed to set up the server --> [Java 25 Downloads](https://www.oracle.com/java/technologies/javase/jdk25-archive-downloads.html)
- NodeJS must be installed to use the dashboard (GUI) --> [NodeJS Downloads](https://nodejs.org/es/download/current)

> [!Note]
>### Supported versions of the installer
> The installer only supports **standard server versions (1.16, 1.18.1, 1.21, 26.2, etc.)**. If you want to use a snapshot (26.2-snapshot-8), pre, or rc version, download it manually and copy it to the `MCServer/server/` directory.

Once the installation is complete, you can run `installer.exe` again whenever you want to open the graphical interface.
***
>[!Note]
>### Installation using Python instead of installer.exe
>1. Clone the repository:
>``` bash
>git clone https://github.com/recuer0/MCServer.git
>cd MCServer
>```
>
>2. Create and start a virtual environment (Optional but recommended):
>``` bash
>python -m venv venv
>source venv/bin/activate # Linux/Mac
>venv\Scripts\activate # Windows
>```
>
>3. Install the dependencies:
>```bash
>pip install -r requirements.txt
>```
>
>4. Run the project:
>```bash
>python installer.py
>```
>***
>When you're done, you can exit the venv by running:
>``` bash
>deactivate # Windows/Linux /Mac
>```
>***
>Whenever you want to run the project:
>```bash
>source venv/bin/activate   # If you're using venv
>python installer.py             # Execute
>```

***
If you prefer, you can perform a manual installation by following these instructions:
- 🔗 https://4imk16.vercel.app 
- 🌐 Versión HTML: `README.html`
---
## ⚠️ Current Project Status

This project **is still in development**.  
It works properly and offers the basic features for creating and managing servers in the dashboard. However, it is subject to future improvements and updates.

---

## ℹ️ Information

This dashboard is designed to:
- Manage a Minecraft server
- Organize project information
- Provide a more visual and user-friendly view of the system
- Execute commands in real time
- Display connected users in real time

---
## ❤️‍🩹 Future Improvements
- More interactive dashboard
- Improved UI design
- User kick/ban system
- More administrative tools
- System resource performance dashboard
- Simultaneous management of multiple servers