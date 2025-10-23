import sqlite3

conn = sqlite3.connect("autos.db")
c = conn.cursor()

with conn:
    c.execute("""
        CREATE TABLE IF NOT EXISTS autos (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            color TEXT,
            year INTEGER,
            price INTEGER
        )
    """)

while True:
    choice = int(input("1 - ieškoti, 2 - įvesti, 3 - peržiūrėti, 0 - išeiti: "))
    match choice:
        case 1:
            make = input("Make: ")
            model = input("Model: ")
            color = input("Color: ")
            year_from = input("Year from: ")
            year_to = input("Year to: ")
            price_from = input("Price from: ")
            price_to = input("Price to: ")
            search_tuple = (
                make if make else "%",
                model if model else "%",
                color if color else "%",
                int(year_from) if year_from else 1900,
                int(year_to) if year_to else 2300,
                int(price_from) if price_from else 0,
                int(price_to) if price_to else 10000000,
            )
            with conn:
                c.execute("""SELECT * FROM autos
                WHERE
                make LIKE ? AND
                model LIKE ? AND
                color LIKE ? AND
                year BETWEEN ? AND ? AND
                price BETWEEN ? AND ? 
                """, search_tuple)
                cars = c.fetchall()
                print("Rasti automobiliai:")
                for car in cars:
                    print(f"{str(car[0]).zfill(4)}. {car[4]} m. {car[1]} {car[2]} ({car[3]}) - {car[5]} Eur")

        case 2:
            make = input("Make: ")
            model = input("Model: ")
            color = input("Color: ")
            year = int(input("Year: "))
            price = int(input("Price: "))
            try:
                with conn:
                    c.execute("INSERT INTO autos VALUES (NULL, ?, ?, ?, ?, ?)", (make, model, color, year, price))
                print("Automobilis pridėtas")
            except:
                print("Nepavyko pridėti")
        case 3:
            with conn:
                c.execute("SELECT * FROM autos")
                cars = c.fetchall()
                for car in cars:
                    print(f"{str(car[0]).zfill(4)}. {car[4]} m. {car[1]} {car[2]} ({car[3]}) - {car[5]} Eur")
        case 0:
            print("Viso gero")
            break