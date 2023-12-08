# RoundTop - Flask Api Server

![License MIT](https://img.shields.io/badge/License-MIT-yellow)

## Overview
RoundTop is a versatile and plug-and-play framework designed for building robust Flask APIs. Whether you're developing a small project or a large-scale application, this framework provides a solid foundation, allowing you to focus on implementing your specific features rather than boilerplate setup.

**Key Features**:

**Plug-and-Play**: Get started quickly by leveraging the framework's modular structure. Plug in components based on your project requirements.

**Scalable Architecture**: Built with scalability in mind, the framework supports the growth of your API as your project evolves.
Customizable: Tailor the app to your needs with a flexible configuration system and easy integration of additional functionalities.

## Table of Contents
- [Usage](#usage)
- [Docker](#running-the-app-with-docker)
- [Configuration](#configuration)
- [Authentication](#authentication)
- [API Documentation](#api-documentation)

## Usage

RoundTop provides a flexible and scalable platform for building and deploying RESTful APIs. Follow the steps below to get started with using the app.

### Prerequisites

Ensure you have the following prerequisites installed before running the Flask API Server App:

- [Python](https://www.python.org/) (>=3.6)
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/NateMount/RoundTop.git
   ```

2. Navigate to the project directory:
    ```bash
    cd RoundTop
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

#### Configuration
Customize the application configuration by setting environment variables or modifying the `settings.py` file. Refer to the [Configuration](#configuration) section for more details.

### Running the App
Run the Flask API Server App with the following command:

```bash
python wsgi.py
```

The app will start running on http://localhost:5000 by default.

## Running the App with Docker

To run the Flask API Server App using Docker, follow these steps:

1. Build the Docker image:

    ```bash
    docker build -t roundtop .
    ```

2. Run the Docker container:

    ```bash
    docker run roundtop
    ```

The app will be accessible at `http://localhost:5000` as configured in the Docker container.

## Configuration
RoundTop is designed to be highly configurable to suit various environments and use cases. This section outlines the available configuration options and how to customize the application's behavior.

### Configuration Files
The configuration settings for RoundTop are defined in the `settings.py` file. This file includes different configurations for development, production, and testing environments.



#### Available Configurations:
- **BaseConfig:** Common configuration settings shared across all environments.
- **DevConfig:** Configuration settings for the development environment.
- **ProductionConfig:** Configuration settings for the production environment.
- **TestConfig:** Configuration settings for running tests.

### Environment-based Configuration

The application dynamically selects the configuration based on the `APP_ENV` environment variable. If `APP_ENV` is not specified, the default configuration is set to `Dev`.

#### Available Environment Variables:

- **APP_ENV:** Set this variable to specify the environment (Dev, Production, Test).

### Customizing Configuration

To customize the configuration, you can either modify the `settings.py` file directly or set environment variables. Environment variables take precedence over the configuration file.

#### Example: Set Environment Variable

```bash
export APP_ENV=Production
export DB_URI="your_custom_database_uri"
export LOGGING=True
```

#### Example: Modify `settings.py`
```python
# settings.py

class ProductionConfig(BaseConfig):
    FLASK_ENV: str = 'production'
    DB_URI: str = 'your_custom_database_uri'
    LOGGING: bool = True
```

### Configuration Options
Here are some key configuration options:

- **LOGGING**: Enable or disable logging.
- **TESTING**: Enable or disable testing mode.
- **DEBUG**: Enable or disable debugging mode.
- **SECRET**: Secret key used for various cryptographic operations.
- **JWT_AUTH**: JWT authentication key for securing JSON Web Tokens.
- **FLASK_ENV**: Flask environment (development, production, testing).
- **DB_URI**: Database URI for connecting to the database.

Feel free to adjust the configuration to meet the requirements of your specific deployment environment.

## Authentication

RoundTop uses JSON Web Tokens **(JWT)** for authentication. JWT is a secure and efficient method to handle user authentication by creating a token that contains encoded information used in authenticating each request.

#### Make Token Response

```python
def make_token_response(**payload) -> object:
    """
    Make Token Response
    Used to generate a valid token response based on global environment data

    @param payload: key value pairs to be included in the JWT
    @returns : JWT
    """

    return jwt.encode(
        {'exp': datetime.utcnow() + timedelta(minutes=30), **payload}, 
        app.config['SECRET_KEY']
    )
```

## Api Documentation

**Note** : All routes make use of JWT authentication, previously mentioned

### Wrapper Functions

#### Check Table

```python
def check_table(funct:callable) -> callable:
    """
    Check Table <Wrapper>
    Will try to run passed in function until an attribute error is raised
    The attribute error indicates that the requested table does not exist
    If an AttributeError is raised then the function will simpy return {}
    
    @param funct <callable>: Function to be wrapped
    @returns <callable>: Wrapped function
    """

    def _wrap(*args, **kwargs) -> object:
        try:
            return funct(*args, **kwargs)
        except AttributeError:
            return jsonify({})
    _wrap.__name__ = funct.__name__
    
    return _wrap
```

#### Token Required

```python
def token_required(funct:callable) -> callable:
    """
    Token Required <Wrapper>
    Will require the use of a JWT in order to process request

    @param funct <callable>: Function to be wrapped
    @returns <callable>: Wrapped Function
    """

    def _wrap(*args, **kwargs):

        if not 'x-access-token' in request.headers: return jsonify({'message' : 'Token is missing !!'}), 401
        
        token = request.headers['x-access-token']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")

        if data['auth'] != config.JWT_AUTH: 
            return jsonify({'message' : 'Token is invalid !!'}), 401
    
        return funct(*args, **kwargs)
    
    _wrap.__name__ = funct.__name__
    return _wrap
```

### Make New Record

**Route:** `/<table_id>/make`

**Method:** `POST`

**Description:** Create a new record in the specified table.

**Parameters**: 
- **table_id** : name of table in database

**Json Body**:
- **Key** : each key is the name of a feature in the selected table
- **Value** : Set value for that feature

```python
@app.route('/<table_id>/make', methods=['POST'])
@check_table
@token_required
def make(table_id:str):
    get_hook(table_id).insert(**request.get_json())
    return {}
```

### Get Record By Index

**Route:** `/<table_id>/get/<i>`

**Method:** `GET`

**Description:** Retrive a record stored at index ***i***.

**Parameters**: 
- **table_id** : name of table in database
- **i** : index of record


```python
@app.route('/<table_id>/get/<i>', methods=['GET'])
@check_table
@token_required
def get(table_id:str, i:int):
    return get_hook(table_id).get(i)
```

### Get All Records

**Route:** `/<table_id>/get`

**Method:** `GET`

**Description:** Retrive all records in table ***table_id***.

**Parameters**: 
- **table_id** : name of table in database

**Json Body** ( *Optional* ):
- **Key** : each key is the name of a feature to filter by
- **Value** : value to match in that feature

```python
@app.route('/<table_id>/get',methods=['GET'])
@check_table
@token_required
def select(table_id:str):
    if request.get_json() == {}:
        return get_hook(table_id).all()
    return get_hook(table_id).select(**request.get_json())
```

### Drop Records

**Route:** `/<table_id>/drop`

**Method:** `GET`

**Description:** Delete all records that match the passed in Json filters.

**Parameters**: 
- **table_id** : name of table in database

**Json Body** ( *Optional* ):
- **Key** : each key is the name of a feature to filter by
- **Value** : value to match in that feature

**NOTE** : No Json body results in clearing whole table

```python
@app.route('/<table_id>/drop',methods=['GET'])
@check_table
@token_required
def drop(table_id:str):
    get_hook(table_id).delete(**request.get_json())
    return {}
```

### Update Record

**Route:** `/<table_id>/update`

**Method:** `GET`

**Description:** Update a record.

**Parameters**: 
- **table_id** : name of table in database

**Json Body**:

```python
@app.route('/<table_id>/update',methods=['GET'])
@check_table
@token_required
def update(table_id:str):
    get_hook(table_id).update(**request.get_json())
    return {}
```
