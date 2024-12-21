
### Project Directory
![Screenshot 2024-12-20 171526](https://github.com/user-attachments/assets/102e02b7-cd3d-467a-91ed-3ab307de15e8)


'''CREATIVE_AD_GENERATOR/
│
├── backend/
│   ├── __pycache__/
│   ├── api/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── input_contract.json
│   │   ├── output_contract.json
│   │   ├── scoring_logic.py
│   │   └── stable_diffusion_api.py
│   ├── assets/                     # Temporary assets folder
│   └── utils/                      # Utility functions (not visible in screenshot)
│
├── cag/                            # Root folder or package for the project
│
├── frontend/
│   └── frontend_ui.py
│
├── tests/
│   └── test_api.py
│
├── .env                            # Environment variables for sensitive data
├── README.md                       # Project documentation
├── main.py                         # Entry point for the application
└── requirements.txt                # Dependency file


- Make sure your project directory looks like above. then 

- Create an environment

- pip install -r re


To run (for backend):
1. New terminal
2. activate environment  , command -> envname\Scripts\Activate
3. cd backend
4. uvicorn app:app --reload (this should run the backend)

For frontend:
1. New terminal
2. acitvate environment
3. cd frontend
4. streamlit run frontend_ui.py, Navigate to the link
