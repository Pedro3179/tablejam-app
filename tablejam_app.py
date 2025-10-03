import re, time

def start_search(str_val):
    return re.search(r'^[1-9]\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n', str_val)

def parse_sub(str_val):
    return re.findall(r'(\d+)\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n(.+\n.*)\n', str_val)

# Ask for input
while True:
    text_origin=input('Enter the original text (file.extesion):')
    text_trans=input('Enter the translation (file.extesion):')

# Read the file and check for wrong formats and encoding errors.    
    try:
        fhandle_origin=open(text_origin, encoding='utf-8-sig')
        original=fhandle_origin.read()
    except:
        try:
            fhandle_origin=open(text_origin, encoding='cp1252')
            original=fhandle_origin.read()
        except:
            print('Error: Original wrong file format or encoding. Try again with a valid file.\n')
            continue
    try:
        fhandle_trans=open(text_trans, encoding='utf-8-sig')
        translation=fhandle_trans.read()
    except:
            try:
                fhandle_trans=open(text_trans, encoding='cp1252')
                translation=fhandle_trans.read()
            except:
                print('Error: Translation wrong file format or encoding. Try again with a valid file.\n')
                continue
    break  
    
#print(f'Content: {original}')

# Check if file format is OK.
## Remember to alter this code to support more formats in the future
if not (start_search(original) and start_search(translation)):
    print('Error: corrupted file. Try a supported file format.')
    time.sleep(4)
    exit()
#print('OK.')

# Create the columns in table.csv
fhandle_table=open('table.csv', "w")
fhandle_table.write('ORIGINAL;TRANSLATION\n')

# Make a list to store original the original subtitles
origin_lst=parse_sub(original)
#print(len(origin_lst))

# Repeat the process with translation
trans_lst=parse_sub(translation)
#print(len(trans_lst))

# If subtitle id of original and translation are the same, they are written in the csv file
for origin_id, o in origin_lst:
    for trans_id, t in trans_lst:
        if origin_id==trans_id:
            o=o.replace('\n',' ').replace(';',',') #Remove \n and ; as this can cause problems in the csv
            t=t.replace('\n',' ').replace(';',',')
            fhandle_table.write(f'{o};')
            fhandle_table.write(f'{t}\n')
fhandle_table.close