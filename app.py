from flask import *
import sqlite3
import secrets
import time
import os
import base64
import google.generativeai as genai
import telepot
genai.configure(api_key='AIzaSyC9VGkZWQ6IzpfnG-2zxKCXgD1WOcu0A7I')
gemini_model = genai.GenerativeModel('gemini-pro')
chat = gemini_model.start_chat()

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

command = '''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image TEXT NOT NULL,
            md TEXT NOT NULL,
            ed TEXT NOT NULL
        );
    '''
cursor.execute(command)

command = '''
        CREATE TABLE IF NOT EXISTS DonateItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image TEXT NOT NULL,
            md TEXT NOT NULL,
            ed TEXT NOT NULL,
            phone TEXT NOT NULL
        );
    '''
cursor.execute(command)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('userlog.html')

@app.route('/scan')
def scan():
    return render_template('scanner.html')

@app.route('/scanner')
def scanner():
    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()

    import cv2
    from pyzbar.pyzbar import decode
    vs = cv2.VideoCapture(0)
    while True:
        # read the image in numpy array using cv2
        ret, img = vs.read()
        # Decode the barcode image
        detectedBarcodes = decode(img)
        d=''
        t=''
        # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes:
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect
            # Put the rectangle in image using
            # cv2 to heighlight the barcode
            cv2.rectangle(img, (x-10, y-10),
                        (x + w+10, y + h+10),
                        (255, 0, 0), 2)
            d = barcode.data
            t = barcode.type
        if d != "":
            d = d.decode('utf-8', 'ignore')
            cv2.putText(img, str(d), (50, 50) , cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0) , 2)		
        #Display the image
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if d != "":
            break
    vs.release()
    cv2.destroyAllWindows()
    print(d)

    name = d
    
    f = open(name+'.txt', 'r')
    recipies = f.read()
    f.close()
    print(recipies)

    if name == 'paneer':
        video1 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/U1LVDFwi8qI?si=HpvQCkVFMXkK8ZLI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """

        video2 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/BwIJHI4KdIE?si=1piargeJ2IJfHQDE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """

    elif name == 'mushroom':
        video1 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/Yu_mkN65E1I?si=KhROZTzESrm3xgmm" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """
        video2 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/rTLMj6FEo20?si=HxwuPbtJmuPqgRIG" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """

    elif name == 'chicken':
        video1 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/dRW3VMfNlaY?si=NLl_OGyjkkkdH1vj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """
        video2 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/F0WJ107nEwg?si=eHMetfZgb0gowbJ5" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """

    elif name == 'mutton':
        video1 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/P2SGDHHelis?si=TvxvEFoWiAdaUsJQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """
        video2 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/jn69U8Kf5Qg?si=XyM_IZedyV5IhLm-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """

    elif name == 'fish':
        video1 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/o8lDCY2_jyw?si=v6niMbGvC2V4ip9e" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """
        video2 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/nV_0srDzbFg?si=nyNvK_gF39VHUceV" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """

    elif name == 'prawns':
        video1 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/4xjE3OhkD0I?si=h6Z5YakQlDhG2k8m" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """
        video2 = """
            <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/LVOZSY3C_Ec?si=6vBWcwyUEeFOPr0p" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        """
    return render_template('scanner.html', recipies=recipies, name=name, img='http://127.0.0.1:5000/static/'+name+'.png', video1=video1, video2=video2)

@app.route('/recipe')
def recipe():
    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()
    query = """
        SELECT * 
        FROM items
        WHERE DATE(ed) = DATE('now', '+1 day') or DATE(ed) = DATE('now', '+2 day');
    """
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        results = list(results[-1])

        print(results)

        name = results[1]
        img = results[2]

        f = open(name+'.txt', 'r')
        recipies = f.read()
        f.close()
        print(recipies)
        msg = f"{name} is going to expire in one day"
        print(msg)
        bot = telepot.Bot('7995629621:AAHPwcfJuL1s6qc8N9nUrT1dtPACSrtoEpU')
        bot.sendMessage('5571946462', str(msg))
        if name == 'paneer':
            video1 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/U1LVDFwi8qI?si=HpvQCkVFMXkK8ZLI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """

            video2 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/BwIJHI4KdIE?si=1piargeJ2IJfHQDE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """

        elif name == 'mushroom':
            video1 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/Yu_mkN65E1I?si=KhROZTzESrm3xgmm" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """
            video2 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/rTLMj6FEo20?si=HxwuPbtJmuPqgRIG" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """

        elif name == 'chicken':
            video1 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/dRW3VMfNlaY?si=NLl_OGyjkkkdH1vj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """
            video2 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/F0WJ107nEwg?si=eHMetfZgb0gowbJ5" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """

        elif name == 'mutton':
            video1 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/P2SGDHHelis?si=TvxvEFoWiAdaUsJQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """
            video2 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/jn69U8Kf5Qg?si=XyM_IZedyV5IhLm-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """

        elif name == 'fish':
            video1 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/o8lDCY2_jyw?si=v6niMbGvC2V4ip9e" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """
            video2 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/nV_0srDzbFg?si=nyNvK_gF39VHUceV" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """

        elif name == 'prawns':
            video1 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/4xjE3OhkD0I?si=h6Z5YakQlDhG2k8m" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """
            video2 = """
                <iframe style="width:100%;" height="315" src="https://www.youtube.com/embed/LVOZSY3C_Ec?si=6vBWcwyUEeFOPr0p" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            """
        return render_template('recipi.html', recipies=recipies, name=name, img=img, video1=video1, video2=video2)
    else:
        return render_template('recipi.html', msg="no items to come expire")
        
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM user WHERE email = '"+email+"' AND password= '"+password+"'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            session['phone'] = result[2]
            return render_template('userlog.html')
        else:
            return render_template('signin.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('signin.html', msg='Successfully Registered')
    
    return render_template('signup.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
        md = request.form['md']
        ed = request.form['ed']

        file_content = image.read()
        my_string = base64.b64encode(file_content).decode('utf-8')

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        cursor.execute("insert into items values (NULL, ?,?,?,?)", [name, my_string, md, ed])
        connection.commit()

        return render_template('userlog.html', msg='item added successfully')
    return render_template('userlog.html')

@app.route('/support', methods=['GET', 'POST'])
def support():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
        md = request.form['md']
        ed = request.form['ed']
        phone = request.form['phone']

        file_content = image.read()
        my_string = base64.b64encode(file_content).decode('utf-8')

        cursor.execute("insert into DonateItems values (NULL, ?,?,?,?,?)", [name, my_string, md, ed, phone])
        connection.commit()

        cursor.execute("SELECT * FROM DonateItems")
        results = cursor.fetchall()
        
        return render_template('support.html', results=results)
    cursor.execute("SELECT * FROM DonateItems")
    results = cursor.fetchall()
    return render_template('support.html', results=results)

@app.route('/Request/<name>')
def Request(name):
    msg = f"request for {name} from {session['phone']}"
    print(msg)
    bot = telepot.Bot('7995629621:AAHPwcfJuL1s6qc8N9nUrT1dtPACSrtoEpU')
    bot.sendMessage('5571946462', str(msg))
    return render_template('userlog.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
