from abc import ABC, abstractmethod

# Implementation of observers using Observer Pattern
class Observer(ABC):
	@abstractmethod
	def update(self, subject):
		pass

class Subject:
	def __init__(self):
		self._observers = []

	def attach(self, observer: Observer):
		if observer not in self._observers:
			self._observers.append(observer)

	def detach(self, observer: Observer):
		try:
			self._observers.remove(observer)
		except ValueError:
			pass

	def notify(self):
		for observer in self._observers:
			observer.update(self)
