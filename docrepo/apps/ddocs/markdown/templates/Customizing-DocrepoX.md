## Customizing DocrepoX

For definition purposes, all Documendous software has three levels of customization:

1. **Configuration**: This level involves adjusting configuration variables, usually without the need to write any code. Most configuration options are listed in the “Using DocrepoX section. These adjustments are straightforward and effective for minor tweaks.

2. **Extending**: This deeper level of customization requires modifying templates and modules. The system provides structured ways to override or subclass components, which is the main focus of this “Customizing DocrepoX" section.

3. **Deep Customizations**: This involves changing applications and modules within the apps directory. Deep customizations are strongly discouraged, as they make your server instance unsupported until restored to a supported configuration. For guidance on this level, refer to the “Contributing to Documendous” section.

---

### Customization Tips

DocrepoX provides **Customization Tips**, which are optional links that can be enabled in your global_settings.py file. These links appear in various sections of DocrepoX and direct users to relevant documentation explaining how to customize that specific section.

#### Enabling Customization Tips

To enable customization tips, add the following setting to global_settings.py:

```python
ENABLE_CUSTOMIZATION_TIPS = True
```

#### Adding a Customization Tip

To add a customization tip to a specific section, include the following code next to the relevant section:

```html
<h2 class="text-xl font-semibold mb-4 flex items-center justify-center">
  Login {% include 'ddocs/customization_tips/_tip.html' with anchor_name="customize-login-page" %}          
</h2>
```

- Replace `"customize-login-page"` with the **anchor name** that corresponds to the relevant section in your documentation.

#### Adding Documentation and Anchor Links

If you need to create or update documentation for customization tips, modify the `Customizing-DocrepoX.md` file.

To define an **anchor link** within the documentation, use the following format:

```html
<a id="customize-login-page"></a>
```

This anchor allows the customization tip link to navigate directly to the relevant documentation section.

---

### Extending DocrepoX

For extension customizations, use the extensions subdirectory. The basic structure is as follows:

```
extensions/
├── apps
│   ├── __init__.py
│   └── repo
│       ├── forms.py
│       ├── __init__.py
│       ├── models.py
│       └── views.py
├── __init__.py
├── settings.py
├── staticfiles
└── templates
    └── registration
        └── login.html
```

If ENABLE_EXTENSIONS is set to True, the extensions file system becomes active, and the system will use any modules and templates placed there. 

**Note:** Be aware that if a module in this directory contains errors, it can disrupt the operation of the system.

Here is how customization with the extensions directory works:

- **Customizing Views:** Add a custom IndexView to extensions/apps/repo/views.py. The system will automatically use this version instead of the default at startup.

- **Overriding Templates:** Place a custom login.html file at extensions/templates/registration/login.html. The system will load your custom template in place of the default.

<a id="customize-login-page"></a>
#### Login Page Customization

For a different login page, you will need to override the apps/repo/templates/registration/login.html file. Copy this file to extensions/templates/registration/login.html. Make your changes to the template and ensure ENABLE_EXTENSIONS is set to True. Restart the server and your changes should be apparent at login.

**Note:** DocrepoX at this time only uses Django's internal authentication and Keycloak OpenID. To make deep changes to Django's internal authentication requires code changes for the django.contrib.auth package and is not supported. In other words, you would have to likely use your own custom Django module.

To make changes to the Keycloak OpenID backend, you'll need to add your own KeycloakOIDCAuthenticationBackend class to extensions/apps/repo/backends.py

Here is the code for the full KeycloakOIDCAuthenticationBackend class:

```

from urllib.parse import urlencode
from django.conf import settings

# Classes to override default OIDCAuthenticationBackend (Keycloak authentication)
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class KeycloakOIDCAuthenticationBackend(OIDCAuthenticationBackend):

    def _get_username(self, claims):
        username = claims.get("preferred_username")
        return username

    def create_user(self, claims):
        """Overrides Authentication Backend so that Django users are
        created with the keycloak preferred_username.
        If nothing found matching the email, then try the username.
        """
        user = super(KeycloakOIDCAuthenticationBackend, self).create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email")
        user.username = self._get_username(claims)
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        """Return all users matching the specified email.
        If nothing found matching the email, then try the username
        """
        email = claims.get("email")
        preferred_username = claims.get("preferred_username")

        if not email:
            return self.UserModel.objects.none()
        users = self.UserModel.objects.filter(email__iexact=email)

        if len(users) < 1:
            if not preferred_username:
                return self.UserModel.objects.none()
            users = self.UserModel.objects.filter(username__iexact=preferred_username)
        return users

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email")
        user.username = self._get_username(claims)
        user.save()
        return user

```

If, for example, you're only interested in making changes to the create_user method, you could just subclass KeycloakOIDCAuthenticationBackend and create your own create_user method:

```
...

class MyKCAuthBackend(KeycloakOIDCAuthenticationBackend):

    ...

    def create_user(self, claims):
        
        ... Add your code here ...

        return user
```

---

### Custom Dashlets

You can use dashlets to provide simple modular components that can be added to the dashboard or other areas of the application. It includes a default dashlet (MOTD), and you can also create custom dashlets in the extensions directory.

Organize dashlet files in this structure:

```
extensions/apps/dashlets/
├── admin.py
├── forms.py
├── __init__.py
├── models.py
├── templates
│   └── dashlets
├── tests.py
├── utils
│   ├── __init__.py
└── views.py
```

Think of each dashlet as a combination of a model (and potentially supporting models), a view, a form if needed, and a template. Familiarity with Django's MVT (Model-View-Template) paradigm will be helpful, as each component plays a role:

- **Model:** Stores structured data.
- **View:** Handles logic.
- **Template:** Presents the output.

#### Example: Custom Dashlet for Recent Documents

To create a custom dashlet displaying recent documents, first create a template file named recent_documents.html:

**Path:** extensions/apps/templates/dashlets/recentdocs/recent_documents.html

```
<section class="w-full md:w-3/4 p-4 mx-6 bg-white rounded-lg shadow-md outline outline-offset-1 outline-1 outline-gray-200 mt-4">
  <h3 class="text-xl font-semibold mb-2">Recent Documents Dashlet</h3>

  <table class="min-w-full divide-y divide-gray-200 border shadow">
    <tr>
      <th class="fl-th">Name</th>
      <th class="fl-th">Owner</th>
      <th class="fl-th">Created</th>
    </tr>
    <tbody class="bg-white divide-y divide-gray-200">
    {% for document in documents %}
        <tr>
            <td class="px-6 py-4 whitespace-nowrap text-gray-700 text-sm">
              {{ document.name|truncatechars:30 }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-700 text-sm">
              {{ document.owner.username }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-700 text-sm">
              {{ document.created }}
            </td>
        </tr>
    {% endfor %}
    </tbody>
  </table>
</section>
```

Then, include this dashlet on the main dashboard by copying app/repo/templates/ui/index.html to extensions/templates/ui/index.html and editing it as follows:

```
{% extends "ui/base/_base.html" %}

{% block main %}
<main>
  {% include "ui/partials/_enhanced_description.html" %}
  {% if use_motd %}
    <div class="py-2">
      {% include "motd/message.html" %}
    </div>
  {% endif %}

  {% include "dashlets/recentdocs/recent_documents.html" %} <!-- Include this line -->

  <div class="py-8">
    {% include "ui/partials/_getting_started.html" %}
    <div class="flex py-8">
      {% include "ui/partials/_project_list.html" %}
      {% include "ui/partials/_latest_documents.html" %}
    </div>
  </div>
</main>
{% endblock main %}
```

#### Updating the Dashboard View

In extensions/apps/repo/views.py, subclass the IndexView to add recent documents to the dashboard template:

```
from django.shortcuts import render
from apps.repo.models.element.document import Document
from apps.repo.views.index import IndexView


class IndexView(IndexView):
    def get(self, request):
        super().get(request)

        # Fetch recent documents
        recent_documents = Document.objects.all().order_by("-created")[:10]

        # Update the context with the recent documents
        self.context.update({"documents": recent_documents})

        # Render the updated context in the response
        return render(request, self.template_name, context=self.context)
```

After restarting your server, navigate to the home page to see the recent documents listed in the new dashlet.

---

### Custom Action Modal

By default, DocrepoX has a few folder actions that make use of action modals:

* Upload a document
* Upload several documents
* Create a folder
* Clipboard modal

In this tutorial, you'll create a very simple modal that will display as an action icon and then when clicked will show a "Hello World".

Before starting, ensure that ENABLE_EXTENSIONS is set to True.

Copy the _folder_actions.html template from apps/repo/templates/repo/partials/actions/_folder_actions.html to extensions/templates/repo/partials/actions/_folder_actions.html.

Make the following change at this location in _folder_actions.html:

```
...
      <a href="#"
        class="hover:text-blue-700 relative group mr-2"
        onclick="showModal('addFolderModal')"
        title="Create a new folder in this space">
        <span class="material-icons-outlined">create_new_folder</span>
      </a>
      <a href="#"
        class="hover:text-blue-700 relative group mr-2"
        onclick="showModal('pasteElementModal')"
        title="Clipboard for items to be Moved/Copied">
        <span class="material-icons-outlined">content_paste</span>
      </a>

      <!-- add the following block -->
      <a href="#"
        class="hover:text-blue-700 relative group mr-2"
        onclick="showModal('displayHelloWorld')"
        title="Displays a hello world message">
        <span class="material-icons-outlined">chat_bubble</span>
      </a>

    {% endif %}
  </div>
...
```

And further down, in the same file, you will need to import the modal that you intend to create.

```
...
{% if can_create %}
  {% include "repo/partials/_add_document_modal.html" %}
  {% include "repo/partials/_add_multi_document_modal.html" %}
  {% include "repo/partials/_create_document_modal.html" %}
  {% include "repo/partials/_add_folder_modal.html" %}
  {% include "repo/partials/_hello_modal.html" %} <!-- add an include here -->
  {% include "clipboard/partials/_paste_element_modal.html" %}
...
```

Create a file at extensions/templates/repo/partials/ called _hello_modal.html. Add the following contents:

```
<div x-data="handleClipboardModal({hasErrors: {{ 0 }}})">
  <div id="displayHelloWorld"
    x-ref="displayHelloWorld"
    class="hidden fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full"
  >
    <div class="relative top-20 mx-auto p-5 border w-[450px] shadow-lg rounded-md bg-gray-900 text-white">
      <div class="material-icons-outlined mb-4">chat_bubble</div>
      <h3 class="text-lg font-bold leading-6 text-gray-100 mb-4">
        Say Hi!
      </h3>
      <div>
        <p>Hello World!</p>
      </div>
      <div class="flex justify-center mt-[72px] space-x-2">
        <button class="bg-gray-500 text-white font-semibold py-2 px-4 rounded" type="button"
          onclick="hideModal('displayHelloWorld')"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</div>
```

And that's it. After a restart, you should see a tooltip icon on the folder list page next to the Create Folder icon. Clicking on it should render a message.

---

<a id="customize-table-sorting"></a>
### Customizing Sortable Table Columns for Folder View

The template you will need to overwrite is at apps/repo/templates/repo/element_list.html

Place a copy of this template in the extensions/templates/repo folder.

```
<thead class="bg-gray-50">
  <tr>
    <th class="fl-th">
      {% include "repo/partials/_sortable_th.html" with column_name="name" %}
    </th>
    <th class="fl-th">
      {% include "repo/partials/_sortable_th.html" with column_name="title" %}
    </th>
    <th class="fl-th">Owner</th>
    <th class="fl-th">
      {% include "repo/partials/_sortable_th.html" with column_name="created" %}
    </th>
    <th class="fl-th">
      {% include "repo/partials/_sortable_th.html" with column_name="modified" %}
    </th>
    <th class="fl-th">Actions</th>
  </tr>
</thead>
```

For example, to make the Owner column sortable, remove 'Owner' from the <th> element and replace it with:

```
{% include "repo/partials/_sortable_th.html" with column_name="owner" %}
```

The column name must match up with a field for an Element. Here are the available element fields:

- Name
- Title
- Description
- Owner
- Created
- Modified
- Parent

See the Folder and Document models for details on what more could be used here.

The _sortable_th.html template below could be used for any named column field name that is supported for the views result object.

```
{% load static %}

<div class="flex align-items gap-1">
  <a href="." class="hover:text-blue-700">
    {{ column_name }}
  </a>
  <a href="#"
    x-data="orderByToggle('{{ column_name }}')"
    :href="`?order_by=${nextOrderBy}`"
    class="hover:text-blue-700"
  >
    <span class="material-symbols-outlined" style="font-size: 15px !important;">
      swap_vert
    </span>
  </a>
</div>

<script src="{% static 'js/repo/utils/table-sort.js' %}"></script>
```

To customize the _sortable_th.html template, copy it to its appropriate extensions directory: extensions/templates/repo/partials/.

Note that this template uses Alpine js to handle sort toggling. 

Other items of note:

- swap_vert: simply a Google icon. If you prefer to customize this to use a different icon, see: https://fonts.google.com/icons

---

### Property Model Usage

The Property model provides a flexible way to attach typed key-value pairs to Document,
Folder, and Project models. This documentation explains how to use the Property system.

**Setting Up Your Model**

First, make your model property-enabled by inheriting from the HasProperties mixin:

```python
from .property import HasProperties

class Folder(models.Model, HasProperties):
    name = models.CharField(max_length=255)
    # ... other fields ...
```

**Available Property Types**

The following property types are supported:
- 'str': String values
- 'int': Integer values
- 'float': Floating-point numbers
- 'bool': Boolean values
- 'datetime': DateTime objects
- 'json': JSON-serializable data (lists, dicts, etc.)

**Basic Usage**

Setting properties:

```python
# Get your instance first
folder = Folder.objects.get(id='your-uuid-here')

# String property (default type)
folder.set_property('description', 'Main documentation folder')

# Integer property
folder.set_property('max_files', 100, type_name='int')

# Boolean property
folder.set_property('is_restricted', True, type_name='bool')

# Float property
folder.set_property('size_limit_gb', 10.5, type_name='float')

# DateTime property
from datetime import datetime
folder.set_property('review_date', datetime.now(), type_name='datetime')

# JSON property (lists, dicts, etc.)
folder.set_property('allowed_types', ['pdf', 'doc', 'txt'], type_name='json')
```

Getting properties:

```python
# Get with default value if not found
description = folder.get_property('description', default='No description')
max_files = folder.get_property('max_files', default=50)

# Values are returned with correct Python type
allowed_types = folder.get_property('allowed_types')  # returns a list
is_restricted = folder.get_property('is_restricted')  # returns a boolean
```

**Additional Usage**

Get all properties for an object:

```python
all_properties = folder.get_all_properties()
for prop in all_properties:
    print(f"{prop.key}: {prop.get_typed_value()} ({prop.type})")
```

Delete a property:

```python
folder.delete_property('max_files')
```

Querying properties:

```python
# Find all folders with a specific property
folders_with_prop = Folder.objects.filter(
    properties__key='is_restricted',
    properties__value='true'
)

# Find all properties of a specific type
int_properties = Property.objects.filter(type=Property.PropertyType.INTEGER)
```

**Type Validation**

The Property model includes automatic type validation:

```python
# This will raise a ValidationError
try:
    folder.set_property('max_files', 'not a number', type_name='int')
except ValidationError:
    print("Invalid value for integer property")

# This will raise a ValueError
try:
    folder.set_property('status', 'active', type_name='invalid_type')
except ValueError:
    print("Invalid property type")
```

**Important Notes**

- Properties are unique per (object, key) pair - setting an existing key updates the value
- Properties are stored as text in the database but converted to/from Python types automatically
- The Property model supports UUIDs for object_id field, compatible with UUID primary keys
- Boolean values can be set using Python booleans (True/False)
- JSON properties can store any JSON-serializable data structure
- DateTime properties are stored in ISO format
- The Property model is indexed for efficient querying
- Properties are automatically deleted when their parent object is deleted
