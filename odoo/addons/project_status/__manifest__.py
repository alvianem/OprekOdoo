{
    "name": "Project Information Status",
    "summary": "Add an Information Status to projects",
    "version": "10.0.1.0.0",
    "category": "ASYST - Project",
    "website": "",
    "license": "AGPL-3",
    "depends": [
        "project", "sale", "web_timeline", "hr", "board", "sale_invoice_tag_pass", "sale_crm", "sale_stock"
    ],
    "data": [
        "security/project_security.xml",
        "security/ir.model.access.csv",
        "views/project_view.xml"
    ],
    "installable": True,
}