from locust import HttpUser, task, between


CSS = [
    "/css/base.css",
    "/css/components.css",
    "/css/layout.css",
    "/css/pages.css",
    "/css/tokens.css",
]


PAGES = {
    "home": {
        "url": "/index.html",
        "js": [
            "/js/menu.js",
            "/js/scroll.js",
            "/js/theme.js",
        ],
        "images": [
            "/img/main hero.webp",
            "/img/hairstyle 1.webp",
            "/img/service1.webp",
            "/img/service2.webp",
            "/img/service3.webp",
            "/img/service4.webp",
            "/img/Features1.svg",
            "/img/Features2.svg",
            "/img/Features3.svg",
            "/img/Features4.svg",
        ],
    },

    "services": {
        "url": "/services.html",
        "js": [
            "/js/menu.js",
            "/js/scroll.js",
            "/js/theme.js",
        ],
        "images": [
            "/img/hairstyle 1.webp",
        ],
    },

    "barbers": {
        "url": "/barbers.html",
        "js": [
            "/js/menu.js",
            "/js/scroll.js",
            "/js/theme.js",
        ],
        "images": [
            "/img/hairstyle 1.webp",
            "/img/Barber_1.webp",
            "/img/barber_2.webp",
            "/img/barber_3.webp",
            "/img/barber_4.webp",
        ],
    },

    "contacts": {
        "url": "/contacts.html",
        "js": [
            "/js/menu.js",
            "/js/scroll.js",
            "/js/theme.js",
            "/js/form.js",
        ],
        "images": [
            "/img/hairstyle 1.webp",
            "/img/main hero.webp",
        ],
    },
}


class WebsiteUser(HttpUser):

    wait_time = between(1, 3)

    def get_resource(self, path, name):
        # Отправляем запрос и проверяем ответ
        with self.client.get(path, name=name, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"HTTP error: {response.status_code}")
                return False
            response.success()
            return True

    def get_asset(self, path, resource_type):

        success = self.get_resource(path, name=f"{resource_type} {path}")
        return success

    def visit_page(self, page_name):
        page = PAGES[page_name]

        # Загрузка HTML, CSS, JS, IMG
        page_loaded = self.get_resource(page["url"], name=f"HTML {page_name}")
        if not page_loaded:
            return

        for css_file in CSS:
            self.get_asset(css_file, "CSS")

        for js_file in page["js"]:
            self.get_asset(js_file, "JS")

        for image_file in page["images"]:
            self.get_asset(image_file, "IMAGE")

    @task(1)
    def open_homepage(self):
        self.visit_page("home")

    @task(1)
    def open_services(self):
        self.visit_page("services")

    @task(1)
    def open_barbers(self):
        self.visit_page("barbers")

    @task(1)
    def open_contacts(self):
        self.visit_page("contacts")
