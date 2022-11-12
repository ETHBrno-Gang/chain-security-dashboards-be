from src.persistence.repositories import DummyRepository, Dummy

#print(Dummy.query.all())
print(DummyRepository.read_first())
DummyRepository.create(Dummy(username='gfdg'))
print(DummyRepository.read_first())
