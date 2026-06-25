# Contributing to Pragma

## Branch Naming

```
feature/<slug>    → Nuevas funcionalidades
fix/<slug>        → Correcciones de bugs
chore/<slug>      → Mantenimiento, tooling, dependencias
```

Usar kebab-case. Ej: `feature/turnos-whatsapp`, `fix/typo-hero`, `chore/update-deps`.

## Commits

Conventional Commits — ya en uso:

```
feat:       nueva funcionalidad
fix:        corrección de bug
chore:      tooling, config, dependencias
refactor:   cambio que no agrega funcionalidad ni corrige bugs
docs:       documentación
style:      formato, linting (sin cambio lógico)
perf:       optimización de rendimiento
```

Scope opcional: `feat(seo): add JSON-LD schema`, `fix(auth): handle 429 retry`.

## PR Process

```
feature/*  ──PR──▶  develop  ──PR──▶  master
```

1. Crear rama desde `develop` con prefijo correspondiente
2. Desarrollar y commiteaer siguiendo conventional commits
3. Abrir PR apuntando a `develop`
4. Squash & merge a `develop`
5. Una vez validado en develop, abrir PR a `master`
6. Merge a `master` = deploy

## Development Setup

```bash
pnpm install     # instalar dependencias
pnpm dev         # servidor de desarrollo
pnpm build       # build de producción
pnpm preview     # previsualizar build local
```

## Coding Standards

Ver `CLAUDE.md` en la raíz del proyecto — constitución técnica del proyecto.
Aplica a todo el equipo, sin excepción.
