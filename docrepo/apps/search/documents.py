from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from apps.repo.models.element.document import Document as RepoDocument
from apps.repo.models.element.folder import Folder as RepoFolder
from apps.projects.models import Project as RepoProject


@registry.register_document
class DocumentIndex(Document):
    """
    Elastic index for document details
    """

    class Index:
        name = "repo_documents"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = RepoDocument
        fields = [
            "name",
            "title",
            "description",
        ]


@registry.register_document
class FolderIndex(Document):
    """
    Elastic index for folder details
    """

    class Index:
        name = "repo_folders"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = RepoFolder
        fields = [
            "name",
            "title",
            "description",
        ]


@registry.register_document
class ProjectIndex(Document):
    """
    Elastic index for project details
    """

    class Index:
        name = "repo_projects"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = RepoProject
        fields = [
            "name",
            "title",
            "description",
        ]
