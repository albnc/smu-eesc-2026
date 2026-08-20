# Site do Simpósio de Mobilidade Urbana

Site Quarto do **Simpósio de Mobilidade Urbana: Modelagem de Tráfego para Cidades Inteligentes e Conectadas** (8 a 11 de setembro de 2026, EESC-USP, São Carlos-SP), publicado no GitHub Pages.

## Estrutura

```
site/
├── _quarto.yml            configuração do site (navbar, rodapé, Open Graph)
├── custom.scss            tema — paleta da arte final do simpósio
├── index.qmd              banner, o evento, público, quando e onde
├── programacao.qmd        grade horária + downloads
├── palestrantes.qmd       sínteses dos convidados
├── materiais.qmd          inscrição, PDFs e material das sessões
├── _fonte/                FONTE ÚNICA de conteúdo estruturado
│   ├── programacao.yml    grade horária
│   ├── palestrantes.yml   sínteses
│   └── gera_conteudo.py   gera os includes a partir dos YAML
├── _includes/             markdown GERADO — não editar à mão
├── images/                banner, grade em PNG, logos
└── materiais/             PDFs e artes para download
```

Pastas com `_` na frente são ignoradas pelo Quarto: não vão para o site publicado.

## Fluxo de trabalho

**Mudou a grade ou uma síntese?** Edite o YAML em `_fonte/`, regenere e renderize:

```bash
cd _proposta/Seminario-CNPq/site
python3 _fonte/gera_conteudo.py    # requer pyyaml
quarto preview                     # visualiza com recarga automática
```

Nunca edite `_includes/_grade.md` nem `_includes/_palestrantes.md` — eles são sobrescritos. O `gera_conteudo.py --check` roda no GitHub Actions e **falha o build** se os includes estiverem fora de sincronia com os YAML: é a trava que impede o site publicado de divergir da fonte.

**Vai publicar um material?** Coloque o arquivo em `materiais/` e troque a linha `<span class="tipo breve">Em breve</span>` correspondente, em `materiais.qmd`, por um link.

## Publicação

O workflow [`.github/workflows/simposio-site.yml`](../../../.github/workflows/simposio-site.yml) renderiza e publica automaticamente a cada push na `main` que toque esta pasta.

**Ativação (uma vez só):** no GitHub, `Settings → Pages → Build and deployment → Source: GitHub Actions`. Depois, o primeiro push publica o site em `https://albnc.github.io/claudeverse/`.

> **Repositório privado.** O GitHub Pages a partir de repositório privado exige plano pago (Pro/Team/Enterprise). Se o `claudeverse` for privado e o plano for gratuito, a alternativa é criar um repositório público só para o simpósio e apontar o workflow para ele — o conteúdo do site não muda.

Para publicar manualmente, sem Actions:

```bash
quarto render                        # gera _site/
quarto publish gh-pages              # publica na branch gh-pages
```

## Ajustes pendentes antes de divulgar

- **Sínteses dos palestrantes** (`_fonte/palestrantes.yml`) foram redigidas a partir das cartas-convite e da programação. Confirmar títulos, vínculos e recorte de pesquisa com cada convidado.
- **Vínculo de Flávio Vaz**: a carta-convite (`_out/03_carta_flavio-vaz.md`) traz EESC-USP; o flier `arte_final/Flier Simposio Mobilidade-programa.png` traz EPUSP. O site segue a carta. Definir qual está correto e alinhar as duas peças.
- **Instituições de Thiago Louro e Lucas Assis** não constavam da proposta; o site as registra como EESC-USP, seguindo o flier. Confirmar.
- **`site-url`** em `_quarto.yml` precisa bater com a URL final — é o que o Open Graph usa nas prévias de link do WhatsApp e do LinkedIn.
- **Local exato** (auditório/sala) e informações de hospedagem e deslocamento em São Carlos ainda não constam do site.
- **Marca do CNPq**: item 3.2 do Termo de Outorga pede consulta prévia à comunicação social do CNPq (comunicacao@cnpq.br) sobre os padrões de aplicação.
