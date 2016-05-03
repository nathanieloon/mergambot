from wsgiref.simple_server import make_server
import lovely.jsonrpc.dispatcher, lovely.jsonrpc.wsgi

def register(token, botname, botversion, game, rpcendpoint, programminglanguage, website, description):
  print token
  print botname
  print botversion
  print game
  print rpcendpoint
  print programminglanguage
  print website
  print description

  response = {"message": "Hello bot"}
  return response

dispatcher = lovely.jsonrpc.dispatcher.JSONRPCDispatcher()
dispatcher.register_method(register, name='RegistrationService.Register')
dispatcher.register_method(register, name='register')
app = lovely.jsonrpc.wsgi.WSGIJSONRPCApplication({'': dispatcher})
server = make_server('localhost', 4001, app)
print "Starting server"
while True:
    server.handle_request()