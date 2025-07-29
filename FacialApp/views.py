from django.shortcuts import render
from django.template import RequestContext
import pymysql
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
import cv2
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np


def Index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def User(request):
    if request.method == 'GET':
       return render(request, 'User.html', {})

def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})

def AdminLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'admin' and password == 'admin':
       context= {'data':'welcome '+username}
       return render(request, 'AdminScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Admin.html', context)

def ViewRating(request):
    if request.method == 'GET':
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'facial',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM rating")
            rows = cur.fetchall()
            
            # Calculate statistics
            total_reviews = len(rows)
            satisfied_count = sum(1 for row in rows if row[2] == 'Satisfied')
            satisfied_percentage = (satisfied_count / total_reviews * 100) if total_reviews > 0 else 0
            
            # Calculate average rating
            total_rating = sum(float(row[1]) for row in rows)
            average_rating = round(total_rating / total_reviews, 1) if total_reviews > 0 else 0
            average_rating_percentage = (average_rating / 5 * 100)
            
            # Calculate monthly reviews
            current_month = datetime.datetime.now().month
            monthly_reviews = sum(1 for row in rows if datetime.datetime.strptime(str(row[4]), "%Y-%m-%d %H:%M:%S").month == current_month)
            monthly_percentage = (monthly_reviews / total_reviews * 100) if total_reviews > 0 else 0
            
            # Format table data
            table_data = '<table class="table table-hover"><thead><tr><th>Customer Name</th><th>Expression</th><th>Photo</th><th>Date & Time</th><th>Actions</th></tr></thead><tbody>'
            for row in rows:
                # Create expression badge
                badge_class = {
                    'Satisfied': 'bg-success',
                    'Neutral': 'bg-warning',
                    'Disappointed': 'bg-danger'
                }.get(row[2], 'bg-secondary')
                
                table_data += f'''
                    <tr>
                        <td>{row[0]}</td>
                        <td><span class="badge {badge_class}">{row[2]}</span></td>
                        <td><img src="/static/photo{row[0]}.png" class="customer-photo" alt="Customer" onclick="showFullImage(this.src)"></td>
                        <td>{row[4]}</td>
                        <td>
                            <button class="btn btn-danger btn-sm" onclick="deleteRating('{row[0]}', '{row[4]}')">
                                <i class="fas fa-trash-alt"></i> Delete
                            </button>
                        </td>
                    </tr>
                '''
            table_data += '</tbody></table>'
            
            context = {
                'data': table_data,
                'total_reviews': total_reviews,
                'satisfied_count': satisfied_count,
                'satisfied_percentage': round(satisfied_percentage, 1),
                'average_rating': average_rating,
                'average_rating_percentage': round(average_rating_percentage, 1),
                'monthly_reviews': monthly_reviews,
                'monthly_percentage': round(monthly_percentage, 1)
            }
            
            return render(request, 'ViewRatings.html', context)

def DeleteRating(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        rating_date = request.POST.get('rating_date')
        
        if not customer_name or not rating_date:
            return HttpResponse('Missing required parameters')
        
        try:
            # Connect to database
            con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'facial',charset='utf8')
            with con:
                cur = con.cursor()
                # Delete the rating
                cur.execute("DELETE FROM rating WHERE customer_name = %s AND rating_date = %s", (customer_name, rating_date))
                con.commit()
                
                if cur.rowcount > 0:
                    # Try to delete the associated photo
                    try:
                        import os
                        photo_path = os.path.join(settings.BASE_DIR, 'FacialApp', 'static', 'photo', f'{customer_name}.png')
                        if os.path.exists(photo_path):
                            os.remove(photo_path)
                    except Exception as photo_error:
                        print(f"Error deleting photo: {photo_error}")
                    
                    return HttpResponse('success')
                else:
                    return HttpResponse('Rating not found')
                
        except Exception as e:
            print(f"Error in DeleteRating: {str(e)}")
            return HttpResponse(f"Database error: {str(e)}")
    
    return HttpResponse('Invalid request method')

def Rating(request):
     if request.method == 'POST' and request.FILES['t3']:
        output = ''
        myfile = request.FILES['t3']
        name = request.POST.get('t1', False)
        rating = request.POST.get('t2', False)
        fs = FileSystemStorage()
        filename = fs.save(r'C:\Users\Mohammed Ayub\Desktop\2. A Deep Learning Facial Expression Recognition Based Scoring System For Restaurants\FacialApp\static\photo'+name+'.png', myfile)
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        detection_model_path = r'c:\Users\Mohammed Ayub\Desktop\2. A Deep Learning Facial Expression Recognition Based Scoring System For Restaurants\FacialApp\haarcascade_frontalface_default.xml'
        emotion_model_path = r'C:\Users\Mohammed Ayub\Desktop\2. A Deep Learning Facial Expression Recognition Based Scoring System For Restaurants\FacialApp\_mini_XCEPTION.106-0.65.hdf5'
        face_detection = cv2.CascadeClassifier(detection_model_path)
        emotion_classifier = load_model(emotion_model_path, compile=False)
        EMOTIONS = ["angry","disgust","scared", "happy", "sad", "surprised","neutral"]
        orig_frame = cv2.imread(r'C:\Users\Mohammed Ayub\Desktop\2. A Deep Learning Facial Expression Recognition Based Scoring System For Restaurants\FacialApp\static\photo'+name+'.png')
        orig_frame = cv2.resize(orig_frame, (48, 48))
        frame = cv2.imread(filename,0)
        faces = face_detection.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
        print("==================="+str(len(faces)))   
        print(emotion_classifier)
        if len(faces) > 0:
            faces = sorted(faces, reverse=True,key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            roi = frame[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]
            if label == 'happy':
               output = 'Satisfied'
            if label == 'neutral':
               output = 'Neutral'
            if label == 'angry' or label == 'sad' or label == 'disgust' or label == 'scared' or label == 'surprised':
               output = 'Disappointed'
        print("==================="+output)	
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'facial',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO rating(customer_name,rating,facial_expression,photo_path,rating_date) VALUES('"+name+"','"+rating+"','"+output+"','"+name+'.png'+"','"+current_time+"')"
        db_cursor.execute(query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context= {'data':'Your Rating is : '+rating+' and Facial Expression : '+output}
            return render(request, 'User.html', context)
        else:
            context= {'data':'Error in request process'}
            return render(request, 'User.html', context)
       