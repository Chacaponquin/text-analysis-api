class EntityServices:
    def find_entities(self):
        entities = ['Entidad 0', 'Entidad 1', 'Entidad 3']
        return [{'entity': e} for e in entities]