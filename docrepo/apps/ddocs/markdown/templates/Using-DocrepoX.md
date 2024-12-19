## Using DocrepoX

### Licensing

DocrepoX LGPLv3

For commercial licensing inquiries, contact documendous@gmail.com.

To view the license in its entirety see LICENSE.txt in this repository.

### Support

#### Supported Features

All features listed in the "Using DocrepoX" and "Customizing DocrepoX" sections are fully supported and should function as described. If you experience any issues, please report them by creating an issue.

#### Unsupported Features Requiring Consulting

Any features not covered in the "Using DocrepoX" section, including those related to development documentation, are not supported and will require consulting services.

### Startup

When the application starts, a default admin user is created with the following credentials:

- **Username:** admin  
- **Password:** admin  
- **Email:** admin@localhost  

To customize these credentials, update the following variables in your .env file to values appropriate for your environment:  

- ADMIN_USERNAME  
- ADMIN_EMAIL  
- ADMIN_PASSWORD  

After the initial startup, ensure you update the admin user's password if you haven't already done so.

### Locale and Timezones

#### Local Browser Timezone

By default, DocrepoX uses tz_detect to manage local browser timezones. This behavior is controlled in apps/repo/settings.py with the following setting:

```
USE_LOCAL_TZ = True
```

To disable this feature, set USE_LOCAL_TZ to False and re-login, as the timezone preference is stored in the user's session.


### Keycloak Integration with DocrepoX

To set up Keycloak with DocrepoX, follow these steps:

#### Setting Up Keycloak in Docker

If you want to include Keycloak and its database in your Docker setup, update docker-compose.yml as follows:

```
### Uncomment the following lines to enable Keycloak and its database services
# kcdb:
#   image: postgres
#   volumes:
#     - dev_postgres_data_kc:/var/lib/postgresql/data
#   environment:
#     POSTGRES_DB: keycloak
#     POSTGRES_USER: keycloak
#     POSTGRES_PASSWORD: password
#     POSTGRES_PORT: 5432
#   ports:
#     - "8764:5432"

# keycloak:
#   image: quay.io/keycloak/keycloak:23.0.5  # Specify version or use 'latest'
#   environment:
#     DB_VENDOR: POSTGRES
#     DB_ADDR: kcdb
#     DB_DATABASE: keycloak
#     DB_USER: keycloak
#     DB_PASSWORD: password
#     KEYCLOAK_USER: admin
#     KEYCLOAK_PASSWORD: admin
#     KEYCLOAK_FRONTEND_URL: http://keycloak:8080/auth
#   command: 
#     - start-dev  # Use for the latest version
#   ports:
#     - 8080:8080
#   depends_on:
#     - kcdb

volumes:
  ...
  ### Uncomment for Keycloak:
  # dev_postgres_data_kc:
```

#### Using Mozilla Django OIDC

DocrepoX uses the Mozilla Django OIDC library to support Keycloak's OpenID Connect protocol. Ensure the following is configured:

The library is already installed in pyproject.toml:

```
mozilla-django-oidc = "^4.0.1"
```

In config/settings/security.py, enable Keycloak:

```
USE_KEYCLOAK = True
```

Add OIDC URLs in config/urls.py:

```
urlpatterns = [
    ...
    # path("auth/oidc/", include("mozilla_django_oidc.urls")),  # Uncomment for Keycloak
    path("", include("apps.repo.urls")),
]
```

Configure Keycloak settings in config/settings/oidc.py:

```
from .utils import env

KC_HOST = env("KC_HOST")
REALM = env("KC_REALM")
OIDC_RP_CLIENT_ID = env("KC_CLIENT")
OIDC_RP_CLIENT_SECRET = env("KC_CLIENT_SECRET")

OIDC_RP_SIGN_ALGO = "RS256"

OIDC_OP_AUTHORIZATION_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/auth"
OIDC_OP_TOKEN_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/token"
OIDC_OP_USER_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/certs"

OIDC_STORE_ACCESS_TOKEN = True
OIDC_STORE_ID_TOKEN = True

OIDC_OP_LOGOUT_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/logout"
OIDC_OP_LOGOUT_URL_METHOD = "apps.authentication.backends.provider_logout"
```

To ensure session validity, add this middleware:

```
MIDDLEWARE.append("mozilla_django_oidc.middleware.SessionRefresh")
```

#### Environment Variables

Set the following variables in your .env file:

```
KC_HOST=http://keycloak:8080  # Default for Linux Docker environments
KC_REALM=documendous  # Your Keycloak realm
KC_CLIENT=documendous  # Your Keycloak client
KC_CLIENT_SECRET=my-secret  # Found in the client credentials tab in Keycloak
```

#### Starting the Integration

Run the application using dev-up.sh. On the login page, you should see a link to the Keycloak login provider. Ensure a user is created in the DocrepoX client within the Documendous realm.

#### Additional Recommendations

If you're new to Keycloak, review the Keycloak documentation. See https://www.keycloak.org/documentation. 

For easier setup, import the provided documendous-realm.json file when creating your Keycloak realm. Note that this file must be imported at the time of realm creation, not from the admin interface. Update the client URLs in Keycloak if your hostname or port is different.

### Minio

Some things to consider:

* This is a serious architecture decision. Treat it as such. You either use Minio or the Django default storage.
* This should be decided upon from the beginning. If you start off with default and switch to Minio, you will not be able to access your default stored file for your document. If you use Minio and switch to default storage, you will not be able to access your Minio stored file for your document.
* Switch Minio with AWS S3 and this means pretty much the same.
* If you do not understand Minio or AWS S3, we recommend using default storage. If you do understand Minio or AWS S3 very well, then use that.

It is possible to switch midstream but this would require consulting hours from Documendous Software to assist with that and be supported.

#### Initial Setup

Ensure the following settings are in config/settings/storage.py:

```
DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"

MINIO_STORAGE_ENDPOINT = "minio:9000"

MINIO_STORAGE_ACCESS_KEY = env("STORAGE_ACCESS_KEY")

MINIO_STORAGE_SECRET_KEY = env("STORAGE_SECRET_KEY")

MINIO_STORAGE_USE_HTTPS = False

MINIO_STORAGE_MEDIA_OBJECT_METADATA = {"Cache-Control": "max-age=1000"}

MINIO_STORAGE_MEDIA_BUCKET_NAME = env("STORAGE_MEDIA_BUCKET_NAME")

MINIO_STORAGE_MEDIA_BACKUP_BUCKET = "Recycle Bin"

MINIO_STORAGE_MEDIA_BACKUP_FORMAT = "%c/"

MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True

# STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"

# MINIO_STORAGE_STATIC_BUCKET_NAME = "docrepo"

# MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
```

* In config/settings/__init__.py, uncomment the following:

```
### Uncomment the following import to use Minio:
# from .minio import (
#     INSTALLED_APPS,
#     DEFAULT_FILE_STORAGE,
#     MINIO_STORAGE_ENDPOINT,
#     MINIO_STORAGE_ACCESS_KEY,
#     MINIO_STORAGE_SECRET_KEY,
#     MINIO_STORAGE_USE_HTTPS,
#     MINIO_STORAGE_MEDIA_BUCKET_NAME,
#     MINIO_STORAGE_MEDIA_BACKUP_BUCKET,
#     MINIO_STORAGE_MEDIA_BACKUP_FORMAT,
#     MINIO_STORAGE_MEDIA_OBJECT_METADATA,
#     MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET,
# )
```

Note that static storage is commented out. We don't recommend using Minio for static (docrepo's css/js/img files that are part of the product) but you can use this if you like.

* Also, uncomment the appropriate area in your docker-compose.yml. For example:

```
services:
  ...
### Uncomment the following to use Minio
  # minio:
  #   # See https://hub.docker.com/r/minio/minio/tags
  #   image: quay.io/minio/minio:RELEASE.2024-07-16T23-46-41Z.fips
  #   environment:
  #     - MINIO_ROOT_USER=admin
  #     - MINIO_ROOT_PASSWORD=adminpass
  #   entrypoint: /bin/bash
  #   command: -c 'minio server /data --console-address ":9001"'
  #   volumes:
  #     - miniodata:/data
  #   ports:
  #     - "9000:9000"
  #     - "9001:9001"

volumes:
  ...
  ### Uncomment the following to use Minio
  # miniodata:
  #   driver: local
```

* Log into Minio at http://localhost:9000 with admin:adminpass (Ensure you secure your installation of course)

* Create a bucket called docrepo or whatever you want to name it.

Enter the bucket name into your .env file:

```
MINIO_STORAGE_MEDIA_BUCKET_NAME=docrepo
```

* Create a user called docrepo.

* For the docrepo user, create the secret key and access key.

* Give this user readwrite access.

* Collect the access key and secret key.

Enter them into your .env file:

```
MINIO_STORAGE_ACCESS_KEY=<your access key>
MINIO_STORAGE_SECRET_KEY=<your secret key>
```

Restart your docker containers. If you delete your volumes however, you'll have to repeat the process.

### Elastic Search

Note that elastic search is not implemented yet.

Here are directions however for adding Elastic Search to this project. 

* In docker-compose.yml uncomment this block:

```
# Elastic Search
  # elasticsearch:
  #   image: elasticsearch:8.15.1
  #   volumes:
  #     - es_data:/usr/share/elasticsearch/data
  #   ports:
  #     - 9200:9200
  #     - 9300:9300
  #   environment:
  #     - discovery.type=single-node
  #     - xpack.security.enabled=false
```

and ...

```
volumes:
  ...
  ### Uncomment to use Elastic
  # es_data:
```

Do the same in docker-compose.prod.yml as well if you wish to use that environment.

* In docrepo/config/settings/__init__.py:

```
# ## Uncomment to use elastic
# from .elastic import ELASTICSEARCH_DSL
```

* In docrepo/config/settings/apps.py:

```
# "django_elasticsearch_dsl", ## Uncomment to use elastic search
```

* If you're using test.sh script for testing, be sure to include these parts:

```
# Uncomment to test with Elastic
# docker compose up elasticsearch &
# sleep 10

...
# Uncomment to test with Elastic
# docker compose down elasticsearch
```

* To use search indexing in your docker containers, enable the following in entrypoint.sh and entrypoint.prod.sh:

```
# Uncomment to use Elastic search indexing
# python manage.py search_index --rebuild -f
```

### Troubleshooting

#### Download Size is Limited

To restrict or increase the size of file downloads, update the client_max_body_size property in nginx.conf as shown below:

```
server {

    listen 80;

    client_max_body_size 1g;
    ...
}
```

**Note:** Restart the server for the changes to take effect.

#### *No preview or download available*

This warning appears on a document detail page when either:

- The document has no data (its content file is empty).
- The content file for the latest document version is missing.

Content files are stored in a date-time structured folder system within the mediafiles/ directory. If a content file is deleted, previews and downloads will not be available.

#### Docker

##### Error response from daemon: network [long hash] not found

You may need to run something like this:

```
# docker compose -f docker-compose.prod.yml up --build --force-recreate
```

#### Settings

In a containerized environment, you can find information about your settings using:

```
python manage.py diffsettings
```

For example, if you're using the production containerized setup, in entrypoint.prod.sh uncomment the diffsettings command:

```
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py diffsettings
```

Warning: the diffsettings will display the values passwords and secret keys. This should be turned on while your install is exposed to the public.

### Get Support  

To receive assistance, click the **Support** link in the footer to open an issue.  

#### Types of Requests

1. Enhancement Request

Describe how something can be improved. Be specific about what changes you’d like to see.  

2. Feature Request

Suggest a new feature that doesn’t currently exist. Explain why it would be valuable or necessary.  

3. Bug Fix

Report an issue by explaining what isn’t working correctly. Include relevant details for troubleshooting.

### UI

#### Dashboard

This guide will help you understand the various sections and features available on the main dashboard.

The DocrepoX dashboard provides an easy-to-use interface for managing and organizing your digital assets and documents. Below is a breakdown of the different sections and their functionalities.

##### Navigation

The header includes several icons for quick navigation:

- **Documendous Logo**: Click to return to the main dashboard.
- **Home Icon**: Navigate back to the home screen.
- **Documents Icon**: Access the document management section to view and manage your documents.
- **Projects Icon**: View and manage your projects.
- **Bookmark Icon**: List of user's bookmarks.
- **Admin Console**: An admin console for use by the system admin user.
- **User Profile Icon**: Access your user settings and profile information.
- **Notifications Icon**: View any notifications and alerts.

##### Welcome Section

This section provides a brief introduction to DocrepoX and its features. It highlights the following points:

- **ECM and DAM**: DocrepoX helps you manage digital assets and documents efficiently.
- **Scalability**: Suitable for businesses of all sizes.
- **Integration**: Works seamlessly with your current systems and third-party applications.
- **Security**: Ensures your data is protected with advanced permissions and encryption.
- **Innovation**: A tool designed to enhance your document management processes and drive innovation.

You can remove the welcome section and the documentation links section by clicking the close button to the right of these areas. If needed, the admin user can reset these settings: 'show_welcome' and 'show_getting_started' in the admin console under UI Settings per user by changing the value to 'true'.

For example if the admin user wants to reset 'show_welcome' to 'true', look for UI Setting: "admin | show_welcome: false", go to its change page and change the string, 'false' to 'true'.

#### Dashlets

DocrepoX makes use of dashlets as a way of providing simple components that can be added to the dashboard or other areas in the application.

* **Message of the Day (MOTD) Dashlet**

A message of the day can be created to be displayed on the dashboard.

Steps to include an MOTD:

1. Set USE_MOTD = True in config/settings/dashlets.py.
2. Create a new MOTD in the admin console.
3. Set the new MOTD is_published to True.

Of course, to disable the MOTD dashlet, set USE_MOTD=False in config/settings/dashlets.py

#### Getting Started

The **Getting Started** section provides introductory information to help you begin using DocrepoX. Currently, it displays a placeholder message "Docs to come ...", indicating that detailed documentation will be available soon.

#### Latest Content

The **Latest Content** section shows the most recent documents added to your system. It currently displays a placeholder message "List of documents in your home folder or projects ...", indicating where your recent documents will be listed.

By default, the number of content items for projects and documents shown on the dashboard in each section is set to 5. This can be changed in ui/settings.py: MAX_CONTENT_ITEM_SIZE.

### Projects

The **Projects** section lists all your active projects. It currently displays a placeholder message "List of projects ...", indicating where your projects will appear.

#### Searching for Projects

Public Projects
- All public projects are automatically visible in your project list
- No special access or search required

Finding Additional Projects
- Use the search function to discover more projects
- Type any part of the project name in the search box
- Search results will include:
  - Public projects
  - Managed projects
  - Private projects (if you have permissions)

#### Requesting Access and Joining a Project

##### Join Process

1. Look for the join request icon next to projects you're not a member of
2. Click the icon to send a membership request
3. Project managers will receive your request
4. Once requested:
   - The join request icon will disappear (a pending icon will show)
   - You'll see a confirmation message
   - Your request remains pending until managers approve or decline

###### After Requesting

- The join request icon remains hidden while your request is pending (a pending icon will show)
- Managers must either:
  - Approve your request and add you to the project
  - Decline your request
  - Remove the pending request message

#### Project Access Levels

Once approved, you may be added as:

- A reader (view-only access)
- An editor (can add documents and folders and make changes)
- A manager (full project control)

_Note: Your specific access level will be determined by the project managers._

As a member of a project, you will be able to see your role and access level below the navigation links in the project's folder view.

#### Project Details

For each project that you own or manage, you can view the project's details by clicking on the gear symbol to the right of it either in the actions to the right of the project in the folder list view or on the gear symbol while in the project (near the breadcrumb or in a project folder or document's detail page).

In the project details page, you will see these fields:

- Name
- Title
- Description
- Visibility

From this page, if you are a project editor or manager, you can update its details.

Visibility means the intended audience. By default there are 3 options:

- Public: any user can find this project and join as a reader.
- Managed: any user can find this project but must be approved by the project manager to join.
- Private: a user will not find this project in a search and must be invited to this project to join.

Below the project details are a list of the project's Managers, Editors and Readers. Each of these groups have a specific role.

- Manager: Denotes project ownership. A project manager can add, edit and delete documents.
- Editor: A project editor can add and edit documents.
- Reader: A project reader can only consume the content.

A member of any project will be able to access all folders in the project. All users regardless of membership will be able to access all folders in a project whose visiblity is set to 'Public'.

The project details page includes a section at the bottom where users can add comments. This feature can be enabled or disabled by setting ENABLE_PROJECT_COMMENTS = True or False in repo/settings.py.

The comment author can delete their own comments.

Project managers can delete any comments on project details, documents or folders.

Public projects can enable comments by anyone including non-members if ENABLE_PUBLIC_COMMENTS is set to True.

### Deactivating a Project

Only project owners can deactivate projects, preventing them from appearing in searches or project lists, regardless of visibility settings.

To deactivate a project, the owner should navigate to the project detail page, scroll to the bottom, and select the option to deactivate the project. Reactivating the project requires the system admin user to access the admin console, locate the project, and set is_active=True by checking the **is_active** checkbox.

### Folder View

#### Folder Actions (shown above the element list)

* Add Documents: This will open an add document modal where the user can add a document to the current folder.

* Create Documents: By default, a new page opens to create a text file in the current folder. To use a modal instead, set CREATE_DOC_USE_MODAL=True in repo/settings.py (rich text not supported). If CREATE_DOC_USE_MODAL=False, enable rich text with CREATE_DOC_AS_RTF=True, which uses the Quill editor. Note: Quill generates and saves HTML content as "text/html" regardless of file extension.

* Upload Multiple Documents: This will allow the user to upload many documents at once. However, this process will automatically create the document names based on the file name. You will be able to make changes to name, title, description, etc. on the document details page.

* Add Folders: This will open an add folder modal where the user can create a subfolder in the current folder. Be aware that 'Recycle' is a reserved system name for folders and cannot be used when creating a folder.

* Clipboard: The clipboard temporarily stores documents and folders for moving to another folder. Items can be removed before pasting. A blue clipboard icon appears next to items in the folder list and disappears after pasting. By default, the clipboard is cleared on logout, but setting DELETE_CLIPBOARD_ON_LOGOUT=False saves items between sessions.

#### Element List View

In the folder view are a list of subfolders and documents (child elements) in the parent folder view.

Each child element should show:

- Name (along with bookmark status if bookmarked)
- Title
- Owner
- Created and Last Modified dates
- List of Actions available for each element

By default, items in the folder view will paginate by 10. This can be changed in repo/settings.py by changing:

```
FOLDER_VIEW_PAGINATE_BY = 10
```

By default, the following columns are sortable:

- Name
- Title
- Created
- Modified

There is a sort icon to the right of the column header. The sort icon toggles between ascending and descending. Clicking on the column head will set the table order back to its default.

For info on customizing table columns see "Customizing Sortable Table Columns for Folder View" in Customizing DocrepoX.

#### Actions

* You can move documents and folders by clicking on the move icon. This will place elements in the user's clipboard (see Clipboard in Folder Actions section).

* You can recycle documents and folders (and their contents) by clicking on the trashcan icon. This will place the document/folder into your Recycle folder. Note that once documents and folders are moved to your recycle folder, you can only move them by restoring them to their original parent folder.

* In the Recycle folder you can then either permanently delete them or restore them to their former parent folder.

* There is also the option of clicking on the trashcan icon to empty all items in the Recycle folder. This will permanently delete all items.

* On the detail page, you can view details about a folder or document. From here you can download a document (or preview if your browser supports the mimetype or if a previewable PDF file is generated for it) and bookmark either a document or folder.

* Note that bookmarks are removed when a document has been recycled or deleted.

* If you own a folder or document, you can update its details from the details page.

* If you need to find the content file path (on the file system) for a document, you can see this in the document details page if you are the admin user. Note that the admin user can also find this information in the admin console.

#### Updating Document/Folder/Project Details

Only the owner (or project editor and manager if in a project) can update the details of the document or folder.

You can update the following:

- Name
- Title
- Tags
- Description

As a project member, you can bookmark documents and folders within the project. In the standard repository, however, you can only bookmark items that you own.

##### Tags

* Tags must be comma delimited.
* By default MAX_TAG_COUNT is set to 5 but this can be changed in apps/etags/settings.py file.

### Special Elements

- User's recycle folder - this folder will not show by default for DocrepoX users though it can be accessed via the recycle folder icon. The recycle folder details cannot be updated.

### Comments

At the bottom of folder and document detail pages, users can add comments. To enable or disable this feature, update repo/settings.py as follows:

- For folders: ENABLE_FOLDER_COMMENTS = True or False
- For documents: ENABLE_DOCUMENT_COMMENTS = True or False
- For projects: ENABLE_DOCUMENT_COMMENTS = True or False

Any comment author can delete his/her own comments.

### Transformations

#### Generating Previews and PDFs with Transformations

DocrepoX provides features for handling document transformations, including generating previews and PDFs. This guide explains how these features work and how they integrate into the platform.

---

#### **Generating Previews**

Note: In order to be able to view previews, you must have LibreOffice (or OpenOffice) installed on your system. The path to its binary must be set in apps/transformations/settings.py: 

```
SOFFICE_EXE = (
    "/usr/bin/soffice"  # Path to open/libre/star office executable for transformations
)
```

If you are using the docker containers, then LibreOffice should be installed.

Previews allow you to quickly view document content without downloading the full file. Supported file types include .doc, .docx, .jpg, .png, .pdf, and more.

##### **How Previews Are Generated**

1. When a document is uploaded, the system checks:
   - File size (must be under 10MB).
   - File type (must be one of the supported preview types).
2. If the file meets the criteria, a preview file is generated automatically using LibreOffice (for transformable types) or directly from the content (for supported image and PDF files).

##### **Preview Actions**

View previews directly from the document details page.

##### **Troubleshooting**

- If a preview is unavailable, ensure the document meets the size and type requirements.
- Admins can check the system logs for errors, such as missing LibreOffice executables or unsupported file extensions.

#### **PDF Generation**

For transformable file types (e.g., .docx, .pptx, .xls), DocrepoX uses LibreOffice to convert files into PDF format. This ensures compatibility and easier preview generation.

##### **When PDFs Are Generated**

- If a document is not already in PDF format, a transformation process is triggered.
- PDF files are stored temporarily for processing before preview files are created.

##### **Key Requirements**

- The LibreOffice executable (/usr/bin/soffice) must be installed and configured in the system settings.
- Supported file types for transformation include .doc, .docx, .ppt, .pptx, .xls, .xlsx, .txt, and .md.

#### **Configuration Settings**

The following settings ensure proper functionality for transformations:
- **SOFFICE_EXE**: Path to the LibreOffice executable.
- **SOFFICE_TEMP_DIR**: Temporary storage for transformation processes.
- **ALLOWED_PREVIEW_TYPES**: List of file extensions allowed for previews.
- **MAX_PREVIEW_SIZE**: Maximum file size for preview transformation (10MB).

#### **Auto-Deleting Previews**

When a preview file is deleted, the system automatically removes its associated content file from storage, freeing up space. This can be set in repo/settings.py with AUTO_DELETE_CONTENT_FILES=True (or False for retaining all document version files).

#### **Using the Features**

1. **Preview Files**
   - Navigate to the document details page to view a preview if available.
   - If no preview is displayed, the document may have exceeded size limits or uses an unsupported type. There can also be an issue where the document version content file is accidentally deleted.

2. **Download Options**
   - Users can download original files or their previews (if supported by the browser or as a previewable PDF).

#### **Best Practices**
- For performance consideration with large files, consider compressing them or breaking them into smaller parts.
- Always ensure your files are in supported formats to take full advantage of previews and transformations.


## Administering DocrepoX

### Maintenance Tasks

#### Removing Orphan Content

##### Managing Orphaned Content Files

Orphaned content files are files that no longer have a linked document version or rendition, such as thumbnails or previews.

This typically happens when `AUTO_DELETE_CONTENT_FILES` is set to `False`. In this setting, content files are not fully deleted even when the parent documents or renditions (e.g., thumbnails or previews) are removed.

Here is the document lifecycle in the system:

- A file is uploaded, creating a document. A new version of the document is also created automatically.
- While the document exists in the system, additional versions can be added.
- The document is recycled (soft deleted and moved to the user's recycle folder).
- The document is permanently deleted (hard deleted) from the recycle folder.
- If `AUTO_DELETE_CONTENT_FILES` is set to `True`, the associated content files for each document version are deleted from the system when the document is hard deleted.
- If `AUTO_DELETE_CONTENT_FILES` is set to `False`, the associated content files remain in the file system. In such cases, it is recommended to periodically run the `manage.py remove_orphan_content` command to clean up orphaned content files.

To maintain a clean and organized system, orphaned content files should be removed regularly. This can be done manually using the Django management command:

```
# python manage.py remove_orphan_content
```

When this command runs, any orphaned files detected will be moved to a designated folder specified in `repo/settings.py`:

```
DELETED_ORPHAN_FOLDER = BASE_DIR / "deleted"  # "deleted" is the default folder name
```

Regularly clearing orphaned content helps free up storage and improve system performance. Adjust the folder path in `settings.py` if a different location is preferred.

##### Automating Orphaned Content Cleanup

To automate this process, schedule the command to run periodically using supported task schedulers:

#### **1. Using Cron (Linux/Unix):**
1. Open the crontab editor:
   ```
   crontab -e
   ```
2. Add a cron job to run the command at the desired frequency (e.g., daily at midnight):
   ```
   0 0 * * * /path/to/your/project/.venv/bin/python /path/to/your/project/manage.py remove_orphan_content
   ```

Automating this process ensures your system stays clean without manual intervention, improving storage efficiency and system performance.