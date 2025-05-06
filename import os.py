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

            #Here the XML XPath is out of alignment, since in our national XML, used in invoices, there can be more than one piece of data in the field, so we have to group them.
            vPag = sum(float(elem.text) for elem in root.findall('.//nfe:detPag/nfe:vPag', ns))

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
            
        #Here, we need to add another exception of error.
        except Exception as e:
            print(f"{nome_arquivo}: {e}")

df = pd.DataFrame(dados)
df.to_excel('notas_fiscais.xlsx', index=False)
print("feito essa merda: notas_fiscais.xlsx")
