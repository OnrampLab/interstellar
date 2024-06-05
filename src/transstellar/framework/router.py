from .route import Route


class Router:
    routes: dict = {}

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
        return self.routes.get(route_key)

    def get_page(self, app, route_key: str):
        route = self.get_route(route_key)

        if route is None:
            return None

        return route.page_class(app)
