# coding: utf-8
"""Rebuild only the two-fluid heating evidence appendix, bibliography and PDF."""
import csv, hashlib, json, re, subprocess, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'specific problems/双流体加热问题'

def tex(value):
    escape = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    s = ''.join(escape.get(c, c) for c in str(value)).replace('−', '-').replace('′', "'").replace(',', ', ').replace(';', '; ')
    s = re.sub('[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ᵀ]+', lambda m: r'\textsuperscript{' + unicodedata.normalize('NFKC', m[0]).replace('−', '-') + '}', s)
    s = re.sub('[₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎]+', lambda m: r'\textsubscript{' + unicodedata.normalize('NFKC', m[0]).replace('−', '-') + '}', s)
    for char, command in {'∇':'nabla', '∝':'propto', '∫':'int', '≪':'ll', '≫':'gg', '≲':'lesssim', '≳':'gtrsim', '∥':'parallel', '⊥':'perp', '⏊':'perp'}.items():
        s = s.replace(char, r'\ensuremath{' + chr(92) + command + '}')
    return s

def main():
    records = json.loads((OUT / 'reading_notes/records.json').read_text())
    catalog = {r['key']: r for r in json.loads((ROOT / 'research/catalog.json').read_text())}
    lines = [r'\chapter{逐篇证据与数值实现档案}',
             '本附录将本专题采用的证据按问题次序列出。旧记录来自已有全文笔记，本轮定向复用不重复计数。新增两篇为电子闭合的观测检验，其中数值部分含混合模型；不能称为新增两次完整双流体模拟。',
             r'\input{batch_stats}']
    bib, rows = [], []
    fields = [('model','实际模型与问题'), ('parameters','参数、初边值与实现'), ('finding','求解得到什么'), ('limitation','成立条件与剩余缺口'), ('assessment','对Hall比较的意义')]
    for item in records:
        key, note = item['key'], item['note']
        p = catalog[key]
        assert (ROOT / p['local_pdf']).is_file(), key
        url = 'https://doi.org/' + p['doi'] if p.get('doi') else p['landing_urls'][0]
        lines += [r'\section{' + tex(key) + '：' + str(p['year']) + r'年}\label{paper:' + key + '}',
                  r'\textbf{' + tex(p['title']) + r'}\citep{' + key + '}',
                  r'\textsf{本轮状态：}' + ('新增全文核读' if item['new_full_read'] else '已有全文记录复用，不增加计数') + '。',
                  r'\textsf{核读范围：}' + tex(note['pages_read']) + r'\par\textsf{图式：}' + tex(note['figures_checked']),
                  r'\href{run:../../' + p['local_pdf'] + r'}{本地原文PDF}\quad\href{' + url + '}{DOI/版本入口}']
        for field, label in fields:
            lines += [r'\paragraph{' + label + '}' + tex(note[field])]
        entries = {'author': ' and '.join(tex(a) for a in p['authors']), 'title': '{' + tex(p['title']) + '}', 'year': p['year'], 'journal': tex(p.get('journal','')), 'doi': p.get('doi',''), 'url': url, 'note': r'文献键：\texttt{' + tex(key) + r'}；\hyperref[paper:' + key + r']{本报告证据档案}'}
        bib.append('@article{' + key + ',\n' + ',\n'.join('  ' + k + ' = {' + str(v) + '}' for k,v in entries.items() if v) + '\n}\n')
        rows.append(dict(key=key, new_full_read=item['new_full_read'], role=item['role'], doi=p.get('doi',''), local_pdf=p['local_pdf'], model=note['model'], finding=note['finding'], limitation=note['limitation'], figures=note['figures_checked']))
    lines += [r'\chapter{访问、版本及未核读线索}',
              'Ohia2012的MIT公开记录已取得，PDF入口返回HTTP 429；OSTI旧入口未返回匹配PDF。Ohia2015出版PDF入口返回403，网页只用于检索和追引，尚未完成原文图式核验；二者不计新全文，不作为本专题科学结论的直接证据。其模型能力仍不能仅由后继论文转述代替原文核读。',
              'Kaptanoglu2020勘误与TenBarge2019MMS正式PDF本轮访问仍未成功，沿用已读接收稿或arXiv版及已有正式网页差异记录。十三/二十矩相关会议摘要、Ohia学位论文和前序EoS原始推导保留为追引；不声称已读、已验证或已复算。',
              'Wetherton2019使用20页OSTI接收稿，后部含重复/放大图页；Wetherton2021使用23页OSTI接收稿。两篇均无文内附录。独立仪器论文、原始MMS数据及前序方法代码未在本轮完整重新分析。']
    (OUT / 'evidence_appendix.tex').write_text('\n\n'.join(lines))
    (OUT / 'references.bib').write_text('\n'.join(bib))
    with (OUT / 'evidence_matrix.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    new = [r for r in records if r['new_full_read']]
    (OUT / 'batch_stats.tex').write_text(f'本专题采用{len(records)}篇核读证据，其中{len(records)-len(new)}篇复用既有记录、{len(new)}篇新增核读；新增主版本共43个PDF物理页（含封面、参考文献及重复图页），全库144增至146篇。页面数量不等于独立研究数量。\n')
    subprocess.run(['latexmk', '-xelatex', '-interaction=nonstopmode', '-halt-on-error', 'report.tex'], cwd=OUT, check=True)
    print('built', OUT / 'report.pdf')

if __name__ == '__main__':
    main()
