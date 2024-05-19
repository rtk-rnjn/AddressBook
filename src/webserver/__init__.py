from __future__ import annotations

from flask import Flask, redirect, render_template, url_for

from src.address import Address, AddressBook, AddressDict
from src.webserver.forms import AddressForm

app = Flask(__name__)
app.secret_key = "secret_key"

book = AddressBook.from_file(r"src/address/address_book.json")


@app.route("/")
def index():
    return render_template("index.html", address_book=book)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddressForm()
    if form.validate_on_submit():
        data: AddressDict = form.data
        book.add_address(Address(**data))
        book.to_file()

        return redirect(url_for("index"))

    return render_template("add.html", form=form)


@app.route("/delete/<address_id>", methods=["GET"])
def delete(address_id):
    for address in book:
        if address.id == address_id:
            book.remove_address(address)
            return redirect(url_for("index"))

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
