import re
import os
import argparse
import shlex
from funciones.utilities import printConsole,printError
from comandos.comando import *
from comandos.reportes import execute_rep


def Commands():
   printConsole(" ---- Bienvenido al Sistema de Archivos de  - 202109754 ---- ")
   while True:
      command = input('\033[36m<<System>> - Ingrese un comando -\n\033[00m').lower()
      command = re.sub(r"[#][^\n]*", "", command)
      if command == "": continue
      elif re.search("[e|E][x|X][i|I][t|T]", command): break
      AnalyzeType(command)
   printConsole("... Saliendo del programa ...")
   

def AnalyzeType(entry):
    try:
        #verificar si tiene la forma de un comentario 
        if re.search(r"^[#][^\n]*", entry) or re.search(r"^[#][^\n]*$", entry):
            printConsole(entry)
        else: 
            printConsole("Analizando comando: " + entry)
            split_args = shlex.split(entry)
            command = split_args.pop(0)
            if (command == "execute"):
                print(" ------ Se detecto execute ------ ")
                fn_execute(split_args)
                print(" ------ Termino execute ------ ")
            elif(command == "mkdisk"):
                print(" ------ Se detecto mkdisk ------ ")
                fn_mkdisk(split_args)
                print(" ------ Termino mkdisk ------ ")
            elif(command == "rmdisk"):
                print(" ------ Se detecto rmdisk ------ ")
                fn_rmdisk(split_args)
                print(" ------ Termino rmdisk ------ ")
            elif(command == "fdisk"):
                print(" ------ Se detecto fdisk ------ ")
                fn_fdisk(split_args)
                print(" ------ Termino fdisk ------ ")
            elif(command == "mount"):
                print(" ------ Se detecto mount ------ ")
                fn_mount(split_args)
                print(" ------ Termino mount ------ ")
            elif(command == "unmount"):
                print(" ------ Se detecto unmount ------ ")
                fn_unmount(split_args)
                print(" ------ Termino unmount ------ ")
            elif (command == "mkfs"):
                print(" ------ Se detecto mkfs ------ ")
                fn_mkfs(split_args)
                print(" ------ Termino mkfs ------ ")
            elif (command == "pause"):
                print(" ------ Se detecto pause ------ ")
                input("Presione enter para continuar...")
                print(" ------ Termino pause ------ ")
            elif (command == "rep"):
                print(" ------ Se detecto rep ------ ")
                fn_rep(split_args)
                print(" ------ Termino rep ------ ")
    except Exception as e: pass

def fn_execute(split_args):
    try:
        parser = argparse.ArgumentParser(description="Parámetros")
        parser.add_argument("-path", required=True, help="Ruta del archivo a ejecutar")
        args = parser.parse_args(split_args)

        if os.path.exists(args.path):
            with open(args.path, 'r') as file:
                for line in file:
                    line = line.lower()
                    AnalyzeType(line)
        else:
            print(f"El archivo {args.path} no existe.")

    except SystemExit: printError("Análisis de argumentos")
    except Exception as e: printError(str(e))

def fn_mkdisk(split_args):
    try:
        parser = argparse.ArgumentParser(description="Parámetros")
        parser.add_argument("-size", required=True, type=int, help="Tamaño del disco")
        parser.add_argument("-path", required=True, help="Ruta donde se creará el disco")
        parser.add_argument("-fit", required=False, choices=["bf", "ff", "wf"], default="ff",help="Tipo de ajuste de disco (opcional)")
        parser.add_argument("-unit", required=False, choices=["k", "m"], default="m", help="Unidad de tamaño (opcional)")
        args = parser.parse_args(split_args)

        execute_mkdisk(args)

    except SystemExit: printError("Análisis de argumentos")
    except Exception as e: printError(str(e))

def fn_rmdisk(split_args):
    try:
        parser = argparse.ArgumentParser(description="Parámetros")
        parser.add_argument("-path", required=True, help="Ruta donde se encuentra el disco a eliminar")

        args = parser.parse_args(split_args)

        execute_rmdisk(args)

    except SystemExit: printError("Análisis de argumentos")
    except Exception as e: printError(str(e))

def fn_fdisk(split_args):
    try:
        parser = argparse.ArgumentParser(description="Parámetros")
        parser.add_argument("-size", type=int, help="Tamaño de la particion")
        parser.add_argument("-path", required=True, help="Ruta del disco en donde se creara la particion")
        parser.add_argument("-name", required=True, help="Nombre de la particion")
        parser.add_argument("-unit", required=False, choices=["b","k", "m"], default="k", help="Unidad de tamaño (opcional)")
        parser.add_argument("-type", required=False, choices=["p", "e", "l"], default="p", help="Tipo de particion (opcional)")
        parser.add_argument("-fit", required=False, choices=["bf", "ff", "wf"], default="wf",help="Tipo de ajuste de disco (opcional)")
        parser.add_argument("-add", required=False, help="Agregar espacio a la particion (opcional)")
        parser.add_argument("-delete", required=False, choices=["full"], help="Eliminar particion (opcional)")
        args = parser.parse_args(split_args)

        execute_fdisk(args)

    except SystemExit: printError("Análisis de argumentos")
    except Exception as e: printError(str(e))


def fn_mount(split_args):
    try:
        parser = argparse.ArgumentParser(description="Parámetros")
        parser.add_argument("-path", required=True, help="Ruta del disco a montar")
        parser.add_argument("-name", required=True, help="Nombre de la particion a cargar")
        args = parser.parse_args(split_args)

        execute_mount(args)

    except SystemExit: printError("Análisis de argumentos")
    except Exception as e: printError(str(e))

def fn_unmount(split_args):
    try:
        parser = argparse.ArgumentParser(description="Parámetros")
        parser.add_argument("-id", required=True, help="Id de la particion a desmontar")
        args = parser.parse_args(split_args)

        execute_unmount(args)

    except SystemExit: printError("Análisis de argumentos")
    except Exception as e: printError(str(e))


def fn_mkfs(split_args):
    try:
        parser = argparse.ArgumentParser(description="Parámetros")
        parser.add_argument("-id", required=True, help="Id de la particion a formatear")
        parser.add_argument("-type", required=False, choices=["full"], default="full", help="Tipo de formateo")
        parser.add_argument("-fs", required=False, choices=["2fs", "3fs"], default="3fs", help="Tipo de sistema de archivos")
        args = parser.parse_args(split_args)

        execute_mkfs(args)

    except SystemExit: printError("Análisis de argumentos")
    except Exception as e: printError(str(e))

def fn_rep(split_args):
    try:
        parser = argparse.ArgumentParser(description="Parámetros")
        parser.add_argument("-name", required=True, choices=["mbr", "disk", "inode", "journaling", "block", "bm_inode", "bm_block", "tree", "sb", "file", "ls"], help="Nombre del reporte")
        parser.add_argument("-path", required=True, help="Ruta del reporte")
        parser.add_argument("-id", required=True, help="Id de la particion a reportar")
        parser.add_argument("-ruta", required=False, help="Nombre del archivo o carpeta del que se mostrara el reporte")
        args = parser.parse_args(split_args)

        execute_rep(args)

    except SystemExit: printError("Análisis de argumentos")
    except Exception as e: printError(str(e))
