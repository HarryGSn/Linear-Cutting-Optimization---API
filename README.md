## Licenses

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Apache License 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![GNU General Public License v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
[![BSD 3-Clause License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)



# Linear Cutting Optimization

A Course Project created for **Applied Programming using Python** by Dr.Karydis, at Ionian University, Department of Informatics.
## Authors

- [@HarryGSn / C.Giannaros](https://www.github.com/harrygsn)
- [@DionyshsTetradhs / D.Tetradis](https://www.github.com/DionyshsTetradhs)


## API Reference

#### Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.

```http
  POST /users/token
```

| Parameter | Type     | Required                | Description |
| :-------- | :------- | :------------------------- | :--------- |
| `username` | `string` | :heavy_check_mark | Users' registered user name |
| `password` | `string` | :heavy_check_mark | Users' registered password |


```http
  POST /users/token/refresh
```

| Parameter | Type     | Required                | Description |
| :-------- | :------- | :------------------------- | :--------- |
| `refresh` | `string` | :heavy_check_mark | JWT Refresh Token |


#### Create an Optimization

```http
  POST /optimizations/
```

| Parameter | Type     | Required                | Description |
| :-------- | :------- | :------------------------- | :--------- |
| `settings.kerf` | `float` | :heavy_check_mark | Kerf (saw cut deduction) |
| `settings.trim.left` | `float` | :x | left trim to be applied |
| `settings.trim.right` | `float` | :x | right trim to be applied |
| `settings.bar_length` | `float` | :heavy_check_mark | Bar Length to be used in optimization |
| `parts[].length` | `float` | :heavy_check_mark | bar length to be cut |
| `parts[].quantity` | `integer` | :heavy_check_mark | Times for this length to be used |


Example Body:
```JSON
{
    "settings": {
        "kerf": 10,
        "trim": {
            "left": 0,
            "right": 0
        },
        "bar_length": 6500
    },
    "parts": [
        { "quantity": 2, "length": 1500 },
        { "quantity": 2, "length": 1650 },
        { "quantity": 4, "length": 1600 },
        { "quantity": 4, "length": 1550 },
        { "quantity": 4, "length": 1000 },
        { "quantity": 4, "length": 800 }
    ]
}
```

Response:
```JSON
{
    "result": "ok",
    "solution": [
        {
            "index": 0,
            "parts": [
                1650,
                1650,
                1600,
                1550
            ],
            "remnant": 10.0
        },
        {
            "index": 1,
            "parts": [
                1600,
                1600,
                1600,
                1550
            ],
            "remnant": 110.0
        },
        {
            "index": 2,
            "parts": [
                1550,
                1550,
                1500,
                1500
            ],
            "remnant": 360.0
        },
        {
            "index": 3,
            "parts": [
                1000,
                1000,
                1000,
                1000,
                800,
                800,
                800
            ],
            "remnant": 30.0
        },
        {
            "index": 4,
            "parts": [
                800
            ],
            "remnant": 5690.0
        }
    ]
}
```

## Authentication
JWTAuthentication is used to generate tokens and refresh tokens
## Run Locally

*Navigate to the Root Directory of the Application*

Install Requirements
```python
  pip install -r requirements.txt

```

Run Migrations
```python
  python3 manage.py makemigrations optimizations
  python3 manage.py makemigrations users
  python3 manage.py migrate optimizations
  python3 manage.py migrate users
  python3 manage.py makemigrations
  python3 manage.py migrate
```

Run the project

```python
  python3 manage.py runserver
```

Create Super User
```python
  python3 manage.py createsuperuser
```
## Software Used

**Client:** Postman

**Server:** Python3


## 🛠 Technical Knowledge
- Python
- Rest API
- SQL
