import csv, random, io
random.seed(20260317)
rows=[]
tid=100000
def add(ts,acct,name,typ,amount,channel,city,country,payee,payee_new,bal):
    global tid; tid+=1
    rows.append(dict(txn_id=f"TXN-{tid}",ts=ts,account_id=acct,account_name=name,type=typ,
        amount=f"{amount:.2f}",channel=channel,city=city,country=country,payee_id=payee,
        payee_new="true" if payee_new else "false",balance_after=f"{bal:.2f}"))

first=["Andi","Budi","Citra","Dewi","Eka","Fajar","Gita","Hadi","Indah","Joko","Kirana","Lukman","Maya","Nanda","Oscar","Putri","Qori","Rudi","Sari","Tono","Umar","Vina","Wahyu","Xena","Yoga","Zahra"]
last=["Saputra","Wibowo","Santoso","Hidayat","Pratama","Kusuma","Nugroho","Halim","Salim","Gunawan","Tanaka","Chen","Wijaya","Lestari","Rahman"]
cities=[("Jakarta","ID"),("Bandung","ID"),("Surabaya","ID"),("Medan","ID"),("Singapore","SG")]
channels=["branch","atm","mobile","online"]
types=["cash_deposit","transfer_out","transfer_in","withdrawal","card_payment"]

# normal background accounts
accts=[]
for i in range(28):
    accts.append((f"A-{1020+i}", f"{random.choice(first)} {random.choice(last)}"))
base_day=17  # March 2026, dataset covers Mar 1-18
for acct,name in accts:
    bal=random.uniform(2000,40000)
    n=random.randint(3,8)
    home=random.choices(cities,weights=[45,20,15,5,3])[0]
    for _ in range(n):
        d=random.randint(1,base_day); h=random.randint(7,20); m=random.randint(0,59)
        typ=random.choice(types)
        amt=round(random.uniform(15,3000),2)
        city,country=home
        payee=f"P-{random.randint(300,999)}" if typ in("transfer_out","card_payment") else ""
        add(f"2026-03-{d:02d}T{h:02d}:{m:02d}:00+07:00",acct,name,typ,amt,random.choice(channels),city,country,payee,False,bal)
        bal+= amt if typ in("cash_deposit","transfer_in") else -amt

# PATTERN 1: structuring, A-1042 R. Wibowo - 4 cash deposits 9,4xx-9,9xx within 60h
for i,(d,h,amt) in enumerate([(10,9,9450.00),(11,13,9780.00),(11,16,9520.00),(12,10,9890.00)]):
    add(f"2026-03-{d:02d}T{h:02d}:00:00+07:00","A-1042","R. Wibowo","cash_deposit",amt,"branch","Jakarta","ID","",False,40000+i*9500)

# PATTERN 2: velocity, A-1077 M. Chen - 6 txns in 47 minutes
for i in range(6):
    add(f"2026-03-14T21:{5+i*8:02d}:00+07:00","A-1077","M. Chen","transfer_out",round(random.uniform(700,1800),2),"mobile","Singapore","SG",f"P-{810+i}",True,15000-i*900)

# PATTERN 3: dormant bust-out, A-1091 - old txn Sep 2025, then 48k withdrawal Mar 2026
add("2025-09-12T10:15:00+07:00","A-1091","H. Gunawan","card_payment",85.40,"online","Jakarta","ID","P-411",False,52000)
add("2026-03-15T11:02:00+07:00","A-1091","H. Gunawan","withdrawal",48000.00,"branch","Jakarta","ID","",False,4000)

# PATTERN 4: round amount to new payee, A-1055
add("2026-03-16T14:22:00+07:00","A-1055","K. Lestari","transfer_out",25000.00,"online","Jakarta","ID","P-999",True,31000)
add("2026-03-16T14:40:00+07:00","A-1055","K. Lestari","transfer_out",12000.00,"online","Jakarta","ID","P-999",False,19000)

# PATTERN 5: impossible travel, A-1063 Jakarta -> Singapore 75 min later
add("2026-03-13T09:10:00+07:00","A-1063","T. Rahman","card_payment",220.00,"online","Jakarta","ID","P-520",False,8000)
add("2026-03-13T10:25:00+07:00","A-1063","T. Rahman","withdrawal",3500.00,"atm","Singapore","SG","",False,4500)

rows.sort(key=lambda r:r["ts"])
with open("data/northbridge-march.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows),"rows")
