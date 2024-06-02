import gettext as __gettext
import os as __os

__gettext.bindtextdomain(
    "messages", __os.path.join(__os.path.dirname(__file__), "locale")
)
_ = __gettext.gettext
