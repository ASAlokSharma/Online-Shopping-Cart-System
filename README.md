## About the System

ADH Cart - Online Shopping System ADH Cart is a simple, intuitive desktop application that simulates a basic online shopping experience. Built using Python's Tkinter, it allows users to browse a list of products, add them to a shopping cart, update quantities, and proceed through a simulated checkout process.

✨ Features Product Catalog: View a list of available products with their IDs, names, prices, and current stock levels.

Add to Cart: Easily add desired products to your shopping cart by specifying the Product ID and quantity.

View Cart: See all items currently in your cart, including quantities, individual prices, and subtotal for each item. A grand total for the entire cart is also displayed.

Update Cart Items: Modify the quantity of existing items in your cart or remove them entirely.

Simulated Checkout: A simple checkout confirmation process.

Responsive UI: Basic responsive layout with a modern aesthetic, custom fonts, and color scheme.

Fullscreen Mode: Toggle fullscreen mode by pressing the Esc key.

🚀 Getting Started These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites You need to have Python installed on your system. This application uses tkinter, which is typically included with standard Python installations.

Python 3.x (preferably 3.7+)

Installation Clone the repository:

git clone https://github.com/ASAlokSharma/Online-Shopping-Cart-System.git cd Online-Shopping-Cart-System

Save the code: Copy the provided Python code into a file named main.py (or any other .py extension) inside the cloned directory.

Running the Application Open your terminal or command prompt, navigate to the directory where you saved main.py, and run:

python main.py

The application window should appear, presenting you with the main menu.

💻 Code Structure The application is structured into several classes for better organization:

Product: Represents a single product with id, name, price, and stock.

CartItem: Represents an item in the shopping cart, linking a Product with a quantity.

OnlineCartApp: The main Tkinter application class, handling overall flow, data (products, cart), and frame management.

BaseFrame: A foundational class for all application screens, providing common UI elements like a title and a "Back to Main Menu" button.

MainMenuFrame: Displays the main navigation options.

ProductDisplayFrame: Shows the list of all available products.

AddToCartFrame: Allows users to add products to the cart.

CartDisplayFrame: Displays the current contents of the shopping cart.

UpdateCartItemFrame: Enables updating quantities or removing items from the cart.

🎨 Customization You can easily customize the appearance and initial data of the application by modifying the constants at the top of the main.py file:

Fonts: FONT_FAMILY, FALLBACK_FONT_FAMILY, FONT_HEADING, FONT\_SUBHEADING, etc.

Colors: COLOR_BACKGROUND, COLOR_PRIMARY, COLOR\_TEXT, etc.

Widget Configurations: COMMON_BUTTON_CONFIG, COMMON_LABEL_CONFIG, etc.

Initial Products: Modify the self.products list within the OnlineCartApp's **init** method to change the available products.

🤝 Contributing Contributions are welcome! If you have suggestions for improvements or find any issues, please open an issue or submit a pull request.

📄 License This project is licensed under the MIT License - see the LICENSE file (if applicable, you might want to create one) for details.

📧 Contact If you have any questions or feedback, feel free to reach out.

Developed with ❤️ for simple desktop shopping simulation.

## Skills Used

<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff"> 

## GitHub Stats

<table><tbody><tr border="none"><td width="50%" align="center">
<img align="center" src="https://readme-stats-fork-mauve.vercel.app/api/?username=ASAlokSharma&theme=dark&show_icons=true&count_private=true">

<img alt="Mark streak" src="https://github-readme-streak-stats-five-roan.vercel.app?user=ASAlokSharma&theme=dark"></td><td width="50%" align="center">
<img align="center" src="https://readme-stats-fork-mauve.vercel.app/api/top-langs/?username=ASAlokSharma&theme=dark&hide_border=false&no-bg=true&no-frame=true&langs_count=6"></td></tr></tbody></table>

## Connect with me

<p align="center">🔗 LinkedIn: <a href="www.linkedin.co/in/ASAlokSharma" target="_blank">Alok Sharma</a> Email: TVM.AaravSharma@outlook.com</p>
