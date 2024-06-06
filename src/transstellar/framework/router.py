from .route import Route


class Router:
    app: None
    routes: dict = {}

    def __init__(self, app):
        self.app = app

    def register_routes(self, routes: dict):
        if routes is None:
            return

        for route_key, value in routes.items():
            self.register_route(route_key, value)

    def register_route(self, route_key: str, route: Route):
        if not isinstance(route, Route):
            raise TypeError("route is not a Route instance")

        self.routes[route_key] = route

    def get_route(self, route_key: str):
        route = self.routes.get(route_key)

        if route is None:
            raise LookupError(f'Route "{route_key}" not found')

        return route

    def get_page(self, route_key: str):
        route = self.get_route(route_key)

        return route.get_page(self.app)
