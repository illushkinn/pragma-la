# CLAUDE.md — Constitución Técnica de Pragma
> Versión 1.0 | Mayo 2026
> Este documento es la fuente de verdad del proyecto. Se lee antes de escribir cualquier código.
> Es agnóstico al modelo de IA — aplica a cualquier LLM, agente o herramienta utilizada.

---

## 1. MISIÓN

Pragma construye infraestructura de software médico privada, auditable y soberana
para centros de salud en LATAM, comenzando por Oberá, Misiones, Argentina.

El médico hace de médico. El sistema hace el resto.

Este documento gobierna el **frontend** de Pragma y sus conexiones con el backend
administrado por Isaac (DevOps / Ciberseguridad). El frontend no inventa contratos
de API — los consume tal como Isaac los expone.

---

## 2. ROLES Y RESPONSABILIDADES

| Integrante | Rol | Autoridad |
|---|---|---|
| Illya | PM / Estrategia / Frontend Pragma | Aprueba specs y prioridades |
| Norberto | Arquitecto n8n / Automatizaciones | Aprueba workflows y pipelines |
| Carlos | Director Creativo / UI | Aprueba identidad visual |
| Isaac | DevOps / Ciberseguridad / Hardening | Aprueba infraestructura y seguridad |

**Regla:** ninguna decisión de infraestructura o seguridad se implementa sin aprobación de Isaac.

---

## 3. STACK TECNOLÓGICO

### Frontend (responsabilidad de Illya)
- Framework: a definir en spec.md de cada feature
- UI: componentes accesibles para adultos mayores — contraste alto, tipografía grande, flujo simple
- SEO: prioritario — usar SSG o SSR según el caso
- Performance: Core Web Vitals como criterio de aceptación
- NO agregar dependencias pesadas sin justificación en el spec

### Conexiones con el backend de Isaac
- Autenticación: consumir JWT de Keycloak — el frontend nunca gestiona sesiones propias
- Llamadas API: siempre sobre HTTPS / TLS 1.3 — nunca HTTP en ningún entorno
- Variables de entorno: declaradas en .env.example — nunca hardcodeadas
- CORS: configurado por Isaac — el frontend respeta lo que está permitido, no negocia
- Rate limiting: el frontend maneja errores 429 con retry y backoff exponencial
- Errores: el frontend nunca expone stack traces ni mensajes internos al usuario

### Backend (responsabilidad de Isaac — solo referencia)
- Base de datos: Supabase con RLS habilitado, región EU
- Automatizaciones: n8n (Norberto)
- Asistente de voz: VAPI
- Inferencia LLM: vLLM en producción

### Modelos de IA
- Agnóstico al modelo — se declara en cada spec.md, no aquí

---

## 4. CONSTRAINTS DE SEGURIDAD — ISAAC
> Estas constraints son NO NEGOCIABLES. Ningún agente, LLM o desarrollador puede ignorarlas.

### 4.1 Datos de pacientes
- Los datos de pacientes NUNCA salen del servidor propio
- NUNCA enviar datos clínicos a APIs externas sin anonimización previa
- NUNCA loggear datos sensibles (nombre, DNI, diagnóstico, obra social)
- NUNCA almacenar datos en región US — solo EU o Argentina

### 4.2 Autenticación y acceso
- Autenticación: JWT con Keycloak (OAuth2/OIDC) — no inventar sistemas propios
- MFA obligatorio para acceso administrativo
- MaxAuthTries SSH: 3
- PermitRootLogin: no — siempre
- Acceso por clave pública únicamente — nunca contraseña

### 4.3 Cifrado
- En reposo: LUKS2 para particiones, pgcrypto para columnas sensibles
- En tránsito: TLS 1.3 obligatorio entre todos los servicios
- Gestión de claves: HashiCorp Vault — nunca hardcodear secretos en el código
- NUNCA commitear .env con credenciales reales al repositorio

### 4.4 Contenedores Docker
- NUNCA ejecutar como root
- DOCKER_CONTENT_TRUST=1 siempre activo
- Filesystems read-only donde sea posible: --read-only
- Limitar capabilities: --cap-drop ALL
- Escanear imágenes con Trivy antes de deploy
- Usar Docker Secrets para contraseñas — nunca variables de entorno en producción

### 4.5 Red (OpenBSD — firewall perimetral)
- Arquitectura de red segmentada:

| Zona | Subred | Propósito |
|---|---|---|
| DMZ | 10.0.0.0/24 | Reverse proxy, WAF |
| Admin | 10.0.1.0/24 | Bastion, VPN WireGuard |
| Aplicación | 10.0.2.0/24 | API, RAG, Workers |
| Datos | 10.0.3.0/24 | PostgreSQL, Supabase, MinIO |
| GPU | 10.0.4.0/24 | Nodos de inferencia |
| Backup | 10.0.5.0/24 | BorgBackup offsite |

- PF (Packet Filter): block all por defecto, allow explícito
- Protección bruteforce activa en SSH
- Rate limiting: 30 req/min texto, 10 req/min imágenes

### 4.6 Cumplimiento legal
- Ley 25.326 (Argentina): datos personales de pacientes protegidos
- Registro ante AAIP y DPA obligatorio por cliente antes del go-live
- HIPAA y GDPR como referencia para buenas prácticas aunque no sean obligatorias
- Todas las respuestas de IA incluyen disclaimer: herramienta de apoyo, no reemplaza juicio médico

### 4.7 Auditoría
- Todo queda registrado: quién accedió, cuándo, qué hizo
- Monitoreo: Prometheus + Grafana (métricas), Loki (logs), Wazuh (SIEM)
- Score mínimo aceptable: Lynis + OpenSCAP > 85 CIS antes de producción
- Pentesting con Garak antes de cualquier deploy público

---

## 5. LO QUE NUNCA HACER

- NUNCA usar Supabase en región US con datos de pacientes
- NUNCA hardcodear API keys, tokens o contraseñas en el código
- NUNCA desplegar sin que Isaac apruebe la infraestructura
- NUNCA implementar autenticación propia — usar Keycloak
- NUNCA ignorar el RLS de Supabase — cada consultorio es un tenant aislado
- NUNCA hacer vibe coding en features que afecten datos clínicos
- NUNCA saltear la fase de Refinement (The Interview) en specs críticas
- NUNCA ejecutar contenedores como root en ningún entorno

---

## 6. CUÁNDO USAR SDD vs VIBE CODING

```
IF (archivos_afectados > 5) OR (requisitos_poco_claros == TRUE)
  → Usar SDD: escribir spec.md antes de cualquier código

IF (fix de un solo archivo) OR (prototipo desechable) OR (incidente en producción)
  → Vibe coding aceptable: moverse rápido, documentar después
```

---

## 7. WORKFLOW DE DESARROLLO

```
1. RESEARCH    → Investigar antes de escribir. Subagentes paralelos si aplica.
2. SPEC        → Escribir spec.md con: arquitectura ref, arquitectura actual,
                 plan de implementación, checklist.
                 Constraints > Requirements — ser explícito, no vago.
3. REFINEMENT  → "Leé este spec y preguntame todo lo que podría causar falla."
                 Resolver ambigüedad ANTES de codificar.
4. IMPLEMENTACIÓN → Tareas atómicas. Un subagente por dominio
                    (Database / API / Frontend). Contexto aislado por tarea.
```

**Regla de oro:** corregir en el spec cuesta 5 minutos. Corregir en producción cuesta 16 horas.

---

## 8. ESTRUCTURA DE ARCHIVOS ESPERADA

```
pragma/
├── CLAUDE.md          ← este archivo (la constitución)
├── specs/
│   └── [feature].spec.md   ← un spec por feature, se descarta al terminar
├── src/
├── tests/
├── .env.example       ← nunca .env real en el repo
└── docker-compose.yml
```

---

## 9. CRITERIOS DE ÉXITO — PILOTO OBERÁ

Un centro médico está "atendido" cuando:
- La secretaria opera sin llamar a pacientes manualmente
- El médico cierra el día sin pendientes administrativos
- El paciente de 3era edad puede interactuar por voz sin asistencia
- Los datos del centro no salen de la infraestructura propia
- El médico puede testimoniar el resultado en sus propias palabras

---

*"A great software project is shaped by extracting the ambiguity before writing the code."*
