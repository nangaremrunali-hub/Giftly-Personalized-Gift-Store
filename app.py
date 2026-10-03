from flask import Flask,render_template,request,redirect,url_for,session,jsonify,flash
import sqlite3,os,json,random,string
from werkzeug.security import generate_password_hash,check_password_hash
app=Flask(__name__);app.secret_key="giftly-demo-2026";DB="giftly.db"

P=[(1, 'Birthday Memory Ticket', 'Birthday', 499, 699, 'Popular', 'products/birthday-01.svg'), (2, 'Mini Memory Book', 'Birthday', 599, 799, 'New', 'products/birthday-02.svg'), (3, 'Custom Birthday Gift Box', 'Birthday', 899, 1199, 'Bundle', 'products/birthday-03.svg'), (4, 'Birthday Photo Carousel', 'Birthday', 749, 999, 'Featured', 'products/birthday-04.svg'), (5, 'Birthday Countdown Frame', 'Birthday', 699, 899, 'New', 'products/birthday-05.svg'), (6, 'Birthday Letter Capsule', 'Birthday', 449, 599, 'Sweet', 'products/birthday-06.svg'), (7, 'Cake Topper Keepsake', 'Birthday', 399, 549, 'Cute', 'products/birthday-07.svg'), (8, 'Birthday Star Map', 'Birthday', 899, 1199, 'Signature', 'products/birthday-08.svg'), (9, 'Wish List Acrylic Plaque', 'Birthday', 649, 849, 'Bestseller', 'products/birthday-09.svg'), (10, 'Birthday Polaroid Stand', 'Birthday', 549, 749, 'Trending', 'products/birthday-10.svg'), (11, 'Party Memory Magnet Set', 'Birthday', 349, 499, 'Fun', 'products/birthday-11.svg'), (12, 'Birthday Message Lamp', 'Birthday', 999, 1299, 'Glow', 'products/birthday-12.svg'), (13, 'Name & Age Desk Plaque', 'Birthday', 599, 799, 'Personal', 'products/birthday-13.svg'), (14, 'Birthday Surprise Envelope Set', 'Birthday', 299, 399, 'Budget Pick', 'products/birthday-14.svg'), (15, 'Our Story Timeline', 'Couple', 799, 999, 'Bestseller', 'products/couple-01.svg'), (16, 'Song & Story Frame', 'Couple', 849, 1099, 'Trending', 'products/couple-02.svg'), (17, 'Couple Puzzle Plaque', 'Couple', 649, 849, 'Romantic', 'products/couple-03.svg'), (18, 'Forever Keychain Pair', 'Couple', 499, 649, 'Pair', 'products/couple-04.svg'), (19, 'Two-City Coordinates Frame', 'Couple', 899, 1199, 'Signature', 'products/couple-05.svg'), (20, 'Date Night Scratch Card', 'Couple', 399, 549, 'Cute', 'products/couple-06.svg'), (21, 'Reasons I Love You Box', 'Couple', 699, 899, 'Popular', 'products/couple-07.svg'), (22, 'His & Hers Passport Set', 'Couple', 749, 949, 'New', 'products/couple-08.svg'), (23, 'Custom Constellation Couple', 'Couple', 999, 1299, 'Unique', 'products/couple-09.svg'), (24, 'Our First Date Ticket', 'Couple', 499, 649, 'Memory', 'products/couple-10.svg'), (25, 'Split Heart Photo Frame', 'Couple', 699, 899, 'Romantic', 'products/couple-11.svg'), (26, 'Love Letter Soundwave', 'Couple', 799, 1049, 'Personal', 'products/couple-12.svg'), (27, 'Couple Name Neon Plaque', 'Couple', 1099, 1399, 'Glow', 'products/couple-13.svg'), (28, 'Anniversary Memory Wheel', 'Couple', 849, 1099, 'Featured', 'products/couple-14.svg'), (29, 'Two Mugs Story Set', 'Couple', 599, 799, 'Pair', 'products/couple-15.svg'), (30, 'Secret Date Decoder Box', 'Couple', 749, 999, 'Secret', 'products/couple-16.svg'), (31, 'Forever Timeline Book', 'Couple', 999, 1299, 'Premium', 'products/couple-17.svg'), (32, 'Reasons Why Gift Cards', 'Friendship', 399, 549, 'Cute', 'products/friendship-01.svg'), (33, 'Best Friend Coordinates Keychain', 'Friendship', 449, 599, 'Gift Pick', 'products/friendship-02.svg'), (34, 'Inside Joke Desk Plaque', 'Friendship', 549, 699, 'Funny', 'products/friendship-03.svg'), (35, 'Friendship Coupon Book', 'Friendship', 349, 499, 'Fun', 'products/friendship-04.svg'), (36, 'Bestie Photo Strip', 'Friendship', 499, 649, 'Popular', 'products/friendship-05.svg'), (37, 'Friendship Soundwave Frame', 'Friendship', 749, 949, 'New', 'products/friendship-06.svg'), (38, 'Secret Handshake Plaque', 'Friendship', 599, 799, 'Unique', 'products/friendship-07.svg'), (39, 'Best Friend Memory Jar', 'Friendship', 649, 849, 'Bestseller', 'products/friendship-08.svg'), (40, 'Friendship Bingo Cards', 'Friendship', 299, 399, 'Budget Pick', 'products/friendship-09.svg'), (41, 'Bestie Timeline Board', 'Friendship', 799, 999, 'Trending', 'products/friendship-10.svg'), (42, 'Custom Nickname Keychain', 'Friendship', 399, 549, 'Personal', 'products/friendship-11.svg'), (43, 'Friendship Map Frame', 'Friendship', 749, 949, 'Signature', 'products/friendship-12.svg'), (44, 'Chaos Partner Mug Set', 'Friendship', 599, 799, 'Funny', 'products/friendship-13.svg'), (45, 'Friendship Survival Kit', 'Friendship', 899, 1199, 'Bundle', 'products/friendship-14.svg'), (46, 'Inside Joke LED Box', 'Friendship', 999, 1299, 'Glow', 'products/friendship-15.svg'), (47, 'Bestie Polaroid Album', 'Friendship', 699, 899, 'Classic', 'products/friendship-16.svg'), (48, 'Friendship Quote Tile Set', 'Friendship', 449, 599, 'Cute', 'products/friendship-17.svg'), (49, 'Memory Receipt Print', 'Friendship', 349, 499, 'Novel', 'products/friendship-18.svg'), (50, 'Moon Phase Memory Frame', 'Personalized', 899, 1199, 'Signature', 'products/personalized-01.svg'), (51, 'Memory Map Frame', 'Personalized', 749, 949, 'New', 'products/personalized-02.svg'), (52, 'Secret Message Shadow Box', 'Personalized', 699, 899, 'Unique', 'products/personalized-03.svg'), (53, 'Star Date Keepsake', 'Personalized', 899, 1199, 'Signature', 'products/personalized-04.svg'), (54, 'Custom Name Story Plaque', 'Personalized', 649, 849, 'Personal', 'products/personalized-05.svg'), (55, 'Birth Flower Name Frame', 'Personalized', 799, 999, 'Botanical', 'products/personalized-06.svg'), (56, 'Voice Note QR Frame', 'Personalized', 899, 1199, 'Tech', 'products/personalized-07.svg'), (57, 'Handwriting Keepsake', 'Personalized', 749, 949, 'Sentimental', 'products/personalized-08.svg'), (58, 'Custom Coordinates Plaque', 'Personalized', 599, 799, 'Minimal', 'products/personalized-09.svg'), (59, 'Family Name Crest', 'Personalized', 999, 1299, 'Premium', 'products/personalized-10.svg'), (60, 'Pet Memory Portrait', 'Personalized', 849, 1099, 'Loved', 'products/personalized-11.svg'), (61, 'Custom Recipe Frame', 'Personalized', 699, 899, 'Kitchen', 'products/personalized-12.svg'), (62, 'Name Initial Light Box', 'Personalized', 999, 1299, 'Glow', 'products/personalized-13.svg'), (63, 'Personalized Memory Cards', 'Personalized', 449, 599, 'Set', 'products/personalized-14.svg'), (64, 'Custom Date Calendar', 'Personalized', 549, 749, 'Useful', 'products/personalized-15.svg'), (65, 'Secret Message Book', 'Personalized', 799, 999, 'Hidden', 'products/personalized-16.svg'), (66, 'Custom Glow Name Box', 'Decor', 999, 1299, 'Glow', 'products/decor-01.svg'), (67, 'Memory Clock', 'Decor', 1099, 1399, 'Premium', 'products/decor-02.svg'), (68, 'Housewarming Memory Plaque', 'Decor', 799, 999, 'Home', 'products/decor-03.svg'), (69, 'Memory Quote Print', 'Decor', 349, 499, 'Minimal', 'products/decor-04.svg'), (70, 'Story Shelf Plaque', 'Decor', 649, 849, 'New', 'products/decor-05.svg'), (71, 'Family Door Sign', 'Decor', 699, 899, 'Home', 'products/decor-06.svg'), (72, 'Custom Skyline Light', 'Decor', 1199, 1499, 'Glow', 'products/decor-07.svg'), (73, 'Memory Corner Neon', 'Decor', 1099, 1399, 'Trending', 'products/decor-08.svg'), (74, 'Pet Portrait Wall Tile', 'Decor', 749, 949, 'Loved', 'products/decor-09.svg'), (75, 'Coordinates Wall Art', 'Decor', 599, 799, 'Minimal', 'products/decor-10.svg'), (76, 'House Story Frame', 'Decor', 899, 1199, 'Signature', 'products/decor-11.svg'), (77, 'Custom Botanical Print', 'Decor', 549, 749, 'Botanical', 'products/decor-12.svg'), (78, 'Couple Corner Sign', 'Decor', 699, 899, 'Romantic', 'products/decor-13.svg'), (79, 'Family Timeline Wall Set', 'Decor', 999, 1299, 'Featured', 'products/decor-14.svg'), (80, 'Memory Photo Grid', 'Decor', 799, 999, 'Classic', 'products/decor-15.svg')]
PRODUCT_PHOTOS = {
    # Real product photography: each group matches the physical object sold.
    "card": "https://katieleamon.com/cdn/shop/files/Happy-Bday-handwritten-KL-C623.jpg?v=1761342548&width=990",
    "giftbox": "https://www.kindredandco.uk/cdn/shop/files/birthday-age-prosecco.jpg?v=1759418459&width=1080",
    "book": "https://i.etsystatic.com/17463840/r/il/bc2045/4525199255/il_794xN.4525199255_yl5y.jpg",
    "stand": "https://popic.com.au/cdn/shop/files/Popic_PT_BrassStand4.jpg?v=1731565546&width=1458",
    "keychain": "https://content.rozetka.com.ua/goods/images/big/460146385.jpg",
    "soundwave": "https://www.bikolihediye.com/kisiye-ozel-ses-izi-fotografli-isikli-tablo-sevgiliye-surprizler-14842-93-B.jpg",
    "neon": "https://m.media-amazon.com/images/I/51neHUYRB-L._AC_.jpg",
    "calendar": "https://img.specialmoment.co.uk/productimageslarge/personalised-photo-upload-desk-calendar.jpg",
    "plaque": "https://cdn.notonthehighstreet.com/fs/e8/32/3ac0-cf57-42c9-93d8-f5501a37ca33/original_custom-name-wall-plaque.jpg",
    "pet": "https://www.thezappybox.com/cdn/shop/files/Personalized_Pet_Photo_Frame_1_cb7c01ff-c4b1-4473-8730-2411209cee3f.webp?v=1774011646&width=1080",
    "mugs": "https://cdnnew.igp.com/f_auto,q_auto,t_pnoptprodlp/products/p-personalized-romantic-couple-mugs-199224-m.jpg",
    "clock": "https://images.unsplash.com/photo-1678109880347-15fe35f3148c?auto=format&fit=crop&fm=jpg&q=80&w=1200",
    "birthday_photo": "https://images.unsplash.com/photo-1783408354775-8f697854b1a1?auto=format&fit=crop&fm=jpg&q=80&w=1200",
    "wallart": "https://images.unsplash.com/photo-1789557167712-bf73a3d8bee5?auto=format&fit=crop&fm=jpg&q=80&w=1200",
}

PHOTO_TYPE = {
 1:'card',2:'book',3:'giftbox',4:'stand',5:'stand',6:'card',7:'card',8:'wallart',9:'plaque',10:'stand',11:'stand',12:'neon',13:'plaque',14:'card',
 15:'book',16:'soundwave',17:'plaque',18:'keychain',19:'wallart',20:'card',21:'giftbox',22:'book',23:'wallart',24:'card',25:'stand',26:'soundwave',27:'neon',28:'book',29:'mugs',30:'giftbox',31:'book',
 32:'card',33:'keychain',34:'plaque',35:'book',36:'stand',37:'soundwave',38:'plaque',39:'giftbox',40:'card',41:'book',42:'keychain',43:'wallart',44:'mugs',45:'giftbox',46:'neon',47:'book',48:'wallart',49:'card',
 50:'wallart',51:'wallart',52:'giftbox',53:'wallart',54:'plaque',55:'wallart',56:'soundwave',57:'card',58:'plaque',59:'plaque',60:'pet',61:'calendar',62:'neon',63:'card',64:'calendar',65:'book',
 66:'neon',67:'clock',68:'plaque',69:'wallart',70:'plaque',71:'plaque',72:'wallart',73:'neon',74:'pet',75:'wallart',76:'plaque',77:'wallart',78:'plaque',79:'wallart',80:'stand'
}

def product_photo(pid, name, category):
    return PRODUCT_PHOTOS[PHOTO_TYPE.get(pid, 'giftbox')]

def products():
 out=[]
 for x in P:
  cat=x[2]
  out.append({"id":x[0],"name":x[1],"category":cat,"price":x[3],"old":x[4],"tag":x[5],"image":x[6],"photo":product_photo(x[0],x[1],cat),"rating":round(4.5+(x[0]%6)/10,1),"desc":"A thoughtful keepsake designed around a name, date, place or memory."})
 return out
PS=products()
C=[{"name":"Birthday","icon":"✦","count":14,"desc":"Unexpected little ways to make their day feel bigger."},{"name":"Couple","icon":"∞","count":17,"desc":"Objects that turn shared moments into keepsakes."},{"name":"Friendship","icon":"+","count":18,"desc":"Inside jokes, coordinates and tiny reminders of your people."},{"name":"Personalized","icon":"◌","count":16,"desc":"Names, dates, voices, places and details that belong to one person."},{"name":"Decor","icon":"⌂","count":15,"desc":"Statement pieces for corners of a home with a story."}]

def con(): c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def init():
 c=con();c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT,email TEXT UNIQUE,password TEXT,phone TEXT,address TEXT,city TEXT,state TEXT,pincode TEXT)");c.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY,user_id INTEGER,items TEXT,total REAL,payment TEXT,address TEXT,status TEXT,created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)");c.commit();c.close()
@app.context_processor
def ctx():
 u=None
 if session.get("uid"):
  c=con();u=c.execute("SELECT * FROM users WHERE id=?",(session["uid"],)).fetchone();c.close()
 return {"current_user":u,"cart_count":sum(session.get("cart",{}).values())}
def getp(i): return next((p for p in PS if p["id"]==int(i)),None)
@app.get("/")
def home(): return render_template("home.html",products=PS[:12],cats=C)
@app.get("/shop")
def shop():
 cat=request.args.get("category","");q=request.args.get("q","").lower();ps=[p for p in PS if (not cat or p["category"]==cat) and (not q or q in p["name"].lower() or q in p["category"].lower())]
 return render_template("shop.html",products=ps,cats=C,active=cat)
@app.get("/product/<int:i>")
def product(i):
 p=getp(i);return render_template("product.html",p=p,related=[x for x in PS if x["category"]==p["category"] and x["id"]!=i][:8])
@app.post("/cart/add")
def add():
 i=str(request.form["id"]);c=session.setdefault("cart",{});c[i]=c.get(i,0)+1;session.modified=True;return jsonify(ok=1,count=sum(c.values()))
@app.get("/cart")
def cart():
 rows=[];total=0
 for i,q in session.get("cart",{}).items():
  p=getp(i)
  if p:r=dict(p);r["qty"]=q;r["sub"]=p["price"]*q;rows.append(r);total+=r["sub"]
 return render_template("cart.html",items=rows,total=total)
@app.post("/cart/update")
def update():
 i=request.form["id"];q=int(request.form["qty"]);c=session.get("cart",{})
 if q<=0:c.pop(i,None)
 else:c[i]=q
 session.modified=True;return redirect(url_for("cart"))
@app.post("/cart/clear")
def clear():session["cart"]={};return redirect(url_for("cart"))
@app.get("/wishlist")
def wishlist():return render_template("shop.html",products=[p for p in PS if p["id"] in session.get("wish",[])],cats=C,active="Wishlist")
@app.post("/wish")
def wish():
 i=int(request.form["id"]);w=session.setdefault("wish",[])
 if i in w:w.remove(i);a=0
 else:w.append(i);a=1
 session.modified=True;return jsonify(active=a)
@app.route("/register",methods=["GET","POST"])
def register():
 if request.method=="POST":
  f=request.form
  if f["password"]!=f["confirm"]:flash("Passwords do not match.","error")
  else:
   c=con()
   try:
    cur=c.execute("INSERT INTO users(name,email,password,phone,address,city,state,pincode) VALUES(?,?,?,?,?,?,?,?)",(f["name"],f["email"].lower(),generate_password_hash(f["password"]),f.get("phone"),f["address"],f["city"],f["state"],f["pincode"]))
    c.commit();session["uid"]=cur.lastrowid;flash("Account created successfully. Welcome to Giftly!","success");return redirect(url_for("home"))
   except sqlite3.IntegrityError:flash("Email already registered.","error")
   finally:c.close()
 return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
 if request.method=="POST":
  c=con();u=c.execute("SELECT * FROM users WHERE email=?",(request.form["email"].lower(),)).fetchone();c.close()
  if u and check_password_hash(u["password"],request.form["password"]):session["uid"]=u["id"];return redirect(request.args.get("next") or url_for("home"))
  flash("Invalid email or password.","error")
 return render_template("login.html")
@app.get("/logout")
def logout():session.pop("uid",None);return redirect(url_for("home"))
@app.get("/finder")
def finder():return render_template("finder.html")
@app.post("/finder")
def finder_post():
 f=request.form;ps=PS;person=f.get("person");budget=f.get("budget");style=f.get("style")
 if person=="Partner":ps=[p for p in ps if p["category"] in ["Couple","Personalized"]]
 elif person=="Friend":ps=[p for p in ps if p["category"] in ["Friendship","Personalized"]]
 elif person=="Family":ps=[p for p in ps if p["category"] in ["Birthday","Decor","Personalized"]]
 if budget=="Under ₹500":ps=[p for p in ps if p["price"]<500]
 elif budget=="₹500 – ₹1000":ps=[p for p in ps if 500<=p["price"]<=1000]
 elif budget=="₹1000+":ps=[p for p in ps if p["price"]>=900]
 if style=="Romantic":ps=[p for p in ps if p["category"] in ["Couple","Personalized"]] or ps
 elif style=="Decorative":ps=[p for p in ps if p["category"]=="Decor"] or ps
 elif style=="Memory-based":ps=[p for p in ps if p["category"] in ["Personalized","Couple"]] or ps
 return render_template("results.html",products=ps[:16],person=person,budget=budget,style=style)
@app.get("/customize/<int:i>")
def customize(i):return render_template("customize.html",p=getp(i))
@app.post("/customize/<int:i>")
def customize_post(i):
 session["custom"]={"id":i,"name":request.form.get("name"),"date":request.form.get("date"),"message":request.form.get("message")};c=session.setdefault("cart",{});c[str(i)]=c.get(str(i),0)+1;session.modified=True;return redirect(url_for("cart"))
@app.get("/checkout")
def checkout():
 if not session.get("uid"):return redirect(url_for("login",next="/checkout"))
 if not session.get("cart"):return redirect(url_for("cart"))
 c=con();u=c.execute("SELECT * FROM users WHERE id=?",(session["uid"],)).fetchone();c.close();total=sum(getp(i)["price"]*q for i,q in session["cart"].items());return render_template("checkout.html",user=u,total=total)
@app.post("/order")
def order():
 if not session.get("uid"):return jsonify(login=1)
 c=con();u=c.execute("SELECT * FROM users WHERE id=?",(session["uid"],)).fetchone();total=sum(getp(i)["price"]*q for i,q in session["cart"].items());no="GF"+''.join(random.choices(string.ascii_uppercase+string.digits,k=8));c.execute("INSERT INTO orders(user_id,items,total,payment,address,status) VALUES(?,?,?,?,?,?)",(session["uid"],json.dumps(session["cart"]),total,request.form.get("payment","COD"),f'{u["address"]}, {u["city"]}, {u["state"]} - {u["pincode"]}',"Placed"));c.commit();c.close();session["cart"]={};return jsonify(ok=1,no=no,msg="Order placed! Your tracking link will be sent to you via email.")
@app.get("/orders")
def orders():
 if not session.get("uid"):return redirect(url_for("login",next="/orders"))
 c=con();o=c.execute("SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",(session["uid"],)).fetchall();c.close();return render_template("orders.html",orders=o)
if __name__=="__main__":init();app.run(debug=True,port=5002)
