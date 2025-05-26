# Personal Website with Streamlit

This is a personal website built using Streamlit, featuring multiple pages and interactive components.

## Project Structure

```
project/
├── streamlit_app.py        # Main application entry point
├── .streamlit/             # Streamlit configuration
│   └── config.toml         # Streamlit configuration file
├── components/             # Reusable UI components
│   ├── footer.py           # Page footer component
│   ├── interactive.py      # Interactive visualizations
│   └── styles.py           # CSS and styling utilities
├── page_content/           # Website pages
│   ├── home.py             # Home page
│   ├── experience.py       # Experience page
│   ├── education.py        # Education page
│   ├── resume.py           # Resume page
│   └── contact.py          # Contact page
└── static/                 # Static assets
    ├── css/                # CSS stylesheets
    │   └── style.css       # Main stylesheet
    ├── images/             # Image files
    │   └── image.png       # Profile image
    └── docs/               # Documents
        ├── resume.md       # Resume in markdown format
        └── resume.pdf      # Resume in PDF format
```

## Running the Application

To run the application, use the following command:

```bash
streamlit run streamlit_app.py
```

## Features

- Multi-page navigation with sidebar
- Interactive data visualizations
- Responsive design with custom CSS
- Downloadable resume
- Contact form
- Streamlit theming via config.toml

## Adding New Pages

To add a new page to the application:

1. Create a new Python file in the `page_content` directory
2. Define a main function for the page content
3. Import the function in `streamlit_app.py`
4. Add the page to the `MultiApp` instance

## Adding New Interactive Components

To add a new interactive component:

1. Create a new Python file in the `components` directory
2. Define your component function
3. Import and use the component in your page files 