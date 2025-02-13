# Gus First Project

## Project Description
[Brief description of what your project does]

## Project Structure 

gaussian_mixed_model_mms/

├── data/

│ ├── processed/
│ └── raw/

├── models/
│ └── gmm_v1.py

├── scripts/
│ └── feature_engineering.py

├── requirements.txt
├── Dockerfile
└── README.md

## Setup and Installation
1. Clone the repository:

bash
git clone https://github.com/YOUR_USERNAME/gaussian_mixed_model_mms.git
cd gaussian_mixed_model_mms


2. Install dependencies:

bash:README.md
pip install -r requirements.txt

3. Using Docker:

bash
docker build -t gaussian_mixed_model_mms .
docker run -v $(pwd)/data:/gaussian_mixed_model_mms/data gaussian_mixed_model_mms


## Usage
TBA

