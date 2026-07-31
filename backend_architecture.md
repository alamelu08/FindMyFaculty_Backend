```text
backend/
│
├── app/
│   │
│   ├── core/
│   │   ├── config.py         
│   │   ├── security.py        
│   │   └── auth.py           
│   │
│   ├── database/
│   │   ├── database.py        
│   │   └── session.py         
│   │
│   ├── models/
│   │   ├── faculty.py
│   │   ├── faculty_timetable.py
│   │   └── period.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── faculty.py
│   │   ├── location.py
│   │   └── upload.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── faculty.py
│   │   ├── admin.py
│   │   └── upload.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── faculty_service.py
│   │   ├── timetable_service.py
│   │   └── pdf_parser.py
│   │
│   ├── utils/
│   │   └── current_period.py
│   │
│   └── main.py
│
├── uploads/                  
│
├── requirements.txt
│
└── README.md
```
