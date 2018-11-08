__author__ = "cotehidalgov"

#Herencia
# -*- coding: utf-8 -*-

from random import randint, choice
from abc import ABCMeta, abstractmethod


class Plate:
	def __init__(self, food, drink):
		self.food = food
		self.drink = drink


class Food(metaclass=ABCMeta):
	def __init__(self, ingredients):
		self.ingredientes = ingredients
		self.calidad = randint(50,200)
		self.tiempo = 0

	def check_time(self): 
		if self.tiempo >= 30:
			self.calidad -=30

	@abstractmethod
	def check_ingredients(self):
		pass


class Drink(metaclass=ABCMeta):
	def __init__(self):
		self.calidad = randint(50,150)


class Personality(metaclass=ABCMeta):
	def react(self, calidad):
		if calidad >= 100:
			self.im_happy()
		else: self.im_mad()

	@abstractmethod
	def im_happy(self):
		pass

	@abstractmethod
	def im_mad(self):
		pass


class Person: # Solo los clientes tienen personalidad en esta actividad
	def __init__(self, name):
		self.name = name


class Restaurant:
	def __init__(self, chefs, clients):
		self.chefs = chefs
		self.clients = clients

	def start(self):
		for i in range(3): # Se hace el estudio por 3 dias
			print("----- Día {} -----".format(i + 1))
			plates = []
			for chef in self.chefs: 
				for j in range(3):  # Cada chef cocina 3 platos
					plates.append(chef.cook()) # Retorna platos de comida y bebida

			for client in self.clients:
				for plate in plates:
					client.eat(plate)


class Pizza(Food):
	def __init__(self, ing1, ing2, ing3):
		super().__init__(["Salsa de tomate", "Queso", ing1, ing2, ing3])
		self.tiempo = randint(20,100)
		self.check_time()
		self.check_ingredients()

	def check_ingredients(self):
		for i in self.ingredientes:
			if i == "Pepperoni":
				self.calidad += 50
			elif i == "Pinia":
				self.calidad -= 50


class Ensalada(Food):
	def __init__(self, ing1, ing2):
		super().__init__(["Lechuga", ing1, ing2])
		self.tiempo = randint(5,60)
		self.check_time()
		self.check_ingredients()

	def check_ingredients(self):
		for i in self.ingredientes:
			if i == "Crutones":
				self.calidad += 20
			elif i == "Manzana":
				self.calidad -= 20


class Soda(Drink):
	def __init__(self):
		super().__init__()
		self.calidad -= 30


class Jugo(Drink):
	def __init__(self):
		super().__init__()
		self.calidad += 30


class Chef(Person):
	def __init__(self,name):
		super().__init__(name)

	def cook(self):
		ingredientes_pizza = ["Pepperoni", "Pinia", "Cebolla", "Tomate", "Jamon", "Pollo"]
		ingredientes_ensalada = ["Crutones", "Espinaca", "Manzana", "Zanahoria"]
		tipo = randint(0,1)
		if tipo == 0:
			food = Pizza(choice(ingredientes_pizza),choice(ingredientes_pizza),choice(ingredientes_pizza))
		else:
			food = Ensalada(choice(ingredientes_ensalada),choice(ingredientes_ensalada))
		bebestible = randint(0,1)
		if bebestible == 0:
			drink = Soda()
		else: drink = Jugo()
		return Plate(food, drink)


class Client(Person):
	def __init__(self,name, perso):
		super().__init__(name)
		self.perso = perso

	def eat(self, plate):
		calidad_final = (plate.food.calidad + plate.drink.calidad)/2
		self.perso.react(calidad_final)


class Cool(Personality):
	def im_happy(self):
		print("Yumi! Que rico")

	def im_mad(self):
		print("Preguntare si puedo cambiar el plato")


class Hater(Personality):
	def im_mad(self):
		print("Nunca mas volvere a Daddy Juan's")

	def im_happy(self):
		print("No esta malo, pero igual prefiero pizza x2")


if __name__ == '__main__':
	chefs = [Chef("Cote"), Chef("Joaquin"), Chef("Andres")]
	clients = [Client("Bastian", Hater()), Client("Flori", Cool()), 
				Client("Antonio", Hater()), Client("Felipe", Cool())]

	restaurant = Restaurant(chefs, clients)
	restaurant.start()

