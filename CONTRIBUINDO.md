# Guia de Contribuição

Padrões adotados pela equipe no desenvolvimento da **Papelaria A3**.

## 1. Preparação do projeto

```bash
git clone https://github.com/anleaes/2026-2-UDWMJ-Quinta-Manha-FAPA-03-MVT.git
cd 2026-2-UDWMJ-Quinta-Manha-FAPA-03-MVT
conda create -n papelariaapp python=3.12 -y
conda activate papelariaapp
pip install -r requirements.txt
```

## 2. Nomenclaturas

| Elemento | Padrão | Exemplo |
|---|---|---|
| Classes e Models | `PascalCase` | `GrupoMaterial` |
| Apps Django | `snake_case` (plural) | `grupos_materiais` |
| Atributos e métodos | `snake_case` | `preco_venda`, `atualizar_grupo()` |
| Templates | `snake_case` | `grupo_material_form.html` |
| URLs | `kebab-case` | `/grupos-materiais/` |
| Branches | `feature/nome-do-app` | `feature/grupos-materiais` |

## 3. Branches

Cada app deve ser desenvolvido em uma **branch própria**, criada a partir da `main` atualizada.

```bash
git switch -c feature/nome-do-app
```

## 4. Commits

Utilize o padrão:

```text
tipo(nome-do-app): descricao da alteracao
```

| Tipo | Finalidade |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção |
| `refactor` | Refatoração |
| `docs` | Documentação |
| `chore` | Configuração ou manutenção |

Exemplo: `feat(grupos-materiais): cria model GrupoMaterial`

**Regra da A3:** mínimo de 4 commits para cada item desenvolvido (Models, Views, URLs e Templates) e pelo menos 2 pushes por branch.