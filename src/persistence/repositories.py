import logging
from .generic import Repository
from typing import Optional
from .models import *

logger = logging.getLogger(__name__)


class DummyRepository(Repository[Dummy]):
    pass


class NakamotoCoefficientRepository(Repository[NakamotoCoefficient]):
    pass


class BitcoinNakamotoCoefficientRepository(Repository[BitcoinNakamotoCoefficient]):
    pass

