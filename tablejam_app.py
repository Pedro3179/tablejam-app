import re, time

def search_begin(str_val):
    return re.search(r'^[1-9]\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n', str_val)

def parse_sub(str_val):
    return re.findall(r'(\d+)\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n(.+\n.*)\n', str_val)


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

# Check if file format is OK.
## Remember to alter this code to support more formats
if not (search_begin(original) and search_begin(translation)):
    print('Error: corrupted file. Try a supported file format.')
    time.sleep(4)
    exit()
#print('OK.')

# Create the columns in table.csv
fhandle_table=open('table.csv', "w")
fhandle_table.write('ORIGINAL;TRANSLATION\n')

# Make a list to store original the original subtitles
origin_lst=parse_sub(original)
print(len(origin_lst))

# Repeat the process with translation
trans_lst=parse_sub(translation)
print(len(trans_lst))

# If subtitle id of original and translation are the same, they are written in the csv file
for origin_id, o in origin_lst:
    for trans_id, t in trans_lst:
        if origin_id==trans_id:
            o=o.replace('\n',' ').replace(';',',') #Remove \n and ; as this can cause problems in the csv
            t=t.replace('\n',' ').replace(';',',')
            fhandle_table.write(f'{o};')
            fhandle_table.write(f'{t}\n')

fhandle_table.close