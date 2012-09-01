from django.db import models
import string
#Cria as tabelas no banco de dados

_char_map = [x for x in string.ascii_letters+string.digits]

def index_to_char(sequence):
    return "".join([_char_map[x] for x in sequence])


class Link(models.Model):
    #Armazena a URL digitada
    link = models.URLField()
    hits = models.IntegerField(default=0)

    #Mostra a estatisticas de visita do link e o link
    
    def __repr__(self):
        return "<Link (Hits %s): %s>"%(self.hits, self.link)

    def get_short_id(self):
        _id = self.id
        digits = []
        while _id > 0:
            rem = _id % 62
            digits.append(rem)
            _id /= 62
        digits.reverse()
        return index_to_char(digits)

    @staticmethod
    def decode_id(string):
        i = 0
        for c in string:
            i = i * 62 + _char_map.index(c)
        return i


class HitsDatePoint(models.Model):
    day = models.DateField(auto_now=True, db_index=True)
    hits = models.IntegerField(default=0)
    link = models.ForeignKey(Link)

    class Meta:
        unique_together = (("day", "link"),)
