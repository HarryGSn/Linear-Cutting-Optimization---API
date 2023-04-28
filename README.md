
## API Reference

#### Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.

```http
  POST /users/token
```

| Parameter | Type     | Required                | Description |
| :-------- | :------- | :------------------------- | :--------- |
| `username` | `string` | &#9745; | Users' registered user name |
| `password` | `string` | &#9745; | Users' registered password |


```http
  POST /users/token/refresh
```

| Parameter | Type     | Required                | Description |
| :-------- | :------- | :------------------------- | :--------- |
| `refresh` | `string` | &#9745; | JWT Refresh Token |


#### Create an Optimization

```http
  POST /optimizations/
```

| Parameter | Type     | Required                | Description |
| :-------- | :------- | :------------------------- | :--------- |
| `settings.kerf` | `float` | &#9745; | Kerf (saw cut deduction) |
| `settings.trim.left` | `float` | &#9744; | left trim to be applied |
| `settings.trim.right` | `float` | &#9744; | right trim to be applied |
| `settings.bar_length` | `float` | &#9745; | Bar Length to be used in optimization |
| `parts[].length` | `float` | &#9745; | bar length to be cut |
| `parts[].quantity` | `integer` | &#9745; | Times for this length to be used |


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
