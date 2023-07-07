class EntityRelation:
    def __init__(self, entity: str):
        self.entity = entity
        self.count = 1


class ReportEntityRelations:
    def __init__(self, root_entity: str):
        self.root_entity = root_entity
        self.relations: list[EntityRelation] = []

    def check_entity_in_relations(self, entity: str) -> EntityRelation | None:
        found = None

        for r in self.relations:
            if r.entity == entity:
                found = r
                break

        return found

