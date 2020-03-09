from app import db

class Games(db.Model):
    __tablename__ = 'games'
    permalink = db.Column(db.String,primary_key = True)
    title = db.Column(db.String)
    price = db.Column(db.Integer)
    image = db.Column(db.String)
    url = db.Column(db.String)
    description = db.Column(db.String)

    prices = db.relationship('Price')

    def __repr__(self):
        return '''
            permalink:{},
            title:{},
            price:{},
            image:{},
            url:{},
            description:{}
        '''.format(
            self.permalink,
            self.title,
            self.price,
            self.image,
            self.url,
            self.description
            )