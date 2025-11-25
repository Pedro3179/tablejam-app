'''
TableJam - A tool to align SRT transcription and translation files
and export them as a clean CSV table.
'''

__version__='1.1.0'
__updated__='2025-11-24'

import re, datetime
from datetime import time, timedelta, datetime

def start_search(str_val):
    return re.search(
        r'^[1-9]\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n',
        str_val
    )

def parse_sub(str_val):
    return re.findall(
        r'(\d+)\n(\d\d:\d\d:\d\d\,\d\d\d\s)\-\-\>\s(\d\d:\d\d:\d\d\,\d\d\d)\n(.+\n.*)\n',
        str_val
    )

def str_to_delta(str_val):
    lst=re.split(r'[:,]', str_val)
    milli_to_micro=(int(lst[3]))*1000
    delta=timedelta(hours=int(lst[0]), minutes=int(lst[1]), seconds=int(lst[2]), microseconds=milli_to_micro)
    return delta
        
def equal_span(origin_time, trans_time):
    origin_time=str_to_delta(origin_time)
    trans_time=str_to_delta(trans_time)
    span=timedelta(microseconds=999999) #The span is the min duration of a subtitle (1s).

    # if translation timestamp is within a given span of the original timestamp, it returns True.
    if (origin_time-span) <trans_time< (origin_time+span): 
        return True
    else:
        return False

print(f'\nTableJam-app - version {__version__} (updated {__updated__})\n')

# Ask for transcription and translation.
while True:
    text_origin=input('Enter the original text (file.extesion):')
    text_trans=input('Enter the translation (file.extesion):')

# Read the file and check for wrong format and encoding errors.    
    try:
        fhandle_origin=open(text_origin, encoding='utf-8-sig')
        original=fhandle_origin.read()
    except:
        try:
            fhandle_origin=open(text_origin, encoding='cp1252')
            original=fhandle_origin.read()
        except:
            print(
                'Error: Original wrong file format or encoding. Try again with a valid file.\n'
            )
            continue
    try:
        fhandle_trans=open(text_trans, encoding='utf-8-sig')
        translation=fhandle_trans.read()
    except:
            try:
                fhandle_trans=open(text_trans, encoding='cp1252')
                translation=fhandle_trans.read()
            except:
                print(
                    'Error: Translation wrong file format or encoding. Try again with a valid file.\n'
                )
                continue
    break  
    
#print(f'Content: {original}')

# Check if file format is OK.
## Remember to alter this code to support more formats in the future
if not (start_search(original) and start_search(translation)):
    print('Error: corrupted file. Try a supported file format.')
    time.sleep(4)
    exit()

# Create the columns in table.csv
fhandle_table=open('table.csv', "w")
fhandle_table.write('ORIGINAL;TRANSLATION\n')

# Make a list to store original subtitles
origin_lst=parse_sub(original)
#print(origin_lst)

# Repeat the process with translation
trans_lst=parse_sub(translation)
#print(len(trans_lst))


for o_id, o_start, o_end, o_body in origin_lst:
    sub_string=''
    for t_id, t_start, t_end, t_body in trans_lst:
        if equal_span(o_start, t_start) is False and str_to_delta(t_start) < str_to_delta(o_start):
            continue
        
        if equal_span(o_end, t_end):
            o_body=o_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            fhandle_table.write(f'{o_id} {o_body}  ;')
            t_body=t_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            fhandle_table.write(f'{sub_string}{t_body}  \n')
            break
        else:
            t_body=t_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            sub_string+=f' {t_body}  '

#        if origin_id==trans_id:
#            o=o.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -') #Remove '\n', ';' and '"' as this can cause problems in the csv
#            t=t.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -') #Add a space before "-", because excel can confuse it with a math operator
#            fhandle_table.write(f'{origin_id} {o};')
#            fhandle_table.write(f'{t}\n')
fhandle_table.close