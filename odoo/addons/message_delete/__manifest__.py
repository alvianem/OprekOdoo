# -*- coding: utf-8 -*-
{
    "name": "Message Delete",
    "version": "10.0.1.0.1",
    "category": "Discuss",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/10.0/message-delete-23",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/templates.xml"
    ],
    "qweb": [
        "static/src/xml/message_delete.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to let Odoo administrators delete messages from threads and channels",
    "description": """
    The app goal is to let admins (superuser only) to remove messages. In other cases a warning appears.

    For message/notes editing use the tool <a href='https://apps.odoo.com/apps/modules/10.0/message_edit/'>Message / Note Editing</a>
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "0.0",
    "currency": "EUR",
}