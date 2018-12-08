from datetime import datetime

from mongoengine import *

from config import CONFIG

connect(CONFIG['DB_NAME'])


class Author(Document):
    CONTINENT = (
        ('EUR', 'Eurasia'),
        ('AFR', 'Africa'),
        ('NAM', 'North America'),
        ('SAM', 'South America'),
        ('AUS', 'Australia'),
        ('ANT', 'Antarctica'),
    )
    name = StringField(required=True)
    age = IntField(min_value=0, required=True)
    home = StringField(choices=CONTINENT)

    def __str__(self):
        return '<Author {}>'.format(self.name)

    def __repr__(self):
        return self.__str__()


class Comment(EmbeddedDocument):
    text = StringField(required=True)

    def __str__(self):
        return '<Comment "{}">'.format(self.text)

    def __repr__(self):
        return self.__str__()


class Article(Document):
    created_at = DateTimeField(default=datetime.utcnow)
    likes_number = IntField(min_value=0)
    author = ReferenceField(Author)
    text = StringField(required=True)
    comments = ListField(EmbeddedDocumentField(Comment))

    meta = {'indexes': ['$text']}  # index for text searching

    @queryset_manager
    def without_comments(doc_cls, queryset):
        return queryset.filter(__raw__={'comments': {'$size': 0}})

    def __str__(self):
        return '<Article text="{}" author={}>'.format(self.text, self.author)

    def __repr__(self):
        return self.__str__()


Article.objects.delete()
Author.objects.delete()

john = Author(name='John Smith', age=42, home='AUS').save()
peter = Author(name='Peter Alvarez', age=30, home='AFR').save()

Article.objects.insert([
    Article(
        likes_number=45,
        author=john,
        text='Do you know something about co...',
        comments=[Comment(text='Good'), Comment(text='Great')],
    ),
    Article(
        likes_number=126,
        author=john,
        text='Attention! Jython vs IronPython...',
        comments=[
            Comment(text='Amazing'), Comment(text='CPython forever'),
            Comment(text='Oh no'), Comment(text='What a pity'),
            Comment(text='Guido sad that..'),
        ],
    ),
    Article(
        likes_number=66,
        text='English scientists have discovered ...',
        comments=[Comment(text='I dont think so!'), Comment(text='((')],
    ),
    Article(
        likes_number=2,
        author=peter,
        text=(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '
            'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut '
            'enim ad minim veniam, quis nostrud exercitation ullamco laboris '
            'nisi ut aliquip ex ea commodo consequat.'
        ),
    ),
    Article(
        likes_number=114,
        author=peter,
        text='You should take your money and ...',
        comments=[Comment(text='What a pyramid?'), Comment(text=';-)')],
    ),
])


print('Articles count:', Article.objects.count())
print('Authors count:', Author.objects.count())
print('Summary likes count', Article.objects.sum('likes_number'))
print('Author average age', Author.objects.average('age'))

print('John articles:', Article.objects(author=john))
print('Peter articles:', Article.objects(author=peter))
print('Anonymous articles:', Article.objects(author=None))

print(
    'Sorted desc articles by likes number:',
    Article.objects.order_by('-likes_number'),
)
print(
    'Sorted esc articles by likes number:',
    Article.objects.order_by('likes_number'),
)

print('Articles about Jython: ', Article.objects.search_text('Jython'))

article = Article.objects.first()
article.comments.append(Comment(text='Not bad'))
article.save()
print(article.comments)

print('Articles without comments:', Article.without_comments())
