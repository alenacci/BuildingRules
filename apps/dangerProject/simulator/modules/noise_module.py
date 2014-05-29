from module import Module
from triggers.trigger import Trigger
import random
from renderer import Renderer
import pygame
from commons.point import Point

class NoiseModule(Module):

	#average frequency of noise in the building in one time interval
	NOISE_FREQUENCY = 0.2

	#accuracy of the noise detector sensor
	SENSOR_ACCURACY = 0.8

	#color of the noise circles
	NOISE_COLOR = [100, 100, 100]

	def __init__(self,simulator):
		Module.__init__(self,simulator)
		simulator.trigger_manager.subscribe("noise", self._on_noise)
		self._next_noise_time = None

	def after_populate(self, agents):
		for a in agents:
			a.loud_noise_start_time = None
			a.loud_noise_duration = None
			a.is_generating_noise = False

	def update(self, time):

		def new_noise_time():
			return time + random.random() * (1.0/NoiseModule.NOISE_FREQUENCY)

		if self._next_noise_time is None:
			self._next_noise_time = new_noise_time()

		if self._next_noise_time < time:
			self._next_noise_time = new_noise_time()
			self._generate_noise_trigger(1 + random.random() * 2)

	def _generate_noise_trigger(self, duration):
		trigger = Trigger("noise")
		trigger.intensity = 1 + random.expovariate(0.1)
		trigger.room = self.simulator.building.random_room()
		trigger.position = trigger.room.random_position()
		trigger.duration = duration
		trigger.time = self.simulator.time

		self.simulator.trigger_manager.fire_trigger(trigger)

	def update_agent(self, agent, time):
		if agent.is_generating_noise and \
						agent.loud_noise_start_time + agent.loud_noise_duration < time:
			agent.is_generating_noise = False


	def _on_noise(self, trigger):
		agents_in_room = trigger.room.agents
		agents_nearby = []

		#select the nearby agents according to the distance and a probability
		for a in agents_in_room:
			dis = a.p.dist(trigger.position)
			#the probability to hear the noise
			probability = NoiseModule.SENSOR_ACCURACY - (dis/trigger.intensity)

			if random.random() <= probability:
				a.is_generating_noise = True
				a.loud_noise_start_time = trigger.time
				a.loud_noise_duration = trigger.duration + random.random() * 2



	def render_agent(self, window, agent):
		if agent.is_generating_noise:

			time = self.simulator.time

			"""Draw around the circle of the agent a series of concentric circles"""

			enhance_duration = 0.5

			start_time = agent.loud_noise_start_time
			now = time
			dt = now - start_time

			def draw_circle(progress):
				max_radius = 15

				#The radius will start from the border to the agent to the max radius
				base_radius = Renderer.AGENT_SIZE/2
				radius = base_radius + (max_radius - base_radius) * progress
				center = Point(int(agent.x*Renderer.SIZE_X + Renderer.SIZE_X/2 + 1) + Renderer.OFFSET_X,
							   int(agent.y*Renderer.SIZE_Y + Renderer.SIZE_Y/2 + 1) + Renderer.OFFSET_Y)

				pygame.draw.circle(window, NoiseModule.NOISE_COLOR, center.to_a(), int(radius), 1)

			progress = (dt % enhance_duration) / enhance_duration
			draw_circle(progress)

			#second circle
			if dt > enhance_duration / 2:
				progress2 = progress - 0.5 if progress > 0.5 else 1 - progress + 0.5
				draw_circle(progress2)

