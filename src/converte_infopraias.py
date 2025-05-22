import csv
from dbfread import DBF
import argparse
import os

def dbf_to_csv(dbf_path, csv_path=None, encoding='utf-8'):
    """
    Convert a DBF file to a CSV file.
    
    Args:
        dbf_path (str): Path to the input DBF file
        csv_path (str): Path to the output CSV file (optional)
        encoding (str): Character encoding for the output CSV
    """
    # If no output path is specified, create one with the same name as the input
    if csv_path is None:
        base_name = os.path.splitext(dbf_path)[0]
        csv_path = f"{base_name}.csv"
    
    # Read the DBF file
    try:
        table = DBF(dbf_path, encoding=encoding)
    except Exception as e:
        print(f"Error reading DBF file: {e}")
        return False
    
    # Write to CSV file
    try:
        with open(csv_path, 'w', newline='', encoding=encoding) as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            writer.writerow([
                'Código da Praia',   
                'Nome da Praia',
                'Região',
                'Concelho',
                'Categoria',
                'Qualidade da água',
                'Vigilancia',
                'Posto de socorro', 
                'Sanitarios',
                'Duche',
                'Recolha lixo',
                'Limpeza praia',
                'Painel informativo',
                'Apoio balnear',
                'Apoio à praia',
                'Estacionamento',
                'Bandeira Azul',
                'Acessível',
                'Cadeira anfíbia',
                'Ondas especiais',
                'Obras em curso',
                'Risco de derrocada'
                ])
            # Write records
            for record in table:

                
                regiao_text = record.get('arh')

                writer.writerow([
                    record.get('codigo_pra'),
                    record.get('nome_praia'),
                    regiao_text.replace("ARH-", ""),
                    record.get('concelho'),
                    'Praia Costeira' if record.get('categoria_') == 1 else 'Praia Interior',
                    record.get('qualidade_'),
                    'Sim' if record.get('vigilancia') == 1 else 'Não',
                    'Sim' if record.get('posto_soco') == 1 else 'Não',
                    'Sim' if record.get('sanitarios') == 1 else 'Não',
                    'Sim' if record.get('duche') == 1 else 'Não',
                    'Sim' if record.get('recolha_li') == 1 else 'Não',
                    'Sim' if record.get('limpeza_pr') == 1 else 'Não',
                    'Sim' if record.get('painel_inf') == 1 else 'Não',
                    'Sim' if record.get('apoio_baln') == 1 else 'Não',
                    'Sim' if record.get('apoio_prai') == 1 else 'Não',
                    'Sim' if record.get('estacionam') == 1 else 'Não',
                    'Sim' if record.get('bandeira_a') == 1 else 'Não',
                    'Sim' if record.get('acessivel') == 1 else 'Não',
                    'Sim' if record.get('cadeira_an') == 1 else 'Não',
                    'Sim' if record.get('ondas_espe') == 1 else 'Não',
                    'Sim' if record.get('obras_em_c') == 1 else 'Não',
                    'Sim' if record.get('risco_derr') == 1 else 'Não',
                    ])
        
        print(f"Successfully converted {dbf_path} to {csv_path}")
        return True
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        return False

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Convert DBF to CSV')
    parser.add_argument('input', help='Input DBF file path')
    parser.add_argument('-o', '--output', help='Output CSV file path (optional)')
    parser.add_argument('-e', '--encoding', default='utf-8',
                        help='Character encoding (default: utf-8)')
    
    args = parser.parse_args()
    
    # Perform conversion
    dbf_to_csv(args.input, args.output, args.encoding)