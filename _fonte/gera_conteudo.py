#!/usr/bin/env python3
"""Gera os includes do site a partir dos YAML em `_fonte/`.

Fonte única de verdade:
    _fonte/programacao.yml  ->  _includes/_grade.md
    _fonte/palestrantes.yml ->  _includes/_palestrantes.md

Uso (a partir da pasta do site):
    python3 _fonte/gera_conteudo.py
    python3 _fonte/gera_conteudo.py --check  # falha se os includes estiverem desatualizados

O `--check` é o que roda no GitHub Actions: garante que ninguém editou o
markdown gerado à mão e esqueceu de atualizar o YAML.
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

import yaml

FONTE = Path(__file__).resolve().parent      # site/_fonte
AQUI = FONTE.parent                          # site/
INCLUDES = AQUI / "_includes"

AVISO = "<!-- GERADO POR _fonte/gera_conteudo.py — NÃO EDITE À MÃO. Edite _fonte/*.yml -->\n\n"


def esc(texto: str) -> str:
    """Escapa o texto preservando as tags <br> usadas nos YAML."""
    return html.escape(str(texto), quote=False).replace("&lt;br&gt;", "<br>")


# --------------------------------------------------------------------------- #
# Grade horária
# --------------------------------------------------------------------------- #
def gera_grade(dados: dict) -> str:
    dias = dados["dias"]
    linhas: list[str] = ['::: {.grade}', "<table>", "<thead><tr>", '<th class="hora"></th>']

    for dia in dias:
        linhas.append(f'<th>{esc(dia["id"])} · {esc(dia["semana"])}</th>')
    linhas += ["</tr></thead>", "<tbody>"]

    for faixa in dados["faixas"]:
        if "intervalo" in faixa:
            rotulo = esc(faixa["intervalo"])
            linhas.append(
                f'<tr class="intervalo"><td></td>'
                f'<td colspan="{len(dias)}">{rotulo}</td></tr>'
            )
            continue

        linhas.append("<tr>")
        linhas.append(f'<td class="hora">{esc(faixa["hora"])}</td>')

        blocos = faixa["blocos"]
        if len(blocos) != len(dias):
            raise SystemExit(
                f"Faixa {faixa['hora']!r}: {len(blocos)} blocos para {len(dias)} dias."
            )

        for bloco in blocos:
            classe = bloco.get("classe", "")
            titulo = bloco.get("titulo")
            if classe == "vazio" and not titulo:
                linhas.append('<td class="vazio"></td>')
                continue
            cls = f' class="{classe}"' if classe else ""
            conteudo = f"<strong>{esc(titulo)}</strong>" if titulo else ""
            if bloco.get("quem"):
                conteudo += f'<span class="quem">{esc(bloco["quem"])}</span>'
            linhas.append(f"<td{cls}>{conteudo}</td>")
        linhas.append("</tr>")

    linhas += ["</tbody>", "</table>", ":::", ""]
    return AVISO + "\n".join(linhas)


# --------------------------------------------------------------------------- #
# Palestrantes
# --------------------------------------------------------------------------- #
def gera_palestrantes(dados: dict) -> str:
    partes: list[str] = []

    for secao in dados["secoes"]:
        partes.append(f'## {secao["nome"]}\n')
        if secao.get("descricao"):
            partes.append(f'{secao["descricao"]}\n')

        for p in secao["pessoas"]:
            partes.append('::: {.pessoa}')
            partes.append(f'### {esc(p["nome"])} {{.unnumbered}}\n')
            partes.append(f'<span class="inst">{esc(p["inst"])}</span>\n')
            if p.get("sintese"):
                partes.append(f'{esc(p["sintese"])}\n')
            if p.get("tema"):
                partes.append(f'<p class="tema"><strong>Tema:</strong> {esc(p["tema"])}</p>')
            if p.get("quando"):
                partes.append(f'<p class="quando">{esc(p["quando"])}</p>')
            partes.append(":::\n")

    return AVISO + "\n".join(partes)


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="não escreve; falha se algum include estiver desatualizado")
    args = ap.parse_args()

    INCLUDES.mkdir(exist_ok=True)

    saidas = {
        INCLUDES / "_grade.md": gera_grade(
            yaml.safe_load((FONTE / "programacao.yml").read_text(encoding="utf-8"))
        ),
        INCLUDES / "_palestrantes.md": gera_palestrantes(
            yaml.safe_load((FONTE / "palestrantes.yml").read_text(encoding="utf-8"))
        ),
    }

    desatualizados = []
    for destino, conteudo in saidas.items():
        atual = destino.read_text(encoding="utf-8") if destino.exists() else None
        if atual == conteudo:
            print(f"= {destino.relative_to(AQUI)} (sem mudanças)")
            continue
        if args.check:
            desatualizados.append(destino.relative_to(AQUI))
            continue
        destino.write_text(conteudo, encoding="utf-8")
        print(f"+ {destino.relative_to(AQUI)}")

    if desatualizados:
        print("\nDesatualizados: " + ", ".join(str(d) for d in desatualizados))
        print("Rode `python3 gera_conteudo.py` e faça commit do resultado.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
