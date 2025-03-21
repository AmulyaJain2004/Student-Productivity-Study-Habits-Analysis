student-habit-analysis/
│── backend/                         # Django + Django REST API
│   ├── student_analysis/            # Main Django app
│   │   ├── models.py                # Database models (SQLite/PostgreSQL)
│   │   ├── views.py                 # API endpoints
│   │   ├── serializers.py           # Django REST Framework serializers
│   │   ├── urls.py                  # API routes
│   │   ├── admin.py                 # Admin configurations
│   │   ├── tests.py                 # Unit tests for backend
│   ├── settings.py                   # Django settings
│   ├── urls.py                        # Project-level URL configuration
│   ├── wsgi.py / asgi.py             # WSGI/ASGI entry point
│   ├── manage.py                     # Django command-line tool
│
│── ml_service/                       # FastAPI ML microservice
│   ├── model/                        # Trained ML models (pickled)
│   │   ├── student_performance.pkl   # ML model to predict GPA/stress
│   ├── api/                          # FastAPI endpoints
│   │   ├── main.py                   # Main FastAPI server
│   ├── utils/                        # Helper functions for preprocessing
│   │   ├── preprocess.py             # Data preprocessing pipeline
│   │   ├── predict.py                # ML prediction functions
│   ├── requirements.txt              # Dependencies for FastAPI service
│
│── frontend/                         # React Frontend
│   ├── src/
│   │   ├── components/               # Reusable React components
│   │   ├── pages/                    # Different pages (Dashboard, Analysis)
│   │   ├── services/                 # API calls to backend & ML service
│   │   ├── App.js                    # Main App component
│   ├── public/                       # Static files
│   ├── package.json                  # Frontend dependencies
│
│── data/                             # Raw and processed data
│   ├── raw_data.csv                   # Collected data (Google Forms)
│   ├── cleaned_data.csv               # Preprocessed dataset
│   ├── feature_engineered.csv         # Data with new features
│
│── notebooks/                         # Jupyter notebooks for analysis
│   ├── EDA.ipynb                      # Exploratory Data Analysis
│   ├── Feature_Engineering.ipynb      # Feature Engineering
│   ├── Model_Training.ipynb           # Training ML models
│
│── scripts/                           # Python scripts for automation
│   ├── data_preprocessing.py          # Cleans & preprocesses dataset
│   ├── train_model.py                 # Trains ML models and saves them
│   ├── evaluate_model.py              # Evaluates trained models
│
│── requirements.txt                    # Dependencies
│── .env                                # Environment variables
│── README.md                           # Project documentation
│── Dockerfile                          # Docker configuration
│── docker-compose.yml                   # Container setup for deployment
│── .gitignore                           # Ignore unnecessary files