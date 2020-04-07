MASCULINO = 1
FEMENINO = 2

GENERO_TYPES = ((MASCULINO, 'Masculino'),(FEMENINO, 'Femenino'),)
genero = models.PositiveSmallIntegerField(choices=GENERO_TYPES)