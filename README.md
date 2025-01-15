# AI Documentation Generator

An intelligent system that automatically generates comprehensive business and technical documentation using AI agents.



## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd AI_Docs_Generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
# Start the backend
cd backend
uvicorn main:app --reload

# In a new terminal, start the frontend
npm run dev
```

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when running the server.

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Cloud API key
- `GEMINI_MODEL_NAME`: The Gemini model to use (default: gemini-2.0-flash)
- `API_V1_STR`: API version prefix
- `PROJECT_NAME`: Project name for API documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 