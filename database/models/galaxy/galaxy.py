from database.database import db
from database.models.galaxy.planet.planet import Planet


class Galaxy(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    planets_occupied = db.Column(db.Integer, nullable=False, default=0)

    planets = db.relationship('Planet', backref='Galaxy', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for i in range(8):
            self.planets.append(Planet(position=i + 1))

        print('Galaxy created: {}, {}'.format(self.x, self.y))

    @property
    def sku(self):
        return ':'.join(map(str, (self.x, self.y)))

    def __repr__(self):
        return '<Galaxy {}, {}>'.format(self.id, self.name)
