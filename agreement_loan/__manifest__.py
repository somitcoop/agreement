# -*- coding: utf-8 -*-
{
    "name": "Agreement_loan",
    "version": "",
    "summary": """ Agreement_loan Summary """,
    "author": "",
    "website": "",
    "category": "",
    "depends": [
        "account_loan",
        "agreement_campaign",
        "agreement_legal",
        "agreement",
    ],
    "data": [
        "data/agreement_type_data.xml",
        "data/mail_template_data_xml_views.xml",
        "views/res_config_settings_views.xml",
        "views/account_loan_views.xml",
        "views/res_company_views.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
