# Mergambot
# Author: Nathaniel Oon
# Date:   30/04/2016

from wsgiref.simple_server import make_server
from bots.tictactoe import TicTacToeBot
import json, requests, sys, ConfigParser
import lovely.jsonrpc.dispatcher, lovely.jsonrpc.wsgi

CONFIG_FILE = 'config.ini'

class GameController:
    def __init__(self):
        # Configure controller
        self.configure_controller()

        # Initialise bots
        ttt_bot = TicTacToeBot()

        # Register the bot
        self.register_controller(ttt_bot.get_game())

        # Configure lovely dispatcher
        dispatcher = lovely.jsonrpc.dispatcher.JSONRPCDispatcher()

        # Register methods
        dispatcher.register_method(self.status_ping, name='Status.Ping')

        # Tic Tac Toe game
        dispatcher.register_method(ttt_bot.make_move, name='TicTacToe.NextMove')
        dispatcher.register_method(ttt_bot.complete, name='TicTacToe.Complete')
        dispatcher.register_method(ttt_bot.error_message, name='TicTacToe.Error')

        app = lovely.jsonrpc.wsgi.WSGIJSONRPCApplication({'': dispatcher})
        server = make_server('0.0.0.0', 4000, app)

        # Start handling requests
        print "Starting Mergambot"
        while True:
            server.handle_request()

    def configure_controller(self):
        """ Function for reading in our config file
        """
        config = ConfigParser.ConfigParser()
        config.readfp(open(CONFIG_FILE))

        # Attributes
        self.name = config.get('BotConfig', 'botname')
        self.version = config.get('BotConfig', 'botversion')
        self.prog_lang = config.get('BotConfig', 'programminglanguage')
        self.website = config.get('BotConfig', 'website')
        self.desc = config.get('BotConfig', 'description')
        self.token = config.get('BotConfig', 'token')

        self.rpc_end_point = config.get('NetworkConfig', 'rpc_endpoint')
        self.merk_server = config.get('NetworkConfig', 'merk_server')

    def register_controller(self, game):
        """ Function for registering the bot to the Merknera server 
        """
        url = self.merk_server
        headers = {'Content-Type': 'application/json'}
        payload = {
            "method": "RegistrationService.Register",
            "params": {
               "token": self.token,
               "botname": self.name,
               "botversion": self.version,
               "game": game,
               "rpcendpoint": self.rpc_end_point,
               "programminglanguage": self.prog_lang,
               "website": self.website,
               "description": self.desc
            },
            "id": 1
        }
        response = requests.post(
            url, data=json.dumps(payload), headers=headers)

        print response
        if 'error' in response.json().keys():
            sys.exit
        else:
            print "Registered successfully: ", response.json()['result']['message']

    def status_ping(self):
        """ Ping ping
        """
        print "Ping received."
        response = {'ping': 'OK'}
        return response

def main():
    game = GameController()

if __name__ == "__main__":
    main()