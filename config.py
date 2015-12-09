from authomatic.providers import oauth2

CONFIG = {
    'fb': {
           
        'class_': oauth2.Facebook,
        
        # Facebook is an AuthorizationProvider too.
        'consumer_key': '974600372617681',
        'consumer_secret': 'e02dec609891e1a96a719da7e5a78ca9',
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'publish_stream', 'read_stream']
    }
}