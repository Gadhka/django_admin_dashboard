---

# Custom Django Admin Dashboard

## Overview

This custom admin dashboard was created to address common challenges in managing related models within a Django application. The goal is to simplify the management of posts and their associated models while providing flexibility for additional functionalities.

## Features

- **Dynamic Related Models**: Easily define related models for your main models using a simple dictionary structure. For example, when defining a post, you can specify related models such as `PostImage`, `Comments`, and others.

```python
from django_admin_dashboard.site import admin_site

registered_model = {
    "PostTitle": {
        "action": "slug",
        "related": [
            "Post",
            "post_images",
            "section_what_i_looking_for",
            "Comments",
            "SinglePagePost",
            "FAQS"
        ]
    },
    "home_visitors": {"related": []},
    "category": {"related": ["single_category", "CategoriesMetaTags"]},
    "Golobal_adam_reviews": {"related": ["SocialMedia", "HomePageMetaTags"]},
    "home_page_best_categories": {"related": []},
    "UserTheirEmails": {"related": []},
    "ServiceModel": {"related": ["CommentsService", "ServicesImages", "ServicesMetaTags"]},
    "RobotsTxt": {"related": []},
    "Contact": {"related": ["ContactImage", "ContactMetaDescription"]},
    "CreatePortfolio": {"related": []},
}

admin_site.RegisterModel(registered_model)
```

- **Action Management**: Define actions such as "slug" to manage relationships effectively. When an action is specified, ensure that all related models have the required foreign key relationships. This allows you to create complex queries more intuitively.

- **Preview Functionality**: If desired, you can add a preview feature that allows you to review posts without publishing them. This helps ensure that all content is ready before going live.

- **Flexible Registration**: The dashboard can be easily updated. You have the flexibility to change or remove models and their relationships as needed.

## Usage Guidelines

- **Defining Models**: When registering models, ensure that if you're using an action (like "slug"), all related models must have the necessary foreign key relationships and etc. This promotes consistency and integrity in your data.

- **Related Models Without Actions**: If you're only using related models and not actions, you won't need to define foreign keys in associated models.

- **Updating the Dashboard**: Feel free to modify any part of this dashboard to suit your needs. The goal is to make it flexible and adaptable to your project's evolving requirements.

## Conclusion

This custom Django admin dashboard is designed to streamline the management of related models, enhancing your development workflow. You can expand and upgrade it as needed, ensuring it meets your unique needs. 

For any questions or contributions, feel free to reach out!

---
