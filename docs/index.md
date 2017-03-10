# API Documentation

> 굵은 글씨로 표시된 `Key`는 필수값  
> 사용자 인증은 Token Authorization을 사용하며, Header의 `Authorization`key에 `Token [Token key value]`value를 추가하여 이용한다.

## API Base

`https://fc-ios.lhy.kr/api`

## API 목록

- Member
	- Signup
	- Login
	- Logout
	- UserDetail
- Post
	- Post Create
	- Post List
	- Post Retrieve

## Signup

### URL

`/member/signup/`

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
**first_name**|이름|String
**last_name**|성|String
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


## Login

### URL

`/member/login/`

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