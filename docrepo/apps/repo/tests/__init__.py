from .bugs import ProjectOwnerCannotAddTest
from .models.folder import FolderModelTest
from .models.document import DocumentModelTest
from .helpers.validation import DuplicateTopLevelPeerTest
from .templatetags import ProjectTagsTest
from .views.document import (
    DocumentViewTest,
    RetrieveDocumentViewTest,
    AddDocumentViewTest,
    CreateDocumentViewTest,
)
from .views.element import (
    ElementDetailsViewTest,
    UpdateElementDetailsViewTest,
    RecycleElementFlowTest,
    RecycleFolderActionTest,
)
from .views.folder import FolderViewTest
from .views.profile import UpdateProfileViewTest
from .views.ui import IndexViewTest
from .views.version import AddVersionViewTest
