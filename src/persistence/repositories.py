import logging
from .generic import Repository
from typing import Optional
from .models import Dummy


logger = logging.getLogger(__name__)


class DummyRepository(Repository[Dummy]):
    pass

