###################################################
TOTPaaS: Time-based One-Time Passwords as a Service
###################################################

Please don't actually use this.

Deployed at https://totpaas.herokuapp.com/


Setup
=====

You'll need to provide the ``TOTP_PARAMS`` environment variable [#]_.

Example value::

    {
        "ayy": {
            "digest": "sha1",
            "digits": 6,
            "key": "lmao",
            "time_step": 30
        }
    }

Afterward, run ``poetry shell``, then ``make`` [#]_.

----

.. [#] Consider using [direnv](https://direnv.net/) for this purpose.
.. [#] Remember not to actually do any of this.
