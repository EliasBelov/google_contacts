def get_link_token(auth_url):
    fin = open('txt/token_authorization.txt', 'w')
    fin.write(auth_url)
    fin.close()

