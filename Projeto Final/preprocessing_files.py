import json, os

def generate_chunks(fragmentation):
    header = fragmentation.get('header', {})
    id_doc = header.get('code', {}).get('values', [None])[0] or str(fragmentation.get('documentId', ''))
    tipo_map = {'1': 'objetivo', '2': 'premissa', '3': 'procedimento_inicial'}
    chunks = []
    fragments = fragmentation.get('fragments', [])
    current_section_title = None
    i = 0
    while i < len(fragments):
        f = fragments[i]
        if f.get('type') == 'section':
            numeration = f.get('numeration', [])
            if len(numeration) == 1:
                sec_id = str(numeration[0])
                current_section_title = f.get('text', '').strip()
                tipo = tipo_map.get(sec_id, 'procedimento')
                if i+1 < len(fragments) and fragments[i+1].get('type') == 'paragraph':
                    p = fragments[i+1]
                    chunks.append({
                        "id_doc": id_doc,
                        "tipo": tipo,
                        "id_secao": sec_id,
                        "titulo_secao": current_section_title,
                        "texto": p.get('text', '').strip()
                    })
                    i += 2
                    continue
            elif len(numeration) >= 2:
                sec_id = str(numeration[0])
                numero_item = ".".join(str(n) for n in numeration)
                texto = f.get('text', '').strip()
                tipo = tipo_map.get(sec_id, 'procedimento')
                chunks.append({
                    "id_doc": id_doc,
                    "tipo": tipo,
                    "id_secao": sec_id,
                    "titulo_secao": current_section_title,
                    "numero_item": numero_item,
                    "texto": f"{numero_item} {texto}"
                })
        i += 1
    return chunks

arquivos = [
    "powerdoc/arquivo.json"
]

for arquivo in arquivos:
    with open(arquivo, 'r', encoding='utf-8') as f:
        frag = json.load(f)
    chunks = generate_chunks(frag)

    # Gera o nome do novo arquivo na pasta 'documentos'
    nome_arquivo = os.path.basename(arquivo)
    caminho_saida = os.path.join("documentos", nome_arquivo)

    # Cria a pasta 'documentos' se não existir
    os.makedirs("documentos", exist_ok=True)

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Gerados {len(chunks)} chunks em: {caminho_saida}")

