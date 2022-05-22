# tb.token.dealer

# .env set up
## set up a password
using base64 "to avoide ant shoulder surfers"
example: password = *your base64 password*
## set up email_reciever
example: email_reciever = *person reseving and sending autentication*
## set email_sender
example: email_sender = *bot's email*
## set up tb_email_login
example: tb_email_login = *your thingsboard email login*
## set up tb_email_login_password
example: tb_email_login_password = *your password to thingboard*

# email notifications
when a device wante to connect you your profile they are to request a token by sending a get request to the endpoint "/deviceName/<string:deviceName>",
this means they will ask have to submit a unique name to the device other wise the divice can not be created on thingsboard.

the user will then revieve an email with the device name and instructions on how to authorise the device or deny it access.

