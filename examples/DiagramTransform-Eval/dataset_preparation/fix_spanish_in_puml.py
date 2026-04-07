"""
Fix remaining Spanish words in .puml files by cross-referencing with English user stories.

Reads each .puml file, identifies Spanish text, and replaces with English equivalents.
Produces a detailed change log.
"""
import os
import re
import json

REVIEW_DIR = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'human_review')

# Comprehensive Spanish-to-English dictionary for all remaining terms found in .puml files.
# Built by cross-referencing Diagrams.json labels with original English user stories.

# Common Spanish nouns/phrases -> English
WORD_MAP = {
    # ===== Common nouns =====
    'datos': 'data',
    'Data': 'Data',
    'archivo': 'file',
    'archivos': 'files',
    'Archivo': 'File',
    'registro': 'record',
    'registros': 'records',
    'Registro': 'Record',
    'informe': 'report',
    'Informe': 'Report',
    'sesion': 'session',
    'Session': 'Session',
    'cuenta': 'account',
    'Cuenta': 'Account',
    'usuario': 'user',
    'Usuario': 'User',
    'usuarios': 'users',
    'contraseña': 'password',
    'nombre': 'name',
    'Nombre': 'Name',
    'apellido': 'last_name',
    'Apellido': 'Last_Name',
    'correo': 'email',
    'Correo': 'Email',
    'direccion': 'address',
    'Direccion': 'Address',
    'dirección': 'address',
    'telefono': 'phone',
    'Telefono': 'Phone',
    'teléfono': 'phone',
    'fecha': 'date',
    'hora': 'time',
    'horario': 'schedule',
    'horarios': 'schedules',
    'Horario': 'Schedule',
    'cita': 'appointment',
    'citas': 'appointments',
    'Cita': 'Appointment',
    'medico': 'doctor',
    'Medico': 'Doctor',
    'paciente': 'patient',
    'pacientes': 'patients',
    'Paciente': 'Patient',
    'enfermera': 'nurse',
    'Enfermera': 'Nurse',
    'historial': 'record',
    'prueba': 'test',
    'pruebas': 'tests',
    'resultado': 'result',
    'resultados': 'results',
    'grupos': 'groups',
    'grupo': 'group',
    'Grupo': 'Group',
    'equipo': 'team',
    'Equipo': 'Team',
    'proyecto': 'project',
    'Proyecto': 'Project',
    'sistema': 'system',
    'Sistema': 'System',
    'base': 'database',
    'campo': 'field',
    'campos': 'fields',
    'reglas': 'rules',
    'regla': 'rule',
    'codigo': 'code',
    'codigos': 'codes',
    'código': 'code',
    'pagina': 'page',
    'Pagina': 'Page',
    'ayuda': 'help',
    'inicio': 'home',
    'entorno': 'environment',
    'casos': 'cases',
    'caso': 'case',
    'logica': 'logic',
    'derivacion': 'derivation',
    'recursos': 'resources',
    'versiones': 'versions',
    'maquetas': 'mockups',
    'contenido': 'content',
    'Content': 'Content',
    'oficinas': 'offices',
    'muestra': 'sample',
    'validaciones': 'validations',
    'flexibles': 'flexible',
    'detalles': 'details',
    'envio': 'submission',
    'periodos': 'periods',
    'esquema': 'schema',
    'filas': 'rows',
    'publicar': 'publish',
    'publicados': 'published',
    'publicadas': 'published',
    'actualizados': 'updated',
    'actualizaciones': 'updates',
    'actualización': 'update',
    'validación': 'validation',
    'derivación': 'derivation',
    'información': 'information',
    'informacion': 'information',
    'agencia': 'agency',
    'agencias': 'agencies',
    'Agencia': 'Agency',
    'problemas': 'problems',
    'duplicado': 'duplicate',
    'auditoria': 'audit',
    'cronograma': 'schedule',
    'ronda': 'round',
    'edicion': 'editing',
    'segunda': 'second',
    'instalacion': 'facility',
    'instalaciones': 'facilities',
    'Instalacion': 'Facility',
    'comentario': 'comment',
    'comentarios': 'comments',
    'Comment': 'Comment',
    'estadisticas': 'statistics',
    'estadísticas': 'statistics',
    'errores': 'errors',
    'empresa': 'company',
    'empleados': 'employees',
    'planificacion': 'planning',
    'Planificación': 'Planning',
    'rutas': 'routes',
    'tarifas': 'rates',
    'actividades': 'activities',
    'reciclables': 'recyclables',
    'contenedores': 'containers',
    'entregas': 'deliveries',
    'eliminacion': 'disposal',
    'segura': 'safe',
    'documentacion': 'documentation',
    'favoritos': 'favorites',
    'recogida': 'pickup',
    'cercanos': 'nearby',
    'cercanas': 'nearby',
    'mapa': 'map',
    'sitios': 'sites',
    'eventos': 'events',
    'especiales': 'special',
    'postal': 'code',
    'quejas': 'complaints',
    'panel': 'dashboard',
    'bloquear': 'block',
    'Bloquear': 'Block',
    'comunicar': 'communicate',
    'Comunicar': 'Communicate',
    'leer': 'read',
    'Leer': 'Read',
    'responder': 'respond',
    'Responder': 'Respond',
    'ingresar': 'enter',
    'Ingresar': 'Enter',
    'escoger': 'choose',
    'Escoger': 'Choose',
    'conocer': 'know',
    'Conocer': 'Know',
    'usar': 'use',
    'Usar': 'Use',
    'incluir': 'include',
    'Incluir': 'Include',
    'evitar': 'avoid',
    'Evitar': 'Avoid',
    # Use case specific nouns
    'miembro': 'member',
    'miembros': 'members',
    'Miembro': 'Member',
    'visitante': 'visitor',
    'Visitante': 'Visitor',
    'patron': 'sponsor',
    'Patron': 'Sponsor',
    'voluntario': 'volunteer',
    'Voluntario': 'Volunteer',
    'ponente': 'speaker',
    'Ponente': 'Speaker',
    'asistente': 'attendee',
    'Asistente': 'Attendee',
    'organizador': 'organizer',
    'Organizador': 'Organizer',
    'moderador': 'moderator',
    'Moderador': 'Moderator',
    'investigador': 'researcher',
    'Investigador': 'Researcher',
    'administrador': 'administrator',
    'Administrador': 'Administrator',
    'propietario': 'owner',
    'programa': 'program',
    'programas': 'programs',
    'Programa': 'Program',
    'sesión': 'session',
    'evento': 'event',
    'Evento': 'Event',
    'tarea': 'task',
    'tareas': 'tasks',
    'Tarea': 'Task',
    'solicitud': 'request',
    'solicitudes': 'requests',
    'Solicitud': 'Request',
    'mensaje': 'message',
    'mensajes': 'messages',
    'notificacion': 'notification',
    'notificaciones': 'notifications',
    'permiso': 'permission',
    'permisos': 'permissions',
    'rol': 'role',
    'roles': 'roles',
    'perfil': 'profile',
    'Perfil': 'Profile',
    'imagen': 'image',
    'imagenes': 'images',
    'etiqueta': 'tag',
    'etiquetas': 'tags',
    'categoria': 'category',
    'categorias': 'categories',
    'formulario': 'form',
    'Formulario': 'Form',
    'busqueda': 'search',
    'Busqueda': 'Search',
    'tipo': 'type',
    'tipos': 'types',
    'nivel': 'level',
    'valor': 'value',
    'estado': 'status',
    'derechos': 'rights',
    'personas': 'people',
    'Personas': 'People',
    'Grupos': 'Groups',
    'factura': 'invoice',
    'Invoice': 'Invoice',
    'motivo': 'reason',
    'visita': 'visit',
    'disponibles': 'available',
    'expediente': 'file',
    'habitacion': 'room',
    'Habitacion': 'Room',
    'enfermeras': 'nurses',
    'Enfermeras': 'Nurses',
    'medicos': 'doctors',
    'Medicos': 'Doctors',
    'nacional': 'national',
    'Base': 'Database',
    'Keyword': 'Keyword',
    'Movil': 'Mobile',
    'movil': 'mobile',
    # Dalpiaz2020 specific
    'liga': 'league',
    'ligas': 'leagues',
    'partido': 'match',
    'partidos': 'matches',
    'jugador': 'player',
    'jugadores': 'players',
    'arbitro': 'referee',
    'arbitros': 'referees',
    'Arbitro': 'Referee',
    'entrenador': 'coach',
    'Entrenador': 'Coach',
    'aficionado': 'fan',
    'Aficionado': 'Fan',
    'marcador': 'score',
    'Marcador': 'Score',
    'clasificacion': 'standings',
    'torneo': 'tournament',
    'torneos': 'tournaments',
    'campeonato': 'championship',
    'temporada': 'season',
    'inscripcion': 'registration',
    'ficha': 'card',
    'tarjeta': 'card',
    'sancion': 'sanction',
    'sanciones': 'sanctions',
    'calendario': 'calendar',
    'Calendario': 'Calendar',
    'convocatoria': 'call',
    'Convocatoria': 'Call',
    'vehiculo': 'vehicle',
    'vehiculos': 'vehicles',
    'Vehiculo': 'Vehicle',
    'semaforo': 'traffic_light',
    'semaforos': 'traffic_lights',
    'Semaforo': 'Traffic_Light',
    'calle': 'street',
    'calles': 'streets',
    'Calle': 'Street',
    'interseccion': 'intersection',
    'intersecciones': 'intersections',
    'Interseccion': 'Intersection',
    'simulacion': 'simulation',
    'Simulacion': 'Simulation',
    'trafico': 'traffic',
    'Trafico': 'Traffic',
    'receta': 'prescription',
    'recetas': 'prescriptions',
    'Receta': 'Prescription',
    'medicamento': 'medication',
    'medicamentos': 'medications',
    'dosis': 'dosage',
    'Dosis': 'Dosage',
    'diagnostico': 'diagnosis',
    'Diagnóstico': 'Diagnosis',
    'laboratorio': 'laboratory',
    'Laboratorio': 'Laboratory',
    'dispositivo': 'device',
    'dispositivos': 'devices',
    'Dispositivo': 'Device',
    'proveedor': 'provider',
    'Proveedor': 'Provider',
    'farmacia': 'pharmacy',
    'Farmacia': 'Pharmacy',
    'recepcionista': 'receptionist',
    'Recepcionista': 'Receptionist',
    'facturador': 'biller',
    'Facturador': 'Biller',
    'ejecutivo': 'executive',
    'Ejecutivo': 'Executive',
    'contador': 'accountant',
    'Contador': 'Accountant',
    'representante': 'representative',
    'Representante': 'Representative',
    'superusuario': 'superuser',
    'Superusuario': 'Superuser',
    'centro': 'center',
    'Centro': 'Center',
    'reciclaje': 'recycling',
    'RRHH': 'HR',
    'nuevas': 'new',
    'nuevos': 'new',
    'nueva': 'new',
    'nuevo': 'new',
    'registradas': 'registered',
    'respectivas': 'respective',
    'participacion': 'participation',
    'integridad': 'integrity',
    'comprobar': 'check',
    'Comprobar': 'Check',
    'fomentar': 'encourage',
    'Fomentar': 'Encourage',
    'agendar': 'schedule',
    'Agendar': 'Schedule',
    'solicitar': 'request',
    'Solicitar': 'Request',
    'emitir': 'issue',
    'Emitir': 'Issue',
    'cambiar': 'change',
    'Cambiar': 'Change',
    'duplicar': 'duplicate',
    'Duplicar': 'Duplicate',
    'desaprobar': 'disapprove',
    'Desaprobar': 'Disapprove',
    'modificar': 'modify',
    'Modify': 'Modify',
    'aprobar': 'approve',
    'Approve': 'Approve',
    'mantener': 'maintain',
    'Maintain': 'Maintain',
    'administrar': 'manage',
    'Administrar': 'Manage',
    'gestionar': 'manage',
    'Gestionar': 'Manage',
    'consultar': 'consult',
    'Consultar': 'Consult',
    'programar': 'schedule',
    'Programar': 'Schedule',
    # Common prepositions/articles that remain
    'de': 'of',
    'del': 'of the',
    'la': 'the',
    'las': 'the',
    'el': 'the',
    'los': 'the',
    'un': 'a',
    'una': 'a',
    'por': 'by',
    'para': 'for',
    'en': 'in',
    'con': 'with',
    'sobre': 'about',
    'al': 'to the',
    'a': 'to',
    'y': 'and',
    'o': 'or',
    'que': 'that',
    'su': 'their',
    'sus': 'their',
    'cada': 'each',
    'todos': 'all',
    'todas': 'all',
    'otro': 'other',
    'otra': 'other',
    'otros': 'others',
    'otras': 'others',
    'mismo': 'same',
    'misma': 'same',
    'como': 'as',
    'sin': 'without',
    'entre': 'between',
    'hasta': 'until',
    'desde': 'from',
    'según': 'according to',
    'durante': 'during',
}

# Full phrase replacements for use case names - these take priority over word-by-word
# Format: (Spanish phrase, English replacement)
PHRASE_MAP = [
    # Common patterns across multiple US entries
    ('reglas de validación', 'validation rules'),
    ('reglas de validacion', 'validation rules'),
    ('a la base', 'to the database'),
    ('de la base', 'from the database'),
    ('base de datos', 'database'),
    ('base de Data', 'database'),
    ('segunda ronda de edicion', 'second round of editing'),
    ('casos a logica de derivacion', 'cases to derivation logic'),
    ('actualización de recursos', 'resource update'),
    ('codigos SQL', 'SQL codes'),
    ('versiones de prueba', 'test versions'),
    ('derivación FABS', 'FABS derivation'),
    ('Report de pruebas', 'test report'),
    ('maquetas de Content', 'content mockups'),
    ('nombres de oficinas', 'office names'),
    ('File de muestra', 'sample file'),
    ('campos flexibles', 'flexible fields'),
    ('fecha y hora de actualización', 'update date and time'),
    ('detalles de envio', 'submission details'),
    ('periodos de envio', 'submission periods'),
    ('esquema v1.1', 'schema v1.1'),
    ('Data actualizados', 'updated data'),
    ('archivos FABS publicados', 'published FABS files'),
    ('archivos publicados por agencia', 'files published by agency'),
    ('archivos D', 'D files'),
    ('información de filas por publicar', 'information on rows to publish'),
    ('informacion sobre instalaciones', 'information about facilities'),
    ('historial de errores de un User', 'error history of a user'),
    ('panel de estadisticas', 'statistics dashboard'),
    ('tarifas de actividades', 'activity rates'),
    ('Data de la empresa', 'company data'),
    ('planificacion de rutas', 'route planning'),
    ('empleados de la empresa', 'company employees'),
    ('código postal', 'zip code'),
    ('codigo postal', 'zip code'),
    ('instalaciones cercanas', 'nearby facilities'),
    ('Schedule de recogida', 'pickup schedule'),
    ('tipos de reciclables', 'types of recyclables'),
    ('mapa de contenedores cercanos', 'map of nearby containers'),
    ('mapa de sitios de entregas especiales cercanos', 'map of nearby special delivery sites'),
    ('eventos de eliminacion segura cercanos', 'nearby safe disposal events'),
    ('historial medico', 'medical record'),
    ('Appointment medica', 'medical appointment'),
    ('motivo de visita', 'visit reason'),
    ('horarios disponibles', 'available schedules'),
    ('resultados de prueba', 'test results'),
    ('un File', 'a file'),
    ('hora de Appointment', 'appointment time'),
    ('estadisticas partidos', 'match statistics'),
    ('estadisticas jugadores', 'player statistics'),
    ('participacion respectivas ligas', 'participation in respective leagues'),
    ('nuevas ligas registradas', 'newly registered leagues'),
    ('nuevas ligas', 'new leagues'),
]


def translate_use_case_name(name: str) -> str:
    """Translate a use case name from Spanish to English."""
    result = name

    # Apply phrase replacements first (longer phrases first to avoid partial matches)
    for es_phrase, en_phrase in sorted(PHRASE_MAP, key=lambda x: -len(x[0])):
        result = result.replace(es_phrase, en_phrase)

    # Then do word-by-word for remaining Spanish words
    words = result.split()
    translated_words = []
    for word in words:
        # Check direct word map (case-sensitive first, then lowercase)
        if word in WORD_MAP:
            translated_words.append(WORD_MAP[word])
        elif word.lower() in WORD_MAP:
            translated_words.append(WORD_MAP[word.lower()])
        else:
            translated_words.append(word)

    result = ' '.join(translated_words)

    # Clean up: remove repeated articles and prepositions, capitalize first word
    result = re.sub(r'\bthe the\b', 'the', result)
    result = re.sub(r'\bof of\b', 'of', result)
    result = re.sub(r'\bto to\b', 'to', result)

    # Capitalize first letter
    if result:
        result = result[0].upper() + result[1:]

    return result


def translate_method_name(name: str) -> str:
    """Translate a method name (inside class definitions)."""
    # Methods look like: +method_name() or +attribute_name
    # Strip the + prefix and () suffix for translation
    prefix = ''
    suffix = ''
    clean = name
    if clean.startswith('+'):
        prefix = '+'
        clean = clean[1:]
    if clean.endswith('()'):
        suffix = '()'
        clean = clean[:-2]

    # Split on underscores and translate each part
    parts = clean.split('_')
    translated = []
    for part in parts:
        if part in WORD_MAP:
            translated.append(WORD_MAP[part])
        elif part.lower() in WORD_MAP:
            translated.append(WORD_MAP[part.lower()])
        else:
            translated.append(part)

    return prefix + '_'.join(translated) + suffix


def translate_actor_name(name: str) -> str:
    """Translate an actor name."""
    parts = name.split('_')
    translated = []
    for part in parts:
        if part in WORD_MAP:
            translated.append(WORD_MAP[part])
        elif part.lower() in WORD_MAP:
            translated.append(WORD_MAP[part.lower()])
        else:
            translated.append(part)
    return '_'.join(translated)


def process_puml_file(filepath: str) -> list:
    """Process a single .puml file and return list of (line_num, old_line, new_line) changes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    changes = []
    new_lines = []

    for i, line in enumerate(lines):
        original = line
        new_line = line

        # Match usecase declarations: usecase "Name" as ALIAS
        uc_match = re.search(r'(usecase\s+")(.*?)("\s+as\s+)', new_line)
        if uc_match:
            old_name = uc_match.group(2)
            new_name = translate_use_case_name(old_name)
            if new_name != old_name:
                new_line = new_line[:uc_match.start(2)] + new_name + new_line[uc_match.end(2):]

        # Match actor declarations: actor "Name" as ALIAS
        actor_match = re.search(r'(actor\s+")(.*?)("\s+as\s+)', new_line)
        if actor_match:
            old_name = actor_match.group(2)
            new_name = translate_actor_name(old_name)
            if new_name != old_name:
                new_line = new_line[:actor_match.start(2)] + new_name + new_line[actor_match.end(2):]

        # Match class attributes/methods: +something or +something()
        method_match = re.search(r'^(\s+)(\+\S+)\s*$', new_line)
        if method_match:
            old_method = method_match.group(2)
            new_method = translate_method_name(old_method)
            if new_method != old_method:
                new_line = method_match.group(1) + new_method + '\n'

        if new_line != original:
            changes.append((i + 1, original.rstrip(), new_line.rstrip()))

        new_lines.append(new_line)

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    return changes


def main():
    all_changes = {}
    total_changes = 0

    review_dir = os.path.abspath(REVIEW_DIR)
    puml_files = sorted([f for f in os.listdir(review_dir) if f.endswith('.puml')])

    for filename in puml_files:
        filepath = os.path.join(review_dir, filename)
        changes = process_puml_file(filepath)
        if changes:
            all_changes[filename] = changes
            total_changes += len(changes)

    # Print change log
    print("=" * 80)
    print("CHANGE LOG: Spanish -> English translations in .puml files")
    print("=" * 80)

    for filename in sorted(all_changes.keys()):
        changes = all_changes[filename]
        print(f"\n--- {filename} ({len(changes)} changes) ---")
        for line_num, old, new in changes:
            print(f"  L{line_num}:")
            print(f"    - {old}")
            print(f"    + {new}")

    print(f"\n{'=' * 80}")
    print(f"SUMMARY: {total_changes} total changes across {len(all_changes)} files")

    # Count unchanged files
    unchanged = len(puml_files) - len(all_changes)
    print(f"         {unchanged} files unchanged (already English or empty)")
    print(f"         {len(puml_files)} total .puml files processed")
    print("=" * 80)

    # Save log to file
    log_path = os.path.join(os.path.dirname(__file__), 'translation_changelog.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("CHANGE LOG: Spanish -> English translations in .puml files\n")
        f.write("=" * 80 + "\n")
        for filename in sorted(all_changes.keys()):
            changes = all_changes[filename]
            f.write(f"\n--- {filename} ({len(changes)} changes) ---\n")
            for line_num, old, new in changes:
                f.write(f"  L{line_num}:\n")
                f.write(f"    - {old}\n")
                f.write(f"    + {new}\n")
        f.write(f"\nSUMMARY: {total_changes} changes across {len(all_changes)} files\n")
    print(f"\nChange log saved to: {log_path}")


if __name__ == '__main__':
    main()
