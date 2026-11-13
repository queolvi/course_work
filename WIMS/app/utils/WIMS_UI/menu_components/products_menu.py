from pydantic import ValidationError

from app.utils.WIMS_UI.menu_components.base_menu import BaseMenu
from app.repositories import ProductRepository
from app.schemas import ProductCreate
from app.utils.console_print import print_menu, print_table, input_int, input_str


class ProductsMenu(BaseMenu):
    def run(self):
        repo = ProductRepository()
        while True:
            self._clear()
            print_menu([
                "View all products",
                "Create new product",
                "Delete product",
            ], "Products Management")

            choice = input_int("Choose option: ", min_val=0, max_val=3)
            if choice == 0:
                return

            if choice == 1:
                self._view_products(repo)
            elif choice == 2:
                self._create_product(repo)
            elif choice == 3:
                self._delete_product(repo)

            self._pause()

    def _view_products(self, repo: ProductRepository):
        products = repo.get_all()
        if products:
            rows = [[p.product_id, p.name, p.stock_keeping_unit, p.unit, p.category_id] for p in products]
            print_table(["ID", "Name", "SKU", "Unit", "Cat.ID"], rows)
        else:
            print("\n  No products found.")

    def _create_product(self, repo: ProductRepository):
        try:
            data = {
                "name": input_str("Name: "),
                "stock_keeping_unit": input_str("SKU: "),
                "category_id": input_int("Category ID: ", min_val=1),
                "unit": input_str("Unit (pcs/kg/l): "),
                "description": input_str("Description (optional): ", allow_empty=True) or None,
                "min_stock": input_int("Min stock: ", min_val=0),
            }
            product_data = ProductCreate(**data)
            pid = repo.create(
                name=product_data.name,
                sku=product_data.stock_keeping_unit,
                category_id=product_data.category_id,
                unit=product_data.unit,
                description=product_data.description,
                min_stock=product_data.min_stock,
            )
            print(f"\nProduct created with id={pid}")
        except ValidationError as e:
            self._print_validation_error(e)
        except Exception as e:
            print(f"\n{e}")

    def _delete_product(self, repo: ProductRepository):
        pid = input_int("Product ID to delete: ", min_val=1)
        if repo.delete(pid):
            print("Product deleted")
        else:
            print("Cannot delete (has batches or not found)")