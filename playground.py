import datetime

from src.persistence.repositories import *

#print(Dummy.query.all())
print(DummyRepository.read_first())


