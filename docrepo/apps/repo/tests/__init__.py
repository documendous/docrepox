from .bugs import ProjectOwnerCannotAddTest
from .helpers.validation import DuplicateTopLevelPeerTest
from .models.document import DocumentModelTest
from .models.folder import FolderModelMethodsTest, FolderModelTest
from .templatetags import ProjectTagsTest
from .views.document import (
    AddDocumentViewTest,
    CreateDocumentViewTest,
    DocumentViewTest,
    RetrieveDocumentViewTest,
    UpdateDocumentContentViewTest,
)
from .views.element import (
    ElementDetailsViewTest,
    RecycleElementFlowTest,
    RecycleElementsViewTest,
    RecycleFolderActionTest,
    RestoreElementsViewTest,
    UpdateElementDetailsViewTest,
)
from .views.folder import FolderViewTest
from .views.profile import UpdateProfileViewTest
from .views.ui import IndexViewTest
from .views.version import AddVersionViewTest
