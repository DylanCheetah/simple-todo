# Lesson 01 - Prerequisites

In this tutorial series, we will learn full-stack web development by creating a simple todo list web app.
Before we begin, follow the project setup instructions for your OS.

## Windows
01. download Node.js from [https://nodejs.org/](https://nodejs.org/)
02. run the installer
03. follow the prompts and leave all default options selected
04. download Python from [https://www.python.org/](https://www.python.org/)
05. run the installer
06. check the box beside "Add python.exe to PATH"
07. follow the prompts and leave all default options selected
08. download Visual Studio Code from [https://code.visualstudio.com/](https://code.visualstudio.com/)
09. run the installer
10. follow the prompts and leave all default options selected
11. create a folder for the project
12. open the folder in Visual Studio Code
13. click Terminal > New Terminal to open a new terminal
14. execute `python -m venv venv` to create a new Python virtual environment
15. execute the following commands to activate the virtual environment:
```sh
cmd
venv\Scripts\activate
```

## Ubuntu
01. open a terminal
02. execute `sudo apt install nodejs npm` to install Node.js
03. execute `sudo apt install python3-venv` to install the Python virtual environment package
04. download the Visual Studio Code .deb package from [https://code.visualstudio.com/](https://code.visualstudio.com/)
05. switch to the folder containing the downloaded .deb package
06. execute `sudo dpkg -iG <vsc_deb>` where `<vsc_deb>` is the name of the .deb package
07. create a folder for the project
08. open the folder in Visual Studio Code
09. click Terminal > New Terminal
10. execute `python3 -m venv venv` to create a new Python virtual environment
11. execute `./venv/bin/activate` to activate the virtual environment
