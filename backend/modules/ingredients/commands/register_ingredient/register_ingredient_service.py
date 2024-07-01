from shared.utils.service_result import ServiceResult
from modules.ingredients.schemas.dtos import RegisterIngredient
from modules.ingredients.repositories.ingredient_repository import IngredientRepository

class RegisterIngredientService:
    # def __init__(self, db: Database):
    #     self.db = db
    
    def __init__(self):
        self.repository = IngredientRepository()
    
    async def register_ingredient(self, ingredient: RegisterIngredient) -> ServiceResult:
        self.repository.register_ingredient()
        return ServiceResult(ingredient)
        