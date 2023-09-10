import os
from elementos.disco import *
from elementos.mbr import Mbr
from comandos.mount import particiones_montadas
from elementos.ebr import Ebr

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

        if elemento_encontrado == None:
            print("No se encontro la particion")
        else:
            inicioEBR = -1
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
            
            #generando codigo .dot de los ebr en caso existan
            if mbrDisco.particion1.type == b'e':
                dot += dotExtendida(mbrDisco.particion1)
                inicioEBR = mbrDisco.particion1.start
            elif mbrDisco.particion2.type == b'e':
                dot += dotExtendida(mbrDisco.particion2)
                inicioEBR = mbrDisco.particion2.start
            elif mbrDisco.particion3.type == b'e':
                dot += dotExtendida(mbrDisco.particion3)
                inicioEBR = mbrDisco.particion3.start
            elif mbrDisco.particion4.type == b'e':
                dot += dotExtendida(mbrDisco.particion4)
                inicioEBR = mbrDisco.particion4.start

            if inicioEBR != -1:
                dot += dotLogica(elemento_encontrado[2], inicioEBR)
            
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

def dotExtendida(particion):
    dot = ""
    dot += " <TR><TD bgcolor=\"yellow\">PARTICION EXTENDIDA</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"yellow\">part_status</TD><TD bgcolor=\"yellow\">{particion.status}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"yellow\">part_type</TD><TD bgcolor=\"yellow\">{particion.type}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"yellow\">part_fit</TD><TD bgcolor=\"yellow\">{particion.fit}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"yellow\">part_start</TD><TD bgcolor=\"yellow\">{particion.start}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"yellow\">part_size</TD><TD bgcolor=\"yellow\">{particion.s}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"yellow\">part_name</TD><TD bgcolor=\"yellow\">{particion.name}</TD></TR>\n"
    return dot

def dotLogica(rutaDisco, puntero):
    with open(rutaDisco, "rb") as discoAbierto:
        discoAbierto.seek(puntero)
        ebr = Ebr()
        obtenerDatosDisco(rutaDisco, puntero, ebr)
        dot = ""
        dot += " <TR><TD bgcolor=\"yellow\">PARTICION LOGICA</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"yellow\">part_status</TD><TD bgcolor=\"yellow\">{ebr.status}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"yellow\">part_fit</TD><TD bgcolor=\"yellow\">{ebr.fit}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"yellow\">part_start</TD><TD bgcolor=\"yellow\">{ebr.start}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"yellow\">part_size</TD><TD bgcolor=\"yellow\">{ebr.s}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"yellow\">part_next</TD><TD bgcolor=\"yellow\">{ebr.next}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"yellow\">part_name</TD><TD bgcolor=\"yellow\">{ebr.name}</TD></TR>\n"
        if ebr.next != -1:
            dot += dotLogica(rutaDisco, ebr.next)
        return dot