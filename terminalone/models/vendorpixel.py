# -*- coding: utf-8 -*-
"""Provides vendor_pixel object."""

from __future__ import absolute_import
from ..entity import Entity


class VendorPixel(Entity):
    """Provides vendor pixel entity."""
    collection = 'vendor_pixels'
    resource = 'vendor_pixel'
    _relations = {
        'creative',
        'vendor_pixel_domains',
    }
    _set_bys = Entity._enum({'SYSTEM', 'USER'}, 'USER')
    _pull = {
        'created_on': Entity._strpt,
        'creative_id': int,
        'id': int,
        'set_by': None,
        'tag': None,
        'tag_type': None,
        'updated_on': Entity._strpt,
        'version': int,
    }
    _push = _pull.copy()
    _push.update({
        'set_by': _set_bys,
    })

    def __init__(self, session, properties=None, **kwargs):
        super(VendorPixel, self).__init__(session, properties, **kwargs)
