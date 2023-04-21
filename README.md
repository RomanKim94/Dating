# Dating
API for dating site. 
## Very short description
This project is a bit like Tinder. You can put marks to persons (like or not). 
___
## List of URLs

### Create person account

`https://testingdatingapi.pythonanywhere.com/api/clients/create/`  
You can create user at this address.
*For POST method only.* Following arguments are accepted: 
- **username** (required, accepted letters, numbers and simbols @.+-_);
- **email** (required);
- **first_name** (optional);
- **last_name** (optional);
- **birthday** (optional);
- **sex** (required, ***"M"*** (Male)/***"F"*** (Female));
- **latitude** (required, maximum digits: 9, value period: (-90)-90);
- **longitude** (required, maximum digits: 9, value period: (-180)-180);
- **password** (required);
- **photo** (optional).  
When user entry is created, watermark is placed on the photo.

### Authorization

`https://testingdatingapi.pythonanywhere.com/api/clients/auth/token/login/`  
You can authorize at this address. The token is returned in response.  
*For POST method only.* Following arguments are required: 
- **username**;
- **password**.

### List users

`https://testingdatingapi.pythonanywhere.com/api/clients/list/`  
At this address you can get list of persons, who are registered already. 
Information includes *username*, *first name*, *last name*, *birthday*, *sex* and *distance to user*.  
**For GET method only.**
Users list can be filtered by distance, sex, age.

#### Filtering by sex

`https://testingdatingapi.pythonanywhere.com/api/clients/list/?sex=M`  
List will filtered by male users.

`https://testingdatingapi.pythonanywhere.com/api/clients/list/?sex=F`  
List will filtered by female users.

#### Filtering by age

`https://testingdatingapi.pythonanywhere.com/api/clients/list/?max_age=<MAX_AGE>`  
List will include users under the age of <MAX_AGE>, where <MAX_AGE> is maximum age of users.

`https://testingdatingapi.pythonanywhere.com/api/clients/list/?min_age=<MIN_AGE>`  
List will include users over the age of <MIN_AGE>, where <MIN_AGE> is minimum age of users.

Filters can combined with simbol **"&"** like:  
`https://testingdatingapi.pythonanywhere.com/api/clients/list/?min_age=<MIN_AGE>&max_age=<MAX_AGE>`  
So you wil get list of users matching the age range.

#### Filtering by distance

`https://testingdatingapi.pythonanywhere.com/api/clients/list/?max_distance=<MAX_DISTANCE>`  
List will be filtered by distance and will include users closer <MAX_DISTANCE> kilometers from current user.

`https://testingdatingapi.pythonanywhere.com/api/clients/list/?max_distance=<MIN_DISTANCE>`  
Same URL, but filtering by minimal distance, i.e. list will include users further than <MIN_DISTANCE> kilometers from current user.

### Detail profile view
There is also detail information function for viewing user profile. 
Detail information includes *username*, *first name*, *last name*, *birthday*, *sex*, *distance to user* and *photo*.  

### Mark to user

`https://testingdatingapi.pythonanywhere.com/api/clients/<PERSON_ID>/match/`  
**For POST method only**.
If user likes any other user first can put mark to second one. There must be {"mark": <MARK>} in the request body.  
<MARK> can be ("True"/1) or ("False"/0) only, i.e. boolean value.  
<PERSON_ID> is an integer number.

If both users like each other then messages are sended to their email. It contains the email address of the user they like.  
Responce contains user email too. And if liking is not mutual, then email is not cantained
