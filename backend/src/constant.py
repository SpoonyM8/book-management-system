# email pattern written by Andy Smith, https://www.regexlib.com/UserPatterns.aspx?authorId=15777db1-4c90-48f2-b323-905b509f16e8
email_pattern = "^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$"

# password pattern, min eight characters with >1 letter, >1 number and >1 special char
# password pattern written by Srinivas, https://stackoverflow.com/a/21456918 
password_pattern = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

_OK = 200
_InputError = 400
_UnauthorizedError = 401
_AccessError = 403