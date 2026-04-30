{
    'name': 'RFQ Multi-Vendor Bidding',
    'version': '19.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Extend RFQ with multi-vendor bidding and purchase requests',
    'description': """
        Adds multi-vendor bidding capabilities to the Purchases module:
        - Send RFQs to multiple vendors simultaneously
        - Collect and compare vendor bids
        - Select a winning bid
        - Generate purchase orders from winning bids
        - Purchase request workflow
    """,
    'author': 'Josh',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['purchase', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/purchase_request_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_bid_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
