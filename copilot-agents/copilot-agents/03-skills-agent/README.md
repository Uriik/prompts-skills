# Skills Agent - Guide

## O que faz?

Cria **SKILLS** reutilizáveis para seu projeto (/testing, /debug, /review, etc)

Skills são tarefas bem-definidas que podem ser ativadas automaticamente ou manualmente.

## Arquivos nesta pasta

- `agente-skills.md` - O agente completo com fluxo passo-a-passo
- `TEMPLATE-skill.md` - Template vazio para você preencher
- Pastas de exemplo com skills prontas:
  - `skill-testing/SKILL.md` - Skill para criar testes
  - `skill-debugging/SKILL.md` - Skill para debugar issues

## Como usar?

1. Abra `agente-skills.md`
2. Descreva a tarefa que a skill automatizará
3. Ele gera SKILL.md com 8 seções essenciais
4. Ele cria estrutura de pastas (scripts/, templates/)
5. Copie tudo para `.github/skills/sua-skill/`
6. Use via `/testing`, `/debug`, ou automático

## Estrutura de Pastas

```
.github/skills/sua-skill/
├── SKILL.md              (documentação principal)
├── scripts/
│   ├── run-tests.sh      (automação)
│   └── validate.sh
└── templates/
    ├── test-template.ts  (snippets)
    └── structure.json
```

## Seções que serão criadas

1. Overview
2. When to Use This Skill
3. Step-by-Step Process
4. Code Templates
5. Best Practices
6. Troubleshooting
7. References
8. (Opcional) Related Skills

## Exemplos

- `skill-testing/SKILL.md` - Cria testes com Jest e React Testing Library
- `skill-debugging/SKILL.md` - Debuga issues com logs e DevTools

Copie esses exemplos para adaptar suas próprias skills!

## Tempo estimado

15-20 minutos por skill (maior que outros)

## Token cost

5-10 discovery + 250 se ativada (~150 quando matched automaticamente)

---

Para voltar ao overview, veja `../README.md`
