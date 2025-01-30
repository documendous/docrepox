from .apps import INSTALLED_APPS

INSTALLED_APPS.append("django_elasticsearch_dsl")

ELASTICSEARCH_DSL = {
    "default": {"hosts": "http://elasticsearch:9200"},
}
