# Facial Expression Recognition Based Restaurant Rating System

A deep learning-based local system that analyzes customer facial expressions to provide restaurant ratings and feedback. This system uses facial expression recognition to automatically detect customer satisfaction levels and generate ratings.

## Features

- Real-time facial expression recognition
- Automatic rating generation based on customer emotions
- Admin dashboard for viewing and managing ratings
- Detailed statistics and analytics
- Photo capture and storage functionality
- Responsive and modern UI design

## Technologies Used

- Python 3.x
- Django Framework
- OpenCV
- Keras/TensorFlow
- MySQL Database
- Bootstrap 5
- HTML5/CSS3/JavaScript

## Prerequisites

- Python 3.x
- MySQL Server
- OpenCV
- Keras/TensorFlow
- Required Python packages (listed in requirements.txt)

## Local Setup

1. Set up MySQL database:
   - Create a database named 'facial'
   - Default credentials: 
     - username: root
     - password: root
     - (You can modify these in views.py if needed)

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the local development server:
```bash
python manage.py runserver
```

4. Access the application locally at `http://localhost:8000`

## Admin Access
- Username: admin
- Password: admin

## Project Structure

```
facial-expression-rating/
├── FacialApp/
│   ├── static/
│   │   └── photo/         # Customer photos storage
│   ├── templates/         # HTML templates
│   ├── views.py          # View functions
│   ├── urls.py           # URL routing
│   └── models.py         # Database models
├── manage.py
└── requirements.txt
```

## Features in Detail

### Customer Rating System
- Capture customer photos
- Analyze facial expressions
- Generate automatic ratings
- Store customer feedback

### Admin Dashboard
- View all ratings
- Delete ratings
- View statistics
- Filter and search ratings

### Analytics
- Total reviews
- Satisfaction percentage
- Average ratings
- Monthly review statistics

## Note
This is a local application intended to run on your own machine. It is not configured for public hosting or deployment.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- OpenCV for image processing
- Keras/TensorFlow for deep learning models
- Django framework
- Bootstrap for UI components

## Contact

Ayub_07 - iamayub007@gmail.com
