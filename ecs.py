class Entity:
    def __init__(self):
        self.components = {}

    def addComponent(self, component):
        self.components[type(component).__name__] = component

    def removeComponent(self, componentType):
        try:
            del self.components[componentType.__name__]
        except:
            pass

    def component(self, componentType):
        return self.components[componentType.__name__]
    
    def hasComponent(self, componentType):
        return componentType.__name__ in self.components.keys()

class System:
    @staticmethod
    def update(entityManager, eventManager, dt):
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
    def __init__(self):
        pass

class Component:
    def __init__(self):
        pass

class ECSApp:
    def __init__(self, entityManager, eventManager):
        self.systems = []
        self.entityManager = entityManager
        self.eventManager = eventManager

    def addSystem(self, systemType):
        self.systems.append(systemType)

    def updateSystem(self, systemType, dt):
        if systemType in self.systems:
            systemType.update(self.entityManager, self.eventManager, dt)

    def updateAll(self, dt):
        for system in self.systems:
            self.updateSystem(system, dt)

