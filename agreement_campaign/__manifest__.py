# -*- coding: utf-8 -*-
{
    "name": "Agreement Funding",
    "version": "16.0.1.0.0",
    "summary": "Integrate agreement module with funding campaign",
    "author": "Som IT Cooperatiu SCCL, Odoo Community Association (OCA)",
    "website": "https://somit.coop",
    "category": "Agreement",
    "depends": [
        "agreement_legal",
        "funding_campaign",
    ],
    "data": [
        "views/funding_campaign_views.xml",
        "views/agreement_views.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
}
