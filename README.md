# Todo List Application

A modern Todo List application built with Django REST Framework backend and Vue.js + Quasar Framework frontend. Features include creating, completing, deleting, and reordering todo items using drag and drop.

## Features

- ✨ Create new todo items
- ✅ Mark todos as complete/incomplete
- 🗑️ Delete todos
- 📋 Drag and drop to reorder todos
- 🎨 Modern UI with Quasar Framework
- 🔔 Toast notifications for actions
- 📱 Responsive design
- 🧪 Comprehensive test suite

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- Node.js 16+
- uv (Python package installer)

To install uv:
```bash
pip install uv
```

## Backend Setup

1. Create and activate a virtual environment:
   ```bash
   cd backend
   uv venv
   source .venv/bin/activate  # On Windows use: .\.venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   # Install project dependencies
   uv pip install -e .

   # Install test dependencies (optional)
   uv pip install -e '.[test]'
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

The backend API will be available at `http://localhost:8000/api/todos/`

Note: The backend uses local settings by default (`backend/settings/local.py`), which includes:
- SQLite database for development
- DEBUG mode enabled
- CORS configured for local development
- Default development secret key

## Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The frontend application will be available at `http://localhost:5173`

## Testing

### Backend Tests

The backend uses pytest for testing. The test suite includes:
- Model tests for Todo model
- API endpoint tests for CRUD operations
- Integration tests for todo reordering

To run the tests:

1. Ensure you're in the backend directory with your virtual environment activated:
   ```bash
   cd backend
   source .venv/bin/activate  # On Windows use: .\.venv\Scripts\activate
   ```

2. Run the test suite:
   ```bash
   pytest
   ```

For more detailed test output:
   ```bash
   pytest -v
   ```

To run tests with coverage report:
   ```bash
   pytest --cov=todos
   ```

### Frontend Tests

The frontend uses Vitest for testing. The test suite includes:
- Unit tests for the `useTodos` composable
  - API interaction tests
  - State management tests
  - Error handling tests
- Component tests for `TodoList`
  - Todo creation
  - Todo completion
  - Todo deletion
  - Todo reordering
  - UI interaction tests

To run the tests:

1. Ensure you're in the frontend directory:
   ```bash
   cd frontend
   ```

2. Run the test suite:
   ```bash
   npm run test
   ```

For watch mode during development:
   ```bash
   npm run test:watch
   ```

The frontend tests use Vue Test Utils for component testing and include mocks for:
- Quasar components (QInput, QCheckbox, QBtn, etc.)
- Vue Draggable component
- API calls via Axios

## Project Structure

```
todo_app/
├── backend/                 # Django backend
│   ├── backend/            # Project settings
│   │   ├── settings/      # Split settings
│   │   │   ├── base.py   # Base settings
│   │   │   └── local.py  # Local development settings
│   ├── todos/             # Todos app
│   │   ├── tests/        # Test suite
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/               # Vue.js frontend
    ├── src/
    │   ├── App.vue        # Main application component
    │   ├── main.js        # Application entry point
    │   └── styles/        # Global styles
    ├── tests/             # Frontend tests
    ├── package.json
    └── vite.config.js
```

## API Endpoints

- `GET /api/todos/` - List all todos
- `POST /api/todos/` - Create a new todo
- `PATCH /api/todos/{id}/` - Update a todo
- `DELETE /api/todos/{id}/` - Delete a todo
- `POST /api/todos/reorder/` - Reorder todos

## Development

### Code Style and Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for both code formatting and linting. Ruff is configured in `pyproject.toml`.

To install development dependencies:
```bash
uv pip install -e '.[dev]'
```

To format code:
```bash
ruff format .
```

To lint and auto-fix issues:
```bash
ruff check . --fix
```

### Backend Development

- The backend uses Django REST Framework for API development
- Models are defined in `backend/todos/models.py`
- API views are in `backend/todos/views.py`
- URL routing is configured in `backend/todos/urls.py`

### Frontend Development

- The frontend uses Vue.js with Quasar Framework
- Main application logic is in `frontend/src/App.vue`
- Quasar theming variables are in `frontend/src/styles/quasar-variables.scss`
- API calls are made using Axios

## Environment Variables

The backend uses a `.env` file for configuration. For local development, the default settings in `backend/settings/local.py` will work out of the box. For production, you should create a `.env` file with appropriate values:

```env
DJANGO_SETTINGS_MODULE=backend.settings.production  # For production only
SECRET_KEY=your-secret-key-here
DEBUG=False  # For production only
```

Note: The development setup uses SQLite as the database for simplicity, which requires no additional configuration.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
