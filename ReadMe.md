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

#### Token Required

### Make New Record

**Route:** `/<table_id>/make`

**Method:** `POST`

**Description:** Create a new record in the specified table.

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

```python
@app.route('/<table_id>/update',methods=['GET'])
@check_table
@token_required
def update(table_id:str):
    get_hook(table_id).update(**request.get_json())
    return {}
```
