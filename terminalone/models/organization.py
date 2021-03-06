# -*- coding: utf-8 -*-
"""Provides agency object."""

from __future__ import absolute_import
from ..entity import Entity


class Organization(Entity):
    """Organization entity."""
    collection = 'organizations'
    resource = 'organization'
    _relations = {
        'currency',
        'seats',
    }
    _dmp_settings = Entity._enum({'disabled', 'enabled'}, 'disabled')
    _org_types = Entity._enum({'buyer', 'partner'}, 'buyer')
    _pull = {
        'address_1': None,
        'address_2': None,
        'adx_seat_account_id': int,
        'allow_byo_price': Entity._int_to_bool,
        'allow_x_agency_pixels': Entity._int_to_bool,
        'billing_country_code': None,
        'city': None,
        'contact_name': None,
        'country': None,
        'created_on': Entity._strpt,
        'curency_code': None,
        'dmp_enabled': None,
        'id': int,
        'mm_contact_name': None,
        'name': None,
        'org_type': None,
        'override_suspicious_traffic_filter': Entity._int_to_bool,
        'phone': None,
        'state': None,
        'status': Entity._int_to_bool,
        'suspicious_traffic_filter_level': int,
        'tag_ruleset': None,
        'updated_on': Entity._strpt,
        'use_evidon_optout': Entity._int_to_bool,
        'version': int,
        'zip': None,
    }
    _push = _pull.copy()
    _push.update({
        'allow_byo_price': int,
        'allow_x_agency_pixels': int,
        'dmp_enabled': _dmp_settings,
        'org_type': _org_types,
        'override_suspicious_traffic_filter': int,
        'status': int,
        'use_evidon_optout': int,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(Organization, self).__init__(session, properties, **kwargs)
