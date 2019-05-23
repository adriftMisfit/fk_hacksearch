from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

ActionItem = {
    'action_1': {'type': 'SearchAction','search_tag': 't1'},
    'action_2': {'type': 'ProductPageAction', 'search_tag': 't2'},
    'action_3': {'type': 'AddToCartAction', 'search_tag': 'random!'},
    'action_4': {'type': 'BuyAction', 'search_tag': 'buy'},
}

Recco_map = {
    'LST1': {'tags': ['t1', 't2', 't3']},

}

def abort_if_action_doesnt_exist(action_id):
    if action_id not in ActionItem:
        abort(404, message="action {} doesn't exist".format(action_id))


parser = reqparse.RequestParser()
parser.add_argument('type')
parser.add_argument('search_tag')


# Todo
# shows a single action item and lets you delete a action item
class ActionData(Resource):
    def get(self, action_id):
        abort_if_action_doesnt_exist(action_id)
        return ActionData[action_id]

    def delete(self, action_id):
        abort_if_action_doesnt_exist(action_id)
        del ActionItem[action_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'type': args['type'], 'search_tag': args['search_tag']}
        ActionItem[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return ActionItem

    def post(self):
        args = parser.parse_args()
        action_id = int(max(ActionItem.keys()).lstrip('action_')) + 1
        action_id = 'action_%i' % action_id
        print("action id {}".format(action_id))
        ActionItem[action_id] = {'type': args['type'], 'search_tag': args['search_tag']}
        return ActionItem[action_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/actions')
api.add_resource(ActionData, '/actions/<action_id>')


if __name__ == '__main__':
    app.run(debug=True)