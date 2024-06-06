import gettext as __gettext
import os as __os

__gettext.bindtextdomain("messages", __os.path.dirname(__file__))
_ = __gettext.gettext
