t = 'a1 int | a2 char(2) | a3 float'
s = '123 | XX | 3.14'
table = [t,s]
print(table)
index = [0,2]
for row in table:
    row = row.split(' | ')
    row_str = ''
    for i in index:
        row_str += f'{row[i]} | '
    row_str = row_str.removesuffix(' | ')
    print(row_str)