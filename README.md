# FAQ Chatbot

A professional FAQ chatbot application built with FastAPI, SpaCy, and TF-IDF cosine similarity matching. Features a modern web-based chat interface for interactive question-answering.

## Features

- 🤖 **Intelligent Matching**: Uses TF-IDF vectorization and cosine similarity to find the best matching FAQ
- 🧠 **NLP Processing**: Leverages SpaCy for advanced text preprocessing (tokenization, lemmatization, stopword removal)
- 💬 **Modern UI**: Beautiful, responsive web-based chat interface
- ⚡ **Fast & Efficient**: Simple logic with high performance
- 📊 **Confidence Scoring**: Displays confidence scores for each answer
- 🔍 **RESTful API**: Clean API endpoints for integration

## Project Structure

```
arhamlab-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic data models
│   ├── chatbot.py           # Core chatbot logic (NLP, matching)
│   └── utils.py             # Utility functions
├── static/
│   ├── css/
│   │   └── style.css        # Professional UI styling
│   └── js/
│       └── chat.js          # Frontend chat interface logic
├── templates/
│   └── index.html           # Main chat UI page
├── data/
│   └── faqs.json            # FAQ data file
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## FAQ Data Format

The FAQ data should be stored in `data/faqs.json` with the following structure:

```json
{
  "faqs": [
    {
      "id": 1,
      "question": "What is your return policy?",
      "answer": "We offer a 30-day return policy...",
      "category": "Returns"
    },
    {
      "id": 2,
      "question": "How long does shipping take?",
      "answer": "Standard shipping typically takes 5-7 business days...",
      "category": "Shipping"
    }
  ]
}
```

### Fields:
- **id** (required): Unique identifier for each FAQ
- **question** (required): The question text
- **answer** (required): The answer text
- **category** (optional): Category/group for the FAQ

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download SpaCy English model** (choose one method):
   
   **Important:** Make sure your virtual environment is activated before installing the model!

   **Method 1 - Using pip directly (Recommended):**
   ```bash
   pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
   ```

   **Method 2 - Using spacy CLI (alternative):**
   ```bash
   python -m spacy download en_core_web_sm
   ```
   
   **Note:** If Method 2 gives a 404 error, use Method 1 instead.

## Running the Application

1. **Start the FastAPI server**:
```bash
uvicorn app.main:app --reload
```

2. **Open your browser** and navigate to:
```
http://localhost:8000
```

3. **API Documentation** (Swagger UI):
```
http://localhost:8000/docs
```

## API Endpoints

### `GET /`
Serves the chat UI interface.

### `POST /api/chat`
Processes user questions and returns the best matching FAQ answer.

**Request Body:**
```json
{
  "question": "What is your return policy?"
}
```

**Response:**
```json
{
  "answer": "We offer a 30-day return policy...",
  "confidence": 0.856,
  "matched_question": "What is your return policy?",
  "category": "Returns"
}
```

### `GET /api/faqs`
Returns all FAQs (for debugging/testing).

### `GET /api/health`
Health check endpoint.

## How It Works

1. **Text Preprocessing**: User questions and FAQ questions are preprocessed using SpaCy:
   - Converted to lowercase
   - Tokenized
   - Lemmatized (words reduced to root form)
   - Stopwords removed
   - Punctuation removed

2. **TF-IDF Vectorization**: Preprocessed text is converted to TF-IDF vectors, which represent the importance of words in the document corpus.

3. **Cosine Similarity**: The user's question vector is compared against all FAQ question vectors using cosine similarity to find the best match.

4. **Response**: The answer from the best matching FAQ is returned, along with a confidence score.

## Customization

### Adding Your Own FAQs

Replace the content in `data/faqs.json` with your own FAQ data following the specified format.

### Adjusting Matching Threshold

In `app/chatbot.py`, modify the `threshold` parameter in the `find_best_match` method (default: 0.1) to adjust the minimum similarity required for a match.

### Styling

Customize the appearance by editing `static/css/style.css`. The CSS uses CSS variables for easy theming.

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **SpaCy**: Advanced NLP library for text processing
- **scikit-learn**: Machine learning library for TF-IDF and cosine similarity
- **Uvicorn**: ASGI server for running FastAPI
- **HTML/CSS/JavaScript**: Frontend technologies for the chat UI

## License

This project is open source and available for use.

## Support

For issues or questions, please contact the development team.

