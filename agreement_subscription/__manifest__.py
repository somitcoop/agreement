{
    "name": "Agreement Subscription",
    "version": "16.0.1.0.0",
    "category": "Agreement",
    "author": "Nicolas Ramos",
    "summary": "Integrate agreement module with cooperator subscriptions",
    "website": "https://nicolasramos.es",
    "license": "AGPL-3",
    "depends": [
        "agreement_legal",
        "cooperator",
    ],
    "data": [
        "data/agreement_type_data.xml",
        "views/subscription_request_views.xml",
        "views/res_company_views.xml",
        "data/mail_template.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
