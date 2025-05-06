import os
import xml.etree.ElementTree as ET
import pandas as pd

pasta_xml = 'C:\\XMLpy\\NFCe'
dados = []

for nome_arquivo in os.listdir(pasta_xml):
    if nome_arquivo.endswith('.xml'):
        caminho_arquivo = os.path.join(pasta_xml, nome_arquivo)
        
        if os.path.getsize(caminho_arquivo) == 0:
            print(f"ignora o arquivo {nome_arquivo}")
            continue
        
        try:
            tree = ET.parse(caminho_arquivo)
            root = tree.getroot()
            ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
            
            nNF = root.find('.//nfe:ide/nfe:nNF', ns).text
            dhEmi = root.find('.//nfe:ide/nfe:dhEmi', ns).text
            dhRecbto = root.find('.//nfe:protNFe/nfe:infProt/nfe:dhRecbto', ns).text
            serie = root.find('.//nfe:ide/nfe:serie', ns).text
            vPag = root.find('.//nfe:detPag/nfe:vPag', ns).text

            dados.append({
                'Arquivo': nome_arquivo,
                'nNF': nNF,
                'dhEmi': dhEmi,
                'dhRecbto': dhRecbto,
                'serie': serie,
                'vPag': vPag
                
            })

        except ET.ParseError:
            print(f"{nome_arquivo}")
        except AttributeError:
            print(f"{nome_arquivo}")

df = pd.DataFrame(dados)
df.to_excel('notas_fiscais.xlsx', index=False)
print("feito essa merda: notas_fiscais.xlsx")