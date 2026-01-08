'''
TableJam - A tool to align SRT transcription and translation files
and export them as a clean CSV table.
'''

__version__='2.0.1'
__updated__='2025-11-28'

import re
from datetime import time, timedelta

# Linked List.
class Node: 
    def __init__(self, data=None, next_node=None):
        self.data=data
        self.next_node=next_node

class Data:
    def __init__(self, id, t1, t2, text):
        self.id=id
        self.t1= t1    # Subtitle start time
        self.t2= t2    # Subtitle end time
        self.text=text

# Define the wrapper.
class LinkedList:
    def __init__(self):
        self.head=None      # You can use this variable to indicate the head later
        self.last_node=None
    
    def print_ll(self):
        ll_string=''
        node=self.head      # Take the node object defined to be the head and store it in node.
        if node is None:
            print(None)

# Vizual representation of the data structure/linked list.
        print('{')
        while node is not None:
            print(f'  {str(node.data.id)} {str(node.data.t1)} {str(node.data.t2)} {str(node.data.text)}')
                                                       
            node=node.next_node             # Take the next_node as defined in the node object.
        print('}')

    def insert_beginning(self, id , t1 , t2 , textual):
        if self.head is None:
            self.head=Node(Data( id , t1 , t2 , textual), None)
            self.last_node=self.head
        else:
            new_node= Node(Data( id , t1 , t2 , textual), self.head)
            self.head=new_node

    def insert_next(self, id , t1 , t2 , textual):
        id=int(id)
        if self.head is None or id<self.head.data.id:
            self.insert_beginning( id , t1 , t2 , textual)
        
        else:
            new_node=Node(Data(id , t1 , t2 , textual))
            node=self.head
            while node.next_node:
                if equal_span(t1, node.data.t1) and equal_span(t2, node.data.t2):
                    return
                
                if t1 > node.data.t2 and t2 < node.next_node.data.t1:
                    node.next_node=new_node
                    return

                node=node.next_node
            if equal_span(t1, node.data.t1) and equal_span(t2, node.data.t2):
                return
            node.next_node=new_node

def start_search(str_val):
    return re.search(
        r'^[1-9]\n\d\d:\d\d:\d\d\,\d\d\d\s\-\-\>\s\d\d:\d\d:\d\d\,\d\d\d\n',
        str_val
    )

def parse_sub(str_val):
    ''' Return a list of tuples with the following items: subtitle id, start time,
    end time and text. '''
    return re.findall(
        r'(\d+)\n(\d\d:\d\d:\d\d\,\d\d\d\s)\-\-\>\s(\d\d:\d\d:\d\d\,\d\d\d)\n(.+\n.*)\n',
        str_val
    )

def str_to_delta(str_val):
    ''' Take a string parameter and convert it to an object timedelta '''
    lst=re.split(r'[:,]', str_val)
    milli_to_micro=(int(lst[3]))*1000
    delta=timedelta(
        hours=int(lst[0]),
        minutes=int(lst[1]),
        seconds=int(lst[2]),
        microseconds=milli_to_micro
    )
    return delta
        
def equal_span(origin_time, trans_time):
    origin_time=str_to_delta(origin_time)
    trans_time=str_to_delta(trans_time)
    span=timedelta(microseconds=800000) #The span should be less than the min duration of a subtitle (1s).

    # if translation timestamp is within a given span of the original timestamp, it returns True.
    if (origin_time-span) <trans_time< (origin_time+span): 
        return True
    else:
        return False

def print_table(table):
    print('[')
    for i in table:
        i_without_new_line=i[3]
        i_without_new_line=i_without_new_line[:-1]
        print(f'    {i[0]} {i[1]} {i[2]} {i_without_new_line},')
    print(']')

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
    
# Check if file format is OK.
## Remember to alter this code to support more formats in the future
if not (start_search(original) and start_search(translation)):
    print('Error: corrupted file. Try a supported file format.')
    time.sleep(4)
    exit()

# Make lists to store original and translation subtitles
origin_lst=parse_sub(original)
trans_lst=parse_sub(translation)

# Firstly, fix split translation lines.
table=[]    # List of tuples to store the original sub and its translation.

for o_id, o_start, o_end, o_body in origin_lst:
    sub_string=''
    for t_id, t_start, t_end, t_body in trans_lst:

        # Skip if two or more lines of the original was concatanated into one in the translation.  
        if equal_span(o_start, t_start) is False and str_to_delta(t_start) < str_to_delta(o_start):
            continue
        
        if equal_span(o_end, t_end):
            o_body=o_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            t_body=t_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            line=(o_id,o_start, o_end, f' {o_body}  ;{sub_string}{t_body} \n') 
            table.append(line)
            break

        else:
            t_body=t_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            sub_string+=f'{t_body}'

# Secondly, fix concatanated translation lines.
table_2=[]

for t_id, t_start, t_end, t_body in trans_lst:
    sub_string=''
    for o_id, o_start, o_end, o_body in origin_lst:

        # Skip if a line of the original was split into two or more in the translation.          
        if equal_span(o_start, t_start) is False and str_to_delta(t_start) > str_to_delta(o_start):
            continue
        
        if equal_span(o_end, t_end):
            o_body=o_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            t_body=t_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            line=(t_id,t_start, t_end, f'{sub_string} {o_body}  ;{t_body}  \n') 
            table_2.append(line)
            break
        else:
            o_body=o_body.replace('\n',' ').replace(';',',').replace('"','').replace('-', ' -')
            sub_string+=f'{o_body} '

# Create a linked list to store the first list that fixes the split lines problem.
ll=LinkedList()

for (id, t1 , t2 , text)  in table:
    ll.insert_next(id, t1 , t2 , text)

# Add list that fixed the concatened translation issue to the previous linked list instance.
for (id, t1 , t2 , text)  in table_2:
    ll.insert_next(id, t1 , t2 , text)

#print_table(table)
#print_table(table_2)

#ll.print_ll()

# Create the columns and write the rows to table.csv.
fhandle_table=open('table.csv', "w")
fhandle_table.write('ORIGINAL;TRANSLATION\n')

# Loop through the linked list and write each node id and text fields to the CSV file.
node=ll.head

while node is not None:
    fhandle_table.write(f'{str(node.data.id)} {str(node.data.text)}')                                                   
    node=node.next_node             # Take the next_node as defined in the node object.

fhandle_table.close