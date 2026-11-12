#!/usr/bin/env python3
"""Lista as correções de classificação a fazer na folha «Controlo Despesas HOME».

Uso:  python3 tools/reclassificar.py caminho/para/home.xlsx > correcoes.json
Saída (JSON):
  correcoes  [{intervalo: "Tosco!C240", antes, depois}]  células Entidade (B) / Descrição (C) a reescrever
  avisos     [texto]  descrições desconhecidas ou escolhas a confirmar (não bloqueiam)
  duplicados [texto]  linhas repetidas (mesma folha, data, entidade, descrição e total) que não
                      constam de tools/duplicados_aceites.json; a rotina só as assinala, nunca apaga.
Não escreve nada: a tarefa diária aplica as correções com o conector Google Sheets.
"""
import sys, os, json, hashlib, collections, warnings
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classificacao import entidade, descricao
warnings.filterwarnings('ignore')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def chave_dup(folha, d, e, c, t):
    # só se guarda a impressão digital (sem dados em claro no repositório)
    return hashlib.sha256(f'{folha}|{d}|{e}|{c}|{t:.2f}'.encode()).hexdigest()[:16]

def analisar(xlsx):
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    folhas = [f for f in ('Tosco', 'Acabamentos', 'Projeto') if f in wb.sheetnames]
    linhas = {f: list(wb[f].iter_rows(values_only=True))[1:] for f in folhas}
    conhecidas = sorted({str(r[1]).strip() for L in linhas.values() for r in L if r[1]})
    corr, avisos, grupos = [], [], collections.defaultdict(list)
    for f in folhas:
        for i, r in enumerate(linhas[f]):
            n = i + 2
            if r[0] is None or not str(r[1] or '').strip(): continue
            e0, c0 = str(r[1]).strip(), str(r[2] or '').strip()
            tot = r[7] if isinstance(r[7], (int, float)) else 0
            e1 = entidade(e0, conhecidas)
            c1, av = descricao(f, e1, c0, tot)
            if e1 != r[1]: corr.append({'intervalo': f'{f}!B{n}', 'antes': r[1], 'depois': e1})
            if c1 != r[2]: corr.append({'intervalo': f'{f}!C{n}', 'antes': r[2], 'depois': c1})
            data = r[0].strftime('%d/%m/%Y') if hasattr(r[0], 'strftime') else str(r[0])
            if av: avisos.append(f'{f}, linha {n} ({data}, {e1}, «{c0}», {tot:.2f} €): {av}')
            grupos[chave_dup(f, data, e1, c1, tot)].append(f'{f}, linha {n} ({data}, {e1}, {c1}, {tot:.2f} €)')
    return corr, avisos, grupos

if __name__ == '__main__':
    corr, avisos, grupos = analisar(sys.argv[1])
    try: aceites = json.load(open(os.path.join(ROOT, 'tools', 'duplicados_aceites.json')))
    except FileNotFoundError: aceites = {}
    dup = []
    for k, L in grupos.items():
        if len(L) > aceites.get(k, 1): dup.append(' / '.join(L))
    print(json.dumps({'correcoes': corr, 'avisos': avisos, 'duplicados': dup}, ensure_ascii=False, indent=1))
