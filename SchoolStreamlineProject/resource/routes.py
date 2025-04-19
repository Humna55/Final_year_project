from .resources import courseApi
def initialize_routes(api):

    api.add_resource(courseApi, '/api/course')