# Agentic Deep Search App

An intelligent research assistant that transforms user queries into comprehensive reports through automated web search and AI-powered synthesis.

## 🚀 Features

- **Intelligent Query Processing**: Advanced natural language understanding to analyze research intent
- **Smart Clarification**: Generates 3 targeted questions to refine research scope
- **Comprehensive Web Search**: Executes 20 strategic DuckDuckGo searches for thorough coverage
- **AI-Powered Synthesis**: Uses Gemini 2.5 Flash to synthesize findings into professional reports
- **PowerPoint Schema**: Optional presentation-ready slide structure generation
- **Real-time Progress**: Live updates showing search progress and processing stages
- **Privacy-Focused**: No user data storage, DuckDuckGo for private searching
- **Easy Downloads**: Export reports in markdown format and PowerPoint schemas

## 🛠️ Tech Stack

- **Frontend**: Gradio for responsive web interface
- **AI Framework**: LangChain for agent orchestration
- **Search Engine**: DuckDuckGo via LangChain tools
- **AI Model**: Gemini 2.5 Flash via OpenAI SDK
- **Data Validation**: Pydantic for schema management
- **Hosting**: Hugging Face Spaces

## 🧪 Development

This project uses modern Python development tools to ensure code quality and consistency.

### Pre-commit Hooks

The project is configured with pre-commit hooks that automatically run code quality checks before each commit:

- **Ruff**: Fast Python linter and formatter
- **Pytest**: Automatic test execution
- **File validation**: YAML, JSON, TOML syntax checking
- **Code cleanup**: Trailing whitespace removal, end-of-file fixes

### Manual Development Commands

```bash
# Manual runs (optional)
uv run ruff check . --fix     # Run linting with auto-fix
uv run ruff format .          # Format code
uv run pytest               # Run tests
uv run pre-commit run --all-files  # Run all hooks

# Automatic runs
git commit -m "message"      # Hooks run automatically before commit
```

#### Command Explanations:

- **`uv run ruff check . --fix`**: Analyzes your Python code for style issues, potential bugs, and automatically fixes problems like unused imports, spacing issues, and import sorting
- **`uv run ruff format .`**: Formats your code consistently with proper indentation, line length (88 chars), and quote style (double quotes)
- **`uv run pytest`**: Runs all tests in the `tests/` directory to ensure your changes don't break existing functionality
- **`uv run pre-commit run --all-files`**: Manually runs all configured hooks on every file in the project
- **`git commit -m "message"`**: When you commit, pre-commit hooks automatically run and must pass before the commit succeeds

### Testing

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests with coverage
pytest --cov=src tests/

# Run tests in verbose mode
pytest -v
```

### Code Quality Standards

- **Line length**: 88 characters maximum
- **Quote style**: Double quotes for strings
- **Import sorting**: Automatic with ruff
- **Type hints**: Encouraged for better code documentation
- **Documentation**: Docstrings for all public functions and classes

## 📋 Requirements

- Python 3.12.9
- API key for Gemini 2.5 Flash (via OpenAI SDK)
- Internet connection for web searches

## 🔧 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd deep_search
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   DEBUG=false
   LOG_LEVEL=INFO
   ```

   **Environment Variable Explanations:**

   - **`GEMINI_API_KEY`**: Your Gemini 2.5 Flash API key (required for AI functionality)

   - **`DEBUG`**: Development mode flag
     - `true`: Development mode - verbose errors, hot reload, detailed logging
     - `false`: Production mode - user-friendly errors, performance optimized

   - **`LOG_LEVEL`**: Controls logging verbosity
     - `DEBUG`: Most verbose - shows all debug traces and messages
     - `INFO`: Standard level - shows informational messages and above (recommended)
     - `WARNING`: Shows only warnings, errors, and critical messages
     - `ERROR`: Shows only errors and critical system failures
     - `CRITICAL`: Shows only critical system failures

   **Configuration Examples:**

   ```bash
   # Development environment
   DEBUG=true
   LOG_LEVEL=DEBUG
   GEMINI_API_KEY=your_api_key_here

   # Production environment
   DEBUG=false
   LOG_LEVEL=INFO
   GEMINI_API_KEY=your_api_key_here

   # Troubleshooting environment
   DEBUG=false
   LOG_LEVEL=WARNING
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

### Hugging Face Spaces Deployment

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Select **Gradio SDK**
3. Upload your code files
4. Add your `OPENAI_API_KEY` in Space settings → Variables and secrets
5. The Space will automatically build and deploy

## 🎯 Usage

1. **Enter your research query** in the main text field
2. **Answer clarification questions** to refine your research scope (optional)
3. **Choose PowerPoint schema** if you want presentation-ready output
4. **Click "Run Research"** and monitor real-time progress
5. **Review the generated report** with comprehensive findings
6. **Download** your report and/or PowerPoint schema

### Example Queries

- "What are the latest trends in sustainable packaging for the food industry?"
- "How is artificial intelligence being used in healthcare diagnostics?"
- "What are the cybersecurity challenges for remote work in 2024?"

## 📊 Project Structure

```
deep_search/
├── src/                    # Main application code
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
├── examples/               # Usage examples
├── app.py                  # Main Gradio application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore patterns
```

## 🔍 How It Works

1. **Query Analysis**: The system analyzes your research query to understand intent and scope
2. **Clarification**: Generates 3 targeted questions to refine the research parameters
3. **Search Strategy**: Creates 20 diverse search queries based on your input and clarifications
4. **Web Search**: Executes searches using DuckDuckGo for privacy-focused results
5. **Content Processing**: Extracts and filters relevant information from search results
6. **AI Synthesis**: Uses Gemini 2.5 Flash to synthesize findings into a coherent report
7. **Report Generation**: Formats the research into a professional markdown report
8. **Schema Creation**: Optionally generates PowerPoint slide structure and talking points

## 🎨 User Interface

The application features a clean, intuitive Gradio interface with:

- **Query Input**: Large text area for research questions
- **Clarification Section**: Dynamic questions with optional responses
- **PowerPoint Option**: Simple checkbox to enable schema generation
- **Progress Tracking**: Real-time updates with progress bars and status messages
- **Results Display**: Formatted report with collapsible sections
- **Download Buttons**: Easy access to generated files

## 🔐 Privacy & Security

- **No Data Storage**: All processing is session-based with no persistent storage
- **Private Search**: Uses DuckDuckGo for privacy-focused web searching
- **Secure API Handling**: API keys managed through environment variables
- **Anonymous Usage**: No user registration or personal data collection required



## 📈 Performance

- **Processing Time**: Typically 3-5 minutes for comprehensive reports
- **Search Coverage**: 20 strategic searches for thorough information gathering
- **Report Length**: 1000-2000 words with executive summary and detailed findings
- **Concurrent Users**: Supports multiple simultaneous users on Hugging Face Spaces

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Comprehensive guides available in the `/docs` folder

## 🗺️ Roadmap

- [ ] Enhanced source credibility scoring
- [ ] Integration with academic databases
- [ ] Advanced visualization options
- [ ] Collaboration features for team research
