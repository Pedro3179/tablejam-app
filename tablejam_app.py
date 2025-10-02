import re, time

while True:
    text_origin=input('Enter the original text (file.extesion):')
    text_trans=input('Enter the translation (file.extesion):')

    try:
        fhandle_origin=open(text_origin, encoding='utf-8-sig')
        fhandle_trans=open(text_trans, encoding='utf-8-sig')
        original=fhandle_origin.read()
        translation=fhandle_trans.read()
    except:
        print('Error: Wrong file format. Try again a file.srt.\n')
        continue
    break  
    

#print(f'Content: {original}')

def search_begin(str_val):
    return re.search(r'^[1-9]\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n', str_val)

# Check if file format is OK.
## Remember to alter this code to support more formats
if not (search_begin(original) and search_begin(translation)):
    print('Error: corrupted file. Try a supported file format.')
    time.sleep(4)
    exit()
#print('OK.')

# Create the columns in table.csv the file
fhandle_table=open('table.csv', "w")
fhandle_table.write('ORIGINAL;TRANSLATION\n')

origin_lst=re.findall(r'(\d+)\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n(.+\n.*)\n', original)
#print('Origin=',origin_lst)
# Repeat the process with translation (maybe create a dict)
trans_lst=re.findall(r'(\d+)\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n(.+\n.*)\n', translation)


# If Subtitle number of original and translation are the same, then they are written in the csv file
for origin_id, o in origin_lst:
    for trans_id, t in trans_lst:
        if origin_id==trans_id:
            o=o.replace('\n',' ')
            t=t.replace('\n',' ')
            fhandle_table.write(f'{o};')
            fhandle_table.write(f'{t}\n')



#print('Original=', subt_list)

#print(len(subt_list))

fhandle_table.close