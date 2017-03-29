from sanic.response import text
from sanic import Blueprint
from archiver.controllers.newsfeed import NewsfeedController
from archiver.controllers.newsfeedlist import NewsfeedListController

bp_v1 = Blueprint('v1', url_prefix='/api/v1')


@bp_v1.route('/')
async def api_v1_root(request):
    return text('ARCHIVE API VERSION 1')

bp_v1.add_route(NewsfeedController().as_view(), '/archive', methods=['POST'])
bp_v1.add_route(NewsfeedController().as_view(), '/archive/<hashid>', methods=['GET'])
bp_v1.add_route(NewsfeedListController().as_view(), '/archive/list', methods=['GET'])
