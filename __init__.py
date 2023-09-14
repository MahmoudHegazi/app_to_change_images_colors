from flask import Flask, jsonify,session,escape, request, abort, make_response, render_template,redirect, url_for, flash
from flask_socketio import SocketIO, emit
import socketio as xio
from flask_login import LoginManager
import os
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from .models import setup_db, Book, db
from PIL import Image
import glob
import secrets

book_per_page = 8

# empty session session.pop('username', None)


def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    login_manager = LoginManager()
    # old socket it look work but not work and use the app
    socketio = SocketIO(app)
    setup_db(app)
    CORS(app)
    # setup socketio
    sio = xio.Client()
    # any request on /api from out soruce any domain will accepted but not allow put
    cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})
    # CORS Headers


    @socketio.event
    def connect():
        print("I'm connected!")

    @socketio.event
    def connect_error(data):

        print("The connection failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")

    @socketio.event
    def my_event(sid, data):
        # handle the message
        return "a3ml eh typ", 123
    @app.after_request
    def after_request(response):
        #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        #response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    secret_key = secrets.token_hex(16)

    app.config.from_mapping(SECRET_KEY=secret_key,DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'))

    # my first socket
    app.config['SECRET_KEY'] = secret_key

    login_manager.init_app(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
         # load the test config if passed in
         app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    current_refresh = 0

    @app.before_request
    def make_session_permanent():
        session.permanent = False

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @sio.event
    def message(data):
        print('I received a message!')

    @sio.on('my message')
    def on_message(data):
        print('I received a message! nice thanks for calling function gj unique skill')

    @sio.on('my message')
    @app.route('/test_something')
    def tested():
        return str("ana astfdt eh")

    socektthings = False
    #if socektthings == False:
    #    sio.connect('http://localhost:5000/hair', wait_timeout = 10) what are u



    @app.route('/')
    @app.route('/home')
    def home():

        shape_color = None
        if "shape_color" in session:
            shape_color = session['shape_color']
        else:
            shape_color = None

        return render_template('index.html', shape_color=shape_color)


    @app.route('/visual_scraper')
    def visual():
        filename = os.path.join(app.root_path, 'static','images', 'target.JPG')
        ## rotate image

        with Image.open(filename).convert('RGB') as img:
            px = img.load()
            # rotate image by degress as you like full rotate
            img.rotate(180).show()


        xWidth=img.size[0]
        yHeight=img.size[1]
        allPixelsLeftToRightUpDown = []
        speed_unites = 0

        # get white lines in the images
        white_lines_location = []
        #         for i in white_lines_location:
        white_pixel_lines = 0
        white_range = 240
        black_range = 40
        total_white = 0
        total_black = 0
        # position of first object of the image pixel
        last_black = 0
        first_black = 0


        first_black_pos = ()
        last_black_pos = ()

        search_forFirst = True
        total_shadow_pixels = 0

        max_color = ()
        find_max = False
        target_shape = []
        for x in range(xWidth):
            line = []
            same_line = True
            previous_pixel = ()
            for y in range(yHeight):
                if find_max = False:
                    max_color = px[x,y]
                    target_shape = []
                else:
                    points = 0
                    if px[x,y][0] > max_color[0]:
                        points += 4
                    if px[x,y][1] > max_color[1]:
                        points += 4
                    if px[x,y][2] > max_color[2]:
                        points += 4
                    if px[x,y][0] == max_color[0]:
                        points += 1
                    if px[x,y][1] == max_color[1]:
                        points += 1
                    if px[x,y][2] == max_color[2]:
                        points += 1

                    if points >= 5:
                        max_color = px[x,y]
                        target_shape = []
                if px[x,y] == max_color:
                    target_shape.append((x, y))
        return jsonify(target_shape)

    @app.route('/image_processing', methods=["POST"])
    def image_processing():
        if request.method == "POST":
            if "shape_color" not in request.json:
                return jsonify({"code": 400, "data": request.json, "message": "invalid Color sent please refresh app"})

            requestData = request.json
            shape_color = requestData["shape_color"]
            newShapeColor = ()

            if shape_color.strip() != '':
                rgbList = shape_color.replace(" ","").split(",")
                if len(rgbList) == 3:
                    newShapeColor = (int(rgbList[0]),int(rgbList[1]),int(rgbList[2]))
                else:
                    return jsonify({"code": 400, "data": request.json, "message": "invalid Color sent please refresh app"})
            else:
                return jsonify({"code": 400, "data": request.json, "message": "invalid Color sent please refresh app"})

            session['shape_color'] = newShapeColor


            # simple app to dedct numbers from 0 to 9 using digital single image for each number static app
            #books = Book.query.all()
            #formated_books = [book.format() for book in books]
            #result = Book.format(books)
            #book = Book.query.filter_by(title='Hi').first()
            #book = Book.query.all() formated_books
            blackwhite_flower = os.path.join(app.root_path, 'static','images', 'asyou_like.jpg')
            simi_full_colored = os.path.join(app.root_path, 'static','images', 'letsee.jpg')
            filename = os.path.join(app.root_path, 'static','images', 'full_digital_num.png')

            ## rotate image

            with Image.open(filename).convert('RGB') as img:
                px = img.load()
                # rotate image by degress as you like full rotate
                img.rotate(180).show()

            # free pixel drawing in image can used to add words for example or other images on this image image widht height and black points and white points and loop in square
            px[0,1] = (55, 120, 120)
            px[0,2] = (55, 120, 120)
            px[0,3] = (55, 120, 120)
            px[0,4] = (55, 120, 120)
            px[0,5] = (55, 120, 120)
            px[1,1] = (55, 120, 120)
            px[1,2] = (55, 120, 120)
            px[1,3] = (55, 120, 120)
            px[1,4] = (55, 120, 120)
            px[1,5] = (55, 120, 120)

            xWidth=img.size[0]
            yHeight=img.size[1]
            allPixelsLeftToRightUpDown = []
            speed_unites = 0

            # get white lines in the images
            white_lines_location = []
            #         for i in white_lines_location:
            white_pixel_lines = 0
            white_range = 240
            black_range = 40
            total_white = 0
            total_black = 0
            # position of first object of the image pixel
            last_black = 0
            first_black = 0


            first_black_pos = ()
            last_black_pos = ()

            search_forFirst = True
            total_shadow_pixels = 0
            for x in range(xWidth):
                line = []
                same_line = True
                previous_pixel = ()
                for y in range(yHeight):
                    if px[x,y][0] >= white_range and px[x,y][1] >= white_range and px[x,y][2] >= white_range:
                        # total white color in image
                        total_white += 1
                    elif px[x,y][0] <= black_range and px[x,y][1] <= black_range and px[x,y][2] <= black_range:
                        # total black color in image
                        # change shape color
                        px[x,y] = session['shape_color']
                        total_black += 1
                        if search_forFirst:
                            first_black = "First black point in the word at position [{},{}]".format(x, y)
                            first_black_pos = (x, y)
                            search_forFirst = False
                        last_black = "Last black point in the word at position [{},{}]".format(x, y)
                        last_black_pos = (x, y)
                    else:
                        # others some times used to helight shape
                        # add shadow layers nice effect
                        px[x,y] = (255, 233, 92)
                        px[x-1,y] = (0, 150, 60)
                        px[x-2,y] = (255, 102, 255)
                        px[x-3,y] = (255, 102, 255)
                        px[x-4,y] = (255, 102, 255)
                        # total not black and not white colors in images
                        total_shadow_pixels += 1

                    if y == 0:
                        previous_pixel = px[x,y]
                    allPixelsLeftToRightUpDown.append("Point At X:{} and at Y{} color Is {}".format(x, y, px[x,y]))
                    speed_unites += 1
                    line.append(px[x,y])

                    # check line empty
                    if y > 0:
                        if px[x,y] != previous_pixel:
                            same_line = False
                            previous_pixel = px[x,y]
                        else:
                            previous_pixel = px[x,y]
                # check if line was white or same color bu ok white range
                if same_line == True and previous_pixel[0] >= white_range and previous_pixel[1] >= white_range and previous_pixel[2] >= white_range:
                    white_pixel_lines += 1
                    white_lines_location.append({'place': x, 'max': xWidth})
            img.show()
            # after anlysis get what you need
            # search for the length of first line and get where it start and end make sure
            # there must be refrence (eight is the refrence for line width)

            # get the width for top part of digital number to dedct it

            #px[4,4] = (15, 150, 150)
            #return str(img[0].size)
            shape_width = last_black_pos[0] - first_black_pos[0]
            shape_height = last_black_pos[1] - first_black_pos[1]

            # shape session color
            current_shape_color = None
            if 'shape_color' in session:
                current_shape_color = session['shape_color']
            else:
                current_shape_color = ""

            removed_files = None
            if 'current_refresh' in session:
                removed_files = session['current_refresh']
            else:
                removed_files = None

            return jsonify({
                            'code':200,
                            "message": "proccessed successfully",
                            "data": {
                                'time':speed_unites,
                                'total_white_lines': white_pixel_lines,
                                'white_lines_location': white_lines_location,
                                'allPixelsLeftToRightUpDown': len(allPixelsLeftToRightUpDown),
                                'total_white_pixels': total_white,
                                'total_black_pixels': total_black,
                                'total_shadow_pixels': total_shadow_pixels,
                                'image_content_start_at': first_black,
                                'image_content_end_at': last_black,
                                'shape_width_dynamicly_identify': shape_width,
                                'shape_height_dynamicly_identify': shape_height,
                                'current_shape_color': current_shape_color,
                                'removed_files': removed_files,
                                }
                            })
    @app.route('/hair')
    def imagePartsDetect():
        # simple app to dedct numbers from 0 to 9 using digital single image for each number static app (trying achive imageToText)
        #books = Book.query.all()
        #formated_books = [book.format() for book in books]
        #result = Book.format(books)
        #book = Book.query.filter_by(title='Hi').first()
        #book = Book.query.all() formated_books
        faceimage = os.path.join(app.root_path, 'static','images', 'face1.jpg')
        filename = os.path.join(app.root_path, 'static','images', 'full_digital_num.png')
        filename1 = os.path.join(app.root_path, 'static','images', 'info.JPG')

        ## rotate image
        with Image.open(filename).convert('RGB') as img:
            px = img.load()
            # rotate image by degress as you like full rotate
            #img.rotate(180).show()

        # free pixel drawing in image can used to add words for example or other images on this image image widht height and black points and white points and loop in square

        xWidth=img.size[0]
        yHeight=img.size[1]
        allPixelsLeftToRightUpDown = []
        speed_unites = 0

        # get white lines in the images
        white_lines_location = []
        #         for i in white_lines_location:
        white_pixel_lines = 0
        white_range = 240
        black_range = 70
        gray_range = 150
        total_white = 0
        total_black = 0
        # position of first object of the image pixel
        last_black = 0
        first_black = 0


        first_black_pos = ()
        last_black_pos = ()

        search_forFirst = True
        total_shadow_pixels = 0

        #step 3 deadct how many colors in the images and list
        all_colors = []
        project_data = []


        image_objects = []
        image_temp_obj = []
        old_x = 0
        old_y = 0
        objects_index = 0
        loop_index = 0
        squ = 0
        is_long_part = 0

        hair_size = 0
        background_color = ()
        found_background = False
        gray_color = ()
        found_gray = False

        columns = []
        loop_index1 = 0

        white_column = 0




        for x in range(xWidth):
            line = []
            same_line = True
            previous_pixel = ()
            column_cell_index = 0
            loop_index1 += 1
            for y in range(yHeight):

                if loop_index1 == 1:
                    columns.append([])
                    columns[column_cell_index].append(px[x,y])
                else:
                    columns[column_cell_index].append(px[x,y])


                loop_index += 1
                # detect how many unqiue color in the image that will used to change needed
                # next step get prcentage of how this color aginset image maybe add something [30%, 28% ook same]
                if px[x,y][0] >= white_range and px[x,y][1] >= white_range and px[x,y][2] >= white_range:
                    # total white color in image
                    total_white += 1
                    if found_background == False:
                        background_color = px[x,y]
                        found_background = True
                elif px[x,y][0] <= black_range and px[x,y][1] <= black_range and px[x,y][2] <= black_range:

                    # total black color in image
                    # change shape color
                    #px[x,y] = (199, 172, 0)
                    total_black += 1
                    if search_forFirst:
                        first_black = "First black point in the word at position [{},{}]".format(x, y)
                        first_black_pos = (x, y)
                        search_forFirst = False
                    last_black = "Last black point in the word at position [{},{}]".format(x, y)
                    last_black_pos = (x, y)

                    # try get equal sequence
                    #if found_background:
                    px[x,y] = (222, 150, 150)
                    """
                    if squ == 0:
                        squ += 30
                        newObj = {'positions': [], 'total_points': 0, 'index':0}
                        newObj['positions'].append((x, y))
                        newObj['total_points'] += 1
                        image_objects.append(newObj)
                    else:
                        # hair
                        if y >= old_y and y - old_y <= 300 and y > (yHeight / 4) and y < (yHeight / 2) + (yHeight / 5):
                            if gray_color:
                                px[x,y] = gray_color
                            hair_size += 1

                        # change eyes and hair and extra black points not needed

                        if y >= old_y and y <= 300 and x - old_x < 2000:
                            px[x,y] = (150, 50, 120)
                            newObj = {'positions': [], 'total_points': 0, 'index':objects_index}
                            newObj['positions'].append((x, y))
                            newObj['total_points'] += 1
                            image_objects.append(newObj)
                        else:
                            px[x,y] = (150, 50, 120)
                            image_objects[objects_index]['positions'].append(px[x,y])
                            image_objects[objects_index]['total_points'] += 1
                        ##################
                        if squ < loop_index and loop_index - squ < 2000:
                            is_long_part += 1
                            if is_long_part >= 30:
                                is_long_part = 0
                                squ = loop_index + 30
                                image_objects[objects_index]['positions'].append(px[x,y])
                                image_objects[objects_index]['total_points'] += 1
                        elif squ < loop_index and loop_index - squ > 2000:
                            objects_index += 1
                            newObj = {'positions': [], 'total_points': 0, 'index':objects_index}
                            newObj['positions'].append((x, y))
                            newObj['total_points'] += 1
                            image_objects.append(newObj)
                        """


                    old_x = x
                    old_y = y
                else:
                    #px[x,y] = (px[x,y][0]+50, px[x,y][1]+50, px[x,y][2]+50)
                    if found_gray == False and px[x,y][0] <= gray_range and px[x,y][1] <= gray_range and  px[x,y][1] <= gray_range:
                        gray_color = px[x,y]
                        found_gray = True
                    if px[x,y] not in all_colors:
                        all_colors.append(px[x,y])
                        project_data.append({"index": len(all_colors)-1, "color": px[x,y], "total": 1})
                    else:
                        current_index = all_colors.index(px[x,y])
                        project_data[current_index]['total'] += 1
                    # others some times used to helight shape
                    # add shadow layers nice effect

                    #px[x-1,y] = (0, 150, 60)
                    #px[x-2,y] = (255, 102, 255)
                    #px[x-3,y] = (255, 102, 255)
                    #px[x-4,y] = (255, 102, 255)
                    # total not black and not white colors in images
                    total_shadow_pixels += 1

                if y == 0:
                    previous_pixel = px[x,y]
                allPixelsLeftToRightUpDown.append("Point At X:{} and at Y{} color Is {}".format(x, y, px[x,y]))
                speed_unites += 1
                line.append(px[x,y])

                # check line empty
                if y > 0:
                    if px[x,y] != previous_pixel:
                        same_line = False
                        previous_pixel = px[x,y]
                    else:
                        previous_pixel = px[x,y]
                column_cell_index += 1
            # check if line was white or same color bu ok white range
            if same_line == True and previous_pixel[0] >= white_range and previous_pixel[1] >= white_range and previous_pixel[2] >= white_range:
                white_pixel_lines += 1
                white_lines_location.append({'place': x, 'max': xWidth})
        img.show()
        # after anlysis get what you need
        # search for the length of first line and get where it start and end make sure
        # there must be refrence (eight is the refrence for line width)

        # get the width for top part of digital number to dedct it

        #px[4,4] = (15, 150, 150)
        #return str(img[0].size)
        shape_width = last_black_pos[0] - first_black_pos[0]
        shape_height = last_black_pos[1] - first_black_pos[1]

        for dataIndex in range(len(project_data)):
            color_precentage = (project_data[dataIndex]['total'] / len(allPixelsLeftToRightUpDown)) * 100
            project_data[dataIndex]['color_precentage'] = color_precentage

        #white columns

        for column in columns:
            white_column_index = 0

            for item in column:
                if item[0] >= white_range and item[1] >= white_range and item[2] >= white_range:
                    white_column_index += 1
            if white_column_index != 0 and white_column_index == len(column):
                white_column += 1
        # shape session color
        return jsonify({
                        'code':200,
                        "message": "proccessed successfully",
                        #'all_colors': all_colors,
                        'how many unqiue colors in the image?': len(all_colors),
                        'time':speed_unites,
                        'total_white_lines': white_pixel_lines,
                        #'white_lines_location': white_lines_location,
                        'allPixelsLeftToRightUpDown': len(allPixelsLeftToRightUpDown),
                        'total_white_pixels': total_white,
                        'total_black_pixels': total_black,
                        'total_shadow_pixels': total_shadow_pixels,
                        'image_content_start_at': first_black,
                        'image_content_end_at': last_black,
                        'shape_width_dynamicly_identify': shape_width,
                        'shape_height_dynamicly_identify': shape_height,
                        'hair_size': hair_size,
                        'white_columns': white_column
                        #'columns': columns,
                        #'project_data': project_data,
                        })
    """ (not related)
    def pagination_checker(page,selection):
        start = (page - 1) * book_per_page
        end = start + book_per_page
        formated_books = [book.format() for book in selection]
        pagie_list = formated_books[start:end]
        if len(pagie_list) == 0:
            return False
        else:
            return True

    def pagination_helper(request,selection):
        page = request.args.get('page',1,type=int)
        start = (page - 1) * book_per_page
        end = start + book_per_page
        formated_books = [book.format() for book in selection]
        pagie_list = formated_books[start:end]
        return pagie_list


    @app.route('/books')
    def page():
        last_page = 1
        books = Book.query.order_by('id').all()
        books_per_request = pagination_helper(request,books)
        books_count = len(books)
        books_in_request_count = len(books_per_request)
        if len(books_per_request) == 0:
            if books_count > book_per_page:
                last_page = round(int(books_count) / int(book_per_page))
                if (books_count / last_page) > book_per_page:
                    last_page = last_page + 1
            # this will return real server error not code and message defined use number to get any error
            #abort(404)
            response = make_response(jsonify(message="Hello, page paramter value exceeded books count try To solve it Last page is:%s" %last_page), 404)
            return response
        return jsonify({'code':200,'books':books_per_request,'total_books':books_count,'success':True})

    # update a book
    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):
        body = request.get_json()
        try:
            book = Book.query.filter_by(id=book_id).one_or_none()
            if book is None:
                response = make_response(jsonify(message="Hello, We Did not Found that book try another one"), 404)
                return response
            if 'rating' in body:
                book.rating = int(body.get('rating'))
            #return str(book.rating)
            book.update()
            return jsonify({'code':200,
            'id':book.id,
            'book_rating':book.rating,
            'success':True})
        except:
            response = make_response(jsonify(message="Hello, this is a Bad Request Error  the server was unable to process the request sent by the client due to invalid syntax "), 400)
            return response


    # delete a book
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter_by(id=book_id).one_or_none()
            if book is None:
                response = make_response(jsonify(message="Hello, We Did not Found that book try another one"), 404)
                return response

            book.delete()
            selection = Book.query.order_by('id').all()
            current_books = pagination_helper(request,selection)
            len_books = len(selection)
            return jsonify({'code':200,
            'success':True,
            'books':current_books,
            'total_books':len_books})
        except:
            response = make_response(jsonify(message="Hello, this is a Bad Request Error  the server was unable to process the request sent by the client due to invalid syntax "), 400)
            return response

    # create new Book
    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()
        # if title get it else make it None make sure title is nullable in DB
        title = body.get('title', None)
        author = body.get('author', None)
        rating = body.get('rating', None)
        try:
            newbook = Book(title=title, author=author,rating=rating)
            newbook.insert()

            selection = Book.query.order_by('id').all()
            current_books = pagination_helper(request, selection)
            len_books = len(selection)
            return jsonify({'code':200,'success':True,
            'books':current_books,'total_books':len_books,
            'created':newbook.id})
        except:
            response = make_response(jsonify(message="Hello, the server understands the content type of the request entity,\
            and the syntax of the request entity is correct, but it was unable to process the contained instructions"), 422)
            return response
        #print('Data Received: "{data}"'.format(data=data))

    # handle form request
    @app.route('/form', methods=['POST'])
    def home_form():
            if request.method == 'POST':
                x = request.form['hello']
                return jsonify({'messsage':x})
    # handle file request
    @app.route('/file', methods=['POST'])
    def home_file():
            if request.method == 'POST':

                file = request.files['test']
                filename=secure_filename(file.filename)
                return jsonify({'messsage':filename})
    """

    return app
