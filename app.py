from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import time

from sudoku import solve
from utils import values2grid, check_sudoku_input


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
api = Api(app)

class Sudoku(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sudoku',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, sudoku):
        (ok, message) = check_sudoku_input(sudoku)
        if not ok:
            return {'message': message}, 400
        start = time.clock()
        result = solve(sudoku)
        t = time.clock()-start
        return {'solution': values2grid(result), 'time': t}


api.add_resource(Sudoku, '/sudoku/<string:sudoku>')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True