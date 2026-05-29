# Pragma

**Infraestructura de software médico privada, auditable y soberana.**  
El médico hace de médico. El sistema hace el resto.

Construimos el sistema operativo digital para centros de salud en LATAM, arrancando por Oberá, Misiones.

## Stack

| Capa | Tecnología |
|------|-----------|
| Frontend | A definir por feature — SSG/SSR según caso |
| Backend | Supabase (RLS, región EU) + n8n + vLLM |
| Auth | Keycloak (JWT, OAuth2/OIDC) |
| Voz | VAPI + Twilio |
| Infra | OpenBSD + Docker con hardening |

## Equipo

| Quién | Hace |
|-------|------|
| **Illya** | PM, estrategia, frontend |
| **Norberto** | n8n, automatizaciones |
| **Carlos** | Dirección creativa, UI |
| **Isaac** | DevOps, ciberseguridad, hardening |

## Arrancar

```bash
git clone https://github.com/illushkinn/pragma-la.git
cd pragma
```

No hay package manager definido todavía — el framework frontend se define por feature en cada spec.

## Desarrollo

Usamos **Spec-Driven Development** (SDD). Antes de escribir código:

1. `specs/[feature].spec.md` — spec con arquitectura, plan y checklist
2. Refinement — resolver ambigüedad antes de codificar
3. Implementación — tareas atómicas, un subagente por dominio

Ver `CLAUDE.md` para la constitución técnica completa.

## Seguridad

- `ignore-scripts=true` en `.npmrc` — [fundamento](https://www.nodejs-security.com/blog/npm-ignore-scripts-best-practices-as-security-mitigation-for-malicious-packages)
- Datos de pacientes nunca salen del servidor propio
- Región EU o Argentina — nunca US
- Sin autenticación propia — Keycloak

## Links

- [GitHub](https://github.com/illushkinn/pragma-la)
- [Vercel](https://pragma-gules.vercel.app)

---

*Oberá, Misiones — Argentina*
