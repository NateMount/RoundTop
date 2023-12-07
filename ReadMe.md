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
- [Configuration](#configuration)
- [Authentication](#authentication)
- [API Documentation](#api-documentation)

## Usage

## Configuration

## Authentication

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
