# BrokerGen
This application allows registered real estate agents in the company to download graphic assets for a new development project, with their personalized and standardized information.

Agents can access templates that include their names, contact details, and branding elements, ensuring consistency and professionalism in the marketing materials they distribute.

The platform streamlines the process of customizing and downloading the materials, making it easy for agents to promote the new development with tailored designs that align with company standards.

## Features

-   Secure user authentication (registration and login) using **JWT (JSON Web Tokens)**
-   Dynamic CORS configuration for development and production environments
-   Image upload, manipulation and retrieval
-   Integration with Google Sheets
-   Custom error handling
-   Database integration (using SQLAlchemy)
-   RESTful API endpoints

## Tech Stack

### Backend

-   Python 3.x
-   Flask
-   Flask-SQLAlchemy
-   Flask-CORS
-   **Flask-JWT-Extended**
-   python-dotenv
-   PIL
-   **Google API Client Libraries (google-api-python-client, google-auth, gspread)**
-   PostgreSQL (for development)

### Frontend

-   JavaScript (ES6+)
-   React.js
-   React Router
-   React Bootstrap
-   Axios

## API Endpoints

### Authentication Endpoints (auth_routes.py)

-   **`POST /api/login`**: Logs in an existing broker.
    -   **Request Body (JSON):**
        ```json
        {
            "email": "<broker_email>",
            "code_uau": "<broker_uau_code>"
        }
        ```
    -   **Response (JSON):**
        -   **Success (200 OK):**
            ```json
            {
                "message": "Login successful",
                "broker": {
                    "id": <broker_id>,
                    "name": "<broker_name>",
                    "email": "<broker_email>",
                    "uau": "<broker_uau_code>",
                    "is_admin": <true|false>
                },
                "token": "<jwt_token>"
            }
            ```
        -   **Error (400 Bad Request):**
            ```json
            {
                "message": "Email e código UAU são obrigatórios."
            }
            ```
        -   **Error (401 Unauthorized):**
            ```json
            {
                "message": "Credenciais inválidas."
            }
            ```

-   **`POST /api/signup`**: Registers a new broker.
    -   **Request Body (JSON):**
        ```json
        {
            "name": "<broker_name>",
            "email": "<broker_email>",
            "code_uau": "<broker_uau_code>"
        }
        ```
    -   **Response (JSON):**
        -   **Success (201 Created):**
            ```json
            {
                "message": "Cadastro realizado com sucesso.",
                "broker": {
                    "id": <broker_id>,
                    "name": "<broker_name>",
                    "email": "<broker_email>",
                    "uau": "<broker_uau_code>",
                    "is_admin": false
                },
                "token": "<jwt_token>"
            }
            ```
        -   **Error (400 Bad Request):**
            ```json
            {
                "message": "<Error message, e.g., 'Campo name é obrigatório.', 'Código UAU inválido.', 'Corretor já cadastrado com este email ou código UAU.'>"
            }
            ```
        -   **Error (500 Internal Server Error):**
            ```json
            {
                "message": "Erro ao cadastrar corretor: <error_message>"
            }
            ```

### Image Endpoints (image_routes.py)

-   **`POST /api/create_image`**: Creates broker images based on the provided data. Requires a valid JWT token in the `Authorization` header.
    -   **Request Headers:**
        -   `Authorization`: `Bearer <jwt_token>`
    -   **Request Body (JSON):**
        ```json
        {
            "phone": "<broker_phone_number>",
            "name": "<broker_name>",
            "creci": "<broker_creci_number>",
            "categories": ["<category1>", "<category2>", ...]
        }
        ```
        -   `phone`: Broker's phone number.
        -   `name`: Broker's name.
        -   `creci`: Broker's CRECI number.
        -   `categories`: An array of categories for which to generate images. 
    -   **Response (JSON):**
        -   **Success (200 OK):**
            ```json
            {
                "generated_images": [
                    {
                        "category": "<category_name>",
                        "feed_image_url": "<url_to_feed_image>",
                        "stories_image_url": "<url_to_stories_image>"
                    },
                    ...
                ]
            }
            ```
        -   **Error (400 Bad Request):**
            ```json
            {
                "message": "<Error message, e.g., 'Preencha todos os campos.', 'Insira um código CRECI válido (4 a 5 dígitos numéricos).'>"
            }
            ```
        -   **Error (500 Internal Server Error):**
            ```json
            {
                "message": "Erro ao criar a peça. Por favor, tente novamente mais tarde."
            }
            ```

### General Notes

*   All API endpoints under `/api` are subject to CORS restrictions as defined in `app.py`.
*   The `AppError` custom exception is used for consistent error responses.
*   The `SECRET_KEY` environment variable is crucial for JWT signing and should be securely managed.
*   The Google API credentials must be correctly configured for the image generation to work.
*   The frontend must handle JWT storage and inclusion in the `Authorization` header for authenticated endpoints.
