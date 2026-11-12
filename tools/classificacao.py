"""Classificação das descrições e nomes das entidades da folha «Controlo Despesas HOME».

O Paulo continua a escrever na folha as descrições e entidades no formato antigo
(«Ferro», «Cobertura», «MBrum Gouveia», ...). Este módulo converte-as na
classificação por capítulo do mapa de quantidades adotada em 09/11/2026 e nos nomes
uniformizados de 10/11/2026. É usado por:
  tools/reclassificar.py  -> lista as células a corrigir na própria folha
  tools/update.py         -> aplica a mesma conversão ao gerar a dashboard (rede de segurança)
"""
import re, unicodedata

# Descrições novas (classificação atual). Uma descrição nesta lista nunca é alterada.
NOVAS = [
    'Mão de obra', 'Diversos',
    'Cobertura – Estrutura de madeira', 'Cobertura – Revestimento (telha)',
    'Cobertura – Acessórios e remates', 'Cobertura – Mão de obra',
    'Movimento de terras – Escavação', 'Movimento de terras – Aterro e enrocamento',
    'Estrutura – Betão', 'Estrutura – Armaduras de aço', 'Estrutura – Cofragem',
    'Alvenarias – Blocos', 'Revestimentos – Reboco', 'Revestimentos – ETICS',
    'Impermeabilizações', 'Caixilharias exteriores', 'Cantarias – Soleiras e peitoris',
    'Redes de águas e esgotos', 'Redes de águas e esgotos – Drenagem', 'Instalações elétricas',
    'Materiais – Cimento', 'Materiais – Areia', 'Materiais – Brita', 'Materiais – Diversos',
    'Estaleiro – Aluguer de equipamento', 'Estaleiro – Segurança', 'Estaleiro – Transportes',
    'Estaleiro – Implantação topográfica', 'Estaleiro – Quadro elétrico de obra',
    'Terreno – Aquisição', 'Terreno – Escritura e registos',
    'Projetos – Arquitetura e especialidades', 'Projetos – Levantamento topográfico',
    'Direção técnica de obra', 'Licenciamento – Taxas e certidões',
    'Segurança e saúde (PSS) e gestão de resíduos',
    'Ligações às redes – Água', 'Ligações às redes – Eletricidade',
    'Financiamento – Vistoria bancária',
]

# Descrição antiga -> nova, válida em qualquer folha (chave em minúsculas).
DESC = {
    'aluguer': 'Estaleiro – Aluguer de equipamento',
    'areia': 'Materiais – Areia',
    'armação': 'Cobertura – Estrutura de madeira',
    'bagacina': 'Movimento de terras – Aterro e enrocamento',
    'betão': 'Estrutura – Betão',
    'blocos': 'Alvenarias – Blocos',
    'brita': 'Materiais – Brita',
    'caixilharias': 'Caixilharias exteriores',
    'canalizações': 'Redes de águas e esgotos',
    'carpintaria': 'Cobertura – Mão de obra',
    'cimento': 'Materiais – Cimento',
    'cofragem': 'Estrutura – Cofragem',
    'etics': 'Revestimentos – ETICS',
    'eletricidade': 'Instalações elétricas',
    'escavações': 'Movimento de terras – Escavação',
    'ferro': 'Estrutura – Armaduras de aço',
    'impermebialização': 'Impermeabilizações',
    'impermeabilização': 'Impermeabilizações',
    'manilhas': 'Redes de águas e esgotos – Drenagem',
    'materiais': 'Materiais – Diversos',
    'mão de obra': 'Mão de obra',
    'reboco': 'Revestimentos – Reboco',
    'segurança': 'Estaleiro – Segurança',
    'soleiras': 'Cantarias – Soleiras e peitoris',
    'transporte': 'Estaleiro – Transportes',
    'transportes': 'Estaleiro – Transportes',
    'diversos': 'Diversos',
    # típicas da folha Projeto
    'abertura de ramal': 'Ligações às redes – Água',
    'arquitetura': 'Projetos – Arquitetura e especialidades',
    'certidão permanente': 'Terreno – Escritura e registos',
    'certidão de nº': 'Licenciamento – Taxas e certidões',
    'confrontações': 'Projetos – Levantamento topográfico',
    'direção de obra': 'Direção técnica de obra',
    'documentação': 'Licenciamento – Taxas e certidões',
    'escritura': 'Terreno – Escritura e registos',
    'fornecimento eletricidade': 'Ligações às redes – Eletricidade',
    'licença': 'Licenciamento – Taxas e certidões',
    'livro de obra': 'Licenciamento – Taxas e certidões',
    'parecer águas': 'Licenciamento – Taxas e certidões',
    'placa licenciamento': 'Licenciamento – Taxas e certidões',
    'plástico': 'Diversos',
    'pss & gr': 'Segurança e saúde (PSS) e gestão de resíduos',
    'quadro obra': 'Estaleiro – Quadro elétrico de obra',
    'terreno': 'Terreno – Aquisição',
    'vistoria de imóveis': 'Financiamento – Vistoria bancária',
}

# Nomes de entidades: forma normalizada (sem acentos, pontuação nem espaços) -> nome uniformizado.
ENT_CANON = [
    'Albano Vieira, Lda.', 'Câmara Municipal do Nordeste', 'Carlos Vieira – Centro de Cópias',
    'Electrorequetim', 'Kaspar, Lda.', 'Leroy Merlin', 'Mariano Brum Gouveia, Lda.',
    'Marques Britas, S.A.', 'Serralharia Outeiro, Lda.', 'Soledade & Filhos', 'Vieiras, Lda.',
]
def chave(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9&]', '', s)
ENT = {chave(n): n for n in ENT_CANON}
ENT.update({chave(k): v for k, v in {
    'Albano Vieira': 'Albano Vieira, Lda.',
    'CMNordeste': 'Câmara Municipal do Nordeste', 'CM Nordeste': 'Câmara Municipal do Nordeste',
    'Electorequetim': 'Electrorequetim',
    'MBrum Gouveia': 'Mariano Brum Gouveia, Lda.', 'Mariano Brum Gouveia': 'Mariano Brum Gouveia, Lda.',
    'Marques Britas': 'Marques Britas, S.A.',
    'Kaspar': 'Kaspar, Lda.', 'Serralharia Outeiro': 'Serralharia Outeiro, Lda.',
    'Vieiras': 'Vieiras, Lda.',
}.items()})

MAO_DE_OBRA = {chave('Hélder Silva')}  # quem fatura mão de obra

def entidade(nome, conhecidas=()):
    """Nome uniformizado; também acerta maiúsculas/minúsculas contra entidades já na folha."""
    s = str(nome or '').strip()
    k = chave(s)
    if k in ENT: return ENT[k]
    for c in conhecidas:
        if chave(c) == k: return c
    return s

def descricao(folha, ent, desc, total=0):
    """Devolve (nova_descrição, aviso). aviso != None quando a escolha deve ser confirmada."""
    s = str(desc or '').strip()
    if s in NOVAS: return s, None
    k = s.lower()
    for n in NOVAS:  # já nova, mas com maiúsculas ou espaços diferentes
        if n.lower() == k: return n, None
    mo = chave(ent) in MAO_DE_OBRA
    if k == 'cobertura':
        if mo: return 'Cobertura – Mão de obra', None
        if abs(total or 0) >= 2000:  # as faturas grandes de cobertura foram a telha
            return 'Cobertura – Revestimento (telha)', 'valor elevado: classificada como telha; confirmar'
        return 'Cobertura – Acessórios e remates', None
    if k == 'madeira':
        return ('Cobertura – Mão de obra' if mo else 'Estrutura – Cofragem'), None
    if k == 'topografia':
        return ('Projetos – Levantamento topográfico' if folha == 'Projeto' else 'Estaleiro – Implantação topográfica'), None
    if k in DESC: return DESC[k], None
    return s, 'descrição desconhecida: não foi reclassificada'
