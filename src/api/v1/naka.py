import logging
import flask
from src import persistence


logger = logging.getLogger(__name__)
blueprint = flask.Blueprint('naka', __name__)


@blueprint.route("nakamoto", methods=["GET"])
def get_nakamoto_coeff():
    all_nc = persistence.BitcoinNakamotoCoefficient.read_all()
    return flask.jsonify(list(map(lambda nc: nc.to_dict(), all_nc)))

