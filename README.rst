###################################################
TOTPaaS: Time-based One-Time Passwords as a Service
###################################################

Please don't actually use this.

Deployed at https://totpaas.herokuapp.com/


Setup
=====

You'll need to provide the ``TOTP_PARAMS`` environment variable [1]_.

.. [1] Consider using [direnv](https://direnv.net/) for this purpose.

Example value::

    {
        "ayy": {
            "digest": "sha1",
            "digits": 6,
            "key": "lmao",
            "time_step": 30
        }
    }

Afterward, run ``poetry shell``, then ``make`` [2]_.

.. [2] Remember not to actually do any of this.
