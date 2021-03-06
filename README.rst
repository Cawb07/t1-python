TerminalOne-Python
==================

.. image:: https://img.shields.io/pypi/v/TerminalOne.svg
    :target: https://pypi.python.org/pypi/TerminalOne

.. image:: https://img.shields.io/travis/MediaMath/t1-python.svg
    :target: https://travis-ci.org/MediaMath/t1-python

.. image:: https://img.shields.io/pypi/dm/TerminalOne.svg
    :target: https://pypi.python.org/pypi/TerminalOne

Python library for MediaMath's APIs. This library consists of
classes for working with T1 APIs and managing entities. It is written
for Python 2.7 and >=3.3. Compatibility with Python 3 is made possible
by bundling the module `six <https://pypi.python.org/pypi/six>`__.

API Documentation is availble at
`https://developer.mediamath.com/docs/TerminalOne_API_Overview <https://developer.mediamath.com/docs/TerminalOne_API_Overview>`__.

Table of Contents
-----------------

-  `Installation <#installation>`__
-  `Usage <#usage>`__

   -  `Service Object <#service-object>`__
   -  `Fetching Entities and
      Collections <#fetching-entities-and-collections>`__

      -  `Collections <#collections>`__
      -  `Searching for entities <#searching-for-entities>`__
      -  `Entities <#entities>`__
      -  `Child Entities <#child-entities>`__
      -  `Reports <#reports>`__
      -  `Appendix <#appendix>`__

-  `Contact <#contact>`__
-  `Copyright <#copyright>`__

Installation
------------

Installation is simple with pip in a virtual environment:

.. code:: bash

    $ pip install TerminalOne

Alternatively, download the latest tag of the
repository as a tarball or zip file and run:

.. code:: bash

    $ python setup.py install

Usage
-----

Service Object
~~~~~~~~~~~~~~

*class* ``terminalone.T1``\ (*username*\ =\ ``None``,
*password*\ =\ ``None``, *api\_key*\ =\ ``None``,
*auth\_method*\ =\ ``None``, *session\_id*\ =\ ``None``,
*environment*\ =\ ``"production"``, *api\_base*\ =\ ``None``)

The starting point for this package. Authentication and session, entity
retrieval, creation, etc. are handled here. Parameters:

-  *username*: Username of a valid T1 user (that is, valid at
   `https://t1.mediamath.com <https://t1.mediamath.com>`__).
-  *password*: Password for corresponding T1 user
-  *api\_key*: Approved API key generated at `MediaMath's Developer
   Portal <https://developer.mediamath.com>`__.
-  *session\_id*: For applications receiving a session ID instead of
   user credentials, such as an app in T1's Apps tab. *api\_key* should
   still be provided.
-  *auth\_method*: string enum corresponding to which method of
   authentication the session to use. Currently only "cookie" is
   supported.
-  Either *environment* or *api\_base* can be provided to specify where
   the request goes.

.. code:: python

    >>> import terminalone
    >>> t1 = terminalone.T1("myusername", "mypassword", "my_api_key", auth_method="cookie")

Using ``auth_method`` authenticates upon instantiation. Authentication
can also be done separately by calling the ``authenticate`` method with
the same acceptable arguments as the keyword:

.. code:: python

    >>> t1 = terminalone.T1("myusername", "mypassword", "my_api_key")
    >>> t1.authenticate("cookie")

If you have a specific API base (for instance, if you are testing
against a sandbox deployment) (*Note*: sandbox environments are not yet
useable), you can use the ``api_base`` keyword. For production
endpoints, neither ``environment`` nor ``api_base`` should be provided:

.. code:: python

    >>> t1 = terminalone.T1("myusername", "mypassword", "my_api_key", api_base="myqaserver.domain.com", auth_method="cookie")

If you are receiving a (cloned) session ID, for instance the norm for
apps, you will not have user credentials to log in with. Instead,
provide the session ID and API key:

.. code:: python

    >>> t1 = terminalone.T1(session_id="13ea5a26e77b64e7361c7ef84910c18a8d952cf0", api_key="my_api_key")

Fetching Entities and Collections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Entity and collection retrieval. Parameters:

``T1.get``\ (*collection*, *entity*\ =\ ``None``, *child*\ =\ ``None``,
*limit*\ =\ ``None``, *include*\ =\ ``None``, *full*\ =\ ``None``,
*page\_limit*\ =\ ``100``, *page\_offset*\ =\ ``0``,
*sort\_by*\ =\ ``"id"``, *get\_all*\ =\ ``False``, *parent*\ \ ``None``,
*query*\ =\ ``None``, *count*\ =\ ``False``)

-  *collection*: T1 collection, e.g. ``"advertisers"``
-  *entity*: Integer ID of entity being retrieved from T1
-  *child*: Child object of a particular entity, e.g. ``"dma"``,
   ``"acl"``
-  *limit*: dict to query for relation entity, e.g.
   ``{"advertiser": 123456}``
-  *include*: str/list of relations:

   -  string, e.g.

      -  ``T1.get('advertiser', include='agency')``

   -  list of *lateral* (non-hierarchical) relations, e.g.

      -  ``T1.get('advertiser', include=['agency', 'ad_server'])``

   -  list of list/strings of *hierarchical* relations, e.g.

      -  ``T1.get('advertiser', include=[['agency', 'organization'],]``
      -  ``T1.get('advertiser', include=[['agency', 'organization'], 'ad_server']``

-  *full*: When retrieving multiple entities, specifies which types to
   return the full record for. e.g.

   -  ``"campaign"`` (full record for campaign entities returned)
   -  ``True`` (full record of all entities returned),
   -  ``["campaign", "advertiser"]`` (full record for campaigns and
      advertisers returned)

-  *page\_limit* and *page\_offset* handle pagination. *page\_limit*
   specifies how many entities to return at a time, default and max of
   100. *page\_offset* specifies which entity to start at for that page.
-  *sort\_by*: sort order. Default ``"id"``. e.g. ``"-id"``, ``"name"``
-  *get\_all*: Whether to retrieve all results for a query or just a
   single page. Mutually exclusive with *page\_limit*/*page\_offset*
-  *parent*: Only return entities with this ``parent_id``. Used for
   ``audience_segments``.
-  *query*: Search parameters. *Note*: it's much simpler to use ``find``
   instead of ``get``, allowing ``find`` to construct the query.
-  *count*: bool return the number of entities as a second parameter

| Raises: ``terminalone.errors.ClientError`` if *page\_limit* > 100,
  ``terminalone.errors.APIError`` on >399 HTTP status code.
| Returns: If single entity is specified, returns a single entity
  object. If multiple entities, generator yielding each entity.

Collections
^^^^^^^^^^^

.. code:: python

    >>> advertisers = t1.get("advertisers")
    >>> for advertiser in advertisers:
    ...     print(advertiser)
    ...
    Advertiser(id=1, name="My Brand Advertiser", _type="advertiser")
    ...

Returns generator over the first 100 advertisers (or fewer if the user
only has access to fewer), ordered ascending by ID. Each entity is the
limited object, containing just ``id``, ``name``, and ``_type``
(``_type`` just signifies the type returned by the API, in this case,
"advertiser").

.. code:: python

    >>> ag_advertisers = t1.get("advertisers",
    ...                         limit={"agency": 123456},
    ...                         include="agency",
    ...                         full="advertiser")
    >>> for advertiser in ag_advertisers:
    ...     print(advertiser)
    ...
    Advertiser(id=1, name="My Brand Advertiser", agency=Agency(id=123456, name="Operating Agency", _type="agency"), agency_id=123456, status=True, ...)
    ...

Generator over up to 100 advertisers within agency ID 123456. Each
advertiser includes its parent agency object as an attribute. The
advertiser objects are the full entities, so all fields are returned.
Agency objects are limited and have the same fields as advertisers in
the previous example.

.. code:: python

    >>> campaigns, count = t1.get("campaigns",
    ...                           get_all=True,
    ...                           full=True,
    ...                           sort_by="-updated_on")
    >>> print(count)
    539
    >>> for campaign in campaigns:
    ...     print(campaign)
    Campaign(id=123, name="Summer Acquisition", updated_on=datetime.datetime(2015, 4, 4, 0, 15, 0, 0), ...)
    Campaign(id=456, name="Spring Acquisition", updated_on=datetime.datetime(2015, 4, 4, 0, 10, 0, 0), ...)
    ...

Generator over every campaign accessible by the user, sorted in
descending order of last update. Second argument is integer number of
campaigns retrieved, as returned by the API. ``get_all=True`` removes
the need to worry about pagination — it is handled by the SDK
internally.

.. code:: python

    >>> _, count = t1.get("advertisers",
    ...                   page_limit=1,
    ...                   count=True)
    >>> print(count)
    23

Sole purpose is to get the count of advertisers accessible by the user.
Use ``page_limit=1`` to minimize unnecessary resources, and assign to
``_`` to throw away the single entity retrieved.

Searching for entities
^^^^^^^^^^^^^^^^^^^^^^

Limiting entities by relation ID is one way to limit entities, but we
can also search with more intricate queries using ``find``:

``T1.find``\ (*collection*, *variable*, *operator*, *candidates*,
\*\*\ *kwargs*)

-  *collection*: T1 collection, same use as with ``get``
-  *variable*: Field to query for, e.g. ``name``
-  *operator*: Arithmetic operator, e.g. ``"<"``
-  *candidates*: Query value, e.g. ``"jonsmith*"``
-  *kwargs*: Additional keyword arguments to pass onto ``get``. All
   keyword arguments applicable for ``get`` are applicable here as well.

*module* ``terminalone.filters``

-  ``IN``
-  ``NULL``
-  ``NOT_NULL``
-  ``EQUALS``
-  ``NOT_EQUALS``
-  ``GREATER``
-  ``GREATER_OR_EQUAL``
-  ``LESS``
-  ``LESS_OR_EQUAL``
-  ``CASE_INS_STRING``

.. code:: python

    >>> greens = t1.find("atomic_creatives",
    ...                  "name",
    ...                  terminalone.filters.CASE_INS_STRING,
    ...                  "*Green*",
    ...                  include="concept",
    ...                  get_all=True)

Generator over all creatives with "Green" in the name. Include concept.

.. code:: python

    >>> my_campaigns = t1.find("campaigns",
    ...                       "id",
    ...                       terminalone.filers.IN,
    ...                       [123, 234, 345],
    ...                       full=True)

Generator over campaign IDs 123, 234, and 345. Note that when using
``terminalone.filers.IN``, *variable* is automatically ID, so that
argument is effectively ignored. Further, *candidates* must be a list of
integer IDs.

.. code:: python

    >>> pixels = t1.find("pixel_bundles",
    ...                  "keywords",
    ...                  terminalone.filters.NOT_NULL,
    ...                  None)

Generator over first 100 pixels with non-null keywords field.

.. code:: python

    >>> strats = t1.find("strategies",
    ...                  "status",
    ...                  terminalone.filters.EQUALS,
    ...                  True,
    ...                  limit={"campaign": 123456})

Active strategies within campaign ID 123456.

Entities
^^^^^^^^

A specific entity can be retrieved by using ``get`` with an entity ID as
the second argument, or using the ``entity`` keyword. You can then
access that entity's properties using instance attributes:

.. code:: python

    >>> my_advertiser = t1.get("advertisers", 111111)
    >>> my_advertiser.id
    111111

*class* ``terminalone.Entity``

-  ``set(properties)``
   Set all data in mapping object ``properties`` to the entity.
-  ``save(data=None)``
   Save the entity. If ``data`` is provided, send that. Typically used
   with no arguments.
-  ``properties``
   Dictionary of entity properties

(*Note: you will typically interact with subclasses, not ``Entity``
itself*)

If for some reason you need to access the object like a dictionary (for
instance, if you need to iterate over fields or dump to a CSV), the dict
``properties`` is available. However, you shouldn't modify
``properties`` directly, as it bypasses validation.

Once you have your instance, you can modify its values, and then save it
back. A return value of ``None`` indicates success. Otherwise, an error
is raised.

.. code:: python

    >>> my_advertiser.name = "Updated name"
    >>> my_advertiser.save()
    >>>

Create new entities by calling ``T1.new`` on your instance.

``T1.new``\ (*collection*, *report=None*, *properties=None*)

-  *collection*: T1 collection, same as above
-  *report*: New report object; discussed in `Reports <#reports>`__
-  *properties*: Properties to pass into new object.

.. code:: python

    >>> new_properties = {
    ...     "name": "Spring Green",
    ...     "status": True,
    ... }
    >>> new_concept = t1.new("concept", properties=new_properties)
    >>> new_concept.advertiser_id = 123456
    >>> new_concept.save()
    >>>

``properties`` is an optional mapping object with properties to get
passed in. You can use a string representation of the object (such as
``"concept"`` above); or, you can use the object itself from
``terminalone.models``:

.. code:: python

    >>> new_concept = t1.new(terminalone.models.Concept, properties=new_properties)
    >>> 

Child Entities
^^^^^^^^^^^^^^

To retrieve child entities (for instance, ``/users/:id/permissions``), include
the ``child`` argument in a call to ``T1.get``:

.. code:: python

    >>> permissions = t1.get("users", 1, child="permissions")


Reports
~~~~~~~

To use MediaMath's `Reports
API <https://developer.mediamath.com/docs/read/reports_api>`__,
instantiate an instance with ``T1.new``:

.. code:: python

    >>> rpts = t1.new("report")

*class* ``terminalone.Report``

-  ``metadata``
   Metadata of reports available or of individual report. Calculated on
   first call (API request made); cached for future calls.
-  ``parameters``
   Dictionary of request parameters
-  ``set(data)``
   Set request parameters with a mapping object ``data``
-  ``report_uri(report)``
   Get URI stub for report
-  ``get(as_dict=False)``
   Get report data (requires calling ``T1.new`` with a report name).
   Returns headers and ``csv.reader``. If ``as_dict`` is True, returns
   data as ``csv.DictReader``

This is a metadata object, and can be used to retrieve information about
which reports are available.

.. code:: python

    >>> pprint.pprint(rpts.metadata)
    {'reports': {...
                 'geo': {'Description': 'Standard Geo Report',
                         'Name': 'Geo Report',
                         'URI_Data': 'https://api.mediamath.com/reporting/v1/std/geo',
                         'URI_Meta': 'https://api.mediamath.com/reporting/v1/std/geo/meta'},
    ...}
    >>> pprint.pprint(rpts.metadata, depth=2)
    {'reports': {'audience_index': {...},
                 'audience_index_pixel': {...},
                 'day_part': {...},
                 'device_technology': {...},
                 'geo': {...},
                 'performance': {...},
                 'pulse': {...},
                 'reach_frequency': {...},
                 'site_transparency': {...},
                 'technology': {...},
                 'video': {...},
                 'watermark': {...}}}

You can retrieve the URI stub of any report by calling
``Report.report_uri``:

.. code:: python

    >>> print(rpts.get_uri("geo"))
    'geo'

Which is just a short-cut to getting the final part of the path of
``Report.metadata[report]['URI_Data']``. Getting the URI from the
specification is preferred to assuming that the name is the same as the
stub. This is more directly applicable by instantiating the object for
it:

.. code:: python

    >>> report = t1.new("report", rpts.report_uri("performance"))

You can access metadata about this report from the ``Report.metadata``
property as well. To get data, first set properties about the query with
``Report.set``, and use the ``Report.get`` method, which returns a tuple
``(headers, data)``.:

.. code:: python

    >>> report.set({
    ...     'dimensions': ['campaign_id', 'strategy_name'],
    ...     'filter': {'campaign_id': 126173},
    ...     'metrics': ['impressions', 'total_spend'],
    ...     'time_rollup': 'by_day',
    ...     'start_date': '2013-01-01',
    ...     'end_date': '2013-12-31',
    ...     'order': ['date'],
    ... })
    >>> headers, data = report.get()
    >>> print(headers)
    ['start_date', 'end_date', 'campaign_id', 'strategy_name', 'impressions']
    >>> for line in data:
    ...     # do work on line
    ...     print(line)
    ...
    ['2013-06-27', '2013-06-27', '126173', 'PS', '231']
    ...

``headers`` is a list of headers, while ``data`` is a ``csv.reader``
object. Type casting is not present in the current version, but is
tentatively planned for a future date.

More information about these parameters can be found
`here <https://developer.mediamath.com/docs/read/reports_api/Data_Retrieval>`__.

Appendix
^^^^^^^^

Why don't we import the object classes directly? For instance, why
doesn't this work?

.. code:: python

    >>> from terminalone import Campaign

The answer here is that we need to keep a common session so that we can
share session information across requests. This allows you to work with
many objects, only passing in authentication information once.

.. code:: python

    >>> t1 = T1("myusername", "mypassword", "my_api_key")
    >>> t1.authenticate("cookie")
    >>> c = t1.new("campaign")
    >>> c.session is t1.session
    True

Contact
-------

For questions about either API workflow or this library, email
`developers@mediamath.com <mailto:developers@mediamath.com>`__.

Copyright
---------

Copyright MediaMath 2015-2016. All rights reserved.
