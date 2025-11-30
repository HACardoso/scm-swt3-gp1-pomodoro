# Relatório de Processos de Desenvolvimento

Este documento descreve a estratégia de branching adotada, os procedimentos de build e CI/CD, o modelo de versionamento (tags/releases) e o processo de gerenciamento de issues usado neste projeto.

# Estratégia de Branching

## Ramos principais:

- `main` (produção) e `develop` (integração).

## Feature branches:

- prefixo `feature/` seguido de resumo e, opcionalmente, número da issue — ex.: `feature/123-expense-calculator`.

- Hotfix branches:** prefixo `hotfix/` para correções críticas que precisam ir diretamente para produção — ex.: `hotfix/fix-calc-rounding`.

## Release branches (opcional):

- `release/x.y` quando queremos preparar uma versão para QA e correção de última hora.

## Políticas de merge:

Pull Requests (PRs) exigem revisão por pelo menos um revisor, execução bem-sucedida de CI (testes + lint) e aprovação antes do merge. Merges de `feature/*` vão para `develop`; merges para `main` são feitos a partir de `develop` (ou `hotfix/*` quando aplicável) e são acompanhados de tag de release.

## Convencionalidade:

Mensagens de commit seguem um padrão curto e descritivo; usar palavras-chave da issue no corpo do PR para rastreabilidade.

## Procedimentos de Build e CI/CD**

### Pipeline (CI) típico:

	- Instalação do ambiente: `pip install -r requirements.txt` ou criar ambiente virtual.
	- Linter/estática: rodar ferramentas como `flake8` / `pylint` (opcional).
	- Testes automatizados: `python -m unittest discover -v` (ou `python -m pytest` se adotado pytest).
	- Verificações adicionais: checagem de formatação (`black --check`) e análise estática (opcional).

### Gatilhos: 

Executar CI em cada push a `feature/*`, `develop` e em cada PR; branches protegidas (`main`, `develop`) exigem CI verde para merge.

### Build de imagem / artefato:

Quando a pipeline de CI para `main` é bem-sucedida (ou em `release/*`) gerar artefato (por exemplo, imagem Docker via `Dockerfile`) e armazenar em um registry (ex.: Docker Hub, Azure Container Registry, GitHub Container Registry).

### CD (deploy):

Ao criar uma release/tags em `main`, pipeline de CD é disparado para publicar a imagem e atualizar o ambiente de destino. Para stacks simples, pode-se usar `docker-compose` com a nova tag;
	- Exemplo de etapas de CD: build image -> push registry -> aplicar update (ssh/ansible/docker-compose pull + up) ou usar uma plataforma de orquestração.

### Segredos e configuração:

Variáveis sensíveis (ex.: `GOOGLE_MAPS_API_KEY`) devem ser guardadas em variáveis de ambiente nos secrets do provedor CI/CD (GitHub Actions Secrets, Azure Key Vault, etc.).

### Exemplo de comandos locais rápidos:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -v
docker build -t myapp:dev .
```

## Forma de Versionamento (tags, releases)

- Esquema: adotar Semantic Versioning (SemVer) — `vMAJOR.MINOR.PATCH`.
- Tags: usar tags anotadas para cada release (ex.: `git tag -a v1.2.0 -m "Release v1.2.0"`).
- Releases: criar uma Release no repositório (GitHub/GitLab) a partir da tag, incluindo changelog resumido e binaries/artefatos se aplicável.
- Fluxo de publicação: merge para `main` → tag de versão → pipeline de CI/CD que faz build e publica a imagem/artefato.
- Histórico/Changelog: manter um changelog conciso (manual ou gerado a partir de mensagens convencionais), idealmente agrupando mudanças por categoria (fix, feat, docs).

## Gerenciamento de Issues (ciclo de vida de um bug/feature)

- Criação: toda nova demanda (bug ou feature) começa com uma issue descrevendo objetivo, passos para reproduzir (se for bug), e critérios de aceitação.
- Triagem: time ou mantenedor avalia prioridade, severidade, e atribui labels (ex.: `bug`, `feature`, `urgent`, `low-priority`) e milestone se aplicável.
- Planejamento / Backlog: issues aprovadas entram no backlog; durante planejamento, mover para uma milestone/sprint ou marcar como prontas para desenvolvimento.
- Desenvolvimento:
	- Criar branch: `feature/<issue>-descrição` ou `hotfix/<issue>` conforme o caso.
	- Linkar branch/PR à issue (número no título/descrição) para rastreabilidade.
	- Implementar alterações com commits pequenos e atômicos, incluindo testes automatizados quando pertinente.
- Revisão: abrir PR e solicitar revisão de pelo menos um colega; CI deve passar antes da aprovação.
- QA / Validação: após merge em `develop` (ou `main` no caso de hotfix), a versão vai para um ambiente de QA ou staging para validação manual e testes de integração.
- Release e fechamento: depois de validado, a release é criada a partir de `develop` → `main` (ou diretamente de `hotfix`), tag publicada e a issue é fechada com referência à release.
- Feedback loop: se regressão ou novo bug é detectado, reabrir issue ou criar nova issue vinculada, priorizar e seguir o ciclo novamente.

# Boas práticas e automações sugeridas
- Automatizar: rodar CI em PRs, bloquear merges com CI falhando, usar templates de issues/PRs para padronizar descrições.
- Labels: padronizar um conjunto de labels (ex.: `bug`, `enhancement`, `documentation`, `help wanted`, `wontfix`) e regras de priorização.
- Templates: usar templates de PR/issue (ex.: checklist de PR com "tests added", "docs updated").
