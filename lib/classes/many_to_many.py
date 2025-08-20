class Article:
    _registry = []

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string with 5–50 characters")
        self._author = author
        self._magazine = magazine
        self._title = title
        Article._registry.append(self)

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    @property
    def title(self):
        return self._title   # immutable (no setter)


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Author name must be a non-empty string")
        self._name = name

    @property
    def name(self):
        return self._name

    def articles(self):
        return [art for art in Article._registry if art.author is self]

    def magazines(self):
        return list({art.magazine for art in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        cats = {mag.category for mag in self.magazines()}
        return list(cats) if cats else None


class Magazine:
    _registry = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine._registry.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str) or not (2 <= len(new_name) <= 16):
            raise ValueError("Magazine name must be 2–16 characters long")
        self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_cat):
        if not isinstance(new_cat, str) or not new_cat.strip():
            raise ValueError("Category must be a non-empty string")
        self._category = new_cat

    def articles(self):
        return [art for art in Article._registry if art.magazine is self]

    def contributors(self):
        return list({art.author for art in self.articles()})

    def article_titles(self):
        titles = [art.title for art in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        authors = [art.author for art in self.articles()]
        return [a for a in set(authors) if authors.count(a) > 2] or None

    @classmethod
    def top_publisher(cls):
        if not cls._registry:
            return None
        return max(cls._registry, key=lambda m: len(m.articles())) \
            if any(m.articles() for m in cls._registry) else None
