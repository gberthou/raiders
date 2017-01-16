import ecs
from sfml import sf

window = sf.RenderWindow(sf.VideoMode(800, 600), "Raiders")
window.vertical_synchronization = True

while window.is_open:
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()

    window.clear(sf.Color(0, 255, 0))
    window.display()

"""

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
    """

