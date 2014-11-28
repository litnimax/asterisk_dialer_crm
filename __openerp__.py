{
    'name' : 'Asterisk Dialer CRM',
    'description': 'CRM Addon for Dialer app',
    'version' : '1.0',
    'depends' : ['asterisk_dialer', 'crm'],
    'author' : 'litnimax',
    'website' : '',
    'category' : 'Asterisk',
    'data' : [
        'security/ir.model.access.csv',        
        'dialer_crm_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
