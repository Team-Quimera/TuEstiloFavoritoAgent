# agent/tools.py — Herramientas del agente
# Generado por AgentKit — Cliente: Tu Estilo Favorito (optica)

"""
Herramientas especificas del negocio.
Estas funciones extienden las capacidades del agente mas alla de responder texto.
Para Tu Estilo Favorito (optica), las herramientas previstas son:
  - Buscar en knowledge (FAQ, catalogo, precios)
  - Registrar solicitud de cita para examen visual
  - Registrar lead/cotizacion
"""

import os
import yaml
import logging
from datetime import datetime

logger = logging.getLogger("agentkit")


def cargar_info_negocio() -> dict:
    """Carga la informacion del negocio desde business.yaml."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    """Retorna el horario de atencion del negocio."""
    info = cargar_info_negocio()
    return {
        "horario": info.get("negocio", {}).get("horario", "No disponible"),
    }


def buscar_en_knowledge(consulta: str) -> str:
    """
    Busca informacion relevante en los archivos de /knowledge.
    Retorna el contenido mas relevante encontrado.
    """
    resultados = []
    knowledge_dir = "knowledge"

    if not os.path.exists(knowledge_dir):
        return "No hay archivos de conocimiento disponibles."

    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:500]}")
        except (UnicodeDecodeError, IOError):
            continue

    if resultados:
        return "\n---\n".join(resultados)
    return "No encontre informacion especifica sobre eso en mis archivos."


# ════════════════════════════════════════════════════════════
# Herramientas especificas para Tu Estilo Favorito (optica)
#
# NOTA: Estas son versiones simples que registran solicitudes a un
# archivo de leads. Para produccion conviene conectar a Google Sheets,
# CRM o un calendario real (Google Calendar, Calendly, etc.).
# ════════════════════════════════════════════════════════════

LEADS_FILE = "knowledge/_leads_registrados.txt"


def registrar_solicitud_cita(nombre: str, telefono: str, dia_preferido: str, motivo: str = "examen visual") -> str:
    """
    Registra una solicitud de cita en un archivo plano.
    Retorna un mensaje de confirmacion para el cliente.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    linea = f"[{timestamp}] CITA — {nombre} | Tel: {telefono} | Dia preferido: {dia_preferido} | Motivo: {motivo}\n"
    try:
        os.makedirs(os.path.dirname(LEADS_FILE), exist_ok=True)
        with open(LEADS_FILE, "a", encoding="utf-8") as f:
            f.write(linea)
        return f"Listo {nombre}, anoté tu solicitud de cita para {dia_preferido}. El equipo te llama al {telefono} para confirmar el horario exacto."
    except IOError as e:
        logger.error(f"Error registrando cita: {e}")
        return "Tuve un problema guardando tu solicitud. Por favor escríbenos directamente y un compañero te atiende."


def registrar_lead(nombre: str, telefono: str, interes: str) -> str:
    """
    Registra un lead/interes en cotizacion o producto especifico.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    linea = f"[{timestamp}] LEAD — {nombre} | Tel: {telefono} | Interes: {interes}\n"
    try:
        os.makedirs(os.path.dirname(LEADS_FILE), exist_ok=True)
        with open(LEADS_FILE, "a", encoding="utf-8") as f:
            f.write(linea)
        return f"Perfecto {nombre}, tomé tus datos. Un compañero del equipo te contacta al {telefono} con la información de {interes}."
    except IOError as e:
        logger.error(f"Error registrando lead: {e}")
        return "Tuve un problema guardando tus datos. Por favor escríbenos directamente y un compañero te atiende."
