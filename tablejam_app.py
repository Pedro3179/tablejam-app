import re, time

text_origin=input('Enter the original text (file.extesion):')
fhandle_origin=open(text_origin)
text_trans=input('Enter the translation (file.extesion):')
fhandle_trans=open(text_trans)

original=fhandle_origin.read()
#print(f'Content: {original}')
translation=fhandle_trans.read()

# Create the columns in the file
#fhandle=open()

#def search_begin(str_val):
#    re.search(r'^[1-9]\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n', str_val)
    
# Check if file format is OK.
## Remember to alter this code to support more formats
if not (not re.search(r'^[1-9]\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n', original)
    and re.search(r'^[1-9]\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n', translation)):
    print('Error: corrupted file. Try a supported file format.')
    time.sleep(4)



for line in fhandle_origin:
    line=line.strip()
