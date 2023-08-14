import imgkit
import os
from common.constant import WKHTMLTOIMAMGE_PATH

# imgkit.config()
imgkit.from_url('http://google.com', os.path.join(os.getcwd(),'static','out.jpg'))