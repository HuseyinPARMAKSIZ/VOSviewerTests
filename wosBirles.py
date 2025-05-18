def merge_vosviewer_files_skip_headers(files, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for idx, fname in enumerate(files):
            with open(fname, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

                # Sonundaki boş satırları temizle
                while lines and lines[-1].strip() == '':
                    lines.pop()

                # Sonundaki EF satırını temizle (son dosyada bırak)
                if idx < len(files) - 1:
                    while lines and lines[-1].strip() == 'EF':
                        lines.pop()

                # 2. ve 3. dosyalarda ilk 3 satırı çıkar (FN, VR, PT)
                if idx > 0:
                    # Kontrollü olarak sadece bu 3 satırı atıyoruz
                    # Eğer dosya daha kısa ise dikkat etmek gerekebilir
                    lines = lines[3:]  

                # Satırları yaz
                for line in lines:
                    outfile.write(line.rstrip() + '\n')

        # En sona tek boş satır bırak
        outfile.write('\n')

files = ['healthsecdig1.txt', 'healthsecdig2.txt', 'healthsecdig3.txt']
output = 'healthSecDig2906en.txt'

files1 = ['healthSecAi1.txt', 'healthSecAi2.txt']
output1 = 'healthSecAi1305en.txt'

files2 = ['healthSecDig2906en.txt', 'healthSecAi1305en.txt']
output2 = 'healthSecDigAi2906pl1305en.txt'
merge_vosviewer_files_skip_headers(files2, output2)
#merge_vosviewer_files_skip_headers(files1, output1)
#merge_vosviewer_files_skip_headers(files, output)
