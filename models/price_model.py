from app import db

class Price(db.Model):
    __tablename__ = 'price'
    permalink = db.Column(db.String,db.ForeignKey("games.permalink"),primary_key=True)
    date = db.Column(db.DateTime,primary_key=True)
    price = db.Column(db.Integer)

    def __repr__(self):
        return '''
            permalink:'{}',
            date:'{}-{}-{}',
            price:'{}'
        '''.format(
            self.permalink.replace(':',''),
            self.date.year,
            self.date.month,
            self.date.day,
            self.price
            )