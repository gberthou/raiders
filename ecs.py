class Entity:
    def __init__(self):
        self.components = {}

    def addComponent(self, component):
        self.components[type(component)] = component

    def removeComponent(self, componentType):
        try:
            del self.components[componentType]
        except KeyError:
            pass

    def component(self, componentType):
        return self.components[componentType]

    def hasComponent(self, componentType):
        return componentType in self.components.keys()

class System:
    def update(self, entityManager, eventManager, dt):
        pass

class EntityManager:
    def __init__(self):
        self.entities = []
        self.systems = []

    def createEntity(self):
        entity = Entity()
        self.entities.append(entity)
        return entity

    def removeEntity(self, entity):
        self.entities.remove(entity)

    def getEntitiesWithComponents(self, componentTypes):
        return [e for e in self.entities if [c for c in componentTypes if e.hasComponent(c)] == componentTypes]

class EventManager:
    pass

class Component:
    pass

class ECSApp:
    def __init__(self, entityManager, eventManager):
        self.systems = {}
        self.entityManager = entityManager
        self.eventManager = eventManager

    def addSystem(self, system):
        self.systems[type(system)] = system

    def updateSystem(self, systemType, dt):
        try:
            system = self.systems[systemType]
        except KeyError:
            pass
        else:
            system.update(self.entityManager, self.eventManager, dt)

    def updateAll(self, dt):
        for systemType in self.systems.keys():
            self.updateSystem(systemType, dt)

