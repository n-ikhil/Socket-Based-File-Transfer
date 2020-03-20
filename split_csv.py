import csv

creds = "../data_files/login_credentials.csv"
rows=[]

def extract():
    global rows
    with open(creds, 'r') as database: 
        csvreader = csv.reader(database) 
        rows.append(next(csvreader))
        for fields in csvreader:
            rows.append(fields)

def write_csv(name,start,end):
    print(start, end)
    global rows
    with open(name, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(rows[0]) 
        csvwriter.writerows(rows[start:end])
    return

def split_csv():
    global rows
    index=[0,0,0]
    strength=len(rows)-1
    split_strength=int(strength/3)
    index[0]=split_strength+1
    index[1]=(split_strength*2)+1
    index[2]=strength+1

    write_csv("ha.csv",1,index[0])
    write_csv("hb.csv",index[0]+1,index[1])
    write_csv("hc.csv",index[1]+1,index[2])

    

extract()
split_csv()
