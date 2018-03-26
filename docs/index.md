# API Documentation

> 굵은 글씨로 표시된 `Key`는 필수값  
> 사용자 인증은 Token Authorization을 사용하며, Header의 `Authorization`key에 `Token [Token key value]`value를 추가하여 이용한다.
> ex) Token 3dfsdbjkdjfkef

## Repository

<https://github.com/LeeHanYeong/FastCampus-API-Server>

## API Base

`https://api.lhy.kr/`

## API 목록

- Member
	- [Signup](#signup)
	- [Login](#login)
	- [Logout](#logout)
	- [UserDetail](#user-detail)
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
**password1**|패스워드|String
**password2**|패스워드 확인|String
first_name|이름|String
last_name|성|String
email|이메일|String

### Success Response

- Code: 201
- Content

Token key value

```json
{
  "key": "4709a4a4174835ac846294f06f6486be9c02b20b"
}
```

### Error Response

- Code: 400
	- Reason
		- 필수항목 누락
		- username 중복
		- password 불일치
	- Content

```json
{
  "username": [
    "해당 사용자 이름은 이미 존재합니다."
  ]
}
```

```json
{
  "non_field_errors": [
    "비밀번호가 일치하지 않습니다."
  ]
}
```

```json
{
  "last_name": [
    "이 항목을 채워주십시오."
  ],
  "password2": [
    "이 항목을 채워주십시오."
  ]
}
```

<a name="login"></a>
## Login

### URL

`/members/login/`

### Method

`GET`

### URL Params

Key			|	Description					|	Type
---			|	---						|	---
**username**	|	(Unique username)	|	String
**password**	|	(Password)			|	String

### Data Params

None

### Success Response

- Code: 200
- Content

Token key value

```json
{
  "key": "a35b9eb7e90d9ecdb5567183fb13f6b813cf2547"
}
```

### Error Response

- Code: 400
	- Reason: 인증 실패
	- Content

```json
{
  "non_field_errors": [
    "제공된 인증데이터(credentials)로는 로그인할 수 없습니다."
  ]
}
```

<a name="logout"></a>
## Logout

> Authenticate required

### URL

`/members/logout/`

### Method

`POST`

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

```json
{
  "detail": "Successfully logged out."
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

<a name="user-detail"></a>
## UserDetail(Profile)

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

Token key value

```json
{
  "key": "a35b9eb7e90d9ecdb5567183fb13f6b813cf2547"
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

```json
{
  "pk": 23,
  "author": {
    "pk": 78,
    "username": "lhy18",
    "first_name": "HanYeong",
    "last_name": "Lee",
    "email": ""
  },
  "title": "Post with Image",
  "img_cover": "http://127.0.0.1:8000/media/posts/120_qaXrLMD.png",
  "content": "Post Content"
}```

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
      "pk": 23,
      "author": {
        "pk": 78,
        "username": "lhy18",
        "first_name": "HanYeong",
        "last_name": "Lee",
        "email": ""
      },
      "title": "Post with Image",
      "img_cover": "http://127.0.0.1:8000/media/posts/120_qaXrLMD.png",
      "content": "Post Content"
    },
    {
      "pk": 22,
      "author": {
        "pk": 78,
        "username": "lhy18",
        "first_name": "HanYeong",
        "last_name": "Lee",
        "email": ""
      },
      "title": "Post Title",
      "img_cover": null,
      "content": "asdf"
    },
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

```json
{
  "pk": 21,
  "author": {
    "pk": 78,
    "username": "lhy18",
    "first_name": "HanYeong",
    "last_name": "Lee",
    "email": ""
  },
  "title": "Post Title",
  "img_cover": null,
  "content": ""
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