import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import font as tkFont

# Font names
FONT_FAMILY = "Figtree"
FALLBACK_FONT_FAMILY = "Figtree"

# Fonts
FONT_HEADING = (FONT_FAMILY, 34, "bold")      
FONT_SUBHEADING = (FONT_FAMILY, 22, "bold")   
FONT_BUTTON = (FONT_FAMILY, 18)             
FONT_LABEL = (FONT_FAMILY, 18)              
FONT_ENTRY = (FALLBACK_FONT_FAMILY, 16)     
FONT_TREEVIEW_HEADER = (FONT_FAMILY, 16, "bold") 
FONT_TREEVIEW_ROW = (FALLBACK_FONT_FAMILY, 14)   

COLOR_BACKGROUND = "#F0F4F8"
COLOR_PRIMARY = "#4A90E2"
COLOR_CLICK = "#6BA8ED"
COLOR_TEXT = "#333333"
COLOR_HEADER_TEXT = "#1A202C"
COLOR_ERROR = "#E74C3C"
COLOR_SUCCESS = "#2ECC71"

# Widget Configuration
COMMON_BUTTON_CONFIG = {
    "font": FONT_BUTTON,
    "bg": COLOR_PRIMARY,
    "fg": "white",
    "activebackground": COLOR_CLICK,
    "activeforeground": "white",
    "relief": "raised",
    "bd": 2
}

COMMON_BACK_BUTTON_CONFIG = {
    "font": FONT_BUTTON,
    "bg": COLOR_PRIMARY,
    "fg": "white",
    "activebackground": COLOR_CLICK,
    "activeforeground": "white",
    "relief": "raised",
    "bd": 2
}

COMMON_LABEL_CONFIG = {
    "font": FONT_LABEL,
    "fg": COLOR_TEXT,
    "bg": COLOR_BACKGROUND
}

COMMON_HEADING_CONFIG = {
    "font": FONT_SUBHEADING,
    "fg": COLOR_HEADER_TEXT,
    "bg": COLOR_BACKGROUND
}

COMMON_ENTRY_CONFIG = {
    "font": FONT_ENTRY,
    "relief": "solid",
    "bd": 1
}

# Models (Classes)
class Product:
    def __init__(self, id, name, price, stock):
        if not all([isinstance(id, str), isinstance(name, str)]):
            raise TypeError("Product ID and name must be strings.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Product price must be a positive number.")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("Product stock must be a non-negative integer.")
        self.id = id.strip().upper()
        self.name = name.strip()
        self.price = float(f"{price:.2f}")
        self.stock = stock

class CartItem:
    def __init__(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise TypeError("CartItem product must be an instance of Product.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("CartItem quantity must be a positive integer.")
        self.product = product
        self.quantity = quantity

    def total_price(self):
        return self.product.price * self.quantity

# GUI Application
class OnlineCartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ADH Cart - Online Shopping System") # Changed title
        self.configure(bg=COLOR_BACKGROUND)
        self.geometry("1200x800")
        self.bind('<Escape>', self._toggle_fullscreen)

        self._configure_styles()

        self.products = [
            Product("P001", "Laptop", 80000.00, 15),
            Product("P002", "Mouse", 2500.00, 50),
            Product("P003", "Keyboard", 3400.00, 30),
            Product("P004", "Monitor", 15000.00, 15),
            Product("P005", "Webcam", 1700.00, 20),
            Product("P006", "Smart Watch", 2300.00, 20),
            Product("P007", "Speaker", 6000.00, 15),
            Product("P008", "Mobile Phone", 25000.00,30),
            Product("P009", "Power Bank", 1200.00, 15),
            Product("P010","Sony Camera", 65000.00, 10)
        ]
        self.cart = []

        self._current_frame = None
        self._fullscreen_state = False
        self._create_main_menu()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=FONT_TREEVIEW_HEADER, background=COLOR_PRIMARY, foreground="white")
        style.configure("Treeview", font=FONT_TREEVIEW_ROW, rowheight=30, background=COLOR_BACKGROUND, foreground=COLOR_TEXT, fieldbackground=COLOR_BACKGROUND) # rowheight
        style.map('Treeview', background=[('selected', COLOR_PRIMARY)])

    def _toggle_fullscreen(self, event=None):
        self._fullscreen_state = not self._fullscreen_state
        self.attributes('-fullscreen', self._fullscreen_state)

    def _show_frame(self, frame_class, *args, **kwargs):
        if self._current_frame:
            self._current_frame.destroy()
        self._current_frame = frame_class(self, self, *args, **kwargs)
        self._current_frame.pack(fill="both", expand=True)

    def _get_product_by_id(self, product_id):
        for p in self.products:
            if p.id == product_id.strip().upper():
                return p
        return None

    # Logic
    def display_products(self): self._show_frame(ProductDisplayFrame)
    def add_to_cart(self): self._show_frame(AddToCartFrame)
    def view_cart(self): self._show_frame(CartDisplayFrame)
    def update_cart_item(self): self._show_frame(UpdateCartItemFrame)
    
    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Checkout", "Your cart is empty. Nothing to checkout.")
            return

        confirm = messagebox.askyesno("Checkout Confirmation",
                                      "Proceed with checkout?\n\n" +
                                      self._get_cart_summary_text() +
                                      f"\n\nFinal Total: ₹{sum(item.total_price() for item in self.cart):.2f}")
        if confirm:
            messagebox.showinfo("Checkout", "Order placed successfully!\nThank you for shopping with us. ~ ADH Cart") # Changed text
            self.cart = []
        else:
            messagebox.showinfo("Checkout", "Checkout cancelled.")
        self._create_main_menu()

    def _get_cart_summary_text(self):
        if not self.cart: return "Your cart is empty."
        summary = "Your Shopping Cart:\n"
        for i, item in enumerate(self.cart):
            summary += f"{i+1}. {item.product.name} (Qty: {item.quantity}) - ₹{item.total_price():.2f}\n"
        return summary.strip()

   
    # Frame
    def _create_main_menu(self): self._show_frame(MainMenuFrame)


class BaseFrame(tk.Frame):
    def __init__(self, parent, app_instance, title_text=None):
        super().__init__(parent, bg=COLOR_BACKGROUND)
        self.app = app_instance
        if title_text:
            tk.Label(self, text=title_text, **COMMON_HEADING_CONFIG).pack(pady=20)

    def _create_back_button(self, command=None, text="Back to Main Menu", pady=30):
        if command is None:
            command = self.app._create_main_menu
        tk.Button(self, text=text, command=command, **COMMON_BACK_BUTTON_CONFIG).pack(pady=pady)

    def _create_treeview(self, parent_frame, columns, data, column_widths, headings, scrollbar_on_right=True):
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings")
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading["text"], anchor=heading["anchor"])
            tree.column(col, width=column_widths.get(col, 100), anchor=heading.get("anchor", tk.W), stretch=heading.get("stretch", tk.YES))
        for row_data in data:
            tree.insert("", tk.END, values=row_data)

        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        if scrollbar_on_right:
            vsb.pack(side="right", fill="y")
            tree.pack(side="left", fill="both", expand=True)
        else:
            tree.pack(fill="both", expand=True)
            vsb.pack(fill="y")
        return tree


class MainMenuFrame(BaseFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, app_instance)
        tk.Label(self, text="ADH Cart", font=FONT_HEADING, fg=COLOR_HEADER_TEXT, bg=COLOR_BACKGROUND).pack(pady=(40, 20)) # Changed text

        button_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        button_frame.pack(pady=20)

        buttons_data = [
            ("View Products", self.app.display_products),
            ("Add to Cart", self.app.add_to_cart),
            ("View Cart", self.app.view_cart),
            ("Update Cart", self.app.update_cart_item),
            ("Checkout", self.app.checkout),
            ("Exit", self.app.destroy)
        ]

        for text, command in buttons_data:
            tk.Button(button_frame, text=text, command=command, width=25, height=2, **COMMON_BUTTON_CONFIG).pack(pady=10)

        tk.Label(self, text="Welcome to ADH Cart !", font=FONT_SUBHEADING, fg=COLOR_TEXT, bg=COLOR_BACKGROUND).pack(pady=(20, 40)) # Changed text


class ProductDisplayFrame(BaseFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, app_instance, title_text="Available Products")

        if not self.app.products:
            tk.Label(self, text="No products available.", **COMMON_LABEL_CONFIG).pack(pady=10)
        else:
            tree_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
            tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

            columns = ("ID", "Name", "Price", "Stock")
            headings = [
                {"text": "ID", "anchor": tk.CENTER, "stretch": tk.NO},
                {"text": "Name", "anchor": tk.W},
                {"text": "Price", "anchor": tk.E, "stretch": tk.NO},
                {"text": "Stock", "anchor": tk.CENTER, "stretch": tk.NO}
            ]
            column_widths = {"ID": 70, "Name": 250, "Price": 120, "Stock": 80}
            data = [(p.id, p.name, f"₹{p.price:.2f}", p.stock) for p in self.app.products]

            self._create_treeview(tree_frame, columns, data, column_widths, headings)

        self._create_back_button()


class AddToCartFrame(BaseFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, app_instance, title_text="Add Product to Cart")

        self._create_product_list_treeview()

        input_section_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        input_section_frame.pack(pady=20)

        tk.Label(input_section_frame, text="Product ID:", **COMMON_LABEL_CONFIG).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.product_id_entry = tk.Entry(input_section_frame, width=25, **COMMON_ENTRY_CONFIG)
        self.product_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(input_section_frame, text="Quantity:", **COMMON_LABEL_CONFIG).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.quantity_entry = tk.Entry(input_section_frame, width=25, **COMMON_ENTRY_CONFIG)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self, text="Add to Cart", command=self._add_to_cart_action, **COMMON_BUTTON_CONFIG).pack(pady=10)
        self._create_back_button(pady=5)

    def _create_product_list_treeview(self):
        if not self.app.products:
            tk.Label(self, text="No products available to add.", **COMMON_LABEL_CONFIG).pack(pady=5)
            return

        tree_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("ID", "Name", "Price", "Stock")
        headings = [
            {"text": "ID", "anchor": tk.CENTER, "stretch": tk.NO},
            {"text": "Name", "anchor": tk.W},
            {"text": "Price", "anchor": tk.E, "stretch": tk.NO},
            {"text": "Stock", "anchor": tk.CENTER, "stretch": tk.NO}
        ]
        column_widths = {"ID": 70, "Name": 250, "Price": 120, "Stock": 80}
        data = [(p.id, p.name, f"₹{p.price:.2f}", p.stock) for p in self.app.products]

        self._create_treeview(tree_frame, columns, data, column_widths, headings)

    def _add_to_cart_action(self):
        product_id = self.product_id_entry.get().strip().upper()
        quantity_str = self.quantity_entry.get().strip()

        if not product_id or not quantity_str:
            messagebox.showerror("Input Error", "Please enter both Product ID and Quantity.")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a positive whole number.")
            return

        product_found = self.app._get_product_by_id(product_id)
        if not product_found:
            messagebox.showerror("Error", f"Product with ID '{product_id}' not found.")
            return
        if product_found.stock == 0:
            messagebox.showinfo("Out of Stock", f"Sorry, '{product_found.name}' is out of stock.")
            return

        # Check existing quantity in cart
        existing_cart_item = next((item for item in self.app.cart if item.product.id == product_id), None)
        current_cart_quantity = existing_cart_item.quantity if existing_cart_item else 0
        total_requested_quantity = current_cart_quantity + quantity

        if total_requested_quantity > product_found.stock + current_cart_quantity:
            messagebox.showerror("Not Enough Stock", f"Error: Only {product_found.stock} of '{product_found.name}' available (already {current_cart_quantity} in cart).")
            return

        if existing_cart_item:
            existing_cart_item.quantity += quantity
        else:
            self.app.cart.append(CartItem(product_found, quantity))

        product_found.stock -= quantity
        messagebox.showinfo("Success", f"'{quantity}' of '{product_found.name}' added to cart.")
        self.product_id_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.app._show_frame(AddToCartFrame)


class CartDisplayFrame(BaseFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, app_instance, title_text="Your Shopping Cart")

        if not self.app.cart:
            tk.Label(self, text="Your cart is empty.", **COMMON_LABEL_CONFIG).pack(pady=10)
        else:
            cart_tree_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
            cart_tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

            columns = ("Product", "Quantity", "Price/Item", "Subtotal")
            headings = [
                {"text": "Product", "anchor": tk.W},
                {"text": "Qty", "anchor": tk.CENTER},
                {"text": "Price/Item", "anchor": tk.E},
                {"text": "Subtotal", "anchor": tk.E}
            ]
            column_widths = {"Product": 250, "Quantity": 80, "Price/Item": 120, "Subtotal": 120}

            total_cart_price = 0
            data = []
            for item in self.app.cart:
                data.append((item.product.name, item.quantity, f"₹{item.product.price:.2f}", f"₹{item.total_price():.2f}"))
                total_cart_price += item.total_price()

            self._create_treeview(cart_tree_frame, columns, data, column_widths, headings)
            tk.Label(self, text=f"Total Cart Value: ₹{total_cart_price:.2f}", **COMMON_HEADING_CONFIG).pack(pady=20)

        self._create_back_button()

class UpdateCartItemFrame(BaseFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, app_instance, title_text="Update Cart Item Quantity")

        self.cart_tree_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        self.cart_tree_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self._populate_cart_tree()

        input_section_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        input_section_frame.pack(pady=20)

        tk.Label(input_section_frame, text="Enter item number:", **COMMON_LABEL_CONFIG).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.item_number_entry = tk.Entry(input_section_frame, width=20, **COMMON_ENTRY_CONFIG)
        self.item_number_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(input_section_frame, text="New Quantity:", **COMMON_LABEL_CONFIG).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.new_quantity_entry = tk.Entry(input_section_frame, width=20, **COMMON_ENTRY_CONFIG)
        self.new_quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self, text="Update Quantity", command=self._update_quantity_action, **COMMON_BUTTON_CONFIG).pack(pady=10)
        self._create_back_button(pady=5)

    def _populate_cart_tree(self):
        for widget in self.cart_tree_frame.winfo_children(): widget.destroy()

        if not self.app.cart:
            tk.Label(self.cart_tree_frame, text="Your cart is empty. Nothing to update.", **COMMON_LABEL_CONFIG).pack(pady=10)
            return

        columns = ("Index", "Product", "Current Quantity", "Price/Item", "Subtotal")
        headings = [
            {"text": "#", "anchor": tk.CENTER, "stretch": tk.NO},
            {"text": "Product", "anchor": tk.W},
            {"text": "Current Qty", "anchor": tk.CENTER},
            {"text": "Price/Item", "anchor": tk.E},
            {"text": "Subtotal", "anchor": tk.E}
        ]
        column_widths = {"Index": 50, "Product": 200, "Current Quantity": 100, "Price/Item": 100, "Subtotal": 100}
        data = [(i+1, item.product.name, item.quantity, f"₹{item.product.price:.2f}", f"₹{item.total_price():.2f}") for i, item in enumerate(self.app.cart)]

        self.cart_tree = self._create_treeview(self.cart_tree_frame, columns, data, column_widths, headings)
        self.cart_tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _on_tree_select(self, event):
        selected_items = self.cart_tree.selection()
        if selected_items:
            item_index = int(selected_items[0])
            self.item_number_entry.delete(0, tk.END)
            self.item_number_entry.insert(0, str(item_index + 1))
            # Also populate current quantity for convenience
            current_quantity = self.app.cart[item_index].quantity
            self.new_quantity_entry.delete(0, tk.END)
            self.new_quantity_entry.insert(0, str(current_quantity))

    def _update_quantity_action(self):
        item_number_str = self.item_number_entry.get().strip()
        new_quantity_str = self.new_quantity_entry.get().strip()

        if not item_number_str or not new_quantity_str:
            messagebox.showerror("Input Error", "Please enter both item number/selection and new quantity.")
            return

        try:
            item_index = int(item_number_str) - 1 # Convert to 0-based index
            new_quantity = int(new_quantity_str)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Item number and quantity must be whole numbers.")
            return

        if not (0 <= item_index < len(self.app.cart)):
            messagebox.showerror("Invalid Item", "Invalid item number.")
            return

        cart_item = self.app.cart[item_index]
        product = cart_item.product
        old_quantity = cart_item.quantity

        if new_quantity < 0:
            messagebox.showerror("Invalid Quantity", "Quantity cannot be negative.")
            return

        if new_quantity == old_quantity:
            messagebox.showinfo("No Change", "Quantity is already the same.")
            return
        elif new_quantity == 0:
            # Remove item from cart
            self.app.cart.pop(item_index)
            product.stock += old_quantity
            messagebox.showinfo("Success", f"'{product.name}' removed from cart.")
        elif new_quantity > old_quantity:
            # Increase quantity
            quantity_to_add = new_quantity - old_quantity
            if quantity_to_add > product.stock:
                messagebox.showerror("Not Enough Stock", f"Error: Only {product.stock} more of '{product.name}' available. Cannot increase to {new_quantity}.")
                return
            cart_item.quantity = new_quantity
            product.stock -= quantity_to_add
            messagebox.showinfo("Success", f"Quantity of '{product.name}' updated to {new_quantity}.")
        else: # new_quantity < old_quantity
            # Decrease quantity
            quantity_to_remove = old_quantity - new_quantity
            cart_item.quantity = new_quantity
            product.stock += quantity_to_remove
            messagebox.showinfo("Success", f"Quantity of '{product.name}' updated to {new_quantity}.")

        # Refresh the frame to reflect changes
        self.app._show_frame(UpdateCartItemFrame)

# Main Execution
if __name__ == "__main__":
    app = OnlineCartApp()
    app.mainloop()