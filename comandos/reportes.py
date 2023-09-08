import os
from elementos.disco import *
from elementos.mbr import Mbr
from comandos.comando import particiones_montadas

def execute_rep(args):
    if args.name == "mbr":
        reporte_mbr(args.path, args.id)
    elif args.name == "disk":
        reporte_mbr(args.path, args.id)

def reporte_disk(ruta, id):
    print("reporte disk")
            

def reporte_mbr(ruta, id):
    #abrir disco y obtener particion
    try:
        #buscar id en particiones montadas
        elemento_encontrado = None

        for elemento in particiones_montadas:
            if elemento[0] == id:
                elemento_encontrado = elemento
                break

        mbrDisco = Mbr()
        obtenerDatosDisco(elemento_encontrado[2], 0, mbrDisco)
        mbrDisco.display_info()

        
        #generando codigo .dot del mbr
        dot = "digraph mbr{\n"
        dot += "a0 [shape=none label=<\n"
        dot += "<TABLE cellspacing=\"10\" cellpadding=\"10\" style=\"rounded\" bgcolor=\"red\">\n"
        dot += " <TR><TD bgcolor=\"yellow\">REPORTE MBR</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"yellow\">mbr_tamano</TD><TD bgcolor=\"yellow\">{mbrDisco.get_tamano()}</TD></TR>\n"
        dot += f" <TR><TD bgcolor=\"yellow\">mbr_fecha_creacion</TD><TD bgcolor=\"yellow\">{mbrDisco.get_time()}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"yellow\">mbr_disk_signature</TD><TD bgcolor=\"yellow\">{mbrDisco.get_dsk_signature()}</TD></TR>\n"
        dot += "</TABLE>>];\n"
        dot += "}"


        #generar la imagen del mbr
        f = open("mbr.dot", "w")
        f.write(dot)
        f.close()

        os.system("dot -Tpng mbr.dot -o mbr.png")
        os.system(f"{ruta}")


    except Exception as e:
        print(f"Error: {e}")
