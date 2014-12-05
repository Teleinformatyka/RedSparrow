**This documentation is automatically generated.**


# gettext
    JSON-RPC

**Args**

*

 * args

 * kwargs
            


**Input Schema**
```json

```

**Output Schema**
```json

```


**Notes**

Method called when JSON-RPC for __name



<br>
<br>

# login
    JSON-RPC

**Args**

*

 * login

 * password
            


**Input Schema**
```json

```

**Output Schema**
```json

```


**Notes**

Login method

:param login: user Login

:param password: hash of password



<br>
<br>

# login-test_method
    JSON-RPC

**Args**
None


**Input Schema**
```json

```

**Output Schema**
```json

```


**Notes**

Test doc



<br>
<br>

# register
    JSON-RPC

**Args**

*

 * login

 * password

 * email

 * name

 * surname
            


**Input Schema**
```json

```

**Output Schema**
```json

```


**Notes**

Register method

params - dict

:param login: user Login

:param email: user email

:param password: hash of user password

:param surname: user surname

:param name: user name

:returns: If success returns all user data else return JSON-RPC error object


