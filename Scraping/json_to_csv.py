import json
import csv

with open('data.json', 'r') as f:
    row_data = json.load(f)

# jsonファイルから抽出したデータの配列を作る処理
# extracted_data = [] # [[index, commented_time, comment, is_emoticon],[],[]]
# for i in range(len(row_data['comments'])):
#     extracted_data.append([
#         i, 
#         row_data['comments'][i]['content_offset_seconds'],
#         row_data['comments'][i]['message']['body'],
#         'emoticons' in row_data['comments'][i]['message']
#     ])

with open('extracted_data.csv', 'a') as f:
    writer = csv.writer(f)
    for i in range(len(row_data['comments'])):
        writer.writerow([
            i, 
            row_data['comments'][i]['content_offset_seconds'],
            row_data['comments'][i]['message']['body'],
            'emoticons' in row_data['comments'][i]['message']
        ])
