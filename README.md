# Controlo Despesas HOME

Dashboard das despesas da Moradia Paulo & Teresa, gerada a partir da folha Google Sheets «Controlo Despesas HOME».

- `public/index.html` é a página servida pelo Vercel. Os dados estão cifrados (AES-256-GCM); só abrem com a palavra-passe.
- `tools/update.py` gera a página a partir de uma exportação `.xlsx` da folha: `DASH_PW=... python3 tools/update.py home.xlsx`.
- `tools/page.tpl.html` é o modelo da dashboard (sem dados); `tools/lock.html` é o ecrã de palavra-passe.

Uma tarefa agendada atualiza `public/index.html` todos os dias. Nunca fazer commit de dados em claro (`build/`, `.xlsx`).

## Reclassificação

O Paulo continua a escrever na folha as descrições e entidades no formato antigo («Ferro», «Cobertura», «MBrum Gouveia»…). A tarefa diária converte-as na classificação atual:

- `tools/classificacao.py` tem as regras (descrição antiga → capítulo do mapa de quantidades; nomes de entidades uniformizados).
- `python3 tools/reclassificar.py home.xlsx` lista as células B/C a reescrever na folha (o que a tarefa aplica com o conector Google Sheets), os avisos (descrições desconhecidas, faturas de cobertura ≥ 2000 € classificadas como telha) e os duplicados novos. Não escreve nada.
- `tools/update.py` aplica as mesmas regras ao gerar a dashboard, para a página ficar certa mesmo que a escrita na folha falhe.
- `tools/duplicados_aceites.json` guarda só impressões digitais (sem dados em claro) das repetições legítimas já conhecidas.
