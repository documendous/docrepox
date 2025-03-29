# Release Notes

## March 29, 2025 – v25.1.0

### New Features
- Document Sharing: Share any document externally using a secure proxy link.
- Encrypted File System (Experimental): Early access to our new encrypted content storage.
- Bulk Upload Tool: Upload multiple documents at once for faster onboarding.
- Indexing Tool: Converts documents to pdf and then to text storage for quick search.
- Versioned Metadata: Documents now include additional metadata sections, including version history.
- Profile Avatars: Users can now upload avatars to personalize their profiles.
- Custom Properties: Easily add custom metadata fields to documents and folders.
- Advanced Search: Improved search with powerful filtering and keyword support.
- Internal Messaging

### Enhancements
- Expanded and improved documentation, including troubleshooting and logging guides.
- Streamlined UI for metadata views across documents, folders, and projects.
- Removed outdated single-document upload feature.
- Added indexes to table creation scripts for better performance.
- Enhanced security for document access and retrieval.
- Improved sorting and pagination for a smoother browsing experience.

### Bug Fixes
- Fixed issues with zero-byte document uploads.
- Resolved edge case errors in document indexing.
- Addressed Jazzmin integration inconsistencies.

---

## Feb 28, 2025 - v24.4.2

### Enhancements
- Bulk item removal enhancement
- Search and filter ui improvement
- Enhanced file name display – Truncated file names and paths now display a tooltip with the full name or path for better visibility.
- Persistent filter selection – Filters now remain active when users add documents to the clipboard, improving workflow continuity.
- Improved document preview experience
- Improved ui styling

### Bug Fixes
- Fixed error displays on forms
- Fixed long form input descriptions causing layout issues in details table
- Fixed admin users recycle folder issues while `allow_admin_all=True`
- Corrected removed projects still appearing in user’s bookmark list
- Solved upload new document icon indication issues
- Solved bookmark cards not showing project details when bookmarkable
- Fixed project bookmarks icon issues
- Corrected project group issues
- Fixed modification date missing updates on new version uploads

## Upcoming: v25.1.0 (April 1, 2025)
- Advanced Search page
- Custom Element Properties
- Multi-select UI functionality
- Internal messaging
- Bulk upload capabilities
- Encrypted Document capabilities
- Multi-select functionality for delete, restore, copy/move actions

---

## Jan 30, 2025 - v24.4.1  

### Enhancements  
- Added upgrade documentation  
- Expanded element actions  
- Integrated Jazzmin for Django Admin console  
- Introduced new global settings capability  

### Bug Fixes  
- Resolved user home folder renaming issues  
- Fixed recycle folder bugs  
- Addressed PDF preview problems  
- Fixed major move/copy issues  
- Resolved project visibility and access issues  
- Fixed ALLOW_ADMIN_ALL setting bugs  
- Corrected minor Tailwind styling issues  
- Fixed folder size reporting inaccuracies  
- Resolved major project deletion problems  

### Other Updates  
- Improved documentation  
- Various UI enhancements  
- Removed cache-busting functionality (temporary removal due to major issues; planned reintroduction in a future release)  

## Upcoming: v25.1.0 (April 1, 2025)  
- Advanced Search page  
- Custom Element Properties  
- Multi-select UI functionality  
- Internal messaging  
- Bulk upload capabilities  

---
