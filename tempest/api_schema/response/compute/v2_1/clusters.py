

list_clusters = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'clusters': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'cluster_ip_netmask': {'type': 'string'},
                        'file_system': {'type': 'string'},
                        'size': {'type': 'string'},
                        'scecondary_public_ip_netmask': {'type': 'string'},
                        'primary_public_ip_netmask': {'type': 'string'},
                        'primary_public_network': {'type': 'string'},
                        'cluster_network': {'type': 'string'},
                        'journal_size': {'type': 'string'},
                        'secondary_public_network': {'type': 'string'}
                    },
                    'required': ['id', 'name', 'cluster_ip_netmask', 'file_system',
                                 'size', 'scecondary_public_ip_netmask', 'primary_public_ip_netmask',
                                 'primary_public_network', 'cluster_network', 'journal_size',
                                 'secondary_public_network']
                }
            }
        },
        'required': ['clusters']
    }
}