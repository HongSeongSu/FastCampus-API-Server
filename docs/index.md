# API Documentation

> 굵은 글씨로 표시된 `Key`는 필수값  
> 사용자 인증은 Token Authorization을 사용  
> Header의 `Authorization`key에 `Token [Token key value]`value를 추가하여 이용한다.  
> 
> ex) Token 3dfsdbjkdjfkef

## 관련 문서

[DRF - TokenAuthentication](http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
[DRF - BasicAuthentication](http://www.django-rest-framework.org/api-guide/authentication/#basicauthentication)

> `HTTP Basic Auth`방식도 지원합니다. Postman으로 간단히 테스트할 때 사용하세요.

## Repository

<https://github.com/LeeHanYeong/FastCampus-API-Server>

## API Base URL

**`https://api.lhy.kr/`**

## API 목록

- Member
	- [Signup](#signup)
	- [AuthToken](#auth-token)
	- [Profile](#profile)
- Post
	- [Post Create](#post-create)
	- [Post List](#post-list)
	- [Post Retrieve](#post-retrive)

<a name="signup"></a>
## Signup

### URL

`/members/signup/`

### Method

`POST`

### URL Params

None

### Data Params

Key|Description|Type
---|---|---
**username**|회원가입하는 사용자명|String
**password**|패스워드|String
first_name|이름|String
last_name|성|String
email|이메일|String

### Success Response

- Code: 201
- Content

Token key value, User object

```json
{
    "user": {
        "pk": 1,
        "username": "lhy",
        "first_name": "",
        "last_name": "",
        "email": "dev@lhy.kr"
    },
    "token": "d3e60437ef417c427f43ac6c09e93b8f86d13356"
}
```

### Error Response

- Code: 400
	- Reason
		- 필수항목 누락
	- Content

```json
{
    "password": [
        "이 필드는 필수 항목입니다."
    ]
}
```

<a name="auth-token"></a>
## Login

### URL

`/members/auth-token/`

### Method

`POST`

### Data

Key			|	Description					|	Type
---			|	---						|	---
**username**	|	(Unique username)	|	String
**password**	|	(Password)			|	String

### Data Params

None

### Success Response

- Code: 200
- Content

Token key value, User object

```json
{
    "user": {
        "pk": 1,
        "username": "lhy",
        "first_name": "",
        "last_name": "",
        "email": "dev@lhy.kr"
    },
    "token": "d3e60437ef417c427f43ac6c09e93b8f86d13356"
}
```

### Error Response

- Code: 400
	- Reason
	    - 필수항목 누락
	    - 인증실패
	- Content

```json
{
    "password": [
        "이 필드는 필수 항목입니다."
    ]
}
```

```json
{
    "non_field_errors": [
        "제공된 인증데이터(credentials)로는 로그인할 수 없습니다."
    ]
}
```

<a name="profile"></a>
## Profile

> Authenticate required

### URL

`/members/profile/`

### Method

`GET`

### Header

Key|Value
---|---
Authorization|Token [Token key value]

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

User object

```json
{
    "pk": 1,
    "username": "lhy",
    "first_name": "",
    "last_name": "",
    "email": "dev@lhy.kr"
}
```

### Error Response

- Code: 401
	- Reason: Invalid token
	- Content

```json
{
  "detail": "토큰이 유효하지 않습니다."
}
```

---

<a name="post-create"></a>
## Post Create

> Authenticate required

### URL

`/posts/`

### Method

`POST`

### Header

Key|Value
---|---
Authorization|Token [Token key value]

### URL Params

None

### Data Params

Key|Value
---|---
**title**|글 제목
content|글 내용
img_cover|이미지

### Success Response

- Code: 201
- Content

Post object

```json
{
    "pk": 6,
    "author": {
        "pk": 1,
        "username": "lhy",
        "first_name": "",
        "last_name": "",
        "email": "dev@lhy.kr"
    },
    "images": [],
    "title": "Post with Image",
    "img_cover": "https://api.lhy.kr/media/post/pby76.jpg",
    "content": "Post Content",
    "created_date": "2018-03-26T20:06:06.886357+09:00"
}
```

### Error Response

- Code: 400
	- Reason: 필수 항목 누락
	- Content

```json
{
  "title": [
    "이 항목을 채워주십시오."
  ]
}
```


<a name="post-list"></a>
## Post List

### URL

`/posts/`

### Method

`GET`

### Header

None

### URL Params

Key|Value
---|---
page|Pagination Number

### Data Params

None

### Success Response

- Code: 200
- Content

```json
[
    {
        "pk": 8,
        "author": {
            "pk": 1,
            "username": "lhy",
            "first_name": "",
            "last_name": "",
            "email": "dev@lhy.kr"
        },
        "images": [],
        "title": "Post Title",
        "img_cover": null,
        "content": "",
        "created_date": "2018-03-26T20:25:20.075944+09:00"
    },
    {
        "pk": 6,
        "author": {
            "pk": 1,
            "username": "lhy",
            "first_name": "",
            "last_name": "",
            "email": "dev@lhy.kr"
        },
        "images": [],
        "title": "Post with Image",
        "img_cover": "https://api.lhy.kr/media/post/pby76.jpg",
        "content": "Post Content",
        "created_date": "2018-03-26T20:06:06.886357+09:00"
    }
]
```

### Error Response

- Code: 404
	- Reason: Invalid page number
	- Content

```json
{
  "detail": "Invalid page."
}
```


<a name="post-retrieve"></a>
## Post Retrieve

### URL

`/posts/<post_pk>/`

### Method

`GET`

### Header

None

### URL Params

None

### Data Params

None

### Success Response

- Code: 200
- Content

Post object

```json
{
    "pk": 6,
    "author": {
        "pk": 1,
        "username": "lhy",
        "first_name": "",
        "last_name": "",
        "email": "dev@lhy.kr"
    },
    "images": [],
    "title": "Post with Image",
    "img_cover": "https://api.lhy.kr/media/post/pby76.jpg",
    "content": "Post Content",
    "created_date": "2018-03-26T20:06:06.886357+09:00"
}
```

### Error Response

- Code: 404
	- Reason: Invalid Post pk
	- Content

```json
{
  "detail": "찾을 수 없습니다."
}
```
