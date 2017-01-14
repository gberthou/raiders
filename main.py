import ecs

class MyComponent:
    def __init__(self, t = 0):
        self.t = t

class MySystem(ecs.System):
    @staticmethod
    def update(entityManager, eventManager, dt):
        for entity in entityManager.getEntitiesWithComponent(MyComponent):
            entity.component(MyComponent).t += dt
            print("New t:", entity.component(MyComponent).t)

entityManager = ecs.EntityManager()
eventManager  = ecs.EventManager()
app = ecs.ECSApp(entityManager, eventManager)

app.addSystem(MySystem)

myEntityWithComp    = entityManager.createEntity()
myEntityWithoutComp = entityManager.createEntity()

myEntityWithComp.addComponent(MyComponent(0))

for i in range(10):
    app.updateAll(28)
