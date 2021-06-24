from flask import Flask, abort, request, url_for, Blueprint
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import json
from flask_ngrok import run_with_ngrok
import datetime
import time
from query import findReservation

app = Flask(__name__)
cors = CORS(app)
run_with_ngrok(app)

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    version="0.1.0",
    title="Rutgers Gym Reservation Monitor",
    doc="/docs"
)

app.register_blueprint(blueprint)

GET_RESERVATION = api.model("Response", {
    "monitoring": fields.Boolean(),
    "spots_remaining": fields.Integer(),
    "currently_availible": fields.Boolean(),
    "category": fields.String()
    })

# documentation for swagger UI
ns_monitor = api.namespace(
    "monitor", description="Monitors reservation portal"
)


@ns_monitor.route("")
class GetUserAnalytics(Resource):
    """
    Returns wether or not there is an open spot
    """

    @api.param(
        "Date and Time",
        description="The date and time you are looking to find a reservation (01/01/2021 11:00 AM)",
        type = "string",
    )

    @api.param(
        "Category",
        description="Type of reservation you are looking to make (badminton, patio pool, olympic pool, basketball, gym, volleyball)",
        type = "string",
    )

    @api.marshal_with(GET_RESERVATION, mask=None)
    def get(self):

        dateString = request.args.get("Date and Time")
        category = request.args.get("Category")

        # check for valid date and time
        try:
            date = datetime.datetime.strptime(dateString, "%m/%d/%Y %I:%M %p")
        except:
            abort(500, "Invalid date!")

        # check for valid category
        if category not in ["badminton", "patio pool", "olympic pool", "basketball", "gym", "volleyball"]:
            abort(500, "Invalid category!")

        # find the reservation
        return findReservation(date, category)
