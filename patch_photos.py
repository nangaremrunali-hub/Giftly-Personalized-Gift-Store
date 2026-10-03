from pathlib import Path
p=Path('/mnt/data/giftly_v6_work/Giftly/app.py')
s=p.read_text()
start=s.index('PHOTO_POOLS=')
end=s.index('\ndef products():', start)
queries = {
1:'birthday,greeting,card',2:'memory,book,notebook',3:'birthday,gift,box',4:'polaroid,photo,display',5:'countdown,frame,celebration',6:'letter,gift,envelope',7:'birthday,cake,topper',8:'star,map,wall,art',9:'acrylic,plaque,desk',10:'polaroid,photo,stand',11:'fridge,magnets,photo',12:'message,lamp,gift',13:'name,desk,plaque',14:'birthday,envelope,gift',
15:'couple,photo,timeline,frame',16:'couple,story,photo,frame',17:'couple,puzzle,gift',18:'couple,keychain,heart',19:'couple,coordinates,map,frame',20:'couple,scratch,card',21:'couple,gift,box',22:'passport,travel,set',23:'couple,stars,constellation',24:'couple,ticket,memory',25:'couple,heart,photo,frame',26:'love,letter,soundwave',27:'couple,neon,sign',28:'couple,anniversary,photos',29:'couple,mugs,gift',30:'couple,secret,box',31:'couple,memory,book',
32:'friendship,gift,cards',33:'friend,keychain,coordinates',34:'friend,desk,plaque',35:'coupon,book,gift',36:'friends,photo,strip',37:'friendship,soundwave,frame',38:'friendship,handshake,plaque',39:'friendship,memory,jar',40:'friends,bingo,cards',41:'friends,timeline,photos',42:'personalized,name,keychain',43:'friends,map,photo,frame',44:'friends,mugs,gift',45:'friendship,gift,box',46:'friendship,led,box',47:'friends,polaroid,album',48:'friendship,quote,tiles',49:'memory,receipt,print',
50:'moon,phase,photo,frame',51:'memory,map,frame',52:'secret,message,shadow,box',53:'star,date,keepsake',54:'name,story,plaque',55:'birth,flower,name,frame',56:'qr,code,photo,frame',57:'handwriting,keepsake,letter',58:'coordinates,plaque,wall',59:'family,name,crest,wall',60:'pet,portrait,frame',61:'recipe,frame,kitchen',62:'name,initial,light,box',63:'personalized,memory,cards',64:'personalized,calendar,desk',65:'secret,message,book',
66:'custom,name,light,box',67:'wall,clock,home,decor',68:'housewarming,plaque,home',69:'quote,wall,print,decor',70:'shelf,plaque,home,decor',71:'house,door,sign,nameplate',72:'skyline,light,decor',73:'neon,sign,room,decor',74:'pet,portrait,wall,art',75:'coordinates,wall,art',76:'house,story,frame,home',77:'botanical,wall,print',78:'couple,corner,sign,decor',79:'family,timeline,wall,photos',80:'photo,grid,wall,decor'
}
# Replace previous pool-based photo assignment with product-specific real-photo URLs.
new='''PRODUCT_PHOTO_QUERIES = %r\n\ndef product_photo(pid, name, category):\n    from urllib.parse import quote\n    query = PRODUCT_PHOTO_QUERIES.get(pid, f"{category},gift,product")\n    return f"https://loremflickr.com/900/700/{quote(query, safe=',')}?lock={pid}"\n''' % queries
s=s[:start]+new+s[end:]
old='''def products():\n out=[]\n counters={k:0 for k in PHOTO_POOLS}\n for x in P:\n  cat=x[2]; pool=PHOTO_POOLS[cat]; idx=counters[cat] % len(pool); counters[cat]+=1\n  out.append({"id":x[0],"name":x[1],"category":cat,"price":x[3],"old":x[4],"tag":x[5],"image":x[6],"photo":pool[idx],"rating":round(4.5+(x[0]%6)/10,1),"desc":"A thoughtful keepsake designed around a name, date, place or memory."})\n return out\n'''
newfn='''def products():\n out=[]\n for x in P:\n  cat=x[2]\n  out.append({"id":x[0],"name":x[1],"category":cat,"price":x[3],"old":x[4],"tag":x[5],"image":x[6],"photo":product_photo(x[0],x[1],cat),"rating":round(4.5+(x[0]%6)/10,1),"desc":"A thoughtful keepsake designed around a name, date, place or memory."})\n return out\n'''
if old not in s:
    raise SystemExit('old products function not found')
s=s.replace(old,newfn)
p.write_text(s)
