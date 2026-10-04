# Controlo Despesas HOME

Dashboard das despesas da Moradia Paulo & Teresa, gerada a partir da folha Google Sheets «Controlo Despesas HOME».

- `public/index.html` é a página servida pelo Vercel. Os dados estão cifrados (AES-256-GCM); só abrem com a palavra-passe.
- `tools/update.py` gera a página a partir de uma exportação `.xlsx` da folha: `DASH_PW=... python3 tools/update.py home.xlsx`.
- `tools/page.tpl.html` é o modelo da dashboard (sem dados); `tools/lock.html` é o ecrã de palavra-passe.

Uma tarefa agendada atualiza `public/index.html` todos os dias. Nunca fazer commit de dados em claro (`build/`, `.xlsx`).
