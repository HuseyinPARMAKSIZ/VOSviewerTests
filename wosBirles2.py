import re
from collections import defaultdict

def parse_wos_file(file_path):
    """Web of Science formatındaki dosyayı ayrıştırır ve çalışmaları listeler."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Çalışmaları 'ER' ile ayır
    records = content.split('\nER\n')
    parsed_records = []

    for record in records:
        if not record.strip():
            continue
        record_dict = {}
        lines = record.strip().split('\n')
        current_field = None
        current_value = []

        for line in lines:
            if line.startswith('  '):  # Çok satırlı alanın devamı
                current_value.append(line.strip())
            elif line == 'EF':  # Dosya sonu
                continue
            else:
                if current_field and current_value:
                    record_dict[current_field] = '\n'.join(current_value)
                match = re.match(r'^(\w{2})\s+(.+)$', line)
                if match:
                    current_field, value = match.groups()
                    current_value = [value]
                else:
                    current_field = None
                    current_value = []

        if current_field and current_value:
            record_dict[current_field] = '\n'.join(current_value)
        parsed_records.append(record_dict)

    return parsed_records

def merge_records(records1, records2):
    """İki listedeki çalışmaları birleştirir, yinelenenleri DOI bazında kaldırır."""
    # DOI'ye göre indeksleme
    record_map = defaultdict(list)
    
    # Her iki listedeki kayıtları tara
    for record in records1 + records2:
        doi = record.get('DI', None)
        if not doi:  # DOI yoksa başlık ve yazar kombinasyonunu kullan
            doi = f"{record.get('TI', '')}_{record.get('AU', '')}_{record.get('PY', '')}"
        record_map[doi].append(record)

    merged_records = []
    
    for doi, records in record_map.items():
        if len(records) == 1:
            merged_records.append(records[0])
        else:
            # Yinelenen kayıtları birleştir
            merged = {}
            for record in records:
                for key, value in record.items():
                    if key not in merged:
                        merged[key] = value
                    elif merged[key] != value:
                        # Farklı değerler varsa, birleştir (örneğin, C1 veya CR)
                        if key in ['C1', 'CR', 'DE', 'ID', 'C3']:
                            merged[key] = f"{merged[key]}\n{value}"
                        else:
                            merged[key] = value  # Son değeri koru
            merged_records.append(merged)

    return merged_records

def write_wos_file(records, output_path):
    """Birleştirilmiş kayıtları Web of Science formatında dosyaya yazar."""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("FN Clarivate Analytics Web of Science\n")
        file.write("VR 1.0\n\n")

        for record in records:
            for field in ['PT', 'AU', 'AF', 'TI', 'SO', 'LA', 'DT', 'DE', 'ID', 'AB', 'C1', 'C3', 'RP', 'EM', 'RI', 'OI', 'FU', 'FX', 'CR', 'NR', 'TC', 'Z9', 'U1', 'U2', 'PU', 'PI', 'PA', 'SN', 'EI', 'BN', 'J9', 'JI', 'PD', 'PY', 'VL', 'IS', 'BP', 'EP', 'AR', 'DI', 'EA', 'PG', 'WC', 'WE', 'SC', 'GA', 'UT', 'PM', 'OA', 'DA']:
                if field in record and record[field]:
                    value = record[field]
                    # Çok satırlı alanlar için formatlama
                    if '\n' in value:
                        lines = value.split('\n')
                        file.write(f"{field} {lines[0]}\n")
                        for line in lines[1:]:
                            file.write(f"   {line}\n")
                    else:
                        file.write(f"{field} {value}\n")
            file.write("ER\n\n")
        file.write("EF\n")

def main():
    # Dosya yollarını belirtin
    file1_path = "healthSecAi1305en.txt"
    file2_path = "healthSecDig2906en.txt"
    output_path = "merged_wos_output.txt"

    # Dosyaları ayrıştır
    records1 = parse_wos_file(file1_path)
    records2 = parse_wos_file(file2_path)

    # Kayıtları birleştir
    merged_records = merge_records(records1, records2)

    # Çıktıyı dosyaya yaz
    write_wos_file(merged_records, output_path)
    print(f"Birleştirilmiş kayıtlar {output_path} dosyasına yazıldı.")

if __name__ == "__main__":
    main()
