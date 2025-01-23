# -*- coding: utf-8 -*-
{
    "name": "Agreement_sign",
    "version": "16.0.1.0.0",
    "summary": """ Agreement_sign Summary """,
    "author": "",
    "website": "",
    "category": "",
    "depends": [
        "agreement_campaign",
        "agreement_legal",
        "sign_oca",
    ],
    "data": [
        # 'security/ir.model.access.csv',
        "views/agreement_views.xml",
        "data/sign_oca_role.xml",
        "data/sign_oca_template.xml",
        "views/agreement_type_views.xml",
        # "views/agreement_sign_views.xml",
        "views/sign_oca_request_views.xml",
    ],
    "assets": {
        "web.assets_backend": ["agreement_sign/static/src/**/*"],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
